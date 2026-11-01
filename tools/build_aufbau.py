#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Baut die Rubrik „Projekte im Aufbau“ (/projekte-im-aufbau/, /en/projects-in-progress/, /fr/projets-en-cours/)
und den Kurzblock auf den Startseiten (zwischen <!-- AUFBAU:START --> und <!-- AUFBAU:END -->).

Neues Projekt oder neuer Stand:
  1. Fotos neutral zuschneiden (keine Kundennamen, keine Standorte, keine erkennbaren Gebäude oder Wahrzeichen),
     als WebP (max. 1000 px breit) nach img/aufbau/ legen.
  2. Eintrag oben in tools/aufbau.json einfügen bzw. Status/Text ändern (DE, EN, FR).
  3. python3 tools/build_aufbau.py && python3 tools/build_news.py && python3 tools/check.py

Kopf, Navigation, Anfrageformular und Fuß kommen aus tools/build_news.py.
"""
import json, re, sys
from pathlib import Path
import build_news as bn

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "tools" / "aufbau.json"
URL = {"de": "/projekte-im-aufbau/", "en": "/en/projects-in-progress/", "fr": "/fr/projets-en-cours/"}
HOME = {"de": "index.html", "en": "en/index.html", "fr": "fr/index.html"}
EX = {"de": "/#beispiele", "en": "/en/#examples", "fr": "/fr/#exemples"}
MON = {
    "de": "Januar Februar März April Mai Juni Juli August September Oktober November Dezember".split(),
    "en": "January February March April May June July August September October November December".split(),
    "fr": "janvier février mars avril mai juin juillet août septembre octobre novembre décembre".split(),
}
TXT = {
    "de": {"title": "Projekte im Aufbau – Schallhauben in Fertigung und Montage | ForCoTech",
           "desc": "Aktuelle Schallhauben-Projekte von ForCoTech im Aufbau: Momentaufnahmen aus Fertigung und Montage – Profilrahmen, Paneele, HSA3-Schalldämpfer. Ohne Kundennamen und Standorte.",
           "kicker": "Aus Fertigung und Montage", "h1": "Projekte im Aufbau",
           "lead": "Momentaufnahmen von Anlagen, die gerade entstehen – vom Tragrahmen bis zur fertigen Haube. Wir aktualisieren diese Seite laufend.",
           "note": "Ohne Kundennamen und Standorte: Die Anlagen gehören nach der Lieferung unseren Kunden. Fertige Anlagen zeigen wir unter <a href=\"{ex}\">Ausführungsbeispiele</a>.",
           "stand": "Stand:", "done": "Abgeschlossen", "running": "Im Aufbau",
           "teaser_h": "Gerade im Aufbau", "teaser_more": "Alle Projekte im Aufbau →",
           "b1": "Projekt anfragen", "b2": "Zum Konfigurator", "zoom": "Foto in voller Größe öffnen"},
    "en": {"title": "Projects in progress – acoustic enclosures in fabrication and installation | ForCoTech",
           "desc": "Current ForCoTech acoustic enclosure projects in progress: snapshots from fabrication and installation – profile frames, panels, HSA3 silencers. No customer names or locations.",
           "kicker": "From fabrication and installation", "h1": "Projects in progress",
           "lead": "Snapshots of installations as they take shape – from the support frame to the finished enclosure. We update this page regularly.",
           "note": "No customer names or locations: after delivery the installations belong to our customers. Finished installations are shown under <a href=\"{ex}\">Examples</a>.",
           "stand": "Updated:", "done": "Completed", "running": "In progress",
           "teaser_h": "Currently in progress", "teaser_more": "All projects in progress →",
           "b1": "Request a project", "b2": "Open configurator", "zoom": "Open photo in full size"},
    "fr": {"title": "Projets en cours – caissons acoustiques en fabrication et en montage | ForCoTech",
           "desc": "Projets de caissons acoustiques ForCoTech en cours : instantanés de fabrication et de montage – châssis profilés, panneaux, silencieux HSA3. Sans noms de clients ni lieux.",
           "kicker": "Fabrication et montage", "h1": "Projets en cours",
           "lead": "Instantanés d’installations en train de prendre forme – du châssis au caisson terminé. Nous mettons cette page à jour régulièrement.",
           "note": "Sans noms de clients ni lieux : après la livraison, les installations appartiennent à nos clients. Les installations terminées figurent sous <a href=\"{ex}\">Exemples</a>.",
           "stand": "Mise à jour :", "done": "Terminé", "running": "En cours",
           "teaser_h": "Actuellement en cours", "teaser_more": "Tous les projets en cours →",
           "b1": "Demander un projet", "b2": "Ouvrir le configurateur", "zoom": "Ouvrir la photo en taille réelle"},
}
e = bn.e


def datum(d, lang):
    """2026-11-08 -> „8. November 2026“ / „8 November 2026“ / „8 novembre 2026“"""
    y, mm, dd = d.split("-")
    name = MON[lang][int(mm) - 1]
    return f"{int(dd)}. {name} {y}" if lang == "de" else f"{int(dd)} {name} {y}"


def img_tag(b, lang, lazy=True):
    from PIL import Image
    f = ROOT / "img" / "aufbau" / b["datei"]
    if not f.exists():
        sys.exit(f"Bild fehlt: {f}")
    w, h = Image.open(f).size
    return (f'<img src="/img/aufbau/{b["datei"]}" width="{w}" height="{h}" alt="{e(b[lang])}"'
            + (' loading="lazy"' if lazy else "") + ">")


def daten(t):
    """Optionale Kenndaten je Haube: t["daten"] = [{"titel": ..., "werte": [[Bezeichnung, Wert], ...]}]."""
    if not t.get("daten"):
        return ""
    boxes = "".join(
        f'<div class="ab-spec"><h3>{e(d["titel"])}</h3><dl>'
        + "".join(f"<dt>{e(k)}</dt><dd>{e(v)}</dd>" for k, v in d["werte"])
        + "</dl></div>"
        for d in t["daten"])
    return f'<div class="ab-specs">{boxes}</div>\n    '


def card(p, lang, first):
    t, T = p[lang], TXT[lang]
    chip = f'<span class="ab-chip{" ab-done" if p.get("fertig") else ""}">{T["done"] if p.get("fertig") else T["running"]}</span>'
    figs = "\n      ".join(
        f'<figure{" class=\"ab-wide\"" if b.get("breit") else ""}><a href="/img/aufbau/{b["datei"]}" title="{T["zoom"]}">'
        f'{img_tag(b, lang, lazy=not (first and i == 0))}</a></figure>'
        for i, b in enumerate(p["bilder"]))
    return f"""  <article class="ab-card" id="{p['id']}">
    <div class="ab-head">{chip}<time datetime="{p['datum']}">{T['stand']} {datum(p['datum'], lang)}</time></div>
    <h2>{e(t['titel'])}</h2>
    <p class="ab-status">{e(t['status'])}</p>
    <p>{e(t['text'])}</p>
    {daten(t)}<div class="ab-photos">
      {figs}
    </div>
  </article>"""


def teaser(projekte, lang):
    T = TXT[lang]
    laufend = [p for p in projekte if not p.get("fertig")] or projekte
    if not laufend:
        return ""
    # je Projekt ein Foto (bevorzugt kein Panorama), höchstens drei Projekte
    bilder = [(p, next((b for b in p["bilder"] if not b.get("breit")), p["bilder"][0])) for p in laufend if p["bilder"]][:3]
    figs = "\n      ".join(
        f'<figure><a href="{URL[lang]}#{p["id"]}">{img_tag(b, lang)}</a><figcaption>{e(p[lang]["titel"])} – {e(p[lang]["status"])}</figcaption></figure>'
        for p, b in bilder)
    return f"""<section class="alt" id="aufbau">
  <div class="wrap">
    <h2>{T['teaser_h']}</h2>
    <div class="gallery ab-teaser">
      {figs}
    </div>
    <p class="nmore"><a href="{URL[lang]}">{T['teaser_more']}</a></p>
  </div>
</section>"""


def build():
    data = json.loads(DATA.read_text(encoding="utf-8"))
    projekte = data["projekte"]
    stand = max((p["datum"] for p in projekte), default=None)
    for lang in URL:
        T = TXT[lang]
        cards = "\n".join(card(p, lang, i == 0) for i, p in enumerate(projekte))
        main = f"""<div class="hero">
  <div class="wrap">
    <span class="kicker">{T['kicker']}</span>
    <h1>{T['h1']}</h1>
    <p class="lead">{T['lead']}</p>
    <div class="btns"><a class="btn" href="#anfrage">{T['b1']}</a><a class="btn ghost" href="{bn.T[lang]['cfg'][0]}">{T['b2']}</a></div>
  </div>
</div>
<section>
  <div class="wrap ab-list">
{cards}
    <p class="note">{T['note'].format(ex=EX[lang])}{f" · {T['stand']} {datum(stand, lang)}" if stand else ""}</p>
  </div>
</section>"""
        og = f"img/aufbau/{projekte[0]['bilder'][0]['datei']}" if projekte else None
        bn.write(URL[lang][1:] + "index.html", bn.page(lang, T["title"], T["desc"], dict(URL), main, og_image=og))

        home = ROOT / HOME[lang]
        s = home.read_text(encoding="utf-8")
        block = "<!-- AUFBAU:START (automatisch, tools/build_aufbau.py) -->\n" + teaser(projekte, lang) + "\n<!-- AUFBAU:END -->"
        s, n = re.subn(r"<!-- AUFBAU:START.*?<!-- AUFBAU:END -->", block, s, flags=re.S)
        if n != 1:
            sys.exit(f"AUFBAU-Marker in {home} nicht gefunden")
        home.write_text(s, encoding="utf-8")
    print(f"Projekte im Aufbau gebaut: {len(projekte)} Projekt(e), de/en/fr")


if __name__ == "__main__":
    build()
