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

## Run
```bash
cd hangman_game

python manage.py runserver
```


## Other useful commands

```bash
# run command in project shell
pipenv run SOME_COMMAND

# enter project shell
pipenv shell
```