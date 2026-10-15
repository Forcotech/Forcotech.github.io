#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Baut die Produktseite der H-Serie (/h-serie/, /en/h-series/) aus hserie/_src/<sprache>.html.

Inhalt ändern: Fragment in hserie/_src/de.html bzw. en.html bearbeiten und  python3 tools/build_hserie.py  ausführen.
Die FAQ-Daten (schema.org FAQPage) werden aus den <details>-Fragen im Fragment erzeugt.
Kopf, Navigation und Fuß kommen aus tools/build_news.py. Eine französische Fassung gibt es nicht.
"""
import html, json, re
from pathlib import Path
import build_news as bn

ROOT = Path(__file__).resolve().parent.parent
URL = {"de": "/h-serie/", "en": "/en/h-series/"}
CFG = {"de": "https://www.forcotech.com/konfigurator/h-serie/", "en": "https://www.forcotech.com/konfigurator/en/h-serie/"}
TXT = {
    "de": {"title": "SilentMode H-Serie – Schallhauben für Wärmepumpen am Haus, Standard und nach Maß | ForCoTech",
           "desc": "Schallschutzhauben H1–H12 für Wärmepumpen und Klimageräte im Ein- und Mehrfamilienhaus: −10, −18 oder −25 dB(A), max. 4 m/s, R290-tauglich, Alu in RAL nach Wahl – auch als Maßanfertigung. Richtpreis im Konfigurator.",
           "kicker": "Kleinanlagen · SilentMode H-Serie",
           "h1": "Schallhauben für Wärmepumpen am Haus – Standard H1–H12 und nach Maß",
           "lead": "Für Wärmepumpen und Klimageräte im Ein- und Mehrfamilienhaus. Bis zu −25 dB(A) leiser, ohne die Anlage auszubremsen – für Hausbesitzer, Verwalter und Anlagenbauer.",
           "b1": "Haube konfigurieren – mit Richtpreis", "b2": "Maßanfertigung anfragen",
           "mail": "mailto:info@forcotech.com?subject=Ma%C3%9Fanfertigung%20Schallhaube"},
    "en": {"title": "SilentMode H-Series – acoustic enclosures for heat pumps at homes, standard and custom-made | ForCoTech",
           "desc": "Acoustic enclosures H1–H12 for heat pumps and air-conditioning units at single and multi-family homes: −10, −18 or −25 dB(A), max. 4 m/s, R290-ready, aluminium in any RAL colour – also custom-made. Guide price in the configurator.",
           "kicker": "Small units · SilentMode H-Series",
           "h1": "Acoustic enclosures for heat pumps at home – standard H1–H12 and custom-made",
           "lead": "For heat pumps and air-conditioning units at single and multi-family homes. Up to −25 dB(A) quieter without holding the unit back – for homeowners, property managers and installers.",
           "b1": "Configure an enclosure – with guide price", "b2": "Request a custom enclosure",
           "mail": "mailto:info@forcotech.com?subject=Custom-made%20acoustic%20enclosure"},
}


def faq_ld(frag, lang):
    qa = re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", frag, re.S)
    strip = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang,
                       "mainEntity": [{"@type": "Question", "name": strip(q),
                                       "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qa]},
                      ensure_ascii=False)


def build():
    for lang in URL:
        t = TXT[lang]
        frag = (ROOT / "hserie" / "_src" / f"{lang}.html").read_text(encoding="utf-8")
        main = f"""<section class="nlist">
  <div class="wrap">
    <span class="kicker">{t["kicker"]}</span>
    <h1 class="nh">{t["h1"]}</h1>
    <p class="sub">{t["lead"]}</p>
    <div class="btns" style="margin-top:18px"><a class="btn" href="{CFG[lang]}">{t["b1"]}</a><a class="btn ghost" href="{t["mail"]}">{t["b2"]}</a></div>
  </div>
</section>
{frag}"""
        head = f'<script type="application/ld+json">{faq_ld(frag, lang)}</script>'
        bn.write(URL[lang][1:] + "index.html",
                 bn.page(lang, t["title"], t["desc"], dict(URL), main, extra_head=head))
    print("H-Serie-Seiten gebaut")


if __name__ == "__main__":
    build()
