# Download DM history from Slack

## Usage

You can run the application with the following command after installing it with pip or inside a virtual environment

```bash
python -m download_slack_dm_history.cli download_history --channel_id $CHANNEL_ID --token $TOKEN --output_file_path path/to/file
```

You can find the `$CHANNEL_ID` by navigating on the Slack web application and selecting the target direct message channel. You will find the channel id on the url : https://app.slack.com/client/WORKSPACE_ID/CHANNEL_ID

To generate an authentification token (`$TOKEN`), you need to [create a slack app](https://api.slack.com/apps), link it to your target workplace and add permissions. You will need to add a user token scope that will allow your app to "View messages and other content in direct messages that your slack app has been added to" ([im:history scope](https://api.slack.com/scopes/im:history)). You will then find an OAuth Access Token on the OAuth & Permissions section of your application. This is your `$TOKEN`.

## Developper guideline
Copied from https://github.com/FabienArcellier/blueprint-cli-multicommands-python

### Install pipenv

### Add a dependency

Write the dependency in ``setup.py``. As it's the distribution standard for pypi,
I prefer to keep ``setup.py`` as single source of truth.

I encourage avoiding using instruction as ``pipenv install requests`` to register
a new library. You would have to write your dependency in both ``setup.py`` and ``Pipfile``.

### Install development environment

Use make to instanciate a python virtual environment in ./venv and install the
python dependencies.

```bash
make install_requirements_dev
```

### Update release dependencies

Use make to instanciate a python virtual environment in ./venv and freeze
dependencies version on requirement.txt.

```bash
make update_requirements
```

### Activate the python environment

When you setup the requirements, a `venv` directory on python 3 is created.
To activate the venv, you have to execute :

```bash
make venv
source venv/bin/activate
```

### Run the linter and the unit tests

Before commit or send a pull request, you have to execute `pylint` to check the syntax
of your code and run the unit tests to validate the behavior.

```bash
make lint
make tests
```