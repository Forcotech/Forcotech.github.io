#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Baut die Lösungsseiten und die HSA3-Seite (Deutsch und Englisch).

  Übersicht     /loesungen/                       /en/solutions/
  Lösungen      /loesungen/<slug>/                /en/solutions/<slug>/
  HSA3          /hsa3/                            /en/hsa3/

Inhalt ändern:
  - Kopf (Titel, Beschreibung, Einleitung, Bild, Kennzahlen, Konfigurator-Link): Tabelle PAGES unten
  - Hauptteil: Fragment loesungen/_src/<id>.<sprache>.html bzw. hsa3/_src/<sprache>.html
  danach  python3 tools/build_loesungen.py  und zum Schluss  python3 tools/build_news.py  (Navigation, Sitemap).

Die FAQ-Daten (schema.org FAQPage) werden aus den <details>-Fragen im Fragment erzeugt, dazu eine Brotkrumen-Navigation
(BreadcrumbList). Kopf, Navigation und Fuß kommen aus tools/build_news.py. Eine französische Fassung gibt es (noch) nicht.
"""
import html, json, re
from pathlib import Path
import build_news as bn

ROOT = Path(__file__).resolve().parent.parent
SITE = bn.SITE
LANGS = ("de", "en")
K = "https://www.forcotech.com/konfigurator/"
E = html.escape

UI = {
    "de": {"home": "/", "home_n": "Start", "sol": "/loesungen/", "sol_n": "Lösungen", "crumb": "Brotkrumen-Navigation",
           "rel_h": "Weitere Lösungen", "rel_more": "Zur Lösung →", "hsa3_more": "HSA3 im Detail →",
           "ask": "#anfrage", "ask_b": "Projekt anfragen",
           "hsa3_tag": "Material", "hsa3_h": "HSA3 – das Material in jeder Haube",
           "hsa3_p": "Meta-Akustik-Metall statt Mineralwolle, im Hallraum geprüft: faserfrei bis αₛ 0,80, mit Wollhinterlegung 0,83 schon bei 100 Hz. Nicht brennbar A1."},
    "en": {"home": "/en/", "home_n": "Home", "sol": "/en/solutions/", "sol_n": "Solutions", "crumb": "Breadcrumb",
           "rel_h": "More solutions", "rel_more": "View solution →", "hsa3_more": "HSA3 in detail →",
           "ask": "#anfrage", "ask_b": "Request a project",
           "hsa3_tag": "Material", "hsa3_h": "HSA3 – the material in every enclosure",
           "hsa3_p": "Acoustic meta-metal instead of mineral wool, reverberation room tested: fibre-free up to αₛ 0.80, with wool backing 0.83 already at 100 Hz. Non-combustible A1."},
}

TYP = {"waermepumpen": "wp", "vrf": "vrf", "grossanlagen": "gross", "wechselrichter": "pv", "schallwand": "wand"}  # Vorauswahl Anlagentyp im Formular

# Reihenfolge = Reihenfolge in Übersicht und „Weitere Lösungen“
PAGES = {
    "waermepumpen": {
        "url": {"de": "/loesungen/waermepumpen-klimaanlagen/", "en": "/en/solutions/heat-pumps-air-conditioning/"},
        "img": "/img/h-serie/h-serie-weiss-kaskade.webp", "w": 810, "h": 567,
        "cfg": {"de": K + "h-serie/", "en": K + "en/h-serie/"},
        "de": {"nav": "Wärmepumpen & Klimaanlagen", "tag": "H-Serie · Kleinanlagen",
               "title": "Schallschutz für Wärmepumpen und Klimaanlagen in Wohngebäuden – Schallhauben H-Serie | ForCoTech",
               "desc": "Wärmepumpe zu laut für den Nachbarn? Schallhauben der H-Serie für Wärmepumpen und Klimageräte im Ein- und Mehrfamilienhaus: −10, −18 oder −25 dB(A), R290-tauglich, Richtpreis sofort im Konfigurator.",
               "h1": "Wärmepumpen und Klimaanlagen leise machen – am Einfamilienhaus wie am Mehrfamilienhaus",
               "lead": "Die Außeneinheit läuft nachts, der Nachbar schläft zwei Meter entfernt. Unsere Schallhauben der H-Serie senken den Pegel um bis zu 25 dB(A) – ohne dass die Wärmepumpe an Leistung verliert.",
               "teaser": "Luft-Wasser-Wärmepumpen, Split- und Klimageräte, Poolwärmepumpen. Standardgrößen H1–H12 oder nach Maß, bis −25 dB(A).",
               "alt": "Mehrere weiße Schallhauben der H-Serie in einer Reihe vor einem Hotel im Schnee",
               "b1": "H-Serie konfigurieren – mit Richtpreis", "subj": "Schallhaube Wärmepumpe",
               "facts": [("bis −25 dB(A)", "drei Stufen: −10 / −18 / −25 dB(A)"), ("H1–H12", "Standardgrößen, auch als Doppelhaube"),
                         ("max. 4 m/s", "in allen Gittern – kein Leistungsverlust"), ("R290", "bodenoffene Bauweise für Propan-Geräte")]},
        "en": {"nav": "Heat pumps & air conditioning", "tag": "H-Series · small units",
               "title": "Noise control for heat pumps and air-conditioning units in residential buildings – H-Series enclosures | ForCoTech",
               "desc": "Heat pump too loud for the neighbours? H-Series acoustic enclosures for heat pumps and AC units in single and multi-family buildings: −10, −18 or −25 dB(A), R290-ready, guide price instantly in the configurator.",
               "h1": "Quiet heat pumps and air conditioning – in single and multi-family buildings",
               "lead": "The outdoor unit runs at night, the neighbour sleeps two metres away. Our H-Series enclosures cut the level by up to 25 dB(A) – without the heat pump losing capacity.",
               "teaser": "Air-to-water heat pumps, split and AC units, pool heat pumps. Standard sizes H1–H12 or custom-made, up to −25 dB(A).",
               "alt": "Several white H-Series acoustic enclosures in a row in front of a hotel in the snow",
               "b1": "Configure the H-Series – with guide price", "subj": "Acoustic enclosure heat pump",
               "facts": [("up to −25 dB(A)", "three levels: −10 / −18 / −25 dB(A)"), ("H1–H12", "standard sizes, also as double enclosure"),
                         ("max. 4 m/s", "in all grilles – no loss of capacity"), ("R290", "floorless design for propane units")]},
    },
    "vrf": {
        "url": {"de": "/loesungen/vrf-vrv/", "en": "/en/solutions/vrf-vrv/"},
        "img": "/img/dach-grosshaube-braun.webp", "w": 1178, "h": 733,
        "cfg": {"de": K + "vrf/", "en": K + "en/vrf/"},
        "de": {"nav": "VRF/VRV-Anlagen", "tag": "V-Serie · Standardprodukt",
               "title": "Schallhauben für VRF/VRV-Außengeräte – Daikin, Mitsubishi Electric, Panasonic, LG u. a. | ForCoTech",
               "desc": "Standard-Schallhauben passend zum VRF/VRV-Außengerät: Daikin, Mitsubishi Electric, Panasonic, LG, Samsung, Toshiba, Haier. Ca. −15 bzw. −20 dB(A), Listenpreise im Katalog, auch für Modulkombinationen.",
               "h1": "Schallhauben für VRF/VRV-Außengeräte – passend zum Gerätemodell",
               "lead": "VRF-Systeme stehen oft auf dem Dach von Büros, Hotels und Praxen – mitten zwischen Fenstern. Unsere V-Serie gibt es als Standardhaube zum jeweiligen Außengerät, mit Maßen und Listenpreis direkt im Katalog.",
               "teaser": "Standardhauben nach Gerätemodell für Daikin, Mitsubishi Electric, Panasonic, LG, Samsung, Toshiba und Haier – mit Listenpreis.",
               "alt": "Lange Schallhaube in Braun mit Wartungstüren auf einem Bürodach",
               "b1": "Haube zum Gerätemodell wählen", "subj": "Schallhaube VRF/VRV",
               "facts": [("ca. −15 / −20 dB(A)", "Standard / Premium"), ("7 Hersteller", "Hauben nach Modellnummer"),
                         ("ab ca. 15.500 €", "netto, Listenpreis im Katalog"), ("auch kombiniert", "Haube für Modulkombinationen")]},
        "en": {"nav": "VRF/VRV systems", "tag": "V-Series · standard product",
               "title": "Acoustic enclosures for VRF/VRV outdoor units – Daikin, Mitsubishi Electric, Panasonic, LG and more | ForCoTech",
               "desc": "Standard acoustic enclosures matched to the VRF/VRV outdoor unit: Daikin, Mitsubishi Electric, Panasonic, LG, Samsung, Toshiba, Haier. Approx. −15 or −20 dB(A), list prices in the catalogue, also for module combinations.",
               "h1": "Acoustic enclosures for VRF/VRV outdoor units – matched to the model",
               "lead": "VRF systems often sit on the roofs of offices, hotels and clinics – right between windows. Our V-Series comes as a standard enclosure for each outdoor unit, with dimensions and a list price straight from the catalogue.",
               "teaser": "Standard enclosures by model for Daikin, Mitsubishi Electric, Panasonic, LG, Samsung, Toshiba and Haier – at list prices.",
               "alt": "Long brown acoustic enclosure with service doors on an office roof",
               "b1": "Choose the enclosure for your model", "subj": "Acoustic enclosure VRF/VRV",
               "facts": [("approx. −15 / −20 dB(A)", "Standard / Premium"), ("7 manufacturers", "enclosures by model number"),
                         ("from approx. €15,500", "net, fixed catalogue price"), ("combinations", "one enclosure for module combinations")]},
    },
    "grossanlagen": {
        "url": {"de": "/loesungen/chiller-grosswaermepumpen/", "en": "/en/solutions/chillers-large-heat-pumps/"},
        "img": "/img/loesungen/grosswaermepumpe-dach-edelstahl.webp", "w": 1400, "h": 706,
        "cfg": {"de": K + "grossanlagen/", "en": K + "en/grossanlagen/"},
        "de": {"nav": "Chiller & Groß-Wärmepumpen", "tag": "CM-Serie · Großanlagen",
               "title": "Schallschutz für Kaltwassersätze, Rückkühler und Großwärmepumpen – CM-Serie | ForCoTech",
               "desc": "Schallhauben für Chiller, Rückkühler und Großwärmepumpen, einzeln oder als gemeinsame Haube für Kaskaden: Akustik nach TA Lärm und Luftführung per CFD, HSA3 nicht brennbar A1, Druckverlust innerhalb der Gerätereserve.",
               "h1": "Kaltwassersätze und Großwärmepumpen einhausen – ohne Kälte- oder Heizleistung zu verlieren",
               "lead": "Ab 100 kW wird Schallschutz zur Strömungsaufgabe: Hunderttausend Kubikmeter Luft pro Stunde müssen durch die Haube, der Ventilator hat nur wenige Pascal Reserve. Wir legen Akustik und Luftführung gemeinsam aus – für eine Anlage oder die ganze Kaskade.",
               "teaser": "Chiller, Rückkühler, Großwärmepumpen und Kaskaden. Akustik und Strömung gemeinsam ausgelegt, A1 nicht brennbar.",
               "alt": "Große Schallhaube aus Aluminium-Paneelen mit Lüftungsgittern für eine Großwärmepumpe auf einem begrünten Dach, mit Rohrleitungen",
               "b1": "Katalog Großanlagen – Richtpreis", "subj": "Schallhaube Grossanlage",
               "facts": [("ca. −15 / −20 dB(A)", "Standard / Premium, projektbezogen mehr"), ("1 bis viele Geräte", "gemeinsame Haube für Kaskaden"),
                         ("bis −40 % Druckverlust", "HSA3 statt klassischer Kulissen"), ("max. 3–5 %", "Leistungseinbuße als Auslegungsziel")]},
        "en": {"nav": "Chillers & large heat pumps", "tag": "CM-Series · large units",
               "title": "Noise control for chillers, dry coolers and large heat pumps – CM-Series | ForCoTech",
               "desc": "Acoustic enclosures for chillers, dry coolers and large heat pumps, individually or as one enclosure for a cascade: acoustics to TA Lärm, air flow by CFD, HSA3 non-combustible A1, pressure drop within the unit's reserve.",
               "h1": "Enclosing chillers and large heat pumps – without losing cooling or heating capacity",
               "lead": "Above 100 kW, noise control becomes an air-flow task: a hundred thousand cubic metres of air per hour must pass through the enclosure, and the fan has only a few pascals in reserve. We engineer acoustics and air flow together – for one unit or the whole cascade.",
               "teaser": "Chillers, dry coolers, large heat pumps and cascades. Acoustics and air flow engineered together, A1 non-combustible.",
               "alt": "Large aluminium-panel acoustic enclosure with ventilation grilles for a large heat pump on a green roof, with pipework",
               "b1": "Large-equipment catalogue – guide price", "subj": "Acoustic enclosure large unit",
               "facts": [("approx. −15 / −20 dB(A)", "Standard / Premium, more per project"), ("1 to many units", "one enclosure for cascades"),
                         ("up to −40 % pressure drop", "HSA3 instead of classic splitters"), ("max. 3–5 %", "capacity loss as design target")]},
    },
    "wechselrichter": {
        "url": {"de": "/loesungen/wechselrichter-bess/", "en": "/en/solutions/inverters-bess/"},
        "img": "/img/loesungen/wechselrichter-haube.svg", "img_en": "/img/loesungen/wechselrichter-haube-en.svg", "w": 800, "h": 520,
        "cfg": {"de": K + "pv/", "en": K + "en/pv/"},
        "de": {"nav": "Wechselrichter & BESS", "tag": "PV · Batteriespeicher",
               "title": "Schallschutz für PV-Wechselrichter und Batteriespeicher (BESS) – Schallhauben | ForCoTech",
               "desc": "Wechselrichter pfeift, Batteriespeicher brummt? Schallhauben für PV-Wechselrichter (Huawei, SMA, Fronius, Sungrow u. a.) als Vorbau oder freistehend für 1–5 Geräte, dazu Wechselrichter-Einhausungen und Lärmschutz für Batteriespeicher (BESS) – HSA3 nicht brennbar A1.",
               "h1": "PV-Wechselrichter und Batteriespeicher leise machen – und vor Hitze schützen",
               "lead": "Bis zu 20 dB(A) leiser – ohne Hitzestau und mit nicht brennbarem Material. Unsere Hauben dämpfen das hohe Pfeifen der Wechselrichter und das Dauerrauschen der Speicherkühlung und schützen die Geräte zugleich vor Sonne, Regen und Hagel.",
               "teaser": "Vorbau- und freistehende Hauben für 1–5 Wechselrichter, Einhausungen für BESS. Ausgelegt auf 16–18 kHz, A1 nicht brennbar.",
               "alt": "Schematische Darstellung: Vorbau-Schallhaube vor einem Wechselrichter an der Wand mit Zuluft unten und Abluft oben",
               "b1": "Haube wählen – Listenpreis sofort", "subj": "Schallhaube Wechselrichter/BESS",
               "facts": [("16–18 kHz", "typische Pegelspitzen – gezielt gedämpft"), ("1 bis 5 Geräte", "Wandmontage oder freistehend"),
                         ("ab ca. 4.400 €", "netto, Listenpreis im Katalog"), ("A1", "nicht brennbar – wichtig am Batteriespeicher")]},
        "en": {"nav": "Inverters & BESS", "tag": "PV · battery storage",
               "title": "Noise control for PV inverters and battery storage (BESS) – acoustic enclosures | ForCoTech",
               "desc": "Inverter whining, battery storage humming? Acoustic enclosures for PV inverters (Huawei, SMA, Fronius, Sungrow and more), wall-mounted or free-standing for 1–5 units, plus enclosures for BESS – HSA3 non-combustible A1.",
               "h1": "Quiet PV inverters and battery storage – and protect them from heat",
               "lead": "Up to 20 dB(A) quieter – without heat build-up and with non-combustible material. Our enclosures damp the high whine of inverters and the constant noise of battery storage cooling, and protect the units from sun, rain and hail at the same time.",
               "teaser": "Wall-mounted and free-standing enclosures for 1–5 inverters, enclosures for BESS. Designed for 16–18 kHz, A1 non-combustible.",
               "alt": "Schematic: wall-mounted acoustic enclosure in front of an inverter with air inlet at the bottom and outlet at the top",
               "b1": "Choose an enclosure – list price instantly", "subj": "Acoustic enclosure inverter/BESS",
               "facts": [("16–18 kHz", "typical peaks – damped specifically"), ("1 to 5 units", "wall-mounted or free-standing"),
                         ("from approx. €4,400", "net, catalogue list price"), ("A1", "non-combustible – key at battery storage")]},
    },
    "schallwand": {
        "url": {"de": "/loesungen/schallwaende/", "en": "/en/solutions/noise-barriers/"},
        "img": "/img/loesungen/schallwand-prinzip.svg", "img_en": "/img/loesungen/schallwand-prinzip-en.svg", "w": 800, "h": 520,
        "cfg": {"de": K + "schallwand/", "en": K + "en/schallwand/"},
        "de": {"nav": "Schallwände", "tag": "Wall-Serie",
               "title": "Schallschutzwände für Wärmepumpen, Kälte- und Klimaanlagen – Wall-Serie mit HSA3 | ForCoTech",
               "desc": "Schallschutzwand statt Einhausung: gerade, Winkel, U-Form oder frei konfigurierbar, mit HSA3-Absorber. Abschirmung nach DIN ISO 9613-2, empfohlene Wandhöhe und Windlast sofort im Konfigurator.",
               "h1": "Schallschutzwände für Anlagen im Freien – wenn eine Haube nicht passt",
               "lead": "Kein Platz für eine Haube, Wartung von allen Seiten nötig oder nur ein Nachbar betroffen? Dann ist eine absorbierende Schallwand oft die einfachere Lösung. Oft reichen schon 6 bis 10 dB(A), um die Richtwerte einzuhalten.",
               "teaser": "Gerade, Winkel, U-Form oder frei geplant, mit HSA3-Absorber. Abschirmung, Wandhöhe und Windlast sofort im Konfigurator.",
               "alt": "Schematische Darstellung: Schallwand zwischen Anlage und Nachbarhaus, Schall wird an der Wandkante gebeugt",
               "b1": "Schallwand konfigurieren", "subj": "Schallschutzwand",
               "facts": [("6–10 dB(A)", "typische Minderung, je nach Geometrie"), ("frei planbar", "gerade, Winkel, U-Form, Polygonzug"),
                         ("absorbierend", "HSA3 statt reflektierender Platten"), ("Windlast", "nach DIN EN 1991-1-4 bemessen")]},
        "en": {"nav": "Noise barriers", "tag": "Wall-Series",
               "title": "Noise barriers for heat pumps, chillers and AC units – Wall-Series with HSA3 | ForCoTech",
               "desc": "Noise barrier instead of an enclosure: straight, L-shaped, U-shaped or freely configured, with HSA3 absorber. Screening to ISO 9613-2, recommended wall height and wind load instantly in the configurator.",
               "h1": "Noise barriers for outdoor equipment – when an enclosure does not fit",
               "lead": "No room for an enclosure, access needed from all sides or only one neighbour affected? Then an absorbing noise barrier is often the simpler solution. 6 to 10 dB(A) is often enough to meet the limits.",
               "teaser": "Straight, L-shaped, U-shaped or freely planned, with HSA3 absorber. Screening, wall height and wind load instantly.",
               "alt": "Schematic: noise barrier between the unit and the neighbouring house, sound diffracted at the top edge",
               "b1": "Configure a noise barrier", "subj": "Noise barrier",
               "facts": [("6–10 dB(A)", "typical reduction, depending on geometry"), ("freely planned", "straight, L, U, polyline"),
                         ("absorbing", "HSA3 instead of reflective panels"), ("wind load", "designed to EN 1991-1-4")]},
    },
}

HSA3 = {
    "url": {"de": "/hsa3/", "en": "/en/hsa3/"},
    "img": "/img/loesungen/hsa3-aufbau.svg", "img_en": "/img/loesungen/hsa3-aufbau-en.svg", "w": 800, "h": 460,
    "de": {"nav": "HSA3", "title": "HSA3 – Meta-Akustik-Metall für Schallhauben: Aufbau, Wirkung, Kennwerte | ForCoTech",
           "desc": "HSA3 von ABSORA: mikroperforiertes, gewelltes Metall mit Resonanzkammern statt Mineralwolle. Bis −40 % Druckverlust, im Hallraum nach DIN EN ISO 354 geprüft (faserfrei bis 0,80, mit Wollhinterlegung 0,83 schon bei 100 Hz), nicht brennbar A1, witterungsfest.",
           "kicker": "Technologie · Engineered with Absora Technology",
           "h1": "HSA3 – Schallabsorption aus Metall, ohne Mineralwolle",
           "lead": "Das Herz jeder ForCoTech-Haube: ein patentiertes Meta-Akustik-Metall der ABSORA GmbH, Berlin. Es dämpft gerade die tiefen Töne von Verdichtern und Ventilatoren, ist nicht brennbar und hält Wind und Wetter dauerhaft stand.",
           "alt": "Schematischer Schnitt durch HSA3: gewellte mikroperforierte Deckschicht, Luftkammern, federnd gelagerte Zwischenlage, Resonanzhohlraum und Trägerplatte",
           "b1": "Haube mit HSA3 konfigurieren", "b2": "Prüfbericht anfordern", "subj": "Pr%C3%BCfbericht%20HSA3",
           "facts": [("bis −40 %", "Druckverlust gegenüber Kulissenschalldämpfern"), ("αₛ 0,83", "schon bei 100 Hz, mit Wollhinterlegung – DIN EN ISO 354"),
                     ("A1", "nicht brennbar nach EN 13501-1"), ("0 Fasern", "keine Mineralwolle, kein Schaum")]},
    "en": {"nav": "HSA3", "title": "HSA3 – acoustic meta-metal for enclosures: structure, effect, key data | ForCoTech",
           "desc": "HSA3 by ABSORA: micro-perforated, corrugated metal with resonance chambers instead of mineral wool. Up to −40 % pressure drop, reverberation room tested to EN ISO 354 (fibre-free up to 0.80, with wool backing 0.83 already at 100 Hz), non-combustible A1, weatherproof.",
           "kicker": "Technology · Engineered with Absora Technology",
           "h1": "HSA3 – sound absorption made of metal, without mineral wool",
           "lead": "The heart of every ForCoTech enclosure: a patented acoustic meta-metal by ABSORA GmbH, Berlin. It damps precisely the low tones of compressors and fans, is non-combustible and withstands wind and weather for good.",
           "alt": "Schematic section through HSA3: corrugated micro-perforated face layer, air chambers, spring-mounted intermediate layer, resonance cavity and carrier plate",
           "b1": "Configure an enclosure with HSA3", "b2": "Request the test report", "subj": "HSA3%20test%20report",
           "facts": [("up to −40 %", "pressure drop vs. splitter silencers"), ("αₛ 0.83", "already at 100 Hz, with wool backing – EN ISO 354"),
                     ("A1", "non-combustible to EN 13501-1"), ("0 fibres", "no mineral wool, no foam")]},
}

OVERVIEW = {
    "de": {"title": "Lösungen – Schallschutz für Wärmepumpen, VRF, Chiller, Wechselrichter, BESS und Schallwände | ForCoTech",
           "desc": "Schallhauben und Schallwände nach Anwendung: Wärmepumpen und Klimaanlagen, VRF/VRV, Kaltwassersätze und Großwärmepumpen, PV-Wechselrichter und Batteriespeicher – jeweils direkt mit dem passenden Konfigurator verknüpft.",
           "kicker": "Lösungen", "h1": "Schallschutz nach Anwendung",
           "lead": "Jede Anlage klingt anders – ein Verdichter brummt, ein Wechselrichter pfeift, ein Chiller rauscht mit 300.000 m³/h. Wählen Sie Ihre Anwendung: Sie finden die passende Bauweise und kommen direkt in den richtigen Teil des Konfigurators."},
    "en": {"title": "Solutions – noise control for heat pumps, VRF, chillers, inverters, BESS and noise barriers | ForCoTech",
           "desc": "Acoustic enclosures and noise barriers by application: heat pumps and AC, VRF/VRV, chillers and large heat pumps, PV inverters and battery storage – each linked straight to the matching configurator.",
           "kicker": "Solutions", "h1": "Noise control by application",
           "lead": "Every unit sounds different – a compressor hums, an inverter whines, a chiller roars with 300,000 m³/h. Choose your application: you will find the right construction and go straight to the matching part of the configurator."},
}


def pic(p, lang):
    return p.get("img_" + lang, p["img"])


def faq_ld(frag, lang):
    qa = re.findall(r"<details><summary>(.*?)</summary><p>(.*?)</p></details>", frag, re.S)
    if not qa:
        return ""
    strip = lambda s: html.unescape(re.sub(r"<[^>]+>", "", s)).strip()
    return json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "inLanguage": lang,
                       "mainEntity": [{"@type": "Question", "name": strip(q),
                                       "acceptedAnswer": {"@type": "Answer", "text": strip(a)}} for q, a in qa]},
                      ensure_ascii=False)


def crumbs(lang, items):
    """items: [(Name, Pfad)], letzter Eintrag = aktuelle Seite."""
    u = UI[lang]
    full = [(u["home_n"], u["home"])] + items
    ld = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                     "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + p}
                                         for i, (n, p) in enumerate(full)]}, ensure_ascii=False)
    links = " <span aria-hidden=\"true\">›</span> ".join(
        f'<a href="{p}">{E(n)}</a>' if i < len(full) - 1 else f'<span aria-current="page">{E(n)}</span>'
        for i, (n, p) in enumerate(full))
    return f'<nav class="crumbs" aria-label="{u["crumb"]}">{links}</nav>', f'<script type="application/ld+json">{ld}</script>'


def hero(lang, kicker, h1, lead, b1, b1_url, b2, b2_url, img, w, h, alt, facts, crumb_html):
    f = "\n      ".join(f"<div><b>{E(b)}</b><span>{E(s)}</span></div>" for b, s in facts)
    return f"""<div class="hero sol-hero">
  <div class="wrap">{crumb_html}</div>
  <div class="wrap hg">
    <div>
      <span class="kicker">{E(kicker)}</span>
      <h1>{E(h1)}</h1>
      <p class="lead">{E(lead)}</p>
      <div class="btns"><a class="btn" href="{b1_url}">{E(b1)}</a><a class="btn ghost" href="{b2_url}">{E(b2)}</a></div>
    </div>
    <figure><img src="{img}" width="{w}" height="{h}" alt="{E(alt)}" fetchpriority="high"></figure>
  </div>
  <div class="wrap">
    <div class="facts">
      {f}
    </div>
  </div>
</div>"""


def related(lang, skip):
    u = UI[lang]
    cards = []
    for pid, p in PAGES.items():
        if pid == skip:
            continue
        t = p[lang]
        cards.append(f'<a class="solcard" href="{p["url"][lang]}"><img src="{pic(p, lang)}" width="{p["w"]}" height="{p["h"]}" alt="" loading="lazy">'
                     f'<span class="tag">{E(t["tag"])}</span><h3>{E(t["nav"])}</h3><p>{E(t["teaser"])}</p><span class="more">{u["rel_more"]}</span></a>')
    if skip != "hsa3":
        cards.append(f'<a class="solcard" href="{HSA3["url"][lang]}"><img src="{pic(HSA3, lang)}" width="{HSA3["w"]}" height="{HSA3["h"]}" alt="" loading="lazy">'
                     f'<span class="tag">{u["hsa3_tag"]}</span><h3>{u["hsa3_h"]}</h3><p>{u["hsa3_p"]}</p><span class="more">{u["hsa3_more"]}</span></a>')
    return f"""<section class="alt sol-rel">
  <div class="wrap">
    <h2>{u["rel_h"]}</h2>
    <div class="solgrid">
      {chr(10).join(cards)}
    </div>
  </div>
</section>"""


def build():
    for lang in LANGS:
        u = UI[lang]
        sol_alts = {k: UI[k]["sol"] for k in LANGS}
        # Lösungsseiten
        for pid, p in PAGES.items():
            t = p[lang]
            frag = (ROOT / "loesungen" / "_src" / f"{pid}.{lang}.html").read_text(encoding="utf-8")
            ch, cl = crumbs(lang, [(u["sol_n"], u["sol"]), (t["nav"], p["url"][lang])])
            main = hero(lang, t["tag"], t["h1"], t["lead"], t["b1"], p["cfg"][lang], u["ask_b"],
                        u["ask"],
                        pic(p, lang), p["w"], p["h"], t["alt"], t["facts"], ch) + "\n" + frag + "\n" + related(lang, pid)
            fl = faq_ld(frag, lang)
            head = cl + (f'\n<script type="application/ld+json">{fl}</script>' if fl else "")
            bn.write(p["url"][lang][1:] + "index.html",
                     bn.page(lang, t["title"], t["desc"], dict(p["url"]), main, extra_head=head, typ=TYP.get(pid)))
        # HSA3
        t = HSA3[lang]
        frag = (ROOT / "hsa3" / "_src" / f"{lang}.html").read_text(encoding="utf-8")
        ch, cl = crumbs(lang, [(t["nav"], HSA3["url"][lang])])
        cfg = K if lang == "de" else K + "en/"
        main = hero(lang, t["kicker"], t["h1"], t["lead"], t["b1"], cfg, t["b2"], u["ask"],
                    pic(HSA3, lang), HSA3["w"], HSA3["h"], t["alt"], t["facts"], ch) + "\n" + frag + "\n" + related(lang, "hsa3")
        fl = faq_ld(frag, lang)
        head = cl + (f'\n<script type="application/ld+json">{fl}</script>' if fl else "")
        bn.write(HSA3["url"][lang][1:] + "index.html", bn.page(lang, t["title"], t["desc"], dict(HSA3["url"]), main, extra_head=head))
        # Übersicht
        o = OVERVIEW[lang]
        ch, cl = crumbs(lang, [(u["sol_n"], u["sol"])])
        cards = []
        for pid, p in PAGES.items():
            pt = p[lang]
            cards.append(f'<a class="solcard" href="{p["url"][lang]}"><img src="{pic(p, lang)}" width="{p["w"]}" height="{p["h"]}" alt="{E(pt["alt"])}" loading="lazy">'
                         f'<span class="tag">{E(pt["tag"])}</span><h2>{E(pt["nav"])}</h2><p>{E(pt["teaser"])}</p><span class="more">{u["rel_more"]}</span></a>')
        cards.append(f'<a class="solcard" href="{HSA3["url"][lang]}"><img src="{pic(HSA3, lang)}" width="{HSA3["w"]}" height="{HSA3["h"]}" alt="{E(HSA3[lang]["alt"])}" loading="lazy">'
                     f'<span class="tag">{u["hsa3_tag"]}</span><h2>{u["hsa3_h"]}</h2><p>{u["hsa3_p"]}</p><span class="more">{u["hsa3_more"]}</span></a>')
        ofrag = (ROOT / "loesungen" / "_src" / f"uebersicht.{lang}.html").read_text(encoding="utf-8")
        main = f"""<section class="nlist">
  <div class="wrap">
    {ch}
    <span class="kicker">{o["kicker"]}</span>
    <h1 class="nh">{E(o["h1"])}</h1>
    <p class="sub">{E(o["lead"])}</p>
    <div class="solgrid">
      {chr(10).join(cards)}
    </div>
  </div>
</section>
{ofrag}"""
        bn.write(u["sol"][1:] + "index.html", bn.page(lang, o["title"], o["desc"], sol_alts, main, extra_head=cl))
    print("Lösungsseiten, Übersicht und HSA3-Seite gebaut (DE/EN)")


if __name__ == "__main__":
    build()
