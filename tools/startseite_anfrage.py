#!/usr/bin/env python3
"""Startseiten DE/EN/FR/IT/ES: Claim im Kopf und Anfrageformular im Kontaktbereich.

Ersetzt die <h1>/Lead-Zeile im Hero und den Inhalt von <section id="kontakt|contact">.
Wiederholbar (erkennt die eigenen Marker). Logik des Formulars: anfrage.js, Gestaltung: style.css.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

L = {
 "index.html": dict(
  typ_l="Anlagentyp", typ_o='<option value="">bitte wählen</option><option value="wp">Wärmepumpe / Klimagerät</option><option value="gross">Kaltwassersatz / Großwärmepumpe / Rückkühler</option><option value="vrf">VRF/VRV-Außengerät</option><option value="pv">PV-Wechselrichter</option><option value="bess">Batteriespeicher (BESS)</option><option value="dc">Rechenzentrum</option><option value="wand">Schallwand</option><option value="iot">IoT-Monitoring / Sensorik</option><option value="sonst">Sonstiges</option>',
  sec="kontakt",
  claim="<span>Ruhe für die Nachbarn.</span><em>Leistung für die Anlage.</em>",
  what="Schallhauben für Wärmepumpen und HVAC-Anlagen",
  lead="<b>Erst der Nachweis, dann die Haube.</b> Für Wärmepumpen, Kälteanlagen, VRF, PV-Wechselrichter und BESS berechnen wir den Pegel am Immissionsort vorab und legen Akustik und Luftführung gemeinsam aus – gefertigt mit Absora-Technologie.",
  nx_h="So geht es weiter", nx="<li><b>Prüfung</b> Ihrer Angaben – bei Bedarf kurze Rückfrage</li><li><b>Pegelberechnung</b> am Immissionsort und Auslegung von Akustik und Luftführung</li><li><b>Verbindliches Angebot</b> mit Zeichnung – bei komplexen Projekten meist in 2–3 Tagen</li>",
  h2="Projekt anfragen",
  intro="Gerät, Anzahl und Aufstellort genügen für den Anfang – mit Datenblatt prüfen wir Maße, Luftmenge und Schallleistung direkt. Ein verbindliches Angebot für komplexe Projekte erhalten Sie in der Regel in 2–3 Tagen.",
  name="Name *", company="Firma", email="E-Mail *", phone="Telefon", place="Projektort (PLZ / Ort)",
  unit="Anlage (Hersteller / Modell)", unit_ph="z. B. York YMAE0260", count="Anzahl Geräte",
  msg="Nachricht", msg_ph="z. B. Richtwert nachts, Abstand zum Nachbarn, Dachaufstellung, Termin …",
  file="Datenblatt, Plan oder Foto (optional · PDF oder Bild, max. 10 MB)",
  privacy_sum="Datenschutzhinweise zu dieser Anfrage",
  privacy=("<p><b>Verantwortlicher:</b> Silent Engineering di Romolo Vicari (Marke ForCoTech), Via Trento 22, 23875 Osnago (LC), Italien · <a href=\"mailto:info@forcotech.com\">info@forcotech.com</a></p>"
           "<p><b>Zweck:</b> Ihre Angaben und ein ggf. beigefügtes Datenblatt verwenden wir ausschließlich zur Bearbeitung Ihrer Anfrage und zur Erstellung eines Angebots. Soweit dafür nötig, geben wir die technischen Projektangaben an unseren Fertigungspartner weiter; keine Weitergabe zu Werbezwecken.</p>"
           "<p><b>Versand:</b> über den Formulardienst FormSubmit (formsubmit.co), der die Anfrage per E-Mail an info@forcotech.com weiterleitet; dabei ist eine Verarbeitung außerhalb der EU möglich. Rechtsgrundlage: Art. 6 Abs. 1 lit. b DSGVO sowie Ihre Einwilligung (Art. 6 Abs. 1 lit. a, Art. 49 Abs. 1 lit. a DSGVO), jederzeit widerruflich. Alternativ erreichen Sie uns direkt per E-Mail.</p>"
           "<p><b>Speicherdauer und Rechte:</b> Löschung nach Abschluss der Anfrage, bei Vertrag nach den gesetzlichen Fristen. Auskunft, Berichtigung, Löschung, Widerspruch und Widerruf formlos an info@forcotech.com. Mehr in der <a href=\"/datenschutz/\">Datenschutzerklärung</a>.</p>"),
  consent="Ich bin einverstanden, dass meine Angaben zur Bearbeitung der Anfrage gespeichert und verarbeitet und dafür über FormSubmit übermittelt werden (siehe <a href=\"/datenschutz/\">Datenschutzerklärung</a>). Die Einwilligung kann ich jederzeit widerrufen. *",
  send="Anfrage senden",
  thanks="<b>Vielen Dank für Ihre Anfrage!</b><br>Wir melden uns in der Regel innerhalb von 2–3 Werktagen.",
  copy="Text kopieren", mailbtn="Im E-Mail-Programm öffnen",
  side="Lieber selbst vordimensionieren?", cfg_url="https://www.forcotech.com/konfigurator/", cfg="Zum Konfigurator",
  addr="<b>Silent Engineering di Romolo Vicari</b><br>Marken ForCoTech und Silent-Mode<br>Via Trento 22 · 23875 Osnago (LC) · Italien<br>E-Mail: <a href=\"mailto:info@forcotech.com\">info@forcotech.com</a><br>Web: <a href=\"https://www.silent-mode.com\">silent-mode.com</a>",
 ),
 "en/index.html": dict(
  typ_l="Equipment type", typ_o='<option value="">please select</option><option value="wp">Heat pump / AC unit</option><option value="gross">Chiller / large heat pump / dry cooler</option><option value="vrf">VRF/VRV outdoor unit</option><option value="pv">PV inverter</option><option value="bess">Battery storage (BESS)</option><option value="dc">Data centre</option><option value="wand">Noise barrier</option><option value="iot">IoT monitoring / sensors</option><option value="sonst">Other</option>',
  sec="contact",
  claim="<span>Quiet for the neighbours.</span><em>Performance for the unit.</em>",
  what="Acoustic enclosures for heat pumps and HVAC systems",
  lead="<b>Proof first, then the enclosure.</b> For heat pumps, chillers, VRF, PV inverters and BESS we calculate the level at the receiver in advance and design acoustics and airflow together – built with Absora technology.",
  nx_h="What happens next", nx="<li><b>Review</b> of your details – with a short follow-up question if needed</li><li><b>Level calculation</b> at the receiver and design of acoustics and airflow</li><li><b>Binding quotation</b> with drawing – usually within 2–3 days for complex projects</li>",
  h2="Start your project",
  intro="Unit, quantity and location are enough to start – with a data sheet we can check dimensions, air volume and sound power straight away. For complex projects you will usually receive a binding quotation within 2–3 days.",
  name="Name *", company="Company", email="E-mail *", phone="Phone", place="Project location (postcode / town)",
  unit="Unit (manufacturer / model)", unit_ph="e.g. York YMAE0260", count="Number of units",
  msg="Message", msg_ph="e.g. night-time limit, distance to neighbours, rooftop installation, schedule …",
  file="Data sheet, drawing or photo (optional · PDF or image, max. 10 MB)",
  privacy_sum="Privacy information for this enquiry",
  privacy=("<p><b>Controller:</b> Silent Engineering di Romolo Vicari (brand ForCoTech), Via Trento 22, 23875 Osnago (LC), Italy · <a href=\"mailto:info@forcotech.com\">info@forcotech.com</a></p>"
           "<p><b>Purpose:</b> we use your details and any attached data sheet solely to handle your enquiry and prepare a quotation. Where necessary, we pass the technical project data to our manufacturing partner; no disclosure for advertising.</p>"
           "<p><b>Transmission:</b> via the form service FormSubmit (formsubmit.co), which forwards the enquiry by e-mail to info@forcotech.com; processing outside the EU is possible. Legal basis: Art. 6(1)(b) GDPR and your consent (Art. 6(1)(a), Art. 49(1)(a) GDPR), revocable at any time. Alternatively, contact us directly by e-mail.</p>"
           "<p><b>Retention and rights:</b> deletion once the enquiry is closed, or after the statutory periods if a contract is concluded. Access, rectification, erasure, objection and withdrawal informally to info@forcotech.com. More in the <a href=\"/en/privacy/\">privacy policy</a>.</p>"),
  consent="I agree that my details are stored and processed to handle the enquiry and transmitted for this purpose via FormSubmit (see <a href=\"/en/privacy/\">privacy policy</a>). I can withdraw my consent at any time. *",
  send="Send enquiry",
  thanks="<b>Thank you for your enquiry!</b><br>We usually get back to you within 2–3 working days.",
  copy="Copy text", mailbtn="Open in e-mail program",
  side="Prefer to size it yourself?", cfg_url="https://www.forcotech.com/konfigurator/en/", cfg="Open the configurator",
  addr="<b>Silent Engineering di Romolo Vicari</b><br>Brands ForCoTech and Silent-Mode<br>Via Trento 22 · 23875 Osnago (LC) · Italy<br>Email: <a href=\"mailto:info@forcotech.com\">info@forcotech.com</a><br>Web: <a href=\"https://www.silent-mode.com\">silent-mode.com</a>",
 ),
 "fr/index.html": dict(
  typ_l="Type d’installation", typ_o='<option value="">veuillez choisir</option><option value="wp">Pompe à chaleur / climatiseur</option><option value="gross">Groupe froid / grande PAC / aéroréfrigérant</option><option value="vrf">Unité extérieure VRF/VRV</option><option value="pv">Onduleur PV</option><option value="bess">Stockage par batteries (BESS)</option><option value="dc">Centre de données</option><option value="wand">Écran acoustique</option><option value="iot">Monitoring IoT / capteurs</option><option value="sonst">Autre</option>',
  sec="contact",
  claim="<span>Le calme pour les voisins.</span><em>La performance pour l’appareil.</em>",
  what="Caissons acoustiques pour pompes à chaleur et installations CVC",
  lead="<b>D’abord la preuve, ensuite le caisson.</b> Pour pompes à chaleur, groupes froids, VRF, onduleurs PV et BESS, nous calculons à l’avance le niveau au point de réception et concevons ensemble acoustique et flux d’air – fabriqués avec la technologie Absora.",
  nx_h="Et ensuite ?", nx="<li><b>Vérification</b> de vos données – avec une courte question si nécessaire</li><li><b>Calcul du niveau</b> au point de réception et conception acoustique et aéraulique</li><li><b>Offre ferme</b> avec plan – en général sous 2 à 3 jours pour les projets complexes</li>",
  h2="Lancer votre projet",
  intro="L’appareil, le nombre et le lieu d’implantation suffisent pour commencer – avec la fiche technique, nous vérifions directement dimensions, débit d’air et puissance acoustique. Pour les projets complexes, vous recevez en général une offre ferme sous 2 à 3 jours.",
  name="Nom *", company="Société", email="E-mail *", phone="Téléphone", place="Lieu du projet (code postal / ville)",
  unit="Appareil (fabricant / modèle)", unit_ph="p. ex. York YMAE0260", count="Nombre d’appareils",
  msg="Message", msg_ph="p. ex. limite de nuit, distance aux voisins, installation en toiture, délai …",
  file="Fiche technique, plan ou photo (facultatif · PDF ou image, max. 10 Mo)",
  privacy_sum="Informations sur la protection des données",
  privacy=("<p><b>Responsable :</b> Silent Engineering di Romolo Vicari (marque ForCoTech), Via Trento 22, 23875 Osnago (LC), Italie · <a href=\"mailto:info@forcotech.com\">info@forcotech.com</a></p>"
           "<p><b>Finalité :</b> vos données et une éventuelle fiche technique servent uniquement au traitement de votre demande et à l’établissement d’une offre. Si nécessaire, nous transmettons les données techniques du projet à notre partenaire de fabrication ; aucune transmission à des fins publicitaires.</p>"
           "<p><b>Transmission :</b> via le service de formulaires FormSubmit (formsubmit.co), qui transfère la demande par e-mail à info@forcotech.com ; un traitement en dehors de l’UE est possible. Base juridique : art. 6(1)(b) RGPD et votre consentement (art. 6(1)(a), art. 49(1)(a) RGPD), révocable à tout moment. Vous pouvez aussi nous écrire directement par e-mail.</p>"
           "<p><b>Durée et droits :</b> suppression après clôture de la demande, ou à l’issue des délais légaux en cas de contrat. Accès, rectification, effacement, opposition et retrait sans formalité à info@forcotech.com. Plus d’informations dans la <a href=\"/fr/confidentialite/\">politique de confidentialité</a>.</p>"),
  consent="J’accepte que mes données soient enregistrées et traitées pour le traitement de la demande et transmises à cette fin via FormSubmit (voir la <a href=\"/fr/confidentialite/\">politique de confidentialité</a>). Je peux retirer mon consentement à tout moment. *",
  send="Envoyer la demande",
  thanks="<b>Merci pour votre demande !</b><br>Nous revenons généralement vers vous sous 2 à 3 jours ouvrés.",
  copy="Copier le texte", mailbtn="Ouvrir dans le logiciel de messagerie",
  side="Vous préférez prédimensionner vous-même ?", cfg_url="https://www.forcotech.com/konfigurator/fr/", cfg="Ouvrir le configurateur",
  addr="<b>Silent Engineering di Romolo Vicari</b><br>Marques ForCoTech et Silent-Mode<br>Via Trento 22 · 23875 Osnago (LC) · Italie<br>E-mail : <a href=\"mailto:info@forcotech.com\">info@forcotech.com</a><br>Web : <a href=\"https://www.silent-mode.com\">silent-mode.com</a>",
 ),
}

FORM = """<section id="{sec}">
  <div class="wrap">
    <div class="contact has-form">
      <div>
        <div class="intro"><h2>{h2}</h2><p>{intro}</p></div>
        <form class="qf" id="qf" novalidate>
          <div class="row">
            <label class="f">{name}<input id="q_name" required autocomplete="name"></label>
            <label class="f">{company}<input id="q_company" autocomplete="organization"></label>
          </div>
          <div class="row">
            <label class="f">{email}<input id="q_email" type="email" required autocomplete="email"></label>
            <label class="f">{phone}<input id="q_phone" type="tel" autocomplete="tel"></label>
          </div>
          <label class="f">{typ_l}<select id="q_typ">{typ_o}</select></label>
          <div class="row">
            <label class="f">{unit}<input id="q_unit" placeholder="{unit_ph}"></label>
            <label class="f">{count}<input id="q_count" inputmode="numeric"></label>
          </div>
          <label class="f">{place}<input id="q_place"></label>
          <label class="f">{msg}<textarea id="q_msg" rows="3" placeholder="{msg_ph}"></textarea></label>
          <label class="f">{file}<input id="q_file" type="file" accept=".pdf,application/pdf,image/png,image/jpeg"></label>
          <div class="hp" aria-hidden="true"><input id="qHp" tabindex="-1" autocomplete="off"></div>
          <details class="privacy"><summary>{privacy_sum}</summary>{privacy}</details>
          <label class="chk"><input type="checkbox" id="qConsent"><span>{consent}</span></label>
          <div class="err" id="qErr" role="alert"></div>
          <div class="btns"><button class="btn" type="submit" id="qSend">{send}</button></div>
        </form>
        <div class="qthanks" id="qThanks" role="status">{thanks}</div>
        <div class="qready" id="qReady" hidden>
          <b id="qReadyMsg"></b>
          <textarea id="qReadyText" rows="9" readonly></textarea>
          <div class="btns"><button class="btn" type="button" id="qCopy">{copy}</button><a class="btn ghost" id="qMail" href="#">{mailbtn}</a></div>
          <span class="hint" id="qCopyHint"></span>
        </div>
      </div>
      <div>
        <div class="qnext"><b>{nx_h}</b><ol>{nx}</ol></div>
        <address>{addr}</address>
        <p style="margin-top:18px"><b>{side}</b></p>
        <div class="btns" style="margin-top:10px"><a class="btn" href="{cfg_url}">{cfg}</a></div>
      </div>
    </div>
  </div>
</section>"""

LANGFILE = {"de": "index.html", "en": "en/index.html", "fr": "fr/index.html"}
SUBTXT = {
 "de": ("Projekt anfragen", "Gerät, Anzahl und Aufstellort genügen für den Anfang – mit Datenblatt prüfen wir Maße, Luftmenge und Schallleistung direkt. Ein verbindliches Angebot für komplexe Projekte erhalten Sie in der Regel in 2–3 Tagen; Sonderanfertigungen liefern wir meist 40–60 Tage nach Bestellung."),
 "en": ("Request a project", "Unit, quantity and location are enough to start – with a data sheet we can check dimensions, air volume and sound power straight away. For complex projects you will usually receive a binding quotation within 2–3 days; custom enclosures are usually delivered 40–60 days after order."),
 "fr": ("Demander un projet", "L’appareil, le nombre et le lieu d’implantation suffisent pour commencer – avec la fiche technique, nous vérifions directement dimensions, débit d’air et puissance acoustique. Pour les projets complexes, vous recevez en général une offre ferme sous 2 à 3 jours ; les caissons sur mesure sont livrés en général 40 à 60 jours après la commande."),
}


# Eigene Texte für IoT-Anfragen (Seite /iot/, typ="iot") – ohne Haubenauslegung und Lieferzeit Sonderanfertigung
IOT = {
 "de": dict(h2="IoT-Monitoring anfragen",
            intro="Anlage, Kältemittel und gewünschte Messgrößen genügen für den Anfang – auch für die Nachrüstung bestehender Schallhauben. Sie erhalten ein Messkonzept mit Angebot.",
            nx="<li><b>Prüfung</b> Ihrer Angaben – bei Bedarf kurze Rückfrage zu Messpunkten, Ex-Zone und Gebäudeleittechnik</li><li><b>Messkonzept</b> mit Sensoren, Gateway, Schnittstellen und Alarmwegen</li><li><b>Angebot</b> für Lieferung, Montage und Inbetriebnahme – Sensoren und Gateway vorkonfiguriert</li>",
            msg_ph="z. B. Messgrößen, neue Haube oder Nachrüstung, Ex-Zone, GLT-Protokoll, vorhandener Energiezähler …"),
 "en": dict(h2="Request IoT monitoring",
            intro="Unit, refrigerant and the variables you want to measure are enough to start – also for retrofitting existing enclosures. You will receive a measuring concept with a quotation.",
            nx="<li><b>Review</b> of your details – with a short question on measuring points, hazardous zone and BMS if needed</li><li><b>Measuring concept</b> with sensors, gateway, interfaces and alarm routes</li><li><b>Quotation</b> for delivery, installation and commissioning – sensors and gateway pre-configured</li>",
            msg_ph="e.g. measured variables, new enclosure or retrofit, hazardous zone, BMS protocol, existing energy meter …"),
 "fr": dict(h2="Demander un monitoring IoT",
            intro="L’appareil, le fluide frigorigène et les grandeurs à mesurer suffisent pour commencer – également pour équiper des caissons existants. Vous recevez un concept de mesure avec une offre.",
            nx="<li><b>Vérification</b> de vos données – avec une courte question sur les points de mesure, la zone Ex et la GTB si nécessaire</li><li><b>Concept de mesure</b> avec capteurs, passerelle, interfaces et chaînes d’alarme</li><li><b>Offre</b> pour la livraison, le montage et la mise en service – capteurs et passerelle préconfigurés</li>",
            msg_ph="p. ex. grandeurs à mesurer, nouveau caisson ou rétrofit, zone Ex, protocole GTB, compteur d’énergie existant …"),
}


# Italienisch und Spanisch (22.11.2026)
L["it/index.html"] = dict(
  typ_l="Tipo di impianto", typ_o='<option value="">selezionare</option><option value="wp">Pompa di calore / climatizzatore</option><option value="gross">Refrigeratore / grande pompa di calore / dry cooler</option><option value="vrf">Unità esterna VRF/VRV</option><option value="pv">Inverter fotovoltaico</option><option value="bess">Accumulo a batterie (BESS)</option><option value="dc">Data center</option><option value="wand">Barriera acustica</option><option value="iot">Monitoraggio IoT / sensori</option><option value="sonst">Altro</option>',
  sec="contact",
  claim="<span>Silenzio per i vicini.</span><em>Prestazioni per l’impianto.</em>",
  what="Cabine acustiche per pompe di calore e impianti HVAC",
  lead="<b>Prima la verifica, poi la cabina.</b> Per pompe di calore, refrigeratori, VRF, inverter fotovoltaici e BESS calcoliamo in anticipo il livello al ricettore e progettiamo insieme acustica e flusso d’aria – realizzate con tecnologia Absora.",
  nx_h="Come proseguiamo", nx="<li><b>Verifica</b> dei vostri dati – se necessario con una breve domanda</li><li><b>Calcolo del livello</b> al ricettore e progettazione di acustica e flusso d’aria</li><li><b>Offerta vincolante</b> con disegno – per progetti complessi di norma entro 2–3 giorni</li>",
  h2="Avviate il vostro progetto",
  intro="Apparecchio, numero e luogo di installazione bastano per iniziare – con la scheda tecnica verifichiamo subito dimensioni, portata d’aria e potenza sonora. Per progetti complessi ricevete di norma un’offerta vincolante entro 2–3 giorni.",
  name="Nome *", company="Azienda", email="E-mail *", phone="Telefono", place="Luogo del progetto (CAP / città)",
  unit="Apparecchio (costruttore / modello)", unit_ph="ad es. York YMAE0260", count="Numero di apparecchi",
  msg="Messaggio", msg_ph="ad es. limite notturno, distanza dai vicini, installazione su tetto, tempistiche …",
  file="Scheda tecnica, disegno o foto (facoltativo · PDF o immagine, max. 10 MB)",
  privacy_sum="Informativa privacy per questa richiesta",
  privacy=("<p><b>Titolare del trattamento:</b> Silent Engineering di Romolo Vicari (marchio ForCoTech), Via Trento 22, 23875 Osnago (LC), Italia · <a href=\"mailto:info@forcotech.com\">info@forcotech.com</a></p>"
           "<p><b>Finalità:</b> utilizziamo i vostri dati ed eventuali schede tecniche allegate esclusivamente per gestire la richiesta e preparare un’offerta. Ove necessario, trasmettiamo i dati tecnici del progetto al nostro partner di produzione; nessuna cessione a fini pubblicitari.</p>"
           "<p><b>Trasmissione:</b> tramite il servizio modulo FormSubmit (formsubmit.co), che inoltra la richiesta per e-mail a info@forcotech.com; è possibile un trattamento al di fuori dell’UE. Base giuridica: art. 6, par. 1, lett. b) GDPR e il vostro consenso (art. 6, par. 1, lett. a), art. 49, par. 1, lett. a) GDPR), revocabile in qualsiasi momento. In alternativa contattateci direttamente per e-mail.</p>"
           "<p><b>Conservazione e diritti:</b> cancellazione alla chiusura della richiesta o, in caso di contratto, dopo i termini di legge. Accesso, rettifica, cancellazione, opposizione e revoca senza formalità a info@forcotech.com. Maggiori informazioni nell’<a href=\"/it/privacy/\">informativa sulla privacy</a>.</p>"),
  consent="Acconsento alla memorizzazione e al trattamento dei miei dati per la gestione della richiesta e alla loro trasmissione a tal fine tramite FormSubmit (vedi l’<a href=\"/it/privacy/\">informativa sulla privacy</a>). Posso revocare il consenso in qualsiasi momento. *",
  send="Invia richiesta",
  thanks="<b>Grazie per la vostra richiesta!</b><br>Di norma vi rispondiamo entro 2–3 giorni lavorativi.",
  copy="Copia testo", mailbtn="Apri nel programma di posta",
  side="Preferite predimensionare da soli?", cfg_url="https://www.forcotech.com/konfigurator/it/", cfg="Apri il configuratore",
  addr="<b>Silent Engineering di Romolo Vicari</b><br>Marchi ForCoTech e Silent-Mode<br>Via Trento 22 · 23875 Osnago (LC) · Italia<br>E-mail: <a href=\"mailto:info@forcotech.com\">info@forcotech.com</a><br>Web: <a href=\"https://www.silent-mode.com\">silent-mode.com</a>",
)
L["es/index.html"] = dict(
  typ_l="Tipo de equipo", typ_o='<option value="">seleccione</option><option value="wp">Bomba de calor / equipo de climatización</option><option value="gross">Enfriadora / gran bomba de calor / aerorrefrigerador</option><option value="vrf">Unidad exterior VRF/VRV</option><option value="pv">Inversor fotovoltaico</option><option value="bess">Almacenamiento en baterías (BESS)</option><option value="dc">Centro de datos</option><option value="wand">Pantalla acústica</option><option value="iot">Monitorización IoT / sensores</option><option value="sonst">Otro</option>',
  sec="contact",
  claim="<span>Silencio para los vecinos.</span><em>Rendimiento para el equipo.</em>",
  what="Cabinas acústicas para bombas de calor e instalaciones HVAC",
  lead="<b>Primero la prueba, después la cabina.</b> Para bombas de calor, enfriadoras, VRF, inversores fotovoltaicos y BESS calculamos de antemano el nivel en el receptor y diseñamos conjuntamente la acústica y el flujo de aire – fabricadas con tecnología Absora.",
  nx_h="Cómo seguimos", nx="<li><b>Revisión</b> de sus datos – con una breve consulta si es necesario</li><li><b>Cálculo del nivel</b> en el receptor y diseño de la acústica y el flujo de aire</li><li><b>Oferta vinculante</b> con plano – en proyectos complejos, normalmente en 2–3 días</li>",
  h2="Inicie su proyecto",
  intro="El equipo, la cantidad y la ubicación bastan para empezar – con la ficha técnica comprobamos directamente dimensiones, caudal de aire y potencia acústica. En proyectos complejos recibirá normalmente una oferta vinculante en 2–3 días.",
  name="Nombre *", company="Empresa", email="Correo electrónico *", phone="Teléfono", place="Ubicación del proyecto (código postal / localidad)",
  unit="Equipo (fabricante / modelo)", unit_ph="p. ej. York YMAE0260", count="Número de equipos",
  msg="Mensaje", msg_ph="p. ej. límite nocturno, distancia a los vecinos, instalación en cubierta, plazos …",
  file="Ficha técnica, plano o foto (opcional · PDF o imagen, máx. 10 MB)",
  privacy_sum="Información sobre privacidad para esta solicitud",
  privacy=("<p><b>Responsable del tratamiento:</b> Silent Engineering di Romolo Vicari (marca ForCoTech), Via Trento 22, 23875 Osnago (LC), Italia · <a href=\"mailto:info@forcotech.com\">info@forcotech.com</a></p>"
           "<p><b>Finalidad:</b> utilizamos sus datos y la ficha técnica adjunta, en su caso, exclusivamente para gestionar su solicitud y preparar una oferta. Cuando es necesario, transmitimos los datos técnicos del proyecto a nuestro socio de fabricación; sin cesión con fines publicitarios.</p>"
           "<p><b>Transmisión:</b> a través del servicio de formularios FormSubmit (formsubmit.co), que reenvía la solicitud por correo electrónico a info@forcotech.com; es posible un tratamiento fuera de la UE. Base jurídica: art. 6.1.b) RGPD y su consentimiento (art. 6.1.a) y art. 49.1.a) RGPD), revocable en cualquier momento. Como alternativa, escríbanos directamente por correo electrónico.</p>"
           "<p><b>Conservación y derechos:</b> supresión al cerrar la solicitud o, si se celebra un contrato, tras los plazos legales. Acceso, rectificación, supresión, oposición y revocación sin formalidades en info@forcotech.com. Más información en la <a href=\"/es/privacidad/\">política de privacidad</a>.</p>"),
  consent="Acepto que mis datos se almacenen y traten para gestionar la solicitud y se transmitan con este fin a través de FormSubmit (véase la <a href=\"/es/privacidad/\">política de privacidad</a>). Puedo revocar mi consentimiento en cualquier momento. *",
  send="Enviar solicitud",
  thanks="<b>¡Gracias por su solicitud!</b><br>Normalmente le respondemos en un plazo de 2–3 días laborables.",
  copy="Copiar texto", mailbtn="Abrir en el programa de correo",
  side="¿Prefiere predimensionar usted mismo?", cfg_url="https://www.forcotech.com/konfigurator/es/", cfg="Abrir el configurador",
  addr="<b>Silent Engineering di Romolo Vicari</b><br>Marcas ForCoTech y Silent-Mode<br>Via Trento 22 · 23875 Osnago (LC) · Italia<br>Correo electrónico: <a href=\"mailto:info@forcotech.com\">info@forcotech.com</a><br>Web: <a href=\"https://www.silent-mode.com\">silent-mode.com</a>",
)
LANGFILE.update({"it": "it/index.html", "es": "es/index.html"})
SUBTXT["it"] = ("Richiedete un progetto", "Apparecchio, numero e luogo di installazione bastano per iniziare – con la scheda tecnica verifichiamo subito dimensioni, portata d’aria e potenza sonora. Per progetti complessi ricevete di norma un’offerta vincolante entro 2–3 giorni; le esecuzioni su misura vengono consegnate di norma 40–60 giorni dopo l’ordine.")
SUBTXT["es"] = ("Solicite un proyecto", "El equipo, la cantidad y la ubicación bastan para empezar – con la ficha técnica comprobamos directamente dimensiones, caudal de aire y potencia acústica. En proyectos complejos recibirá normalmente una oferta vinculante en 2–3 días; las cabinas a medida se entregan normalmente 40–60 días después del pedido.")
IOT["it"] = dict(h2="Richiedete il monitoraggio IoT",
            intro="Apparecchio, refrigerante e grandezze da misurare bastano per iniziare – anche per l’adeguamento di cabine esistenti. Riceverete un concetto di misura con offerta.",
            nx="<li><b>Verifica</b> dei vostri dati – se necessario con una breve domanda su punti di misura, zona Ex e BMS</li><li><b>Concetto di misura</b> con sensori, gateway, interfacce e percorsi di allarme</li><li><b>Offerta</b> per fornitura, installazione e messa in servizio – sensori e gateway preconfigurati</li>",
            msg_ph="ad es. grandezze da misurare, nuova cabina o adeguamento, zona Ex, protocollo BMS, contatore di energia esistente …")
IOT["es"] = dict(h2="Solicite la monitorización IoT",
            intro="El equipo, el refrigerante y las magnitudes a medir bastan para empezar – también para equipar cabinas existentes. Recibirá un concepto de medición con oferta.",
            nx="<li><b>Revisión</b> de sus datos – con una breve consulta sobre puntos de medición, zona Ex y BMS si es necesario</li><li><b>Concepto de medición</b> con sensores, pasarela, interfaces y rutas de alarma</li><li><b>Oferta</b> de suministro, instalación y puesta en marcha – sensores y pasarela preconfigurados</li>",
            msg_ph="p. ej. magnitudes a medir, cabina nueva o adaptación, zona Ex, protocolo BMS, contador de energía existente …")


def form_section(lang, sec="anfrage", typ=None):
    """Formular-Abschnitt für Unterseiten (tools/build_news.py → page()). typ="iot" → eigene IoT-Texte."""
    t = dict(L[LANGFILE[lang]])
    t["sec"] = sec
    t["h2"], t["intro"] = SUBTXT[lang]
    if typ == "iot":
        t.update(IOT[lang])
    return FORM.format(**t)


def main():
  for f, t in L.items():
      p = ROOT / f
      s = p.read_text(encoding="utf-8")
      h1 = f'<h1><span class="claim">{t["claim"]}</span><span class="what">{t["what"]}</span></h1>\n      <p class="lead">{t["lead"]}</p>'
      s, n1 = re.subn(r'<h1>.*?</h1>\s*<p class="lead">.*?</p>', h1, s, count=1, flags=re.S)
      s, n2 = re.subn(r'<section id="' + t["sec"] + r'">.*?</section>', FORM.format(**t), s, count=1, flags=re.S)
      if 'src="/anfrage.js"' not in s:
          s = s.replace("</body>", '<script src="/anfrage.js" defer></script>\n</body>', 1)
      assert n1 == 1 and n2 == 1, (f, n1, n2)
      p.write_text(s, encoding="utf-8")
      print("ok", f)


if __name__ == "__main__":
    main()
