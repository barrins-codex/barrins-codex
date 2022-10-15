import collections
import re

import unidecode

Page = collections.namedtuple("Page", ["name", "path", "url", "cat", "crop", "season"])


class Nav:
    def __init__(
        self, name, index=False, children=None, cat=None, crop=False, season="2"
    ):
        self.name = name
        self.index = index
        self.children = children or []
        self.cat = cat or ""
        self.crop = crop
        self.season = season

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
        return Page(self.name, res, url, self.cat, self.crop, self.season)

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
                    "season": self.season,
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
                Nav("Anaël « Aliquanto »", cat="invite", season="1"),
                Nav("Bastien « threem »", cat="invite", season="1"),
                Nav("Damien « eventwin »", cat="invite", season="1"),
                Nav("Domino", cat="habitue"),
                Nav("Félix « Midas »", cat="invite", season="1"),
                Nav("Florian « Trotte »", cat="invite", season="1"),
                Nav("Grégoire « Koraysh »", cat="invite", season="1"),
                Nav("Louis « Imperia86 »", cat="habitue"),
                Nav("Martin « Spigushe »", cat="habitue"),
                Nav("Apparitions", cat="invite", season="1"),
            ],
        ),
        Nav(
            "📝 Decks",
            index=True,
            children=[
                Nav("Adeliz, the Cinder Wind", cat="tempo", season="1"),
                Nav("Aminatou, the Fateshifter", cat="controle", season="1"),
                Nav("Azusa, Lost but Seeking", cat="controle", season="1"),
                Nav("Bjorna-Wernog", cat="controle", crop=True, season="1"),
                Nav("Dennick, Pious Apprentice", cat="midrange", season="1"),
                Nav("Doran, the Siege Tower", cat="midrange", season="1"),
                Nav("Dragonlord Ojutai", cat="controle", season="1"),
                Nav("Elmar-Hargilde", cat="midrange", crop=True, season="1"),
                Nav("Elmar-Sophina", cat="agro", crop=True, season="1"),
                Nav("Elminster", cat="controle", season="1"),
                Nav("Erinis, Gloom Stalker", cat="midrange", crop=True, season="1"),
                Nav("Esika, God of the Tree", cat="controle", season="1"),
                Nav("Grist, the Hunger Tide", cat="midrange", season="1"),
                Nav("Gut, True Soul Zealot", cat="agro", crop=True),
                Nav("Hinata, Dawn-Crowned", cat="controle", season="1"),
                Nav("Hogaak, Arisen Necropolis", cat="agro", season="1"),
                Nav("Isamaru, Hound of Konda", cat="agro", season="1"),
                Nav("Ishai-Tevesh", cat="controle", crop=True, season="1"),
                Nav("Jori En, Ruin Diver", cat="controle", season="1"),
                Nav("Juri, Master of the Revue", cat="agro", season="1"),
                Nav("Kari Zev, Skyship Raider", cat="agro", season="1"),
                Nav("Karlov of the Ghost Council", cat="agro", season="1"),
                Nav("Killian, Ink Duelist", cat="agro", season="1"),
                Nav("Kinnan, Bonder Prodigy", cat="combo", season="1"),
                Nav("Klothys, God of Destiny", cat="controle", season="1"),
                Nav("Light-Paws, Emperor's Voice", cat="combo", season="1"),
                Nav("Livio-Malcolm", cat="midrange", crop=True, season="1"),
                Nav("Livio-Prava", cat="agro", crop=True, season="1"),
                Nav("Maelstrom Wanderer", cat="combo", season="1"),
                Nav("Marath, Will of the Wild", cat="midrange", season="1"),
                Nav("Miara-Tevesh", cat="controle", crop=True, season="1"),
                Nav("Minsc, Beloved Ranger", cat="combo", season="1"),
                Nav("❌ Minsc&Boo, Timeless Heroes", cat="ban", season="1"),
                Nav("Niv-Mizzet Reborn", cat="midrange", season="1"),
                Nav("Prossh, Skyraider of Kher", cat="combo", season="1"),
                Nav("Queen Marchesa", cat="midrange", season="1"),
                Nav("Raff, Weatherlight Stalwart", cat="midrange", season="1"),
                Nav("Raffine, Scheming Seer", cat="tempo"),
                Nav("Sai, Master Thopterist", cat="controle", season="1"),
                Nav("Saskia the Unyielding", cat="agro", season="1"),
                Nav("❌ Shorikai, Genesis Engine", cat="ban", season="1"),
                Nav("Soul of Windgrace", cat="controle"),
                Nav("Sygg, River Cutthroat", cat="controle", season="1"),
                Nav("Sythis, Harvest's Hand", cat="combo", season="1"),
                Nav("The Beamtown Bullies", cat="combo", season="1"),
                Nav("The Gitrog Monster", cat="combo", season="1"),
                Nav("The Reality Chip", cat="controle", season="1"),
                Nav("Tiamat", cat="combo", season="1"),
                Nav("Tivit, Seller of Secrets", cat="controle", season="1"),
                Nav("Wilson, Refined Grizzly", cat="agro", crop=True, season="1"),
                Nav("Yoshimaru, Ever faithful", cat="agro", crop=True),
            ],
        ),
        Nav(
            "⏯️ Matchs",
            index=True,
            children=[
                Nav("1. Adeliz vs Kinnan", cat="01-10", season="1"),
                Nav("2. Kari Zev vs Saskia", cat="01-10", season="1"),
                Nav("3. Isamaru vs Gitrog", cat="01-10", season="1"),
                Nav("4. Livio-Malcolm vs Niv 5C", cat="01-10", season="1"),
                Nav("5. Jori En vs Sygg", cat="01-10", season="1"),
                Nav("6. Aminatou vs Klothys", cat="01-10", season="1"),
                Nav("7. Livio-Prava vs Ojutai", cat="01-10", season="1"),
                Nav("8. Esika vs Niv 5C", cat="01-10", season="1"),
                Nav("9. Miara-Tevesh vs Prossh", cat="01-10", season="1"),
                Nav("10. Kari Zev vs Marath", cat="01-10", season="1"),
                Nav("11. Doran vs Marchesa", cat="11-20", season="1"),
                Nav("12. Light Paws vs Ishai-Tevesh", cat="11-20", season="1"),
                Nav("13. Bjorna-Wernog vs Grist", cat="11-20", season="1"),
                Nav("14. Minsc vs ❌ Shorikai", cat="11-20", season="1"),
                Nav("15. Dennick vs Hinata", cat="11-20", season="1"),
                Nav("16. Aminatou vs Tiamat", cat="11-20", season="1"),
                Nav("17. Grist vs Sythis", cat="11-20", season="1"),
                Nav("18. Kari Zev vs Killian [Budget]", cat="11-20", season="1"),
                Nav("19. Elmar-Sophina vs ❌ Shorikai", cat="11-20", season="1"),
                Nav("20. Juri vs Sai", cat="11-20", season="1"),
                Nav("21. Aminatou vs Beamtown", cat="21-30", season="1"),
                Nav("22. Raffine vs Tivit", cat="21-30", season="1"),
                Nav("23. Karlov vs Reality Chip", cat="21-30", season="1"),
                Nav("24. Grist vs ❌ Minsc&Boo", cat="21-30", season="1"),
                Nav("25. Elminster vs Wilson", cat="21-30", season="1"),
                Nav("26. Hogaak vs ❌ Minsc&Boo", cat="21-30", season="1"),
                Nav("27. Jori En vs Maelstrom Wanderer", cat="21-30", season="1"),
                Nav("28. Azusa vs Elmar-Hargilde", cat="21-30", season="1"),
                Nav("29. Erinis vs Raff", cat="21-30", season="1"),
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
