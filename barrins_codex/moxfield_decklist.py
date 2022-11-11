import re

import requests


def get_moxfield_decklist(link):
    url = "https://api.moxfield.com/v2/decks/all/"
    deck_json = requests.get(url + link).json()
    return deck_json


def get_card_data(card):
    return {
        "key": card["card"]["scryfall_id"],
        "name": re.split(" // ", card["card"]["name"])[0],
        "types": card["card"]["type"],
        "count": card["quantity"],
    }


def add_to_type(deck: dict, name: str, quantity: int, type: str):
    deck[type]["cards"].append(str(quantity) + " " + name)


def deck_name(text, day):
    return "[Barrin's Codex] " + day + " " + text[11:]


def build_deck(list):
    deck = {
        "0": {"name": "Command Zone", "cards": []},
        "1": {"name": "Planeswalkers", "cards": []},
        "2": {"name": "Creatures", "cards": []},
        "3": {"name": "Sorceries", "cards": []},
        "4": {"name": "Instants", "cards": []},
        "5": {"name": "Artifacts", "cards": []},
        "6": {"name": "Enchantments", "cards": []},
        "7": {"name": "Lands", "cards": []},
    }

    for k, v in list["mainboard"].items():
        card = get_card_data(v)
        add_to_type(deck, card["name"], card["count"], card["types"])

    for k, v in list["commanders"].items():
        card = get_card_data(v)
        add_to_type(deck, card["name"], 1, "0")

    return deck


def export(url):
    list = get_moxfield_decklist(url)
    deck = build_deck(list)

    text_return = ""
    command_zone = ""
    for k, v in deck.items():
        v["cards"].sort()
        if k == "0":
            command_zone += "\n".join(v["cards"])
        else:
            if len(v["cards"]) > 0:
                text_return += "\n".join(v["cards"])
                text_return += "\n"

    return {
        "name": deck_name(list["name"], list["createdAtUtc"][:10]),
        "list": text_return + "\nSideboard\n" + command_zone,
    }
