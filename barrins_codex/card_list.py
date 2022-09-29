import gzip
import json
import os
import re

import requests
import unidecode


def _name(card, name=None):
    name = name or card["name"]
    name = unidecode.unidecode(name).lower()
    name = re.sub(r"[^a-zA-Z0-9]", "", name)
    return name


def _get(card, set, name=None):
    return {
        "key": _name(card),
        "name": (name or card["name"]),
        "date": set["releaseDate"],
        "id": card["identifiers"]["scryfallId"],
    }


def _download(url):
    file = url.split("/")[-1]
    response = requests.get(url, stream=True)
    with open(file, "wb") as file:
        response = requests.get(url)
        file.write(response.content)


def _delete(file):
    if os.path.isfile(file):
        os.remove(file)
    else:
        print(r"{file} not found")


SKIP_TYPES = [
    "promo",
    "funny",
    "box",
    "memorabilia",
    "alchemy",
    "masterpiece",
    "archenemy",
    "starter",
    "token",
    "arsenal",
    "duel_deck",
    "from_the_vault",
    "treasure_chest",
    "vanguard",
    "premium_deck",
    "spellbook",
]


def build():
    # Download SetList.json.gz
    _download("https://mtgjson.com/api/v5/SetList.json.gz")
    sets = json.load(gzip.open("SetList.json.gz"))
    # Download AllPrintings.json.gz
    _download("https://mtgjson.com/api/v5/AllPrintings.json.gz")
    prints = json.load(gzip.open("AllPrintings.json.gz"))

    library = {}
    for set in sets["data"]:
        if set["type"] not in SKIP_TYPES:
            for card in prints["data"][set["code"]]["cards"]:
                # Adding it to library
                if _name(card) not in library:
                    library[_name(card)] = _get(card, set)
                if _name(card) in library:
                    # If newer version exists
                    if set["releaseDate"] < library[_name(card)]["date"]:
                        library[_name(card)] = _get(card, set)

                # Cards may have another face : name_face_a / name_face_b
                # Cards with other faces have a "//" separator
                if "//" in card["name"]:
                    (face_a, face_b) = card["name"].split(" // ")
                    # Adding faces to main card and every parts
                    faces = [_name(card, face_a), _name(card, face_b)]
                    library[_name(card)]["faces"] = faces
                    if _name(card, face_a) not in library:
                        library[_name(card, face_a)] = _get(card, set, face_a)
                        library[_name(card, face_a)]["faces"] = faces
                    if _name(card, face_b) not in library:
                        library[_name(card, face_b)] = _get(card, set, face_b)
                        library[_name(card, face_b)]["faces"] = faces

    # Deleting downloaded files
    _delete("AllPrintings.json.gz")
    _delete("SetList.json.gz")

    try:
        with open("library.json", "w", encoding="utf-8") as file:
            json.dump(library, file, ensure_ascii=False, indent=4)
    except IOError:
        pass

    # Returning constructed library
    return library


if __name__ == "__main__":
    build()
