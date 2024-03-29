# A Simple Job Description Generator Using GPT-3 

This is a simple job description generator that uses a finetuned version of OpenAI's GPT-3 ([Brown et al.](https://arxiv.org/abs/2005.14165)). 


<sub><sub>Wrote in 2 hours. Quality not guaranteed.</sub></sub>

## Features:
- A web app that anyone can deploy and use for their own, even on a raspberry pi
- Automate job description writing with just 2 lines of Python (pip install and run) 
- Specifically designed and finetuned GPT-3 for job description generation - no more copied training data and no more repeated nonsense
- Accounts for all levels of needs: level of experience, skills, education, location and more
- Option to create your own examples and specify what you want
- Faster, newer, and better version and package control

## Demo:
![demo](https://github.com/Cveinnt/jd-generator/blob/main/demo.gif)

### Upcoming:
- Prompt engineering tips
- UI fixes

## Installation:
### Before you start, make sure you have:
* OpenAI GPT-3 API key
* Python 3
* `yarn` - [installation](https://classic.yarnpkg.com/en/docs/install).

### Clone and cd into this repository, and:
1. Install python libraries: `pip install -r requirements.txt`
2. Place your API key: use `echo export OPENAI_API_KEY=[key] > .env` to create an environment file, where `[key]` is your OpenAI API key. 
3. Run `yarn install`
4. Run `python3 app.py` and have fun!

A new tab should pop up in your browser, and the webapp should be ready! 
To stop this app, run `ctrl-c` or `command-c` in your terminal.

## Reminder:
Please **do not** leave your API key in text file when you push this code online!
If you put it in a `.env` file, make sure it is included in your `.gitignore`!

## Tech stack:
- Frontend: React.js
- Backend: Flask 
- Language model: GPT-3 DaVinci

## Credits:
Inspired by [gpt-3 sandbox](https://github.com/shreyashankar/gpt3-sandbox).
