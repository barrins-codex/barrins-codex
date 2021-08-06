# Fichier en paramètre
import os
import sys

# Base de données des cartes
import gzip
import json
library = {}
# Vérification de la présence de la table de correspondance
if (os.path.isfile("barrins_codex/library.json.gz")):
	# File exists === dev
	cartes = json.load(gzip.open("barrins_codex/library.json.gz"))
else:
	# Build file === prod
	import build_library
	cartes = build_library.build()
# Utilisation du fichier
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

			if "Creature" in ajout["types"]:
				crea["count"] = crea["count"] + int(ajout["count"])
				if "Land" not in ajout["types"]:
					crea["cards"].append(ajout)
				if "Land" in ajout["types"] and "/" in ligne:
					# MDFC creature-land case
					crea["cards"].append(ajout)
				if "Land" in ajout["types"] and "/" not in ligne:
					# Dryad Arbor case
					land["count"] = land["count"] + int(ajout["count"])
					land["cards"].append(ajout)

			elif "Planeswalker" in ajout["types"]:
				plan["count"] = plan["count"] + int(ajout["count"])
				if "Land" not in ajout["types"]: #: usual case
					plan["cards"].append(ajout)
				if "Land" in ajout["types"] and "/" in ligne: #: (m)dfc
					plan["cards"].append(ajout)
				if "Land" in ajout["types"] and "/" not in ligne: #: hybrid types
					land["count"] = land["count"] + int(ajout["count"])
					land["cards"].append(ajout)

			elif "Artifact" in ajout["types"]:
				arti["count"] = arti["count"] + int(ajout["count"])
				if "Land" not in ajout["types"]: #: usual case
					arti["cards"].append(ajout)
				if "Land" in ajout["types"] and "/" in ligne: #: (m)dfc
					arti["cards"].append(ajout)
				if "Land" in ajout["types"] and "/" not in ligne: #: hybrid types
					land["count"] = land["count"] + int(ajout["count"])
					land["cards"].append(ajout)


			elif "Enchantment" in ajout["types"]:
				ench["count"] = ench["count"] + int(ajout["count"])
				if "Land" not in ajout["types"]: #: usual case
					ench["cards"].append(ajout)
				if "Land" in ajout["types"] and "/" in ligne: #: (m)dfc
					ench["cards"].append(ajout)
				if "Land" in ajout["types"] and "/" not in ligne: #: hybrid types
					land["count"] = land["count"] + int(ajout["count"])
					land["cards"].append(ajout)


			elif "Instant" in ajout["types"]:
				inst["count"] = inst["count"] + int(ajout["count"])
				if "Land" not in ajout["types"]: #: usual case
					inst["cards"].append(ajout)
				if "Land" in ajout["types"] and "/" in ligne: #: (m)dfc
					inst["cards"].append(ajout)
				if "Land" in ajout["types"] and "/" not in ligne: #: hybrid types
					land["count"] = land["count"] + int(ajout["count"])
					land["cards"].append(ajout)

			elif "Sorcery" in ajout["types"]:
				sorc["count"] = sorc["count"] + int(ajout["count"])
				if "Land" not in ajout["types"]: #: usual case
					sorc["cards"].append(ajout)
				if "Land" in ajout["types"] and "/" in ligne: #: (m)dfc
					sorc["cards"].append(ajout)
				if "Land" in ajout["types"] and "/" not in ligne: #: hybrid types
					land["count"] = land["count"] + int(ajout["count"])
					land["cards"].append(ajout)

			elif "Land" in ajout["types"]:
				land["count"] = land["count"] + int(ajout["count"])
				land["cards"].append(ajout)

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
