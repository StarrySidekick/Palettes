# Intent

What this is for, and what to build next. Recorded **2026-09-06** from Timothy's
own answers to a direct set of questions, so this is *stated* intent rather than
intent inferred from the code.

**Read this before choosing what to build.** Where it disagrees with the rest of
the docs about **direction**, this file is newer and wins. Where it disagrees
about **mechanics** — how the code works, what was decided deliberately, the
invariants — the other docs win, always.

When something here is done, or turns out to be wrong, **edit it**. A stale
intent file is worse than no intent file.

## What it is for

Timothy's own music brainstorming. **He does not reach for it yet**, mostly
because he has not been making much music, and because it is very early.

## What is next

Two concrete things, both his:

**1. Make it mobile-friendly.** The real use case is **sitting at the piano with
a phone in hand.** This is the single most useful change available in this repo,
and the page is currently a desktop page.

**2. A piano practice mode.** ~~Shuffles scales, modes and keys, plus other
random things to practise.~~ **Built 2026-09-06** — the *Practise* button, or `T`
from the list, `N` for another. It deals a key, a scale or mode, something to do
with it, and about four times in seven a constraint that changes how it feels.
Twelve keys with practical spellings, twenty scales, twenty tasks, eleven
twists. It belongs to no deck, because what you sit down to practise has nothing
to do with which words you were sweeping, and nothing is stored, because a
practice card you have to keep is a chore list.

What it does not do yet, if this wants going further: it cannot hear you, it
does not know what you practised last week, and it has no notion of difficulty
— so it will hand a beginner the altered scale in G flat. Any of those would be
a real next step; none is obviously wanted yet.

## Do not forget the build

`index.html` is **generated**. Edit `src/template.html` and `src/pal2.py`, then:

```bash
cd src && python3 build.py && python3 check.py
```

`check.py` asserts the shipped page is what the build produces. The failure mode
this guards is editing the generated `index.html` by hand and losing the work on
the next build, and the marker system exists because the previous chain of
thirteen string substitutions had already corrupted itself in real use. See
`HANDOFF.md` §3.

## Where it is going

Personal for now, public when it is good enough. **Eventually linked from his
website**, like every other project.
