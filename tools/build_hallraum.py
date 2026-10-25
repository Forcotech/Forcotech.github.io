#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Abschnitt „Messwerte im Hallraum“ (#hallraum) der HSA3-Seite, Deutsch und Englisch.

Daten: Prüfbericht-Exzerpt BeSB Schalltechnisches Büro, Auftraggeber ABSORA GmbH,
Hallraum TU Berlin, Messung 10./11.02.2026, Bericht vom 12.03.2026 (Veröffentlichung mit ABSORA abgestimmt).

Das Skript erzeugt Diagramm (SVG), Tabellen und Text und setzt sie in hsa3/_src/de.html und en.html
zwischen <!-- HALLRAUM:START --> und <!-- HALLRAUM:END --> ein (wiederholbar). Danach
python3 tools/build_loesungen.py und python3 tools/build_news.py ausführen.
"""
from pathlib import Path
from html import escape as E

ROOT = Path(__file__).resolve().parent.parent
PDF = "/downloads/absora-hsa3-hallraum-absorptionsgrade-2026.pdf"

F = [100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000]

# id, Gruppe, Farbe, Strich, standardmäßig sichtbar, Klasse, NRC, SAA, Form, Prüffläche m², α_s je Terz
S = [
    ("h3w", "hsa3", "#c8202f", "", True, "C", 0.85, 0.85, "L M H", 6.0,
     [0.61, 0.71, 0.91, 0.99, 0.94, 0.91, 0.93, 0.90, 0.87, 0.79, 0.83, 0.79, 0.78, 0.76, 0.72, 0.60, 0.52, 0.36]),
    ("h1w", "hsa3", "#1d4ed8", "", True, "D", 0.65, 0.66, "L", 6.0,
     [0.83, 0.84, 0.93, 0.89, 0.83, 0.77, 0.74, 0.67, 0.63, 0.61, 0.59, 0.56, 0.54, 0.54, 0.52, 0.43, 0.36, 0.22]),
    ("h3", "hsa3", "#1a1a1a", "", True, "D", 0.60, 0.61, "L", 6.0,
     [0.14, 0.20, 0.33, 0.48, 0.62, 0.80, 0.74, 0.69, 0.63, 0.48, 0.50, 0.59, 0.59, 0.59, 0.58, 0.53, 0.41, 0.29]),
    ("h3l", "hsa3", "#d97706", "", True, "D", 0.65, 0.65, "L M", 6.0,
     [0.13, 0.28, 0.39, 0.49, 0.67, 0.76, 0.75, 0.75, 0.68, 0.55, 0.58, 0.65, 0.65, 0.67, 0.62, 0.52, 0.48, 0.31]),
    ("st1", "tasche", "#0f766e", "6 4", False, "C", 0.75, 0.75, "L M H", 8.52,
     [0.15, 0.35, 0.38, 0.40, 0.69, 0.81, 0.87, 0.88, 0.83, 0.72, 0.62, 0.68, 0.84, 0.89, 0.76, 0.72, 0.72, 0.65]),
    ("st2", "tasche", "#7c3aed", "6 4", False, "C", 0.75, 0.75, "L M H", 8.7,
     [0.12, 0.26, 0.32, 0.41, 0.64, 0.76, 0.85, 0.86, 0.85, 0.79, 0.72, 0.78, 0.87, 0.79, 0.70, 0.67, 0.62, 0.54]),
    ("st3", "tasche", "#8a8a8a", "6 4", False, "D", 0.55, 0.53, "—", 8.85,
     [0.03, 0.11, 0.14, 0.23, 0.36, 0.46, 0.59, 0.65, 0.66, 0.66, 0.57, 0.49, 0.58, 0.58, 0.51, 0.50, 0.44, 0.36]),
]

T = {
    "de": {
        "kicker": "Messwerte im Hallraum",
        "h2": "Schallabsorptionsgrad nach DIN EN ISO 354",
        "sub": "Im Februar 2026 hat ABSORA mehrere HSA3-Aufbauten und Schalltaschen im Hallraum der TU Berlin prüfen lassen; "
               "gemessen und ausgewertet hat das BeSB Schalltechnisches Büro. Hier alle Ergebnisse in Terzbändern von 100 bis 5000 Hz.",
        "names": {
            "h3w": ("HSA3 (0,3) + 100 mm Mineralwolle", "Wandabstand 200 mm (E-200), Hohlraum mit 100 mm Mineralwolle"),
            "h1w": ("HSA3 (0,1) + 100 mm Mineralwolle", "Wandabstand 200 mm (E-200), Hohlraum mit 100 mm Mineralwolle"),
            "h3":  ("HSA3 (0,3), faserfrei", "Wandabstand 200 mm (E-200), leerer Hohlraum"),
            "h3l": ("HSA3 (0,3) mit L-Profilen, faserfrei", "Wandabstand 200 mm (E-200), L-Profile im Raster 250 mm"),
            "st1": ("Schalltaschen 90°, dicht", "Reihen ohne Zwischenraum"),
            "st2": ("Schalltaschen 90°, Rücken an Rücken", "Reihen paarweise Rücken an Rücken"),
            "st3": ("Schalltaschen 90°, jede zweite Reihe", "halbe Belegung"),
        },
        "g_hsa3": "HSA3-Paneele", "g_tasche": "Schalltaschen",
        "show": "Kurven ein- und ausblenden:",
        "y": "Schallabsorptionsgrad αₛ", "x": "Frequenz in Hz (Terzmitten)",
        "low": "tiefe Frequenzen: Verdichter, Ventilatoren",
        "fig": "Schallabsorptionsgrad αₛ über der Frequenz. 1,0 bedeutet: die auftreffende Schallenergie wird vollständig absorbiert.",
        "t_cap": "Einzahlwerte je Aufbau",
        "th": ("Aufbau", "Absorberklasse (DIN EN ISO 11654)", "NRC", "SAA", "αₛ bei 125 Hz", "αₛ bei 250 Hz", "Prüffläche"),
        "pts": [
            "<b>Tiefe Frequenzen:</b> HSA3 (0,1) mit Mineralwolle erreicht schon bei 100 Hz einen Absorptionsgrad von 0,83 und bei 160 Hz 0,93 – bei nur 200 mm Aufbauhöhe. Poröse Absorber allein bräuchten dafür ein Vielfaches an Dicke.",
            "<b>Breitbandig am stärksten:</b> HSA3 (0,3) mit Mineralwolle liegt von 160 bis 500 Hz bei 0,9 und darüber, NRC 0,85, Absorberklasse C.",
            "<b>Ganz ohne Fasern:</b> Die faserfreien HSA3-Aufbauten erreichen bis 0,80 (315 Hz) und NRC 0,60–0,65 – die Wahl für R290-Anlagen und Batteriespeicher, wo weder Fasern noch brennbare Stoffe zulässig sind. L-Profile heben die Absorption unter 250 Hz und über 1 kHz zusätzlich an.",
            "<b>Schalltaschen:</b> dicht gesetzt NRC 0,75 und Absorberklasse C, bei halber Belegung nur noch NRC 0,55 – die Anordnung zählt.",
        ],
        "data": "Alle Messwerte als Tabelle (Terzbänder)",
        "f": "f in Hz",
        "note": "Messung im Hallraum der TU Berlin (200 m³), 10./11.02.2026, Verfahren des abgeschalteten Rauschens, Terzbänder. "
                "Auftraggeber ABSORA GmbH, Berlin; Prüfbericht BeSB Schalltechnisches Büro vom 12.03.2026. "
                "Abweichend von der Norm mit verringerter Prüffläche (6–8,85 m² statt 10–12 m²), bei den HSA3-Aufbauten zudem mit verkürztem Messumfang – "
                "kleinere Prüfflächen können durch Kanteneffekte etwas höhere Werte ergeben. (0,3) und (0,1) kennzeichnen zwei HSA3-Blechvarianten. "
                "Laborwerte des Materials; die Pegelminderung einer Haube hängt von Gerät, Geometrie und Einbausituation ab und wird projektbezogen berechnet.",
        "dl": "Prüfbericht (Exzerpt, PDF) herunterladen",
    },
    "en": {
        "kicker": "Reverberation room data",
        "h2": "Sound absorption coefficient to EN ISO 354",
        "sub": "In February 2026 ABSORA had several HSA3 build-ups and sound pockets tested in the reverberation room of TU Berlin; "
               "measurement and evaluation by BeSB Schalltechnisches Büro. All results in one-third octave bands from 100 to 5000 Hz.",
        "names": {
            "h3w": ("HSA3 (0.3) + 100 mm mineral wool", "200 mm cavity (E-200), filled with 100 mm mineral wool"),
            "h1w": ("HSA3 (0.1) + 100 mm mineral wool", "200 mm cavity (E-200), filled with 100 mm mineral wool"),
            "h3":  ("HSA3 (0.3), fibre-free", "200 mm cavity (E-200), empty"),
            "h3l": ("HSA3 (0.3) with L-profiles, fibre-free", "200 mm cavity (E-200), L-profiles at 250 mm spacing"),
            "st1": ("Sound pockets 90°, dense", "rows without gap"),
            "st2": ("Sound pockets 90°, back to back", "rows in back-to-back pairs"),
            "st3": ("Sound pockets 90°, every second row", "half coverage"),
        },
        "g_hsa3": "HSA3 panels", "g_tasche": "Sound pockets",
        "show": "Show or hide curves:",
        "y": "Sound absorption coefficient αₛ", "x": "Frequency in Hz (one-third octave centres)",
        "low": "low frequencies: compressors, fans",
        "fig": "Sound absorption coefficient αₛ versus frequency. 1.0 means the incident sound energy is fully absorbed.",
        "t_cap": "Single-number ratings per build-up",
        "th": ("Build-up", "Absorber class (EN ISO 11654)", "NRC", "SAA", "αₛ at 125 Hz", "αₛ at 250 Hz", "Test area"),
        "pts": [
            "<b>Low frequencies:</b> HSA3 (0.1) with mineral wool already reaches an absorption coefficient of 0.83 at 100 Hz and 0.93 at 160 Hz – with a build-up depth of only 200 mm. Porous absorbers alone would need several times that thickness.",
            "<b>Strongest across the band:</b> HSA3 (0.3) with mineral wool stays at 0.9 and above from 160 to 500 Hz, NRC 0.85, absorber class C.",
            "<b>Entirely fibre-free:</b> the fibre-free HSA3 build-ups reach up to 0.80 (315 Hz) and NRC 0.60–0.65 – the choice for R290 units and battery storage, where neither fibres nor combustible materials are allowed. L-profiles additionally raise absorption below 250 Hz and above 1 kHz.",
            "<b>Sound pockets:</b> NRC 0.75 and absorber class C when placed densely, only NRC 0.55 at half coverage – the arrangement matters.",
        ],
        "data": "All measured values as a table (one-third octave bands)",
        "f": "f in Hz",
        "note": "Measured in the reverberation room of TU Berlin (200 m³), 10/11 Feb 2026, interrupted noise method, one-third octave bands. "
                "Client ABSORA GmbH, Berlin; test report by BeSB Schalltechnisches Büro dated 12 Mar 2026. "
                "Deviating from the standard with a reduced test area (6–8.85 m² instead of 10–12 m²), for the HSA3 build-ups also with a reduced measurement scope – "
                "smaller test areas can give slightly higher values due to edge effects. (0.3) and (0.1) denote two HSA3 sheet variants. "
                "Laboratory values of the material; the noise reduction of an enclosure depends on unit, geometry and installation and is calculated per project.",
        "dl": "Download the test report (excerpt, PDF)",
    },
}


def num(v, lang, d=2):
    s = f"{v:.{d}f}"
    return s.replace(".", ",") if lang == "de" else s


def svg(lang):
    t = T[lang]
    W, H = 760, 430
    L, R, TOP, B = 58, 16, 18, 64
    pw, ph = W - L - R, H - TOP - B
    n = len(F)
    step = pw / (n - 1)
    X = lambda i: L + i * step
    Y = lambda a: TOP + ph * (1 - a)
    o = [f'<svg class="hr-svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="hr-t-{lang}" xmlns="http://www.w3.org/2000/svg">',
         f'<title id="hr-t-{lang}">{E(t["fig"])}</title>']
    # Tieffrequenzbereich 100–250 Hz
    o.append(f'<rect x="{L}" y="{TOP}" width="{X(4) - L:.1f}" height="{ph}" class="hr-low"/>')
    o.append(f'<text x="{L + 6}" y="{TOP + ph - 8}" class="hr-lowt">{E(t["low"])}</text>')
    for k in range(0, 11):
        a = k / 10
        cls = "hr-g0" if k == 0 else "hr-g"
        o.append(f'<line x1="{L}" x2="{W - R}" y1="{Y(a):.1f}" y2="{Y(a):.1f}" class="{cls}"/>')
        if k % 2 == 0:
            o.append(f'<text x="{L - 8}" y="{Y(a) + 4:.1f}" class="hr-yl">{num(a, lang, 1)}</text>')
    for i, f in enumerate(F):
        o.append(f'<line x1="{X(i):.1f}" x2="{X(i):.1f}" y1="{TOP}" y2="{TOP + ph}" class="hr-gv"/>')
        o.append(f'<text transform="translate({X(i):.1f},{TOP + ph + 12}) rotate(-45)" class="hr-xl">{f}</text>')
    o.append(f'<text x="{L + pw / 2:.0f}" y="{H - 6}" class="hr-at">{E(t["x"])}</text>')
    o.append(f'<text transform="translate(14,{TOP + ph / 2:.0f}) rotate(-90)" class="hr-at">{E(t["y"])}</text>')
    for sid, grp, col, dash, vis, *_r, vals in S:
        pts = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(vals))
        da = f' stroke-dasharray="{dash}"' if dash else ""
        hid = "" if vis else ' style="display:none"'
        o.append(f'<g data-s="{sid}" stroke="{col}" fill="{col}"{hid}>'
                 f'<polyline points="{pts}" fill="none" stroke-width="2.6" stroke-linejoin="round"{da}/>'
                 + "".join(f'<circle cx="{X(i):.1f}" cy="{Y(v):.1f}" r="3"><title>{E(t["names"][sid][0])} · {F[i]} Hz · αₛ = {num(v, lang)}</title></circle>'
                           for i, v in enumerate(vals)) + "</g>")
    o.append("</svg>")
    return "".join(o)


def section(lang):
    t = T[lang]
    groups = []
    for g in ("hsa3", "tasche"):
        btn = []
        for sid, grp, col, dash, vis, *_ in S:
            if grp != g:
                continue
            nm, ds = t["names"][sid]
            sw = f'<i style="border-color:{col}{";border-top-style:dashed" if dash else ""}"></i>'
            btn.append(f'<button type="button" data-s="{sid}" aria-pressed="{"true" if vis else "false"}" title="{E(ds)}">{sw}{E(nm)}</button>')
        groups.append(f'<div class="hr-grp"><span>{E(t["g_" + g])}</span>{"".join(btn)}</div>')
    rows = []
    for sid, grp, col, dash, vis, cls, nrc, saa, form, area, vals in S:
        nm, ds = t["names"][sid]
        best = ""
        rows.append(f'<tr><th scope="row"><i class="hr-sw" style="border-color:{col}{";border-top-style:dashed" if dash else ""}"></i>{E(nm)}<small>{E(ds)}</small></th>'
                    f'<td{best}>{cls}</td><td>{num(nrc, lang)}</td><td>{num(saa, lang)}</td>'
                    f'<td>{num(vals[1], lang)}</td><td>{num(vals[4], lang)}</td><td>{num(area, lang, 2 if area % 1 else 0)} m²</td></tr>')
    th = "".join(f'<th scope="col">{E(h)}</th>' for h in t["th"])
    # Vollständige Datentabelle
    dh = f'<th scope="col">{E(t["f"])}</th>' + "".join(f'<th scope="col">{E(t["names"][s[0]][0])}</th>' for s in S)
    drows = "".join(f'<tr><th scope="row">{f}</th>' + "".join(f"<td>{num(s[-1][i], lang)}</td>" for s in S) + "</tr>"
                    for i, f in enumerate(F))
    pts = "".join(f"<li>{p}</li>" for p in t["pts"])
    return f"""<!-- HALLRAUM:START – erzeugt mit tools/build_hallraum.py, nicht von Hand bearbeiten -->
<section id="hallraum">
  <div class="wrap">
    <span class="kicker">{E(t["kicker"])}</span>
    <h2>{E(t["h2"])}</h2>
    <p class="sub">{E(t["sub"])}</p>
    <figure class="hr-fig">
      <div class="hr-ctl" aria-label="{E(t["show"])}" role="group">{"".join(groups)}</div>
      <div class="hr-scroll">{svg(lang)}</div>
      <figcaption>{E(t["fig"])}</figcaption>
    </figure>
    <ul class="check hr-list">{pts}</ul>
    <div class="cmp">
      <table>
        <caption>{E(t["t_cap"])}</caption>
        <thead><tr>{th}</tr></thead>
        <tbody>{"".join(rows)}</tbody>
      </table>
    </div>
    <details class="hr-data"><summary>{E(t["data"])}</summary>
      <div class="cmp"><table class="hr-full"><thead><tr>{dh}</tr></thead><tbody>{drows}</tbody></table></div>
    </details>
    <p class="note">{E(t["note"])}</p>
    <p><a class="btn ghost" href="{PDF}" download>{E(t["dl"])}</a></p>
  </div>
  <script>
  (function(){{var s=document.getElementById('hallraum');if(!s)return;
  s.querySelectorAll('.hr-ctl button').forEach(function(b){{b.addEventListener('click',function(){{
  var on=b.getAttribute('aria-pressed')!=='true';b.setAttribute('aria-pressed',on);
  var g=s.querySelector('svg g[data-s="'+b.dataset.s+'"]');if(g)g.style.display=on?'':'none';}});}});}})();
  </script>
</section>
<!-- HALLRAUM:END -->"""


def main():
    import re
    for lang in ("de", "en"):
        p = ROOT / "hsa3" / "_src" / f"{lang}.html"
        src = p.read_text(encoding="utf-8")
        block = section(lang)
        if "<!-- HALLRAUM:START" in src:
            src = re.sub(r"<!-- HALLRAUM:START.*?<!-- HALLRAUM:END -->", lambda m: block, src, flags=re.S)
        else:
            # nach dem Abschnitt Kennwerte einsetzen
            i = src.index('<section class="alt" id="messung">' if lang == "de" else '<section class="alt" id="measurement">')
            src = src[:i] + block + "\n\n" + src[i:]
        p.write_text(src, encoding="utf-8")
    print("Abschnitt #hallraum in hsa3/_src/de.html und en.html gesetzt")


if __name__ == "__main__":
    main()
