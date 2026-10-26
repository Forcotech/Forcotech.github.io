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
        "heat": "Schallenergie → Wärme",
        "b_grid": "Netz", "b_tr": "Transformator", "b_wr": "Wechselrichter", "b_cont": "BESS-Container",
        "b_hvac": "Klimagerät", "b_racks": "Batterie-Racks",
        "b_n1": "Brummen 100/200 Hz", "b_n2": "Lüfter, Schaltfrequenz", "b_n3": "Verdichter, Ventilatoren",
        "b_s1": "HSA3-Einhausung", "b_s2": "HSA3-Schallhaube", "b_s3": "HSA3-Kulisse",
        "b_aria0": "BESS-Anlage ohne Schallschutz: Transformator, Wechselrichter und Klimagerät des Containers strahlen Schall frei ab",
        "b_aria1": "BESS-Anlage mit ForCoTech-Lösung: Trafo-Einhausung, Schallhaube am Wechselrichter und Kulisse vor dem Klimagerät aus HSA3",
        "f_hi": "Hohe Frequenz – z. B. 2.000 Hz, λ ≈ 17 cm", "f_lo": "Tiefe Frequenz – 100 Hz, λ ≈ 3,4 m",
        "f_hi2": "deutlicher Schallschatten", "f_lo2": "Schall beugt sich in den Schatten",
        "f_aria": "Vergleich: Hohe Frequenzen enden an der Wand in einem deutlichen Schallschatten, tiefe Frequenzen beugen sich über die Wandkrone bis zum Empfänger",
        "r_ref": "Reflektierende Wand", "r_abs": "Absorbierende Wand mit HSA3",
        "r_ref2": "Mehrfachreflexion:\njede Reflexion strahlt\nzusätzlich über die Krone", "r_abs2": "Schall wird auf der\nQuellseite geschluckt",
        "r_mirror": "Spiegelquellen", "r_heat": "Schallenergie → Wärme im HSA3",
        "r_aria": "Vergleich: Bei einer reflektierenden Wand wird der Schall zwischen Anlage und Wand mehrfach hin und her geworfen und strahlt mehrfach über die Krone ab; eine absorbierende HSA3-Wand schluckt ihn auf der Quellseite"},
 "en": {"wall": "Building wall", "wr": "Inverter", "in": "Cool supply air", "out": "Exhaust via HSA3 tubes",
        "lin": "HSA3 inner lining", "front": "Front opens fully", "gap": "500 / 800 mm clearance",
        "src": "Unit", "bar": "Noise barrier with HSA3", "diff": "Diffraction at the top edge", "imm": "Neighbour's window",
        "shadow": "Acoustic shadow", "direct": "direct path – blocked",
        "core": "HSA3 build-up (section)", "l1": "corrugated, micro-perforated face layer", "l2": "air chambers (resonators)",
        "l3": "spring-mounted intermediate layer", "l4": "resonance cavity", "l5": "carrier plate / panel", "snd": "Sound",
        "heat": "sound energy → heat",
        "b_grid": "Grid", "b_tr": "Transformer", "b_wr": "Inverter (PCS)", "b_cont": "BESS container",
        "b_hvac": "HVAC unit", "b_racks": "Battery racks",
        "b_n1": "Hum 100/200 Hz", "b_n2": "Fans, switching freq.", "b_n3": "Compressors, fans",
        "b_s1": "HSA3 enclosure", "b_s2": "HSA3 acoustic hood", "b_s3": "HSA3 silencer",
        "b_aria0": "BESS site without noise control: transformer, inverter and the container's HVAC unit radiate noise freely",
        "b_aria1": "BESS site with ForCoTech solution: transformer enclosure, acoustic hood on the inverter and silencer in front of the HVAC unit, all in HSA3",
        "f_hi": "High frequency – e.g. 2,000 Hz, λ ≈ 17 cm", "f_lo": "Low frequency – 100 Hz, λ ≈ 3.4 m",
        "f_hi2": "clear acoustic shadow", "f_lo2": "sound bends into the shadow",
        "f_aria": "Comparison: high frequencies end at the barrier in a clear acoustic shadow, low frequencies bend over the top edge to the receiver",
        "r_ref": "Reflective barrier", "r_abs": "Absorbing barrier with HSA3",
        "r_ref2": "Multiple reflections:\nevery reflection also\nradiates over the top", "r_abs2": "Sound is absorbed\non the source side",
        "r_mirror": "Image sources", "r_heat": "sound energy → heat in the HSA3",
        "r_aria": "Comparison: with a reflective barrier, sound bounces back and forth between unit and barrier and radiates over the top several times; an absorbing HSA3 barrier absorbs it on the source side"},
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


def bess(L, mit):
    """BESS-Anlage im Seitenschnitt: Netz, Trafo, Wechselrichter, Container mit Klimagerät – ohne bzw. mit HSA3-Lösung."""
    U = 'fill="#ece8e8" stroke="#9c9494" stroke-width="2"'
    H = f'fill="url(#hsa)" stroke="{INK}" stroke-width="3"'
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1300 390" role="img" aria-label="{L["b_aria1" if mit else "b_aria0"]}">', DEFS,
         '<pattern id="cor" width="23" height="10" patternUnits="userSpaceOnUse"><line x1="11" y1="0" x2="11" y2="10" stroke="#9c9494" stroke-opacity=".5"/></pattern>',
         '<rect width="1300" height="390" fill="#fff"/>',
         f'<line x1="0" y1="300" x2="1300" y2="300" stroke="{INK}" stroke-width="3"/>',
         '<rect x="0" y="301" width="1300" height="12" fill="url(#hatch)"/>',
         # Netz / Mittelspannung
         f'<path d="M0 120 H85 V190" fill="none" stroke="{MUT}" stroke-width="2"/>',
         f'<rect x="40" y="190" width="90" height="110" rx="3" {U}/>',
         '<line x1="85" y1="196" x2="85" y2="294" stroke="#9c9494"/>',
         '<rect x="55" y="205" width="20" height="14" fill="none" stroke="#9c9494"/>',
         f'<path d="M130 215 H{158 if mit else 180}" fill="none" stroke="#9c9494" stroke-width="2"/>',
         # Transformator
         f'<rect x="215" y="158" width="120" height="16" rx="8" {U}/>']
    for x in (232, 270, 308):
        s.append(f'<rect x="{x}" y="176" width="10" height="24" {U}/>')
    s += [f'<rect x="200" y="200" width="150" height="100" rx="3" {U}/>',
          f'<rect x="180" y="210" width="20" height="80" {U}/>', f'<rect x="350" y="210" width="20" height="80" {U}/>',
          '<path d="M185 214V286M190 214V286M195 214V286M355 214V286M360 214V286M365 214V286" stroke="#9c9494"/>',
          # Wechselrichter / PCS
          f'<rect x="440" y="160" width="180" height="140" rx="3" {U}/>',
          f'<rect x="470" y="140" width="120" height="20" rx="3" {U}/>',
          '<path d="M485 150H515M545 150H575" stroke="#9c9494" stroke-width="2"/>',
          '<circle cx="500" cy="150" r="3" fill="#9c9494"/><circle cx="560" cy="150" r="3" fill="#9c9494"/>',
          '<rect x="490" y="185" width="110" height="30" fill="none" stroke="#9c9494" stroke-width="1.5"/>',
          '<rect x="490" y="225" width="110" height="30" fill="none" stroke="#9c9494" stroke-width="1.5"/>',
          '<path d="M446 240H466M446 250H466M446 260H466M446 270H466M446 280H466" stroke="#9c9494" stroke-width="1.5"/>',
          f'<path d="M{392 if mit else 370} 290H{418 if mit else 440}M{642 if mit else 620} 290H680" fill="none" stroke="#9c9494" stroke-width="2"/>',
          # Container mit Klimagerät
          f'<rect x="680" y="150" width="460" height="150" rx="3" {U}/>',
          '<rect x="681" y="151" width="458" height="148" fill="url(#cor)"/>',
          f'<rect x="700" y="180" width="56" height="112" {U}/>',
          txt(940, 235, L["b_racks"], 22, MUT, "middle", "700"),
          f'<rect x="1140" y="180" width="60" height="95" rx="3" {U}/>',
          '<circle cx="1170" cy="212" r="18" fill="none" stroke="#9c9494" stroke-width="2"/>',
          '<path d="M1152 212H1188M1170 194V230M1148 245H1192M1148 252H1192M1148 259H1192M1148 266H1192" stroke="#9c9494" stroke-width="1.5"/>']
    if mit:
        s += [  # HSA3: Trafo-Einhausung, Wechselrichter-Haube, Kulisse vor dem Klimagerät
            f'<rect x="158" y="140" width="14" height="160" {H}/>', f'<rect x="378" y="140" width="14" height="160" {H}/>',
            f'<rect x="158" y="112" width="234" height="28" {H}/>',
            f'<rect x="418" y="120" width="14" height="180" {H}/>', f'<rect x="628" y="120" width="14" height="180" {H}/>',
            f'<rect x="418" y="92" width="224" height="28" {H}/>',
            f'<rect x="1205" y="176" width="44" height="103" {H}/>']
        air = [("M136 278H194", ""), ("M275 154V66", ""), ("M384 266H446", ""), ("M530 136V48", ""),
               ("M1185 112V176", ' stroke-dasharray="7 6"'), ("M1200 228H1294", "")]
        snd = ["M398 222Q406 230 398 238", "M337 100Q345 92 353 100", "M592 82Q600 74 608 82",
               "M650 192Q658 200 650 208", "M1262 254Q1270 262 1262 270"]
        badges = [(136, 124, 1), (396, 74, 2), (1148, 138, 3)]
        sub, subc = [(275, L["b_s1"]), (530, L["b_s2"]), (1185, L["b_s3"])], INK
    else:
        air = [("M190 205V150", ""), ("M360 205V150", ""), ("M396 272H438", ""), ("M530 136V78", ""),
               ("M1185 112V176", ' stroke-dasharray="7 6"'), ("M1205 222H1292", "")]
        snd = ["M172 232Q164 240 172 248M164 226Q152 240 164 254M156 220Q140 240 156 260",
               "M378 232Q386 240 378 248M386 226Q398 240 386 254M394 220Q410 240 394 260",
               "M267 140Q275 132 283 140M261 132Q275 120 289 132M255 124Q275 108 295 124",
               "M582 128Q590 120 598 128M576 120Q590 108 604 120M570 112Q590 96 610 112",
               "M432 182Q424 190 432 198M424 176Q412 190 424 204M416 170Q400 190 416 210",
               "M1210 254Q1218 262 1210 270M1218 248Q1230 262 1218 276M1226 242Q1242 262 1226 282M1234 236Q1254 262 1234 288"]
        badges = [(158, 174, 1), (452, 122, 2), (1148, 138, 3)]
        sub, subc = [(275, L["b_n1"]), (530, L["b_n2"]), (1170, L["b_n3"])], RED
    for d, ex in air:
        s.append(f'<path d="{d}" fill="none" stroke="{COOL}" stroke-width="4" stroke-linecap="round" marker-end="url(#ac)"{ex}/>')
    for d in snd:
        s.append(f'<path d="{d}" fill="none" stroke="{RED}" stroke-width="3" stroke-linecap="round"/>')
    for x, y, n in badges:
        s.append(f'<circle cx="{x}" cy="{y}" r="18" fill="{RED}"/>' + txt(x, y + 7, str(n), 20, "#fff", "middle", "700"))
    hx = 1185 if mit else 1170
    for x, t in [(85, L["b_grid"]), (275, L["b_tr"]), (530, L["b_wr"]), (910, L["b_cont"]), (hx, L["b_hvac"])]:
        s.append(txt(x, 344, t, 21, INK, "middle", "700"))
    for x, t in sub:
        s.append(txt(x, 372, t, 18, subc, "middle", "700"))
    s.append('</svg>')
    return "".join(s)


def _arc(cx, cy, r, a0, a1, **kw):
    import math
    x0, y0 = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0))
    x1, y1 = cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1))
    large = 1 if (a1 - a0) > 180 else 0
    attrs = " ".join(f'{k.replace("_", "-")}="{v}"' for k, v in kw.items())
    return f'<path d="M{x0:.1f} {y0:.1f} A{r} {r} 0 {large} 1 {x1:.1f} {y1:.1f}" fill="none" {attrs}/>'


def _house(x, gy):
    return (f'<path d="M{x} {gy} V{gy-130} L{x+55} {gy-170} L{x+110} {gy-130} V{gy}z" fill="#ece8e8" stroke="#9c9494" stroke-width="2"/>'
            f'<rect x="{x+34}" y="{gy-105}" width="42" height="52" fill="#fff" stroke="{INK}" stroke-width="3"/>')


def frequency(L):
    """Zwei Felder: hohe Frequenz mit Schallschatten, tiefe Frequenz mit Beugung in den Schatten."""
    W, H, GY = 1300, 430, 380
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{L["f_aria"]}">', DEFS,
         f'<rect width="{W}" height="{H}" fill="#fff"/>',
         f'<line x1="650" y1="30" x2="650" y2="{H-20}" stroke="{LINE}" stroke-width="2"/>']
    for i, (title, sub, lam, a_end, faint) in enumerate(((L["f_hi"], L["f_hi2"], 13, -52, True),
                                                          (L["f_lo"], L["f_lo2"], 58, 82, False))):
        ox = i * 655
        sx, sy = ox + 95, 310          # Quelle
        wx, wy = ox + 215, 150         # Wandkrone
        s.append(f'<clipPath id="cl{i}"><rect x="{ox+10}" y="40" width="{wx-ox-10}" height="{GY-40}"/></clipPath>')
        s.append(f'<clipPath id="cr{i}"><rect x="{wx+14}" y="40" width="{ox+640-wx-14}" height="{GY-40}"/></clipPath>')
        s.append(f'<line x1="{ox+10}" y1="{GY}" x2="{ox+640}" y2="{GY}" stroke="{INK}" stroke-width="3"/>')
        s.append(f'<rect x="{ox+10}" y="{GY}" width="630" height="14" fill="url(#hatch)"/>')
        if faint:  # geometrischer Schatten unterhalb der Linie Quelle–Kante
            s.append(f'<path d="M{wx+7} {wy} L{wx+7+(wy-40)/1.26:.0f} 40 L{ox+640} 40 L{ox+640} {GY} L{wx+14} {GY} L{wx+14} {wy}z" fill="#f3eff0"/>')
        g = [f'<g clip-path="url(#cl{i})">']
        r = lam
        while r < 260:
            g.append(f'<circle cx="{sx}" cy="{sy}" r="{r}" fill="none" stroke="{RED}" stroke-width="{1.6 if faint else 2.4}" opacity=".75"/>')
            r += lam
        g.append('</g>')
        s += g
        g = [f'<g clip-path="url(#cr{i})">']
        r = lam
        while r < 470:
            if faint:
                g.append(_arc(wx + 7, wy, r, -90, a_end, stroke=RED, stroke_width=1.6, opacity=".75"))
                g.append(_arc(wx + 7, wy, r, a_end, 25, stroke=RED, stroke_width=1.2, opacity=".14"))
            else:
                g.append(_arc(wx + 7, wy, r, -90, a_end, stroke=RED, stroke_width=2.4, opacity=".75"))
            r += lam
        g.append('</g>')
        s += g
        s.append(f'<rect x="{ox+40}" y="{sy-20}" width="120" height="{GY-sy+20}" rx="5" fill="#4a4a4a"/>')
        s.append(f'<circle cx="{sx}" cy="{sy}" r="8" fill="{RED}"/>')
        s.append(f'<rect x="{wx}" y="{wy}" width="14" height="{GY-wy}" fill="#7a7a7a"/>')
        s.append(_house(ox + 505, GY))
        s.append(txt(ox + 25, 30, title, 19, INK, "start", "700"))
        s.append(f'<rect x="{ox+245}" y="{GY-44}" width="{len(sub)*9.4+20:.0f}" height="30" rx="4" fill="#fff" opacity=".92"/>')
        s.append(txt(ox + 255, GY - 23, sub, 17, MUT if faint else RED, "start", "700"))
    s.append('</svg>')
    return "".join(s)


def reflection(L):
    """Zwei Felder: Mehrfachreflexion an harter Wand gegenüber Absorption mit HSA3."""
    W, H, GY = 1300, 430, 380
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-label="{L["r_aria"]}">', DEFS,
         f'<rect width="{W}" height="{H}" fill="#fff"/>',
         f'<line x1="650" y1="30" x2="650" y2="{H-20}" stroke="{LINE}" stroke-width="2"/>']
    for i in (0, 1):
        ox = i * 655
        ux0, ux1, uy = ox + 50, ox + 230, 200     # Anlage
        wx, wy = ox + 300, 110                    # Wand nah an der Quelle
        s.append(f'<line x1="{ox+10}" y1="{GY}" x2="{ox+640}" y2="{GY}" stroke="{INK}" stroke-width="3"/>')
        s.append(f'<rect x="{ox+10}" y="{GY}" width="630" height="14" fill="url(#hatch)"/>')
        s.append(f'<rect x="{ux0}" y="{uy}" width="{ux1-ux0}" height="{GY-uy}" rx="6" fill="#4a4a4a"/>')
        s.append(f'<rect x="{ux0+20}" y="{uy-14}" width="{ux1-ux0-40}" height="14" rx="3" fill="#6b6b6b"/>')
        s.append(txt((ux0 + ux1) / 2, uy + 110, L["src"], 17, "#fff", "middle", "700"))
        s.append(f'<rect x="{wx}" y="{wy}" width="18" height="{GY-wy}" fill="#7a7a7a"/>')
        if i == 0:
            s.append(txt(ox + 25, 30, L["r_ref"], 19, INK, "start", "700"))
            pts = [(ux1, 340), (wx, 310), (ux1, 280), (wx, 250), (ux1, 220), (wx, 190)]
            d = "M" + " L".join(f"{x} {y}" for x, y in pts)
            s.append(f'<path d="{d}" fill="none" stroke="{RED}" stroke-width="4" stroke-linejoin="round"/>')
            for (x, y), op, ey in zip(((ux1, 280), (ux1, 220), (wx, 190)), (".45", ".7", "1"), (300, 270, 240)):
                s.append(f'<path d="M{x} {y} L{wx+9} {wy} L{ox+610} {ey}" fill="none" stroke="{RED}" stroke-width="3.5" opacity="{op}" marker-end="url(#ar)"/>')
            for x, y in ((wx, 310), (wx, 250), (ux1, 280), (ux1, 220)):
                s.append(f'<circle cx="{x}" cy="{y}" r="6" fill="#fff" stroke="{RED}" stroke-width="3"/>')
            s.append(f'<circle cx="{wx+9}" cy="{wy}" r="7" fill="#fff" stroke="{RED}" stroke-width="3"/>')
            s.append(txt(ox + 360, 320, L["r_ref2"], 16, RED, "start", "700"))
            s.append(txt(ox + 25, 75, L["r_mirror"], 15, MUT))
            s.append(f'<line x1="{ox+90}" y1="82" x2="{ux1-6}" y2="216" stroke="{MUT}" stroke-width="1.5"/>')
        else:
            s.append(f'<rect x="{wx-14}" y="{wy}" width="14" height="{GY-wy}" fill="url(#hsa)"/>')
            s.append(txt(ox + 25, 30, L["r_abs"], 19, INK, "start", "700"))
            for y0, y1 in ((340, 310), (280, 260)):
                s.append(f'<line x1="{ux1}" y1="{y0}" x2="{wx-18}" y2="{y1}" stroke="{RED}" stroke-width="4" marker-end="url(#ar)"/>')
            s.append(f'<path d="M{ux1} 215 L{wx+9} {wy} L{ox+610} 300" fill="none" stroke="{RED}" stroke-width="3" opacity=".45" marker-end="url(#ar)"/>')
            s.append(f'<circle cx="{wx+9}" cy="{wy}" r="7" fill="#fff" stroke="{RED}" stroke-width="3"/>')
            s.append(txt(ox + 360, 320, L["r_abs2"], 16, INK, "start", "700"))
            s.append(txt(ox + 360, 366, L["r_heat"], 15, MUT))
    s.append('</svg>')
    return "".join(s)


def build():
    OUT.mkdir(parents=True, exist_ok=True)
    for lang, L in T.items():
        sfx = "" if lang == "de" else "-en"
        (OUT / f"wechselrichter-haube{sfx}.svg").write_text(inverter(L), encoding="utf-8")
        (OUT / f"schallwand-prinzip{sfx}.svg").write_text(barrier(L), encoding="utf-8")
        (OUT / f"schallwand-frequenz{sfx}.svg").write_text(frequency(L), encoding="utf-8")
        (OUT / f"schallwand-reflexion{sfx}.svg").write_text(reflection(L), encoding="utf-8")
        (OUT / f"hsa3-aufbau{sfx}.svg").write_text(hsa3(L), encoding="utf-8")
        (OUT / f"bess-ohne-schallschutz{sfx}.svg").write_text(bess(L, False), encoding="utf-8")
        (OUT / f"bess-mit-forcotech{sfx}.svg").write_text(bess(L, True), encoding="utf-8")
    print("SVG-Zeichnungen erzeugt")


if __name__ == "__main__":
    build()
