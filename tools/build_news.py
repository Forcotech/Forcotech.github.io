#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Baut den News-Bereich der Visitenkarte aus news/posts.json.

Neuer Beitrag:
  1. Bild nach img/news/<name>.webp legen
  2. Eintrag in news/posts.json ergänzen (slug, date, image, de/en/fr: title, alt, teaser);
     optional image_full + image_full_size [Breite, Höhe] für das große Bild auf der Beitragsseite;
     Grafiken mit Text: image / image_full / image_full_size auch je Sprache unter de/en möglich;
     bei Kopien von silent-mode.com "original": <URL> setzen
     (DE-Seite verweist per canonical auf das Original, EN bleibt eigenständig)
  3. Text als HTML-Fragment in news/_src/<slug>.de.html, .en.html und .fr.html
     (fehlt der fr-Block in posts.json, erscheint der Beitrag auf Französisch nicht)
  4. status auf "online" setzen und  python3 tools/build_news.py  ausführen

Erzeugt bzw. aktualisiert:
  - Vorschau der 3 neuesten Beiträge auf index.html, en/index.html und fr/index.html (zwischen NEWS-Markern)
  - Übersichten news/, en/news/ und fr/actualites/
  - Beitragsseiten news/<slug>/, en/news/<slug>/ und fr/actualites/<slug>/
  - sitemap.xml und den News-Abschnitt in llms.txt

Option --alle nimmt auch Entwürfe mit (nur für lokale Vorschau, nicht veröffentlichen).
"""
import html, json, re, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.forcotech.com"
ALLE = "--alle" in sys.argv

T = {
    "de": {
        "lang": "de", "home": "/", "news": "/news/", "other": "en",
        "h_pre": "News und", "h_acc": "Analysen",
        "sub": "Projekte, Messungen und Hintergründe aus der Auslegung unserer Schallhauben.",
        "all": "Alle Beiträge", "back": "Alle Beiträge", "skip": "Zum Inhalt",
        "nav": [("#leistungen", "Leistungen"), ("#hsa3", "HSA3"), ("#technik", "Technik"),
                ("/news/", "News"), ("#ueber-uns", "Über uns"), ("#kontakt", "Kontakt")],
        "cfg": ("https://www.forcotech.com/konfigurator/", "Konfigurator"),
        "nav_label": "Hauptnavigation", "home_label": "ForCoTech Startseite",
        "title_list": "News und Analysen – ForCoTech Schallhauben",
        "desc_list": "News und Analysen von ForCoTech: Projekte, Messungen und Hintergründe zu Schallhauben für Wärmepumpen, Kälteanlagen, VRF und PV-Wechselrichter.",
        "cta_h": "Projekt anfragen",
        "cta_p": "Schicken Sie uns Gerätetyp, Anzahl und Aufstellort – oder holen Sie sich direkt einen Richtpreis im Konfigurator.",
        "cta_b": "Zum Konfigurator", "privacy": "Datenschutz", "privacy_url": "/datenschutz/", "imprint": "Impressum", "imprint_url": "/impressum/", "other_name": "English",
        "empty": "Hier erscheinen in Kürze unsere ersten Beiträge.",
        "months": None, "locale": "de_DE", "zoom": "Grafik in voller Größe öffnen",
    },
    "en": {
        "lang": "en", "home": "/en/", "news": "/en/news/", "other": "de",
        "h_pre": "News and", "h_acc": "analyses",
        "sub": "Projects, measurements and background from the design of our acoustic enclosures.",
        "all": "All posts", "back": "All posts", "skip": "Skip to content",
        "nav": [("#services", "Applications"), ("#hsa3", "HSA3"), ("#technology", "Technology"),
                ("/en/news/", "News"), ("#about", "About us"), ("#contact", "Contact")],
        "cfg": ("https://www.forcotech.com/konfigurator/en/", "Configurator"),
        "nav_label": "Main navigation", "home_label": "ForCoTech home",
        "title_list": "News and analyses – ForCoTech acoustic enclosures",
        "desc_list": "News and analyses from ForCoTech: projects, measurements and background on acoustic enclosures for heat pumps, chillers, VRF and PV inverters.",
        "cta_h": "Request a project",
        "cta_p": "Send us the unit type, quantity and location – or get a budget price straight from the configurator.",
        "cta_b": "Open configurator", "privacy": "Privacy", "privacy_url": "/en/privacy/", "imprint": "Legal notice", "imprint_url": "/en/legal-notice/", "other_name": "Deutsch",
        "empty": "Our first posts will appear here shortly.",
        "months": None, "locale": "en_GB", "zoom": "Open graphic in full size",
    },
    "fr": {
        "lang": "fr", "home": "/fr/", "news": "/fr/actualites/", "other": "de",
        "h_pre": "Actualités et", "h_acc": "analyses",
        "sub": "Projets, mesures et contexte issus de la conception de nos caissons acoustiques.",
        "all": "Toutes les publications", "back": "Toutes les publications", "skip": "Aller au contenu",
        "nav": [("#applications", "Applications"), ("#hsa3", "HSA3"), ("#technologie", "Technologie"),
                ("/fr/actualites/", "Actualités"), ("#qui-sommes-nous", "Qui sommes-nous"), ("#contact", "Contact")],
        "cfg": ("https://www.forcotech.com/konfigurator/fr/", "Configurateur"),
        "nav_label": "Navigation principale", "home_label": "ForCoTech – accueil",
        "title_list": "Actualités et analyses – caissons acoustiques ForCoTech",
        "desc_list": "Actualités et analyses de ForCoTech : projets, mesures et contexte sur les caissons acoustiques pour pompes à chaleur, groupes froids, VRF et onduleurs PV.",
        "cta_h": "Demander un projet",
        "cta_p": "Envoyez-nous le type d’appareil, le nombre et le lieu d’implantation – ou obtenez directement un prix indicatif dans le configurateur.",
        "cta_b": "Ouvrir le configurateur", "privacy": "Confidentialité", "privacy_url": "/fr/confidentialite/", "imprint": "Mentions légales", "imprint_url": "/fr/mentions-legales/", "other_name": "Deutsch",
        "empty": "Nos premières publications apparaîtront ici prochainement.",
        "months": None, "locale": "fr_FR", "zoom": "Ouvrir le graphique en taille réelle",
    },
}
LANGS = ("de", "en", "fr")
LANG_NAME = {"de": "Deutsch", "en": "English", "fr": "Français"}
COUNTRY = {"de": ("Italien", "in Allianz mit"), "en": ("Italy", "in alliance with"), "fr": ("Italie", "en alliance avec")}
LOGO_ALT = "ForCoTech – Stop Noise · Enjoy Silence · Improve Efficiency – Engineered with Absora Technology"
FOOT = "© {y} Silent Engineering di Romolo Vicari · Via Trento 22 · 23875 Osnago (LC) · {it} · P.IVA IT03833150133 · {al} ABSORA GmbH, Berlin"

CTA = """<section>
  <div class="wrap">
    <div class="contact">
      <div>
        <h2>{L[cta_h]}</h2>
        <p>{L[cta_p]}</p>
        <div class="btns" style="margin-top:18px"><a class="btn" href="{L[cfg][0]}">{L[cta_b]}</a><a class="btn" href="mailto:info@forcotech.com">info@forcotech.com</a></div>
      </div>
      <address><b>Silent Engineering di Romolo Vicari</b><br>ForCoTech · Silent-Mode<br>Via Trento 22 · 23875 Osnago (LC) · {it}<br>{mail}: <a href="mailto:info@forcotech.com">info@forcotech.com</a></address>
    </div>
  </div>
</section>
"""

e = html.escape


def fmt(d):
    y, m, dd = d.split("-")
    return f"{dd}.{m}.{y}"


def url(lang, slug=None):
    base = T[lang]["news"]
    return base + (slug + "/" if slug else "")


def load():
    posts = json.loads((ROOT / "news/posts.json").read_text(encoding="utf-8"))
    posts = [p for p in posts if ALLE or p.get("status") == "online"]
    return sorted(posts, key=lambda p: p["date"], reverse=True)


def body(slug, lang):
    f = ROOT / f"news/_src/{slug}.{lang}.html"
    return f.read_text(encoding="utf-8").strip() if f.exists() else ""


def card(p, lang, h="h3", lazy=True):
    t = p[lang]
    teaser = ""  # Kurztext nur als Meta-Beschreibung, Karten zeigen wie im Vorbild Datum + Titel
    return (f'<article class="ncard"><a href="{url(lang, p["slug"])}">'
            f'<img src="/{t.get("image", p["image"])}" width="522" height="313" alt="{e(t["alt"])}"{' loading="lazy"' if lazy else ""}>'
            f'<time datetime="{p["date"]}">{fmt(p["date"])}</time>'
            f'<{h}>{e(t["title"])}</{h}>{teaser}</a></article>')


def teaser_section(posts, lang):
    L = T[lang]
    if not posts:
        return ""
    cards = "\n      ".join(card(p, lang) for p in posts[:3])
    more = f'<p class="nmore"><a href="{L["news"]}">{L["all"]} →</a></p>'
    return f"""<section id="news">
  <div class="wrap">
    <h2 class="nh">{L["h_pre"]} <span>{L["h_acc"]}</span></h2>
    <div class="ngrid">
      {cards}
    </div>
    {more}
  </div>
</section>"""


def page(lang, title, desc, alts, main, og_image=None, extra_head="", cta=True, canon_abs=None):
    """alts: {Sprache: Pfad} aller Fassungen dieser Seite, inkl. der eigenen."""
    L = T[lang]
    canon = alts[lang]
    others = [k for k in LANGS if k in alts and k != lang]
    hreflang = "\n".join(f'<link rel="alternate" hreflang="{k}" href="{SITE}{alts[k]}">' for k in LANGS if k in alts)
    switch = "\n      ".join(f'<a class="lang" href="{alts[k]}" lang="{k}" hreflang="{k}">{k.upper()}</a>' for k in others)
    foot_lang = " · ".join(f'<a href="{alts[k]}" lang="{k}">{LANG_NAME[k]}</a>' for k in others)
    nav = "\n      ".join(
        f'<a class="opt" href="{h if h.startswith("/") else L["home"] + h}">{n}</a>' for h, n in L["nav"])
    og = f'<meta property="og:image" content="{SITE}/{og_image}">' if og_image else ""
    it, al = COUNTRY[lang]
    cta_html = (CTA.format(L=L, it=it, mail="E-mail" if lang == "fr" else "E-Mail") if cta else "")
    return f"""<!doctype html>
<!-- © Silent Engineering di Romolo Vicari, Osnago (LC), Italien – Alle Rechte vorbehalten. -->
<!-- Automatisch erzeugt mit tools/build_news.py – Änderungen in news/posts.json bzw. news/_src/ vornehmen. -->
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<meta name="robots" content="index,follow,max-snippet:-1,max-image-preview:large">
<link rel="canonical" href="{canon_abs or SITE + canon}">
{hreflang}
<meta property="og:type" content="{'article' if og_image else 'website'}">
<meta property="og:site_name" content="ForCoTech">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}{canon}">
{og}
<meta property="og:locale" content="{L['locale']}">
<link rel="icon" href="/img/forcotech-logo.png">
<link rel="stylesheet" href="/style.css">
{extra_head}
</head>
<body>
<a class="skip" href="#main">{L["skip"]}</a>
<header class="top">
  <div class="wrap">
    <a class="logo" href="{L['home']}" aria-label="{L['home_label']}"><img src="/img/forcotech-logo.png" width="415" height="231" alt="{LOGO_ALT}"></a>
    <nav class="nav" aria-label="{L['nav_label']}">
      {nav}
      <a class="cta" href="{L['cfg'][0]}">{L['cfg'][1]}</a>
      {switch}
    </nav>
  </div>
</header>

<main id="main">
{main}
{cta_html}</main>

<footer>
  <div class="wrap">
    <span>{FOOT.format(y=date.today().year, it=it, al=al)}</span>
    <span><a href="{L['imprint_url']}">{L["imprint"]}</a> · <a href="{L['privacy_url']}">{L["privacy"]}</a> · {foot_lang}</span>
  </div>
</footer>
</body>
</html>
"""


def write(rel, text):
    f = ROOT / rel
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_text(text, encoding="utf-8")


def build():
    posts = load()
    for lang in LANGS:
        L = T[lang]
        lposts = [p for p in posts if lang in p]  # Beiträge ohne Übersetzung fehlen in dieser Sprache
        # Übersicht
        if lposts:
            grid = "\n      ".join(card(p, lang, "h2", lazy=i > 2) for i, p in enumerate(lposts))
            grid = f'<div class="ngrid">\n      {grid}\n    </div>'
        else:
            grid = f'<p class="sub">{L["empty"]}</p>'
        main = f"""<section class="nlist">
  <div class="wrap">
    <h1 class="nh">{L["h_pre"]} <span>{L["h_acc"]}</span></h1>
    <p class="sub">{L["sub"]}</p>
    {grid}
  </div>
</section>"""
        write(url(lang)[1:] + "index.html",
              page(lang, L["title_list"], L["desc_list"], {k: url(k) for k in LANGS}, main))

        # Beitragsseiten
        for p in lposts:
            t = p[lang]
            desc = t.get("teaser") or t["title"]
            ld = json.dumps({
                "@context": "https://schema.org", "@type": "BlogPosting", "headline": t["title"],
                "datePublished": p["date"], "dateModified": p.get("updated", p["date"]),
                "inLanguage": lang, "image": f"{SITE}/{t.get('image_full', p.get('image_full', t.get('image', p['image'])))}", "mainEntityOfPage": (p.get("original") if lang == "de" and p.get("original") else SITE + url(lang, p["slug"])),
                "author": {"@type": "Person", "name": "Romolo Vicari"},
                "publisher": {"@id": f"{SITE}/#org", "@type": "Organization", "name": "Silent Engineering di Romolo Vicari",
                              "logo": {"@type": "ImageObject", "url": f"{SITE}/img/forcotech-logo.png"}},
            }, ensure_ascii=False)
            content = body(p["slug"], lang)
            orig = p.get("original") if lang == "de" else None  # DE = Kopie des Originals, EN = eigene Übersetzung
            if p.get("original"):
                note = {"de": "Zuerst erschienen auf", "en": "Originally published in German on",
                        "fr": "Publié initialement en allemand sur"}[lang]
                content += f'\n<p class="norig">{note} <a href="{e(p["original"])}">silent-mode.com</a></p>'
            # optional: eigenes Bild in voller Größe für die Beitragsseite (image_full, image_full_size)
            # je Sprache überschreibbar: de/en.image, de/en.image_full, de/en.image_full_size (Grafiken mit Text)
            full = t.get("image_full", p.get("image_full", t.get("image", p["image"])))
            fw, fh = t.get("image_full_size", p.get("image_full_size", [522, 313]))
            main = f"""<article class="npost">
  <div class="wrap">
    <p class="nback"><a href="{url(lang)}">← {L["back"]}</a></p>
    <time datetime="{p["date"]}">{fmt(p["date"])}</time>
    <h1>{e(t["title"])}</h1>
    <figure><a href="/{full}" title="{L["zoom"]}"><img src="/{full}" width="{fw}" height="{fh}" alt="{e(t["alt"])}" fetchpriority="high"></a></figure>
    <div class="nbody">
{content}
    </div>
  </div>
</article>"""
            write(url(lang, p["slug"])[1:] + "index.html",
                  page(lang, f'{t["title"]} – ForCoTech', desc,
                       {k: url(k, p["slug"]) for k in LANGS if k in p}, main, og_image=t.get("image", p["image"]), canon_abs=orig,
                       extra_head=f'<script type="application/ld+json">{ld}</script>'))

        # Startseite
        home = ROOT / ("index.html" if lang == "de" else f"{lang}/index.html")
        s = home.read_text(encoding="utf-8")
        block = "<!-- NEWS:START (automatisch, tools/build_news.py) -->\n" + teaser_section(lposts, lang) + "\n<!-- NEWS:END -->"
        s, n = re.subn(r"<!-- NEWS:START.*?<!-- NEWS:END -->", block, s, flags=re.S)
        if n != 1:
            sys.exit(f"NEWS-Marker in {home} nicht gefunden")
        home.write_text(s, encoding="utf-8")

    # Sitemap: jede URL mit allen Sprachfassungen (hreflang)
    today = date.today().isoformat()
    def group(alts, lm, skip=()):
        out = []
        links = "".join(f'<xhtml:link rel="alternate" hreflang="{k}" href="{SITE}{v}"/>' for k, v in alts.items())
        for k, v in alts.items():
            if k not in skip:
                out.append(f'  <url><loc>{SITE}{v}</loc><lastmod>{lm}</lastmod>{links}</url>')
        return out
    lines = []
    lines += group({"de": "/", "en": "/en/", "fr": "/fr/"}, today)
    lines += group({k: url(k) for k in LANGS}, today)
    lines += group({"de": "/impressum/", "en": "/en/legal-notice/", "fr": "/fr/mentions-legales/"}, today)
    lines += group({"de": "/datenschutz/", "en": "/en/privacy/", "fr": "/fr/confidentialite/"}, today)
    for p in posts:
        # DE-Kopien von silent-mode.com verweisen per canonical auf das Original -> nicht in die Sitemap
        lines += group({k: url(k, p["slug"]) for k in LANGS if k in p}, p.get("updated", p["date"]),
                       skip=("de",) if p.get("original") else ())
    write("sitemap.xml", '<?xml version="1.0" encoding="UTF-8"?>\n'
          '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n'
          + "\n".join(lines) + "\n</urlset>\n")

    # llms.txt
    f = ROOT / "llms.txt"
    s = f.read_text(encoding="utf-8")
    items = "\n".join(f'- [{p["en"]["title"]}]({SITE}{url("en", p["slug"])}) ({p["date"]}, Deutsch: {SITE}{url("de", p["slug"])})' for p in posts)
    block = f"<!-- NEWS:START -->\n## News and analyses\n- [News (Deutsch)]({SITE}/news/) · [News (English)]({SITE}/en/news/) · [Actualités (Français)]({SITE}/fr/actualites/)\n{items}\n<!-- NEWS:END -->"
    if "<!-- NEWS:START -->" in s:
        s = re.sub(r"<!-- NEWS:START -->.*?<!-- NEWS:END -->", block, s, flags=re.S)
    else:
        s = s.rstrip() + "\n\n" + block + "\n"
    f.write_text(s, encoding="utf-8")
    print(f"{len(posts)} Beitrag/Beiträge gebaut" + (" (inkl. Entwürfe)" if ALLE else ""))


if __name__ == "__main__":
    build()
