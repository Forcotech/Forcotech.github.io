# www.forcotech.com – Arbeitsregeln

Pflichtlektüre zu Beginn jeder Arbeit an der Firmenseite (für Claude und für jeden Menschen, der hier arbeitet).
Die Beschreibung der einzelnen Seiten und Build-Skripte steht im `README.md`.

**Dieses Repository ist öffentlich.** Hier stehen keine internen Informationen: keine Zugangsdaten, keine Konten,
keine Vertrags- oder Kundeninformationen. Die interne Dokumentation (Entscheidungen, Änderungsprotokoll, Betrieb,
Konten, Notfälle) liegt im privaten Repository `Forcotech/konfigurator` im Ordner `intern/`
(`intern/FIRMENSEITE.md` und `intern/BETRIEB.md`).

## Was das ist

Statische Firmenseite von ForCoTech (Silent Engineering di Romolo Vicari, Osnago; Fertigung und Montage mit
ABSORA GmbH, Berlin) auf GitHub Pages unter www.forcotech.com, Deutsch, `en/` Englisch, `fr/` Französisch.
Der Konfigurator unter `/konfigurator/` ist ein eigenes Repository.

## Feste Regeln

- **Veröffentlicht wird über GitHub Actions** (`.github/workflows/veroeffentlichen.yml`): Jeder Push auf `main` geht
  nach bestandener Prüfung live; schlägt sie fehl, bleibt der letzte gute Stand online. Trotzdem immer auf einem
  eigenen Zweig arbeiten und über einen Pull Request zusammenführen. Nicht ausgeliefert werden `tools/`, alle `_src/`,
  `README.md` und diese Datei.
- **`CNAME` nie löschen oder ändern** – sonst ist die Domain www.forcotech.com weg.
- **Seiten mit `_src/` nur dort bearbeiten**, dann das zugehörige Build-Skript ausführen (siehe README). Die erzeugten
  `index.html` nicht von Hand ändern, sonst überschreibt der nächste Build die Änderung.
- **Keine Kundennamen und keine Projektstandorte** in Texten, Bildern, Dateinamen oder Bildunterschriften.
  Referenzen nur neutral („500+ Projekte“, „Muster-Rechenzentrum“).
- **Messwerte und Prüfberichte nur nach Freigabe** veröffentlichen; Werte ohne Prüfbericht als Schätzung kennzeichnen.
- **Keine Preise außer veröffentlichten Listenpreisen**; individuelle Lösungen „Preis mit dem Angebot“.
- **B2B:** Ansprache von Planern, Anlagenbauern, Fachbetrieben und Betreibern – nicht von Privatkunden.
- **Datenschutz:** Kommt ein neuer Dienst hinzu (Video, Karte, Schrift, Formular), Datenschutzerklärung in
  `tools/build_legal.py` ergänzen und ausführen. Keine Cookies, kein Tracking.
- **Gestaltung:** ForCoTech-Rot als Akzent, Schrift Schwarz, Logo `img/forcotech-logo.png`; DE/EN/FR gleichwertig.

## Ablauf einer Änderung

1. Eigenen Zweig anlegen.
2. Quelle bearbeiten (`_src/` oder Tabelle im Build-Skript), Build-Skript ausführen, zuletzt `python3 tools/build_news.py`
   (Navigation, Sitemap).
3. `python3 tools/check.py` – muss „OK – keine Fehler.“ melden.
4. Eintrag im Änderungsprotokoll `intern/FIRMENSEITE.md` (privates Repository `Forcotech/konfigurator`).
5. Pull Request; automatische Prüfung grün → zusammenführen.

## Berichten

Ergebnisse in klarem Deutsch berichten: was geändert wurde, ob die Prüfung grün ist, was noch offen ist.
