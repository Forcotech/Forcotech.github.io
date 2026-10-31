/* © Silent Engineering di Romolo Vicari – ForCoTech
   Hörprobe ohne/mit Haube: ersetzt die Browser-Steuerung durch einen eigenen Player.
   Ohne JavaScript bleibt die normale <audio>-Steuerung sichtbar. */
(function () {
  var lang = (document.documentElement.lang || 'de').slice(0, 2);
  var T = {
    de: { play: 'Abspielen', pause: 'Pause', seek: 'Springe zu Sekunde ' },
    en: { play: 'Play', pause: 'Pause', seek: 'Jump to second ' },
    fr: { play: 'Lecture', pause: 'Pause', seek: 'Aller à la seconde ' }
  }[lang] || { play: 'Play', pause: 'Pause', seek: '' };
  var ICON_PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M8 5.5v13l11-6.5z"/></svg>';
  var ICON_PAUSE = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M7 5h3.5v14H7zM13.5 5H17v14h-3.5z"/></svg>';
  var SEG = 3; // Sekunden je Abschnitt

  function fmt(t) { t = Math.max(0, Math.floor(t || 0)); return Math.floor(t / 60) + ':' + ('0' + (t % 60)).slice(-2); }

  document.querySelectorAll('.ab').forEach(function (c) {
    var a = c.querySelector('audio'), st = c.querySelector('.ab-state'), bar = c.querySelector('.ab-bar');
    if (!a || !bar) return;
    var bars = bar.querySelectorAll('i');
    a.controls = false;
    a.preload = 'metadata';
    c.classList.add('ab-js');

    var ctl = document.createElement('div');
    ctl.className = 'ab-ctl';
    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'ab-play';
    btn.innerHTML = ICON_PLAY;
    btn.setAttribute('aria-label', T.play);
    var right = document.createElement('div');
    right.className = 'ab-track';
    var time = document.createElement('div');
    time.className = 'ab-time';
    var leg = document.createElement('div');
    leg.className = 'ab-legend';
    leg.innerHTML = '<span class="off"></span><span class="on"></span>';
    leg.children[0].textContent = st ? st.dataset.off : '';
    leg.children[1].textContent = st ? st.dataset.on : '';
    a.parentNode.insertBefore(ctl, a);
    ctl.appendChild(btn);
    ctl.appendChild(right);
    right.appendChild(bar);
    right.appendChild(leg);
    leg.appendChild(time);
    bar.removeAttribute('aria-hidden');

    bars.forEach(function (b, i) {
      b.setAttribute('role', 'button');
      b.setAttribute('tabindex', '-1');
      b.setAttribute('aria-label', T.seek + i * SEG);
      b.addEventListener('click', function () {
        a.currentTime = i * SEG;
        if (a.paused) a.play();
      });
    });

    function u() {
      var seg = Math.floor(a.currentTime / SEG), on = seg % 2 === 1;
      if (st) { st.textContent = on ? st.dataset.on : st.dataset.off; st.classList.toggle('on', on); }
      bars.forEach(function (b, i) { b.classList.toggle('cur', i === seg && !a.paused); b.classList.toggle('done', i < seg); });
      time.textContent = fmt(a.currentTime) + ' / ' + fmt(a.duration || bars.length * SEG);
      btn.innerHTML = a.paused ? ICON_PLAY : ICON_PAUSE;
      btn.setAttribute('aria-label', a.paused ? T.play : T.pause);
      c.classList.toggle('playing', !a.paused);
    }
    btn.addEventListener('click', function () { if (a.paused) a.play(); else a.pause(); });
    ['timeupdate', 'pause', 'play', 'loadedmetadata', 'ended'].forEach(function (ev) { a.addEventListener(ev, u); });
    a.addEventListener('play', function () {
      document.querySelectorAll('.ab audio').forEach(function (o) { if (o !== a) o.pause(); });
    });
    u();
  });
})();
