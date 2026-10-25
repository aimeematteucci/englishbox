# Slides

The deck is 1600×900, scaled to the window. You write only the `<section>` elements; `build.py` wraps them in the template (fonts, grain, navigation, notes panel). See `examples/deal-vs-handle.slides.html` for a complete approved deck.

## The 12-slide arc
1. Title (green): kicker “Today's question”, `<h1>X <i>or</i><br>Y?</h1>`, a one-line promise.
2. Warm-up (paper): pill question, `<h2>` with the Portuguese sentence, three `.bub` options A/B/C.
3. Concordance for word 1 (paper), 6 lines, then a `.step` question.
4. Concordance for word 2 (paper), same.
5. “What did you notice?” (green): `.qs` list with `.ans.step` reveals.
6. Groups/contexts (paper): `.three` or `.four` boxes, then a `.step` question.
7. The rule (paper): `.two`/`.three` boxes revealed as a `.step`, then `.never`.
8. The nuance (green): frequency, the overlap or the “know how to” note.
9. Practice (paper): `.sits` situations or a dialogue with blanks and a `.step` answer line.
10. Correct or wrong (paper): `.errs` grid with `.step` corrections.
11. SkELL (green): `.url` and `.steps-list`.
12. Back to the start (green): the warm-up sentence, the answer as a `.step`, the exit task.

## Slide shell
```html
<section class="slide p" data-notes="Português: o que perguntar, resposta esperada, tempo.">
  <div class="corner l">@aimee.<i>matteucci</i><br><b>English Box</b></div>
  <div class="kick" style="margin-top:20px">Step 1 · Look at the data</div>
  …
</section>
```
`g` = green editorial slide, `p` = paper slide. Slide 1 also gets `<div class="corner r">Data-Driven<br><b>Learning</b></div>`.

## Components
- `.kick`: condensed caps kicker. `.pill`: lime label with a black border. `h1` (180px), `h2` (84px), `<i>` for emphasis. `.big`: 40px body. `.small`. `.hl`: sage highlighter. `.mt-auto`: pushes to the bottom.
- `.bubbles > .bub > small`: speech bubbles for warm-up options. Keep each option under ~30 characters; for longer options use `<div class="bubbles compact">` (40px). If it still overflows, shorten the sentence. Avoid inline style overrides.
- `.conc`: concordance. Repeat `<span class="l">…</span><span class="k">word</span><span class="r"><u>next</u> rest</span>`. **Keep each line short** (left ≤ ~30 characters, right ≤ ~32) or it spills out of the box; shorten lines from the activity if needed.
- Boxes: wrapper `.two` / `.three` / `.four`, each child `.box` plus a color: `b-can` (lime), `b-know` (yellow), `b-how` (sage), `b-d` (peach). Inside: `.t` title, `.f` mono formula, `.e` example, `.pt` Portuguese gloss.
- `.qs` (ordered list) with `<span class="ans step hide">`. On green slides set `style="color:var(--cream);font-weight:700"` on `.ans`.
- `.errs`: `<div><span>wrong sentence</span><b class="step hide">→ fix</b></div>`.
- `.sits`: `<div><span class="c">context</span><span>“sentence ______”</span><b class="step hide">answer · context</b></div>`.
- `.never` (struck-out errors with `<s>`), `.url`, `.steps-list` with `<code>`.

## Reveals
Any element with `class="step hide"` appears on the next click or → key, in document order. Use reveals for answers so the teacher can elicit first.
