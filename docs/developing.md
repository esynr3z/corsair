# Developing

## Code style

[PEP 8 Speaks](https://github.com/OrkoHunter/pep8speaks) is added to automatically review Python code style over Pull Requests.

* Linter: pycodestyle
* Max line length: 120
* Errors and warnings to ignore: W504, E402, E731, C406, E741

## Testing

Install pytest

```
python3 -m pip install pytest
```

Run tests from the root folder:

```
pytest -v
```