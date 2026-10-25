#!/usr/bin/env python3
"""Build an English Box DDL activity from a content JSON file.

Usage:
  python3 build.py <content.json> --out <folder> [--slides <slides-sections.html>]

Writes:
  <folder>/activity.html        student page (artifact style: no <html>/<head> wrapper)
  <folder>/deploy/index.html    the same page as a complete standalone HTML document
  <folder>/slides.html          classroom deck (only with --slides)

The content is validated first; any problem is printed and nothing is written.
"""
import argparse, json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ACT_TPL = HERE / "assets" / "activity-template.html"
SLD_TPL = HERE / "assets" / "slides-template.html"
COLORS = {"lime", "yellow", "sage", "peach"}


def validate(d):
    p = []
    for k in ["slug", "title", "h1", "lede", "level", "warmup", "concordance", "notice",
              "classify", "rule", "texts", "errors", "skell"]:
        if k not in d:
            p.append(f"missing top-level key: {k}")
    if p:
        return p
    if not re.fullmatch(r"[a-z0-9-]+", d["slug"]):
        p.append("slug must be lowercase letters, digits and hyphens")

    w = d["warmup"]
    if len(w.get("options", [])) < 2:
        p.append("warmup needs at least 2 options")
    for i, o in enumerate(w.get("options", [])):
        if not o.get("msg"):
            p.append(f"warmup option {i} has no end-of-lesson msg")

    c = d["concordance"]
    ids = [k["id"] for k in c["keys"]]
    for i, ln in enumerate(c["lines"]):
        if ln.get("w") not in ids:
            p.append(f"concordance line {i} has w={ln.get('w')!r}, not one of {ids}")
        for f in ("l", "k", "r"):
            if f not in ln:
                p.append(f"concordance line {i} missing {f!r}")
    for k in ids:
        n = sum(1 for ln in c["lines"] if ln.get("w") == k)
        if n < 5:
            p.append(f"concordance key {k!r} has only {n} lines (aim for 8-12)")

    def check_mcq(q, where):
        oks = [o for o in q["opts"] if o.get("ok")]
        if len(oks) != 1:
            p.append(f"{where}: needs exactly one option with ok:true (has {len(oks)})")
        if not q.get("ok"):
            p.append(f"{where}: missing 'ok' feedback")
        if not q.get("no") and not all(o.get("why") for o in q["opts"] if not o.get("ok")):
            p.append(f"{where}: missing 'no' feedback")

    for i, q in enumerate(d["notice"]):
        check_mcq(q, f"notice question {i+1}")

    k = d["classify"]
    gids = [g["id"] for g in k["groups"]]
    if not 2 <= len(gids) <= 4:
        p.append("classify needs 2 to 4 groups")
    for g in k["groups"]:
        if g.get("color") not in COLORS:
            p.append(f"classify group {g['id']!r}: color must be one of {sorted(COLORS)}")
    for i, it in enumerate(k["items"]):
        if it.get("a") not in gids:
            p.append(f"classify item {i} answer {it.get('a')!r} is not a group id")
    for g in gids:
        if not any(it.get("a") == g for it in k["items"]):
            p.append(f"classify group {g!r} has no items")
    if k.get("after"):
        check_mcq(k["after"], "classify 'after' question")

    r = d["rule"]
    for i, ln in enumerate(r["lines"]):
        if ln["a"] not in ln["opts"]:
            p.append(f"rule line {i}: answer {ln['a']!r} not in opts")
    for i, b in enumerate(r.get("boxes", [])):
        if b.get("color") not in COLORS:
            p.append(f"rule box {i}: bad color")

    for i, s in enumerate(d.get("situations", [])):
        if not 0 <= s.get("a", -1) < len(s.get("o", [])):
            p.append(f"situation {i}: answer index out of range")

    for t in d["texts"]:
        W = [x.lower() for x in t["W"]]
        src = t.get("prose") or " ".join(s for _, s in t.get("turns", []))
        gaps = re.findall(r"\[\[([^\]]+)\]\]", src)
        if not gaps:
            p.append(f"text {t['h']!r} has no [[gaps]]")
        for g in gaps:
            for alt in g.lower().split("/"):
                if alt not in W:
                    p.append(f"text {t['h']!r}: gap answer {alt!r} is not in its word list W")

    for i, e in enumerate(d["errors"]):
        if e.get("ok") is False and not e.get("fix"):
            p.append(f"error sentence {i} is wrong but has no 'fix'")
        if not e.get("why"):
            p.append(f"error sentence {i} has no 'why'")
    if not any(e.get("ok") for e in d["errors"]):
        p.append("errors: include some correct sentences too, so students must think")

    if not d["skell"].get("steps"):
        p.append("skell needs steps")
    return p


def standalone(page):
    head_end = page.index("</style>") + len("</style>")
    return ("<!doctype html>\n<html lang=\"en\">\n<head>\n<meta charset=\"utf-8\">\n"
            "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1, viewport-fit=cover\">\n"
            + page[:head_end] + "\n</head>\n<body>\n" + page[head_end:] + "\n</body>\n</html>\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("content")
    ap.add_argument("--out", required=True)
    ap.add_argument("--slides")
    a = ap.parse_args()

    d = json.loads(Path(a.content).read_text(encoding="utf-8"))
    problems = validate(d)
    if problems:
        print("Content problems, nothing written:")
        for x in problems:
            print("  -", x)
        sys.exit(1)

    out = Path(a.out)
    (out / "deploy").mkdir(parents=True, exist_ok=True)
    data = json.dumps(d, ensure_ascii=False).replace("</", "<\\/")
    title = d["title"].replace("<", "&lt;")
    page = ACT_TPL.read_text(encoding="utf-8").replace("__TITLE__", title).replace("/*__DATA__*/null", data)
    (out / "activity.html").write_text(page, encoding="utf-8")
    (out / "deploy" / "index.html").write_text(standalone(page), encoding="utf-8")
    print("wrote", out / "activity.html")
    print("wrote", out / "deploy" / "index.html")

    if a.slides:
        body = Path(a.slides).read_text(encoding="utf-8")
        n = len(re.findall(r'<section class="slide', body))
        deck = SLD_TPL.read_text(encoding="utf-8").replace("__TITLE__", title).replace("<!--__SLIDES__-->", body)
        (out / "slides.html").write_text(deck, encoding="utf-8")
        print("wrote", out / "slides.html", f"({n} slides)")


if __name__ == "__main__":
    main()
