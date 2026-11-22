/* © Silent Engineering di Romolo Vicari – ForCoTech
   IoT-Systemschema als interaktive Animation (Seite /iot/ in DE, EN, FR, IT, ES).
   Ersetzt das statische Bild in <figure data-iot-anim>; ohne JavaScript bleibt das Bild stehen.
   Drei Szenarien: Normalbetrieb, Schalldämpfer zugesetzt, Kältemittel-Leck. Sensoren anklickbar.
   Die Werte sind Beispielwerte. Auch für das Post-Video genutzt: window.FCTIoTAnim(el, {lang, post:true}). */
(function () {
  var RED = "#c8202f", INK = "#1a1a1a", MUT = "#4a4a4a", LINE = "#cfc8c8", BG = "#f6f3f3", PALE = "#fde8ea", OK = "#1f7a4d";
  var NS = "http://www.w3.org/2000/svg";

  var T = {
    de: {
      hood: "Schallhaube", unit: "Wärmepumpe / Chiller", sil: "Schalldämpfer", radio: "Funk 868 MHz", wire: "Kabel – Sicherheitsfunktion",
      gw: "LoRaWAN-Gateway", gw2: "LAN oder Mobilfunk", ns: "Netzwerkserver", ns2: "beim Betreiber|oder in der EU",
      d1: "Dashboard", d1b: "Grenzwerte, Trends", d2: "Alarme", d2b: "E-Mail · SMS", d3: "Leittechnik", d3b: "BACnet · Modbus|MQTT",
      gwz: "Gaswarnzentrale", gwz2: "fest verdrahtet:", gwz3: "Ventilatoren 100 %, Verdichter aus",
      l: ["Δp Druckverlust Schalldämpfer", "v Luftgeschwindigkeit / Volumenstrom", "T Temperatur Zuluft, Abluft, Umgebung",
          "IR Kältemittel (NDIR), Ex", "dB Schallpegel (LAeq, LAFmax)", "kW Lastgang Strom (Zähler)"],
      off: "Verdichter AUS · Ventilatoren 100 %", clog: "zugesetzt",
      sc: ["Normalbetrieb", "Schalldämpfer zugesetzt", "Kältemittel-Leck (R290)"], auto: "Automatisch", hint: "Sensor anklicken für Details",
      cap: {
        n: "Normalbetrieb: Alle Messwerte gehen per Funk ans Dashboard – Grenzwerte und Trends im Blick.",
        p1: "Laub oder Schnee setzen den Schalldämpfer zu: Der Druckverlust Δp steigt.",
        p2: "Δp über dem Grenzwert von 20 Pa → Alarm per E-Mail und SMS, bevor Leistung oder Pegel leiden.",
        k1: "Kältemittel-Leck (R290): Der Infrarot-Sensor misst 28 % UEG.",
        k2: "Sicherheitsfunktion per Kabel: Die Gaswarnzentrale schaltet die Ventilatoren auf 100 % und den Verdichter aus – auch ohne Funk.",
        k3: "Meldung an die Leittechnik, Alarm per Funk an den Betreiber."
      },
      info: {
        dp: "Δp – Druckverlust am Schalldämpfer. Steigt er, setzt sich der Schalldämpfer zu (Laub, Schnee) und der Ventilator verlässt seine Reserve.",
        v: "v – Luftgeschwindigkeit bzw. Volumenstrom. Zeigt, ob die Anlage die ausgelegte Luftmenge bekommt.",
        t: "T – Temperatur von Zuluft, Abluft und Umgebung. Steigt die Zulufttemperatur, wird Abluft zurückgesaugt.",
        ir: "IR – Kältemittelsensor (NDIR), für R290 in Ex-Ausführung. Zusätzlich fest mit der Gaswarnzentrale verdrahtet.",
        db: "dB – Schallpegel LAeq und LAFmax. Belegt im Betrieb, dass der Grenzwert eingehalten wird – auch nachts.",
        kw: "kW – Lastgang am Stromzähler. Zeigt Mehrverbrauch, Taktung und Abtauzyklen."
      },
      now: "Aktuell", sample: "Beispielwerte", ueg: "% UEG", alarm: "Alarm"
    },
    en: {
      hood: "Acoustic enclosure", unit: "Heat pump / chiller", sil: "Silencer", radio: "Radio 868 MHz", wire: "Cable – safety function",
      gw: "LoRaWAN gateway", gw2: "LAN or cellular", ns: "Network server", ns2: "on premises|or in the EU",
      d1: "Dashboard", d1b: "limits, trends", d2: "Alarms", d2b: "e-mail · SMS", d3: "BMS", d3b: "BACnet · Modbus|MQTT",
      gwz: "Gas warning controller", gwz2: "hard-wired:", gwz3: "fans 100 %, compressors off",
      l: ["Δp silencer pressure drop", "v air velocity / air flow", "T intake, exhaust, ambient temperature",
          "IR refrigerant (NDIR), Ex", "dB sound level (LAeq, LAFmax)", "kW power load profile (meter)"],
      off: "Compressor OFF · fans 100 %", clog: "clogged",
      sc: ["Normal operation", "Silencer clogged", "Refrigerant leak (R290)"], auto: "Automatic", hint: "Click a sensor for details",
      cap: {
        n: "Normal operation: all readings go to the dashboard by radio – limits and trends at a glance.",
        p1: "Leaves or snow clog the silencer: the pressure drop Δp rises.",
        p2: "Δp above the 20 Pa limit → alarm by e-mail and SMS before capacity or noise level suffer.",
        k1: "Refrigerant leak (R290): the infrared sensor measures 28 % LEL.",
        k2: "Safety function by cable: the gas warning controller sets the fans to 100 % and switches the compressor off – even without radio.",
        k3: "Message to the BMS, alarm by radio to the operator."
      },
      info: {
        dp: "Δp – silencer pressure drop. If it rises, the silencer is clogging (leaves, snow) and the fan leaves its reserve.",
        v: "v – air velocity or air flow. Shows whether the unit gets its design air flow.",
        t: "T – intake, exhaust and ambient temperature. A rising intake temperature means exhaust air is being drawn back in.",
        ir: "IR – refrigerant sensor (NDIR), explosion-proof for R290. Also hard-wired to the gas warning controller.",
        db: "dB – sound level LAeq and LAFmax. Proves in operation that the limit is met – at night too.",
        kw: "kW – load profile at the power meter. Shows extra consumption, cycling and defrost cycles."
      },
      now: "Now", sample: "Sample values", ueg: "% LEL", alarm: "Alarm"
    },
    fr: {
      hood: "Caisson acoustique", unit: "PAC / groupe froid", sil: "Silencieux", radio: "Radio 868 MHz", wire: "Câble – fonction de sécurité",
      gw: "Passerelle LoRaWAN", gw2: "LAN ou réseau mobile", ns: "Serveur réseau", ns2: "chez l’exploitant|ou dans l’UE",
      d1: "Tableau de bord", d1b: "seuils, tendances", d2: "Alarmes", d2b: "e-mail · SMS", d3: "GTB", d3b: "BACnet · Modbus|MQTT",
      gwz: "Centrale détection gaz", gwz2: "câblée :", gwz3: "ventil. 100 %, compresseurs arrêt",
      l: ["Δp perte de charge silencieux", "v vitesse d’air / débit", "T temp. air neuf, rejeté, ambiant",
          "IR fluide (NDIR), Ex", "dB niveau sonore (LAeq, LAFmax)", "kW courbe de charge (compteur)"],
      off: "Compresseur ARRÊT · ventil. 100 %", clog: "colmaté",
      sc: ["Fonctionnement normal", "Silencieux colmaté", "Fuite de fluide (R290)"], auto: "Automatique", hint: "Cliquez sur un capteur pour les détails",
      cap: {
        n: "Fonctionnement normal : toutes les mesures arrivent par radio au tableau de bord – seuils et tendances en vue.",
        p1: "Feuilles ou neige colmatent le silencieux : la perte de charge Δp augmente.",
        p2: "Δp au-dessus du seuil de 20 Pa → alarme par e-mail et SMS avant que la puissance ou le niveau sonore n’en souffrent.",
        k1: "Fuite de fluide (R290) : le capteur infrarouge mesure 28 % LIE.",
        k2: "Fonction de sécurité par câble : la centrale gaz passe les ventilateurs à 100 % et arrête le compresseur – même sans radio.",
        k3: "Message à la GTB, alarme par radio à l’exploitant."
      },
      info: {
        dp: "Δp – perte de charge du silencieux. Si elle augmente, le silencieux se colmate (feuilles, neige) et le ventilateur sort de sa réserve.",
        v: "v – vitesse d’air ou débit. Montre si l’unité reçoit le débit prévu.",
        t: "T – température d’air neuf, d’air rejeté et ambiante. Une hausse de l’air neuf signale un recyclage d’air rejeté.",
        ir: "IR – capteur de fluide (NDIR), antidéflagrant pour le R290. Également câblé à la centrale de détection gaz.",
        db: "dB – niveau sonore LAeq et LAFmax. Prouve en exploitation que la valeur limite est respectée – la nuit aussi.",
        kw: "kW – courbe de charge au compteur. Montre surconsommation, cycles courts et dégivrages."
      },
      now: "Actuel", sample: "Valeurs d’exemple", ueg: "% LIE", alarm: "Alarme"
    },
    it: {
      hood: "Cabina insonorizzata", unit: "Pompa di calore / refrigeratore", sil: "Silenziatore", radio: "Radio 868 MHz", wire: "Cavo – funzione di sicurezza",
      gw: "Gateway LoRaWAN", gw2: "LAN o rete mobile", ns: "Network server", ns2: "presso il gestore|o nell’UE",
      d1: "Dashboard", d1b: "limiti, andamenti", d2: "Allarmi", d2b: "e-mail · SMS", d3: "BMS", d3b: "BACnet · Modbus|MQTT",
      gwz: "Centralina rilevazione gas", gwz2: "cablata:", gwz3: "ventilatori 100 %, compressori spenti",
      l: ["Δp perdita di carico silenziatore", "v velocità dell’aria / portata", "T temp. aspirazione, espulsione, ambiente",
          "IR fluido refrigerante (NDIR), Ex", "dB livello sonoro (LAeq, LAFmax)", "kW curva di carico elettrico (contatore)"],
      off: "Compressore SPENTO · ventilatori 100 %", clog: "intasato",
      sc: ["Funzionamento normale", "Silenziatore intasato", "Perdita di refrigerante (R290)"], auto: "Automatico", hint: "Cliccate su un sensore per i dettagli",
      cap: {
        n: "Funzionamento normale: tutti i valori arrivano via radio alla dashboard – limiti e andamenti sotto controllo.",
        p1: "Foglie o neve intasano il silenziatore: la perdita di carico Δp aumenta.",
        p2: "Δp oltre il limite di 20 Pa → allarme via e-mail e SMS prima che potenza o livello sonoro ne risentano.",
        k1: "Perdita di refrigerante (R290): il sensore a infrarossi misura il 28 % LIE.",
        k2: "Funzione di sicurezza via cavo: la centralina gas porta i ventilatori al 100 % e spegne il compressore – anche senza radio.",
        k3: "Segnalazione al BMS, allarme via radio al gestore."
      },
      info: {
        dp: "Δp – perdita di carico del silenziatore. Se aumenta, il silenziatore si intasa (foglie, neve) e il ventilatore esce dalla sua riserva.",
        v: "v – velocità dell’aria o portata. Mostra se l’unità riceve la portata di progetto.",
        t: "T – temperatura di aspirazione, espulsione e ambiente. Se l’aria aspirata si scalda, l’aria espulsa viene riaspirata.",
        ir: "IR – sensore di refrigerante (NDIR), in esecuzione Ex per R290. Anche cablato alla centralina di rilevazione gas.",
        db: "dB – livello sonoro LAeq e LAFmax. Dimostra in esercizio che il limite è rispettato – anche di notte.",
        kw: "kW – curva di carico al contatore. Mostra consumi in eccesso, cicli brevi e sbrinamenti."
      },
      now: "Attuale", sample: "Valori di esempio", ueg: "% LIE", alarm: "Allarme"
    },
    es: {
      hood: "Cerramiento acústico", unit: "Bomba de calor / enfriadora", sil: "Silenciador", radio: "Radio 868 MHz", wire: "Cable – función de seguridad",
      gw: "Gateway LoRaWAN", gw2: "LAN o red móvil", ns: "Servidor de red", ns2: "en el explotador|o en la UE",
      d1: "Panel", d1b: "límites, tendencias", d2: "Alarmas", d2b: "e-mail · SMS", d3: "BMS", d3b: "BACnet · Modbus|MQTT",
      gwz: "Central de detección de gas", gwz2: "cableada:", gwz3: "ventiladores 100 %, compresores parados",
      l: ["Δp pérdida de carga del silenciador", "v velocidad del aire / caudal", "T temp. de entrada, salida, ambiente",
          "IR refrigerante (NDIR), Ex", "dB nivel sonoro (LAeq, LAFmax)", "kW curva de carga eléctrica (contador)"],
      off: "Compresor PARADO · ventiladores 100 %", clog: "obstruido",
      sc: ["Funcionamiento normal", "Silenciador obstruido", "Fuga de refrigerante (R290)"], auto: "Automático", hint: "Haga clic en un sensor para ver detalles",
      cap: {
        n: "Funcionamiento normal: todas las mediciones llegan por radio al panel – límites y tendencias a la vista.",
        p1: "Hojas o nieve obstruyen el silenciador: la pérdida de carga Δp aumenta.",
        p2: "Δp por encima del límite de 20 Pa → alarma por e-mail y SMS antes de que sufran la potencia o el nivel sonoro.",
        k1: "Fuga de refrigerante (R290): el sensor infrarrojo mide un 28 % LIE.",
        k2: "Función de seguridad por cable: la central de gas pone los ventiladores al 100 % y para el compresor – también sin radio.",
        k3: "Aviso al BMS, alarma por radio al explotador."
      },
      info: {
        dp: "Δp – pérdida de carga del silenciador. Si aumenta, el silenciador se obstruye (hojas, nieve) y el ventilador sale de su reserva.",
        v: "v – velocidad del aire o caudal. Muestra si la unidad recibe el caudal de diseño.",
        t: "T – temperatura de entrada, salida y ambiente. Si sube la del aire de entrada, se está reaspirando aire expulsado.",
        ir: "IR – sensor de refrigerante (NDIR), antideflagrante para R290. Además cableado a la central de detección de gas.",
        db: "dB – nivel sonoro LAeq y LAFmax. Demuestra en servicio que se cumple el límite – también de noche.",
        kw: "kW – curva de carga en el contador. Muestra sobreconsumo, ciclos cortos y desescarches."
      },
      now: "Actual", sample: "Valores de ejemplo", ueg: "% LIE", alarm: "Alarma"
    }
  };

  // Sensoren: Lage wie im statischen Schema (tools/build_iot.py)
  var S = [
    {k: "dp", s: "Δp", x: 52, y: 158}, {k: "v", s: "v", x: 318, y: 158}, {k: "t", s: "T", x: 52, y: 230},
    {k: "ir", s: "IR", x: 110, y: 296}, {k: "db", s: "dB", x: 318, y: 228}, {k: "kw", s: "kW", x: 318, y: 296}
  ];
  var LEG = ["dp", "v", "t", "ir", "db", "kw"];
  // Ziele ab Netzwerkserver
  var TAIL = {dash: [[732, 150], [748, 104], [762, 76]], alarm: [[762, 160]], bms: [[732, 160], [748, 214], [762, 248]]};

  function num(lang, v, d) {
    var s = v.toFixed(d);
    return lang === "en" ? s : s.replace(".", ",");
  }
  function val(lang, k, x) {
    var t = T[lang];
    switch (k) {
      case "dp": return "Δp " + num(lang, x, 0) + " Pa";
      case "v": return "v " + num(lang, x, 1) + " m/s";
      case "t": return "T " + num(lang, x, 0) + " °C";
      case "ir": return "IR " + num(lang, x, 0) + " " + t.ueg;
      case "db": return num(lang, x, 0) + " dB(A)";
      case "kw": return num(lang, x, 1) + " kW";
    }
  }
  var BASE = {dp: 8, v: 4.2, t: 24, ir: 0, db: 38, kw: 12.4};

  // Szenarien: Dauer und Datenpakete {k, t0, x, to}
  var SC = [
    {d: 9, p: S.map(function (s, i) { return {k: s.k, t0: i * 1.5, x: BASE[s.k], to: "dash"}; })},
    {d: 9, p: [{k: "dp", t0: 0, x: 11, to: "dash"}, {k: "dp", t0: 1.8, x: 16, to: "dash"}, {k: "dp", t0: 3.6, x: 22, to: "alarm"},
               {k: "db", t0: 4.6, x: 39, to: "dash"}, {k: "dp", t0: 5.6, x: 25, to: "alarm"}]},
    {d: 10, p: [{k: "ir", t0: 0.3, x: 28, to: "alarm"}, {k: "kw", t0: 4.4, x: 1.8, to: "dash"}, {k: "ir", t0: 6, x: 31, to: "alarm"}]}
  ];
  var TRAVEL = 1.7;
  var WIRE = [0.3, 1.3], GWZ = 1.3, OFF = 1.6, BMSL = [1.6, 2.6], BMS = 2.6;

  function el(tag, attrs, parent) {
    var e = document.createElementNS(NS, tag);
    for (var a in attrs) e.setAttribute(a, attrs[a]);
    if (parent) parent.appendChild(e);
    return e;
  }
  function txt(parent, x, y, s, attrs) {
    var a = {x: x, y: y, "text-anchor": "middle", "font-size": 15, fill: INK};
    for (var k in attrs) a[k] = attrs[k];
    var e = el("text", a, parent); e.textContent = s; return e;
  }
  function plen(pts) {
    var L = 0; for (var i = 1; i < pts.length; i++) L += Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]);
    return L;
  }
  function along(pts, f) {
    var L = plen(pts) * Math.max(0, Math.min(1, f));
    for (var i = 1; i < pts.length; i++) {
      var dx = pts[i][0] - pts[i - 1][0], dy = pts[i][1] - pts[i - 1][1], l = Math.hypot(dx, dy);
      if (L <= l) return [pts[i - 1][0] + dx * L / l, pts[i - 1][1] + dy * L / l, i];
      L -= l;
    }
    var q = pts[pts.length - 1]; return [q[0], q[1], pts.length - 1];
  }

  function FCTIoTAnim(host, opt) {
    opt = opt || {};
    var lang = opt.lang || (document.documentElement.lang || "de").slice(0, 2);
    if (!T[lang]) lang = "en";
    var t = T[lang];
    var reduce = !opt.post && window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    var svg = el("svg", {viewBox: "0 0 920 540", "font-family": "Inter, Segoe UI, Arial, sans-serif", role: "img", class: "iot-anim-svg"});
    if (opt.label) svg.setAttribute("aria-label", opt.label);
    el("rect", {width: 920, height: 540, fill: "#fff"}, svg);
    var defs = el("defs", {}, svg);
    var mk = el("marker", {id: "fa" + (opt.post ? "p" : "w"), viewBox: "0 0 10 10", refX: 9, refY: 5, markerWidth: 6, markerHeight: 6, orient: "auto"}, defs);
    el("path", {d: "M0 0 10 5 0 10z", fill: INK}, mk);
    var mkr = el("marker", {id: "fr" + (opt.post ? "p" : "w"), viewBox: "0 0 10 10", refX: 9, refY: 5, markerWidth: 6, markerHeight: 6, orient: "auto"}, defs);
    el("path", {d: "M0 0 10 5 0 10z", fill: RED}, mkr);
    var AR = "url(#" + mk.id + ")", ARR = "url(#" + mkr.id + ")";

    // Haube
    txt(svg, 185, 34, t.hood, {"font-size": 20, "font-weight": 700});
    el("rect", {x: 20, y: 48, width: 330, height: 282, rx: 6, fill: BG, stroke: INK, "stroke-width": 2.5}, svg);
    el("rect", {x: 38, y: 84, width: 294, height: 40, rx: 4, fill: "#fff", stroke: LINE, "stroke-width": 1.5}, svg);
    var tubes = [];
    for (var x = 62; x < 320; x += 28) {
      var g = el("g", {}, svg);
      el("circle", {cx: x, cy: 104, r: 10, fill: "#fff", stroke: MUT, "stroke-width": 1.8}, g);
      tubes.push(el("circle", {cx: x, cy: 104, r: 0, fill: "#8a7d6b", opacity: 0.85}, g));
    }
    var silT = txt(svg, 185, 76, t.sil, {fill: MUT});
    // Luftströmung über dem Schalldämpfer (innerhalb der Haube)
    var flow = [];
    for (var i = 0; i < 9; i++) flow.push(el("line", {x1: 0, y1: 0, x2: 0, y2: 0, stroke: "#9aa7b0", "stroke-width": 2, "stroke-linecap": "round", opacity: 0}, svg));
    el("rect", {x: 82, y: 168, width: 216, height: 104, rx: 6, fill: "#e8e2e2", stroke: LINE, "stroke-width": 1.5}, svg);
    var fans = [];
    [150, 230].forEach(function (cx) {
      var g = el("g", {}, svg);
      el("circle", {cx: cx, cy: 200, r: 15, fill: "#fff", stroke: LINE, "stroke-width": 1.5}, g);
      var r = el("g", {}, g);
      for (var b = 0; b < 3; b++) el("path", {d: "M0 0 C 4 -5 4 -11 0 -13 C -3 -9 -3 -4 0 0z", fill: MUT, transform: "rotate(" + b * 120 + ")"}, r);
      el("circle", {cx: 0, cy: 0, r: 2.2, fill: INK}, r);
      fans.push({g: r, cx: cx, cy: 200});
    });
    var unitT = txt(svg, 190, 248, t.unit, {"font-size": Math.min(16, 16 * 22 / t.unit.length).toFixed(1)});
    var offT = txt(svg, 190, 264, t.off, {"font-size": 12.5, "font-weight": 700, fill: RED, opacity: 0});

    // Funk und Gateway
    var arcs = [];
    for (i = 0; i < 3; i++) arcs.push(el("path", {d: "M " + (362 + i * 16) + " " + (170 - i * 6) + " q 14 -17 0 -34", fill: "none", stroke: RED, "stroke-width": 3, opacity: 0.3}, svg));
    txt(svg, 364, 112, t.radio, {"text-anchor": "start", fill: MUT});
    el("line", {x1: 490, y1: 62, x2: 490, y2: 132, stroke: INK, "stroke-width": 3.5}, svg);
    var ant = el("path", {d: "M471 52 q19 -19 38 0 M461 42 q29 -31 58 0", fill: "none", stroke: RED, "stroke-width": 3, opacity: 0.5}, svg);
    el("rect", {x: 436, y: 132, width: 108, height: 44, rx: 9, fill: "#fff", stroke: RED, "stroke-width": 2.5}, svg);
    for (i = 0; i < 3; i++) el("circle", {cx: 470 + i * 10, cy: 154, r: 2.5, fill: i === 0 ? OK : LINE}, svg);
    txt(svg, 490, 200, t.gw, {"font-size": 17, "font-weight": 700});
    txt(svg, 490, 220, t.gw2, {"font-size": 14.5, fill: MUT});
    el("line", {x1: 546, y1: 154, x2: 574, y2: 154, stroke: INK, "stroke-width": 2.2, "marker-end": AR}, svg);

    function box(x, y, w, h, a, b, strong) {
      var g = el("g", {}, svg);
      var r = el("rect", {x: x, y: y, width: w, height: h, rx: 9, fill: "#fff", stroke: strong ? RED : INK, "stroke-width": 2.2}, g);
      var lines = b.split("|"), y0 = y + h / 2 - 4 - 9 * (lines.length - 1);
      txt(g, x + w / 2, y0, a, {"font-size": 18, "font-weight": 700});
      var subs = lines.map(function (l, i) { return txt(g, x + w / 2, y0 + 22 + 18 * i, l, {"font-size": 14.5, fill: MUT}); });
      return {r: r, subs: subs, orig: lines, strong: strong};
    }
    box(578, 110, 152, 88, t.ns, t.ns2, true);
    el("path", {d: "M732 140 C 748 140 744 74 760 74", fill: "none", stroke: INK, "stroke-width": 2.2, "marker-end": AR}, svg);
    el("line", {x1: 732, y1: 154, x2: 760, y2: 160, stroke: INK, "stroke-width": 2.2, "marker-end": AR}, svg);
    el("path", {d: "M732 168 C 748 168 744 246 760 246", fill: "none", stroke: INK, "stroke-width": 2.2, "marker-end": AR}, svg);
    var B = {dash: box(764, 40, 152, 68, t.d1, t.d1b), alarm: box(764, 126, 152, 68, t.d2, t.d2b), bms: box(764, 212, 152, 80, t.d3, t.d3b)};

    // Kabel und Gaswarnzentrale
    var CABLE = "M110 319 V 324 H 392 V 384";
    el("path", {d: CABLE, fill: "none", stroke: INK, "stroke-width": 3}, svg);
    var cableHot = el("path", {d: CABLE, fill: "none", stroke: RED, "stroke-width": 4.5, "stroke-dasharray": "14 10", opacity: 0}, svg);
    var cableLen = 5 + 282 + 60;
    txt(svg, 404, 366, t.wire, {"text-anchor": "start", "font-weight": 700});
    var gz = el("rect", {x: 380, y: 384, width: 330, height: 92, rx: 9, fill: "#fff", stroke: INK, "stroke-width": 2.5}, svg);
    txt(svg, 545, 414, t.gwz, {"font-size": 18, "font-weight": 700});
    txt(svg, 545, 438, t.gwz2, {"font-size": 14.5, fill: MUT});
    var gz3 = txt(svg, 545, 460, t.gwz3, {"font-size": 14.5, fill: MUT});
    var BMSP = "M712 430 H 840 V 296";
    el("path", {d: BMSP, fill: "none", stroke: INK, "stroke-width": 2.2, "marker-end": AR}, svg);
    var bmsHot = el("path", {d: BMSP, fill: "none", stroke: RED, "stroke-width": 4, "stroke-dasharray": "12 9", opacity: 0, "marker-end": ARR}, svg);

    // Legende
    var leg = el("g", {"font-size": 15.5, fill: INK}, svg);
    var legT = t.l.map(function (s, i) {
      var e = txt(leg, 20, 364 + 26 * i, s, {"text-anchor": "start", "font-size": 15.5, class: "iot-anim-leg"});
      e.dataset.k = LEG[i];
      return e;
    });
    var sampleT = txt(svg, 20, 526, "* " + t.sample, {"text-anchor": "start", "font-size": 12, fill: MUT});

    // Sensoren
    var SE = {};
    S.forEach(function (s) {
      var g = el("g", {class: "iot-anim-sensor", tabindex: opt.post ? -1 : 0, role: "button", "aria-label": t.info[s.k]}, svg);
      g.dataset.k = s.k;
      var ring = el("circle", {cx: s.x, cy: s.y, r: 23, fill: "none", stroke: RED, "stroke-width": 3, opacity: 0}, g);
      var c = el("circle", {cx: s.x, cy: s.y, r: 23, fill: RED}, g);
      txt(g, s.x, s.y + 7, s.s, {"font-size": s.s.length > 1 ? 18 : 21, "font-weight": 700, fill: "#fff"});
      SE[s.k] = {g: g, ring: ring, c: c, s: s};
    });

    // Datenpakete (wiederverwendbar)
    var pk = [];
    for (i = 0; i < 4; i++) {
      var g2 = el("g", {opacity: 0}, svg);
      var pill = el("rect", {x: 0, y: 0, width: 60, height: 22, rx: 11, fill: "#fff", stroke: RED, "stroke-width": 1.8}, g2);
      var dot = el("circle", {cx: 0, cy: 0, r: 6, fill: RED}, g2);
      var lab = txt(g2, 0, 0, "", {"font-size": 13, "font-weight": 700});
      pk.push({g: g2, pill: pill, dot: dot, lab: lab});
    }
    var sel = null;

    function route(p) {
      var s = SE[p.k].s;
      var pts = [[s.x, s.y], [356, 150], [436, 154], [578, 154], [732, 154]];
      return pts.concat(TAIL[p.to]);
    }

    function render(sc, tt, auto) {
      var D = SC[sc], i, k;
      // Grundzustand
      for (k in B) {
        B[k].r.setAttribute("fill", "#fff"); B[k].r.setAttribute("stroke", B[k].strong ? RED : INK); B[k].r.setAttribute("stroke-width", 2.2);
        B[k].subs.forEach(function (e, j) { e.textContent = B[k].orig[j] || ""; e.setAttribute("fill", MUT); e.setAttribute("font-weight", 400); });
      }
      for (k in SE) { SE[k].ring.setAttribute("opacity", 0); SE[k].c.setAttribute("fill", RED); SE[k].g.setAttribute("opacity", 1); }
      // Funkbögen
      arcs.forEach(function (a, j) { a.setAttribute("opacity", 0.25 + 0.75 * Math.max(0, Math.sin(tt * 4 - j * 0.9))); });
      ant.setAttribute("opacity", 0.4 + 0.6 * Math.max(0, Math.sin(tt * 4 - 3)));
      // Ventilatoren und Luft
      var leak = sc === 2, off = leak && tt >= OFF, clog = sc === 1 ? Math.min(1, tt / 6) : 0;
      var speed = off ? 5 : 1.4 * (1 - 0.35 * clog);
      fans.forEach(function (f) { f.g.setAttribute("transform", "translate(" + f.cx + " " + f.cy + ") rotate(" + ((tt * 360 * speed) % 360) + ")"); });
      flow.forEach(function (l, j) {
        var x0 = 62 + j * 32, ph = ((tt * (off ? 1.6 : 0.8) * (1 - 0.6 * clog) + j * 0.37) % 1);
        var y = 160 - ph * 34;
        l.setAttribute("x1", x0); l.setAttribute("x2", x0); l.setAttribute("y1", y); l.setAttribute("y2", y - 8);
        l.setAttribute("opacity", (1 - ph) * (off ? 0.9 : 0.55) * (1 - 0.7 * clog));
      });
      tubes.forEach(function (c, j) { c.setAttribute("r", Math.max(0, Math.min(9, clog * 12 - (j % 3) * 1.5))); });
      silT.textContent = clog > 0.4 ? t.sil + " – " + t.clog : t.sil;
      silT.setAttribute("fill", clog > 0.4 ? RED : MUT);
      offT.setAttribute("opacity", off ? 1 : 0);
      unitT.setAttribute("y", off ? 244 : 248);
      // Kabel, Gaswarnzentrale, Leittechnik
      var wp = leak ? Math.max(0, Math.min(1, (tt - WIRE[0]) / (WIRE[1] - WIRE[0]))) : 0;
      cableHot.setAttribute("opacity", wp > 0 ? 1 : 0);
      cableHot.setAttribute("stroke-dasharray", wp >= 1 ? "14 10" : (cableLen * wp) + " 2000");
      cableHot.setAttribute("stroke-dashoffset", wp >= 1 ? -tt * 40 : 0);
      var gzOn = leak && tt >= GWZ, blink = Math.sin(tt * 9) > -0.2;
      gz.setAttribute("stroke", gzOn ? RED : INK); gz.setAttribute("fill", gzOn && blink ? PALE : "#fff"); gz.setAttribute("stroke-width", gzOn ? 3.5 : 2.5);
      gz3.setAttribute("fill", gzOn ? RED : MUT); gz3.setAttribute("font-weight", gzOn ? 700 : 400);
      var bp = leak ? Math.max(0, Math.min(1, (tt - BMSL[0]) / (BMSL[1] - BMSL[0]))) : 0;
      bmsHot.setAttribute("opacity", bp > 0 ? 1 : 0);
      bmsHot.setAttribute("stroke-dasharray", bp >= 1 ? "12 9" : (300 * bp) + " 2000");
      bmsHot.setAttribute("stroke-dashoffset", bp >= 1 ? -tt * 40 : 0);
      if (leak && tt >= BMS) {
        B.bms.r.setAttribute("stroke", RED); B.bms.r.setAttribute("stroke-width", 3.2); B.bms.r.setAttribute("fill", blink ? PALE : "#fff");
        B.bms.subs[0].textContent = "R290 · " + t.alarm; B.bms.subs[0].setAttribute("fill", RED); B.bms.subs[0].setAttribute("font-weight", 700);
      }
      if (leak && tt >= 0.2) { SE.ir.ring.setAttribute("opacity", blink ? 1 : 0.2); SE.ir.ring.setAttribute("r", 23 + 6 * ((tt * 2) % 1)); }
      // Pakete
      var used = 0, last = {}, alarmOn = null;
      D.p.forEach(function (p) {
        var s = tt - p.t0;
        if (s >= 0 && s < 0.45) { var e = SE[p.k]; e.ring.setAttribute("opacity", 1 - s / 0.45); e.ring.setAttribute("r", 23 + 18 * s / 0.45); }
        if (s >= 0.25 && s < 0.25 + TRAVEL && used < pk.length) {
          var P = pk[used++], f = (s - 0.25) / TRAVEL, q = along(route(p), f), lbl = val(lang, p.k, p.x);
          var w = lbl.length * 7.4 + 22;
          P.g.setAttribute("opacity", f > 0.94 ? (1 - f) / 0.06 : 1);
          var over = (q[0] > 428 && q[0] < 548) || (q[0] > 572 && q[0] < 734);  // über Gateway und Netzwerkserver nur der Punkt
          P.pill.setAttribute("opacity", over ? 0 : 1); P.lab.setAttribute("opacity", over ? 0 : 1);
          P.dot.setAttribute("cx", q[0]); P.dot.setAttribute("cy", q[1]);
          P.pill.setAttribute("x", q[0] + 8); P.pill.setAttribute("y", q[1] - 30); P.pill.setAttribute("width", w);
          P.pill.setAttribute("stroke", p.to === "alarm" ? RED : INK);
          P.lab.setAttribute("x", q[0] + 8 + w / 2); P.lab.setAttribute("y", q[1] - 14.5); P.lab.textContent = lbl;
          P.lab.setAttribute("fill", p.to === "alarm" ? RED : INK);
        }
        if (s >= 0.25 + TRAVEL) {
          last[p.to] = p;
          if (p.to === "alarm") alarmOn = p;
        }
      });
      for (i = used; i < pk.length; i++) pk[i].g.setAttribute("opacity", 0);
      var dl = last.dash;
      if (sc === 0 && !dl && auto) dl = D.p[D.p.length - 1];
      if (dl) {
        B.dash.subs[0].textContent = val(lang, dl.k, dl.x) + " ✓"; B.dash.subs[0].setAttribute("fill", OK); B.dash.subs[0].setAttribute("font-weight", 700);
        var ago = tt - (dl.t0 + 0.25 + TRAVEL);
        if (ago >= 0 && ago < 0.4) { B.dash.r.setAttribute("stroke", OK); B.dash.r.setAttribute("stroke-width", 3.2); }
      }
      if (alarmOn) {
        B.alarm.r.setAttribute("stroke", RED); B.alarm.r.setAttribute("stroke-width", 3.2); B.alarm.r.setAttribute("fill", blink ? PALE : "#fff");
        B.alarm.subs[0].textContent = val(lang, alarmOn.k, alarmOn.x) + (alarmOn.k === "dp" ? " > 20 Pa" : "");
        B.alarm.subs[0].setAttribute("fill", RED); B.alarm.subs[0].setAttribute("font-weight", 700);
        if (alarmOn.k === "dp") { SE.dp.ring.setAttribute("opacity", blink ? 1 : 0.2); SE.dp.ring.setAttribute("r", 28); }
      }
      // Auswahl
      for (k in SE) if (sel) SE[k].g.setAttribute("opacity", k === sel ? 1 : 0.35);
      legT.forEach(function (e) { e.setAttribute("font-weight", e.dataset.k === sel ? 700 : 400); e.setAttribute("fill", e.dataset.k === sel ? RED : INK); });
      if (sel) { SE[sel].ring.setAttribute("opacity", 1); SE[sel].ring.setAttribute("r", 28); }
      // Text
      var c = t.cap;
      if (sc === 0) return c.n;
      if (sc === 1) return alarmOn ? c.p2 : c.p1;
      return (tt >= BMS ? c.k2 + " " + c.k3 : tt >= GWZ ? c.k2 : c.k1);
    }

    var api = {svg: svg, render: render, T: t, SC: SC, durations: SC.map(function (s) { return s.d; })};
    if (opt.post) { host.appendChild(svg); return api; }

    // ---------- Webseite: Steuerung ----------
    var wrap = document.createElement("div"); wrap.className = "iot-anim";
    var bar = document.createElement("div"); bar.className = "iot-anim-bar"; bar.setAttribute("role", "group");
    var cap = document.createElement("p"); cap.className = "iot-anim-cap"; cap.setAttribute("aria-live", "polite");
    var btns = [t.auto].concat(t.sc).map(function (s, i) {
      var b = document.createElement("button"); b.type = "button"; b.textContent = s; b.dataset.i = i - 1;
      bar.appendChild(b); return b;
    });
    var hint = document.createElement("span"); hint.className = "iot-anim-hint"; hint.textContent = t.hint; bar.appendChild(hint);
    wrap.appendChild(svg); wrap.appendChild(bar); wrap.appendChild(cap);
    host.innerHTML = ""; host.appendChild(wrap);

    var mode = -1, cur = 0, t0 = performance.now(), visible = true, raf = 0, lastCap = "";
    function press() { btns.forEach(function (b) { b.setAttribute("aria-pressed", String(+b.dataset.i === mode)); }); }
    function setCap(s) {
      if (sel) s = t.info[sel];
      s = s.replace(/ %/g, "\u00a0%");
      if (s !== lastCap) { cap.textContent = s; lastCap = s; }
    }
    function frame(now) {
      raf = 0;
      if (!wrap.isConnected) return;  // Grafik wurde entfernt
      var tt = (now - t0) / 1000;
      if (mode === -1 && tt > SC[cur].d) { cur = (cur + 1) % SC.length; t0 = now; tt = 0; }
      if (mode >= 0) { cur = mode; if (tt > SC[cur].d + 2) { t0 = now; tt = 0; } }
      setCap(render(cur, Math.min(tt, SC[cur].d + 2), true));
      if (visible && !reduce) raf = requestAnimationFrame(frame);
    }
    function still() { setCap(render(cur, SC[cur].d, true)); }
    function go() { if (reduce) still(); else if (!raf) raf = requestAnimationFrame(frame); }
    bar.addEventListener("click", function (e) {
      var b = e.target.closest("button"); if (!b) return;
      mode = +b.dataset.i; cur = mode < 0 ? 0 : mode; t0 = performance.now(); sel = null; press(); go();
    });
    function pick(k) { sel = sel === k ? null : k; if (reduce) still(); else go(); setCap(lastCap); if (!sel) lastCap = ""; }
    svg.addEventListener("click", function (e) {
      var g = e.target.closest(".iot-anim-sensor, .iot-anim-leg"); if (g) pick(g.dataset.k); else if (sel) pick(sel);
    });
    svg.addEventListener("keydown", function (e) {
      var g = e.target.closest(".iot-anim-sensor");
      if (g && (e.key === "Enter" || e.key === " ")) { e.preventDefault(); pick(g.dataset.k); }
    });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (en) { visible = en[0].isIntersecting; if (visible) go(); }).observe(wrap);
    }
    press(); go();
    return api;
  }

  window.FCTIoTAnim = FCTIoTAnim;
  function init() {
    var figs = document.querySelectorAll("[data-iot-anim]");
    for (var i = 0; i < figs.length; i++) {
      var img = figs[i].querySelector("img");
      FCTIoTAnim(figs[i], {label: img ? img.alt : ""});
    }
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init); else init();
})();
