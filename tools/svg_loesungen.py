#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Erzeugt die schematischen Zeichnungen der Lösungsseiten (img/loesungen/*.svg, DE und EN)."""
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "img" / "loesungen"
INK, RED, MUT, LINE, COOL = "#1a1a1a", "#c8202f", "#5c5c5c", "#d9d4d4", "#2a7ab8"
FONT = 'font-family="system-ui,-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif"'

T = {
 "de": {"wall": "Hauswand", "wr": "Wechselrichter", "in": "Zuluft kalt", "out": "Abluft über HSA3-Röhren",
        "lin": "HSA3-Innenverkleidung", "front": "Front ganz zu öffnen", "gap": "500 / 800 mm Abstand",
        "src": "Anlage", "bar": "Schallwand mit HSA3", "diff": "Beugung an der Oberkante", "imm": "Nachbarfenster",
        "shadow": "Schallschatten", "direct": "direkter Weg – blockiert",
        "core": "HSA3-Aufbau (Schnitt)", "l1": "gewellte, mikroperforierte Deckschicht", "l2": "Luftkammern (Resonatoren)",
        "l3": "federnd gelagerte Zwischenlage", "l4": "Resonanzhohlraum", "l5": "Trägerplatte / Paneel", "snd": "Schall",
        "heat": "Schallenergie → Wärme"},
 "en": {"wall": "Building wall", "wr": "Inverter", "in": "Cool supply air", "out": "Exhaust via HSA3 tubes",
        "lin": "HSA3 inner lining", "front": "Front opens fully", "gap": "500 / 800 mm clearance",
        "src": "Unit", "bar": "Noise barrier with HSA3", "diff": "Diffraction at the top edge", "imm": "Neighbour's window",
        "shadow": "Acoustic shadow", "direct": "direct path – blocked",
        "core": "HSA3 build-up (section)", "l1": "corrugated, micro-perforated face layer", "l2": "air chambers (resonators)",
        "l3": "spring-mounted intermediate layer", "l4": "resonance cavity", "l5": "carrier plate / panel", "snd": "Sound",
        "heat": "sound energy → heat"},
}

DEFS = f'''<defs>
<marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{RED}"/></marker>
<marker id="ac" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{COOL}"/></marker>
<marker id="ak" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{INK}"/></marker>
<pattern id="hatch" width="8" height="8" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="8" height="8" fill="#ece8e8"/><line x1="0" y1="0" x2="0" y2="8" stroke="#bdb6b6" stroke-width="2"/></pattern>
<pattern id="hsa" width="10" height="10" patternUnits="userSpaceOnUse"><rect width="10" height="10" fill="#fbe3e6"/><circle cx="5" cy="5" r="1.6" fill="{RED}"/></pattern>
</defs>'''


def txt(x, y, s, size=17, fill=INK, anchor="start", weight="400"):
    lines = s.split("\n")
    out = []
    for i, l in enumerate(lines):
        out.append(f'<text x="{x}" y="{y + i * (size + 3)}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" font-weight="{weight}" {FONT}>{l}</text>')
    return "".join(out)


def inverter(L):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520" role="img" aria-label="{L["wr"].replace(chr(10), "")} – {L["out"]}">', DEFS,
         '<rect width="800" height="520" fill="#fff"/>',
         f'<line x1="40" y1="470" x2="760" y2="470" stroke="{INK}" stroke-width="3"/>',
         '<rect x="40" y="470" width="720" height="16" fill="url(#hatch)"/>',
         # Wand
         '<rect x="110" y="40" width="40" height="430" fill="url(#hatch)" stroke="#9c9494"/>',
         txt(130, 30, L["wall"], 15, MUT, "middle"),
         # Haube: Dach, Front, mit HSA3-Auskleidung
         f'<path d="M150 120 H540 V400" fill="none" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>',
         '<path d="M150 131 H529 V400 H517 V143 H150z" fill="url(#hsa)"/>',
         # Dach-Röhren
         ]
    for cx in (250, 320, 390, 460):
        s.append(f'<rect x="{cx-26}" y="70" width="52" height="56" rx="6" fill="#fff" stroke="{INK}" stroke-width="3"/>')
        s.append(f'<circle cx="{cx}" cy="98" r="17" fill="url(#hsa)" stroke="{RED}" stroke-width="2"/>')
    s += [
        # Wechselrichter
        f'<rect x="150" y="210" width="62" height="170" rx="4" fill="#3a3a3a"/>',
        '<rect x="160" y="226" width="42" height="26" rx="3" fill="#6b6b6b"/>',
        txt(181, 200, L["wr"], 15, INK, "middle", "700"),
        # Zuluft unten vorne (Lamellen)
        f'<g stroke="{INK}" stroke-width="3">' + "".join(f'<line x1="530" y1="{y}" x2="552" y2="{y+10}"/>' for y in (408, 422, 436, 450)) + '</g>',
        f'<path d="M700 445 H470 C420 445 380 430 330 380 C300 350 290 300 300 250" fill="none" stroke="{COOL}" stroke-width="6" marker-end="url(#ac)"/>',
        txt(515, 432, L["in"], 17, COOL, "end", "700"),
        # Abluft durch Röhren
    ]
    for cx in (250, 320, 390, 460):
        s.append(f'<line x1="{cx}" y1="170" x2="{cx}" y2="42" stroke="{RED}" stroke-width="5" marker-end="url(#ar)"/>')
    s += [txt(560, 60, L["out"], 17, RED, "start", "700"),
          f'<line x1="555" y1="64" x2="490" y2="90" stroke="{RED}" stroke-width="2"/>',
          txt(560, 200, L["lin"], 16, INK), f'<line x1="556" y1="196" x2="534" y2="196" stroke="{INK}" stroke-width="2" marker-end="url(#ak)"/>',
          txt(560, 300, L["front"], 16, INK), f'<line x1="556" y1="296" x2="545" y2="296" stroke="{INK}" stroke-width="2" marker-end="url(#ak)"/>',
          txt(560, 330, L["gap"], 14, MUT),
          '</svg>']
    return "".join(s)


def barrier(L):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 520" role="img" aria-label="{L["bar"]} – {L["diff"]}">', DEFS,
         '<rect width="800" height="520" fill="#fff"/>',
         f'<line x1="20" y1="450" x2="780" y2="450" stroke="{INK}" stroke-width="3"/>',
         '<rect x="20" y="450" width="760" height="16" fill="url(#hatch)"/>',
         # Schattenzone
         '<path d="M318 172 L780 330 L780 450 L318 450z" fill="#f3eff0"/>',
         txt(455, 432, L["shadow"], 15, MUT, "middle"),
         # Anlage
         f'<rect x="60" y="300" width="170" height="150" rx="6" fill="#4a4a4a"/>',
         '<circle cx="145" cy="300" r="1" fill="none"/>',
         f'<rect x="80" y="286" width="130" height="14" rx="3" fill="#6b6b6b"/>',
         txt(145, 385, L["src"], 17, "#fff", "middle", "700"),
         # Quelle
         f'<circle cx="145" cy="330" r="9" fill="{RED}"/>',
         # Wand
         f'<rect x="300" y="170" width="18" height="280" fill="#7a7a7a"/>',
         '<rect x="292" y="170" width="8" height="280" fill="url(#hsa)"/>',
         txt(290, 150, L["bar"], 16, INK, "end", "700"),
         # Haus
         f'<path d="M600 450 V250 L690 190 L780 250 V450z" fill="#ece8e8" stroke="#9c9494" stroke-width="2"/>',
         f'<rect x="640" y="300" width="44" height="58" fill="#fff" stroke="{INK}" stroke-width="3"/>',
         f'<circle cx="662" cy="329" r="7" fill="{INK}"/>',
         txt(662, 395, L["imm"], 15, INK, "middle"),
         # direkter Weg
         f'<line x1="154" y1="330" x2="296" y2="330" stroke="{RED}" stroke-width="3" stroke-dasharray="8 7"/>',
         f'<line x1="318" y1="330" x2="640" y2="329" stroke="{RED}" stroke-width="2" stroke-dasharray="3 9" opacity=".45"/>',
         f'<path d="M280 315 l22 22 m0 -22 l-22 22" stroke="{INK}" stroke-width="4"/>',
         txt(470, 356, L["direct"], 14, MUT, "middle"),
         # gebeugter Weg
         f'<path d="M150 322 L309 170" fill="none" stroke="{RED}" stroke-width="4"/>',
         f'<path d="M309 170 L636 326" fill="none" stroke="{RED}" stroke-width="4" marker-end="url(#ar)"/>',
         f'<circle cx="309" cy="170" r="7" fill="#fff" stroke="{RED}" stroke-width="3"/>',
         txt(340, 120, L["diff"], 16, RED, "start", "700"),
         f'<line x1="338" y1="125" x2="318" y2="160" stroke="{RED}" stroke-width="2"/>',
         '</svg>']
    return "".join(s)


def hsa3(L):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 460" role="img" aria-label="{L["core"]}">', DEFS,
         '<rect width="800" height="460" fill="#fff"/>',
         txt(40, 44, L["core"], 20, INK, "start", "700")]
    x0, x1 = 50, 440
    # Trägerplatte
    s.append(f'<rect x="{x0}" y="370" width="{x1-x0}" height="16" fill="#7a7a7a"/>')
    # Resonanzhohlraum (leer) 300-370
    # Federn
    for x in range(90, x1, 60):
        pts = " ".join(f"{x + (8 if i % 2 else -8)},{300 + i * 7}" for i in range(11))
        s.append(f'<polyline points="{x},296 {pts} {x},370" fill="none" stroke="{MUT}" stroke-width="2.5"/>')
    # Zwischenlage
    s.append(f'<rect x="{x0}" y="282" width="{x1-x0}" height="12" rx="2" fill="#4a4a4a"/>')
    # Kammern 200-282
    w = (x1 - x0) / 10
    for x in [x0 + i * w for i in range(11)]:
        s.append(f'<line x1="{x}" y1="200" x2="{x}" y2="282" stroke="{INK}" stroke-width="2.5"/>')
    s.append(f'<rect x="{x0}" y="200" width="{x1-x0}" height="82" fill="url(#hsa)" opacity=".55"/>')
    # gewellte Deckschicht mit Löchern
    d = f"M{x0} 200 " + " ".join(f"Q{x0 + w/2 + i*w:.1f} {180 if i % 2 == 0 else 220} {x0 + w + i*w:.1f} 200" for i in range(10))
    s.append(f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="5"/>')
    for i in range(10):
        cx = x0 + w / 2 + i * w
        cy = 191 if i % 2 == 0 else 209
        s.append(f'<circle cx="{cx}" cy="{cy}" r="2.6" fill="#fff" stroke="{INK}" stroke-width="1"/>')
    # Schall
    for x in (120, 240, 360):
        s.append(f'<path d="M{x} 70 q10 12 0 24 q-10 12 0 24 q10 12 0 24" fill="none" stroke="{RED}" stroke-width="4"/>')
        s.append(f'<line x1="{x}" y1="140" x2="{x}" y2="168" stroke="{RED}" stroke-width="4" marker-end="url(#ar)"/>')
    s.append(txt(385, 92, L["snd"], 17, RED, "start", "700"))
    s.append(txt(x0 + 10, 425, L["heat"], 15, MUT))
    # Beschriftungen
    labels = [(196, L["l1"]), (244, L["l2"]), (288, L["l3"]), (336, L["l4"]), (378, L["l5"])]
    for y, l in labels:
        s.append(f'<line x1="{x1 + 8}" y1="{y}" x2="{x1 + 40}" y2="{y}" stroke="{INK}" stroke-width="1.5"/>')
        s.append(txt(x1 + 48, y + 6, l, 15, INK))
    s.append('</svg>')
    return "".join(s)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    for lang, L in T.items():
        sfx = "" if lang == "de" else "-en"
        (OUT / f"wechselrichter-haube{sfx}.svg").write_text(inverter(L), encoding="utf-8")
        (OUT / f"schallwand-prinzip{sfx}.svg").write_text(barrier(L), encoding="utf-8")
        (OUT / f"hsa3-aufbau{sfx}.svg").write_text(hsa3(L), encoding="utf-8")
    print("SVG-Zeichnungen erzeugt")


if __name__ == "__main__":
    build()
