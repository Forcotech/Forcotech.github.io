#!/usr/bin/env python3
# © Silent Engineering di Romolo Vicari – ForCoTech
"""Erzeugt Impressum und Datenschutzerklärung (DE/EN/FR) im Layout der Visitenkarte.
Texte hier ändern, dann  python3 tools/build_legal.py  ausführen."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_news as bn  # Seitenrahmen (Kopf, Navigation, Fuß)

STAND_DE = "Oktober 2026"
STAND_EN = "October 2026"
STAND_FR = "octobre 2026"

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
<p>Diese Website setzt keine Cookies, verwendet keine Analyse- oder Tracking-Werkzeuge und bindet keine externen Schriftarten oder Karten ein. Alle Schriften, Bilder und Skripte werden direkt von dieser Website geladen.</p>
<p><b>YouTube-Videos:</b> Auf der Startseite sind Videos von YouTube (Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irland) eingebunden. Sie werden erst geladen, wenn Sie aktiv auf „Video abspielen“ klicken; vorher werden keine Daten an YouTube übermittelt. Mit dem Klick wird eine Verbindung zu YouTube im erweiterten Datenschutzmodus (youtube-nocookie.com) hergestellt; dabei werden u. a. Ihre IP-Adresse und Angaben zum Browser an Google übertragen, ggf. auch in die USA (EU-US Data Privacy Framework, Art. 45 DSGVO), und YouTube kann Daten im Browser speichern. Rechtsgrundlage ist Ihre Einwilligung durch den Klick (Art. 6 Abs. 1 lit. a DSGVO, § 25 Abs. 1 TDDDG). Weitere Informationen: <a href="https://policies.google.com/privacy?hl=de">Datenschutzerklärung von Google</a>.</p>

<h2>4. Kontaktaufnahme per E-Mail oder Telefon</h2>
<p>Wenn Sie uns per E-Mail oder Telefon kontaktieren, verarbeiten wir die von Ihnen mitgeteilten Daten (z. B. Name, Firma, E-Mail-Adresse, Telefonnummer, Inhalt der Anfrage und übermittelte Projektunterlagen), um Ihre Anfrage zu bearbeiten und für mögliche Anschlussfragen. Unsere E-Mails werden über unseren E-Mail-Anbieter Webland verarbeitet und gespeichert.</p>
<p>Rechtsgrundlage ist Art. 6 Abs. 1 lit. b DSGVO (Anbahnung eines Vertrags) bzw. Art. 6 Abs. 1 lit. f DSGVO (berechtigtes Interesse an der Beantwortung von Anfragen). Die Daten werden gelöscht, sobald sie für den Zweck nicht mehr erforderlich sind, spätestens nach Ablauf gesetzlicher Aufbewahrungsfristen.</p>

<h2>5. Anfrageformular im Konfigurator</h2>
<p>Der <a href="https://www.forcotech.com/konfigurator/">Schallhauben-Konfigurator</a> rechnet ausschließlich lokal in Ihrem Browser; solange Sie keine Anfrage absenden, werden keine Daten an uns übertragen. Wenn Sie über das Anfrageformular eine Anfrage senden, verarbeiten wir Ihre Kontaktdaten (Name, Firma, E-Mail, Telefon, Projektort), Ihre Nachricht und die gewählte Konfiguration, um Ihre Anfrage zu bearbeiten und ein Angebot zu erstellen.</p>
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
<p>This website does not set cookies, does not use analytics or tracking tools and does not embed external fonts or maps. All fonts, images and scripts are loaded directly from this website.</p>
<p><b>YouTube videos:</b> The home page embeds videos from YouTube (Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Ireland). They are only loaded when you actively click “Play video”; no data is sent to YouTube before that. On click, a connection to YouTube in privacy-enhanced mode (youtube-nocookie.com) is established; your IP address and browser information, among other data, are transmitted to Google, possibly also to the USA (EU-US Data Privacy Framework, Art. 45 GDPR), and YouTube may store data in your browser. The legal basis is your consent given by clicking (Art. 6(1)(a) GDPR). More information: <a href="https://policies.google.com/privacy?hl=en">Google privacy policy</a>.</p>

<h2>4. Contact by e-mail or phone</h2>
<p>If you contact us by e-mail or phone, we process the data you provide (e.g. name, company, e-mail address, phone number, content of your enquiry and any project documents) in order to handle your enquiry and any follow-up questions. Our e-mails are processed and stored by our e-mail provider Webland.</p>
<p>The legal basis is Art. 6(1)(b) GDPR (pre-contractual measures) or Art. 6(1)(f) GDPR (legitimate interest in answering enquiries). The data are deleted once they are no longer needed for this purpose, at the latest after statutory retention periods have expired.</p>

<h2>5. Enquiry form in the configurator</h2>
<p>The <a href="https://www.forcotech.com/konfigurator/en/">acoustic enclosure configurator</a> calculates exclusively in your browser; no data are transmitted to us unless you send an enquiry. If you send an enquiry via the form, we process your contact details (name, company, e-mail, phone, project location), your message and the selected configuration in order to handle your enquiry and prepare a quotation.</p>
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

IMPRESSUM_FR = f"""
<h2>Éditeur du site</h2>
<p>Informations conformément à l’art. 5 de la directive 2000/31/CE (directive sur le commerce électronique) et à l’art. 7 du décret législatif italien 70/2003.</p>
<p>Silent Engineering di Romolo Vicari<br>Entreprise individuelle (ditta individuale)<br>Titulaire : Romolo Vicari<br>Via Trento 22<br>23875 Osnago (LC)<br>Italie</p>

<h2>Contact</h2>
<p>E-mail : <a href="mailto:info@forcotech.com">info@forcotech.com</a><br>Téléphone : <a href="tel:+393494317342">+39 349 431 73 42</a></p>

<h2>TVA</h2>
<p>Partita IVA / N° TVA intracommunautaire : IT03833150133</p>

<h2>Hébergement</h2>
<p>GitHub Pages – GitHub B.V., Prins Bernhardplein 200, 1097 JB Amsterdam, Pays-Bas.</p>

<h2>Marques</h2>
<p>ForCoTech et Silent-Mode sont des marques de Silent Engineering di Romolo Vicari. Fabrication et montage en alliance avec ABSORA GmbH, Berlin.</p>

<h2>Directeur de la publication</h2>
<p>Romolo Vicari, adresse ci-dessus.</p>

<h2>Responsabilité pour les contenus et les liens</h2>
<p>Les contenus de ce site ont été élaborés avec le plus grand soin. Nous ne garantissons pas l’exactitude, l’exhaustivité ni l’actualité des contenus, en particulier des données techniques et des prix indicatifs ; seules nos offres écrites font foi. Les exploitants des sites externes vers lesquels nous renvoyons sont seuls responsables de leur contenu.</p>

<h2>Droits d’auteur</h2>
<p>L’ensemble des contenus de ce site, en particulier les textes, images, graphiques, logos et désignations de produits, est protégé par le droit d’auteur. Toute reproduction ou réutilisation sans l’autorisation écrite de Silent Engineering di Romolo Vicari est interdite.</p>
<p>En cas de divergence, la version allemande prévaut.</p>
"""

DS_FR = f"""
<p class="nlead">La protection de vos données personnelles nous tient à cœur. Conformément au Règlement général sur la protection des données (RGPD) et au code italien de la protection des données (décret législatif 196/2003 modifié), la présente politique explique quelles données nous traitons lorsque vous consultez ce site et dans le cadre de notre relation commerciale.</p>

<h2>1. Responsable du traitement</h2>
<p>Silent Engineering di Romolo Vicari<br>Titulaire : Romolo Vicari<br>Via Trento 22<br>23875 Osnago (LC)<br>Italie</p>
<p>E-mail : <a href="mailto:romolo@forcotech.com">romolo@forcotech.com</a><br>Téléphone : <a href="tel:+393494317342">+39 349 431 73 42</a></p>

<h2>2. Hébergement et fichiers journaux du serveur</h2>
<p>Ce site est fourni via GitHub Pages. Les prestataires sont GitHub B.V., Prins Bernhardplein 200, 1097 JB Amsterdam, Pays-Bas, et GitHub, Inc., 88 Colin P. Kelly Jr. Street, San Francisco, CA 94107, États-Unis.</p>
<p>Lorsque vous consultez le site, votre navigateur transmet aux serveurs de GitHub des données techniquement nécessaires, notamment l’adresse IP, la date et l’heure de l’accès, la page ou le fichier demandé, le volume de données transféré, le type et la version du navigateur, le système d’exploitation et la page précédemment consultée (référent). Selon GitHub, l’adresse IP est conservée à des fins de sécurité. Nous ne recevons ni n’analysons nous-mêmes ces données de journal.</p>
<p>La base légale est l’art. 6(1)(f) RGPD. Notre intérêt légitime consiste à mettre le site à disposition de manière sûre et fiable.</p>
<p>Des données peuvent à cette occasion être transférées aux États-Unis. GitHub participe au cadre de protection des données UE–États-Unis (Data Privacy Framework) ; le transfert repose sur la décision d’adéquation de la Commission européenne (art. 45 RGPD). Pour en savoir plus, consultez la <a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement">déclaration de confidentialité de GitHub</a>.</p>

<h2>3. Aucun cookie, aucun traçage</h2>
<p>Ce site ne dépose aucun cookie, n’utilise aucun outil d’analyse ou de traçage et n’intègre ni polices externes ni cartes. Toutes les polices, images et scripts sont chargés directement depuis ce site.</p>
<p><b>Vidéos YouTube :</b> la page d’accueil intègre des vidéos YouTube (Google Ireland Limited, Gordon House, Barrow Street, Dublin 4, Irlande). Elles ne sont chargées que lorsque vous cliquez activement sur « Lire la vidéo » ; aucune donnée n’est transmise à YouTube auparavant. Au clic, une connexion à YouTube en mode de confidentialité renforcée (youtube-nocookie.com) est établie ; votre adresse IP et des informations sur votre navigateur, entre autres, sont transmises à Google, le cas échéant aussi aux États-Unis (EU-US Data Privacy Framework, art. 45 RGPD), et YouTube peut enregistrer des données dans votre navigateur. La base juridique est votre consentement donné par le clic (art. 6, par. 1, point a RGPD). Plus d’informations : <a href="https://policies.google.com/privacy?hl=fr">politique de confidentialité de Google</a>.</p>

<h2>4. Contact par e-mail ou par téléphone</h2>
<p>Si vous nous contactez par e-mail ou par téléphone, nous traitons les données que vous nous communiquez (p. ex. nom, société, adresse e-mail, numéro de téléphone, contenu de votre demande et éventuels documents de projet) afin de traiter votre demande et les questions qui en découlent. Nos e-mails sont traités et stockés par notre fournisseur de messagerie Webland.</p>
<p>La base légale est l’art. 6(1)(b) RGPD (mesures précontractuelles) ou l’art. 6(1)(f) RGPD (intérêt légitime à répondre aux demandes). Les données sont supprimées dès qu’elles ne sont plus nécessaires à cette fin, au plus tard à l’expiration des délais légaux de conservation.</p>

<h2>5. Formulaire de demande du configurateur</h2>
<p>Le <a href="https://www.forcotech.com/konfigurator/fr/">configurateur de caissons acoustiques</a> calcule exclusivement dans votre navigateur ; aucune donnée ne nous est transmise tant que vous n’envoyez pas de demande. Si vous envoyez une demande via le formulaire, nous traitons vos coordonnées (nom, société, e-mail, téléphone, lieu du projet), votre message et la configuration choisie afin de traiter votre demande et d’établir une offre.</p>
<p>Pour la transmission technique, nous utilisons le service de formulaires FormSubmit (formsubmit.co), qui transfère la demande par e-mail à info@forcotech.com. FormSubmit n’indique pas où les données sont traitées ; un traitement en dehors de l’UE sans décision d’adéquation est donc possible. La transmission n’a donc lieu qu’avec votre consentement explicite donné dans le formulaire (art. 6(1)(a) et art. 49(1)(a) RGPD) et pour des mesures précontractuelles (art. 6(1)(b) RGPD). Vous pouvez retirer votre consentement à tout moment avec effet pour l’avenir. Vous pouvez aussi envoyer votre demande directement par e-mail à <a href="mailto:info@forcotech.com">info@forcotech.com</a> ; FormSubmit n’est alors pas utilisé.</p>

<h2>6. Traitement des données clients</h2>
<p>Dans le cadre de notre relation commerciale, nous traitons des données d’entreprise (raison sociale, adresse, numéro fiscal), des données de contact (nom, e-mail, téléphone, fonction), des données contractuelles (offres, commandes, factures), des données techniques liées aux projets et des informations de paiement.</p>
<p>La base légale est l’art. 6(1)(b) RGPD (exécution d’un contrat) et l’art. 6(1)(c) RGPD (obligations légales, notamment obligations de conservation fiscales et commerciales). Les données clients sont conservées pendant la durée de la relation commerciale et conformément aux délais légaux de conservation.</p>

<h2>7. Communication des données</h2>
<p>Vos données ne sont transmises à des tiers que si vous y avez consenti (art. 6(1)(a) RGPD), si cela est nécessaire à l’exécution d’un contrat (art. 6(1)(b) RGPD), en cas d’obligation légale (art. 6(1)(c) RGPD) ou si cela est nécessaire à la défense d’intérêts légitimes et que vos intérêts ne prévalent pas (art. 6(1)(f) RGPD).</p>
<p>Les destinataires possibles sont notamment les conseillers fiscaux et commissaires aux comptes, les prestataires informatiques (hébergement, messagerie, transmission des formulaires), les prestataires comptables, notre partenaire de fabrication et de montage dans le cadre d’une commande (ABSORA GmbH, Berlin) et les autorités en cas d’obligation légale d’information.</p>

<h2>8. Durée de conservation</h2>
<p>Nous ne conservons les données personnelles que le temps nécessaire à la finalité concernée ou exigé par les délais légaux de conservation : en général 10 ans au titre du droit commercial et fiscal (p. ex. factures, pièces comptables, selon le droit italien), la documentation de projet pendant la durée du projet plus 5 ans. Les données sont ensuite supprimées.</p>

<h2>9. Vos droits</h2>
<p>En vertu du RGPD, vous disposez d’un droit d’accès (art. 15), de rectification (art. 16), d’effacement (art. 17), de limitation du traitement (art. 18), de portabilité (art. 20) et d’opposition au traitement (art. 21). Vous pouvez retirer à tout moment un consentement donné, avec effet pour l’avenir. Il suffit de nous écrire par e-mail.</p>
<p>Vous avez également le droit d’introduire une réclamation auprès d’une autorité de contrôle. L’autorité compétente pour nous est :<br>Garante per la Protezione dei Dati Personali, Piazza Venezia 11, 00187 Rome, Italie – tél. +39 06 696771 – <a href="https://www.gpdp.it">www.gpdp.it</a><br>Vous pouvez aussi vous adresser à l’autorité de votre lieu de résidence, en France la CNIL (<a href="https://www.cnil.fr">www.cnil.fr</a>).</p>

<h2>10. Sécurité des données</h2>
<p>Le site est fourni exclusivement sous forme chiffrée via HTTPS (TLS). Nous protégeons en outre vos données par des mesures techniques et organisationnelles telles que des sauvegardes régulières, des restrictions d’accès, des mots de passe sûrs et des mises à jour de sécurité continues.</p>

<h2>11. Mineurs</h2>
<p>Notre offre s’adresse aux entreprises et non aux personnes de moins de 16 ans. Nous ne collectons pas sciemment de données personnelles de mineurs.</p>

<h2>12. Modifications</h2>
<p>Version de la présente politique : {STAND_FR}. Nous la mettons à jour lorsque le site ou les exigences légales évoluent. La version publiée ici fait foi. En cas de divergence, la version allemande prévaut.</p>
"""

IMP = {"de": "/impressum/", "en": "/en/legal-notice/", "fr": "/fr/mentions-legales/"}
DS = {"de": "/datenschutz/", "en": "/en/privacy/", "fr": "/fr/confidentialite/"}

PAGES = [
    ("de", IMP, "Impressum", "Impressum von ForCoTech – Silent Engineering di Romolo Vicari, Osnago (LC), Italien.", IMPRESSUM_DE),
    ("en", IMP, "Legal notice", "Legal notice of ForCoTech – Silent Engineering di Romolo Vicari, Osnago (LC), Italy.", IMPRESSUM_EN),
    ("fr", IMP, "Mentions légales", "Mentions légales de ForCoTech – Silent Engineering di Romolo Vicari, Osnago (LC), Italie.", IMPRESSUM_FR),
    ("de", DS, "Datenschutzerklärung", "Datenschutzerklärung von ForCoTech – Silent Engineering di Romolo Vicari: Hosting, keine Cookies, Kontakt, Ihre Rechte.", DS_DE),
    ("en", DS, "Privacy policy", "Privacy policy of ForCoTech – Silent Engineering di Romolo Vicari: hosting, no cookies, contact, your rights.", DS_EN),
    ("fr", DS, "Politique de confidentialité", "Politique de confidentialité de ForCoTech – Silent Engineering di Romolo Vicari : hébergement, aucun cookie, contact, vos droits.", DS_FR),
]

for lang, alts, title, desc, body in PAGES:
    path = alts[lang]
    main = f"""<article class="npost legal">
  <div class="wrap">
    <h1>{title}</h1>
    <div class="nbody">
{body.strip()}
    </div>
  </div>
</article>"""
    bn.write(path[1:] + "index.html", bn.page(lang, f"{title} – ForCoTech", desc, alts, main, cta=False))
print("Impressum und Datenschutz gebaut")
