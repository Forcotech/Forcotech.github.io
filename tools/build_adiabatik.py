#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Baut die Produktseite Adiabatik-Modul (/adiabatik/, /en/adiabatic-precooling/, /fr/pre-refroidissement-adiabatique/)
aus adiabatik/_src/<sprache>.html.

Inhalt ändern: Fragment in adiabatik/_src/de.html, en.html bzw. fr.html bearbeiten und
python3 tools/build_adiabatik.py  ausführen.
Die FAQ-Daten (schema.org FAQPage) werden aus den <details>-Fragen im Fragment erzeugt.
Kopf, Navigation und Fuß kommen aus tools/build_news.py.

Die Prinzipskizze img/adiabatik/adiabatik-prinzip(.svg, -en.svg, -fr.svg) erzeugt dieses Skript selbst
aus der Tabelle LBL – Beschriftungen dort ändern.
"""
from pathlib import Path
import build_news as bn
from build_hserie import faq_ld

ROOT = Path(__file__).resolve().parent.parent
URL = {"de": "/adiabatik/", "en": "/en/adiabatic-precooling/", "fr": "/fr/pre-refroidissement-adiabatique/"}
TECH = {"de": "/technik/", "en": "/en/technology/", "fr": "/fr/technique/"}
SVG = {"de": "img/adiabatik/adiabatik-prinzip.svg", "en": "img/adiabatik/adiabatik-prinzip-en.svg",
       "fr": "img/adiabatik/adiabatik-prinzip-fr.svg"}
TXT = {
    "de": {"title": "Adiabatische Vorkühlung in der Schallhaube – Adiabatik-Modul für Kälteanlagen | ForCoTech",
           "desc": "Schallschutz, der mitkühlt: Adiabatik-Modul in der Schallhaube kühlt die Ansaugluft von Kaltwassersätzen und Rückkühlern um ca. 6–9 K vor – Einweg, ohne Sprühdüsen, Zielwert < 25 Pa Druckverlust. Pilotanwender gesucht.",
           "kicker": "Neu · in Erprobung · Adiabatik-Modul",
           "h1": "Schallschutz, der mitkühlt – adiabatische Vorkühlung in der Schall&shy;haube",
           "lead": "Das Adiabatik-Modul kühlt die Ansaugluft von Kälteanlagen an Hitzetagen um ca. 6–9 K vor. Weniger Hochdruckstörungen, mehr Leistung – und leiser, weil die Ventilatoren langsamer drehen dürfen.",
           "b1": "Pilotanwender werden", "b2": "Technik im Detail",
           "mail": "mailto:info@forcotech.com?subject=Pilotanwender%20Adiabatik-Modul",
           "facts": [("6–9 K", "Abkühlung bei 35 °C / 30 % r. F."), ("< 25 Pa", "zusätzlicher Druckverlust (Zielwert)"),
                     ("Einweg", "ohne Umwälzung und Sprühdüsen"), ("A1", "HSA3, nicht brennbar")]},
    "en": {"title": "Adiabatic pre-cooling in the acoustic enclosure – adiabatic module for chillers | ForCoTech",
           "desc": "Noise control that also cools: an adiabatic module in the acoustic enclosure pre-cools the intake air of chillers and dry coolers by approx. 6–9 K – once-through, no spray nozzles, target < 25 Pa pressure drop. Pilot users wanted.",
           "kicker": "New · under test · Adiabatic module",
           "h1": "Noise control that also cools – adiabatic pre-cooling in the acoustic enclosure",
           "lead": "On hot days, the adiabatic module pre-cools the intake air of chillers by approx. 6–9 K. Fewer high-pressure trips, more capacity – and quieter, because the fans can run slower.",
           "b1": "Become a pilot user", "b2": "Technology in detail",
           "mail": "mailto:info@forcotech.com?subject=Pilot%20user%20adiabatic%20module",
           "facts": [("6–9 K", "cooling at 35 °C / 30 % RH"), ("< 25 Pa", "additional pressure drop (target)"),
                     ("Once-through", "no recirculation, no spray nozzles"), ("A1", "HSA3, non-combustible")]},
    "fr": {"title": "Pré-refroidissement adiabatique dans le caisson acoustique – module adiabatique pour groupes froids | ForCoTech",
           "desc": "Une protection acoustique qui rafraîchit : le module adiabatique intégré au caisson pré-refroidit l’air aspiré des groupes froids et aéroréfrigérants d’environ 6 à 9 K – eau perdue, sans buses, objectif < 25 Pa de perte de charge. Utilisateurs pilotes recherchés.",
           "kicker": "Nouveau · en essai · Module adiabatique",
           "h1": "Une protection acoustique qui rafraîchit – pré-refroidissement adiabatique dans le caisson",
           "lead": "Par forte chaleur, le module adiabatique pré-refroidit l’air aspiré des groupes froids d’environ 6 à 9 K. Moins de coupures haute pression, plus de puissance – et moins de bruit, car les ventilateurs peuvent tourner moins vite.",
           "b1": "Devenir utilisateur pilote", "b2": "La technique en détail",
           "mail": "mailto:info@forcotech.com?subject=Utilisateur%20pilote%20module%20adiabatique",
           "facts": [("6–9 K", "de refroidissement à 35 °C / 30 % HR"), ("< 25 Pa", "perte de charge supplémentaire (objectif)"),
                     ("Eau perdue", "sans recirculation ni buses"), ("A1", "HSA3, incombustible")]},
}

# Beschriftungen der Prinzipskizze
LBL = {
    "de": {"out": "Außenluft", "out2": "35 °C · 30 % r. F.", "mod": "Adiabatik-Modul", "water": "Wasser, enthärtet",
           "water2": "Systemtrenner EN 1717", "drain": "Ablauf · Einweg, ohne Umwälzung", "pre": "vorgekühlt",
           "pre2": "≈ 26–29 °C", "hood": "Schallhaube mit HSA3-Innenverkleidung", "coil": "Register",
           "unit": "Kaltwassersatz", "sil": "Abluft-Schalldämpfer", "exh": "Abluft",
           "key": "6–9 K Abkühlung · < 25 Pa zusätzlich (Zielwert)", "title": "Prinzipschnitt Schallhaube mit Adiabatik-Modul"},
    "en": {"out": "Outdoor air", "out2": "35 °C · 30 % RH", "mod": "Adiabatic module", "water": "Water, softened",
           "water2": "Backflow preventer EN 1717", "drain": "Drain · once-through, no recirculation", "pre": "pre-cooled",
           "pre2": "≈ 26–29 °C", "hood": "Acoustic enclosure with HSA3 lining", "coil": "Coil",
           "unit": "Chiller", "sil": "Exhaust silencer", "exh": "Exhaust air",
           "key": "6–9 K cooling · < 25 Pa additional (target)", "title": "Schematic section of an acoustic enclosure with adiabatic module"},
    "fr": {"out": "Air extérieur", "out2": "35 °C · 30 % HR", "mod": "Module adiabatique", "water": "Eau adoucie",
           "water2": "Disconnecteur EN 1717", "drain": "Évacuation · eau perdue, sans recirculation", "pre": "pré-refroidi",
           "pre2": "≈ 26–29 °C", "hood": "Caisson acoustique avec revêtement HSA3", "coil": "Batterie",
           "unit": "Groupe froid", "sil": "Silencieux d’air rejeté", "exh": "Air rejeté",
           "key": "6–9 K de refroidissement · < 25 Pa en plus (objectif)", "title": "Coupe de principe d’un caisson acoustique avec module adiabatique"},
}


def svg(lang):
    L = {k: bn.e(v) for k, v in LBL[lang].items()}
    ink, mut, red, blue, grey = "#1a1a1a", "#5c5c5c", "#c8202f", "#2f6f9f", "#d9d4d4"
    media = "".join(f'<path d="M{x} 168 l8 14 l-8 14 l8 14 l-8 14 l8 14 l-8 14 l8 14 l-8 14 l8 14 l-8 14 l8 14 l-8 14 l8 14" fill="none" stroke="{blue}" stroke-width="2"/>'
                    for x in range(140, 196, 12))
    lining = "".join(f'<line x1="{x}" y1="116" x2="{x}" y2="374" stroke="{red}" stroke-width="1.2" stroke-dasharray="3 4"/>' for x in (208, 672))
    fans = "".join(f'<ellipse cx="{cx}" cy="196" rx="38" ry="7" fill="#fff" stroke="{ink}" stroke-width="2"/>' for cx in (400, 480, 560))
    tubes = "".join(f'<circle cx="{cx}" cy="{cy}" r="9" fill="#fff" stroke="{red}" stroke-width="2"/>'
                    for i, cy in enumerate((58, 82)) for cx in range(352 + 14 * i, 620, 28))
    up = "".join(f'<path d="M{x} 36 V8" stroke="{mut}" stroke-width="2.5" marker-end="url(#a)"/>' for x in (400, 480, 560))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 420" font-family="system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif" role="img" aria-label="{L["title"]}">
<title>{L["title"]}</title>
<defs><marker id="a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="{mut}"/></marker>
<marker id="b" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 0 L10 5 L0 10z" fill="{blue}"/></marker></defs>
<rect width="800" height="420" fill="#fff"/>
<!-- Abluft-Schalldämpfer -->
<rect x="330" y="44" width="300" height="66" fill="#fdecee" stroke="{ink}" stroke-width="2"/>{tubes}
<text x="642" y="70" font-size="14" font-weight="700" fill="{ink}">{L["sil"]}</text>
{up}<text x="590" y="22" font-size="14" fill="{mut}">{L["exh"]}</text>
<!-- Haube -->
<rect x="200" y="110" width="480" height="270" fill="none" stroke="{ink}" stroke-width="3"/>{lining}
<text x="680" y="405" text-anchor="end" font-size="14.5" font-weight="700" fill="{ink}">{L["hood"]}</text>
<!-- Kaltwassersatz -->
<rect x="330" y="200" width="300" height="150" fill="#f3f1f1" stroke="{ink}" stroke-width="2"/>
<rect x="330" y="200" width="26" height="150" fill="url(#c)" stroke="{ink}" stroke-width="1.5"/>
<pattern id="c" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0 6 L6 0" stroke="{mut}" stroke-width="1.2"/></pattern>
<text x="343" y="368" text-anchor="middle" font-size="13" fill="{mut}">{L["coil"]}</text>
<text x="490" y="282" text-anchor="middle" font-size="18" font-weight="700" fill="{ink}">{L["unit"]}</text>
{fans}
<!-- Adiabatik-Modul -->
<rect x="132" y="160" width="68" height="210" fill="#eaf2f8" stroke="{blue}" stroke-width="2.5"/>{media}
<text x="178" y="150" text-anchor="end" font-size="14.5" font-weight="700" fill="{blue}">{L["mod"]}</text>
<path d="M188 66 V158" stroke="{blue}" stroke-width="3" marker-end="url(#b)"/>
<text x="20" y="72" font-size="13.5" font-weight="700" fill="{blue}">{L["water"]}</text>
<text x="20" y="90" font-size="12.5" fill="{mut}">{L["water2"]}</text>
<path d="M166 370 V392 H120" fill="none" stroke="{blue}" stroke-width="3" marker-end="url(#b)"/>
<text x="20" y="412" font-size="13" fill="{mut}">{L["drain"]}</text>
<!-- Luftweg -->
<path d="M20 262 H126" stroke="{mut}" stroke-width="4" marker-end="url(#a)"/>
<text x="20" y="236" font-size="14.5" font-weight="700" fill="{ink}">{L["out"]}</text>
<text x="20" y="290" font-size="13.5" fill="{red}" font-weight="700">{L["out2"]}</text>
<path d="M214 262 H322" stroke="{blue}" stroke-width="4" marker-end="url(#b)"/>
<text x="218" y="236" font-size="14" font-weight="700" fill="{blue}">{L["pre"]}</text>
<text x="218" y="290" font-size="13.5" font-weight="700" fill="{blue}">{L["pre2"]}</text>
<rect x="472" y="122" width="196" height="54" rx="8" fill="#fff" stroke="#e6e1e1"/>
<text x="570" y="145" text-anchor="middle" font-size="12.5" fill="{ink}">{L["key"].split(" · ")[0]}</text>
<text x="570" y="164" text-anchor="middle" font-size="12.5" fill="{mut}">{L["key"].split(" · ")[1]}</text>
</svg>
"""


def build():
    for lang in URL:
        (ROOT / SVG[lang]).parent.mkdir(parents=True, exist_ok=True)
        (ROOT / SVG[lang]).write_text(svg(lang), encoding="utf-8")
        t = TXT[lang]
        frag = (ROOT / "adiabatik" / "_src" / f"{lang}.html").read_text(encoding="utf-8")
        facts = "".join(f"<div><b>{bn.e(b)}</b><span>{bn.e(s)}</span></div>" for b, s in t["facts"])
        main = f"""<div class="hero">
  <div class="wrap hg">
    <div>
      <span class="kicker">{t["kicker"]}</span>
      <h1>{t["h1"]}</h1>
      <p class="lead">{t["lead"]}</p>
      <div class="btns"><a class="btn" href="{t["mail"]}">{t["b1"]}</a><a class="btn ghost" href="{TECH[lang]}">{t["b2"]}</a></div>
    </div>
    <div class="stats">{facts}</div>
  </div>
</div>
{frag}"""
        head = f'<script type="application/ld+json">{faq_ld(frag, lang)}</script>'
        bn.write(URL[lang][1:] + "index.html",
                 bn.page(lang, t["title"], t["desc"], dict(URL), main, extra_head=head))
    print("Adiabatik-Seiten gebaut (de, en, fr)")


if __name__ == "__main__":
    build()
