#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Baut die Seite Data-Center-Lösungen (/rechenzentren/, /en/data-centres/, /fr/centres-de-donnees/)
aus rechenzentren/_src/<sprache>.html.

Inhalt ändern: Fragment in rechenzentren/_src/de.html, en.html bzw. fr.html bearbeiten und
python3 tools/build_rechenzentren.py  ausführen.
Die FAQ-Daten (schema.org FAQPage) werden aus den <details>-Fragen im Fragment erzeugt.
Kopf, Navigation und Fuß kommen aus tools/build_news.py.

Die Zeichnungen img/rechenzentren/*.svg sind die deutschen Originale. Die englischen und französischen
Fassungen (*-en.svg, *-fr.svg) erzeugt dieses Skript daraus über die Tabelle SVG_TXT – wer eine
Beschriftung im deutschen SVG ändert, muss sie dort nachtragen (das Skript meldet fehlende Texte).
"""
import re
from pathlib import Path
import build_news as bn
from build_hserie import faq_ld

ROOT = Path(__file__).resolve().parent.parent
URL = {"de": "/rechenzentren/", "en": "/en/data-centres/", "fr": "/fr/centres-de-donnees/"}
TECH = {"de": "/technik/", "en": "/en/technology/", "fr": "/fr/technique/"}
IMG = "img/rechenzentren/acoustic-packs-rechenzentrum-v2.webp"
TXT = {
    "de": {"title": "Schallschutz für Rechenzentren – Acoustic Packs für Kaltwassersätze und Rückkühler | ForCoTech",
           "desc": "Freistehende Acoustic Packs für Chiller auf Rechenzentrumsdächern: Helmholtz-Röhrenschalldämpfer über den Ventilatoren, HSA3-Innenverkleidung A1, Druckverlust innerhalb der Gerätereserve, ca. 13 kg/m².",
           "kicker": "Data-Center-Lösungen · Acoustic Packs",
           "h1": "Schallschutz für Kalt&shy;wasser&shy;sätze auf dem Rechen&shy;zentrums&shy;dach – ultraleicht, A1, innerhalb der Druckreserve",
           "lead": "Freistehende Acoustic Packs für Chiller mit 20 und mehr Ventilatoren. Gebaut mit ABSORA-HSA3-Technologie: Metallakustik statt Mineralwolle, Helmholtz-Röhrenschalldämpfer direkt über den Ventilatoren.",
           "b1": "Projekt anfragen", "b2": "Technik im Detail",
           "mail": "mailto:info@forcotech.com?subject=Anfrage%20Acoustic%20Pack%20Rechenzentrum",
           "alt": "Acoustic Packs von ForCoTech: zwei freistehende Schallhauben aus Metallpaneelen mit Dachschalldämpfern über den Kaltwassersätzen eines Rechenzentrums – Visualisierung"},
    "en": {"title": "Noise control for data centres – acoustic packs for chillers and dry coolers | ForCoTech",
           "desc": "Free-standing acoustic packs for chillers on data-centre roofs: Helmholtz tube silencers above the fans, HSA3 inner lining A1, pressure drop within the unit reserve, approx. 13 kg/m².",
           "kicker": "Data centre solutions · Acoustic packs",
           "h1": "Noise control for chillers on the data&shy;centre roof – ultra-light, A1, within the pressure reserve",
           "lead": "Free-standing acoustic packs for chillers with 20 or more fans. Built with ABSORA HSA3 technology: metal acoustics instead of mineral wool, Helmholtz tube silencers directly above the fans.",
           "b1": "Request a project", "b2": "Technology in detail",
           "mail": "mailto:info@forcotech.com?subject=Enquiry%20acoustic%20pack%20data%20centre",
           "alt": "ForCoTech acoustic packs: two free-standing metal-panel enclosures with roof silencers over the chillers of a data centre – visualisation"},
    "fr": {"title": "Protection acoustique pour centres de données – acoustic packs pour groupes froids et aéroréfrigérants | ForCoTech",
           "desc": "Acoustic packs autoportants pour groupes froids en toiture de centres de données : silencieux tubulaires de Helmholtz au-dessus des ventilateurs, revêtement intérieur HSA3 A1, perte de charge dans la réserve de l’appareil, environ 13 kg/m².",
           "kicker": "Solutions pour centres de données · Acoustic packs",
           "h1": "Protection acoustique des groupes froids sur le toit des centres de données – ultra&shy;léger, A1, dans la réserve de pression",
           "lead": "Acoustic packs autoportants pour groupes froids de 20 ventilateurs et plus. Réalisés avec la technologie ABSORA HSA3&nbsp;: acoustique métallique au lieu de laine minérale, silencieux tubulaires de Helmholtz directement au-dessus des ventilateurs.",
           "b1": "Demander un projet", "b2": "La technique en détail",
           "mail": "mailto:info@forcotech.com?subject=Demande%20acoustic%20pack%20centre%20de%20donn%C3%A9es",
           "alt": "Acoustic packs ForCoTech : deux caissons autoportants en panneaux métalliques avec silencieux en toiture au-dessus des groupes froids d’un centre de données – visualisation"},
}

# Beschriftungen der Zeichnungen: deutscher Text -> (englisch, französisch)
SVG_TXT = {
    # abluft-schalldaempfer-modul.svg
    "HSA3-Helmholtz-Röhren Ø 200, 3 Reihen versetzt": ("HSA3 Helmholtz tubes Ø 200, 3 staggered rows", "Tubes de Helmholtz HSA3 Ø 200, 3 rangées en quinconce"),
    "Halbschalen an den Wänden": ("Half-shells on the walls", "Demi-coques sur les parois"),
    "Rahmen MiniTec 45×45": ("MiniTec 45×45 frame", "Châssis MiniTec 45×45"),
    "Axialventilatoren, Plenum 400 mm frei": ("Axial fans, 400 mm clear plenum", "Ventilateurs axiaux, plénum 400 mm"),
    "Trennebene zur Zuluft": ("Separation plane", "Plan de séparation"),
    "Röhrenquerschnitt": ("Tube cross-section", "Coupe d’un tube"),
    "HSA3 gewellt, mikroperforiert – A1": ("HSA3 corrugated, perforated – A1", "HSA3 ondulé, microperforé – A1"),
    "Resonanzkammern nach Helmholtz-": ("Helmholtz resonance chambers,", "Chambres de résonance Helmholtz,"),
    "Prinzip, abgestimmt auf 63–250 Hz": ("tuned to 63–250 Hz", "accordées sur 63–250 Hz"),
    "Runde Anströmkante: ζ ≈ 0,3 je Reihe": ("Round inlet edge: ζ ≈ 0.3 per row", "Bord arrondi : ζ ≈ 0,3 par rangée"),
    "Kein Faserdämmstoff": ("No fibrous insulation", "Sans isolant fibreux"),
    "ca. 1,6 kg/lfm – ultraleicht": ("approx. 1.6 kg/m – ultra-light", "env. 1,6 kg/m – ultraléger"),
    # acoustic-pack-isometrie.svg
    "Abluft-Schalldämpfer HSA3-Helmholtz, 3 Reihen": ("Exhaust silencer HSA3 Helmholtz, 3 rows", "Silencieux d’air rejeté HSA3 Helmholtz, 3 rangées"),
    "Trennebene / Kurzschlusssperre": ("Separation plane / anti-recirculation", "Plan de séparation / anti-recirculation"),
    "22 Axialventilatoren": ("22 axial fans", "22 ventilateurs axiaux"),
    "Zuluft-Schalldämpferfeld 12,0 × 2,2 m (beidseitig)": ("Supply-air silencer panel 12.0 × 2.2 m (both sides)", "Silencieux d’air neuf 12,0 × 2,2 m (des deux côtés)"),
    "Servicetüren": ("Service doors", "Portes de service"),
    "Kaltwassersatz XCAF1913+2V": ("Chiller XCAF1913+2V", "Groupe froid XCAF1913+2V"),
    "L = 15.075 mm": ("L = 15 075 mm", "L = 15 075 mm"),
    "B = 5.311": ("W = 5 311", "l = 5 311"),
    "H = 3.616": ("H = 3 616", "H = 3 616"),
    # acoustic-pack-querschnitt.svg
    "Gantry / Dach (bauseits)": ("Gantry / roof (by others)", "Structure porteuse / toiture (hors lot)"),
    "V-Register": ("V-coil", "Batterie en V"),
    "Verdichter / Hydraulik": ("Compressors / hydraulics", "Compresseurs / hydraulique"),
    "Abluft-Schalldämpfer HSA3-Helmholtz Ø 200 – 3 Reihen versetzt, Plenum 400": (
        "Exhaust silencer HSA3 Helmholtz Ø 200 – 3 staggered rows, plenum 400",
        "Silencieux d’air rejeté HSA3 Helmholtz Ø 200 – 3 rangées en quinconce, plénum 400"),
    "Trennebene": ("Separation plane", "Plan de séparation"),
    "Zuluft": ("Intake", "Air neuf"),
    "XCAF1913+2V": ("XCAF1913+2V", "XCAF1913+2V"),
}
SVGS = ("acoustic-pack-isometrie", "acoustic-pack-querschnitt", "abluft-schalldaempfer-modul")


def build_svgs():
    i = {"en": 0, "fr": 1}
    for name in SVGS:
        src = (ROOT / "img" / "rechenzentren" / f"{name}.svg").read_text(encoding="utf-8")
        for lang, k in i.items():
            def sub(m):
                text = m.group(2)
                if text.strip() in SVG_TXT:
                    return m.group(1) + text.replace(text.strip(), SVG_TXT[text.strip()][k]) + "<"
                if re.search(r"[^\d\s.,×]", text):  # Zahlen/Maße bleiben, alles andere muss übersetzt sein
                    print(f"  WARNUNG {name}.svg: keine Übersetzung für „{text.strip()}“")
                elif lang in ("en", "fr"):  # Tausenderpunkt in Maßen -> geschütztes Leerzeichen
                    return m.group(1) + re.sub(r"(\d)\.(\d{3})\b", "\\1\u00a0\\2", text) + "<"
                return m.group(0)
            out = re.sub(r"(>)([^<>]*[^\s<>][^<>]*)<", sub, src)
            (ROOT / "img" / "rechenzentren" / f"{name}-{lang}.svg").write_text(out, encoding="utf-8")


def build():
    build_svgs()
    for lang in URL:
        t = TXT[lang]
        frag = (ROOT / "rechenzentren" / "_src" / f"{lang}.html").read_text(encoding="utf-8")
        main = f"""<div class="hero">
  <div class="wrap hg">
    <div>
      <span class="kicker">{t["kicker"]}</span>
      <h1>{t["h1"]}</h1>
      <p class="lead">{t["lead"]}</p>
      <div class="btns"><a class="btn" href="{t["mail"]}">{t["b1"]}</a><a class="btn ghost" href="{TECH[lang]}">{t["b2"]}</a></div>
    </div>
    <figure class="dc-hero"><img src="/{IMG}" width="1500" height="695" alt="{t["alt"]}" fetchpriority="high"></figure>
  </div>
</div>
{frag}"""
        head = f'<script type="application/ld+json">{faq_ld(frag, lang)}</script>'
        bn.write(URL[lang][1:] + "index.html",
                 bn.page(lang, t["title"], t["desc"], dict(URL), main, og_image=IMG, extra_head=head))
    print("Rechenzentren-Seiten gebaut (de, en, fr)")


if __name__ == "__main__":
    build()
