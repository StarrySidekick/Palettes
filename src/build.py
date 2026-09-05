# -*- coding: utf-8 -*-
"""Build ../index.html from template.html plus the three data sources.

This used to be a chain of thirteen literal string substitutions applied to
`base.html`, which was itself a frozen earlier build of this page — so the
template was an output, the instruments deck could not be rebuilt from
`instruments.json` at all, and two patches could silently match each other's
search text. `template.html` is the hand-authored page now, and the build only
fills three named markers. Nothing here searches for prose it did not put there.
"""
import json, os, sys

# Every path below is relative to this file, so the build works from anywhere
# rather than only from inside src/.
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())

from pal2 import P
from wtitles import W as WTITLE

# Which deck looks itself up where. `wp` is Wikipedia (the item becomes a link,
# and the hover card carries a photo and a summary); `wt` is Wiktionary (not a
# link, one-sentence definition, click pins instead of navigating); absent is no
# lookup at all. The hint is the disambiguating term appended to a search.
LOOKUP = {"theory": ("wp", "music theory"), "production": ("wp", "audio production"),
          "genre": ("wp", "music genre"), "adjective": ("wt", ""), "abstract": ("wt", ""),
          "emotion": ("wt", ""), "verb": ("wt", "")}

ORDER_IDS = ["emotion", "theory", "adjective", "verb", "abstract", "production", "genre"]


def decks():
    """The seven word decks, as the shape the page's `WORD` global expects."""
    out = {}
    for k in ORDER_IDS:
        name, blurb, grouped, flat = P[k]
        mode, hint = LOOKUP.get(k, ("", ""))

        def item(word, cat):
            it = {"n": word, "c": cat}
            # Only a Wikipedia deck carries a title override; a Wiktionary deck
            # is looked up by the word itself, lowercased, at hover time.
            if mode == "wp":
                it["w"] = WTITLE.get(word, word)
            return it

        if flat is not None:
            out[k] = {"name": name, "blurb": blurb, "flat": 1, "order": [],
                      "lk": mode, "hint": hint,
                      "items": [item(w, "") for w in flat]}
        else:
            out[k] = {"name": name, "blurb": blurb, "order": list(grouped.keys()),
                      "lk": mode, "hint": hint,
                      "items": [item(w, cat) for cat, ws in grouped.items() for w in ws]}
    return out


def compact(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(',', ':'))


def main():
    page = open('template.html', encoding='utf-8').read()

    fills = [
        ('/*@INSTRUMENTS@*/', compact(json.load(open('instruments.json', encoding='utf-8')))),
        ('/*@WORDS@*/', compact(decks())),
        ('/*@ENGINES@*/', open('engines.js', encoding='utf-8').read()),
    ]

    for marker, text in fills:
        # Exactly once, or the template has drifted from this script and the
        # page would ship missing a deck or with two copies of the lookup layer.
        if page.count(marker) != 1:
            sys.exit('MARKER %s appears %d times in template.html, expected 1'
                     % (marker, page.count(marker)))
        page = page.replace(marker, text)

    open('../index.html', 'w', encoding='utf-8').write(page)
    word = decks()
    print(len(word), "word decks |", sum(len(v['items']) for v in word.values()),
          "words |", len(page), "chars")


if __name__ == '__main__':
    main()
