# AiSuite-Core

---

This repository contains all the AI projects categorized based on the modules and learning purposes.

These projects should have the basic and core implementations which can be used by other projects.
It might be some of them use any third party library, so the source code available in this repository will be available 
for AS IT IS usage.


## Build Status


| Build | Tests | Pages |
|:------|:------|-------|
|       |       |       |



## Folder Structure Conventions

---

```
/
├── Core                        # The Core Project
└── README.md
```


## Building Application

---

### Local Development

#### Check ```Python``` settings

```shell
python3 --version
python3 -m pip --version
python3 -m ensurepip --default-pip
```

#### Setup a virtual environment

```
python3 -m pip install virtualenv
python3 -m venv venv
source deactivate
source venv/bin/activate
```

### Activate ```venv```

```source``` is Linux/macOS command and doesn't work in Windows.

- Windows

```shell
venv\Scripts\activate
```

- Mac OS/Linux

```shell
source venv/bin/activate

OR

. ./venv/bin/activate  
```

Output:

```
(venv) <UserName>@<HostName> PyTheorem %
```

The parenthesized ```(venv)``` in front of the prompt indicates that you’ve successfully activated the virtual
environment.

### Deactivate Virtual Env

```shell
deactivate
```

Output:

```
<UserName>@<HostName> PyTheorem %
```

### Upgrade ```pip``` release

```shell
pip install --upgrade pip
```

### Install Packages/Requirements (Dependencies)

- Install at the system level

```shell
brew install python-requests
```

- Install in specific Virtual Env

```shell
pip install requests
pip install beautifulsoup4
python -m pip install requests
```

### Install Requirements

```shell
pip install -r requirements.txt
```

### Save Requirements (Dependencies)

```shell
pip freeze > requirements.txt
```

### Build Python Project
```shell
python -m build
```

### Configuration Setup

Set a local configuration file.
Create or update local ```.env``` configuration file.

```shell
pip install python-dotenv
cp default.env .env
```

Now, update the default local configurations as follows:

```text
# App Configs
APP_HOST = 0.0.0.0
HOST = 0.0.0.0
APP_PORT = 8080
PORT = 8080
APP_ENV = develop
DEBUG = False

#
# Pool Configs
#
DEFAULT_POOL_SIZE = 1
RDS_POOL_SIZE = 1

#
# Logger Configs
#
LOG_FILE_NAME = 'AiSuite.log'

#
# Database Configs
#
DB_HOSTNAME = 127.0.0.1
DB_PORT =
DB_NAME = AiSuite
DB_USERNAME = AiSuite
DB_PASSWORD = AiSuite
```


**By default**, Flask will run the application on **port 5000**.

## Run Flask Application

```shell
python -m flask --app webapp run --port 8080 --debug
```


**By default**, Flask runs the application on **port 5000**.

```shell
python wsgi.py

OR

#flask --app wsgi run
python -m flask --app wsgi run
# http://127.0.0.1:5000/AiSuite

OR

python -m flask --app wsgi run --port 8080 --debug
# http://127.0.0.1:8080/AiSuite

OR

# Production Mode

# equivalent to 'from app import app'
gunicorn wsgi:app
# gunicorn -w <n> 'wsgi:app'
gunicorn -w 2 'wsgi:app'
# http://127.0.0.1:8000/AiSuite

gunicorn -c gunicorn.conf.py wsgi:app
# http://127.0.0.1:8080/AiSuite

```


**Note**:- You can stop the development server by pressing ```Ctrl+C``` in your terminal.

## Access Application

```shell
- [IWS on port 8080](http://127.0.0.1:8080/AiSuite)
- [IWS on port 8000](http://127.0.0.1:8000/AiSuite)
- [IWS on port 5000](http://127.0.0.1:5000/AiSuite)
```

## Testing

### Unit Tests

```shell
python -m unittest
python -m unittest discover -s ./aisuite/tests -p "test_*.py"
```

### Performance Testing

```shell
# Run this in a separate terminal
# so that the load generation continues and you can carry on with the rest of the steps
kubectl run -i --tty load-generator --rm --image=busybox:1.28 --restart=Never -- /bin/sh -c "while sleep 0.01; do wget -q -O- http://php-apache; done"
```

## Capacity Planning

### CPU Bound Systems

- Formula

```text
RPS = TotalCore * (1/TaskDurationInSeconds)

i.e.:
4 * (1000/100) = 40

```

| Total Cores | Task Duration | RPS |
|:-----------:|:--------------|:----|
|      4      | 100ms         | 40  |
|      4      | 50ms          | 80  |
|      4      | 10ms          | 400 |



# Reference

---



# Author

---

* [Rohtash Lakra](https://github.com/rslakra)



# License

---

This project is licensed under the Apache License - see the [LICENSE.md](https://github.com/rslakra/AiSuite/LICENSE.md)
file for details
