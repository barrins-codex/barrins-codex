# Barrin's Codex
[![PyPI version](https://badge.fury.io/py/barrins-codex.svg)](https://badge.fury.io/py/barrins-codex)
[![Validation](https://github.com/Spigushe/barrins-codex/actions/workflows/static.yml/badge.svg)](https://github.com/Spigushe/barrins-codex/actions/workflows/static.yml)
[![Python version](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-blue)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

A website about MtG Duel Commander Strategy

## Special Thanks
I started working with [lionel-panhaleux](https://github.com/lionel-panhaleux) on a project during first lockdown (around April 2020).
We worked on his [Codex of the Damned](https://codex-of-the-damned.org/) ([repo](https://github.com/lionel-panhaleux/codex-of-the-damned)) to support internationalisation.
The whole structure of this project is derived from his Codex, hence the name as a small tribute.

## Contributing
Contributions are welcome.
- [Pull Requests](https://github.com/Spigushe/barrins-codex/pulls) will be merged if they respect the general style.
- [Issues](https://github.com/Spigushe/barrins-codex/issues) will be dealt with as quickly as possible.

This site uses [Flask](https://flask.palletsprojects.com) and [Babel](http://babel.pocoo.org)
to generate pages dynamically and handle internationalisation.

## Instructions to contributors
Here are various general guidelines this website is enforcing:
- Do not talk about yourself
- Do not talk to the reader
- Do not engage the reader in the talk
- Use spaces between the call and the variable for better clarity `{{ some_variable }}`
- Use mana symbols, they are emojis in the context (currently `{{ W }}`, `{{ U }}`, `{{ B }}`, `{{ R }}`, `{{ G }}`)
- Use card names variables, they are in the context (example `{{ jace_the_mind_sculptor }}` for `Jace, the Mind Sculptor`)
- If a card name doesn't compile, you are free to declare the name, it is mandatory for Adventure card and some other

## Installation
To install a working developpment version of the site, use `pip`:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"
```

The first time the project is started, the page will take some time to compile a list of
cards and their `scryfallId` to gain access to the card image. This script is also used
to build a JSON version of a decklist.

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

You can set the `DEBUG` environment variable to activate the debug mode:

```bash
DEBUG=1 codex
```

## Useful tools

There are some utils provided in the codex:

### Decklist Converter
Using an alphabetically sorted decklist, just put `SB:` before every card in Command Zone.
```bash
cd ./barrins_codex
python ./build_deck.py PATH_TO_FILE
```

### Google Translate

Use python and Google Translate to help with translation:

```python
import clipboard
import pprint
import re

def pre():
    s = "".join(s[1:-1] for s in clipboard.paste().split("\n"))
    s = re.sub(r"%\(([^\)]*)\)s", r"§KEEP\1§", s)
    clipboard.copy(s)

def post():
    s = clipboard.paste()
    s = pprint.pformat(re.sub(r"§KEEP([^§]*)§", r"%(\1)s", s), width=88)
    s = re.sub(
            r"(^')|('$)",
            '"',
            re.sub(r"^\s*", "", s[1:-1], flags=re.MULTILINE),
            flags=re.MULTILINE
        ).replace("\\n", "")
    clipboard.copy(s)

# usage:
#  > copy paragraph to translate from the PO file
# pre()
# > copy translation
# post()
# > copy result to the PO file
```

## Versioning
The version number take the form X.Y.Z where X, Y, and Z are non-negative integers, and do not
contain leading zeroes. X is the major version, Y is the minor version, and Z is the patch version.
Each element MUST increase numerically. For instance: `1.9.0` -> `1.10.0` -> `1.11.0`.

Given a version number MAJOR.MINOR.PATCH, I increment the:
1. MAJOR version when I make a backend evolution or a design evolution,
1. MINOR version when I add content, and
1. PATCH version when I make bug and typo fixes.

Additional labels for pre-release and build metadata are available as extensions to the
MAJOR.MINOR.PATCH format.
