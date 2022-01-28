# TMT

TMT employee time clocking system, as a graphql service in Django

## Table of contents

- [TMT](#tmt)
  - [Table of contents](#table-of-contents)
  - [Installation](#installation)

## Installation

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
