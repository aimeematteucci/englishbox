---
name: ddl-activity
description: Build English Box data-driven learning (DDL) lessons that teach Brazilian learners the difference between two easily confused English words or structures (can vs know, deal vs handle, make vs do, since vs for, say vs tell, borrow vs lend…). Produces an interactive student page with concordance lines, context sorting, rule discovery, situations, gap-fill dialogues, error correction and a SkELL corpus task, plus a classroom slide deck with teacher notes in Portuguese and a deploy-ready index.html, all in the English Box (@aimee.matteucci) visual identity. Use this skill whenever the user asks for a DDL activity, an "atividade baseada em corpus / concordância", a lesson showing "a diferença entre X e Y", a guided-discovery grammar or vocabulary task, or says "faz uma atividade dessa para…" after a previous DDL lesson, even if they don't say "DDL".
---

# DDL activity (English Box)

You are building a 50-minute guided-discovery lesson in which students look at real-looking English data, find the pattern themselves, and only then see the rule. The teacher (Aimee, English Box) approved a fixed structure and look; your job is the **content**. A template and a build script take care of the page, so all your effort goes into the language.

## Why the lesson works the way it does

DDL (Johns, 1991) is inductive: the teacher hands over data and guides noticing; the student builds the rule. Every design choice follows from that:

- The rule is **never shown first**. It appears only after students complete it themselves (the page hides the summary table until the rule is right).
- Concordance lines keep the key word in the middle so the eye can scan what comes **after** and **around** it. Sorting by next word / word before is the concordancer feature that makes patterns jump out.
- Instructions are short, plain English, step by step. Learners using DDL on their own get lost when instructions are vague (Zakiyah et al., 2026), so every task says exactly what to look at.
- The last step sends students to a real, free corpus tool (SkELL) so they can test the claims themselves.

## Workflow

### 1. Understand the contrast (ask only what is missing)

Defaults the teacher already chose, so don't ask about these: instructions in simple English only; about 50 minutes; English Box look; activity + slides + deploy file; SkELL as the student tool; preview first, publish later.

Ask (one message, multiple choice if the tool exists) only for what you can't infer:
- **Level**, if not obvious. Rough guide: basic modal/verb contrasts → A2; collocation and context contrasts → B1; subtle register contrasts → B2.
- **Focus**, when the pair allows both: grammar pattern (what follows each word) vs **context** of use (situations in which each is chosen). The teacher has liked context-focused lessons; for most vocabulary pairs, do both: grammar in Step 1, context as the heart of Steps 2–4.

### 2. Plan the language before writing anything

Work out, for yourself:
1. **The Portuguese interference.** Which single Portuguese word or structure covers both English options (saber → can/know; lidar com → deal with/handle)? That's the warm-up sentence and the source of the typical errors.
2. **The grammar signal** students can see in the lines (deal + *with*; handle + object; can + bare verb).
3. **2–4 contexts** that separate the two words. Each needs a short, kid-friendly label and a one-line description. Think about what really co-occurs in corpora: collocates (*well/badly*, *too much to*), subjects, typical objects, emotional tone.
4. **The overlap zone.** Real usage overlaps (deal with / handle a problem). Say so honestly and give the difference in focus. Gaps where both are natural accept both answers.
5. **The noun or other meanings** (a deal, a door handle) if they're frequent. Mention them, but don't let them take over.

Read `references/content-guide.md` for how to write each part well (lines, distractors, errors, level calibration, honesty rules).

### 3. Write the content JSON

Copy `examples/deal-vs-handle.json` (an approved lesson) and replace the content. Field-by-field notes are in `references/content-guide.md`. Key shapes:
- `concordance.lines`: `{l, k, r, w}`, left context / key word as written / right context / which key it belongs to. 8–12 lines per key.
- `classify.groups[].color`: `lime`, `yellow`, `sage` or `peach`. Use the same color for the same context in `rule.boxes`.
- Gaps in `texts`: `[[answer]]` or `[[answer/alternative]]`. Every answer must be in that text's `W` list.

### 4. Write the slides

Write only the `<section class="slide …">` elements (12 slides, same arc as the activity) into a `.slides.html` file. Start from `examples/deal-vs-handle.slides.html` and read `references/slides.md` for the available components. Teacher notes (`data-notes`) are in **Portuguese**, saying what to ask, what answer to expect, and how long to spend.

### 5. Build and check

```bash
python3 <skill>/scripts/build.py content.json --slides content.slides.html --out <repo>/activities/<slug>
node <skill>/scripts/check.js <repo>/activities/<slug> <scratchpad>/shots   # needs Playwright
```

`build.py` validates the content first (every answer present, one correct option per question, gap answers in their word lists, colors valid) and writes nothing if something is wrong. Fix what it reports. `check.js` loads the pages and fails on script errors, horizontal overflow on a phone, or text spilling out of a slide. It also fails on concordance lines cut off with “…”. Then look at the section screenshots it saves (`activity-notice.png`, `activity-rule.png`, …) and the concordance and rule slides, checking that formulas match their examples, before showing the teacher. If `check.js` can't run (no Playwright), say so.

Output folder:
```
activities/<slug>/
  activity.html        student page
  slides.html          teacher deck (arrows/click to advance, N for notes)
  deploy/index.html    standalone copy of the student page, for publishing
```

### 6. Preview, then publish

Send the teacher `activity.html` and `slides.html` as a rendered preview, plus a short summary **in Portuguese** of what each step does and any judgment calls (level chosen, overlap answers accepted, lines shortened). Don't publish until the teacher approves. Only the **student activity** is published, to the student tasks site (tasks-students.englishboxcomunidade.com), using `deploy/index.html`. If you don't know that site's deploy steps, ask; don't guess. If the work lives in a git repo, commit to the working branch.

## Honesty rules (non-negotiable, because students and the teacher trust the data)

- The lines are **adapted from common corpus patterns**, not quotations from a corpus. The footer says this; never claim otherwise.
- Never invent frequency numbers. Comparative statements ("much more common") are fine only when they're clearly true of English, and the SkELL step lets students check them.
- If a "wrong" sentence is actually acceptable in some register, don't mark it wrong. Pick another error.
