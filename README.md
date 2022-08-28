# Barrin's Codex
[![License](https://img.shields.io/badge/License-MIT-blue)](https://opensource.org/licenses/MIT)
[![Python version](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org/downloads/)
[![Validation](https://github.com/Spigushe/barrins-codex/actions/workflows/static.yml/badge.svg)](https://github.com/Spigushe/barrins-codex/actions/workflows/static.yml)
[![PyPI version](https://badge.fury.io/py/barrins-codex.svg)](https://badge.fury.io/py/barrins-codex)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)

A website about MtG Duel Commander Strategy

## Special Thanks
I started working with [lionel-panhaleux](https://github.com/lionel-panhaleux)
on a project during first lockdown (around April 2020). We worked on his
[Codex of the Damned](https://codex-of-the-damned.org/)
([repo](https://github.com/lionel-panhaleux/codex-of-the-damned)) to support
internationalisation. The whole structure of this project is derived from his
Codex, hence the name as a small tribute.

## Contributing
Contributions are welcome.
- [Pull Requests](https://github.com/Spigushe/barrins-codex/pulls) will be merged if they respect the general style.
- [Issues](https://github.com/Spigushe/barrins-codex/issues) will be dealt with as quickly as possible.

This site uses [Flask](https://flask.palletsprojects.com) to generate pages
dynamically .

## Installation
To install a working developpment version of the site, use `pip`:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

## Run the Codex
You can run the development version of the site using the `codex` entrypoint:

```bash
$ codex
* Serving Flask app "barrins_codex" (lazy loading)
* Environment: production
  WARNING: This is a development server. Do not use it in a production deployment.
  Use a production WSGI server instead.
* Debug mode: off
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

The Makefile has a command to start codex in debug : `make codex`

## Versioning
The version number take the form X.Y.Z where X, Y, and Z are non-negative
integers, and do not contain leading zeroes. X is the major version, Y is the
minor version, and Z is the patch version. Each element MUST increase
numerically. For instance: `1.9.0` -> `1.10.0` -> `1.11.0`.

Given a version number MAJOR.MINOR.PATCH, I increment the:
1. MAJOR version when I make a backend evolution or a design evolution,
1. MINOR version when I add content (most likely a match), and
1. PATCH version when I make bug and typo fixes.

Additional labels for pre-release and build metadata are available as
extensions to the MAJOR.MINOR.PATCH format.
