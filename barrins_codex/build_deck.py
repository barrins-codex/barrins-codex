# Base de données des cartes
import gzip
import json
cartes = json.load(gzip.open("static/json/library.json.gz"))
library = {}
for carte in cartes:
	library[list(carte)[0]] = carte[list(carte)[0]]


# Traitement de texte
import re
import unidecode
def _name(name):
	name = unidecode.unidecode(name).lower()
	name = re.sub(r"[^a-zA-Z]", "", name)
	return name


# Ajout dans un réceptacle
def _get(ligne):
	qte = re.sub(r"[a-zA-Z]","",ligne.split(r" ")[0])
	info = library[_name(ligne)]
	return {
		"count":qte,
		"name":re.split("/",info["name"])[0],
		"id":info["id"],
		"types":info["types"]
	}


# Réceptacles
import json
czon = []
crea = { "type": "Creatures", "count": 0, "cards": [] }
plan = { "type": "Planeswalkers", "count": 0, "cards": [] }
arti = { "type": "Artifacts", "count": 0, "cards": [] }
ench = { "type": "Enchantments", "count": 0, "cards": [] }
inst = { "type": "Instants", "count": 0, "cards": [] }
sorc = { "type": "Sorceries", "count": 0, "cards": [] }
land = { "type": "Lands", "count": 0, "cards": [] }


# Fichier en paramètre
import os
import sys

fn = sys.argv[1]
if os.path.exists(fn):
	# Le fichier existe
	print(os.path.basename(fn))
	# Ouverture du fichier
	f = open(fn, "r")
	# Lecture ligne à ligne
	lignes = f.readlines()
	for ligne in lignes:
		if ligne.startswith("SB:"):
			# Command Zone
			czon.append(_get(ligne[3:]))

		name = _name(re.split("/",ligne)[0])
		if name in library:
			ajout = _get(ligne)
			# First lands because of some specific cards
			if "Land" in ajout["types"]:
				# Increase land count before hand to handle mdfc
				land["count"] = land["count"] + int(ajout["count"])
				# Land first in case of Dryad Arbor
				if "Creature" in ajout["types"] and "/" not in ligne:
					# Dryad Arbor-like case
					land["cards"].append(ajout)
				if len(ajout["types"]) == 1:
					# Usual land cards
					land["cards"].append(ajout)

			elif "Creature" in ajout["types"]:
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

	# Fermeture du fichier
	f.close()

	# Affichage du tableau
	table = {
		"library": {
			"cards": [
				crea,
				plan,
				arti,
				ench,
				inst,
				sorc,
				land
			],
			"count": (100-len(czon))
		},
		"command": {
			"cards":czon,
			"count":len(czon)
		}
	}
	print(json.dumps(table, indent=4, sort_keys=True))# Prettyprint
	#print(json.dumps(table))
	"""
	table = {"library":{"cards":deck,"count":len(deck)},"command":{"cards":czon,"count":len(czon)}}
	print(json.dumps(table))
	"""