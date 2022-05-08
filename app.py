"""Runs the web app given a GPT object and UI configuration."""

from http import HTTPStatus
import json
import subprocess
import uuid
import openai

from flask import Flask, request, Response
from dotenv import load_dotenv
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

# Load .env file and get API key
load_dotenv()
key = os.getenv('OPENAI_API_KEY')

"""Finetunes GPT-3 with Example and GPT classes."""

class Example:
    """Stores an input, output pair and formats it to prime the model."""
    def __init__(self, inp, out):
        self.input = inp
        self.output = out
        self.id = uuid.uuid4().hex

    def get_input(self):
        """Returns the input of the example."""
        return self.input

    def get_output(self):
        """Returns the intended output of the example."""
        return self.output

    def get_id(self):
        """Returns the unique ID of the example."""
        return self.id

    def as_dict(self):
        return {
            "input": self.get_input(),
            "output": self.get_output(),
            "id": self.get_id(),
        }


class GPT:
    """The main class for a user to interface with the OpenAI API.

    A user can add examples and set parameters of the API request.
    """
    def __init__(self,
                 engine='davinci',
                 temperature=0.5,
                 max_tokens=100,
                 input_prefix="input: ",
                 input_suffix="\n",
                 output_prefix="output: ",
                 output_suffix="\n\n",
                 append_output_prefix_to_query=False):
        self.examples = {}
        self.engine = engine
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.input_prefix = input_prefix
        self.input_suffix = input_suffix
        self.output_prefix = output_prefix
        self.output_suffix = output_suffix
        self.append_output_prefix_to_query = append_output_prefix_to_query
        self.stop = (output_suffix + input_prefix).strip()

    def add_example(self, ex):
        """Adds an example to the object.

        Example must be an instance of the Example class.
        """
        assert isinstance(ex, Example), "Please create an Example object."
        self.examples[ex.get_id()] = ex

    def delete_example(self, id):
        """Delete example with the specific id."""
        if id in self.examples:
            del self.examples[id]

    def get_example(self, id):
        """Get a single example."""
        return self.examples.get(id, None)

    def get_all_examples(self):
        """Returns all examples as a list of dicts."""
        return {k: v.as_dict() for k, v in self.examples.items()}

    def get_prime_text(self):
        """Formats all examples to prime the model."""
        return "".join(
            [self.format_example(ex) for ex in self.examples.values()])

    def get_engine(self):
        """Returns the engine specified for the API."""
        return self.engine

    def get_temperature(self):
        """Returns the temperature specified for the API."""
        return self.temperature

    def get_max_tokens(self):
        """Returns the max tokens specified for the API."""
        return self.max_tokens

    def craft_query(self, prompt):
        """Creates the query for the API request."""
        q = self.get_prime_text(
        ) + self.input_prefix + prompt + self.input_suffix
        if self.append_output_prefix_to_query:
            q = q + self.output_prefix
        return q

    def submit_request(self, prompt):
        """Calls the OpenAI API with the specified parameters."""
        response = openai.Completion.create(engine=self.get_engine(),
                                            prompt=self.craft_query(prompt),
                                            max_tokens=self.get_max_tokens(),
                                            temperature=self.get_temperature(),
                                            top_p=1,
                                            n=1,
                                            stream=False,
                                            stop=self.stop)
        return response

    def get_top_reply(self, prompt):
        """Obtains the best result as returned by the API."""
        response = self.submit_request(prompt)
        return response['choices'][0]['text']

    def format_example(self, ex):
        """Formats the input, output pair."""
        return self.input_prefix + ex.get_input(
        ) + self.input_suffix + self.output_prefix + ex.get_output(
        ) + self.output_suffix


"""Class to store customized UI parameters."""
class UIConfig():
    """Stores customized UI parameters."""
    def __init__(self, description='Description',
                 button_text='Submit',
                 placeholder='Default placeholder',
                 show_example_form=False):
        self.description = description
        self.button_text = button_text
        self.placeholder = placeholder
        self.show_example_form = show_example_form

    def get_description(self):
        """Returns the input of the example."""
        return self.description

    def get_button_text(self):
        """Returns the intended output of the example."""
        return self.button_text

    def get_placeholder(self):
        """Returns the intended output of the example."""
        return self.placeholder

    def get_show_example_form(self):
        """Returns whether editable example form is shown."""
        return self.show_example_form

    def json(self):
        """Used to send the parameter values to the API."""
        return {"description": self.description,
                "button_text": self.button_text,
                "placeholder": self.placeholder,
                "show_example_form": self.show_example_form}


def run_app(gpt, config=UIConfig()):
    """Creates Flask app to serve the React app."""
    app = Flask(__name__)
    openai.api_key = key

    # GET params
    @app.route("/params", methods=["GET"])
    def get_params():
        response = config.json()
        return response

    def error(err_msg, status_code):
        return Response(json.dumps({"error": err_msg}), status=status_code)

    def get_example(example_id):
        """Gets a single example or all the examples."""
        # return all examples
        if not example_id:
            return json.dumps(gpt.get_all_examples())

        example = gpt.get_example(example_id)
        if not example:
            return error("id not found", HTTPStatus.NOT_FOUND)
        return json.dumps(example.as_dict())

    def post_example():
        """Adds an empty example."""
        new_example = Example("", "")
        gpt.add_example(new_example)
        return json.dumps(gpt.get_all_examples())

    def put_example(args, example_id):
        """Modifies an existing example."""
        if not example_id:
            return error("id required", HTTPStatus.BAD_REQUEST)

        example = gpt.get_example(example_id)
        if not example:
            return error("id not found", HTTPStatus.NOT_FOUND)

        if "input" in args:
            example.input = args["input"]
        if "output" in args:
            example.output = args["output"]

        # update the example
        gpt.add_example(example)
        return json.dumps(example.as_dict())

    def delete_example(example_id):
        """Deletes an example."""
        if not example_id:
            return error("id required", HTTPStatus.BAD_REQUEST)

        gpt.delete_example(example_id)
        return json.dumps(gpt.get_all_examples())

    @app.route(
        "/examples",
        methods=["GET", "POST"],
        defaults={"example_id": ""},
    )
    @app.route(
        "/examples/<example_id>",
        methods=["GET", "PUT", "DELETE"],
    )
    def examples(example_id):
        method = request.method
        args = request.json
        if method == "GET":
            return get_example(example_id)
        if method == "POST":
            return post_example()
        if method == "PUT":
            return put_example(args, example_id)
        if method == "DELETE":
            return delete_example(example_id)
        return error("Not implemented", HTTPStatus.NOT_IMPLEMENTED)

    # POST translate
    @app.route("/translate", methods=["GET", "POST"])
    def translate():
        prompt = request.json["prompt"]
        response = gpt.submit_request(prompt)
        offset = 0
        if not gpt.append_output_prefix_to_query:
            offset = len(gpt.output_prefix)
        return {'text': response['choices'][0]['text'][offset:]}

    subprocess.Popen(["yarn", "start"])
    app.run()

def main():
    gpt = GPT(temperature=0.7, max_tokens=500)
    gpt.add_example(Example(
        "Senior Software Engineer",
        "Description: \nWe are looking for a Senior Software Engineer to produce and implement functional software solutions. You will work with upper management to define software requirements and take the lead on operational and technical projects. In this role, you should be able to work independently with little supervision. You should have excellent organization and problem-solving skills. If you also have hands-on experience in software development and agile methodologies, we’d like to meet you. Your goal will be to develop high-quality software that is aligned with user needs and business goals.\n\nResponsibilities: \n• Develop high-quality software design and architecture\n• Identify, prioritize and execute tasks in the software development life cycle\n• Develop tools and applications by producing clean, efficient code\n• Automate tasks through appropriate tools and scripting\n• Review and debug code\n• Perform validation and verification testing\n• Collaborate with internal teams and vendors to fix and improve products\n• Document development phases and monitor systems\n• Ensure software is up-to-date with latest technologies\n\nRequirements: \n• Proven experience as a Senior Software Engineer\n• Extensive experience in software development, scripting and project management\n• Experience using system monitoring tools (e.g. New Relic) and automated testing frameworks\n• Knowledge of selected programming languages (e.g. Python, C++) and the Java/J2EE platform\n• In-depth knowledge of relational databases (e.g. PostgreSQL, MySQL) and NoSQL databases (e.g. MongoDB)\n• Familiarity with various operating systems (Linux, Mac OS, Windows)\n• Analytical mind with problem-solving aptitude\n• Ability to work independently\n• Excellent organizational and leadership skills\n• BSc/BA in Computer Science or a related degree"
    ))
    gpt.add_example(Example(
        "Associate Product Manager",
        "Description: \nWe are looking for an experienced Associate Product Manager to participate in the creation of new products and features, from the idea stage to launch. To be successful in this role, you should have previous experience in end-to-end project management. Your main responsibilities include gathering product requirements, prioritizing feature implementations and improving overall user experience. Our ideal candidates should combine technical background with a Business Administration or Marketing degree. Ultimately, you’ll work with internal teams to build products that fill gaps in market and increase customer satisfaction.\n\nResponsibilities: \n• Suggest product enhancements to improve user experience\n• Perform quality assurance controls on products\n• Coordinate with the engineering department to deliver functional solutions\n• Conduct research to identify customer needs and market gaps\n• Prioritize the implementation of new features and set specific timelines\n• Liaise with the Marketing department to ensure proper advertisement and positioning of new products\n• Monitor and report on users’ reactions after launching\n• Create support and training documents for internal and external users\n• Participate in system configuration\n• Analyze competition \n\nRequirements: \n• Previous work experience as an Associate Product Manager, Product Marketing Manager or similar role\n• Experience managing the entire product lifecycle\n• Familiarity with market research, consumers’ behavior and marketing techniques\n• Hands-on experience with web technologies\n• Knowledge of project management tools, like Jira or Trello\n• Strong time management skills\n• Good communication skills along with the ability to effectively collaborate with cross functional teams\n• BSc in Business Administration, Marketing or similar field"
    ))
    config = UIConfig(description= "Generate Job Descriptions",
                      button_text= "Generate!",
                      placeholder= "Senior Software Engineer",
                      show_example_form=False)
    
    run_app(gpt, config)

if __name__ == "__main__":
    main()
