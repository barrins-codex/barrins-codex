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
            url = res
        elif self.index:
            url = res + "/index"
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
                Nav("Alexandre « OneSauk »", cat="invite"),
                Nav("Anaël « Aliquanto »", cat="invite"),
                Nav("Bastien « threem »", cat="invite"),
                Nav("Damien « eventwin »", cat="invite"),
                Nav("Domino", cat="habitue"),
                Nav("Félix « Midas »", cat="invite"),
                Nav("Florian « Trotte »", cat="invite"),
                Nav("Grégoire « Koraysh »", cat="invite"),
                Nav("Jules « Askeladden »", cat="invite"),
                Nav("Louis « Imperia86 »", cat="habitue"),
                Nav("Martin « Spigushe »", cat="habitue"),
                Nav("Nicolas « NicolasP »", cat="invite"),
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
                Nav("Cecily-Wernog", cat="combo", crop=True),
                Nav("Dennick, Pious Apprentice", cat="midrange"),
                Nav("Doran, the Siege Tower", cat="midrange"),
                Nav("Dragonlord Ojutai", cat="controle"),
                Nav("Elmar-Hargilde", cat="midrange", crop=True),
                Nav("Elmar-Sophina", cat="agro", crop=True),
                Nav("Elminster", cat="controle"),
                Nav("Erinis, Gloom Stalker", cat="midrange", crop=True),
                Nav("Esika, God of the Tree", cat="controle"),
                Nav("Ghyrson Starn, Kelermorph", cat="agro"),
                Nav("Grenzo, Dungeon Warden", cat="combo"),
                Nav("Grist, the Hunger Tide", cat="midrange"),
                Nav("Gut, True Soul Zealot", cat="agro", crop=True),
                Nav("Hinata, Dawn-Crowned", cat="controle"),
                Nav("❌ Hogaak, Arisen Necropolis", cat="ban"),
                Nav("Isamaru, Hound of Konda", cat="agro"),
                Nav("Ishai-Tevesh", cat="controle", crop=True),
                Nav("Jori En, Ruin Diver", cat="controle"),
                Nav("Juri, Master of the Revue", cat="agro"),
                Nav("Kari Zev, Skyship Raider", cat="agro"),
                Nav("Karlov of the Ghost Council", cat="agro"),
                Nav("Killian, Ink Duelist", cat="agro"),
                Nav("Kinnan, Bonder Prodigy", cat="combo"),
                Nav("Klothys, God of Destiny", cat="controle"),
                Nav("Kroxa, Titan of Death's Hunger", cat="midrange"),
                Nav("Leovold, Emissary of Trest", cat="controle"),
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
                Nav("Shanna, Purifying Blade", cat="agro"),
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
                # Il faut garder les matchs dans l'ordre chronologique
                Nav("Adeliz vs Kinnan", cat="match"),
                Nav("Kari Zev vs Saskia", cat="match"),
                Nav("Isamaru vs Gitrog", cat="match"),
                Nav("Livio-Malcolm vs Niv 5C", cat="match"),
                Nav("Jori En vs Sygg", cat="match"),
                Nav("Aminatou vs Klothys", cat="match"),
                Nav("Livio-Prava vs Ojutai", cat="match"),
                Nav("Esika vs Niv 5C", cat="match"),
                Nav("Miara-Tevesh vs Prossh", cat="match"),
                Nav("Kari Zev vs Marath", cat="match"),
                Nav("Doran vs Marchesa", cat="match"),
                Nav("Light Paws vs Ishai-Tevesh", cat="match"),
                Nav("Bjorna-Wernog vs Grist", cat="match"),
                Nav("Minsc vs ❌ Shorikai", cat="match"),
                Nav("Dennick vs Hinata", cat="match"),
                Nav("Aminatou vs Tiamat", cat="match"),
                Nav("Grist vs Sythis", cat="match"),
                Nav("Kari Zev vs Killian [Budget]", cat="match"),
                Nav("Elmar-Sophina vs ❌ Shorikai", cat="match"),
                Nav("Juri vs Sai", cat="match"),
                Nav("Aminatou vs Beamtown", cat="match"),
                Nav("Raffine vs Tivit", cat="match"),
                Nav("Karlov vs Reality Chip", cat="match"),
                Nav("Grist vs ❌ Minsc&Boo", cat="match"),
                Nav("Elminster vs Wilson Simic", cat="match"),
                Nav("❌ Hogaak vs ❌ Minsc&Boo", cat="match"),
                Nav("Jori En vs Maelstrom Wanderer", cat="match"),
                Nav("Azusa vs Elmar-Hargilde", cat="match"),
                Nav("Erinis Selesnya vs Raff", cat="match"),
                Nav("Gut Boros vs Yoshimaru Boros", cat="match"),
                Nav("Raffine vs Soul of Windgrace", cat="match"),
                Nav("Grenzo vs Shanna", cat="match"),
                Nav("Juri vs Wilson Simic", cat="match"),
                Nav("Grist vs Raffine", cat="match"),
                Nav("Cecily-Wernog vs Kroxa", cat="match"),
                Nav("Ghyrson vs Niv-Mizzet", cat="match"),
                Nav("Leovold vs Yoshimaru Naya", cat="match"),
                # Il faut garder les matchs dans l'ordre chronologique
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
