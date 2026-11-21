#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Baut die Seite IoT-Services (/iot/, /en/iot/, /fr/iot/) aus iot/_src/<sprache>.html.

Inhalt ändern: Fragment in iot/_src/de.html, en.html bzw. fr.html bearbeiten und
python3 tools/build_iot.py  ausführen.
Die FAQ-Daten (schema.org FAQPage) werden aus den <details>-Fragen im Fragment erzeugt.
Kopf, Navigation und Fuß kommen aus tools/build_news.py.

Das Systemschema img/iot/lorawan-system-<sprache>.svg erzeugt dieses Skript selbst (Texte in SVG_TXT).
"""
from pathlib import Path
import build_news as bn
from build_hserie import faq_ld

ROOT = Path(__file__).resolve().parent.parent
URL = {"de": "/iot/", "en": "/en/iot/", "fr": "/fr/iot/"}
TECH = {"de": "/technik/#r290-havarie", "en": "/en/technology/#r290-havarie", "fr": "/fr/technique/#r290-havarie"}
TXT = {
    "de": {"title": "IoT-Services für Schallhauben – LoRaWAN-Monitoring von Druckverlust, Temperatur und Kältemittel bis ATEX | ForCoTech",
           "desc": "Funksensoren per LoRaWAN für Schallhauben und HVAC-Anlagen: Druckverlust, Luftgeschwindigkeit, Temperatur, Kältemittelleckage per Infrarot (NDIR) – nachrüstbar, bis zur ATEX-Ausführung für R290.",
           "kicker": "IoT-Services · LoRaWAN-Monitoring",
           "h1": "Messen statt vermuten: Druck&shy;verlust, Luft&shy;geschwindigkeit, Temperatur und Kälte&shy;mittel – bis zur ATEX-Lösung",
           "lead": "Funksensoren in und an der Schallhaube zeigen im Betrieb, was die Auslegung verspricht: Druckverlust innerhalb der Reserve, keine Rezirkulation, dichter Kältekreis. Übertragen per LoRaWAN, batteriebetrieben und nachrüstbar – für R290-Anlagen in Ex-Ausführung.",
           "b1": "IoT-Monitoring anfragen", "b2": "R290 und ATEX",
           "alt": "Systemschema: Sensoren für Differenzdruck, Luftgeschwindigkeit, Temperatur und Kältemittel in einer Schallhaube senden per LoRaWAN an ein Gateway und einen Netzwerkserver; von dort gehen die Daten an Dashboard, Alarme und Gebäudeleittechnik. Der Gassensor ist zusätzlich fest mit der Gaswarnzentrale verdrahtet."},
    "en": {"title": "IoT services for acoustic enclosures – LoRaWAN monitoring of pressure drop, temperature and refrigerant up to ATEX | ForCoTech",
           "desc": "Wireless LoRaWAN sensors for acoustic enclosures and HVAC units: pressure drop, air velocity, temperature, refrigerant leaks via infrared (NDIR) – retrofittable, up to ATEX design for R290.",
           "kicker": "IoT services · LoRaWAN monitoring",
           "h1": "Measure, don’t guess: pressure drop, air velocity, temperature and refrigerant – up to the ATEX solution",
           "lead": "Wireless sensors in and on the enclosure show in operation what the design promises: pressure drop within the reserve, no recirculation, a tight refrigerant circuit. Transmitted via LoRaWAN, battery-powered and retrofittable – in explosion-proof design for R290 units.",
           "b1": "Request IoT monitoring", "b2": "R290 and ATEX",
           "alt": "System diagram: sensors for differential pressure, air velocity, temperature and refrigerant inside an acoustic enclosure transmit via LoRaWAN to a gateway and a network server; from there data go to dashboard, alarms and building management system. The gas sensor is additionally hard-wired to the gas warning controller."},
    "fr": {"title": "Services IoT pour caissons acoustiques – monitoring LoRaWAN de la perte de charge, de la température et du fluide frigorigène jusqu’à l’ATEX | ForCoTech",
           "desc": "Capteurs sans fil LoRaWAN pour caissons acoustiques et installations CVC : perte de charge, vitesse d’air, température, fuites de fluide frigorigène par infrarouge (NDIR) – en rétrofit, jusqu’à l’exécution ATEX pour le R290.",
           "kicker": "Services IoT · Monitoring LoRaWAN",
           "h1": "Mesurer plutôt que supposer&nbsp;: perte de charge, vitesse d’air, température et fluide frigorigène – jusqu’à la solution ATEX",
           "lead": "Des capteurs sans fil dans et sur le caisson montrent en service ce que promet le dimensionnement&nbsp;: perte de charge dans la réserve, pas de recirculation, circuit frigorifique étanche. Transmission LoRaWAN, alimentation sur pile, installation en rétrofit possible – en exécution antidéflagrante pour les installations au R290.",
           "b1": "Demander un monitoring IoT", "b2": "R290 et ATEX",
           "alt": "Schéma du système : des capteurs de pression différentielle, de vitesse d’air, de température et de fluide frigorigène dans un caisson acoustique transmettent par LoRaWAN à une passerelle et à un serveur réseau ; de là, les données vont vers le tableau de bord, les alarmes et la GTB. Le détecteur de gaz est en outre câblé à la centrale de détection gaz."},
}

# Texte des Systemschemas je Sprache
SVG_TXT = {
    "de": {"hood": "Schallhaube", "unit": "Wärmepumpe / Chiller", "sil": "Schalldämpfer",
           "l1": "Δp  Druckverlust Schalldämpfer", "l2": "v  Luftgeschwindigkeit / Volumenstrom",
           "l3": "T  Temperatur Zuluft, Abluft, Umgebung", "l4": "IR  Kältemittel (NDIR), Ex",
           "gw": "LoRaWAN-Gateway", "gw2": "LAN oder Mobilfunk",
           "ns": "Netzwerkserver", "ns2": "beim Betreiber|oder in der EU",
           "d1": "Dashboard", "d1b": "Grenzwerte, Trends",
           "d2": "Alarme", "d2b": "E-Mail · SMS",
           "d3": "Leittechnik", "d3b": "BACnet · Modbus|MQTT",
           "gwz": "Gaswarnzentrale", "gwz2": "fest verdrahtet:", "gwz3": "Ventilatoren 100 %, Verdichter aus",
           "radio": "Funk 868 MHz", "wire": "Kabel – Sicherheitsfunktion"},
    "en": {"hood": "Acoustic enclosure", "unit": "Heat pump / chiller", "sil": "Silencer",
           "l1": "Δp  silencer pressure drop", "l2": "v  air velocity / air flow",
           "l3": "T  intake, exhaust, ambient temperature", "l4": "IR  refrigerant (NDIR), Ex",
           "gw": "LoRaWAN gateway", "gw2": "LAN or cellular",
           "ns": "Network server", "ns2": "on premises|or in the EU",
           "d1": "Dashboard", "d1b": "limits, trends",
           "d2": "Alarms", "d2b": "e-mail · SMS",
           "d3": "BMS", "d3b": "BACnet · Modbus|MQTT",
           "gwz": "Gas warning controller", "gwz2": "hard-wired:", "gwz3": "fans 100 %, compressors off",
           "radio": "Radio 868 MHz", "wire": "Cable – safety function"},
    "fr": {"hood": "Caisson acoustique", "unit": "PAC / groupe froid", "sil": "Silencieux",
           "l1": "Δp  perte de charge silencieux", "l2": "v  vitesse d’air / débit",
           "l3": "T  temp. air neuf, rejeté, ambiant", "l4": "IR  fluide (NDIR), Ex",
           "gw": "Passerelle LoRaWAN", "gw2": "LAN ou réseau mobile",
           "ns": "Serveur réseau", "ns2": "chez l’exploitant|ou dans l’UE",
           "d1": "Tableau de bord", "d1b": "seuils, tendances",
           "d2": "Alarmes", "d2b": "e-mail · SMS",
           "d3": "GTB", "d3b": "BACnet · Modbus|MQTT",
           "gwz": "Centrale détection gaz", "gwz2": "câblée :", "gwz3": "ventil. 100 %, compresseurs arrêt",
           "radio": "Radio 868 MHz", "wire": "Câble – fonction de sécurité"},
}


def svg(lang):
    t = SVG_TXT[lang]
    red, ink, mut, line, bg = "#c8202f", "#1a1a1a", "#4a4a4a", "#cfc8c8", "#f6f3f3"

    def sensor(x, y, s):
        return (f'<circle cx="{x}" cy="{y}" r="23" fill="{red}"/>'
                f'<text x="{x}" y="{y + 7}" text-anchor="middle" font-size="{18 if len(s) > 1 else 21}" font-weight="700" fill="#fff">{s}</text>')

    def box(x, y, w, h, a, b, strong=False):
        lines = b.split("|")  # "|" = Zeilenumbruch im Kasten
        y0 = y + h / 2 - 4 - 9 * (len(lines) - 1)
        sub = "".join(f'<text x="{x + w / 2}" y="{y0 + 22 + 18 * i}" text-anchor="middle" font-size="14.5" fill="{mut}">{l}</text>'
                      for i, l in enumerate(lines))
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="9" fill="#fff" stroke="{red if strong else ink}" stroke-width="2.2"/>'
                f'<text x="{x + w / 2}" y="{y0}" text-anchor="middle" font-size="18" font-weight="700" fill="{ink}">{a}</text>' + sub)

    tubes = "".join(f'<circle cx="{x}" cy="104" r="10" fill="none" stroke="{mut}" stroke-width="1.8"/>' for x in range(62, 320, 28))
    arcs = "".join(f'<path d="M {362 + i * 16} {170 - i * 6} q 14 -17 0 -34" fill="none" stroke="{red}" stroke-width="3" opacity="{1 - i * 0.25}"/>' for i in range(3))
    arrow = f'stroke="{ink}" stroke-width="2.2" marker-end="url(#a)"'
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 490" font-family="Inter, Segoe UI, Arial, sans-serif">
<rect width="920" height="490" fill="#fff"/>
<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10z" fill="{ink}"/></marker></defs>
<text x="185" y="34" text-anchor="middle" font-size="20" font-weight="700" fill="{ink}">{t["hood"]}</text>
<rect x="20" y="48" width="330" height="282" rx="6" fill="{bg}" stroke="{ink}" stroke-width="2.5"/>
<rect x="38" y="84" width="294" height="40" rx="4" fill="#fff" stroke="{line}" stroke-width="1.5"/>{tubes}
<text x="185" y="76" text-anchor="middle" font-size="15" fill="{mut}">{t["sil"]}</text>
<rect x="82" y="168" width="216" height="104" rx="6" fill="#e8e2e2" stroke="{line}" stroke-width="1.5"/>
<text x="190" y="226" text-anchor="middle" font-size="17" fill="{ink}">{t["unit"]}</text>
{sensor(52, 158, "Δp")}{sensor(318, 158, "v")}{sensor(52, 230, "T")}{sensor(110, 300, "IR")}
{arcs}
<text x="364" y="112" font-size="15" fill="{mut}">{t["radio"]}</text>
<line x1="490" y1="62" x2="490" y2="132" stroke="{ink}" stroke-width="3.5"/>
<path d="M471 52 q19 -19 38 0 M461 42 q29 -31 58 0" fill="none" stroke="{red}" stroke-width="3"/>
<rect x="436" y="132" width="108" height="44" rx="9" fill="#fff" stroke="{red}" stroke-width="2.5"/>
<text x="490" y="200" text-anchor="middle" font-size="17" font-weight="700" fill="{ink}">{t["gw"]}</text>
<text x="490" y="220" text-anchor="middle" font-size="14.5" fill="{mut}">{t["gw2"]}</text>
<line x1="546" y1="154" x2="574" y2="154" {arrow}/>
{box(578, 110, 152, 88, t["ns"], t["ns2"], True)}
<path d="M732 140 C 748 140 744 74 760 74" fill="none" {arrow}/>
<line x1="732" y1="154" x2="760" y2="160" {arrow}/>
<path d="M732 168 C 748 168 744 246 760 246" fill="none" {arrow}/>
{box(764, 40, 152, 68, t["d1"], t["d1b"])}{box(764, 126, 152, 68, t["d2"], t["d2b"])}{box(764, 212, 152, 80, t["d3"], t["d3b"])}
<path d="M133 300 H 392 V 384" fill="none" stroke="{ink}" stroke-width="3"/>
<text x="404" y="366" font-size="15" font-weight="700" fill="{ink}">{t["wire"]}</text>
<rect x="380" y="384" width="330" height="92" rx="9" fill="#fff" stroke="{ink}" stroke-width="2.5"/>
<text x="545" y="414" text-anchor="middle" font-size="18" font-weight="700" fill="{ink}">{t["gwz"]}</text>
<text x="545" y="438" text-anchor="middle" font-size="14.5" fill="{mut}">{t["gwz2"]}</text>
<text x="545" y="460" text-anchor="middle" font-size="14.5" fill="{mut}">{t["gwz3"]}</text>
<path d="M712 430 H 840 V 296" fill="none" {arrow}/>
<g font-size="15.5" fill="{ink}"><text x="20" y="364">{t["l1"]}</text><text x="20" y="390">{t["l2"]}</text><text x="20" y="416">{t["l3"]}</text><text x="20" y="442">{t["l4"]}</text></g>
</svg>
"""


def build():
    for lang in URL:
        t = TXT[lang]
        name = f"img/iot/lorawan-system-{lang}.svg"
        bn.write(name, svg(lang))
        frag = (ROOT / "iot" / "_src" / f"{lang}.html").read_text(encoding="utf-8")
        main = f"""<div class="hero">
  <div class="wrap hg">
    <div>
      <span class="kicker">{t["kicker"]}</span>
      <h1>{t["h1"]}</h1>
      <p class="lead">{t["lead"]}</p>
      <div class="btns"><a class="btn" href="#anfrage" data-typ="iot">{t["b1"]}</a><a class="btn ghost" href="{TECH[lang]}">{t["b2"]}</a></div>
    </div>
    <figure class="dc-hero iot-hero"><img src="/{name}" width="920" height="490" alt="{t["alt"]}" fetchpriority="high"></figure>
  </div>
</div>
{frag}"""
        head = f'<script type="application/ld+json">{faq_ld(frag, lang)}</script>'
        bn.write(URL[lang][1:] + "index.html",
                 bn.page(lang, t["title"], t["desc"], dict(URL), main, extra_head=head, typ="iot"))
    print("IoT-Seiten gebaut (de, en, fr)")


if __name__ == "__main__":
    build()
