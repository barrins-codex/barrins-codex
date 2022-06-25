import collections
import re
import unidecode


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
    "Home",
    index=True,
    children=[
        Nav(
            "🧍 Pilotes",
            index=True,
            children=[
                Nav("Anaël « Aliquanto »"),
                Nav("Bastien « threem »"),
                Nav("Damien « eventwin »"),
                Nav("Domino"),
                Nav("Félix « Midas »"),
                Nav("Florian « Trotte »"),
                Nav("Grégoire « Koraysh »"),
                Nav("Louis « Imperia86 »"),
                Nav("Martin « Spigushe »"),
                Nav("Apparitions"),
            ],
        ),
        Nav(
            "📝 Decks",
            index=True,
            children=[
                Nav("Adeliz, the Cinder Wind"),
                Nav("Aminatou, the Fateshifter"),
                Nav("Bjorna-Wernog"),
                Nav("Dennick, Pious Apprentice"),
                Nav("Doran, the Siege Tower"),
                Nav("Dragonlord Ojutai"),
                Nav("Elmar-Sophina"),
                Nav("Elminster"),
                Nav("Esika, God of the Tree"),
                Nav("Grist, the Hunger Tide"),
                Nav("Hinata, Dawn-Crowned"),
                Nav("Hogaak, Arisen Necropolis"),
                Nav("Isamaru, Hound of Konda"),
                Nav("Ishai-Tevesh"),
                Nav("Jori En, Ruin Diver"),
                Nav("Juri, Master of the Revue"),
                Nav("Kari Zev, Skyship Raider"),
                Nav("Karlov of the Ghost Council"),
                Nav("Killian, Ink Duelist"),
                Nav("Kinnan, Bonder Prodigy"),
                Nav("Klothys, God of Destiny"),
                Nav("Light-Paws, Emperor's Voice"),
                Nav("Livio-Malcolm"),
                Nav("Livio-Prava"),
                Nav("Marath, Will of the Wild"),
                Nav("Miara-Tevesh"),
                Nav("Minsc, Beloved Ranger"),
                Nav("Minsc&Boo, Timeless Heroes"),
                Nav("Niv-Mizzet Reborn"),
                Nav("Prossh, Skyraider of Kher"),
                Nav("Queen Marchesa"),
                Nav("Raffine, Scheming Seer"),
                Nav("Sai, Master Thopterist"),
                Nav("Saskia the Unyielding"),
                Nav("❌ Shorikai, Genesis Engine"),
                Nav("Sygg, River Cutthroat"),
                Nav("Sythis, Harvest's Hand"),
                Nav("The Beamtown Bullies"),
                Nav("The Gitrog Monster"),
                Nav("The Reality Chip"),
                Nav("Tiamat"),
                Nav("Tivit, Seller of Secrets"),
                Nav("Wilson, Refined Grizzly"),
            ],
        ),
        Nav(
            "⏯️ Matchs",
            index=True,
            children=[
                Nav("1. Adeliz vs Kinnan"),
                Nav("2. Kari Zev vs Saskia"),
                Nav("3. Isamaru vs Gitrog"),
                Nav("4. Livio-Malcolm vs Niv 5C"),
                Nav("5. Jori En vs Sygg"),
                Nav("6. Aminatou vs Klothys"),
                Nav("7. Livio-Prava vs Ojutai"),
                Nav("8. Esika vs Niv 5C"),
                Nav("9. Miara-Tevesh vs Prossh"),
                Nav("10. Kari Zev vs Marath"),
                Nav("11. Doran vs Marchesa"),
                Nav("12. Light Paws vs Ishai-Tevesh"),
                Nav("13. Bjorna-Wernog vs Grist"),
                Nav("14. Minsc vs Shorikai"),
                Nav("15. Dennick vs Hinata"),
                Nav("16. Aminatou vs Tiamat"),
                Nav("17. Grist vs Sythis"),
                Nav("18. Kari Zev vs Killian [Budget]"),
                Nav("19. Elmar-Sophina vs Shorikai"),
                Nav("20. Juri vs Sai"),
                Nav("21. Aminatou vs Beamtown"),
                Nav("22. Raffine vs Tivit"),
                Nav("23. Karlov vs Reality Chip"),
                Nav("24. Grist vs Minsc&Boo"),
                Nav("25. Elminster vs Wilson"),
                Nav("26. Hogaak vs Minsc&Boo"),
            ],
        ),
    ],
)


HELPER = dict(STRUCTURE.walk())
