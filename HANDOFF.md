# Palettes — handoff to Claude Code

> **Read [`INTENT.md`](INTENT.md) first.** It records what this project is for
> and what Timothy wants next, in his own words, dated. Where it disagrees with
> this file about *direction* it is newer and wins; where it disagrees about
> *mechanics* — how the code works, what was decided deliberately, the
> invariants — this file wins.

A single-page music brainstorming tool: eight switchable decks of words and instruments,
each of which explains itself on hover by calling Wikipedia / Wiktionary from the
viewer's browser. Built in a Cowork session; this bundle is everything needed to host it
and keep working on it.

**Goal for this handoff: get `index.html` live on GitHub Pages, then keep editing the
decks from `src/`.**

---

## 1. Deploy it (5 minutes, nothing to compile)

`index.html` is complete and self-contained — no build step, no dependencies, no API
keys, no secrets. It is ready to serve as-is.

```bash
cd palettes
git init && git add . && git commit -m "Palettes: music brainstorming decks"
gh repo create palettes --public --source=. --push
gh api -X POST repos/:owner/palettes/pages -f 'source[branch]=main' -f 'source[path]=/'
```

Then confirm Pages is on (Settings → Pages → Deploy from branch `main`, folder `/root`).
Live at `https://<user>.github.io/palettes/` within a minute or two.

**Why hosting matters here, beyond convenience:** the page fetches from Wikipedia and
Wiktionary at hover time. Opened as a local `file://` document those requests are
frequently blocked, and on iOS a downloaded `.html` opens in a Quick Look preview where
the JavaScript barely runs at all. Served over HTTPS, everything works, including on
phones — this was the specific reason for moving to Pages.

`.nojekyll` is not required (no underscore-prefixed paths), but adding an empty one is
harmless insurance.

---

## 2. What's in the bundle

```
palettes/
  index.html              ← THE DEPLOYABLE. 257 KB, self-contained, generated.
  HANDOFF.md              ← this file
  src/
    build.py              ← generates ../index.html.  `cd src && python3 build.py`
    check.py              ← asserts index.html is what build.py produces
    template.html         ← THE PAGE. Hand-authored. Edit the HTML/CSS/JS here.
    engines.js            ← the Wikipedia + Wiktionary lookup layer, injected by build.py
    pal2.py               ← ALL SEVEN WORD DECKS live here. Edit this for content.
    pal_data.py           ← older deck source that pal2.py imports and reshapes
    emo.py                ← raw emotion word source
    emo_final.txt         ← deduped emotion list pal2.py reads
    abstract_clean.json   ← deduplicated Abstract Nouns, baked
    dedup.py              ← category-assignment + replacement pools for the dedup pass
    wtitles.py            ← 277 Wikipedia title overrides for Theory/Production/Genres
    instruments.json      ← the 1000 instruments (name, family, role, region, wiki title)
    research/             ← raw research output per region, kept for provenance
```

Verified: a clean `python3 build.py` reproduces the shipped `index.html` byte-for-byte.

---

## 3. The build

`build.py` reads `template.html` and fills **three named markers**:

| Marker | Filled from |
|---|---|
| `/*@INSTRUMENTS@*/` | `instruments.json` — the 1000 instruments |
| `/*@WORDS@*/` | `pal2.py` + `wtitles.py`, via `decks()` |
| `/*@ENGINES@*/` | `engines.js` — the Wikipedia/Wiktionary lookup layer |

Each marker must appear exactly once or the build exits, because a template that
has drifted from the script would otherwise ship a page missing a deck or
carrying two copies of the lookup layer.

`cd src && python3 build.py` writes `../index.html`. `python3 check.py` asserts
that the shipped page is what the build produces — run it before committing,
since the failure mode here is editing the generated `index.html` by hand and
losing the work on the next build.

**This replaced a chain of thirteen literal string substitutions applied to a
`base.html` that was itself a frozen earlier build of this page.** That
arrangement had three problems, and all three are gone:

- The template was an *output*, which made the whole thing circular.
- **The instruments deck could not be rebuilt at all.** `const DATA=[…]` was
  baked into `base.html`, so `instruments.json` sat in the tree unread. It is
  live source again.
- Patches searched for prose they did not put there, so two of them could match
  each other's search text and silently corrupt the next one's pattern. It had
  already failed that way in real use. Nothing searches for arbitrary text now.

`base.html` is deleted — it was generated, and keeping it would mean keeping it
in sync with a template that has replaced it. It is in git history if needed.

The rewrite was verified by reproducing the shipped 257 KB `index.html`
**byte for byte**, then loading the result in a browser with the live APIs
blocked and confirming all eight tabs and their counts (Emotions 611, Verbs 638,
Genres 298).

## 4. Editing content

Almost all content edits happen in **`src/pal2.py`**, then `python3 build.py`.

**The practice deck is the exception.** Its keys, scales, tasks and twists are
hand-authored lists near `modePractise()` in `src/template.html`, not in
`pal2.py`, because they are not a word deck — nothing looks them up, nothing
pins them, and they are read as sentences rather than browsed as a list.

Each deck is `P['id'] = (name, blurb, categories_dict, flat_list)`.
Use `categories_dict` OR `flat_list` — the other is `None`.

```python
P['verb'] = ("Verbs", "What the music does.", {
    "Break": ["Shatter", "Crack", ...],
    "Build": ["Construct", ...],
}, None)

P['emotion'] = ("Emotions", "One feeling, aimed at.", None, ["Abandon", "Awe", ...])
```

Deck order and lookup mode are set at the top of `build.py`:

```python
ORDER_IDS = ["emotion","theory","adjective","verb","abstract","production","genre"]
LOOKUP = {"theory":("wp","music theory"), "production":("wp","audio production"),
          "genre":("wp","music genre"), "adjective":("wt",""), "abstract":("wt",""),
          "emotion":("wt",""), "verb":("wt","")}
```

- `wp` = Wikipedia (item becomes a link; hover shows photo + summary)
- `wt` = Wiktionary (item is not a link; hover shows a one-sentence definition; **click
  pins** instead of navigating)
- absent = no lookup at all

The Instruments deck is separate — it reads `instruments.json` and has its own audio and
article-verification machinery.

### Content rules that are already enforced — don't regress them
- **`wt` decks must contain single words only.** Multi-word entries were stripped because
  Wiktionary has no entry for invented compounds like "grateful grief".
- **Emotions and Abstract Nouns must not overlap.** Emotions holds *felt states*,
  Abstract Nouns holds *concepts*. 81 shared words were resolved on that principle.
- **No word appears twice inside one deck.** Enforced by a pass at the bottom of
  `pal2.py`.
- **Words repeating across *unrelated* decks are intentional.** "Drop" is a Theory term,
  a Production move, and a Verb. Do not globally deduplicate.

---

## 5. How the runtime works

No backend. No keys. Everything is fetched client-side, on hover, from public APIs.

| Deck | Source | Endpoint |
|---|---|---|
| Instruments | Wikipedia + Wikimedia Commons | `en.wikipedia.org/w/api.php` |
| Theory, Production, Genres | Wikipedia | same |
| Emotions, Adjectives, Verbs, Abstract Nouns | Wiktionary | `en.wiktionary.org/api/rest_v1/page/definition/` |

**Instruments deck, at page load:**
1. Batches all 1000 titles, 20 per call (the TextExtracts extension caps multi-page
   requests at 20 when `exintro`/`exsentences` are used) → ~50 calls.
2. Any title that 404s triggers a Wikipedia **search fallback** that repairs the link in
   place. Needed for ambiguous names — Gender, Tres, Anvil, Spoons, Bones.
3. Entries with no article at all are **hidden**, and a toggle reveals them.
   A missing *picture* is explicitly NOT grounds for exclusion (changed by request).
4. Then discovers audio via `prop=images` per article.

**Two runtime details that are load-bearing — do not "simplify" them:**

- **Audio filtering.** Instrument articles carry Spoken-Wikipedia narrations
  (`En-*.ogg`, someone reading the article aloud) and Lingua Libre pronunciation clips
  (`LL-Q*.wav`, someone saying the word). Neither is the instrument. They are rejected by
  pattern in `base.html`'s `JUNK` array. Remove that and playback becomes maddening.
- **MP3 transcode first.** Commons audio is mostly Ogg Vorbis, which Safari cannot
  decode. Playback requests the Commons auto-transcoded
  `.../transcoded/<path>/<file>.ogg.mp3` before falling back to the original. Without
  this the whole feature is silent on Mac and iOS.
- **Wiktionary is case-sensitive.** Words are stored Title Case but looked up **lowercase
  first** — "Frigid" 404s where "frigid" exists. This one bug made nearly every
  definition fail until it was found.
- **Part of speech is per-deck.** Adjectives asks for the adjective sense, Verbs for the
  verb, everything else for the noun. Otherwise "Frigid" defines as "a frigid person".

Offline / blocked-network behavior is deliberate: nothing is hidden, links still resolve
from pre-built titles, and the status pill reads
"no Wikipedia access here — links still work".

---

## 6. Features to preserve

- **Eight decks** via the tab row. Instruments additionally regroups three ways
  (family / sonic role / tradition).
- **Five draw modes**: Brief (one item from *every* deck — the most useful one),
  Roll 3, Collide (two items forced together), Focus (one item full-screen), Shuffle
  (breaks alphabetical order).
- **Pin tray** — collect items across decks, copy them out. `wt` decks pin on click;
  everything has a pin button in the hover card.
- **Keyboard**: `B` brief, `R` roll, `N` next in focus, `P` pin, `Esc` close.
- **Print CSS** — 5 dense columns, all controls hidden. The instruments deck prints to
  ~5 pages. Don't let a redesign break this; it's a real use case.
- **Theme-aware** via `prefers-color-scheme`.

---

## 7. Testing

`src/check.py` guards the build. Beyond that there is still no test suite.

The session that built this used Playwright with a **mocked** Wikipedia/Wiktionary
layer, which is the right approach — it makes tests fast, offline, and able to simulate failure modes
(missing article, missing image, Title-Case 404, network down). Worth reconstructing:

```js
await page.route('**/en.wikipedia.org/**', route => route.fulfill({...}));
await page.route('**/en.wiktionary.org/**', route => route.fulfill({...}));
```

Cases that caught real bugs and are worth keeping:
- Title Case 404s but lowercase resolves (Wiktionary casing)
- A deck item whose article is missing → search fallback fires, link repairs
- Network fully blocked → graceful message, links still present
- `#focus` overlay hidden but still intercepting clicks (needed `#focus[hidden]{display:none}`)
- Print output still paginates to the expected page count

---

## 8. Known gaps / backlog

- **Coverage is unverified.** Wikipedia was cache-only from the Cowork sandbox, so the
  1000 instrument titles and the Commons audio hit-rate have never been checked against
  the live API. The page self-reports both ("N kept of 1000", "N with sound") — read
  those numbers once it's live and fix the stragglers.
- **`wtitles.py` covers 277 overrides.** Anything missed falls through to search. Once
  live, spot-check Theory/Production/Genres for words that land on the wrong article.
- ~~Replace the substitution-chain build.~~ Done — see §3.
- **The rhythm/composition checklist was never built.** This whole palette started as
  step one of a larger "music composition and production sheet" whose actual purpose was
  catching the habit of over-focusing on melody and forgetting rhythm. That deliverable
  is still outstanding — see `music/composition-sheet-notes.md` in the Claude project.
- **Emotions capped at 611**, deliberately short of the 1000 ceiling; padding further
  would mean admitting adjectives and abstract nouns, which the deck explicitly excludes.
- Consider a service worker so the page works offline once visited.
- Consider `localStorage` for the pin tray so pins survive a reload.
