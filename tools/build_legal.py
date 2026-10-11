#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Erzeugt Impressum und Datenschutzerklärung (DE/EN) im Layout der Visitenkarte.
Texte hier ändern, dann  python3 tools/build_legal.py  ausführen."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_news as bn  # Seitenrahmen (Kopf, Navigation, Fuß)

STAND_DE = "Oktober 2026"
STAND_EN = "October 2026"

ADDR = """<p>Silent Engineering di Romolo Vicari<br>Inhaber: Romolo Vicari<br>Via Trento 22<br>23875 Osnago (LC)<br>Italien</p>
<p>E-Mail: <a href="mailto:romolo@forcotech.com">romolo@forcotech.com</a><br>Telefon: <a href="tel:+393494317342">+39 349 431 73 42</a></p>"""
ADDR_EN = (ADDR.replace("Inhaber", "Owner").replace("Italien", "Italy").replace("Telefon", "Phone"))

IMPRESSUM_DE = f"""
<h2>Angaben zum Anbieter</h2>
<p>Angaben gemäß Art. 5 der Richtlinie 2000/31/EG (E-Commerce-Richtlinie) bzw. Art. 7 D.Lgs. 70/2003.</p>
<p>Silent Engineering di Romolo Vicari<br>Einzelunternehmen (ditta individuale)<br>Inhaber: Romolo Vicari<br>Via Trento 22<br>23875 Osnago (LC)<br>Italien</p>

<h2>Kontakt</h2>
<p>E-Mail: <a href="mailto:info@forcotech.com">info@forcotech.com</a><br>Telefon: <a href="tel:+393494317342">+39 349 431 73 42</a></p>

<h2>Umsatzsteuer</h2>
<p>Partita IVA / USt-IdNr.: IT03833150133</p>

<h2>Marken</h2>
<p>ForCoTech und Silent-Mode sind Marken von Silent Engineering di Romolo Vicari. Fertigung und Montage in Allianz mit der ABSORA GmbH, Berlin.</p>

<h2>Verantwortlich für den Inhalt</h2>
<p>Romolo Vicari, Anschrift wie oben.</p>

<h2>Haftung für Inhalte und Links</h2>
<p>Die Inhalte dieser Website wurden mit größter Sorgfalt erstellt. Für die Richtigkeit, Vollständigkeit und Aktualität der Inhalte, insbesondere technischer Angaben und Richtpreise, übernehmen wir keine Gewähr; verbindlich sind allein unsere schriftlichen Angebote. Für Inhalte externer Websites, auf die wir verlinken, sind ausschließlich deren Betreiber verantwortlich.</p>

<h2>Urheberrecht</h2>
<p>Sämtliche Inhalte dieser Website, insbesondere Texte, Bilder, Grafiken, Logos und Produktbezeichnungen, sind urheberrechtlich geschützt. Vervielfältigung oder Weiterverwendung ist ohne schriftliche Genehmigung von Silent Engineering di Romolo Vicari nicht gestattet.</p>
"""

IMPRESSUM_EN = f"""
<h2>Service provider</h2>
<p>Information pursuant to Art. 5 of Directive 2000/31/EC (e-Commerce Directive) and Art. 7 of Italian Legislative Decree 70/2003.</p>
<p>Silent Engineering di Romolo Vicari<br>Sole proprietorship (ditta individuale)<br>Owner: Romolo Vicari<br>Via Trento 22<br>23875 Osnago (LC)<br>Italy</p>

<h2>Contact</h2>
<p>E-mail: <a href="mailto:info@forcotech.com">info@forcotech.com</a><br>Phone: <a href="tel:+393494317342">+39 349 431 73 42</a></p>

<h2>VAT</h2>
<p>Partita IVA / VAT ID: IT03833150133</p>

<h2>Brands</h2>
<p>ForCoTech and Silent-Mode are brands of Silent Engineering di Romolo Vicari. Manufacturing and installation in alliance with ABSORA GmbH, Berlin.</p>

<h2>Responsible for content</h2>
<p>Romolo Vicari, address as above.</p>

<h2>Liability for content and links</h2>
<p>The content of this website has been prepared with great care. We accept no liability for the accuracy, completeness or timeliness of the content, in particular technical data and budget prices; only our written quotations are binding. The operators of external websites we link to are solely responsible for their content.</p>

<h2>Copyright</h2>
<p>All content on this website, in particular texts, images, graphics, logos and product names, is protected by copyright. Reproduction or further use without written permission from Silent Engineering di Romolo Vicari is not permitted.</p>
"""

DS_DE = f"""
<p class="nlead">Der Schutz Ihrer personenbezogenen Daten ist uns ein wichtiges Anliegen. Diese Datenschutzerklärung informiert Sie gemäß der Datenschutz-Grundverordnung (DSGVO) und dem italienischen Datenschutzgesetz (D.Lgs. 196/2003 in der geltenden Fassung) darüber, welche Daten wir beim Besuch dieser Website und im Rahmen unserer Geschäftsbeziehung verarbeiten.</p>

<h2>1. Verantwortlicher</h2>
{ADDR}

<h2>2. Hosting und Server-Logfiles</h2>
<p>Diese Website wird über GitHub Pages bereitgestellt. Anbieter sind die GitHub B.V., Prins Bernhardplein 200, 1097 JB Amsterdam, Niederlande, und die GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA.</p>
<p>Beim Aufruf der Website übermittelt Ihr Browser technisch notwendige Daten an die Server von GitHub. Dazu gehören insbesondere die IP-Adresse, Datum und Uhrzeit des Zugriffs, die abgerufene Seite bzw. Datei, die übertragene Datenmenge, Browsertyp und -version, Betriebssystem sowie die zuvor besuchte Seite (Referrer). GitHub speichert die IP-Adresse nach eigenen Angaben aus Sicherheitsgründen. Wir selbst erhalten diese Protokolldaten nicht und werten sie nicht aus.</p>
<p>Rechtsgrundlage ist Art. 6 Abs. 1 lit. f DSGVO. Unser berechtigtes Interesse liegt in der sicheren und zuverlässigen Bereitstellung der Website.</p>
<p>Dabei können Daten in die USA übermittelt werden. GitHub nimmt am EU-US Data Privacy Framework teil; die Übermittlung stützt sich auf den Angemessenheitsbeschluss der EU-Kommission (Art. 45 DSGVO). Weitere Informationen finden Sie in der <a href="https://docs.github.com/de/site-policy/privacy-policies/github-general-privacy-statement">Datenschutzerklärung von GitHub</a>.</p>

<h2>3. Keine Cookies, kein Tracking</h2>
<p>Diese Website setzt keine Cookies, verwendet keine Analyse- oder Tracking-Werkzeuge und bindet keine Inhalte von Drittanbietern wie externe Schriftarten, Karten oder Videos ein. Alle Schriften, Bilder und Skripte werden direkt von dieser Website geladen.</p>

<h2>4. Kontaktaufnahme per E-Mail oder Telefon</h2>
<p>Wenn Sie uns per E-Mail oder Telefon kontaktieren, verarbeiten wir die von Ihnen mitgeteilten Daten (z. B. Name, Firma, E-Mail-Adresse, Telefonnummer, Inhalt der Anfrage und übermittelte Projektunterlagen), um Ihre Anfrage zu bearbeiten und für mögliche Anschlussfragen. Unsere E-Mails werden über unseren E-Mail-Anbieter Webland verarbeitet und gespeichert.</p>
<p>Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO (Anbahnung eines Vertrags) bzw. Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an der Beantwortung von Anfragen). Die Daten werden gelöscht, sobald sie für den Zweck nicht mehr erforderlich sind, spätestens nach Ablauf gesetzlicher Aufbewahrungsfristen.</p>

<h2>5. Anfrageformular im Konfigurator</h2>
<p>Der <a href="https://forcotech.github.io/konfigurator/">Schallhauben-Konfigurator</a> rechnet ausschließlich lokal in Ihrem Browser; solange Sie keine Anfrage absenden, werden keine Daten an uns übertragen. Wenn Sie über das Anfrageformular eine Anfrage senden, verarbeiten wir Ihre Kontaktdaten (Name, Firma, E-Mail, Telefon, Projektort), Ihre Nachricht und die gewählte Konfiguration, um Ihre Anfrage zu bearbeiten und ein Angebot zu erstellen.</p>
<p>Für den technischen Versand nutzen wir den Formulardienst FormSubmit (formsubmit.co), der die Anfrage per E-Mail an info@forcotech.com weiterleitet. FormSubmit macht keine Angaben zum Ort der Datenverarbeitung; eine Verarbeitung außerhalb der EU ohne Angemessenheitsbeschluss ist daher möglich. Die Übermittlung erfolgt deshalb nur mit Ihrer ausdrücklichen Einwilligung, die Sie im Formular erteilen (Art. 6 Abs. 1 lit. a und Art. 49 Abs. 1 lit. a DSGVO), sowie zur Anbahnung eines Vertrags (Art. 6 Abs. 1 lit. b DSGVO). Sie können die Einwilligung jederzeit mit Wirkung für die Zukunft widerrufen. Alternativ können Sie uns Ihre Anfrage direkt per E-Mail an <a href="mailto:info@forcotech.com">info@forcotech.com</a> senden; dann wird FormSubmit nicht genutzt.</p>

<h2>6. Verarbeitung von Kundendaten</h2>
<p>Im Rahmen unserer Geschäftsbeziehung verarbeiten wir Firmendaten (Firmenname, Anschrift, Steuernummer), Kontaktdaten (Name, E-Mail, Telefon, Position), Vertragsdaten (Angebote, Aufträge, Rechnungen), projektbezogene technische Daten sowie Zahlungsinformationen.</p>
<p>Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO (Vertragserfüllung) und Art. 6 Abs. 1 lit. c DSGVO (gesetzliche Pflichten, insbesondere steuer- und handelsrechtliche Aufbewahrungspflichten). Kundendaten werden für die Dauer der Geschäftsbeziehung und gemäß den gesetzlichen Aufbewahrungspflichten gespeichert.</p>

<h2>7. Weitergabe von Daten</h2>
<p>Eine Übermittlung Ihrer Daten an Dritte erfolgt nur, wenn Sie eingewilligt haben (Art. 6 Abs. 1 lit. a DSGVO), wenn sie zur Vertragserfüllung erforderlich ist (Art. 6 Abs. 1 lit. b DSGVO), wenn eine gesetzliche Verpflichtung besteht (Art. 6 Abs. 1 lit. c DSGVO) oder wenn sie zur Wahrung berechtigter Interessen erforderlich ist und Ihre Interessen nicht überwiegen (Art. 6 Abs. 1 lit. f DSGVO).</p>
<p>Mögliche Empfänger sind insbesondere Steuerberater und Wirtschaftsprüfer, IT-Dienstleister (Hosting, E-Mail, Formularversand), Buchhaltungsdienstleister, unsere Fertigungs- und Montagepartner im Rahmen eines Auftrags (ABSORA GmbH, Berlin) sowie Behörden bei gesetzlicher Auskunftspflicht.</p>

<h2>8. Speicherdauer</h2>
<p>Wir speichern personenbezogene Daten nur so lange, wie es für den jeweiligen Zweck erforderlich ist oder gesetzliche Aufbewahrungsfristen bestehen: handels- und steuerrechtlich in der Regel 10 Jahre (z. B. Rechnungen, Buchungsbelege, nach italienischem Recht), Projektdokumentation für die Dauer des Projekts zuzüglich 5 Jahre. Danach werden die Daten routinemäßig gelöscht.</p>

<h2>9. Ihre Rechte</h2>
<p>Sie haben nach der DSGVO das Recht auf Auskunft (Art. 15), Berichtigung (Art. 16), Löschung (Art. 17), Einschränkung der Verarbeitung (Art. 18), Datenübertragbarkeit (Art. 20) und Widerspruch gegen die Verarbeitung (Art. 21). Eine erteilte Einwilligung können Sie jederzeit mit Wirkung für die Zukunft widerrufen. Wenden Sie sich dazu einfach per E-Mail an uns.</p>
<p>Sie haben außerdem das Recht, sich bei einer Datenschutz-Aufsichtsbehörde zu beschweren. Zuständig für uns ist:<br>Garante per la Protezione dei Dati Personali, Piazza Venezia 11, 00187 Roma, Italien – Telefon +39 06 696771 – <a href="https://www.gpdp.it">www.gpdp.it</a></p>

<h2>10. Datensicherheit</h2>
<p>Die Website wird ausschließlich verschlüsselt per HTTPS (TLS) ausgeliefert. Darüber hinaus schützen wir Ihre Daten mit technischen und organisatorischen Maßnahmen, etwa regelmäßigen Datensicherungen, Zugriffsbeschränkungen, sicheren Passwörtern und laufenden Sicherheitsupdates.</p>

<h2>11. Minderjährige</h2>
<p>Unser Angebot richtet sich an Unternehmen und nicht an Personen unter 16 Jahren. Wir erheben wissentlich keine personenbezogenen Daten von Minderjährigen.</p>

<h2>12. Änderungen</h2>
<p>Stand dieser Datenschutzerklärung: {STAND_DE}. Wir passen sie an, wenn sich die Website oder die rechtlichen Vorgaben ändern. Es gilt die jeweils hier veröffentlichte Fassung.</p>
"""

DS_EN = f"""
<p class="nlead">Protecting your personal data is important to us. In accordance with the General Data Protection Regulation (GDPR) and the Italian data protection code (Legislative Decree 196/2003 as amended), this privacy policy explains which data we process when you visit this website and in the course of our business relationship.</p>

<h2>1. Controller</h2>
{ADDR_EN}

<h2>2. Hosting and server log files</h2>
<p>This website is provided via GitHub Pages. The providers are GitHub B.V., Prins Bernhardplein 200, 1097 JB Amsterdam, the Netherlands, and GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, USA.</p>
<p>When you visit the website, your browser transmits technically necessary data to GitHub's servers, in particular the IP address, date and time of access, the page or file requested, the amount of data transferred, browser type and version, operating system and the previously visited page (referrer). According to GitHub, the IP address is stored for security purposes. We do not receive or analyse these log data ourselves.</p>
<p>The legal basis is Art. 6(1)(f) GDPR. Our legitimate interest lies in providing the website securely and reliably.</p>
<p>Data may be transferred to the USA in this context. GitHub participates in the EU-U.S. Data Privacy Framework; the transfer is based on the European Commission's adequacy decision (Art. 45 GDPR). For more information see <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">GitHub's privacy statement</a>.</p>

<h2>3. No cookies, no tracking</h2>
<p>This website does not set cookies, does not use analytics or tracking tools and does not embed third-party content such as external fonts, maps or videos. All fonts, images and scripts are loaded directly from this website.</p>

<h2>4. Contact by e-mail or phone</h2>
<p>If you contact us by e-mail or phone, we process the data you provide (e.g. name, company, e-mail address, phone number, content of your enquiry and any project documents) in order to handle your enquiry and any follow-up questions. Our e-mails are processed and stored by our e-mail provider Webland.</p>
<p>The legal basis is Art. 6(1)(b) GDPR (pre-contractual measures) or Art. 6(1)(f) GDPR (legitimate interest in answering enquiries). The data are deleted once they are no longer needed for this purpose, at the latest after statutory retention periods have expired.</p>

<h2>5. Enquiry form in the configurator</h2>
<p>The <a href="https://forcotech.github.io/konfigurator/en/">acoustic enclosure configurator</a> calculates exclusively in your browser; no data are transmitted to us unless you send an enquiry. If you send an enquiry via the form, we process your contact details (name, company, e-mail, phone, project location), your message and the selected configuration in order to handle your enquiry and prepare a quotation.</p>
<p>For the technical transmission we use the form service FormSubmit (formsubmit.co), which forwards the enquiry by e-mail to info@forcotech.com. FormSubmit does not state where data are processed; processing outside the EU without an adequacy decision is therefore possible. The transmission therefore only takes place with your explicit consent given in the form (Art. 6(1)(a) and Art. 49(1)(a) GDPR) and for pre-contractual measures (Art. 6(1)(b) GDPR). You can withdraw your consent at any time with effect for the future. Alternatively, you can send your enquiry directly by e-mail to <a href="mailto:info@forcotech.com">info@forcotech.com</a>; FormSubmit is then not used.</p>

<h2>6. Processing of customer data</h2>
<p>In the course of our business relationship we process company data (company name, address, tax number), contact data (name, e-mail, phone, position), contract data (quotations, orders, invoices), project-related technical data and payment information.</p>
<p>The legal basis is Art. 6(1)(b) GDPR (performance of a contract) and Art. 6(1)(c) GDPR (legal obligations, in particular retention obligations under tax and commercial law). Customer data are stored for the duration of the business relationship and in accordance with statutory retention periods.</p>

<h2>7. Disclosure of data</h2>
<p>Your data are only passed on to third parties if you have consented (Art. 6(1)(a) GDPR), if this is necessary to perform a contract (Art. 6(1)(b) GDPR), if there is a legal obligation (Art. 6(1)(c) GDPR) or if it is necessary to protect legitimate interests and your interests do not override them (Art. 6(1)(f) GDPR).</p>
<p>Possible recipients are in particular tax advisers and auditors, IT service providers (hosting, e-mail, form delivery), accounting service providers, our manufacturing and installation partner within the scope of an order (ABSORA GmbH, Berlin) and authorities where there is a legal duty to provide information.</p>

<h2>8. Retention period</h2>
<p>We store personal data only as long as necessary for the respective purpose or as required by statutory retention periods: generally 10 years under commercial and tax law (e.g. invoices, accounting records, under Italian law), project documentation for the duration of the project plus 5 years. After that, the data are routinely deleted.</p>

<h2>9. Your rights</h2>
<p>Under the GDPR you have the right of access (Art. 15), rectification (Art. 16), erasure (Art. 17), restriction of processing (Art. 18), data portability (Art. 20) and to object to processing (Art. 21). You can withdraw any consent given at any time with effect for the future. Simply contact us by e-mail.</p>
<p>You also have the right to lodge a complaint with a data protection supervisory authority. The authority responsible for us is:<br>Garante per la Protezione dei Dati Personali, Piazza Venezia 11, 00187 Rome, Italy – phone +39 06 696771 – <a href="https://www.gpdp.it">www.gpdp.it</a></p>

<h2>10. Data security</h2>
<p>The website is delivered exclusively in encrypted form via HTTPS (TLS). In addition, we protect your data with technical and organisational measures such as regular backups, access restrictions, secure passwords and ongoing security updates.</p>

<h2>11. Minors</h2>
<p>Our offer is aimed at businesses and not at persons under 16. We do not knowingly collect personal data from minors.</p>

<h2>12. Changes</h2>
<p>Version of this privacy policy: {STAND_EN}. We update it when the website or legal requirements change. The version published here applies.</p>
"""

PAGES = [
    ("de", "/impressum/", "/en/legal-notice/", "Impressum", "Impressum von ForCoTech – Silent Engineering di Romolo Vicari, Osnago (LC), Italien.", IMPRESSUM_DE),
    ("en", "/en/legal-notice/", "/impressum/", "Legal notice", "Legal notice of ForCoTech – Silent Engineering di Romolo Vicari, Osnago (LC), Italy.", IMPRESSUM_EN),
    ("de", "/datenschutz/", "/en/privacy/", "Datenschutzerklärung", "Datenschutzerklärung von ForCoTech – Silent Engineering di Romolo Vicari: Hosting, keine Cookies, Kontakt, Ihre Rechte.", DS_DE),
    ("en", "/en/privacy/", "/datenschutz/", "Privacy policy", "Privacy policy of ForCoTech – Silent Engineering di Romolo Vicari: hosting, no cookies, contact, your rights.", DS_EN),
]

for lang, path, alt, title, desc, body in PAGES:
    main = f"""<article class="npost legal">
  <div class="wrap">
    <h1>{title}</h1>
    <div class="nbody">
{body.strip()}
    </div>
  </div>
</article>"""
    bn.write(path[1:] + "index.html", bn.page(lang, f"{title} – ForCoTech", desc, path, alt, main, cta=False))
print("Impressum und Datenschutz gebaut")
