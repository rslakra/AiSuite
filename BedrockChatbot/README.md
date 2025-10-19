# Bedrock Chatbot

---


Building an AI chatbot library or SDK in Python for automobile usage is an exciting and complex project. This kind of
SDK would empower developers to integrate intelligent conversational interfaces directly into vehicle infotainment
systems, mobile companion apps, or even diagnostic tools.

The core idea is to create a Python package that can understand user queries related to automobiles, process them, and
generate relevant responses or trigger specific actions.

Here's a guide to help you structure such an SDK, along with key components and a simplified example using the Gemini
API for natural language generation.

## Project Structure

Although this layout is pretty straightforward, it has several drawbacks that arise as the app complexity increases.


```
    /
    ├── sdk                             # The Core SDK libary
    ├── iws                             # An internal web-service
    │    ├── config.py                  # contains the application configuration parameters.
    │    └── README.md                  # The README file of ews module
    ├── README.md                       # Instructions and helpful links
    └── robots.txt                      # tells which URLs the search engine crawlers can access on your site
```

## Local Development

### Check python settings

```shell
python3 --version
python3 -m pip --version
python3 -m ensurepip --default-pip
```

### Setup a virtual environment

```
python3 -m pip install virtualenv
python3 -m venv venv
source deactivate
source venv/bin/activate
```


### Install Requirements (Dependencies)

```
pip install --upgrade pip
python3 -m pip install -r requirements.txt
```


### Configuration Setup

Create or update local .env configuration file.

```shell
cp ./iws/default.env .env
OR
touch .env

#
# App Configs
#
FLASK_ENV = development
DEBUG = False
HOST = 127.0.0.1
PORT = 8080
#
# Pool Configs
#
DEFAULT_POOL_SIZE = 1
RDS_POOL_SIZE = 1
#
# Logger Configs
#
LOG_FILE_NAME = 'chatbot.log'
#
# Database Configs
#
DB_HOSTNAME = 127.0.0.1
DB_PORT =
DB_NAME = posts
DB_USERNAME = posts
DB_PASSWORD = Password
```

### Build Project

```shell
python3 -m build
```


### Save Requirements (Dependencies)

```shell
pip freeze > requirements.txt
```

## Testing

### Unit Tests

```shell
python3 -m unittest
python -m unittest discover -s ./tests -p "test_*.py"
```


# Reference


## AI Reference

https://platform.openai.com/docs/guides/text?api-mode=responses&prompt-example=prompt
https://repost.aws/questions/QUhLXxElk-Rm6FTkwkLdX9_w/how-to-correctly-build-up-a-conversation-using-the-invoke-api
https://repost.aws/questions/QUhLXxElk-Rm6FTkwkLdX9_w/how-to-correctly-build-up-a-conversation-using-the-invoke-api
https://dev.to/sunil_yaduvanshi/creating-your-own-chatbot-with-amazon-bedrock-api-gateway-and-lambda-aws-2n2e
https://medium.com/@harangpeter/setting-up-aws-bedrock-for-api-based-text-inference-dc25ab2b216b



# Author

- Rohtash Lakra
