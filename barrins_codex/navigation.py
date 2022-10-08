import collections
import re

import unidecode

Page = collections.namedtuple("Page", ["name", "path", "url", "cat", "crop"])


class Nav:
    def __init__(self, name, index=False, children=None, cat=None, crop=False):
        self.name = name
        self.index = index
        self.children = children or []
        self.cat = cat or ""
        self.crop = crop

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
        return Page(self.name, res, url, self.cat, self.crop)

    def walk(self, path=None, top=None, ante=None, post=None):
        page = self.page(path or "")
        if not self.children or self.index:
            yield (
                page.path,
                {
                    "self": page,
                    "top": top,
                    "prev": ante,
                    "next": post,
                    "cat": self.cat,
                    "crop": self.crop,
                },
            )
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
    "Home",
    index=True,
    children=[
        Nav(
            "🧍 Pilotes",
            index=True,
            children=[
                Nav("Anaël « Aliquanto »", cat="invite"),
                Nav("Bastien « threem »", cat="invite"),
                Nav("Damien « eventwin »", cat="invite"),
                Nav("Domino", cat="habitue"),
                Nav("Félix « Midas »", cat="invite"),
                Nav("Florian « Trotte »", cat="invite"),
                Nav("Grégoire « Koraysh »", cat="invite"),
                Nav("Louis « Imperia86 »", cat="habitue"),
                Nav("Martin « Spigushe »", cat="habitue"),
                Nav("Apparitions", cat="invite"),
            ],
        ),
        Nav(
            "📝 Decks",
            index=True,
            children=[
                Nav("Adeliz, the Cinder Wind", cat="tempo"),
                Nav("Aminatou, the Fateshifter", cat="controle"),
                Nav("Azusa, Lost but Seeking", cat="controle"),
                Nav("Bjorna-Wernog", cat="controle", crop=True),
                Nav("Dennick, Pious Apprentice", cat="midrange"),
                Nav("Doran, the Siege Tower", cat="midrange"),
                Nav("Dragonlord Ojutai", cat="controle"),
                Nav("Elmar-Hargilde", cat="midrange", crop=True),
                Nav("Elmar-Sophina", cat="agro", crop=True),
                Nav("Elminster", cat="controle"),
                Nav("Erinis, Gloom Stalker", cat="midrange", crop=True),
                Nav("Esika, God of the Tree", cat="controle"),
                Nav("Grist, the Hunger Tide", cat="midrange"),
                Nav("Gut, True Soul Zealot", cat="agro", crop=True),
                Nav("Hinata, Dawn-Crowned", cat="controle"),
                Nav("Hogaak, Arisen Necropolis", cat="agro"),
                Nav("Isamaru, Hound of Konda", cat="agro"),
                Nav("Ishai-Tevesh", cat="controle", crop=True),
                Nav("Jori En, Ruin Diver", cat="controle"),
                Nav("Juri, Master of the Revue", cat="agro"),
                Nav("Kari Zev, Skyship Raider", cat="agro"),
                Nav("Karlov of the Ghost Council", cat="agro"),
                Nav("Killian, Ink Duelist", cat="agro"),
                Nav("Kinnan, Bonder Prodigy", cat="combo"),
                Nav("Klothys, God of Destiny", cat="controle"),
                Nav("Light-Paws, Emperor's Voice", cat="combo"),
                Nav("Livio-Malcolm", cat="midrange", crop=True),
                Nav("Livio-Prava", cat="agro", crop=True),
                Nav("Maelstrom Wanderer", cat="combo"),
                Nav("Marath, Will of the Wild", cat="midrange"),
                Nav("Miara-Tevesh", cat="controle", crop=True),
                Nav("Minsc, Beloved Ranger", cat="combo"),
                Nav("❌ Minsc&Boo, Timeless Heroes", cat="ban"),
                Nav("Niv-Mizzet Reborn", cat="midrange"),
                Nav("Prossh, Skyraider of Kher", cat="combo"),
                Nav("Queen Marchesa", cat="midrange"),
                Nav("Raff, Weatherlight Stalwart", cat="midrange"),
                Nav("Raffine, Scheming Seer", cat="tempo"),
                Nav("Sai, Master Thopterist", cat="controle"),
                Nav("Saskia the Unyielding", cat="agro"),
                Nav("❌ Shorikai, Genesis Engine", cat="ban"),
                Nav("Soul of Windgrace", cat="controle"),
                Nav("Sygg, River Cutthroat", cat="controle"),
                Nav("Sythis, Harvest's Hand", cat="combo"),
                Nav("The Beamtown Bullies", cat="combo"),
                Nav("The Gitrog Monster", cat="combo"),
                Nav("The Reality Chip", cat="controle"),
                Nav("Tiamat", cat="combo"),
                Nav("Tivit, Seller of Secrets", cat="controle"),
                Nav("Wilson, Refined Grizzly", cat="agro", crop=True),
                Nav("Yoshimaru, Ever faithful", cat="agro", crop=True),
            ],
        ),
        Nav(
            "⏯️ Matchs",
            index=True,
            children=[
                Nav("1. Adeliz vs Kinnan", cat="01-10"),
                Nav("2. Kari Zev vs Saskia", cat="01-10"),
                Nav("3. Isamaru vs Gitrog", cat="01-10"),
                Nav("4. Livio-Malcolm vs Niv 5C", cat="01-10"),
                Nav("5. Jori En vs Sygg", cat="01-10"),
                Nav("6. Aminatou vs Klothys", cat="01-10"),
                Nav("7. Livio-Prava vs Ojutai", cat="01-10"),
                Nav("8. Esika vs Niv 5C", cat="01-10"),
                Nav("9. Miara-Tevesh vs Prossh", cat="01-10"),
                Nav("10. Kari Zev vs Marath", cat="01-10"),
                Nav("11. Doran vs Marchesa", cat="11-20"),
                Nav("12. Light Paws vs Ishai-Tevesh", cat="11-20"),
                Nav("13. Bjorna-Wernog vs Grist", cat="11-20"),
                Nav("14. Minsc vs ❌ Shorikai", cat="11-20"),
                Nav("15. Dennick vs Hinata", cat="11-20"),
                Nav("16. Aminatou vs Tiamat", cat="11-20"),
                Nav("17. Grist vs Sythis", cat="11-20"),
                Nav("18. Kari Zev vs Killian [Budget]", cat="11-20"),
                Nav("19. Elmar-Sophina vs ❌ Shorikai", cat="11-20"),
                Nav("20. Juri vs Sai", cat="11-20"),
                Nav("21. Aminatou vs Beamtown", cat="21-30"),
                Nav("22. Raffine vs Tivit", cat="21-30"),
                Nav("23. Karlov vs Reality Chip", cat="21-30"),
                Nav("24. Grist vs ❌ Minsc&Boo", cat="21-30"),
                Nav("25. Elminster vs Wilson", cat="21-30"),
                Nav("26. Hogaak vs ❌ Minsc&Boo", cat="21-30"),
                Nav("27. Jori En vs Maelstrom Wanderer", cat="21-30"),
                Nav("28. Azusa vs Elmar-Hargilde", cat="21-30"),
                Nav("29. Erinis vs Raff", cat="21-30"),
                Nav("30. Gut vs Yoshimaru", cat="21-30"),
                Nav("31. Raffine vs Soul of Windgrace", cat="31-40"),
            ],
        ),
        Nav(
            "📚 Articles",
            index=False,
            children=[
                Nav("Classifier un deck", cat="article"),
            ],
        ),
    ],
)


HELPER = dict(STRUCTURE.walk())
