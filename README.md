# barrins-codex
A website about MtG Duel Strategy

## Installation

To install a working developpment version of the site, use `pip`:

```bash
python3 -m venv venv
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

You can set the `DEBUG` environment variable to activate the debug mode:

```bash
DEBUG=1 codex
```
