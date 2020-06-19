# The Hangman game

A conventional hangman game

## Requirements
```bash
sudo apt-get install python3-pip python3-dev python3-venv python3.8-venv
```

## Setup

### setup the environment
```
pip install --user pipenv
```
**cd** to project dir
```
# initiate
# python3 will be used
pipenv install --three

pipenv install -r requirements.txt
```
## Setup project

```bash
python manage.py migrate
```

## Run
```bash
cd hangman_project

python manage.py runserver
```

## Run tests
```bash
cd hangman_project
pytest
```

## Other useful commands

```bash
# run command in project shell
pipenv run SOME_COMMAND

# enter project shell
pipenv shell
```