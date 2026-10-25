# Writing the content

The page has a fixed sequence. Each section below says what the JSON field holds and what makes it good.

## Top level
- `slug`: folder name and storage key, e.g. `make-vs-do`.
- `title`: tab/gallery name, e.g. `Make or Do?`. `h1`: same with the connector in italics: `Make <i>or</i> do?`.
- `lede`: two short sentences naming the Portuguese problem and the promise ("In Portuguese, both are “fazer”. In English, …").
- `level`: `A2`, `B1`, ….
- `duration`: optional label in the header (default “About 50 minutes”).
- `times`: optional overrides, e.g. `{"classify": "10 min"}` (defaults: notice 10, classify 8, rule 5, context 12, errors 8, explore 5 + homework).

## Warm-up (`warmup`)
One Portuguese sentence (`pt`, key word in `<i>`) that triggers the interference, and 3 English options: the typical Brazilian error plus one or two correct versions. Each option has a `msg` shown at the end of the lesson that explains why it is right or wrong **in terms of what students discovered**. `close` is the oral exit task ("Tell a partner …"). Having two correct options (like *I can't deal with it* / *I can't handle it*) is a great setup for a context lesson.

## Concordance (`concordance`)
- `keys`: the two words, `{id, label}`. The first is shown first.
- 8–12 lines per key, sorted so the first few make the main pattern obvious and later ones add contexts, the overlap and the noun/other meaning.
- `k` is the word exactly as written (`can't`, `handled`, `Deals`); `w` groups it under its key id.
- Make the **right side start with the signal** (with / a verb / an object) so “sort by next word” groups them. Put the collocates you want noticed **around** the key word (can, too much, well, tomorrow, stress).
- Everyday, teen-and-adult-friendly topics: school, work, family, phones, football, travel, food. Brazilian touches are welcome (Neymar, reais, Rio). Vary subjects (I, she, my mom, nurses, the government).
- Length: A2 lines under ~12 words total; B1 can be longer. A left context longer than ~40 characters gets cut on screen, so keep the important word close to the key.
- A line can start a sentence: use `"l": ""`.

## Noticing questions (`notice`)
Not every pair has a visible grammar signal (make/do, say/tell partly, borrow/lend). Then start from **what follows** (the kinds of nouns: food vs work) or **who does what** (who gives, who receives), and use the grammar question only if there is one.
3–5 multiple-choice questions, each telling students which filter to use ("Show “handle”. …"). Order: the grammar signal first, then what kinds of words follow, then the collocates around, then the noun or other meaning. Exactly one option has `"ok": true`. `ok` is the praise plus the generalisation in bold; `no` is a hint that sends them back to the data (never the answer). An option can carry its own `why`.

## Classify (`classify`)
- `kicker` (after “Step 2 ·”, e.g. “Find the context”), `title` (the h2, e.g. “Four contexts”), `task` (one instruction line).
- 2–4 `groups` = the contexts (or the grammar categories for a grammar-focused pair). `title` + `desc` show in the legend; `chip` is the short button label.
- 9–10 `items`, sentences from the lines with the key phrase in `<mark>`. Mix the order. Each group gets at least 2.
- The legend does **not** name the verb. The `after` question then asks which verb appeared in each group, so students connect context → word themselves.

## Rule (`rule`)
- `lines`: 3–5 sentences with one dropdown each (`pre`, `opts`, `a`, `post`). Grammar first, then contexts.
- `boxes`: the summary table, one per context, with the same `color` as its classify group. `f` formula (mono), `ex` examples, `pt` Portuguese gloss.
- `both`: the overlap explanation (HTML; start with `<b>…</b>` and use `<span>` per line). Leave it out if there's no real overlap.
- `never`: the two classic errors struck out.
- `hint`: the noun / other meanings, or a frequency note you can stand behind.

## Situations (`situations`)
6–8 mini-contexts in which **the situation decides**, not the grammar: a one-line context `c`, a sentence `s` with `___`, two options `o` (same form so grammar doesn't give it away, unless the point is grammar), answer index `a`, and `why` naming the context in bold. Cover every context at least once and include one capacity/emotion contrast that is obviously different.

## Dialogues and a text (`texts`)
Two short dialogues (5–6 turns, named people, realistic: a job, exams, a trip, a shop) and one prose text (a blog post, a profile, an ad). `W` is the dropdown list, and include inflected forms as distractors. `textsTitle` is the h2 above them (e.g. “Dialogues and a blog post”). Write gaps as `[[answer]]`; if both are natural, `[[a/b]]`. Make most gaps decidable by context or by a visible signal (a following *with*), and keep accept-both gaps rare. `textsTip` is the hint shown after a wrong check.

## Errors (`errors`)
8–9 sentences: about 5–6 typical Brazilian errors caused by the Portuguese word (`ok: false`, with `fix` and `why`) and 3 correct ones, including at least one **trap** that looks wrong but is right (*Handle the box with care.*). Errors must be genuinely wrong in standard English. `fix` can offer two corrections separated by ` / `.

## SkELL (`skell`)
4–5 steps that let students verify the lesson in https://skell.sketchengine.eu/: search each phrase, use **Word sketch** for collocates, search the collocation from the lesson (*handled well*), and finish with personal sentences that mirror the exit task. Put search terms in `<code>`. `notesPlaceholder` and `mePlaceholder` are the example texts shown in the two empty note boxes.

## Level calibration
- **A2**: shorter lines, very common verbs, 3 groups max, simpler `why` texts, situations optional.
- **B1+**: four contexts, an overlap box, idiomatic noun uses, longer texts.

Sample A2 lines (can vs know):
`{"l": "My little sister is only five, but she", "k": "can", "r": "swim really well.", "w": "can"}`
`{"l": "Excuse me, do you", "k": "know", "r": "where the bus station is?", "w": "know"}`
`{"l": "My son", "k": "knows", "r": "how to fix computers. He learned on YouTube.", "w": "know"}`
