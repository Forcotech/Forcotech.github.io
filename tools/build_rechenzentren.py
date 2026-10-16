#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Baut die Seite Data-Center-Lösungen (/rechenzentren/) aus rechenzentren/_src/de.html.

Inhalt ändern: Fragment in rechenzentren/_src/de.html bearbeiten und  python3 tools/build_rechenzentren.py  ausführen.
Die FAQ-Daten (schema.org FAQPage) werden aus den <details>-Fragen im Fragment erzeugt.
Kopf, Navigation und Fuß kommen aus tools/build_news.py. Bisher nur deutsche Fassung.
"""
from pathlib import Path
import build_news as bn
from build_hserie import faq_ld

ROOT = Path(__file__).resolve().parent.parent
URL = {"de": "/rechenzentren/"}
TXT = {
    "de": {"title": "Schallschutz für Rechenzentren – Acoustic Packs für Kaltwassersätze und Rückkühler | ForCoTech",
           "desc": "Freistehende Acoustic Packs für Chiller auf Rechenzentrumsdächern: Helmholtz-Röhrenschalldämpfer über den Ventilatoren, HSA3-Innenverkleidung A1, Druckverlust innerhalb der Gerätereserve, ca. 13 kg/m².",
           "kicker": "Data-Center-Lösungen · Acoustic Packs",
           "h1": "Schallschutz für Kalt&shy;wasser&shy;sätze auf dem Rechen&shy;zentrums&shy;dach – ultraleicht, A1, innerhalb der Druckreserve",
           "lead": "Freistehende Acoustic Packs für Chiller mit 20 und mehr Ventilatoren. Gebaut mit ABSORA-HSA3-Technologie: Metallakustik statt Mineralwolle, Helmholtz-Röhrenschalldämpfer direkt über den Ventilatoren.",
           "b1": "Projekt anfragen", "b2": "Technik im Detail",
           "mail": "mailto:info@forcotech.com?subject=Anfrage%20Acoustic%20Pack%20Rechenzentrum",
           "img": "img/rechenzentren/acoustic-packs-rechenzentrum.webp",
           "alt": "Acoustic Packs von ForCoTech: Rückkühler mit aufgesetztem Abluftschalldämpfer (1) und eingehauste Kälteanlagen und Container mit Dachschalldämpfern (2) – Visualisierung"},
}


def build():
    for lang in URL:
        t = TXT[lang]
        frag = (ROOT / "rechenzentren" / "_src" / f"{lang}.html").read_text(encoding="utf-8")
        main = f"""<div class="hero">
  <div class="wrap hg">
    <div>
      <span class="kicker">{t["kicker"]}</span>
      <h1>{t["h1"]}</h1>
      <p class="lead">{t["lead"]}</p>
      <div class="btns"><a class="btn" href="{t["mail"]}">{t["b1"]}</a><a class="btn ghost" href="/technik/">{t["b2"]}</a></div>
    </div>
    <figure class="dc-hero"><img src="/{t["img"]}" width="718" height="615" alt="{t["alt"]}" fetchpriority="high"></figure>
  </div>
</div>
{frag}"""
        head = f'<script type="application/ld+json">{faq_ld(frag, lang)}</script>'
        bn.write(URL[lang][1:] + "index.html",
                 bn.page(lang, t["title"], t["desc"], dict(URL), main, og_image=t["img"], extra_head=head))
    print("Rechenzentren-Seite gebaut")


if __name__ == "__main__":
    build()
