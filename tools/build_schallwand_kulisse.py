#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Baut die Spezialthema-Seite „Schallwand + Abluft-Schalldämpfer“
(/loesungen/schallwand-kulisse/, /en/solutions/noise-barrier-and-silencer/, /fr/ecran-et-silencieux/)
aus schallwand-kulisse/_src/<sprache>.html.

Inhalt ändern: Fragment in schallwand-kulisse/_src/de.html, en.html bzw. fr.html bearbeiten und
python3 tools/build_schallwand_kulisse.py  ausführen (danach wie immer tools/build_news.py für Navigation/Sitemap).
Die FAQ-Daten (schema.org FAQPage) werden aus den <details>-Fragen erzeugt. Kopf, Navigation und Fuß aus tools/build_news.py.

Die Zeichnungen img/schallwand-kulisse/*(.svg, -en.svg, -fr.svg) erzeugt dieses Skript (Beschriftungen in LBL).
Musterauslegung: Werte aus dem Konfigurator (Schallwand mit Option RK-200, Rechenstand 28.10.2026) – bei einer
Änderung des Rechenkerns im Fragment nachziehen.
"""
from pathlib import Path
import build_news as bn
from build_hserie import faq_ld

ROOT = Path(__file__).resolve().parent.parent
URL = {"de": "/loesungen/schallwand-kulisse/", "en": "/en/solutions/noise-barrier-and-silencer/", "fr": "/fr/ecran-et-silencieux/"}
K = "https://www.forcotech.com/konfigurator/"
Q = "?sd=1&amp;L=4900&amp;B=2240&amp;H=2400&amp;lw=92&amp;hp=500&amp;dist=25&amp;hR=5&amp;hW=4000"
CFG = {"de": K + "schallwand/" + Q, "en": K + "en/schallwand/" + Q, "fr": K + "fr/schallwand/" + Q}
SD = {"de": K + "schalldaempfer/", "en": K + "en/schalldaempfer/", "fr": K + "fr/schalldaempfer/"}
IMG = ROOT / "img" / "schallwand-kulisse"
SUF = {"de": "", "en": "-en", "fr": "-fr"}

TXT = {
    "de": {"title": "Schallwand + Abluft-Schalldämpfer – mehr Schallschutz ohne Haube | ForCoTech",
           "desc": "Wenn eine Schallwand allein nicht reicht und eine Haube zu viel ist: Kombination aus HSA3-Schallwand und aufgesetztem Abluft-Schalldämpfer RK-200. Zwei Schallwege, eine Höhenregel, Musterauslegung und Rechnung im Konfigurator.",
           "kicker": "Spezialthema · Neu",
           "h1": "Schallwand + Abluft-Schalldämpfer – mehr Minderung, ohne Haube",
           "lead": "Eine Schallwand schirmt die seitliche Abstrahlung ab, der Schalldämpfer auf dem Gerät mindert alles, was oben durch die Ventilatoren austritt. Zusammen schließen sie die Lücke zwischen Wand und Haube – Gerät frei zugänglich, oben offen, nur wenige Pascal Druckverlust.",
           "b1": "Kombination berechnen", "b2": "Schalldämpfer auslegen",
           "facts": [("2 Wege", "oben und seitlich – getrennt gemindert"), ("−13…17 dB(A)", "Schalldämpfer im Abluftweg (Abschätzung)"),
                     ("≈ 4–8 Pa", "Druckverlust des Schalldämpfers"), ("A1", "Wand und Röhren aus HSA3, nicht brennbar")]},
    "en": {"title": "Noise barrier + exhaust silencer – more noise reduction without an enclosure | ForCoTech",
           "desc": "When a noise barrier alone is not enough and an enclosure is too much: combination of an HSA3 noise barrier and the exhaust silencer RK-200 on the unit. Two sound paths, one height rule, sample design and calculation in the configurator.",
           "kicker": "Special topic · New",
           "h1": "Noise barrier + exhaust silencer – more reduction, no enclosure",
           "lead": "A noise barrier screens the side radiation, the silencer on the unit reduces everything leaving at the top through the fans. Together they close the gap between barrier and enclosure – unit freely accessible, open at the top, only a few pascals of pressure drop.",
           "b1": "Calculate the combination", "b2": "Design the silencer",
           "facts": [("2 paths", "top and side – reduced separately"), ("−13…17 dB(A)", "silencer in the exhaust path (estimate)"),
                     ("≈ 4–8 Pa", "pressure drop of the silencer"), ("A1", "barrier and tubes of HSA3, non-combustible")]},
    "fr": {"title": "Écran acoustique + silencieux d’extraction – plus d’atténuation sans caisson | ForCoTech",
           "desc": "Quand un écran seul ne suffit pas et qu’un caisson est de trop : combinaison d’un écran acoustique HSA3 et du silencieux d’extraction RK-200 posé sur l’appareil. Deux chemins acoustiques, une règle de hauteur, exemple de dimensionnement et calcul dans le configurateur.",
           "kicker": "Dossier spécial · Nouveau",
           "h1": "Écran acoustique + silencieux d’extraction – plus d’atténuation, sans caisson",
           "lead": "L’écran protège du rayonnement latéral, le silencieux posé sur l’appareil réduit tout ce qui sort par le haut à travers les ventilateurs. Ensemble, ils comblent l’écart entre écran et caisson – appareil librement accessible, ouvert en partie haute, quelques pascals de perte de charge seulement.",
           "b1": "Calculer la combinaison", "b2": "Dimensionner le silencieux",
           "facts": [("2 chemins", "haut et latéral – réduits séparément"), ("−13…17 dB(A)", "silencieux au refoulement (estimation)"),
                     ("≈ 4–8 Pa", "perte de charge du silencieux"), ("A1", "écran et tubes en HSA3, incombustibles")]},
}

LBL = {
    "de": {"t1": "Zwei Schallwege – zwei Maßnahmen", "top": "Abluft oben", "top2": "Ventilatoren + ausgetragener Verdichterschall",
           "top3": "→ Abluft-Schalldämpfer RK-200", "side": "seitliche Abstrahlung", "side2": "Gehäuse, Verdichter",
           "side3": "→ Schallwand mit HSA3", "unit": "Gerät", "sil": "RK-200", "wall": "Schallwand", "win": "Fenster",
           "rule": "seitlich typisch 5 dB (Scroll) bzw. 7 dB (Schraube) unter oben",
           "t2": "Die Höhenregel", "bad": "Wand zu niedrig", "bad2": "Austritt sieht das Fenster – Abluftweg maßgeblich",
           "good": "Wand hoch genug", "good2": "Sichtlinie unterbrochen – beide Wege abgeschirmt", "line": "Sichtlinie"},
    "en": {"t1": "Two sound paths – two measures", "top": "Exhaust at the top", "top2": "fans + compressor noise carried out with the air",
           "top3": "→ exhaust silencer RK-200", "side": "side radiation", "side2": "casing, compressor",
           "side3": "→ noise barrier with HSA3", "unit": "Unit", "sil": "RK-200", "wall": "Barrier", "win": "Window",
           "rule": "side typically 5 dB (scroll) or 7 dB (screw) below top",
           "t2": "The height rule", "bad": "Barrier too low", "bad2": "outlet sees the window – exhaust path dominant",
           "good": "Barrier high enough", "good2": "line of sight broken – both paths screened", "line": "line of sight"},
    "fr": {"t1": "Deux chemins acoustiques – deux mesures", "top": "Refoulement en haut", "top2": "ventilateurs + bruit du compresseur entraîné",
           "top3": "→ silencieux d’extraction RK-200", "side": "rayonnement latéral", "side2": "enveloppe, compresseur",
           "side3": "→ écran acoustique HSA3", "unit": "Appareil", "sil": "RK-200", "wall": "Écran", "win": "Fenêtre",
           "rule": "latéral en général 5 dB (scroll) ou 7 dB (vis) sous le haut",
           "t2": "La règle de hauteur", "bad": "Écran trop bas", "bad2": "la sortie voit la fenêtre – refoulement déterminant",
           "good": "Écran assez haut", "good2": "ligne de vue interrompue – les deux chemins protégés", "line": "ligne de vue"},
}
INK, MUT, RED, GRN, LINE = "#1a1a1a", "#5c5c5c", "#c8202f", "#1d7a3e", "#e6e1e1"
FONT = 'font-family="system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif"'


def _unit(x, y0, w, h, sil_h, frame_h, L):
    """Gerät mit Ventilatoren, Übergangsrahmen und Schalldämpfer (Seitenansicht). y0 = Boden."""
    top = y0 - h
    s = f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="#f3f1f1" stroke="{INK}" stroke-width="2.5"/>'
    s += f'<text x="{x + w / 2}" y="{top + h / 2 + 7}" text-anchor="middle" font-size="19" font-weight="700" fill="{INK}">{L["unit"]}</text>'
    for i in range(3):
        cx = x + w * (i + 0.5) / 3
        s += f'<ellipse cx="{cx}" cy="{top}" rx="{w / 8}" ry="5" fill="#fff" stroke="{INK}" stroke-width="1.8"/>'
    fy = top - frame_h
    s += f'<rect x="{x}" y="{fy}" width="{w}" height="{frame_h}" fill="#e9e6e6" stroke="{INK}" stroke-width="1.5"/>'
    sy = fy - sil_h
    s += f'<rect x="{x}" y="{sy}" width="{w}" height="{sil_h}" fill="#fdecee" stroke="{RED}" stroke-width="2.5"/>'
    for i in range(int(w // 22)):
        cx = x + 11 + i * 22
        s += f'<line x1="{cx}" y1="{sy + 4}" x2="{cx}" y2="{fy - 4}" stroke="{RED}" stroke-width="1.2" stroke-opacity=".55"/>'
    return s, sy


def _house(x, y0, L, wy):
    s = f'<path d="M{x} {y0} V{y0 - 190} L{x + 70} {y0 - 240} L{x + 140} {y0 - 190} V{y0} Z" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
    s += f'<rect x="{x + 18}" y="{wy - 18}" width="40" height="36" fill="#eaf2f8" stroke="{INK}" stroke-width="2"/>'
    s += f'<text x="{x + 70}" y="{y0 - 12}" text-anchor="middle" font-size="15" fill="{MUT}">{L["win"]}</text>'
    return s


def svg_wege(lang):
    L = {k: bn.e(v) for k, v in LBL[lang].items()}
    y0 = 400
    u, sy = _unit(90, y0, 190, 130, 46, 20, L)
    wall_x, wall_top = 360, 176
    wx, wy = 640, 262
    s = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 470" {FONT} role="img" aria-label="{L["t1"]}">
<title>{L["t1"]}</title>
<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="{RED}"/></marker>
<marker id="ag" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="{INK}"/></marker></defs>
<rect width="820" height="470" fill="#fff"/>
<line x1="20" y1="{y0}" x2="800" y2="{y0}" stroke="{INK}" stroke-width="2"/>
{u}
<rect x="{wall_x}" y="{wall_top}" width="16" height="{y0 - wall_top}" fill="#fdecee" stroke="{RED}" stroke-width="2.5"/>
<text x="{wall_x + 26}" y="{y0 - 16}" font-size="15" font-weight="700" fill="{INK}">{L["wall"]}</text>
{_house(wx - 20, y0, L, wy)}
<path d="M185 {sy - 4} C 230 {sy - 70}, 320 {wall_top - 40}, {wall_x + 8} {wall_top - 6} S 560 {wy - 60}, {wx - 4} {wy - 6}" fill="none" stroke="{RED}" stroke-width="3.5" marker-end="url(#ar)"/>
<path d="M282 {y0 - 70} L {wall_x - 4} {y0 - 120}" fill="none" stroke="{INK}" stroke-width="3.5" stroke-dasharray="9 6" marker-end="url(#ag)"/>
<text x="20" y="36" font-size="18" font-weight="700" fill="{RED}">{L["top"]}</text>
<text x="20" y="58" font-size="15" fill="{INK}">{L["top2"]}</text>
<text x="20" y="80" font-size="15" font-weight="700" fill="{RED}">{L["top3"]}</text>
<text x="20" y="440" font-size="16" font-weight="700" fill="{INK}">{L["side"]} ({L["side2"]}) {L["side3"]}</text>
<text x="20" y="462" font-size="14" fill="{MUT}">{L["rule"]}</text>
<rect x="145" y="{sy + 12}" width="80" height="24" rx="4" fill="#fff"/><text x="185" y="{sy + 30}" text-anchor="middle" font-size="15" font-weight="700" fill="{RED}">{L["sil"]}</text>
</svg>
'''
    return s


def _panel(ox, wall_top, ok, L):
    y0 = 380
    u, sy = _unit(ox + 20, y0, 120, 110, 40, 16, L)
    wall_x, wx, wy = ox + 200, ox + 300, 250
    out = (ox + 80, sy)
    s = u
    s += f'<rect x="{wall_x}" y="{wall_top}" width="13" height="{y0 - wall_top}" fill="#fdecee" stroke="{RED}" stroke-width="2.5"/>'
    s += f'<rect x="{wx}" y="{wy - 16}" width="34" height="32" fill="#eaf2f8" stroke="{INK}" stroke-width="2"/>'
    s += f'<line x1="{wx + 17}" y1="{wy + 16}" x2="{wx + 17}" y2="{y0}" stroke="{INK}" stroke-width="2"/>'
    s += f'<line x1="{ox}" y1="{y0}" x2="{ox + 360}" y2="{y0}" stroke="{INK}" stroke-width="2"/>'
    s += f'<line x1="{out[0]}" y1="{out[1]}" x2="{wx}" y2="{wy}" stroke="{RED if not ok else MUT}" stroke-width="3" stroke-dasharray="{"0" if not ok else "8 6"}"/>'
    if ok:
        s += f'<path d="M{out[0]} {out[1]} L{wall_x + 6} {wall_top - 4} L{wx} {wy}" fill="none" stroke="{GRN}" stroke-width="3"/>'
    sym = (f'<circle cx="{ox + 330}" cy="140" r="20" fill="{GRN}"/><path d="M{ox + 320} 140 l7 8 l14 -16" fill="none" stroke="#fff" stroke-width="4"/>' if ok else
           f'<circle cx="{ox + 330}" cy="140" r="20" fill="{RED}"/><path d="M{ox + 322} 132 l16 16 M{ox + 338} 132 l-16 16" stroke="#fff" stroke-width="4"/>')
    s += sym
    s += f'<text x="{ox}" y="66" font-size="19" font-weight="700" fill="{GRN if ok else RED}">{L["good"] if ok else L["bad"]}</text>'
    s += f'<text x="{ox}" y="90" font-size="14.5" fill="{INK}">{L["good2"] if ok else L["bad2"]}</text>'
    return s


def svg_hoehe(lang):
    L = {k: bn.e(v) for k, v in LBL[lang].items()}
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 820 420" {FONT} role="img" aria-label="{L["t2"]}">
<title>{L["t2"]}</title>
<rect width="820" height="420" fill="#fff"/>
{_panel(20, 250, False, L)}
<line x1="410" y1="40" x2="410" y2="400" stroke="{LINE}" stroke-width="2"/>
{_panel(440, 150, True, L)}
<text x="20" y="410" font-size="13.5" fill="{MUT}">— {L["line"]}</text>
</svg>
'''


def build():
    IMG.mkdir(parents=True, exist_ok=True)
    for lang in URL:
        (IMG / f"zwei-wege{SUF[lang]}.svg").write_text(svg_wege(lang), encoding="utf-8")
        (IMG / f"hoehenregel{SUF[lang]}.svg").write_text(svg_hoehe(lang), encoding="utf-8")
        t = TXT[lang]
        frag = (ROOT / "schallwand-kulisse" / "_src" / f"{lang}.html").read_text(encoding="utf-8")
        frag = frag.replace("{{CFG}}", CFG[lang]).replace("{{SD}}", SD[lang]).replace("{{SUF}}", SUF[lang])
        facts = "".join(f"<div><b>{bn.e(b)}</b><span>{bn.e(s)}</span></div>" for b, s in t["facts"])
        main = f"""<div class="hero">
  <div class="wrap hg">
    <div>
      <span class="kicker">{t["kicker"]}</span>
      <h1>{t["h1"]}</h1>
      <p class="lead">{t["lead"]}</p>
      <div class="btns"><a class="btn" href="{CFG[lang]}">{t["b1"]}</a><a class="btn ghost" href="{SD[lang]}">{t["b2"]}</a></div>
    </div>
    <div class="stats">{facts}</div>
  </div>
</div>
{frag}"""
        head = f'<script type="application/ld+json">{faq_ld(frag, lang)}</script>'
        bn.write(URL[lang][1:] + "index.html", bn.page(lang, t["title"], t["desc"], dict(URL), main, extra_head=head, typ="wand"))
    print("Seiten Schallwand + Abluft-Schalldämpfer gebaut (de, en, fr)")


if __name__ == "__main__":
    build()
