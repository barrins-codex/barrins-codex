import gzip
import json
import os
import sys
import unidecode
import re


def _name(card):
	name = card["name"]
	name = unidecode.unidecode(name).lower()
	name = re.sub(r"[^a-zA-Z0-9]", "", name)
	return name


def _get(card,set):
	return {
		"name":card["name"],
		"date":set["releaseDate"],
		"id":card["identifiers"]["scryfallId"],
		"types":card["types"],
	}


DIR_NAME = "static/json"
SKIP_TYPES = {"from_the_vault","masterpiece","promo","duel_deck","premium_deck","spellbook","token"}

# https://api.scryfall.com/cards/{scryfallId}?format=image

if __name__ == "__main__":
	prints = json.load(gzip.open("AllPrintings.json.gz"))
	sets = json.load(gzip.open("SetList.json.gz"))

	library = {}
	for set in sets["data"]:
		if set["isOnlineOnly"]:
			# Only images of paper versions
			pass
		if set["type"] in SKIP_TYPES:
			# Only regular expansions
			pass
		if len(set["code"]) == 3:
			# Only regular sets
			for card in prints["data"][set["code"]]["cards"]:
				# Cards may have another face : name_face_a / name_face_b
				if "/" in card["name"]:
					card["name"] = card["name"].split(" /")[0]
				# Adding it to library
				if _name(card) not in library:
					library[_name(card)] = {_name(card):_get(card, set)}
				if _name(card) in library:
					# If newer version exists
					if set["releaseDate"] > library[_name(card)][_name(card)]["date"]:
						library[_name(card)] = {_name(card):_get(card, set)}


	if not os.path.isdir(DIR_NAME):
		os.mkdir(DIR_NAME)

	fname = "library.json.gz"
	fpath = os.path.join(DIR_NAME, fname)
	json.dump(list(library.values()), gzip.open(fpath, "wt"))

	fname = "cardlist.txt"
	fpath = os.path.join(DIR_NAME, fname)
	with open(fpath, "wt") as f:
		f.write("\n".join(sorted(library.keys())))
