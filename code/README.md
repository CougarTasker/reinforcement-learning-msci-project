

## Commands

These are the commands that should be executed in this current folder

Firstly run this command to install the libraries such as `kivy` that this project depends on
```Bash
poetry install
```

To run the project run:

```Bash
poetry run start
```

To view the documentation
```Bash 
python3 -m pydoc -p 3000 src
```


To run all linting and testing
```Bash
pre-commit run --all-files
```


To format the code run:
```Bash
poetry run black src
```

To run tests: 
```Bash
poetry run pytest --cov
```
To run linting
```Bash
poetry run flake8
poetry run mypy
```

To setup pre-commit hooks for code quality:
```Bash
poetry run pre-commit install
```