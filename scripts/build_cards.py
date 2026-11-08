# Copyright (c) 2026 Janat Yasser. All rights reserved.
"""
Draws the animated cards on the profile README, in a light and a dark version.

    python scripts/build_cards.py        ->  assets/cards/*.svg

Every card is a plain SVG with its own CSS animations, so it plays inside a
GitHub README (which allows no JavaScript). Fonts are subset to the characters
each card uses and embedded, so the cards look the same everywhere. Under
"reduce motion" every animation is switched off and each card shows its final
frame. The "On the bench" card is drawn from now.json, so updating it means
editing that file.

Every number on a card is a result from one of the linked repositories.
"""
import base64
import io
import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parent.parent
FONTS = ROOT / "assets" / "fonts"
OUT = ROOT / "assets" / "cards"

THEMES = {
    "light": dict(bg="#fbfaf7", card="#fbfaf7", ink="#16181d", muted="#565d69", faint="#8e95a1", line="#e4e0d8",
                  honest="#3346d3", leaky="#e4572e", ok="#12976a", soft="#efece5"),
    "dark": dict(bg="#0d1117", card="#11161d", ink="#e9ebef", muted="#a5acb7", faint="#6f7784", line="#262d37",
                 honest="#8b97ff", leaky="#ff7f57", ok="#3fcf98", soft="#1a212b"),
}
FACES = {  # css family -> file
    "Fr": "fraunces-latin-600-normal.woff2",
    "In": "inter-latin-400-normal.woff2",
    "In6": "inter-latin-600-normal.woff2",
    "Jb": "jetbrains-mono-latin-500-normal.woff2",
}


def font_data_uri(file, chars):
    font = TTFont(FONTS / file)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = ["kern", "liga"]
    opts.name_IDs = []
    s = subset.Subsetter(opts)
    s.populate(text="".join(sorted(chars | {" "})))
    s.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff2"
    font.save(buf)
    return "data:font/woff2;base64," + base64.b64encode(buf.getvalue()).decode()


class Card:
    """Collects SVG markup and the characters each font needs."""

    def __init__(self, w, h, t, label):
        self.w, self.h, self.t, self.label = w, h, t, label
        self.parts, self.css = [], []
        self.chars = {k: set() for k in FACES}

    def add(self, s):
        self.parts.append(s)

    def text(self, x, y, s, face="In", size=14, fill="ink", anchor="start", cls="", style="", spacing=0):
        self.chars[face].update(s)
        c = self.t.get(fill, fill)
        ls = f' letter-spacing="{spacing}"' if spacing else ""
        klass = f' class="{cls}"' if cls else ""
        st = f' style="{style}"' if style else ""
        self.add(f'<text x="{x}" y="{y}" font-family="{face}" font-size="{size}" fill="{c}" text-anchor="{anchor}"{ls}{klass}{st}>{escape(s)}</text>')

    def frame(self):
        t = self.t
        self.add(f'<rect x="1" y="1" width="{self.w - 2}" height="{self.h - 2}" rx="16" fill="{t["card"]}" stroke="{t["line"]}" stroke-width="1.5"/>')

    def render(self):
        faces = "".join(
            f'@font-face{{font-family:{k};src:url({font_data_uri(f, self.chars[k])}) format("woff2");}}'
            for k, f in FACES.items() if self.chars[k])
        base = (".fade{animation:fade .8s ease-out both}"
                "@keyframes fade{from{opacity:0}to{opacity:1}}"
                ".rise{animation:rise .9s cubic-bezier(.2,.7,.2,1) both}"
                "@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
                "@media (prefers-reduced-motion: reduce){*{animation:none!important}}")
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" '
                f'role="img" aria-label="{escape(self.label)}"><title>{escape(self.label)}</title>'
                f'<style>{faces}{base}{"".join(self.css)}</style>{"".join(self.parts)}</svg>')


def delay(s):
    return f"animation-delay:{s}s"


# ---------------------------------------------------------------- hero
def hero(t):
    c = Card(880, 320, t, "Janat Yasser. I build machine-learning systems, then check whether their numbers hold up on "
                          "data they've never seen. Figure: on HAM10000, a model validated on a leaky image-level split "
                          "scored 0.853 on validation and 0.716 on the official test set (mean of three seeds); split by lesion, 0.779 and 0.731.")
    c.frame()
    c.text(44, 60, "LAB NOTEBOOK", "Jb", 11, "faint", spacing=2.5, cls="fade")
    c.text(40, 128, "Janat Yasser", "Fr", 60, "ink", cls="rise", style=delay(0.1))
    c.text(44, 170, "I build machine-learning systems, then check", "In", 16, "muted", cls="rise", style=delay(0.35))
    c.text(44, 193, "whether their numbers hold up on data they've never seen.", "In", 16, "muted", cls="rise", style=delay(0.45))
    c.add(f'<line x1="44" y1="226" x2="84" y2="226" stroke="{t["line"]}" stroke-width="2" class="fade" style="{delay(0.6)}"/>')
    for i, line in enumerate(["Fig. 1. HAM10000 skin lesions. With photos of the same mole on both sides",
                              "of the split, validation flattered the model by 13.7 points (3 seeds).",
                              "The official test set didn't. Split by lesion, the drop was 4.8."]):
        c.text(44, 254 + i * 19, line, "In", 13, "faint", cls="fade", style=delay(2.6 + i * 0.1))

    # Fig. 1: validation -> official test, both splits (mean of 3 seeds, from step5_seeds.py)
    x0, x1, top, bot = 640, 790, 92, 262
    y = lambda v: bot - (v - 0.70) / 0.18 * (bot - top)
    c.text(846, 60, "FIG. 1  BALANCED ACCURACY, TWO SPLITS, 3 SEEDS", "Jb", 10.5, "faint", "end", spacing=1.2, cls="fade", style=delay(0.5))
    for x, lab in [(x0, "validation"), (x1, "official test")]:
        c.add(f'<line x1="{x}" y1="{top - 8}" x2="{x}" y2="{bot + 6}" stroke="{t["line"]}" stroke-width="1.5" stroke-dasharray="3 4" class="fade" style="{delay(0.6)}"/>')
        c.text(x, bot + 26, lab, "In", 12.5, "muted", "middle", cls="fade", style=delay(0.7))
    c.css.append(".draw{stroke-dasharray:var(--l);stroke-dashoffset:var(--l);animation:draw 1.3s cubic-bezier(.6,0,.2,1) forwards}"
                 "@keyframes draw{to{stroke-dashoffset:0}}"
                 ".pop{transform-box:fill-box;transform-origin:center;animation:pop .45s cubic-bezier(.3,1.6,.5,1) both}"
                 "@keyframes pop{from{transform:scale(0)}to{transform:scale(1)}}"
                 "@media (prefers-reduced-motion: reduce){.draw{stroke-dashoffset:0}}")
    for key, v0, v1, name, d0 in [("leaky", 0.853, 0.716, "split by image", 1.0), ("honest", 0.779, 0.731, "split by lesion", 1.25)]:
        col = t[key]
        ya, yb = y(v0), y(v1)
        L = math.hypot(x1 - x0, yb - ya) + 2
        c.add(f'<path d="M{x0} {ya:.1f} L{x1} {yb:.1f}" stroke="{col}" stroke-width="3.2" fill="none" stroke-linecap="round" '
              f'class="draw" style="--l:{L:.0f};{delay(d0)}"/>')
        c.add(f'<circle cx="{x0}" cy="{ya:.1f}" r="5.5" fill="{col}" class="pop" style="{delay(d0)}"/>')
        c.add(f'<circle cx="{x1}" cy="{yb:.1f}" r="5.5" fill="{col}" class="pop" style="{delay(d0 + 1.25)}"/>')
        c.text(x0 - 14, ya - 3, name, "In6", 12.5, col, "end", cls="fade", style=delay(d0))
        c.text(x0 - 14, ya + 13, f"{v0:.3f}", "Jb", 11.5, "muted", "end", cls="fade", style=delay(d0))
        c.text(x1 + 14, yb + 4, f"{v1:.3f}", "Jb", 12, col, cls="fade", style=delay(d0 + 1.25))
    # the drops, along each line
    c.text((x0 + x1) / 2 + 10, y(0.7845) - 12, "−13.7", "Jb", 12.5, "leaky", "middle", cls="rise", style=delay(2.4))
    c.text((x0 + x1) / 2 - 6, y(0.755) + 22, "−4.8", "Jb", 12.5, "honest", "middle", cls="rise", style=delay(2.55))
    return c


# ---------------------------------------------------------------- big cards
def card_base(t, title, lines, footer, label):
    c = Card(430, 250, t, label)
    c.frame()
    c.text(26, 46, title, "Fr", 24, "ink")
    for i, l in enumerate(lines):
        c.text(26, 182 + i * 20, l, "In", 13.5, "muted")
    c.text(26, 230, footer, "Jb", 10, "faint", spacing=1.4)
    return c


def ecg_beat(x, v=False):
    """One beat starting at x, 64 px wide. Normal: P, narrow QRS, T. V: no P, wide tall QRS, inverted T."""
    b = 120
    if not v:
        return (f"M{x} {b} l8 0 q4 -7 8 0 l6 0 l3 4 l4 -40 l4 48 l3 -12 l6 0 q7 -12 14 0 l7 0")
    return f"M{x} {b} l10 0 l6 6 l9 -52 l10 70 l7 -24 q8 14 16 0 l6 0"


def cardiosim(t):
    c = card_base(t, "CardioSim",
                  ["An ECG monitor whose CNN labels every beat. On unseen",
                   "patients: 91% of ventricular beats caught, 90% precise."],
                  "PYTHON · PYQT5 · MIT-BIH · PAPER",
                  "CardioSim: an animated ECG trace with ventricular beats highlighted. 91% of ventricular beats caught, 90% precise, on unseen patients.")
    t_ = t
    seq = "NNNVNNNNVNNN"
    w = 64
    normal, ventric, labels = [], [], []
    for rep in range(2):
        for i, s in enumerate(seq):
            x = (rep * len(seq) + i) * w
            (ventric if s == "V" else normal).append(ecg_beat(x, s == "V"))
            if s == "V":
                labels.append(x + 20)
    period = len(seq) * w
    c.add(f'<defs><clipPath id="ecg"><rect x="26" y="62" width="378" height="92" rx="8"/></clipPath>'
          f'<linearGradient id="fadeR" x1="0" x2="1"><stop offset="0" stop-color="{t_["card"]}" stop-opacity="0"/>'
          f'<stop offset="1" stop-color="{t_["card"]}"/></linearGradient></defs>')
    c.add(f'<rect x="26" y="62" width="378" height="92" rx="8" fill="{t_["soft"]}"/>')
    c.css.append(f".scroll{{animation:scroll 9s linear infinite}}@keyframes scroll{{from{{transform:translateX(26px)}}to{{transform:translateX({26 - period}px)}}}}")
    vlab = "".join(f'<text x="{x}" y="72" font-family="Jb" font-size="10" fill="{t_["leaky"]}">V</text>' for x in labels)
    c.chars["Jb"].update("V")
    c.add(f'<g clip-path="url(#ecg)"><g class="scroll">'
          f'<path d="{" ".join(normal)}" stroke="{t_["ok"]}" stroke-width="1.8" fill="none" stroke-linejoin="round"/>'
          f'<path d="{" ".join(ventric)}" stroke="{t_["leaky"]}" stroke-width="2.2" fill="none" stroke-linejoin="round"/>'
          f'{vlab}</g></g>')
    c.add(f'<rect x="364" y="62" width="40" height="92" fill="url(#fadeR)"/>')
    return c


def rag(t):
    c = card_base(t, "RAG Faithfulness Detector",
                  ["Does an AI answer say what its sources say? It checks",
                   "claim by claim, without calling a language model."],
                  "PYTHON · SCIKIT-LEARN · LIVE DEMO · PAPER",
                  "RAG Faithfulness Detector: held-out accuracy rose from 46% (version 1) to 86% (version 2).")
    c.text(26, 78, "held-out set, written before the rules existed", "In", 12, "faint")
    c.css.append(".grow{transform-box:fill-box;transform-origin:left center;animation:grow 1.4s cubic-bezier(.3,.8,.2,1) both}"
                 "@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}")
    full = 290
    for i, (lab, v, col, d) in enumerate([("v1", 0.46, "faint", 0.3), ("v2", 0.86, "honest", 0.9)]):
        yy = 96 + i * 32
        c.text(26, yy + 15, lab, "Jb", 12, "muted")
        c.add(f'<rect x="58" y="{yy}" width="{full}" height="20" rx="5" fill="{t["soft"]}"/>')
        c.add(f'<rect x="58" y="{yy}" width="{full * v:.0f}" height="20" rx="5" fill="{t[col]}" class="grow" style="{delay(d)}"/>')
        c.text(58 + full + 12, yy + 15, f"{round(v * 100)}%", "Jb", 13, col if col != "faint" else "muted", cls="fade", style=delay(d + 1.1))
    return c


def roboforge(t):
    c = card_base(t, "RoboForge",
                  ["Describe a robot once: get firmware, ROS 2 packages and",
                   "wiring docs, then watch it drive before you build it."],
                  "TYPESCRIPT · NEXT.JS · 48 TESTS · LIVE DEMO",
                  "RoboForge: a robot drives around obstacles in a 2D simulator, its distance sensor's ray sweeping ahead.")
    c.add(f'<rect x="26" y="62" width="378" height="98" rx="8" fill="{t["soft"]}" stroke="{t["line"]}"/>')
    for gx in range(26 + 42, 404, 42):
        c.add(f'<line x1="{gx}" y1="62" x2="{gx}" y2="160" stroke="{t["line"]}" stroke-width="1"/>')
    for (bx, by, bw, bh) in [(120, 74, 34, 30), (250, 118, 40, 30)]:
        c.add(f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="4" fill="{t["card"]}" stroke="{t["line"]}" stroke-width="1.5"/>')
    c.add(f'<circle cx="345" cy="98" r="15" fill="{t["card"]}" stroke="{t["line"]}" stroke-width="1.5"/>')
    route = "M50 136 C 95 136, 95 136, 160 132 S 225 84, 290 92 S 370 140, 330 146 S 160 150, 90 112 S 40 136, 50 136 Z"
    c.add(f'<path d="{route}" fill="none" stroke="{t["honest"]}" stroke-opacity=".25" stroke-width="1.5" stroke-dasharray="3 5"/>')
    c.css.append(".ray{animation:ray 1.2s ease-in-out infinite alternate}@keyframes ray{from{opacity:.25}to{opacity:.9}}")
    c.add(f'<g><g class="ray"><line x1="0" y1="0" x2="38" y2="0" stroke="{t["ok"]}" stroke-width="1.6" stroke-dasharray="3 3"/></g>'
          f'<circle r="8" fill="{t["card"]}" stroke="{t["honest"]}" stroke-width="2.4"/>'
          f'<path d="M-2 -4 L4 0 L-2 4 Z" fill="{t["honest"]}"/>'
          f'<animateMotion dur="11s" repeatCount="indefinite" rotate="auto" path="{route}"/></g>')
    return c


def bench(t, now):
    c = Card(430, 250, t, "On the bench now: " + "; ".join(i["title"] for i in now["items"]))
    c.frame()
    c.text(26, 46, "On the bench", "Fr", 24, "ink")
    c.text(404, 44, f"UPDATED {now['updated'].upper()}", "Jb", 10, "faint", "end", spacing=1.2)
    c.css.append(".pulse{transform-box:fill-box;transform-origin:center;animation:pulse 1.8s ease-out infinite}"
                 "@keyframes pulse{0%{transform:scale(1);opacity:.6}100%{transform:scale(2.6);opacity:0}}")
    yy = 82
    for it in now["items"][:3]:
        running = it.get("status") == "running"
        col = t["ok"] if running else t["faint"]
        if running:
            c.add(f'<circle cx="32" cy="{yy - 5}" r="4.5" fill="{col}" class="pulse"/>')
        c.add(f'<circle cx="32" cy="{yy - 5}" r="4.5" fill="{col}"/>')
        c.text(46, yy, it["title"], "In6", 13.5, "ink")
        c.text(46, yy + 19, it["detail"], "In", 12.5, "muted")
        c.text(404, yy, it.get("status", "").upper(), "Jb", 9.5, "ok" if running else "faint", "end", spacing=1.2)
        yy += 52
    return c


# ---------------------------------------------------------------- small tiles
def tile(t, title, sub, label):
    c = Card(280, 132, t, label)
    c.frame()
    c.text(20, 38, title, "Fr", 17.5, "ink")
    c.text(260, 36, "LIVE ↗", "Jb", 10, "honest", "end", spacing=1.2)
    c.text(20, 58, sub, "In", 12, "muted")
    return c


def algoviz(t):
    c = tile(t, "AlgoViz", "Sorts, paths and trees, step by step.", "AlgoViz: bars swapping places as a sort runs.")
    hs = [22, 40, 14, 34, 28, 46, 18, 30, 38, 24, 44, 16]
    x0, w, gap, base = 20, 15, 5, 116
    c.css.append(".swapA{animation:swapA 3.2s ease-in-out infinite}.swapB{animation:swapB 3.2s ease-in-out infinite}"
                 "@keyframes swapA{0%,25%{transform:none}45%,100%{transform:translateX(40px)}}"
                 "@keyframes swapB{0%,25%{transform:none}45%,100%{transform:translateX(-40px)}}"
                 ".hot{animation:hot 3.2s ease-in-out infinite}@keyframes hot{0%,15%,55%,100%{opacity:0}22%,45%{opacity:1}}")
    for i, h in enumerate(hs):
        x = x0 + i * (w + gap)
        cls = "swapA" if i == 3 else "swapB" if i == 5 else ""
        if cls:
            c.add(f'<g class="{cls}"><rect x="{x}" y="{base - h}" width="{w}" height="{h}" rx="3" fill="{t["faint"]}" opacity=".55"/>'
                  f'<rect x="{x}" y="{base - h}" width="{w}" height="{h}" rx="3" fill="{t["honest"]}" class="hot"/></g>')
        else:
            c.add(f'<rect x="{x}" y="{base - h}" width="{w}" height="{h}" rx="3" fill="{t["faint"]}" opacity=".55"/>')
    return c


def sysplay(t):
    c = tile(t, "Systems Playground", "Huffman, a key-value store, packets.",
             "Systems Playground: a Huffman tree being built; the sample text shrinks by 55.8%.")
    nodes = {"r": (110, 72), "a": (70, 92), "b": (150, 92), "c": (48, 112), "d": (92, 112), "e": (130, 112), "f": (172, 112)}
    edges = [("r", "a", "0"), ("r", "b", "1"), ("a", "c", "0"), ("a", "d", "1"), ("b", "e", "0"), ("b", "f", "1")]
    c.css.append(".edge{stroke-dasharray:40;stroke-dashoffset:40;animation:edge 4s ease-out infinite}"
                 "@keyframes edge{0%{stroke-dashoffset:40}30%,85%{stroke-dashoffset:0}100%{stroke-dashoffset:0;opacity:0}}"
                 ".node{animation:node 4s ease-out infinite}@keyframes node{0%,10%{opacity:0}25%,85%{opacity:1}100%{opacity:0}}"
                 "@media (prefers-reduced-motion: reduce){.edge{stroke-dashoffset:0}}")
    for k, (a, b, bit) in enumerate(edges):
        (xa, ya), (xb, yb) = nodes[a], nodes[b]
        c.add(f'<line x1="{xa}" y1="{ya}" x2="{xb}" y2="{yb}" stroke="{t["muted"]}" stroke-width="1.5" class="edge" style="{delay(k * 0.15)}"/>')
        c.text((xa + xb) / 2 + (-7 if bit == "0" else 5), (ya + yb) / 2 + 2, bit, "Jb", 9, "faint")
    for k, (x, yv) in nodes.items():
        col = t["honest"] if k in "cdef" else t["muted"]
        c.add(f'<circle cx="{x}" cy="{yv}" r="5" fill="{col}" class="node" style="{delay(0.2)}"/>')
    c.text(260, 100, "55.8%", "Jb", 20, "leaky", "end", cls="fade", style=delay(0.8))
    c.text(260, 116, "smaller", "In", 11, "muted", "end")
    return c


def attendly(t):
    c = tile(t, "Attendly", "Attendance, warned before the limit.",
             "Attendly: an attendance grid fills in; one student's row turns amber before they hit the absence limit.")
    c.css.append(".dot{animation:fill 6s ease-out infinite}@keyframes fill{0%{opacity:.15}8%,92%{opacity:1}100%{opacity:.15}}")
    rows, cols = 4, 12
    absent = {(2, 2), (2, 5), (2, 7), (2, 9), (0, 6), (3, 3)}
    for r in range(rows):
        for k in range(cols):
            x, yv = 26 + k * 19, 76 + r * 12
            miss = (r, k) in absent
            col = t["leaky"] if (miss and r == 2) else t["faint"] if miss else t["ok"]
            op = ".9" if not miss or r == 2 else ".5"
            c.add(f'<circle cx="{x}" cy="{yv}" r="4" fill="{col}" fill-opacity="{op}" class="dot" style="{delay(k * 0.18)}"/>')
    c.add(f'<rect x="10" y="{76 + 2 * 12 - 7}" width="7" height="14" rx="2" fill="{t["leaky"]}" class="fade" style="{delay(2.2)}"/>')
    return c


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    now = json.loads((ROOT / "now.json").read_text(encoding="utf-8"))
    builders = {"hero": hero, "cardiosim": cardiosim, "rag": rag, "roboforge": roboforge,
                "bench": lambda t: bench(t, now), "algoviz": algoviz, "sysplay": sysplay, "attendly": attendly}
    for name, build in builders.items():
        for theme, t in THEMES.items():
            (OUT / f"{name}-{theme}.svg").write_text(build(t).render(), encoding="utf-8")
    print("cards ->", OUT)


if __name__ == "__main__":
    main()
