/* © Silent Engineering di Romolo Vicari – ForCoTech
   Einfache Foto-Lightbox für „Projekte im Aufbau“. Ohne externe Dienste, ohne Cookies.
   Fotos eines Projekts (article) bilden eine Gruppe: Pfeile, Tastatur (← → Esc) und Wischen. */
(function () {
  var root = document.querySelector("[data-lb]");
  if (!root) return;
  var L = {};
  try { L = JSON.parse(root.getAttribute("data-lb")); } catch (e) {}
  var group = [], idx = 0, startX = null, lastFocus = null;

  var box = document.createElement("div");
  box.className = "lb";
  box.setAttribute("role", "dialog");
  box.setAttribute("aria-modal", "true");
  box.hidden = true;
  box.innerHTML =
    '<button class="lb-btn lb-close" type="button" aria-label="' + (L.close || "Close") + '">×</button>' +
    '<button class="lb-btn lb-prev" type="button" aria-label="' + (L.prev || "Previous") + '">‹</button>' +
    '<figure class="lb-fig"><img alt=""><figcaption></figcaption></figure>' +
    '<button class="lb-btn lb-next" type="button" aria-label="' + (L.next || "Next") + '">›</button>';
  document.body.appendChild(box);
  var img = box.querySelector("img"), cap = box.querySelector("figcaption");
  var bPrev = box.querySelector(".lb-prev"), bNext = box.querySelector(".lb-next"), bClose = box.querySelector(".lb-close");

  function show(i) {
    idx = (i + group.length) % group.length;
    var a = group[idx], t = a.querySelector("img");
    img.src = a.getAttribute("href");
    img.alt = t ? t.alt : "";
    cap.textContent = (t ? t.alt : "") + (group.length > 1 ? "  ·  " + (idx + 1) + " " + (L.of || "/") + " " + group.length : "");
    bPrev.hidden = bNext.hidden = group.length < 2;
  }
  function open(a) {
    var art = a.closest("article") || root;
    group = Array.prototype.slice.call(art.querySelectorAll("a.lb-link"));
    lastFocus = a;
    box.hidden = false;
    document.documentElement.classList.add("lb-open");
    show(group.indexOf(a));
    bClose.focus();
  }
  function close() {
    box.hidden = true;
    img.removeAttribute("src");
    document.documentElement.classList.remove("lb-open");
    if (lastFocus) lastFocus.focus();
  }

  root.addEventListener("click", function (ev) {
    var a = ev.target.closest("a.lb-link");
    if (!a || ev.ctrlKey || ev.metaKey || ev.shiftKey) return;
    ev.preventDefault();
    open(a);
  });
  bClose.addEventListener("click", close);
  bPrev.addEventListener("click", function () { show(idx - 1); });
  bNext.addEventListener("click", function () { show(idx + 1); });
  box.addEventListener("click", function (ev) { if (ev.target === box || ev.target.classList.contains("lb-fig")) close(); });
  document.addEventListener("keydown", function (ev) {
    if (box.hidden) return;
    if (ev.key === "Escape") close();
    else if (ev.key === "ArrowLeft") show(idx - 1);
    else if (ev.key === "ArrowRight") show(idx + 1);
    else if (ev.key === "Tab") {
      var f = [bClose, bPrev, bNext].filter(function (b) { return !b.hidden; });
      var i = f.indexOf(document.activeElement);
      ev.preventDefault();
      f[(i + (ev.shiftKey ? -1 : 1) + f.length) % f.length].focus();
    }
  });
  box.addEventListener("touchstart", function (ev) { startX = ev.touches[0].clientX; }, { passive: true });
  box.addEventListener("touchend", function (ev) {
    if (startX === null) return;
    var dx = ev.changedTouches[0].clientX - startX;
    startX = null;
    if (Math.abs(dx) > 50 && group.length > 1) show(idx + (dx < 0 ? 1 : -1));
  });
})();
