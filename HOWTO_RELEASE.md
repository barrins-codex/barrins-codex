# Release

To release the project, follow PyPa
[instructions](https://packaging.python.org/tutorials/packaging-projects/).

## Update your packages

```bash
python3 -m pip install --user --upgrade setuptools wheel
python3 -m pip install --user --upgrade twine
```

## Prepare the distribution
```bash
python3 setup.py sdist bdist_wheel
```

## Check release using [testpypi](https://test.pypi.org/):
```bash
python3 -m twine upload --repository testpypi dist/*
```
Check it works using the `pip` command prompted on the website.

## Final Release on [pypi](https://pypi.org/):
```bash
python3 -m twine upload dist/*
```

You can now install your project: `pip install project_name`!
