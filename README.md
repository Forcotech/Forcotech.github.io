# www.forcotech.com

Firmenseite (Visitenkarte) von ForCoTech / Silent-Mode – Silent Engineering di Romolo Vicari, Osnago (LC), Italien.
Live (eigene Domain, seit 14.10.2026): https://www.forcotech.com/ – Repository forcotech.github.io mit CNAME-Datei.
Deutsch: https://www.forcotech.com/ · English: https://www.forcotech.com/en/ · Français: https://www.forcotech.com/fr/
Konfigurator: https://www.forcotech.com/konfigurator/

© Silent Engineering di Romolo Vicari. Alle Rechte vorbehalten. Texte, Bilder und Gestaltung dürfen ohne
schriftliche Genehmigung nicht vervielfältigt oder weiterverwendet werden.

## Alte Adressen der früheren forcotech.com-Website

Weiterleitungsseiten für bekannte alte Adressen (z. B. /contact.html, /blog/…) und die 404-Seite mit
Muster-Weiterleitungen erzeugt `python3 tools/build_redirects.py`. Neue alte Adressen (z. B. aus der Google
Search Console, „Nicht gefunden (404)“) dort in `OLD` eintragen und das Skript erneut ausführen.

## Startseite und Technik-Seite

Die Startseiten (index.html, en/index.html, fr/index.html) führen kurz durch Nutzen, Einsatzbereiche, Vorteile,
Beispiele und Ablauf. Die technischen Abschnitte (HSA3, Luftführung, Auslegung, Bauweise, R290) stehen auf eigenen
Seiten /technik/, /en/technology/, /fr/technique/: Inhalt in technik/_src/<sprache>.html bearbeiten, dann
`python3 tools/build_technik.py`. Navigation und Sitemap kommen aus tools/build_news.py.

## Produktseite H-Serie

/h-serie/ und /en/h-series/ (keine französische Fassung): Inhalt in hserie/_src/de.html bzw. en.html bearbeiten,
dann `python3 tools/build_hserie.py`. Die FAQ-Daten (FAQPage) werden aus den <details>-Fragen erzeugt.
Menüpunkt „H‑Serie“ in DE/EN steht in tools/build_news.py (nav) und auf den Startseiten index.html, en/index.html.
