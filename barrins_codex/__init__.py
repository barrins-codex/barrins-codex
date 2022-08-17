import re
import unidecode
import requests
import os
import json
import pkg_resources
import copy

import urllib.parse
from urllib.parse import urlparse

import flask
from flask import make_response, request, render_template
import jinja2.exceptions

from . import config
from .navigation import HELPER
from . import card_list


version = pkg_resources.Environment()["barrins-codex"][0].version
if version[-5:] == ".dev0":  # To pass tests on commits during development
    version = version[:-5]
    version = version[:-1] + str(int(version[-1]) - 1)

app = flask.Flask(__name__, template_folder="templates", static_folder="static")
app.jinja_env.policies["ext.i18n.trimmed"] = True
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True
config.configure_app(app)

if os.path.isfile("library.json"):
    with open("library.json", "r", encoding="utf-8") as file:
        CARDS = json.load(file)
else:
    CARDS = card_list.build()

BASE_CONTEXT = {
    "version": version,
    "pilotes_habitue": [
        page for page in HELPER if HELPER.get(page, {}).get("cat") == "habitue"
    ],
    "pilotes_invite": [
        page for page in HELPER if HELPER.get(page, {}).get("cat") == "invite"
    ],
    "decks_agro": [
        page for page in HELPER if HELPER.get(page, {}).get("cat") == "agro"
    ],
    "decks_tempo": [
        page for page in HELPER if HELPER.get(page, {}).get("cat") == "tempo"
    ],
    "decks_controle": [
        page for page in HELPER if HELPER.get(page, {}).get("cat") == "controle"
    ],
    "decks_combo": [
        page for page in HELPER if HELPER.get(page, {}).get("cat") == "combo"
    ],
    "decks_midrange": [
        page for page in HELPER if HELPER.get(page, {}).get("cat") == "midrange"
    ],
    "decks_ban": [page for page in HELPER if HELPER.get(page, {}).get("cat") == "ban"],
    "needs_crop": [page for page in HELPER if HELPER.get(page, {}).get("crop")],
    "matchs_0110": [
        page for page in HELPER if HELPER.get(page, {}).get("cat") == "01-10"
    ],
    "matchs_1120": [
        page for page in HELPER if HELPER.get(page, {}).get("cat") == "11-20"
    ],
    "matchs_2130": [
        page for page in HELPER if HELPER.get(page, {}).get("cat") == "21-30"
    ],
}


def main():
    # print(HELPER)
    # print(BASE_CONTEXT)
    app.run()


# Defining Errors
@app.errorhandler(jinja2.exceptions.TemplateNotFound)
@app.errorhandler(404)
def page_not_found(error):
    context = copy.copy(BASE_CONTEXT)
    return flask.render_template("404.html", **context), 404


# Static file redirection
@app.route("/favicon.ico")
def favicon():
    return flask.redirect(flask.url_for("static", filename="img/favicon.ico"))


# Serve robots static file
@app.route("/robots.txt")
def static_from_root():
    return flask.send_from_directory(app.static_folder, flask.request.path[1:])


# Serve sitemap template
# code used from https://gist.github.com/Julian-Nash/aa3041b47183176ca9ff81c8382b655a
@app.route("/sitemap.xml")
def sitemap():
    host_components = urlparse(request.host_url)
    host_base = host_components.scheme + "://" + host_components.netloc

    urls = [host_base + p["self"].url for p in HELPER.values()]

    xml_sitemap = render_template("sitemap.xml", urls=urls, host_base=host_base)
    response = make_response(xml_sitemap)
    response.headers["Content-Type"] = "application/xml"

    return response


# Serve webfonts
@app.route("/webfonts/<path:font>")
def static_fonts(font=None):
    return flask.redirect(flask.url_for("static", filename=f"fonts/{font}"))


# Default route
@app.route("/")
@app.route("/<path:page>")
def index(page=None):
    redirect = False
    if not page:
        page = "index.html"
        redirect = True
    page = "/" + page
    if redirect:
        return flask.redirect(page, 301)

    context = copy.copy(BASE_CONTEXT)
    return flask.render_template(page, **context)


def _build_url(page, _anchor=None, **params):
    url = page.url
    if params:
        url += "?" + urllib.parse.urlencode(params)
    if _anchor:
        url += "#" + _anchor
    return url


def _link(page, name=None, _anchor=None, _class=None, **params):
    if not page or not page.url:
        return ""
    name = name or page.name
    url = _build_url(page, _anchor, **params)
    if _class:
        # _class = f"class='{_class} text-reset'"
        _class = f"class='{_class}'"
    else:
        _class = "class='text-reset'"
    return flask.Markup(f'<a {_class} href="{url}">{name}</a>')


@app.context_processor
def linker():
    path = flask.request.path
    if path[-11:] == "/index.html":
        path = path[:-11]
    if path[-5:] == ".html":
        path = path[:-5]
    if path[-1:] == "/":
        path = path[:-1]

    def _url(page, _anchor=None, **params):
        return _build_url(HELPER.get(page, {}).get("self"), _anchor=_anchor, **params)

    def link(page, name=None, _anchor=None, **params):
        return _link(
            HELPER.get(page, {}).get("self"),
            name=name,
            _anchor=_anchor,
            **params,
        )

    def name(page, name=None):
        return name or HELPER.get(page, {}).get("self").name

    def top():
        return _link(HELPER.get(path, {}).get("top"), _class="text-reset")

    def next():
        return _link(HELPER.get(path, {}).get("next"), _class="next text-reset")

    def prev():
        return _link(HELPER.get(path, {}).get("prev"), _class="prev text-reset")

    def external(url, name, _class=None):
        if _class:
            _class = f"class='{_class}'"
        else:
            _class = "class='text-reset text-decoration-underline'"
        return flask.Markup(
            f'<a {_class} target="_blank" rel="noreferrer" href="{url}">{name}</a>'
        )

    def title():
        try:
            if HELPER.get(path, {}).get("self").path != "":
                name = HELPER.get(path, {}).get("self").name
                return f"Barrin's Codex - {name}"
        except AttributeError:
            pass
        return "Barrin's Codex"

    def page_name():
        try:
            if HELPER.get(path, {}).get("self").path != "":
                name = HELPER.get(path, {}).get("self").name
                return f"{name}"
        except AttributeError:
            pass
        return "Barrin's Codex"

    return dict(
        url=_url,
        link=link,
        title=title,
        name=name,
        page_name=page_name,
        top=top,
        next=next,
        prev=prev,
        external=external,
    )


@app.context_processor
def display_card():
    def get_card(name, firstprint=True):
        fuzzy = re.sub(r"[^\w\s]", "", name)
        fuzzy = re.sub(r"\s+", "-", fuzzy)
        url = f"https://api.scryfall.com/cards/search?q={fuzzy}"
        if firstprint:
            url = url + "+is%3Afirstprint"
        r = requests.get(url)
        return r.json()

    def _name(name):
        name = name
        name = unidecode.unidecode(name).lower()
        name = re.sub(r"[^a-zA-Z0-9]", "", name)
        return name

    def card_name_from_page(name):
        page_name = HELPER.get(name, {}).get("self").name
        if "❌" in page_name:
            page_name = page_name[2:]
        return page_name

    def img_crop(name, front=True):
        card = CARDS[_name(name)]
        if "faces" in card:
            if not front:
                card = get_card(name)["data"][0]
                return card["card_faces"][1]["image_uris"]["art_crops"]
            return (
                "https://api.scryfall.com/cards/"
                + f"{CARDS[card['faces'][0]]['id']}"
                + "?format=image&version=art_crop"
            )
        return (
            "https://api.scryfall.com/cards/"
            + f"{card['id']}?format=image&version=art_crop"
        )

    def img_card(name, firstprint=True, front=True):
        card = CARDS[_name(name)]
        if "faces" in card:
            if not front:
                card = get_card(name, firstprint)["data"][0]
                return card["card_faces"][1]["image_uris"]["png"]
            card = get_card(name, firstprint)["data"][0]
            return card["card_faces"][0]["image_uris"]["png"]
        if firstprint:
            card = get_card(name, firstprint)["data"][0]
            return card["image_uris"]["png"]
        return f"https://api.scryfall.com/cards/{card['id']}?format=image"

    def card_link(name):
        return flask.Markup(
            '<a target="_blank" class="text-reset text-decoration-underline" '
            + 'rel="noreferrer" href="'
            + get_card(name)["data"][0]["scryfall_uri"]
            + '">'
            + name
            + "</a>"
        )

    return dict(
        deck_name=card_name_from_page,
        img_crop=img_crop,
        img_card=img_card,
        card_link=card_link,
    )


@app.context_processor
def display_match():
    def match_name(page):
        try:
            if HELPER.get(page, {}).get("self").path != "":
                name = HELPER.get(page, {}).get("self").name
                return name.split(" ", 1)[1]
        except AttributeError:
            pass
        return "Barrin's Codex"

    return dict(match_name=match_name)


@app.context_processor
def players():
    def player_name(page):
        try:
            if HELPER.get(page, {}).get("self").path != "":
                name = HELPER.get(page, {}).get("self").name
                if name == "Apparitions":
                    return "Guest"
                return name.split(" ", 1)[0]
        except AttributeError:
            pass
        return "Barrin's Codex"

    def player_nickname(page):
        try:
            if HELPER.get(page, {}).get("self").path != "":
                name = HELPER.get(page, {}).get("self").name
                name = name.split(" ", 1)
                if len(name) == 1:
                    if name[0] == "Apparitions":
                        return "Pilote mystérieux·euse"
                    return name[0]
                return name[1][2:-2]
        except AttributeError:
            pass
        return "Barrin's Codex"

    return dict(player_name=player_name, player_nickname=player_nickname)
