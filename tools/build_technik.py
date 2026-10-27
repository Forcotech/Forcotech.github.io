#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Baut die Technik-Seiten (/technik/, /en/technology/, /fr/technique/) aus technik/_src/<sprache>.html.

Inhalt ändern: Fragment in technik/_src/de.html, en.html bzw. fr.html bearbeiten (HSA3, Luftführung,
Technik und Auslegung, Bauweise, R290, Nachhaltigkeit), Fragen als strukturierte Daten in technik/_src/<sprache>.faq.json und  python3 tools/build_technik.py  ausführen.
Kopf, Navigation und Fuß kommen aus tools/build_news.py.
"""
from pathlib import Path
import build_news as bn

ROOT = Path(__file__).resolve().parent.parent
URL = {"de": "/technik/", "en": "/en/technology/", "fr": "/fr/technique/"}
TXT = {
    "de": {"title": "Technik – HSA3, Luftführung und Bauweise der Schallhauben | ForCoTech",
           "desc": "Wie ForCoTech Schallhauben auslegt: Meta-Akustik-Metall HSA3, Luftführung und Druckverlust, CFD-Simulation und TA Lärm, Bauweise, Ausführung für R290 sowie Nachhaltigkeit und Beitrag zu LEED, BREEAM und DGNB.",
           "h1": "Technik im Detail",
           "lead": "Für Planer und Anlagenbauer: wie wir Akustik, Strömung und Bauweise auslegen – und warum die Luftführung über die Wirkung einer Haube entscheidet."},
    "en": {"title": "Technology – HSA3, air flow and construction of the enclosures | ForCoTech",
           "desc": "How ForCoTech engineers acoustic enclosures: HSA3 acoustic meta-metal, air flow and pressure drop, CFD simulation, construction, R290 versions, sustainability and contribution to LEED, BREEAM and DGNB.",
           "h1": "Technology in detail",
           "lead": "For designers and installers: how we engineer acoustics, air flow and construction – and why air flow decides whether an enclosure works."},
    "fr": {"title": "Technique – HSA3, flux d’air et construction des caissons | ForCoTech",
           "desc": "Comment ForCoTech conçoit ses caissons acoustiques : méta-métal acoustique HSA3, flux d’air et perte de charge, simulation CFD, construction, exécution pour le R290, durabilité et contribution à LEED, BREEAM et DGNB.",
           "h1": "La technique en détail",
           "lead": "Pour les bureaux d’études et installateurs : comment nous concevons acoustique, flux d’air et construction – et pourquoi le flux d’air décide de l’efficacité d’un caisson."},
}


def build():
    for lang in bn.LANGS:
        t = TXT[lang]
        frag = (ROOT / "technik" / "_src" / f"{lang}.html").read_text(encoding="utf-8")
        main = f"""<section class="nlist">
  <div class="wrap">
    <h1 class="nh">{t["h1"]}</h1>
    <p class="sub">{t["lead"]}</p>
  </div>
</section>
{frag}"""
        faq = ROOT / "technik" / "_src" / f"{lang}.faq.json"  # strukturierte Daten zu den Fragen auf der Seite
        head = f'<script type="application/ld+json">{faq.read_text(encoding="utf-8")}</script>' if faq.exists() else ""
        bn.write(URL[lang][1:] + "index.html", bn.page(lang, t["title"], t["desc"], dict(URL), main, extra_head=head))
    print("Technik-Seiten gebaut")


if __name__ == "__main__":
    build()
