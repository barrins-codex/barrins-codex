# barrins-codex
A website about MtG Duel Strategy

## Installation

To install a working developpment version of the site, use `pip`:

```bash
python3 -m venv venv
pip install -e ".[dev]"
```

## Release

To release the project, follow PyPa
[instructions](https://packaging.python.org/tutorials/packaging-projects/).

First, check you have the latest version of those packages:
```bash
python3 -m pip install --user --upgrade setuptools wheel
python3 -m pip install --user --upgrade twine
```

Then, prepare de distribution:
```bash
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository testpypi dist/*
```

Then, test the release with [testpypi](https://test.pypi.org/):
```bash
python3 -m twine upload --repository testpypi dist/*
```

Check it works using the `pip` command prompted on the website.

If everything is fine, you can release the project on
[pypi](https://pypi.org/):
```bash
python3 -m twine upload dist/*
```

You can now install your project: `pip install project_name`!
