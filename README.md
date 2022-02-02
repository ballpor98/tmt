# TMT

TMT employee time clocking system, as a graphql service in Django

## Table of contents

- [TMT](#tmt)
    - [Table of contents](#table-of-contents)
    - [Installation](#installation)

## Installation

### Installation local

0. Install pyenv https://github.com/pyenv/pyenv  
   if you use macOS and zsh
    ```shell
    brew install pyenv
    eval "$(pyenv init -)"
    ```
1. Create virtualenv
    ```shell
    pyenv install 3.9.10
    pyenv shell 3.9.10
    python -m venv venv
    ```
2. Activate virtualenv
    ```shell
    source venv/bin/activate
    ```
3. Install python requirements
    ```shell
    pip install -r requirements.txt
    ```

### Installation docker

1. Build docker image
    ```shell
    docker compose build
    ```

## Run

### run on local

1. Set environment variable

```shell
export TMT_DJANGO_SECRET_KEY=django-insecure-secret-key
export DEBUG_MODE=True
```

2. Migrate django

```shell
python -m manage makemigrations
python -m manage migrate
```

2. Start service

```shell
source venv/bin/activate
python -m manage runserver
```

### run on docker

```shell
docker compose up
```

## Test

### service test

```shell
TMT_DJANGO_SECRET_KEY=some-key python -m manage test
```

### postman

https://kb.datamotion.com/?ht_kb=postman-instructions-for-exporting-and-importing