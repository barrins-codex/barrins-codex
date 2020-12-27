import gzip
import json
import os
import sys
import unidecode
import re
# File Download
import requests
from tqdm.auto import tqdm


def _name(card):
	if "name" in card:
		name = card["name"]
	else:
		name = card
	name = unidecode.unidecode(name).lower()
	name = re.sub(r"[^a-zA-Z0-9]", "", name)
	return name


def _get(card,set,name=None):
	if name is not None:
		name = card["name"]
	return {
		"name":name or card["name"],
		"date":set["releaseDate"],
		"id":card["identifiers"]["scryfallId"],
		"types":card["types"],
	}


def _download(url):
	file = url.split('/')[-1]
	response = requests.get(url, stream=True)
	with tqdm.wrapattr(open(file, "wb"), "write", miniters=1,
			total=int(response.headers.get('content-length', 0)),
			desc=file) as fout:
		for chunk in response.iter_content(chunk_size=4096):
			fout.write(chunk)

DIR_NAME = "barrins_codex"
SKIP_TYPES = {"from_the_vault","masterpiece","promo","duel_deck","premium_deck","spellbook","token"}

# https://api.scryfall.com/cards/{scryfallId}?format=image

def build():
	# Download AllPrintings.json.gz
	_download("https://mtgjson.com/api/v5/AllPrintings.json.gz")
	# Download AllPrintings.json.gz
	_download("https://mtgjson.com/api/v5/SetList.json.gz")

	prints = json.load(gzip.open("AllPrintings.json.gz"))
	sets = json.load(gzip.open("SetList.json.gz"))

	library = {}
	for set in sets["data"]:
		if not set["isOnlineOnly"]:
			if set["type"] not in SKIP_TYPES:
				if len(set["code"]) == 3:
					# Only regular sets
					for card in prints["data"][set["code"]]["cards"]:
						# Adding it to library
						if _name(card) not in library:
							library[_name(card)] = {_name(card):_get(card, set)}
						if _name(card) in library:
							# If newer version exists
							if set["releaseDate"] > library[_name(card)][_name(card)]["date"]:
								library[_name(card)] = {_name(card):_get(card, set)}
						# Cards may have another face : name_face_a / name_face_b
						# Cards with other faces have a "//" separator
						if "//" in card["name"]:
							# Specific handling
							card_faces = card["name"].split(" // ")
							face_a = card_faces[0]
							face_b = card_faces[1]
							# Cards are already in the library
							if (_name(face_a) or _name(face_b)) in library:
								# Need to check types for any new type
								list_types = library[_name(card)][_name(card)]["types"]
								# library[_name(card)] if used above and will be updated
								for t in card["types"]:
									if t not in list_types:
										list_types.append(t)
								# Adding full set of types to card and all faces
								library[_name(face_a)][_name(face_a)]["types"] = list_types
								library[_name(face_b)][_name(face_b)]["types"] = list_types
							# Adding Face A to library
							if _name(face_a) not in library:
								library[_name(face_a)] = {_name(face_a):_get(card, set, face_a)}
							# Adding Face B to library
							if _name(face_b) not in library:
								library[_name(face_b)] = {_name(face_b):_get(card, set, face_b)}

	try:
		# Generating a file on dev
		if not os.path.isdir(DIR_NAME):
			os.mkdir(DIR_NAME)
		fname = "library.json.gz"
		fpath = os.path.join(DIR_NAME, fname)
		json.dump(list(library.values()), gzip.open(fpath, "wt"))
	except IOError:
		# No generation on prod
		pass

	# Deleting downloaded files
	os.remove("AllPrintings.json.gz")
	os.remove("SetList.json.gz")

	# Returning constructed library
	return library.values()

if __name__ == "__main__":
	build()
