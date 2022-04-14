# A Simple Job Description Generator Using GPT-3 

This is a simple job description generator that uses a finetuned version of OpenAI's GPT-3 ([Brown et al.](https://arxiv.org/abs/2005.14165)). 


<sub><sub>Wrote in 2 hours. Quality not guaranteed.</sub></sub>

## Features:
- Automate job description writing with 2 lines of Python (install and run). 
- Specifically designed and finetuned GPT-3 for job description generation - no more copied data, and no more repeated nonsense.
- Accounts for all levels of needs: level of experience,
- Create your own template and specify what you need
- Prompt engineering tips
- A web app anyone can deploy and use for their own
- Better, newer, faster version and package control

## Installation:
### Before you start, make sure you have:
* OpenAI GPT-3 API key
* Python 3 (duh)
* `yarn` - installation instruction [here](https://classic.yarnpkg.com/en/docs/install/#mac-stable).

### Clone and cd into this repository, and:
1. Install required libraries: `pip install -r api/requirements.txt`
2. Place your API key: use `echo export OPENAI_API_KEY=[key] > .env` to create an environment file, where `[key]` is your OpenAI API key. 
3. Run `yarn install`
4. Run `python jd_generator_app.py` and have fun!

A new tab should pop up in your browser, and the webapp should be ready! 
To stop this app, run `ctrl-c` or `command-c` in your terminal.

## Reminder:
Please **do not** leave your API key in plaintext when you push this code online!
If you put it in a `.env` file, make sure it is included in your `.gitignore`!

### Windows users:
To run the webapp, you will need to modify `api/app.py`: 
change `subprocess.Popen(["yarn", "start"])` to `subprocess.Popen(["yarn", "start"], shell=True)`

## Tech Stack:
- Frontend: React
- Backend: Flask
- Language model: GPT-3 DaVinci

## Credits:
Inspired by [gpt-3 sandbox](https://github.com/shreyashankar/gpt3-sandbox).
