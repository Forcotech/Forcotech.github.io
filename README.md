# www.forcotech.com

**Zuerst lesen:** `CLAUDE.md` (Arbeitsregeln). Vor jeder Veröffentlichung: `python3 tools/check.py`.

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

## Data-Center-Lösungen

/rechenzentren/, /en/data-centres/, /fr/centres-de-donnees/: Inhalt in rechenzentren/_src/de.html, en.html bzw. fr.html
bearbeiten, dann `python3 tools/build_rechenzentren.py`. Die englischen und französischen Zeichnungen
(img/rechenzentren/*-en.svg, *-fr.svg) erzeugt das Skript aus den deutschen SVGs über die Tabelle SVG_TXT.

## Adiabatik-Modul

/adiabatik/, /en/adiabatic-precooling/, /fr/pre-refroidissement-adiabatique/: Inhalt in adiabatik/_src/de.html, en.html bzw. fr.html
bearbeiten, dann `python3 tools/build_adiabatik.py`. Die Prinzipskizze img/adiabatik/*.svg erzeugt das Skript (Beschriftungen in LBL).
Karte auf den Startseiten index.html, en/index.html, fr/index.html; Sitemap-Eintrag in tools/build_news.py.

## Spezialthema Schallwand + Abluft-Schalldämpfer

/loesungen/schallwand-kulisse/, /en/solutions/noise-barrier-and-silencer/, /fr/ecran-et-silencieux/: Inhalt in
schallwand-kulisse/_src/de.html, en.html bzw. fr.html bearbeiten, dann `python3 tools/build_schallwand_kulisse.py`
(Zeichnungen img/schallwand-kulisse/*.svg aus der Tabelle LBL). Musterauslegung mit Werten aus dem Konfigurator
(Schallwand mit Option RK-200, Rechenstand 28.10.2026) – bei Änderungen am Rechenkern nachziehen. Link „Beispiel im
Konfigurator öffnen“ übergibt Gerät und L_WA (`?sd=1&L=…`). Karte auf den Startseiten, Hinweis auf der Seite Schallwände,
Sitemap-Eintrag in tools/build_news.py.

## Lösungsseiten und HSA3-Seite

Übersicht /loesungen/ (EN /en/solutions/), je eine Seite pro Anwendung – Wärmepumpen & Klimaanlagen, VRF/VRV,
Chiller & Groß-Wärmepumpen, Wechselrichter & BESS, Schallwände – jeweils direkt mit dem passenden Teil des
Konfigurators verlinkt, dazu /hsa3/ (EN /en/hsa3/) mit Aufbau, Wirkprinzip, Kennwerten und Vergleich. Keine FR-Fassung.

- Kopf (Titel, Beschreibung, Einleitung, Bild, Kennzahlen, Konfigurator-Link): Tabelle `PAGES` / `HSA3` in tools/build_loesungen.py
- Hauptteil: loesungen/_src/<id>.de.html / .en.html, Übersicht loesungen/_src/uebersicht.<sprache>.html, HSA3 hsa3/_src/<sprache>.html
- Zeichnungen img/loesungen/*.svg (DE und -en) erzeugt `python3 tools/svg_loesungen.py`

Abschnitt „Messwerte im Hallraum“ (#hallraum) auf der HSA3-Seite: Daten und Texte in tools/build_hallraum.py
(Prüfbericht BeSB/ABSORA 02/2026, Veröffentlichung mit ABSORA abgestimmt, PDF in downloads/), setzt den Block in
hsa3/_src/de.html und en.html ein – `python3 tools/build_hallraum.py`.

Danach `python3 tools/build_loesungen.py` und zuletzt `python3 tools/build_news.py` (Navigation, Sitemap).
Menüpunkte „Lösungen“ und „HSA3“ stehen in tools/build_news.py (nav) und auf den Startseiten index.html, en/index.html.

## Praxisleitfaden (PDF)

/leitfaden/ (nur Deutsch, handgeschriebene Seite) mit Download `downloads/forcotech-leitfaden-schallschutz-hvac.pdf`.
Das PDF ist die auf das ForCoTech-Layout (schwarz/rot, Logo, forcotech.com) umgestellte Fassung des Leitfadens
von Silent Engineering; Umstellskript liegt außerhalb des Repositorys.

## Startseite: Claim und Anfrageformular

Claim im Kopf („Ruhe für die Nachbarn. Leistung für die Anlage.“, mit Suchbegriff-Zeile im selben <h1>) und das
Anfrageformular im Kontaktbereich der Startseiten DE/EN/FR setzt `python3 tools/startseite_anfrage.py` (Texte im Skript,
wiederholbar). Versandlogik `anfrage.js` (FormSubmit, gleicher Zugang wie der Konfigurator, Empfänger info@forcotech.com;
bei Fehler Text zum Kopieren bzw. als E-Mail), Gestaltung am Ende von `style.css`.
Dasselbe Formular steht seit 23.10.2026 als Abschluss auf allen Unterseiten (Abschnitt `#anfrage`, aus `form_section()` in
`tools/startseite_anfrage.py`, eingebunden über `page()` in tools/build_news.py). Vorauswahl „Anlagentyp“: `page(..., typ="pv")`
setzt `data-anfrage-typ` am <body>; Knöpfe mit `href="#anfrage" data-typ="bess"` wählen beim Klick um.
Impressum und Datenschutzerklärung DE/EN/FR: Texte in tools/build_legal.py, dann `python3 tools/build_legal.py`
(seit 29.10.2026 mit dem Live-Stand abgeglichen, inkl. YouTube-Absatz).

## Prüfung vor dem Veröffentlichen

    python3 tools/check.py      # wenige Sekunden: Links, Bilder, Sitemap, Titel/Beschreibung, CNAME

Läuft bei jedem Push und Pull Request automatisch auf GitHub (`.github/workflows/pruefung.yml`); bei Fehlern
erscheint ein rotes ✗ und GitHub schickt eine E-Mail. Achtung: Diese Seite wird direkt aus `main` veröffentlicht –
die Prüfung warnt, hält eine fehlerhafte Fassung aber nicht auf. Deshalb nur über Zweig und Pull Request arbeiten.
