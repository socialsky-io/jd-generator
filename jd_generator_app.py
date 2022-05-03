import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from app import run_app, GPT, Example, UIConfig

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
