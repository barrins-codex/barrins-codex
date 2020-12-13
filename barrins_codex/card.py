import collections
import re
import unidecode
import scrython

Library = dict()
Carte = collections.namedtuple("Carte",["name","short","uris"])

catalogue = scrython.catalog.CardNames()
for carte in catalogue.data():
	if carte not in Library:
		if scrython.cards.Named(exact=carte).legalities()['duel'] == "legal":
			print(carte)
			name = re.sub(r"[^a-zA-Z0-9]", "", unidecode.unidecode(carte).lower())
			scryfall = scrython.cards.Named(exact=carte)

			try:
				faces = len(scryfall.card_faces())
				pass
			except AttributeError:
				faces = 1
				pass

			if len(.card_faces()) == 2:
				# Some Action
				print("\tTwo faces")
				uri = "empty"
			else:
				uri = scrython.cards.Named(fuzzy=name).image_uris()

			Library[carte] = Carte(carte,name,uri)

print(Library)
