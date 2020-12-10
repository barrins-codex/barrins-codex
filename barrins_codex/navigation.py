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
			lazy_gettext("Philosophie"),
			index=True,
			children=[
				#Nav(lazy_gettext("LackeyCCG")),
			],
		),
		Nav(
			lazy_gettext("Stratégie"),
			index=True,
			children=[
				#Nav(
					#lazy_gettext("Deck guides"),
					#children=[
						#Nav(lazy_gettext("Den of Fiends")),
					#],
				#),
			],
		),
		Nav(
			lazy_gettext("Maths et Magic"),
			index=True,
			children=[
				#Nav(lazy_gettext("LackeyCCG")),
			],
		),
		Nav(
			lazy_gettext("Rapports"),
			index=True,
			children=[
				#Nav(lazy_gettext("LackeyCCG")),
			],
		),
	],
)


HELPER = dict(STRUCTURE.walk())
