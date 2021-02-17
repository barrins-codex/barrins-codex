import collections
import re
import unidecode
from flask_babel import lazy_gettext


Page = collections.namedtuple("Page", ["name", "path", "url"])


class Nav:
	def __init__(self, name, index=False, children=None):
		self.name = name
		self.index = index
		self.children = children or []

	def page(self, path):
		res = unidecode.unidecode(str(self.name))
		res = re.sub(r"[^\sa-zA-Z0-9]", "", res).lower().strip()
		res = re.sub(r"\s+", "-", res)
		if res == "home":
			res = path
		else:
			res = path + "/" + res
		if not self.children:
			url = res + ".html"
		elif self.index:
			url = res + "/index.html"
		else:
			url = None
		return Page(self.name, res, url)

	def walk(self, path=None, top=None, ante=None, post=None):
		page = self.page(path or "")
		if not self.children or self.index:
			yield (page.path, {"self": page, "top": top, "prev": ante, "next": post})
		if self.index:
			top = page
		for i, child in enumerate(self.children):
			if i > 0:
				ante = self.children[i - 1].page(page.path)
			else:
				ante = None
			if i < len(self.children) - 1:
				post = self.children[i + 1].page(page.path)
			else:
				post = None
			yield from child.walk(path=page.path, top=top, ante=ante, post=post)


STRUCTURE = Nav(
	# TRANSLATORS: please abide by MTG translation choices for game terms when possible.
	lazy_gettext("Home"),
	index=True,
	children=[
		Nav(
			lazy_gettext("Articles"),
			index=True,
			children=[
				Nav(
					lazy_gettext("Classifier un deck"),
					index=True,
					children=[
						Nav(lazy_gettext("Les macrotypes")),
						Nav(lazy_gettext("Les archétypes")),
						Nav(lazy_gettext("Les tiers")),
						Nav(lazy_gettext("Pour aller plus loin")),
					],
				),
				Nav(
					lazy_gettext("Complexité et Machine de Turing"),
					index=True,
					children=[
						Nav(lazy_gettext("Jeu, Complexité et Résolution")),
						Nav(lazy_gettext("Magic et Complexité")),
					],
				),
				Nav(lazy_gettext("Construire un deck")),
				Nav(lazy_gettext("Mélanger un deck")),
			],
		),
		Nav(
			lazy_gettext("Archétypes"),
			index=True,
			children=[
				Nav(lazy_gettext("Adeliz, the Cinder Wind")),
				Nav(lazy_gettext("Aminatou, the Fateshifter")),
				Nav(lazy_gettext("Isamaru, Hound of Konda")),
				Nav(lazy_gettext("Golos, Tireless Pilgrim")),
				Nav(lazy_gettext("Kelsien, the Plague")),
				Nav(lazy_gettext("Kess, Dissident Mage")),
				Nav(lazy_gettext("Orvar, the All-Form")),
				Nav(lazy_gettext("Rowan and Will Kenrith")),
				Nav(lazy_gettext("The Gitrog Monster")),
				Nav(lazy_gettext("Titania, Protector of Argoth")),
				Nav(lazy_gettext("Venser, Shaper Savant")),
				Nav(lazy_gettext("Winota, Joiner of Forces")),
			],
		),
		Nav(
			lazy_gettext("Cartes thématiques"),
			index=True,
			children=[
				Nav(
					lazy_gettext("Mécaniques de la colorpie"),
					index=False,
					children=[
						Nav(lazy_gettext("La Destruction de permanents")),
						Nav(lazy_gettext("Les Cartes de taxe")),
						Nav(lazy_gettext("La Protection")),
						Nav(lazy_gettext("Les Contresorts")),
						Nav(lazy_gettext("Le Bounce de permanents")),
						Nav(lazy_gettext("Les Cantrips")),
						Nav(lazy_gettext("La Défausse")),
						Nav(lazy_gettext("La Gestion de créatures")),
						Nav(lazy_gettext("La Réanimation de créatures")),
						Nav(lazy_gettext("Les Dégâts directs")),
						Nav(lazy_gettext("Les Créatures agressives")),
						Nav(lazy_gettext("Le Remplacement de cartes")),
						Nav(lazy_gettext("Le Ramp")),
						Nav(lazy_gettext("Les Mana dorks")),
						Nav(lazy_gettext("Les Grosses Créatures")),
					],
				),
				Nav(lazy_gettext("Les Cantrips")),
				Nav(lazy_gettext("Les Piocheurs")),
				Nav(lazy_gettext("Les Spot Removals")),
				Nav(lazy_gettext("Les Mass Removals")),
			],
		),
		Nav(
			lazy_gettext("Maths"),
			index=True,
			children=[
				Nav(lazy_gettext("Combo A + B")),
				Nav(lazy_gettext("Ik-O-Maths")),
			],
		),
	],
)


HELPER = dict(STRUCTURE.walk())
