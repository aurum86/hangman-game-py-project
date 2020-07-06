# The Hangman game

A conventional hangman game

[![Build Status](https://github.com/aurum86/hangman-game-py-project/workflows/Django%20CI/badge.svg)](https://github.com/aurum86/hangman-game-py-project)

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

# then click on the link provided in the terminal output
```
## Run in docker container
```
cd docker

docker-compose up
# then click on the link provided in the terminal output
```

## Run tests
```bash
cd hangman_project

# and then
pytest

# or
python manage.py test
```
### Run tests in docker container
```
cd docker

# build an image
docker build .. -f Dockerfile -t hangman_game:latest

# run tests in temporary container based on image given image
docker run -it --tty --rm hangman_game:latest sh -c 'pytest'
```

## Other useful commands

```bash
# run command in project shell
pipenv run SOME_COMMAND

# enter project shell
pipenv shell
```
