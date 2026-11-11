#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Baut die Seite „Nachhaltigkeit mit HSA3“ (/nachhaltigkeit/, /en/sustainability/, /fr/durabilite/) aus nachhaltigkeit/_src/<sprache>.html.

Inhalt ändern: Fragment in nachhaltigkeit/_src/de.html, en.html bzw. fr.html bearbeiten und
python3 tools/build_nachhaltigkeit.py  ausführen, danach  python3 tools/build_news.py  (Sitemap).
Kopf (Titel, Beschreibung, Einleitung, Kennzahlen) steht in der Tabelle TXT.
Die FAQ-Daten (schema.org FAQPage) werden aus den <details>-Fragen im Fragment erzeugt.
Die französische Fassung verlinkt mangels FR-Lösungs- und HSA3-Seiten auf /fr/technique/.

Zahlen auf der Seite nur aus bereits veröffentlichten Werten (HSA3-Seite, Data-Center-Seite, Adiabatik-Seite);
das Energie-Rechenbeispiel ist als Schätzung mit Annahmen gekennzeichnet.
"""
from pathlib import Path
import build_news as bn
from build_hserie import faq_ld

ROOT = Path(__file__).resolve().parent.parent
URL = {"de": "/nachhaltigkeit/", "en": "/en/sustainability/", "fr": "/fr/durabilite/"}
HSA3 = {"de": "/hsa3/", "en": "/en/hsa3/", "fr": "/fr/technique/#hsa3"}
TXT = {
    "de": {"title": "Nachhaltigkeit mit HSA3 – Schallschutz für Wärmewende, Speicher und Rechenzentren | ForCoTech",
           "desc": "Wie das Meta-Akustik-Metall HSA3 nachhaltige Technik möglich macht: Wärmepumpen, R290-Anlagen, Batteriespeicher und Rechenzentren leise aufstellen, bis zu 40 % weniger Druckverlust, faserfrei, A1, sortenrein rückbaubar.",
           "kicker": "Nachhaltigkeit · HSA3",
           "h1": "Leise Technik für die Energie&shy;wende – HSA3 und Nachhaltigkeit",
           "lead": "Lärm ist eine der häufigsten Hürden für Wärmepumpen, Speicher und Kälteanlagen in dichter Bebauung. HSA3 löst sie mit einem Werkstoff, der selbst kreislauffähig ist und im Betrieb Energie spart.",
           "b1": "Projekt anfragen", "b2": "Mehr über HSA3",
           "facts": [("bis −40 %", "Druckverlust gegenüber Mineralwolle-Kulissen"), ("0 Fasern", "keine Mineralwolle, kein Schaum"),
                     ("A1", "nicht brennbar nach EN 13501-1"), ("sortenrein", "verschraubt, rückbaubar, Metallkreislauf")]},
    "en": {"title": "Sustainability with HSA3 – noise control for the heat transition, storage and data centres | ForCoTech",
           "desc": "How the meta-acoustic metal HSA3 enables sustainable technology: install heat pumps, R290 systems, battery storage and data centres quietly, up to 40 % lower pressure drop, fibre-free, A1, separable for recycling.",
           "kicker": "Sustainability · HSA3",
           "h1": "Quiet technology for the energy transition – HSA3 and sustainability",
           "lead": "Noise is one of the most common obstacles for heat pumps, storage systems and chillers in dense urban areas. HSA3 removes it with a material that is itself circular and saves energy in operation.",
           "b1": "Request a project", "b2": "More about HSA3",
           "facts": [("up to −40 %", "pressure drop vs. mineral-wool splitters"), ("0 fibres", "no mineral wool, no foam"),
                     ("A1", "non-combustible to EN 13501-1"), ("separable", "bolted, dismountable, back into the metal cycle")]},
    "fr": {"title": "Durabilité avec HSA3 – protection acoustique pour la transition thermique, le stockage et les centres de données | ForCoTech",
           "desc": "Comment le métal méta-acoustique HSA3 rend possible une technique durable : pompes à chaleur, installations R290, stockage par batteries et centres de données silencieux, jusqu’à 40 % de perte de charge en moins, sans fibres, A1, démontable par matériau.",
           "kicker": "Durabilité · HSA3",
           "h1": "Une technique silencieuse pour la transition énergétique – HSA3 et durabilité",
           "lead": "Le bruit est l’un des obstacles les plus fréquents pour les pompes à chaleur, les stockages et les groupes froids en milieu urbain dense. HSA3 le lève avec un matériau lui-même circulaire, qui économise de l’énergie en exploitation.",
           "b1": "Demander un projet", "b2": "En savoir plus sur HSA3",
           "facts": [("jusqu’à −40 %", "de perte de charge face aux baffles en laine minérale"), ("0 fibre", "ni laine minérale, ni mousse"),
                     ("A1", "incombustible selon EN 13501-1"), ("recyclable", "vissé, démontable, retour dans le cycle des métaux")]},
}


def build():
    for lang in URL:
        t = TXT[lang]
        frag = (ROOT / "nachhaltigkeit" / "_src" / f"{lang}.html").read_text(encoding="utf-8")
        facts = "".join(f"<div><b>{bn.e(b)}</b><span>{bn.e(s)}</span></div>" for b, s in t["facts"])
        main = f"""<div class="hero">
  <div class="wrap hg">
    <div>
      <span class="kicker">{t["kicker"]}</span>
      <h1>{t["h1"]}</h1>
      <p class="lead">{t["lead"]}</p>
      <div class="btns"><a class="btn" href="#anfrage">{t["b1"]}</a><a class="btn ghost" href="{HSA3[lang]}">{t["b2"]}</a></div>
    </div>
    <div class="stats">{facts}</div>
  </div>
</div>
{frag}"""
        head = f'<script type="application/ld+json">{faq_ld(frag, lang)}</script>'
        bn.write(URL[lang][1:] + "index.html",
                 bn.page(lang, t["title"], t["desc"], dict(URL), main, extra_head=head))
    print("Nachhaltigkeits-Seiten gebaut (de, en, fr)")


if __name__ == "__main__":
    build()
