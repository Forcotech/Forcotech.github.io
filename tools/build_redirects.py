#!/usr/bin/env python3
"""Weiterleitungen für alte Adressen der früheren forcotech.com-Website (Webland/Designer).

Erzeugt für jede bekannte alte Adresse eine kleine Weiterleitungsseite an derselben Stelle
(z. B. /contact.html, /blog/<artikel>/) und eine 404-Seite, die unbekannte alte Adressen
per Muster auf die passende neue Seite schickt.

Neue alte Adresse gefunden (z. B. in der Google Search Console unter „Nicht gefunden (404)“)?
In OLD eintragen und ausführen:
    python3 tools/build_redirects.py
"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE = "https://www.forcotech.com"

# alte Adresse (ohne führenden Schrägstrich) -> neue Adresse (Pfad)
OLD = {
    "contact.html": "/en/#contact",
    "kontakt/": "/#kontakt",
    "en/contact/": "/en/#contact",
    "fr/contact/": "/fr/#contact",
    "about-us.html": "/en/#about",
    "schallschutzhauben.html": "/konfigurator/",
    "district-heat-pumps.html": "/konfigurator/en/grossanlagen/",
    "residential-equipment.html": "/konfigurator/en/",
    "soundproofing-for-solar-inverters.html": "/konfigurator/en/pv/",
    "blog.html": "/en/news/",
    "blog/schallhaube-fur-einen-ruckkuhler/": "/news/",
    "blog/cavity-to-improve-sound-absorption/": "/en/news/",
    "blog/noise-reduction-of-large-heat-pumps-and-large-refrigeration-systems/": "/en/news/",
    "blog/combination-of-iot-ai-and-anc-technology-for-effective-noise-reduction-in-large-heat-pumps-and-refrigeration-systems/": "/en/news/",
    "blog/hvac-equipment-noise-proffing-and-sensors/": "/en/news/",
}
# Muster für unbekannte alte Adressen (in der 404-Seite, Reihenfolge zählt)
PATTERNS = [
    ["^/blog", "/en/news/"],
    ["^/(store|shop|products?|produkte)", "/konfigurator/en/"],
    ["kontakt", "/#kontakt"],
    ["^/fr/.*contact", "/fr/#contact"],
    ["contact", "/en/#contact"],
    ["(about|ueber-uns|uber-uns)", "/en/#about"],
    ["(inverter|wechselrichter|solar|pv)", "/konfigurator/en/pv/"],
    ["(vrf|vrv)", "/konfigurator/en/vrf/"],
    ["(district|gross|large|chiller|kaltwasser)", "/konfigurator/en/grossanlagen/"],
    ["(schallhaube|enclosure|soundproof|noise)", "/konfigurator/en/"],
]


def stub(target):
    url = BASE + target
    u = html.escape(url, quote=True)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>ForCoTech – moved</title>
<meta name="robots" content="noindex,follow">
<link rel="canonical" href="{u}">
<meta http-equiv="refresh" content="0; url={u}">
<script>location.replace({json.dumps(url)});</script>
</head>
<body style="font:16px system-ui,sans-serif;padding:24px">
<p>This page has moved / Diese Seite ist umgezogen: <a href="{u}">{html.escape(url)}</a></p>
</body>
</html>
"""


PAGE404 = """<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Seite nicht gefunden – ForCoTech</title>
<meta name="robots" content="noindex">
<link rel="icon" href="/img/forcotech-logo.png">
<link rel="stylesheet" href="/style.css">
<script>
(function(){
  var MAP=__MAP__, PAT=__PAT__;
  var p=location.pathname.toLowerCase(), k=p.replace(/^\\/+/,"");
  var t=MAP[k]||MAP[k+"/"]||MAP[k.replace(/\\/$/,"")]||MAP[k.replace(/\\/$/,"")+".html"];
  if(!t){for(var i=0;i<PAT.length;i++){if(new RegExp(PAT[i][0]).test(p)){t=PAT[i][1];break;}}}
  if(t) location.replace(t);
})();
</script>
</head>
<body>
<main style="max-width:720px;margin:0 auto;padding:48px 16px;font:16px/1.6 system-ui,sans-serif">
<p><a href="/"><img src="/img/forcotech-logo.png" alt="ForCoTech" style="height:56px"></a></p>
<h1>Seite nicht gefunden · Page not found · Page introuvable</h1>
<p>Unsere Website ist umgezogen – viele alte Adressen gibt es nicht mehr. Hier geht es weiter:</p>
<ul>
<li><a href="/">Startseite (Deutsch)</a> · <a href="/en/">Home (English)</a> · <a href="/fr/">Accueil (Français)</a></li>
<li><a href="/konfigurator/">Schallhauben-Konfigurator</a> · <a href="/konfigurator/en/">Configurator (English)</a> · <a href="/konfigurator/fr/">Configurateur (Français)</a></li>
<li><a href="/news/">News</a> · <a href="/en/news/">News (English)</a></li>
<li>Kontakt / Contact: <a href="mailto:info@forcotech.com">info@forcotech.com</a></li>
</ul>
</main>
</body>
</html>
"""


def main():
    for old, target in OLD.items():
        f = ROOT / (old + "index.html" if old.endswith("/") else old)
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(stub(target), encoding="utf-8")
        print(f"{old:60s} -> {target}")
    (ROOT / "404.html").write_text(
        PAGE404.replace("__MAP__", json.dumps(OLD)).replace("__PAT__", json.dumps(PATTERNS)), encoding="utf-8")
    print("404.html")


if __name__ == "__main__":
    main()
