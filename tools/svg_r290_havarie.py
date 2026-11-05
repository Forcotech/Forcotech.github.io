#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Erzeugt img/r290/r290-5-havarie-<sprache>.svg (ATEX-Konzept, Havariefall) für die Technik-Seite.

Aufruf:  python3 tools/svg_r290_havarie.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INK, RED, BLUE, GREY = "#3A3A3A", "#C8102E", "#1F5FA8", "#E6E6E6"

T = {
    "de": dict(title="Havariefall R290: Gaswarnung schaltet die Geräteventilatoren",
               fans="Ventilatoren 100 %", air="Außenluft", gas="Propan am Boden",
               sens="Gassensor", gwz=["Gaswarn-", "zentrale"], exz="außerhalb Ex-Zone",
               steps=[("Voralarm", "Ventilatoren 100 %, Meldung GLT"),
                      ("Hauptalarm", "Verdichter aus, Warnleuchte und Hupe"),
                      ("Entwarnung", "Nachlauf, Freigabe nur nach Quittierung")],
               foot="Schema, nicht maßstäblich. Voraussetzung: Freigabe des Geräteherstellers."),
    "en": dict(title="R290 leak: gas detection switches the unit fans",
               fans="Fans 100 %", air="Outdoor air", gas="Propane at floor level",
               sens="Gas sensor", gwz=["Gas detection", "controller"], exz="outside Ex zone",
               steps=[("Pre-alarm", "Fans 100 %, signal to BMS"),
                      ("Main alarm", "Compressors off, beacon and horn"),
                      ("All clear", "Run-on, restart only after reset")],
               foot="Schematic, not to scale. Requires approval by the unit manufacturer."),
    "fr": dict(title="Fuite de R290 : la détection gaz pilote les ventilateurs",
               fans="Ventilateurs 100 %", air="Air extérieur", gas="Propane au sol",
               sens="Détecteur", gwz=["Centrale de", "détection gaz"], exz="hors zone Ex",
               steps=[("Pré-alarme", "Ventilateurs 100 %, report GTB"),
                      ("Alarme", "Compresseurs arrêtés, flash et sirène"),
                      ("Fin d’alarme", "Post-ventilation, réarmement manuel")],
               foot="Schéma, sans échelle. Condition : accord du fabricant de l’appareil."),
}


def svg(lang):
    t = T[lang]
    o = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 900 400" width="900" height="400" '
         f'font-family="Arial, Helvetica, sans-serif" lang="{lang}"><title>{t["title"]}</title>',
         '<rect width="900" height="400" fill="#ffffff"/>',
         f'<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
         f'<marker id="ab" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto">'
         f'<path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker>'
         '<linearGradient id="gas" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FF9A1F" stop-opacity="0"/>'
         '<stop offset="1" stop-color="#FF9A1F" stop-opacity="0.6"/></linearGradient></defs>']
    a = o.append
    G = 300
    # Boden
    a(f'<line x1="20" y1="{G}" x2="500" y2="{G}" stroke="{INK}" stroke-width="4"/>')
    for x in range(40, 500, 40):
        a(f'<line x1="{x}" y1="{G}" x2="{x-12}" y2="{G+12}" stroke="{INK}" stroke-width="2"/>')
    # Gasschicht
    a(f'<rect x="96" y="{G-34}" width="308" height="34" fill="url(#gas)"/>')
    # Haube: Wände mit Bodenspalt, Dachring
    a(f'<path d="M90,{G-48} L90,70 L410,70 L410,{G-48}" fill="none" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    for y in (G-46, G-34, G-22):
        a(f'<line x1="70" y1="{y}" x2="88" y2="{y+6}" stroke="{INK}" stroke-width="3"/>')
        a(f'<line x1="430" y1="{y}" x2="412" y2="{y+6}" stroke="{INK}" stroke-width="3"/>')
    a(f'<rect x="150" y="62" width="200" height="16" fill="#fff"/>')
    for x in range(160, 350, 32):
        a(f'<line x1="{x}" y1="78" x2="{x+12}" y2="62" stroke="{INK}" stroke-width="3"/>')
    # Gerät
    a(f'<rect x="150" y="140" width="200" height="{G-140}" rx="4" fill="{GREY}" stroke="{INK}" stroke-width="3"/>')
    for cx in (195, 250, 305):
        a(f'<circle cx="{cx}" cy="160" r="16" fill="none" stroke="{INK}" stroke-width="3"/>')
    a(f'<text x="250" y="232" font-size="15" font-weight="bold" fill="{RED}" text-anchor="middle">R290</text>')
    # Abluft Ventilatoren
    for cx in (195, 250, 305):
        a(f'<path d="M{cx},138 L{cx},28" stroke="{BLUE}" stroke-width="4" fill="none" marker-end="url(#ab)"/>')
    a(f'<text x="320" y="40" font-size="15" font-weight="bold" fill="{BLUE}">{t["fans"]}</text>')
    # Nachströmung bodennah
    a(f'<path d="M22,{G-30} L120,{G-30}" stroke="{INK}" stroke-width="3.5" fill="none" marker-end="url(#ar)"/>')
    a(f'<path d="M500,{G-30} L420,{G-30}" stroke="{INK}" stroke-width="3.5" fill="none" marker-end="url(#ar)"/>')
    a(f'<text x="20" y="{G+38}" font-size="14" fill="{INK}">{t["air"]}</text>')
    a(f'<text x="232" y="{G+38}" font-size="14" fill="#B35C00" text-anchor="middle">{t["gas"]}</text>')
    # Sensor
    a(f'<path d="M372,{G-24} l12,22 l-24,0 z" fill="{RED}" stroke="#fff" stroke-width="1.5"/>')
    a(f'<text x="392" y="{G+38}" font-size="14" fill="{RED}" text-anchor="middle">{t["sens"]}</text>')
    # Gaswarnzentrale + Leitung
    a(f'<rect x="430" y="96" width="120" height="56" rx="4" fill="#fff" stroke="{INK}" stroke-width="3"/>')
    a(f'<text x="490" y="119" font-size="13" font-weight="bold" fill="{INK}" text-anchor="middle">{t["gwz"][0]}</text>')
    a(f'<text x="490" y="137" font-size="13" font-weight="bold" fill="{INK}" text-anchor="middle">{t["gwz"][1]}</text>')
    a(f'<text x="490" y="170" font-size="12" fill="{INK}" text-anchor="middle">{t["exz"]}</text>')
    a(f'<path d="M384,{G-12} L566,{G-12} L566,124 L550,124" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="6 4"/>')
    a(f'<path d="M430,110 L370,110 L330,150" fill="none" stroke="{RED}" stroke-width="2" stroke-dasharray="6 4"/>')
    # Ablauf rechts
    x0, y0 = 578, 70
    for i, (h, d) in enumerate(t["steps"]):
        y = y0 + i * 82
        a(f'<rect x="{x0}" y="{y}" width="310" height="64" rx="6" fill="#fff" stroke="{INK}" stroke-width="2"/>')
        a(f'<circle cx="{x0+26}" cy="{y+32}" r="15" fill="{RED}"/>')
        a(f'<text x="{x0+26}" y="{y+38}" font-size="16" font-weight="bold" fill="#fff" text-anchor="middle">{i+1}</text>')
        a(f'<text x="{x0+52}" y="{y+27}" font-size="16" font-weight="bold" fill="{INK}">{h}</text>')
        a(f'<text x="{x0+52}" y="{y+48}" font-size="13" fill="{INK}">{d}</text>')
        if i < 2:
            a(f'<path d="M{x0+155},{y+64} L{x0+155},{y+80}" stroke="{INK}" stroke-width="2.5" marker-end="url(#ar)"/>')
    a(f'<text x="450" y="368" font-size="20" font-weight="bold" fill="{INK}" text-anchor="middle">{t["title"]}</text>')
    a(f'<text x="450" y="392" font-size="13" fill="{INK}" text-anchor="middle">{t["foot"]}</text>')
    a('</svg>')
    return "".join(o)


if __name__ == "__main__":
    for lang in T:
        p = ROOT / "img" / "r290" / f"r290-5-havarie-{lang}.svg"
        p.write_text(svg(lang), encoding="utf-8")
        print("geschrieben:", p.relative_to(ROOT))
