Contributing
============


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

```sh
python3 -m pip install -U corsair
```

(**NOT IMPLEMENTED YET**) You can install the latest development version from GitHub:

```sh
python3 -m pip install -U git+https://github.com/esynr3z/corsair.git
```

You can clone GitHub repository and run application from the project root:

```sh
git clone https://github.com/esynr3z/corsair.git
cd corsair
python3 -m corsair --help
```


pip3 install sphinx sphinx_rtd_theme --user
