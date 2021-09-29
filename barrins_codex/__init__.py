import copy
import urllib.parse
import re
import unidecode
import os
import requests

import flask
import flask_babel
import jinja2.exceptions

from . import config
from . import navigation

# Base de données des cartes
import gzip
import json


if os.path.isfile("barrins_codex/library.json.gz"):
    # File exists
    cartes = json.load(gzip.open("barrins_codex/library.json.gz"))
else:
    # Build file
    from . import build_library

    cartes = build_library.build()
library = {}


app = flask.Flask(__name__, template_folder="templates", static_folder="static")
app.jinja_env.policies["ext.i18n.trimmed"] = True
babel = flask_babel.Babel(app)
config.configure_app(app)


def main():
    app.run()


# Adding symbols to context_processor
BASE_CONTEXT = {
    "W": flask.Markup("🔆"),
    "U": flask.Markup("💧"),
    "B": flask.Markup("💀"),
    "R": flask.Markup("🔥"),
    "G": flask.Markup("🌳"),
}


# Retrieving locale and timezone information
@babel.localeselector
def get_locale():
    return flask.g.get("lang_code", app.config["BABEL_DEFAULT_LOCALE"])


@babel.timezoneselector
def get_timezone():
    user = flask.g.get("user", None)
    if user is not None:
        return user.timezone


# Defining Errors
@app.errorhandler(jinja2.exceptions.TemplateNotFound)
@app.errorhandler(404)
def page_not_found(error):
    return flask.render_template("404.html"), 404


# Static file redirection
@app.route("/favicon.ico")
def favicon():
    return flask.redirect(flask.url_for("static", filename="img/favicon.ico"))


# Serve robots and sitemap static files
@app.route("/robots.txt")
@app.route("/sitemap.xml")
def static_from_root():
    return flask.send_from_directory(app.static_folder, flask.request.path[1:])


# Serve webfonts
@app.route("/webfonts/<path:font>")
@app.route("/<lang_code>/webfonts/<path:font>")
def static_fonts(lang_code=None, font=None):
    return flask.redirect(flask.url_for("static", filename=f"fonts/{font}"))


# Default route
@app.route("/")
@app.route("/<path:page>")
@app.route("/<lang_code>/<path:page>")
def index(lang_code=None, page=None):
    redirect = False
    if not page:
        page = "index.html"
        redirect = True
    if not lang_code or lang_code not in app.config["SUPPORTED_LANGUAGES"].keys():
        if lang_code:
            page = lang_code + "/" + page
        lang_code = (
            flask.request.accept_languages.best_match(
                app.config["SUPPORTED_LANGUAGES"].keys()
            )
            or "fr"
        )
        page = "/" + lang_code + "/" + page
        redirect = True
    if redirect:
        return flask.redirect(page, 301)

    flask.g.lang_code = lang_code
    context = copy.copy(BASE_CONTEXT)
    context["lang"] = lang_code
    return flask.render_template(page, **context)


def _i18n_url(page, _anchor=None, locale=None, **params):
    url = "/" + (locale or get_locale()) + page.url
    if params:
        url += "?" + urllib.parse.urlencode(params)
    if _anchor:
        url += "#" + _anchor
    return url


def _link(page, name=None, _anchor=None, _class=None, locale=None, **params):
    if not page or not page.url:
        return ""
    name = name or page.name
    url = _i18n_url(page, _anchor, locale, **params)
    if _class:
        _class = f"class={_class} "
    else:
        _class = ""
    return flask.Markup(f'<a {_class}href="{url}">{name}</a>')


@app.context_processor
def linker():
    path = flask.request.path
    if path[1:3] in app.config["SUPPORTED_LANGUAGES"].keys():
        path = path[3:]
    if path[-11:] == "/index.html":
        path = path[:-11]
    if path[-5:] == ".html":
        path = path[:-5]
    if path[-1:] == "/":
        path = path[:-1]

    def i18n_url(page, _anchor=None, **params):
        return _i18n_url(
            navigation.HELPER.get(page, {}).get("self"), _anchor=_anchor, **params
        )

    def link(page, name=None, _anchor=None, **params):
        return _link(
            navigation.HELPER.get(page, {}).get("self"),
            name=name,
            _anchor=_anchor,
            **params,
        )

    def translation(locale, name):
        return _link(
            navigation.HELPER.get(path, {}).get("self"), name=name, locale=locale
        )

    def top():
        return _link(navigation.HELPER.get(path, {}).get("top"))

    def next():
        return _link(navigation.HELPER.get(path, {}).get("next"), _class="next")

    def prev():
        return _link(navigation.HELPER.get(path, {}).get("prev"), _class="prev")

    def external(url, name):
        return flask.Markup(
            f'<a target="_blank" rel="noreferrer" href="{url}">{name}</a>'
        )

    def title():
        try:
            if navigation.HELPER.get(path, {}).get("self").path != "":
                name = navigation.HELPER.get(path, {}).get("self").name
                return f"Barrin's Codex - {name}"
        except AttributeError:
            pass
        return "Barrin's Codex"

    def page_name():
        try:
            if navigation.HELPER.get(path, {}).get("self").path != "":
                name = navigation.HELPER.get(path, {}).get("self").name
                return f"{name}"
        except AttributeError:
            pass
        return "Barrin's Codex"

    return dict(
        i18n_url=i18n_url,
        link=link,
        translation=translation,
        title=title,
        page_name=page_name,
        top=top,
        next=next,
        prev=prev,
        external=external,
    )


# reecriture en variables
def _var_name(name):
    name = unidecode.unidecode(name).lower()
    name = re.sub(r"'", "", name)
    name = re.sub(r",", "", name)
    name = re.sub(r"[^a-zA-Z0-9]", "_", name)
    return name


def _name(name):
    name = unidecode.unidecode(name).lower()
    name = re.sub(r"[^a-zA-Z0-9]", "", name)
    return name


def scryfall_id(name):
    name = _name(name)
    return library[name]["id"]


@app.context_processor
def display_card():
    def card(name, display_name=None):
        return flask.Markup(
            """<span class="card" scryfallId="{scryfallId}" data-tippy-content="
<div class='card-container'>
    <img
        data-src='https://api.scryfall.com/cards/{scryfallId}?format=image'
        class='card-image'
    />
</div>">{name}</span>""".format(
                # replace spaces with non-breakable spaces in card names
                name=(display_name or name).replace(" ", " "),
                scryfallId=scryfall_id(name),
            )
        )

    for carte in cartes:
        # Enabling card names checks
        library[list(carte)[0]] = carte[list(carte)[0]]
        # Adding card to context
        BASE_CONTEXT[_var_name(library[list(carte)[0]]["name"])] = card(
            library[list(carte)[0]]["name"]
        )

    def card_image(name, version="png"):
        img = """
<img
    src="https://api.scryfall.com/cards/{scryfallId}?format=image&version={version}"
    alt="{name}" scryfallId="{scryfallId}"
/>
        """

        return flask.Markup(
            img.format(
                name=name.replace(" ", " "),
                scryfallId=scryfall_id(name),
                version=version,
            )
        )

    def card_art(name):
        return flask.Markup(
            """<img
    src="https://api.scryfall.com/cards/{scryfallId}?format=image&version=art_crop"
    alt="{name}"
/>""".format(
                name=name.replace(" ", " "), scryfallId=scryfall_id(name)
            )
        )

    return dict(card=card, card_image=card_image, card_art=card_art)


@app.context_processor
def display_deck():
    def frame_moxfield(key, id="moxfield-frame"):
        return flask.Markup(
            """
<iframe
    src="https://www.moxfield.com/embed/{key}?hideTotal=true"
    id="{id}"
    frameBorder="0"
    width="100%"
    onload="moxfieldOnLoad(event)"
></iframe>
        """.format(
                key=key, id=id
            )
        )

    def _exportId(key: str):
        url = "https://api.moxfield.com/v2/decks/all/"
        r = requests.get(url + key)
        return r.json().get("exportId")

    def _decklist(key: str):
        url = "https://api.moxfield.com/v1/decks/all/"
        url = url + f"{key}/export?arenaOnly=false&exportId="
        r = requests.get(url + _exportId(key))
        return r.text

    def _name(name):
        name = unidecode.unidecode(name).lower()
        name = re.sub(r"[^a-zA-Z]", "", name)
        return name

    def _get(ligne):
        qte = re.sub(r"[a-zA-Z]", "", ligne.split(r" ")[0])
        info = library[_name(ligne)]
        return {
            "count": qte,
            "name": re.split("/", info["name"])[0],
            "id": info["id"],
            "types": info["types"],
        }

    def _formalize(list, command):
        czon = []
        crea = {"type": "Creatures", "count": 0, "cards": []}
        plan = {"type": "Planeswalkers", "count": 0, "cards": []}
        arti = {"type": "Artifacts", "count": 0, "cards": []}
        ench = {"type": "Enchantments", "count": 0, "cards": []}
        inst = {"type": "Instants", "count": 0, "cards": []}
        sorc = {"type": "Sorceries", "count": 0, "cards": []}
        land = {"type": "Lands", "count": 0, "cards": []}

        lignes = list.split("\r\n")
        for ligne in lignes:
            if re.search(command, ligne):
                czon.append(_get(ligne))
                continue

            name = _name(re.split("/", ligne)[0])
            if name in library:
                ajout = _get(ligne)

                if "Land" in ajout["types"]:
                    land["count"] = land["count"] + int(ajout["count"])

                    if len(ajout["types"]) == 1:
                        land["cards"].append(ajout)
                    elif "Creature" in ajout["types"]:
                        if "/" not in ligne:
                            crea["count"] = crea["count"] + int(ajout["count"])
                            land["cards"].append(ajout)
                            continue  #: Will never add "Dryad Arbor" to Creatures
                    elif "Enchantment" in ajout["types"]:
                        if "/" not in ligne:
                            ench["count"] = ench["count"] + int(ajout["count"])
                            land["cards"].append(ajout)
                            continue  #: Will never add Urza's Saga to Enchantments
                    elif "Artifact" in ajout["types"]:
                        if "/" not in ligne:
                            arti["count"] = arti["count"] + int(ajout["count"])
                            land["cards"].append(ajout)
                            continue  #: Will never add Seat of the Synod to Artifacts

                if "Creature" in ajout["types"]:
                    crea["count"] = crea["count"] + int(ajout["count"])
                    crea["cards"].append(ajout)

                elif "Planeswalker" in ajout["types"]:
                    plan["count"] = plan["count"] + int(ajout["count"])
                    plan["cards"].append(ajout)

                elif "Artifact" in ajout["types"]:
                    arti["count"] = arti["count"] + int(ajout["count"])
                    arti["cards"].append(ajout)

                elif "Enchantment" in ajout["types"]:
                    ench["count"] = ench["count"] + int(ajout["count"])
                    ench["cards"].append(ajout)

                elif "Instant" in ajout["types"]:
                    inst["count"] = inst["count"] + int(ajout["count"])
                    inst["cards"].append(ajout)

                elif "Sorcery" in ajout["types"]:
                    sorc["count"] = sorc["count"] + int(ajout["count"])
                    sorc["cards"].append(ajout)

        table = {
            "library": {
                "cards": [crea, plan, arti, ench, inst, sorc, land],
                "count": (100 - len(czon)),
            },
            "command": {"cards": czon, "count": len(czon)},
        }

        return json.dumps(table, indent=4, sort_keys=True)

    def decklist(key: str, command: str):
        print(f"Command: {command}")
        print(f"Moxfield: {key}")
        d = _decklist(key)
        d = _formalize(d, command)
        return d

    return dict(frame_moxfield=frame_moxfield, decklist=decklist)
