import os
import sys
import json

fn = sys.argv[1]
if os.path.exists(fn):
    # Le fichier existe
    print(os.path.basename(fn))
    # Ouverture du fichier et chargement du deck
    with open(fn) as jsonFile:
        jsonObject = json.load(jsonFile)
        jsonFile.close()
    # Impression de la bibliothèque
    for cat in jsonObject["library"]["cards"]:
        for card in cat["cards"]:
            print(card["count"] + " " + card["name"])
    # Impression de la command zone
    print("Sideboard")
    for card in jsonObject["command"]["cards"]:
        print(card["count"] + " " + card["name"])
