/* © Silent Engineering di Romolo Vicari – ForCoTech. Anfrageformular der Startseite (DE/EN/FR).
   Versand über FormSubmit (gleicher Zugang wie der Konfigurator) an info@forcotech.com.
   Klappt der Versand nicht, wird der Text zum Kopieren bzw. als E-Mail angeboten. */
(function () {
  var f = document.getElementById('qf');
  if (!f) return;
  var END = 'https://formsubmit.co/ajax/3793e685b5eeab6c70c5141d3ca8d77e', MAIL = 'info@forcotech.com';
  var T = {
    de: { consent: 'Bitte stimmen Sie der Verarbeitung Ihrer Angaben zu.', req: 'Bitte Name und eine gültige E-Mail-Adresse angeben.',
      big: 'Die Datei ist zu groß (max. 10 MB). Bitte eine kleinere Datei wählen oder nach dem Absenden per E-Mail schicken.',
      type: 'Bitte ein PDF oder ein Bild wählen.', sending: 'Wird gesendet …', send: 'Anfrage senden',
      fail: 'Der automatische Versand hat nicht geklappt. Bitte senden Sie den folgenden Text per E-Mail an ' + MAIL + '.',
      attach: ' Die Datei bitte an die E-Mail anhängen.', copied: 'Kopiert – jetzt in eine E-Mail einfügen.', subj: 'Anfrage Startseite – ',
      none: 'nicht beigefügt',
      k: { typ: 'Anlagentyp', name: 'Name', company: 'Firma', email: 'E-Mail', phone: 'Telefon', place: 'Projektort', unit: 'Anlage (Hersteller / Modell)', count: 'Anzahl Geräte', msg: 'Nachricht', file: 'Datenblatt' } },
    en: { consent: 'Please agree to the processing of your details.', req: 'Please enter your name and a valid e-mail address.',
      big: 'The file is too large (max. 10 MB). Please choose a smaller file or send it by e-mail after submitting.',
      type: 'Please choose a PDF or an image.', sending: 'Sending …', send: 'Send enquiry',
      fail: 'Automatic sending did not work. Please send the following text by e-mail to ' + MAIL + '.',
      attach: ' Please attach the file to the e-mail.', copied: 'Copied – now paste it into an e-mail.', subj: 'Enquiry homepage – ',
      none: 'not attached',
      k: { typ: 'Equipment type', name: 'Name', company: 'Company', email: 'E-mail', phone: 'Phone', place: 'Project location', unit: 'Unit (manufacturer / model)', count: 'Number of units', msg: 'Message', file: 'Data sheet' } },
    fr: { consent: 'Veuillez accepter le traitement de vos données.', req: 'Veuillez indiquer votre nom et une adresse e-mail valide.',
      big: 'Le fichier est trop volumineux (max. 10 Mo). Choisissez un fichier plus petit ou envoyez-le par e-mail après l’envoi.',
      type: 'Veuillez choisir un PDF ou une image.', sending: 'Envoi en cours …', send: 'Envoyer la demande',
      fail: 'L’envoi automatique n’a pas fonctionné. Veuillez envoyer le texte suivant par e-mail à ' + MAIL + '.',
      attach: ' Merci de joindre le fichier à l’e-mail.', copied: 'Copié – collez-le maintenant dans un e-mail.', subj: 'Demande page d’accueil – ',
      none: 'non joint',
      k: { typ: 'Type d’installation', name: 'Nom', company: 'Société', email: 'E-mail', phone: 'Téléphone', place: 'Lieu du projet', unit: 'Appareil (fabricant / modèle)', count: 'Nombre d’appareils', msg: 'Message', file: 'Fiche technique' } }
  };
  var L = T[(document.documentElement.lang || 'de').slice(0, 2)] || T.de;
  var $ = function (id) { return document.getElementById(id); };
  var err = $('qErr'), btn = $('qSend');
  function show(m) { err.textContent = m; err.style.display = 'block'; }

  f.addEventListener('submit', function (e) {
    e.preventDefault();
    err.style.display = 'none';
    if ($('qHp').value) return; // Spam-Falle
    var v = {};
    ['name', 'company', 'email', 'phone', 'place', 'unit', 'count', 'msg'].forEach(function (k) { v[k] = ($('q_' + k).value || '').trim(); });
    var ts = $('q_typ'); v.typ = ts && ts.value ? ts.options[ts.selectedIndex].text : '';
    if (!v.name || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v.email)) return show(L.req);
    if (!$('qConsent').checked) return show(L.consent);
    var fl = $('q_file').files && $('q_file').files[0] ? $('q_file').files[0] : null;
    if (fl && fl.size > 10 * 1024 * 1024) return show(L.big);
    if (fl && !/pdf|image\//i.test(fl.type || '') && !/\.(pdf|png|jpe?g)$/i.test(fl.name)) return show(L.type);

    var F = { _subject: L.subj + (v.company || v.name), _template: 'box', _captcha: 'false', _replyto: v.email };
    Object.keys(v).forEach(function (k) { F[L.k[k]] = v[k]; });
    F[L.k.file] = fl ? fl.name : L.none;
    var body = Object.keys(v).map(function (k) { return L.k[k] + ': ' + v[k]; }).join('\n') + '\n' + L.k.file + ': ' + F[L.k.file];

    btn.disabled = true; btn.textContent = L.sending;
    var req;
    if (fl) {
      var fd = new FormData();
      Object.keys(F).forEach(function (k) { fd.append(k, F[k]); });
      fd.append('attachment', fl, fl.name);
      req = fetch(END, { method: 'POST', headers: { Accept: 'application/json' }, body: fd });
    } else {
      req = fetch(END, { method: 'POST', headers: { 'Content-Type': 'application/json', Accept: 'application/json' }, body: JSON.stringify(F) });
    }
    req.then(function (r) {
      return r.json().catch(function () { return {}; }).then(function (j) {
        if (!r.ok || j.success === false || j.success === 'false') throw new Error(j.message || r.status);
        f.style.display = 'none';
        $('qThanks').style.display = 'block';
      });
    }).catch(function () {
      var box = $('qReady');
      $('qReadyMsg').textContent = L.fail + (fl ? L.attach : '');
      $('qReadyText').value = F._subject + '\n\n' + body;
      $('qMail').href = 'mailto:' + MAIL + '?subject=' + encodeURIComponent(F._subject) + '&body=' + encodeURIComponent(body);
      box.hidden = false;
      box.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }).then(function () { btn.disabled = false; btn.textContent = L.send; });
  });

  // Knöpfe „… anfragen“ mit data-typ wählen den Anlagentyp vor
  document.addEventListener('click', function (e) {
    var a = e.target.closest && e.target.closest('a[data-typ],button[data-typ]');
    if (a && $('q_typ')) $('q_typ').value = a.getAttribute('data-typ');
  });
  var pre = document.body.getAttribute('data-anfrage-typ');
  if (pre && $('q_typ')) $('q_typ').value = pre;

  $('qCopy').addEventListener('click', function () {
    var t = $('qReadyText');
    t.focus(); t.select();
    try { navigator.clipboard.writeText(t.value).then(function () { $('qCopyHint').textContent = L.copied; }); } catch (_) { }
  });
})();
