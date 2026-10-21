#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Isometrie Schallhaube mit Adiabatik-Modul (img/adiabatik/adiabatik-isometrie(-en|-fr).svg).
Wird von tools/build_adiabatik.py aufgerufen; Beschriftungen in ISO_LBL.
Schematische Darstellung, Maße in mm (Musterhaube L 6000 × B 2500 × H 2600)."""
import math
from html import escape as e

ISO_LBL = {
    "de": {"title": "Isometrie Schallhaube mit Adiabatik-Modul", "mod": "Adiabatik-Modul", "mod2": "benetzte Verdunstungsfläche",
           "water": "Wasserzulauf", "water2": "Osmosewasser · Systemtrenner EN 1717", "drain": "Ablaufrinne",
           "drain2": "Einweg, ohne Umwälzung", "out": "Außenluft 35 °C", "pre": "vorgekühlt ≈ 26–29 °C",
           "sil": "Abluft-Schalldämpfer HSA3", "exh": "Abluft", "hood": "Schallhaube, HSA3-Innenverkleidung A1",
           "unit": "Kaltwassersatz", "coil": "Register", "cut": "Teilschnitt"},
    "en": {"title": "Isometric view of an acoustic enclosure with adiabatic module", "mod": "Adiabatic module", "mod2": "wetted evaporation surface",
           "water": "Water supply", "water2": "RO water · backflow preventer EN 1717", "drain": "Drain channel",
           "drain2": "once-through, no recirculation", "out": "Outdoor air 35 °C", "pre": "pre-cooled ≈ 26–29 °C",
           "sil": "Exhaust silencer HSA3", "exh": "Exhaust air", "hood": "Acoustic enclosure, HSA3 lining A1",
           "unit": "Chiller", "coil": "Coil", "cut": "Cutaway"},
    "fr": {"title": "Vue isométrique d’un caisson acoustique avec module adiabatique", "mod": "Module adiabatique", "mod2": "surface d’évaporation humidifiée",
           "water": "Arrivée d’eau", "water2": "osmosée · disconnecteur EN 1717", "drain": "Goulotte d’évacuation",
           "drain2": "eau perdue, sans recirculation", "out": "Air extérieur 35 °C", "pre": "pré-refroidi ≈ 26–29 °C",
           "sil": "Silencieux d’air rejeté HSA3", "exh": "Air rejeté", "hood": "Caisson acoustique, revêtement HSA3 A1",
           "unit": "Groupe froid", "coil": "Batterie", "cut": "Coupe partielle"},
}

INK, MUT, RED, BLUE, LINE = "#1a1a1a", "#5c5c5c", "#c8202f", "#2f6f9f", "#e6e1e1"
S, OX, OY = 0.062, 480, 255  # Maßstab px/mm, Ursprung
C30, S30 = math.cos(math.radians(30)), 0.5
L, W, H = 6000, 2500, 2600


def P(x, y, z):
    return (OX + (x - y) * C30 * S, OY + (x + y) * S30 * S - z * S)


def pts(*p):
    return " ".join(f"{a:.1f},{b:.1f}" for a, b in (P(*q) for q in p))


def poly(*p, fill="#fff", stroke=INK, sw=1.6, extra=""):
    return f'<polygon points="{pts(*p)}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"{extra}/>'


def line(a, b, stroke=INK, sw=1.5, extra=""):
    (x1, y1), (x2, y2) = P(*a), P(*b)
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{stroke}" stroke-width="{sw}"{extra}/>'


def label(anchor, dx, dy, t1, t2="", color=INK, end=False):
    ax, ay = P(*anchor)
    tx, ty = ax + dx, ay + dy
    a = ' text-anchor="end"' if end else ""
    out = (f'<line x1="{ax:.1f}" y1="{ay:.1f}" x2="{tx:.1f}" y2="{ty:.1f}" stroke="{MUT}" stroke-width="1"/>'
           f'<circle cx="{ax:.1f}" cy="{ay:.1f}" r="2.6" fill="{MUT}"/>'
           f'<text x="{tx + (-4 if end else 4):.1f}" y="{ty - 4:.1f}" font-size="14" font-weight="700" fill="{color}"{a}>{e(t1)}</text>')
    if t2:
        out += f'<text x="{tx + (-4 if end else 4):.1f}" y="{ty + 13:.1f}" font-size="12.5" fill="{MUT}"{a}>{e(t2)}</text>'
    return out


def svg(lang):
    T = ISO_LBL[lang]
    o = []
    # Bodenplatte
    o.append(poly((-200, -200, 0), (L + 200, -200, 0), (L + 200, W + 700, 0), (-200, W + 700, 0), fill="#f3f1f1", stroke="#d9d4d4", sw=1))
    # Haube: sichtbare Flächen y=W (links vorn), x=L (rechts vorn, mit Teilschnitt), Dach
    o.append(poly((0, W, 0), (L, W, 0), (L, W, H), (0, W, H), fill="#ffffff"))
    # Teilschnitt in Fläche x=L: Rahmen mit Öffnung (evenodd)
    y0, y1, z0, z1 = 250, W - 250, 250, H - 300
    outer = [P(L, 0, 0), P(L, W, 0), P(L, W, H), P(L, 0, H)]
    hole = [P(L, y0, z0), P(L, y0, z1), P(L, y1, z1), P(L, y1, z0)]
    d = "M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in outer) + " Z M" + " L".join(f"{a:.1f},{b:.1f}" for a, b in hole) + " Z"
    # Innenleben hinter der Öffnung: Rückwand, Boden, Kaltwassersatz-Stirnseite
    o.append(poly((L, y0, z0), (L - 2000, y0, z0), (L - 2000, y0, z1), (L, y0, z1), fill="#ece8e8", stroke="#d9d4d4", sw=1))
    cx = L - 450  # Stirnseite Kaltwassersatz
    cy0, cy1 = 300, W - 1100
    o.append(poly((cx, cy0, 0), (cx, cy1, 0), (cx, cy1, 1900), (cx, cy0, 1900), fill="#e9e6e6", stroke=INK, sw=1.4))
    o.append(poly((cx, cy1, 0), (cx, cy1 - 220, 0), (cx, cy1 - 220, 1900), (cx, cy1, 1900), fill="url(#ih)", stroke=INK, sw=1))
    o.append(poly((cx, cy0, 1900), (cx, cy1, 1900), (cx - 900, cy1, 1900), (cx - 900, cy0, 1900), fill="#f6f4f4", stroke=INK, sw=1))
    # vorgekühlte Luft im Schnitt (Richtung −y zum Register)
    a, b = P(cx + 150, W - 280, 1000), P(cx + 150, W - 1060, 1000)
    o.append(f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" stroke="{BLUE}" stroke-width="3.5" marker-end="url(#ib)"/>')
    o.append(f'<path d="{d}" fill="#ffffff" fill-rule="evenodd" stroke="{INK}" stroke-width="1.6" stroke-linejoin="round"/>')
    # HSA3-Innenverkleidung an der Schnittkante
    o.append(poly((L, y0, z0), (L, y0, z1), (L, y1, z1), (L, y1, z0), fill="none", stroke=RED, sw=2, extra=' stroke-dasharray="5 4"'))
    # Dach
    o.append(poly((0, 0, H), (L, 0, H), (L, W, H), (0, W, H), fill="#faf9f9"))
    # Abluft-Schalldämpfer auf dem Dach
    sx0, sx1, sy0, sy1, sh = 700, L - 700, 350, W - 350, 650
    o.append(poly((sx0, sy1, H), (sx1, sy1, H), (sx1, sy1, H + sh), (sx0, sy1, H + sh), fill="#fdecee"))
    o.append(poly((sx1, sy0, H), (sx1, sy1, H), (sx1, sy1, H + sh), (sx1, sy0, H + sh), fill="#f8dde0"))
    o.append(poly((sx0, sy0, H + sh), (sx1, sy0, H + sh), (sx1, sy1, H + sh), (sx0, sy1, H + sh), fill="#ffffff"))
    for i, yy in enumerate((sy0 + 330, sy0 + 900, sy1 - 330)):
        for xx in range(sx0 + 260 + (i % 2) * 230, sx1 - 150, 460):
            ring = " ".join(f"{px:.1f},{py:.1f}" for px, py in
                            (P(xx + 170 * math.cos(t / 12 * math.pi), yy + 170 * math.sin(t / 12 * math.pi), H + sh) for t in range(24)))
            o.append(f'<polygon points="{ring}" fill="#fff" stroke="{RED}" stroke-width="1.8"/>')
    for xx in (sx0 + 900, (sx0 + sx1) / 2, sx1 - 900):
        a, b = P(xx, (sy0 + sy1) / 2, H + sh + 120), P(xx, (sy0 + sy1) / 2, H + sh + 900)
        o.append(f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" stroke="{MUT}" stroke-width="3" marker-end="url(#ia)"/>')
    # Adiabatik-Modul vor der Fläche y=W
    mx0, mx1, md, mz0, mz1 = 450, L - 450, 480, 250, 2250
    o.append(poly((mx0, W, mz1), (mx1, W, mz1), (mx1, W + md, mz1), (mx0, W + md, mz1), fill="#dbe9f3", stroke=BLUE, sw=1.8))
    o.append(poly((mx1, W, mz0), (mx1, W + md, mz0), (mx1, W + md, mz1), (mx1, W, mz1), fill="#cfe1ee", stroke=BLUE, sw=1.8))
    o.append(poly((mx0, W + md, mz0), (mx1, W + md, mz0), (mx1, W + md, mz1), (mx0, W + md, mz1), fill="#eaf2f8", stroke=BLUE, sw=2.2))
    for xx in range(mx0 + 150, mx1 - 100, 150):  # Zickzack der benetzten Fläche
        zz, path, k = mz1 - 80, [], 0
        while zz > mz0 + 80:
            path.append(P(xx + (60 if k % 2 else 0), W + md, zz)); zz -= 140; k += 1
        o.append('<polyline points="' + " ".join(f"{a:.1f},{b:.1f}" for a, b in path) + f'" fill="none" stroke="{BLUE}" stroke-width="1.3"/>')
    # Verteilrohr oben, Zulauf, Ablaufrinne unten
    o.append(line((mx0, W + md - 120, mz1 + 60), (mx1, W + md - 120, mz1 + 60), stroke=BLUE, sw=5, extra=' stroke-linecap="round"'))
    o.append(line((mx0, W + md - 120, mz1 + 60), (mx0, W + md - 120, mz1 + 900), stroke=BLUE, sw=5, extra=' stroke-linecap="round"'))
    o.append(poly((mx0, W + md, mz0), (mx1, W + md, mz0), (mx1, W + md + 160, mz0 - 60), (mx0, W + md + 160, mz0 - 60), fill="#a9c9df", stroke=BLUE, sw=1.5))
    o.append(line((mx0, W + md + 80, mz0 - 40), (mx0 - 500, W + md + 80, 0), stroke=BLUE, sw=4, extra=' stroke-linecap="round"'))
    # Außenluft-Pfeile auf das Modul
    for xx in (1500, 3000, 4500):
        a, b = P(xx, W + md + 1500, 1250), P(xx, W + md + 180, 1250)
        o.append(f'<path d="M{a[0]:.1f},{a[1]:.1f} L{b[0]:.1f},{b[1]:.1f}" stroke="{MUT}" stroke-width="4" marker-end="url(#ia)"/>')
    # Beschriftungen
    o.append(label((mx0 + 300, W + md, mz1 - 300), -150, -40, T["mod"], T["mod2"], BLUE, end=True))
    o.append(label((mx0, W + md - 120, mz1 + 900), -70, -10, T["water"], T["water2"], BLUE, end=True))
    o.append(label((mx0 + 900, W + md + 160, mz0 - 60), -60, 52, T["drain"], T["drain2"], BLUE, end=True))
    o.append(label((1500, W + md + 1500, 1250), -10, 40, T["out"], "", RED, end=True))
    o.append(label((cx + 150, W - 600, 1000), 175, 50, T["pre"], "", BLUE))
    o.append(label((cx, 900, 1300), 180, 0, T["unit"], f'{T["cut"]} · {T["coil"]}'))
    o.append(label((L, W - 120, 120), 60, 52, T["hood"]))
    o.append(label((sx1, sy0 + 500, H + sh * 0.6), 110, -20, T["sil"]))
    ex = P(sx1 - 900, (sy0 + sy1) / 2, H + sh + 820)
    o.append(f'<text x="{ex[0] + 16:.1f}" y="{ex[1] + 5:.1f}" font-size="13.5" fill="{MUT}">{e(T["exh"])}</text>')
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 60 1060 560" font-family="system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif" role="img" aria-label="{e(T["title"])}">
<title>{e(T["title"])}</title>
<defs><marker id="ia" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="{MUT}"/></marker>
<marker id="ib" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="{BLUE}"/></marker>
<pattern id="ih" width="6" height="6" patternUnits="userSpaceOnUse"><rect width="6" height="6" fill="#f3f1f1"/><path d="M0 6 L6 0" stroke="{MUT}" stroke-width="1"/></pattern></defs>
<rect y="60" width="1060" height="560" fill="#fff"/>
{chr(10).join(o)}
</svg>
"""
