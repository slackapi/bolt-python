# Getting Started with The Project

## Python Runtime Management

We recommend using pyenv for Python runtime management.

https://github.com/pyenv/pyenv

If you use macOS, follow the following steps:

```bash
$ brew update
$ brew install pyenv
```

Then, install Python runtimes for this project:

```bash
$ pyenv install -l | grep -v "-e[conda|stackless|pypy]"

$ pyenv install 3.8.5
$ pyenv local 3.8.5

$ pyenv versions
  system
  3.6.10
  3.7.7
* 3.8.5 (set by /path-to-bolt-python/.python-version)

$ pyenv rehash
```

## Create a Virtual Environment

```
$ python -m venv env_3.8.5
$ source env_3.8.5/bin/activate
```

## Run All the Tests

```bash
$ pip install -U pip
$ python setup.py test # or ./scripts/run_tests.sh
```

# Run the Samples

```bash
# Install all optional dependencies
$ pip install -e ".[adapter]"

$ cd samples/
$ export SLACK_SIGNING_SECRET=***
$ export SLACK_BOT_TOKEN=xoxb-***
$ python app.py

# In another terminal
$ ngrok http 3000 --subdomain {your-domain}
```

# Deploying to test.pypi.org

## $HOME/.pypirc

```
[testpypi]
username: {your username}
password: {your password}
```

## Run the Script

```bash
$ echo '__version__ = "{the version}"' > slack_bolt/version.py
$ ./scripts/deploy_to_test_pypi_org.sh
```
