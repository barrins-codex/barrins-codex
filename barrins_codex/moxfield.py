import requests

key = "ghTXBoESP0SlSSCr_QT-hg"


def _exportId(key):
    url = "https://api.moxfield.com/v2/decks/all/"
    r = requests.get(url + key)
    return r.json().get("exportId")


def _decklist(key):
    url = (
        f"https://api.moxfield.com/v1/decks/all/{key}/export?arenaOnly=false&exportId="
    )
    r = requests.get(url + _exportId(key))
    return r.text


def decklist(key):
    d = _decklist(key)
    d = d.split("\n")
    print(d)


decklist(key)
