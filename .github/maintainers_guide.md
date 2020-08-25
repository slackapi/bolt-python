# Maintainers Guide

This document describes tools, tasks and workflow that one needs to be familiar with in order to effectively maintain
this project. If you use this package within your own software as is but don't plan on modifying it, this guide is
**not** for you.

## Tools

### Python (and friends)

We recommend using [pyenv](https://github.com/pyenv/pyenv) for Python runtime management. If you use macOS, follow the following steps:

```bash
$ brew update
$ brew install pyenv
```

Install necessary Python runtimes for development/testing. You can rely on Travis CI builds for testing with various major versions. https://github.com/slackapi/bolt-python/blob/main/.travis.yml

```bash
$ pyenv install -l | grep -v "-e[conda|stackless|pypy]"

$ pyenv install 3.8.5 # select the latest patch version
$ pyenv local 3.8.5

$ pyenv versions
  system
  3.6.10
  3.7.7
* 3.8.5 (set by /path-to-bolt-python/.python-version)

$ pyenv rehash
```

Then, you can create a new Virtual Environment this way:

```
$ python -m venv env_3.8.5
$ source env_3.8.5/bin/activate
```

### Additional settings for pip

pip 20.2 introduced a new flag to test the upcoming change: https://discuss.python.org/t/announcement-pip-20-2-release/4863/2
Turn on the feature on your local machine for testing it. Just running the following command helps you turn it on.

```bash
pip config set global.use-feature 2020-resolver
```

The following file should be generated.

```yaml
# ~/.config/pip/pip.conf
[global]
use-feature = 2020-resolver
```

## Tasks

### Testing

#### Run All the Unit Tests

If you make some changes to this SDK, please write corresponding unit tests as much as possible. You can easily run all the tests by running the following script

```bash
$ ./scripts/run_tests.sh
```

#### Run the Samples

If you make changes to `slack_bolt/adapter/*`, please verify if it surely works by running the apps under `samples` directory.

```bash
# Install all optional dependencies
$ pip install -e ".[adapter]"

# Set required env variables
$ export SLACK_SIGNING_SECRET=***
$ export SLACK_BOT_TOKEN=xoxb-***

# Standalone apps
$ cd samples/
$ python app.py
$ python async_app.py

# Flask apps
$ cd samples/flask
$ FLASK_APP=app.py FLASK_ENV=development flask run -p 3000

# In another terminal
$ ngrok http 3000 --subdomain {your-domain}
```

### Releasing

#### test.pypi.org deployment

##### $HOME/.pypirc

```
[testpypi]
username: {your username}
password: {your password}
```

##### Deployment

You can deploy a new version using `./scripts/deploy_to_test_pypi_org.sh`.

```bash
$ echo '__version__ = "{the version}"' > slack_bolt/version.py
$ ./scripts/deploy_to_test_pypi_org.sh
```

#### Production Deployment

1.  Create the commit for the release:

- Bump the version number in adherence to [Semantic Versioning](http://semver.org/) in `slack_bolt/version.py`
  - `echo '__version__ = "1.2.3"' > slack_bolt/version.py`
- Commit with a message including the new version number. For example `1.2.3` & Push the commit to a branch and create a PR to sanity check.
  - `git checkout -b v1.2.3-release`
  - `git commit -m'version 1.2.3'`
  - `git push {your-fork} v1.2.3-release`
- Merge in release PR after getting an approval from at least one maintainer.
- Create a git tag for the release. For example `git tag v1.2.3`.
- Push the tag up to github with `git push origin --tags`

2.  Distribute the release

- Use the latest stable Python runtime
- `python -m venv env`
- `./scripts/deploy_to_prod_pypi_org.sh`
- Create a GitHub release - https://github.com/slackapi/bolt-python/releases

```markdown
## New Features

### Awesome Feature 1

Description here.

### Awesome Feature 2

Description here.

## Changes

* #123 Make it better - thanks @SlackHQ
* #123 Fix something wrong - thanks @seratch
```

3. (Slack Internal) Communicate the release internally

- Include a link to the GitHub release

4. Make announcements

- #slack-api in dev4slack.slack.com
- #tools-bolt in community.slack.com

5. (Slack Internal) Tweet by @SlackAPI

- Not necessary for patch updates, might be needed for minor updates, definitely needed for major updates. Include a link to the GitHub release

## Workflow

### Versioning and Tags

This project uses semantic versioning, expressed through the numbering scheme of
[PEP-0440](https://www.python.org/dev/peps/pep-0440/).

### Branches

`main` is where active development occurs. Long running named feature branches are occasionally created for
collaboration on a feature that has a large scope (because everyone cannot push commits to another person's open Pull
Request). At some point in the future after a major version increment, there may be maintenance branches for older major
versions.

### Issue Management

Labels are used to run issues through an organized workflow. Here are the basic definitions:

- `bug`: A confirmed bug report. A bug is considered confirmed when reproduction steps have been
  documented and the issue has been reproduced.
- `enhancement`: A feature request for something this package might not already do.
- `docs`: An issue that is purely about documentation work.
- `tests`: An issue that is purely about testing work.
- `discussion`: An issue that is purely meant to hold a discussion. Typically the maintainers are looking for feedback in this issues.
- `question`: An issue that is like a support request because the user's usage was not correct.

**Triage** is the process of taking new issues that aren't yet "seen" and marking them with a basic level of information
with labels. An issue should have **one** of the following labels applied: `bug`, `enhancement`, `question`,
`needs feedback`, `docs`, `tests`, or `discussion`.

Issues are closed when a resolution has been reached. If for any reason a closed issue seems relevant once again,
reopening is great and better than creating a duplicate issue.

## Everything else

When in doubt, find the other maintainers and ask.
