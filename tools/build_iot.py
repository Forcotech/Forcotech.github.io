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
import re
import build_news as bn
from build_hserie import faq_ld

ROOT = Path(__file__).resolve().parent.parent
URL = {"de": "/iot/", "en": "/en/iot/", "fr": "/fr/iot/"}
TECH = {"de": "/technik/#r290-havarie", "en": "/en/technology/#r290-havarie", "fr": "/fr/technique/#r290-havarie"}
TXT = {
    "de": {"title": "IoT-Services für Schallhauben – LoRaWAN-Monitoring von Druckverlust, Schall, Strom und Kältemittel bis ATEX | ForCoTech",
           "desc": "Funksensoren per LoRaWAN für Schallhauben und HVAC-Anlagen: Druckverlust, Luftgeschwindigkeit, Temperatur, Schallpegel, Lastgang (Strom), Kältemittelleckage per Infrarot (NDIR) – nachrüstbar, bis zur ATEX-Ausführung für R290.",
           "kicker": "IoT-Services · LoRaWAN-Monitoring",
           "h1": "IoT-Monitoring bis zur ATEX-Lösung",
           "lead": "Funksensoren messen Druckverlust, Luftgeschwindigkeit, Temperatur, Schallpegel, Stromverbrauch und Kältemittel. So zeigt der Betrieb, was die Auslegung verspricht: Pegel eingehalten, Druckverlust innerhalb der Reserve, kein Mehrverbrauch, dichter Kältekreis. Übertragen per LoRaWAN, nachrüstbar – für R290-Anlagen in Ex-Ausführung.",
           "b1": "IoT-Monitoring anfragen", "b2": "R290 und ATEX",
           "alt": "Systemschema: Sensoren für Differenzdruck, Luftgeschwindigkeit, Temperatur und Kältemittel in einer Schallhaube senden per LoRaWAN an ein Gateway und einen Netzwerkserver; von dort gehen die Daten an Dashboard, Alarme und Gebäudeleittechnik. Der Gassensor ist zusätzlich fest mit der Gaswarnzentrale verdrahtet."},
    "en": {"title": "IoT services for acoustic enclosures – LoRaWAN monitoring of pressure drop, sound, power and refrigerant up to ATEX | ForCoTech",
           "desc": "Wireless LoRaWAN sensors for acoustic enclosures and HVAC units: pressure drop, air velocity, temperature, sound level, load profile (power), refrigerant leaks via infrared (NDIR) – retrofittable, up to ATEX design for R290.",
           "kicker": "IoT services · LoRaWAN monitoring",
           "h1": "IoT monitoring up to the ATEX solution",
           "lead": "Wireless sensors measure pressure drop, air velocity, temperature, sound level, power consumption and refrigerant. Operation then shows what the design promises: noise limits met, pressure drop within the reserve, no extra consumption, a tight refrigerant circuit. Transmitted via LoRaWAN, retrofittable – in explosion-proof design for R290 units.",
           "b1": "Request IoT monitoring", "b2": "R290 and ATEX",
           "alt": "System diagram: sensors for differential pressure, air velocity, temperature and refrigerant inside an acoustic enclosure transmit via LoRaWAN to a gateway and a network server; from there data go to dashboard, alarms and building management system. The gas sensor is additionally hard-wired to the gas warning controller."},
    "fr": {"title": "Services IoT pour caissons acoustiques – monitoring LoRaWAN de la perte de charge, du bruit, de l’électricité et du fluide frigorigène jusqu’à l’ATEX | ForCoTech",
           "desc": "Capteurs sans fil LoRaWAN pour caissons acoustiques et installations CVC : perte de charge, vitesse d’air, température, niveau sonore, courbe de charge (électricité), fuites de fluide frigorigène par infrarouge (NDIR) – en rétrofit, jusqu’à l’exécution ATEX pour le R290.",
           "kicker": "Services IoT · Monitoring LoRaWAN",
           "h1": "Monitoring IoT jusqu’à la solution ATEX",
           "lead": "Des capteurs sans fil mesurent perte de charge, vitesse d’air, température, niveau sonore, consommation électrique et fluide frigorigène. L’exploitation montre alors ce que promet le dimensionnement&nbsp;: niveaux respectés, perte de charge dans la réserve, pas de surconsommation, circuit frigorifique étanche. Transmission LoRaWAN, rétrofit possible – en exécution antidéflagrante pour le R290.",
           "b1": "Demander un monitoring IoT", "b2": "R290 et ATEX",
           "alt": "Schéma du système : des capteurs de pression différentielle, de vitesse d’air, de température et de fluide frigorigène dans un caisson acoustique transmettent par LoRaWAN à une passerelle et à un serveur réseau ; de là, les données vont vers le tableau de bord, les alarmes et la GTB. Le détecteur de gaz est en outre câblé à la centrale de détection gaz."},
}

# Texte des Systemschemas je Sprache
SVG_TXT = {
    "de": {"hood": "Schallhaube", "unit": "Wärmepumpe / Chiller", "sil": "Schalldämpfer",
           "l1": "Δp  Druckverlust Schalldämpfer", "l2": "v  Luftgeschwindigkeit / Volumenstrom",
           "l3": "T  Temperatur Zuluft, Abluft, Umgebung", "l4": "IR  Kältemittel (NDIR), Ex", "l5": "dB  Schallpegel (LAeq, LAFmax)", "l6": "kW  Lastgang Strom (Zähler)",
           "gw": "LoRaWAN-Gateway", "gw2": "LAN oder Mobilfunk",
           "ns": "Netzwerkserver", "ns2": "beim Betreiber|oder in der EU",
           "d1": "Dashboard", "d1b": "Grenzwerte, Trends",
           "d2": "Alarme", "d2b": "E-Mail · SMS",
           "d3": "Leittechnik", "d3b": "BACnet · Modbus|MQTT",
           "gwz": "Gaswarnzentrale", "gwz2": "fest verdrahtet:", "gwz3": "Ventilatoren 100 %, Verdichter aus",
           "radio": "Funk 868 MHz", "wire": "Kabel – Sicherheitsfunktion"},
    "en": {"hood": "Acoustic enclosure", "unit": "Heat pump / chiller", "sil": "Silencer",
           "l1": "Δp  silencer pressure drop", "l2": "v  air velocity / air flow",
           "l3": "T  intake, exhaust, ambient temperature", "l4": "IR  refrigerant (NDIR), Ex", "l5": "dB  sound level (LAeq, LAFmax)", "l6": "kW  power load profile (meter)",
           "gw": "LoRaWAN gateway", "gw2": "LAN or cellular",
           "ns": "Network server", "ns2": "on premises|or in the EU",
           "d1": "Dashboard", "d1b": "limits, trends",
           "d2": "Alarms", "d2b": "e-mail · SMS",
           "d3": "BMS", "d3b": "BACnet · Modbus|MQTT",
           "gwz": "Gas warning controller", "gwz2": "hard-wired:", "gwz3": "fans 100 %, compressors off",
           "radio": "Radio 868 MHz", "wire": "Cable – safety function"},
    "fr": {"hood": "Caisson acoustique", "unit": "PAC / groupe froid", "sil": "Silencieux",
           "l1": "Δp  perte de charge silencieux", "l2": "v  vitesse d’air / débit",
           "l3": "T  temp. air neuf, rejeté, ambiant", "l4": "IR  fluide (NDIR), Ex", "l5": "dB  niveau sonore (LAeq, LAFmax)", "l6": "kW  courbe de charge (compteur)",
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
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 920 540" font-family="Inter, Segoe UI, Arial, sans-serif">
<rect width="920" height="540" fill="#fff"/>
<defs><marker id="a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0 10 5 0 10z" fill="{ink}"/></marker></defs>
<text x="185" y="34" text-anchor="middle" font-size="20" font-weight="700" fill="{ink}">{t["hood"]}</text>
<rect x="20" y="48" width="330" height="282" rx="6" fill="{bg}" stroke="{ink}" stroke-width="2.5"/>
<rect x="38" y="84" width="294" height="40" rx="4" fill="#fff" stroke="{line}" stroke-width="1.5"/>{tubes}
<text x="185" y="76" text-anchor="middle" font-size="15" fill="{mut}">{t["sil"]}</text>
<rect x="82" y="168" width="216" height="104" rx="6" fill="#e8e2e2" stroke="{line}" stroke-width="1.5"/>
<text x="190" y="226" text-anchor="middle" font-size="17" fill="{ink}">{t["unit"]}</text>
{sensor(52, 158, "Δp")}{sensor(318, 158, "v")}{sensor(52, 230, "T")}{sensor(110, 296, "IR")}{sensor(318, 228, "dB")}{sensor(318, 296, "kW")}
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
<path d="M110 319 V 324 H 392 V 384" fill="none" stroke="{ink}" stroke-width="3"/>
<text x="404" y="366" font-size="15" font-weight="700" fill="{ink}">{t["wire"]}</text>
<rect x="380" y="384" width="330" height="92" rx="9" fill="#fff" stroke="{ink}" stroke-width="2.5"/>
<text x="545" y="414" text-anchor="middle" font-size="18" font-weight="700" fill="{ink}">{t["gwz"]}</text>
<text x="545" y="438" text-anchor="middle" font-size="14.5" fill="{mut}">{t["gwz2"]}</text>
<text x="545" y="460" text-anchor="middle" font-size="14.5" fill="{mut}">{t["gwz3"]}</text>
<path d="M712 430 H 840 V 296" fill="none" {arrow}/>
<g font-size="15.5" fill="{ink}"><text x="20" y="364">{t["l1"]}</text><text x="20" y="390">{t["l2"]}</text><text x="20" y="416">{t["l3"]}</text><text x="20" y="442">{t["l4"]}</text><text x="20" y="468">{t["l5"]}</text><text x="20" y="494">{t["l6"]}</text></g>
</svg>
"""


# ---------- Icons bei den Messgrößen (data-ico im Fragment) ----------
_IP = {
    "dp": '<path d="M4 16a8 8 0 1 1 16 0"/><path d="M12 16l4-5"/><circle cx="12" cy="16" r="1.4" fill="currentColor"/>',
    "v": '<path d="M3 8h11a3 3 0 1 0-3-3"/><path d="M3 12h16a3 3 0 1 1-3 3"/><path d="M3 16h7"/>',
    "t": '<path d="M10 4a2 2 0 0 1 4 0v9.5a4 4 0 1 1-4 0z"/><path d="M12 9v7"/>',
    "ir": '<path d="M12 3s5 6 5 10a5 5 0 0 1-10 0c0-4 5-10 5-10z"/><path d="M9.5 14h5"/>',
    "db": '<path d="M4 10v4h4l5 4V6L8 10z"/><path d="M16 9a4 4 0 0 1 0 6"/><path d="M18.5 6.5a7.5 7.5 0 0 1 0 11"/>',
    "kw": '<path d="M13 3L5 14h6l-1 7 8-11h-6z"/>',
    "shield": '<path d="M12 3l7 3v5c0 4.5-3 8.2-7 10-4-1.8-7-5.5-7-10V6z"/><path d="M9 12l2 2 4-4"/>',
    "wrench": '<path d="M14.5 6.5a4 4 0 0 0-5.3 5.3L4 17l3 3 5.2-5.2a4 4 0 0 0 5.3-5.3l-2.6 2.6-2.4-.6-.6-2.4z"/>',
    "lock": '<rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V8a4 4 0 0 1 8 0v3"/><circle cx="12" cy="15.5" r="1.3" fill="currentColor"/>',
    "ex": '<path d="M12 3l9.5 17h-19z"/><text x="12" y="17.2" text-anchor="middle" font-size="7" font-weight="800" fill="currentColor" stroke="none" font-family="Arial">Ex</text>',
}


def icons(frag):
    def rep(m):
        k = m.group(2)
        ic = (f'<span class="iot-ico" aria-hidden="true"><svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor" '
              f'stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round">{_IP[k]}</svg></span>')
        return m.group(1) + ">" + ic
    return re.sub(r'(<div class="card(?: iot-atex| iot-aud)?" data-ico="(\w+)")>', rep, frag)


# ---------- Beispielgrafiken und Beispielrechnung (Abschnitt <!--BEISPIELE-->) ----------
# Werte sind bewusst Beispielwerte (keine Messdaten, keine Projektdaten) und so gekennzeichnet.
CALC = dict(V=60000, dp=40, eta=0.5, h=3000, price=0.25, P=100, dT=2, pk=2.5)


def calc():
    c = CALC
    w_air = c["V"] / 3600 * c["dp"]                 # W Luftleistung
    p_el = w_air / c["eta"] / 1000                  # kW elektrisch
    e1 = p_el * c["h"]                              # kWh/a
    e2 = c["P"] * c["h"] * c["dT"] * c["pk"] / 100  # kWh/a
    return dict(w_air=w_air, p_el=p_el, e1=e1, eur1=e1 * c["price"], e2=e2, eur2=e2 * c["price"])


def fmt(x, lang, d=0):
    s = f"{x:,.{d}f}"
    if lang == "en":
        return s
    sep = "." if lang == "de" else " "
    return s.replace(",", "X").replace(".", ",").replace("X", sep)


EX = {
    "de": dict(k="Im Betrieb", h="So sieht das im Dashboard aus", note="Beispieldarstellungen – keine Messdaten einer realen Anlage.",
               c1="Lastgang und Druckverlust über vier Wochen", c2="Rezirkulations-Alarm im Dashboard",
               w="Woche", kw="Leistung kW", pa="Δp Pa", lim="Grenzwert Δp", clean="Reinigung", leg1="Leistung (Mittel aus 15-Minuten-Werten)", leg2="Druckverlust Schalldämpfer",
               dash="Anlage 1 · Schallhaube Dach", alarm="Alarm: Rezirkulation", tout="Außen", tin="Zuluft", band="Zuluft > Außen + 3 K",
               k1="Druckverlust", k2="LAeq Nacht", k3="Leistung", h24="Uhr",
               rk="Beispielrechnung", rh="Was ein unbemerkter Mehrdruck und Rezirkulation kosten",
               rnote="Beispielrechnung mit typischen Annahmen, keine Projektdaten. Mit Ihren Anlagendaten rechnen wir es konkret.",
               r1h="Verschmutzte Schalldämpfer", r2h="Rezirkulation warmer Abluft",
               r1=["Volumenstrom {V} m³/h, Druckverlust steigt um {dp} Pa", "Zusätzliche Luftleistung: {w_air} W", "Bei 50 % Ventilator-Gesamtwirkungsgrad: {p_el} kW elektrisch",
                   "{h} Betriebsstunden pro Jahr"],
               r2=["Elektrische Leistung der Anlage {P} kW, {h} Betriebsstunden pro Jahr", "Zuluft im Mittel {dT} K wärmer als außen",
                   "Faustwert: ca. {pk} % Effizienzverlust je Kelvin"],
               per="kWh pro Jahr", eur="€ pro Jahr bei {price} €/kWh"),
    "en": dict(k="In operation", h="What it looks like in the dashboard", note="Example illustrations – not measured data from a real unit.",
               c1="Load profile and pressure drop over four weeks", c2="Recirculation alarm in the dashboard",
               w="Week", kw="Power kW", pa="Δp Pa", lim="Δp limit", clean="Cleaning", leg1="Power (mean of 15-minute values)", leg2="Silencer pressure drop",
               dash="Unit 1 · rooftop enclosure", alarm="Alarm: recirculation", tout="Ambient", tin="Intake", band="Intake > ambient + 3 K",
               k1="Pressure drop", k2="LAeq night", k3="Power", h24="h",
               rk="Example calculation", rh="What unnoticed extra pressure and recirculation cost",
               rnote="Example calculation with typical assumptions, not project data. With your unit data we calculate it specifically.",
               r1h="Fouled silencers", r2h="Recirculation of warm exhaust air",
               r1=["Air flow {V} m³/h, pressure drop rises by {dp} Pa", "Additional air power: {w_air} W", "At 50 % overall fan efficiency: {p_el} kW electrical",
                   "{h} operating hours per year"],
               r2=["Electrical power of the unit {P} kW, {h} operating hours per year", "Intake air on average {dT} K warmer than ambient",
                   "Rule of thumb: approx. {pk} % efficiency loss per kelvin"],
               per="kWh per year", eur="€ per year at €{price}/kWh"),
    "fr": dict(k="En service", h="À quoi cela ressemble dans le tableau de bord", note="Illustrations d’exemple – pas de données mesurées sur une installation réelle.",
               c1="Courbe de charge et perte de charge sur quatre semaines", c2="Alarme de recirculation dans le tableau de bord",
               w="Semaine", kw="Puissance kW", pa="Δp Pa", lim="Seuil Δp", clean="Nettoyage", leg1="Puissance (moyenne pas de 15 min)", leg2="Perte de charge silencieux",
               dash="Installation 1 · caisson en toiture", alarm="Alarme : recirculation", tout="Extérieur", tin="Air neuf", band="Air neuf > extérieur + 3 K",
               k1="Perte de charge", k2="LAeq nuit", k3="Puissance", h24="h",
               rk="Exemple de calcul", rh="Ce que coûtent une surpression et une recirculation non détectées",
               rnote="Exemple de calcul avec des hypothèses typiques, pas de données de projet. Avec les données de votre installation, nous le chiffrons précisément.",
               r1h="Silencieux encrassés", r2h="Recirculation de l’air chaud rejeté",
               r1=["Débit {V} m³/h, la perte de charge augmente de {dp} Pa", "Puissance aéraulique supplémentaire : {w_air} W", "Avec un rendement global du ventilateur de 50 % : {p_el} kW électriques",
                   "{h} heures de fonctionnement par an"],
               r2=["Puissance électrique de l’installation {P} kW, {h} heures de fonctionnement par an", "Air neuf en moyenne {dT} K plus chaud que l’extérieur",
                   "Valeur indicative : env. {pk} % de perte d’efficacité par kelvin"],
               per="kWh par an", eur="€ par an à {price} €/kWh"),
}


# Einordnung der Wirtschaftlichkeit (unter der Beispielrechnung); Preise passend zur Richtpreistabelle in iot/_src
ROI = {
    "de": ("Einordnung: Wann rechnet sich das?", [
        ("Kleine Wärmepumpen", "Basis-Paket, ca. 1.800 €", "Über die Stromersparnis allein rechnet es sich erst nach etwa 4–6 Jahren. Hier ist das Monitoring vor allem eine Absicherung gegen Gewährleistungsstreit und Lärmbeschwerden."),
        ("Großanlagen und Kaltwassersätze", "Performance-Paket, ca. 2.800 €", "Deckt das System eine Rezirkulation oder verschmutzte Kulissen wie in der Beispielrechnung auf, ist es oft schon im ersten Betriebsjahr bezahlt."),
        ("R290-Großanlagen", "ATEX-Paket, ca. 6.500 €", "Hier zählen Genehmigungsfähigkeit und Haftungssicherheit. Eine Gaswarnanlage ist ohnehin vorgeschrieben – Fernmeldung und Dokumentation kosten im Verhältnis zur Gesamtanlage wenig."),
        ("Mehrere Hauben auf einem Dach", "ein Gateway für alle", "Das Gateway wird nur einmal benötigt. Jede weitere Haube am selben Standort wird dadurch spürbar günstiger.")]),
    "en": ("In context: when does it pay off?", [
        ("Small heat pumps", "Basic package, approx. €1,800", "On power savings alone it pays off only after about 4–6 years. Here monitoring is mainly protection against warranty disputes and noise complaints."),
        ("Large units and chillers", "Performance package, approx. €2,800", "If the system uncovers recirculation or fouled silencers as in the example calculation, it often pays for itself in the first year of operation."),
        ("Large R290 units", "ATEX package, approx. €6,500", "What counts here is approvability and liability protection. A gas warning system is required anyway – remote reporting and documentation cost little compared with the whole installation."),
        ("Several enclosures on one roof", "one gateway for all", "The gateway is needed only once. Each additional enclosure at the same site therefore costs noticeably less.")]),
    "fr": ("En perspective : quand est-ce rentable ?", [
        ("Petites pompes à chaleur", "Offre Base, env. 1 800 €", "Par la seule économie d’électricité, le retour prend environ 4 à 6 ans. Le monitoring est ici surtout une protection contre les litiges de garantie et les plaintes pour bruit."),
        ("Grandes installations et groupes froids", "Offre Performance, env. 2 800 €", "Si le système détecte une recirculation ou des silencieux encrassés comme dans l’exemple de calcul, il est souvent amorti dès la première année d’exploitation."),
        ("Grandes installations au R290", "Offre ATEX, env. 6 500 €", "Ce qui compte ici, c’est l’autorisation et la sécurité juridique. Une détection gaz est de toute façon obligatoire – le report à distance et la documentation coûtent peu au regard de l’installation complète."),
        ("Plusieurs caissons sur un toit", "une passerelle pour tous", "La passerelle n’est nécessaire qu’une fois. Chaque caisson supplémentaire sur le même site coûte donc nettement moins.")]),
}


def svg_lastgang(lang):
    t = EX[lang]
    import math
    W, H, x0, x1, y0, y1 = 640, 330, 46, 594, 48, 262
    n = 28 * 4
    def X(i): return x0 + (x1 - x0) * i / (n - 1)
    clean_i = int(n * 0.80)
    pts_p, pts_d = [], []
    for i in range(n):
        day = i / 4
        foul = min(day, 22.4) / 22.4 if i < clean_i else 0
        base = 33 + 1.2 * math.sin(i * 0.9) + (2.5 if (day % 7) < 5 else -4)
        p = base * (1 + 0.09 * foul)
        d = 58 + 44 * foul + 1.2 * math.sin(i * 1.3)
        pts_p.append((X(i), y1 - (p - 20) / 30 * (y1 - y0)))
        pts_d.append((X(i), y1 - (d - 40) / 80 * (y1 - y0)))
    pl = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts_p)
    dl = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts_d)
    ylim = y1 - (95 - 40) / 80 * (y1 - y0)
    xc = X(clean_i)
    ia = next(i for i in range(n) if 58 + 44 * (min(i / 4, 22.4) / 22.4) >= 95)
    xa, ya = X(ia), ylim
    grid = "".join(f'<line x1="{x0}" y1="{y0 + k * (y1 - y0) / 4:.0f}" x2="{x1}" y2="{y0 + k * (y1 - y0) / 4:.0f}" stroke="#ece8e8"/>' for k in range(5))
    yl = "".join(f'<text x="{x0 - 8}" y="{y1 - k * (y1 - y0) / 3 + 5:.0f}" text-anchor="end" font-size="13" fill="#4a4a4a">{20 + 10 * k}</text>' for k in range(4))
    yr = "".join(f'<text x="{x1 + 8}" y="{y1 - k * (y1 - y0) / 4 + 5:.0f}" font-size="13" fill="#c8202f">{40 + 20 * k}</text>' for k in range(5))
    xl = "".join(f'<text x="{x0 + (x1 - x0) * (k + .5) / 4:.0f}" y="{y1 + 22}" text-anchor="middle" font-size="13.5" fill="#4a4a4a">{t["w"]} {k + 1}</text>' for k in range(4))
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Inter, Segoe UI, Arial, sans-serif">
<rect width="{W}" height="{H}" fill="#fff"/>{grid}
<text x="6" y="26" font-size="13" font-weight="700" fill="#1a1a1a">{t["kw"]}</text>
<text x="{W - 6}" y="26" text-anchor="end" font-size="13" font-weight="700" fill="#c8202f">{t["pa"]}</text>{yl}{yr}{xl}
<line x1="{x0}" y1="{ylim:.0f}" x2="{x1}" y2="{ylim:.0f}" stroke="#c8202f" stroke-width="1.5" stroke-dasharray="6 5"/>
<text x="{x0 + 6}" y="{ylim - 8:.0f}" font-size="13" font-weight="700" fill="#c8202f">{t["lim"]}</text>
<polyline points="{pl}" fill="none" stroke="#1a1a1a" stroke-width="2.2" stroke-linejoin="round"/>
<polyline points="{dl}" fill="none" stroke="#c8202f" stroke-width="3"/>
<line x1="{xc:.0f}" y1="{y0}" x2="{xc:.0f}" y2="{y1}" stroke="#1a1a1a" stroke-width="1.5" stroke-dasharray="3 4"/>
<text x="{xc + 6:.0f}" y="{y0 + 14}" font-size="13.5" font-weight="700" fill="#1a1a1a">{t["clean"]}</text>
<circle cx="{xa:.0f}" cy="{ya:.0f}" r="9" fill="#c8202f"/><text x="{xa:.0f}" y="{ya + 5:.0f}" text-anchor="middle" font-size="13" font-weight="800" fill="#fff">!</text>
<line x1="{x0}" y1="{y1}" x2="{x1}" y2="{y1}" stroke="#1a1a1a" stroke-width="1.4"/>
<g font-size="13.5" fill="#1a1a1a"><line x1="{x0}" y1="{H - 18}" x2="{x0 + 26}" y2="{H - 18}" stroke="#1a1a1a" stroke-width="2"/><text x="{x0 + 34}" y="{H - 13}">{t["leg1"]}</text>
<line x1="{x0 + 320}" y1="{H - 18}" x2="{x0 + 346}" y2="{H - 18}" stroke="#c8202f" stroke-width="3"/><text x="{x0 + 354}" y="{H - 13}">{t["leg2"]}</text></g>
</svg>
"""


def svg_dashboard(lang):
    t = EX[lang]
    import math
    W, H = 640, 330
    gx0, gx1, gy0, gy1 = 40, 600, 92, 214
    n = 97
    def X(i): return gx0 + (gx1 - gx0) * i / (n - 1)
    def Y(v): return gy1 - (v - 10) / 22 * (gy1 - gy0)
    out, inn = [], []
    for i in range(n):
        hh = i / 4
        to = 19 + 8 * math.sin((hh - 9) / 24 * 2 * math.pi)
        rec = max(0.0, math.sin((hh - 11) / 8 * math.pi)) * 5.2 if 11 <= hh <= 19 else 0
        out.append(to); inn.append(to + 0.6 + rec)
    band = [i for i in range(n) if inn[i] - out[i] > 3]
    bx0, bx1 = X(band[0]), X(band[-1])
    po = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(out))
    pi_ = " ".join(f"{X(i):.1f},{Y(v):.1f}" for i, v in enumerate(inn))
    xt = "".join(f'<text x="{X(k * 24):.0f}" y="{gy1 + 18}" text-anchor="middle" font-size="12.5" fill="#4a4a4a">{k * 6:02d}{"" if lang == "en" else ":00"}</text>' for k in range(5))
    def kpi(x, a, b):
        return (f'<rect x="{x}" y="250" width="176" height="62" rx="8" fill="#f6f3f3"/>'
                f'<text x="{x + 12}" y="272" font-size="12.5" fill="#4a4a4a">{a}</text><text x="{x + 12}" y="300" font-size="22" font-weight="800" fill="#1a1a1a">{b}</text>')
    dec = "," if lang != "en" else "."
    return f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" font-family="Inter, Segoe UI, Arial, sans-serif">
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="12" fill="#fff" stroke="#d9d4d4" stroke-width="1.5"/>
<text x="24" y="38" font-size="16" font-weight="800" fill="#1a1a1a">{t["dash"]}</text>
<rect x="{W - 24 - 196}" y="18" width="196" height="30" rx="15" fill="#c8202f"/>
<text x="{W - 24 - 98}" y="38" text-anchor="middle" font-size="13.5" font-weight="700" fill="#fff">⚠ {t["alarm"]}</text>
<g font-size="13" fill="#1a1a1a"><line x1="24" y1="66" x2="46" y2="66" stroke="#8a8484" stroke-width="2.5"/><text x="52" y="71">{t["tout"]} °C</text>
<line x1="150" y1="66" x2="172" y2="66" stroke="#c8202f" stroke-width="3"/><text x="178" y="71">{t["tin"]} °C</text>
<rect x="290" y="58" width="22" height="14" fill="#c8202f" opacity=".14"/><text x="318" y="71">{t["band"]}</text></g>
<rect x="{bx0:.0f}" y="{gy0}" width="{bx1 - bx0:.0f}" height="{gy1 - gy0}" fill="#c8202f" opacity=".12"/>
<line x1="{gx0}" y1="{gy1}" x2="{gx1}" y2="{gy1}" stroke="#1a1a1a" stroke-width="1.2"/>
<polyline points="{po}" fill="none" stroke="#8a8484" stroke-width="2.5"/>
<polyline points="{pi_}" fill="none" stroke="#c8202f" stroke-width="3"/>{xt}
{kpi(24, t["k1"], "62 Pa")}{kpi(232, t["k2"], "38 dB(A)")}{kpi(440, t["k3"], "41" + dec + "5 kW")}
</svg>
"""


def beispiele(lang):
    t, c, r = EX[lang], CALC, calc()
    for nm, fn in (("lastgang", svg_lastgang), ("dashboard", svg_dashboard)):
        bn.write(f"img/iot/beispiel-{nm}-{lang}.svg", fn(lang))
    v = dict(V=fmt(c["V"], lang), dp=c["dp"], w_air=fmt(r["w_air"], lang), p_el=fmt(r["p_el"], lang, 2), h=fmt(c["h"], lang),
             P=c["P"], dT=c["dT"], pk=fmt(c["pk"], lang, 1), price=fmt(c["price"], lang, 2))
    def card(head, lines, e, eur):
        li = "".join(f"<li>{x.format(**v)}</li>" for x in lines)
        return (f'<div class="iot-calc"><h3>{head}</h3><ul class="check">{li}</ul>'
                f'<div class="iot-res"><b>≈ {fmt(round(e, -2), lang)}</b> {t["per"]}<br><b>≈ {fmt(round(eur, -1), lang)}</b> {t["eur"].format(**v)}</div></div>')
    return f"""<section class="alt" id="beispiele">
  <div class="wrap">
    <span class="kicker">{t["k"]}</span>
    <h2>{t["h"]}</h2>
    <div class="iot-ex">
      <figure><img src="/img/iot/beispiel-lastgang-{lang}.svg" width="640" height="330" alt="{t["c1"]}" loading="lazy"><figcaption>{t["c1"]}</figcaption></figure>
      <figure><img src="/img/iot/beispiel-dashboard-{lang}.svg" width="640" height="330" alt="{t["c2"]}" loading="lazy"><figcaption>{t["c2"]}</figcaption></figure>
    </div>
    <p class="note">{t["note"]}</p>
    <span class="kicker" style="margin-top:34px;display:inline-block">{t["rk"]}</span>
    <h2>{t["rh"]}</h2>
    <div class="iot-calcs">{card(t["r1h"], t["r1"], r["e1"], r["eur1"])}{card(t["r2h"], t["r2"], r["e2"], r["eur2"])}</div>
    <p class="note">{t["rnote"]}</p>
    <h3 class="iot-roi-h">{ROI[lang][0]}</h3>
    <div class="iot-roi">{"".join(f'<div><h4>{a}</h4><span class="tag">{b}</span><p>{c}</p></div>' for a, b, c in ROI[lang][1])}</div>
  </div>
</section>"""


def build():
    for lang in URL:
        t = TXT[lang]
        name = f"img/iot/lorawan-system-{lang}.svg"
        bn.write(name, svg(lang))
        frag = (ROOT / "iot" / "_src" / f"{lang}.html").read_text(encoding="utf-8")
        frag = icons(frag).replace("<!--BEISPIELE-->", beispiele(lang))
        main = f"""<div class="hero">
  <div class="wrap hg">
    <div>
      <span class="kicker">{t["kicker"]}</span>
      <h1>{t["h1"]}</h1>
      <p class="lead">{t["lead"]}</p>
      <div class="btns"><a class="btn" href="#anfrage" data-typ="iot">{t["b1"]}</a><a class="btn ghost" href="{TECH[lang]}">{t["b2"]}</a></div>
    </div>
    <figure class="dc-hero iot-hero"><img src="/{name}" width="920" height="540" alt="{t["alt"]}" fetchpriority="high"></figure>
  </div>
</div>
{frag}"""
        head = f'<script type="application/ld+json">{faq_ld(frag, lang)}</script>'
        bn.write(URL[lang][1:] + "index.html",
                 bn.page(lang, t["title"], t["desc"], dict(URL), main, extra_head=head, typ="iot"))
    print("IoT-Seiten gebaut (de, en, fr)")


if __name__ == "__main__":
    build()
