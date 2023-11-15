
## Useful info  

[we make python](https://readthedocs.org/projects/wemake-python-styleguide/) is the style guide that this project follows have a look at the [docs here](https://wemake-python-styleguide.readthedocs.io/en/latest/) for an explanation of their rules, some I have found to be contradictory with other tooling or excessively restrictive so I have disabled them



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