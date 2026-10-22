#!/usr/bin/env python3
"""Startseiten DE/EN/FR: Claim im Kopf und Anfrageformular im Kontaktbereich.

Ersetzt die <h1>/Lead-Zeile im Hero und den Inhalt von <section id="kontakt|contact">.
Wiederholbar (erkennt die eigenen Marker). Logik des Formulars: anfrage.js, Gestaltung: style.css.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent.parent

L = {
 "index.html": dict(
  sec="kontakt",
  claim="<span>Ruhe für die Nachbarn.</span><em>Leistung für die Anlage.</em>",
  what="Schallhauben für Wärmepumpen und HVAC-Anlagen",
  lead="Für Wärmepumpen, Kälteanlagen, VRF, PV-Wechselrichter und BESS – individuell ausgelegt, gefertigt mit Absora-Technologie.",
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
  sec="contact",
  claim="<span>Quiet for the neighbours.</span><em>Performance for the unit.</em>",
  what="Acoustic enclosures for heat pumps and HVAC systems",
  lead="For heat pumps, chillers, VRF, PV inverters and BESS – individually engineered, built with Absora technology.",
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
  sec="contact",
  claim="<span>Le calme pour les voisins.</span><em>La performance pour l’appareil.</em>",
  what="Caissons acoustiques pour pompes à chaleur et installations CVC",
  lead="Pour pompes à chaleur, groupes froids, VRF, onduleurs PV et BESS – conçus sur mesure, fabriqués avec la technologie Absora.",
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
        <address>{addr}</address>
        <p style="margin-top:18px"><b>{side}</b></p>
        <div class="btns" style="margin-top:10px"><a class="btn" href="{cfg_url}">{cfg}</a></div>
      </div>
    </div>
  </div>
</section>"""

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
