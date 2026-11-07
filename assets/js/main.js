/* ==========================================================================
   GLS Refrigeration & Air Conditioning - site script
   Designed and developed by COR3 Haus Production

   Modules (each is a no-op when its markup is absent):
   1. Navigation drawer (mobile hamburger)  - one implementation, one set of listeners
   2. Map chooser dialog (Google Maps / Apple Maps / Waze)
   3. Fault triage on the homepage
   4. Enquiry form -> WhatsApp hand-off (contact page)
   5. Video: pause other videos when one starts
   6. Lightbox for the Our work gallery

   No dependencies. Contact numbers are read from <body data-*> so they live in
   exactly one place (the build script).
   ========================================================================== */
(function () {
  'use strict';

  // Guard: never initialise twice (prevents duplicate listeners).
  if (window.__glsInit) return;
  window.__glsInit = true;

  var doc = document;
  var root = doc.documentElement;
  var cfg = doc.body.dataset;               // wa, tel, telDisplay, email

  /* ------------------------------------------------------------------ 1. Nav */
  function initNav() {
    var toggle = doc.getElementById('nav-toggle');
    var nav = doc.getElementById('site-nav');
    var scrim = doc.getElementById('nav-scrim');
    if (!toggle || !nav) return;

    var mq = window.matchMedia('(min-width: 62em)');
    var inertTargets = [].slice.call(doc.querySelectorAll('[data-inert-when-nav-open]'));
    var isOpen = false;

    function setInert(on) {
      inertTargets.forEach(function (el) {
        if (on) el.setAttribute('inert', '');
        else el.removeAttribute('inert');
      });
    }

    function setOpen(open, returnFocus) {
      if (open && mq.matches) return;          // desktop navigation is never a drawer
      if (open === isOpen) return;
      isOpen = open;
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      nav.setAttribute('data-open', String(open));
      if (scrim) scrim.setAttribute('data-open', String(open));
      root.classList.toggle('nav-open', open);
      setInert(open);
      if (open) {
        var first = nav.querySelector('a');
        if (first) first.focus({ preventScroll: true });
      } else if (returnFocus) {
        toggle.focus({ preventScroll: true });
      }
    }

    toggle.addEventListener('click', function () { setOpen(!isOpen, isOpen); });

    // Any link inside the drawer closes it (covers same-page anchors and bfcache returns).
    nav.addEventListener('click', function (e) {
      if (isOpen && e.target.closest('a')) setOpen(false, false);
    });

    // Click on the dimmed area outside the drawer.
    if (scrim) scrim.addEventListener('click', function () { setOpen(false, true); });

    doc.addEventListener('keydown', function (e) {
      if (!isOpen) return;
      if (e.key === 'Escape') { e.preventDefault(); setOpen(false, true); return; }
      if (e.key !== 'Tab') return;
      // Keep focus inside toggle + drawer while open.
      var items = [toggle].concat([].slice.call(nav.querySelectorAll('a[href], button:not([disabled])')));
      var first = items[0], last = items[items.length - 1];
      if (e.shiftKey && doc.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && doc.activeElement === last) { e.preventDefault(); first.focus(); }
    });

    // Crossing to desktop width resets everything.
    var onChange = function () { if (mq.matches) setOpen(false, false); };
    if (mq.addEventListener) mq.addEventListener('change', onChange);
    else if (mq.addListener) mq.addListener(onChange);

    // Back/forward cache restores the page in whatever state it was left.
    window.addEventListener('pageshow', function (e) { if (e.persisted) setOpen(false, false); });
  }

  /* ------------------------------------------------------------- 2. Map chooser */
  function initMapChooser() {
    var dlg = doc.getElementById('map-dialog');
    if (!dlg || typeof dlg.showModal !== 'function') return;   // links fall back to Google Maps
    var lastTrigger = null;

    [].forEach.call(doc.querySelectorAll('[data-map-open]'), function (el) {
      el.addEventListener('click', function (e) {
        e.preventDefault();
        lastTrigger = el;
        if (!dlg.open) dlg.showModal();
      });
    });
    var closeBtn = dlg.querySelector('[data-map-close]');
    if (closeBtn) closeBtn.addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });   // backdrop
    [].forEach.call(dlg.querySelectorAll('a'), function (a) {
      a.addEventListener('click', function () { setTimeout(function () { if (dlg.open) dlg.close(); }, 60); });
    });
    dlg.addEventListener('close', function () { if (lastTrigger) lastTrigger.focus(); });
  }

  /* ---------------------------------------------------------------- 3. Triage */
  var ISSUES = {
    fridge: {
      title: 'Fridge or freezer not keeping cold',
      say: "my fridge or freezer isn't keeping cold",
      service: 'Refrigeration repair',
      page: 'commercial-refrigeration.html',
      pageLabel: 'Commercial refrigeration services',
      items: [
        'The make and model on the unit’s plate.',
        'When it stopped keeping cold.',
        'Whether you can hear the compressor running.',
        'Any code or alarm on the controller display.'
      ]
    },
    coldroom: {
      title: 'Cold room or walk-in freezer problem',
      say: 'I have a problem with a cold room or walk-in freezer',
      service: 'Cold room or walk-in freezer',
      page: 'commercial-refrigeration.html#cold-rooms',
      pageLabel: 'Cold rooms and walk-in freezers',
      items: [
        'What the room stores, and roughly how big it is.',
        'When the temperature started rising.',
        'Any code or alarm on the controller display.',
        'The make of the condensing unit, if you can see it.'
      ]
    },
    aircon: {
      title: 'Air conditioner not cooling',
      say: "my air conditioner isn't cooling",
      service: 'Air-conditioning repair',
      page: 'air-conditioning.html',
      pageLabel: 'Air-conditioning services',
      items: [
        'The brand and model on the indoor unit.',
        'Whether it switches on, and whether the air is warm or there is no air.',
        'Any error code on the display, or any water leaking.',
        'Whether it is a split unit or a ducted system.'
      ]
    },
    other: {
      title: 'Something else, or not sure',
      say: "I'm not sure what is wrong with my system",
      service: 'Other',
      page: 'contact.html',
      pageLabel: 'Contact GLS',
      items: [
        'Whether it is a fridge, cold room or air conditioner.',
        'What you have noticed, and when it started.',
        'Where the property is.'
      ]
    }
  };

  function waLink(text) {
    return 'https://wa.me/' + cfg.wa + '?text=' + encodeURIComponent(text);
  }

  function initTriage() {
    var group = doc.getElementById('triage-options');
    var out = doc.getElementById('triage-result');
    if (!group || !out) return;
    var buttons = [].slice.call(group.querySelectorAll('[data-issue]'));

    function render(key) {
      var it = ISSUES[key];
      if (!it) return;
      out.textContent = '';

      var h = doc.createElement('h3');
      h.className = 'h3';
      h.textContent = 'Tell us this when you get in touch';
      out.appendChild(h);

      var ul = doc.createElement('ul');
      ul.className = 'triage__list';
      it.items.forEach(function (t) {
        var li = doc.createElement('li'); li.textContent = t; ul.appendChild(li);
      });
      out.appendChild(ul);

      var safety = doc.createElement('p');
      safety.className = 'triage__safety';
      safety.textContent = 'If you smell burning or see sparks, switch the unit off at the isolator and keep clear until a technician arrives.';
      out.appendChild(safety);

      var actions = doc.createElement('div');
      actions.className = 'actions';

      var wa = doc.createElement('a');
      wa.className = 'btn';
      wa.href = waLink('Hi GLS, ' + it.say + '. Can you help?');
      wa.target = '_blank'; wa.rel = 'noopener noreferrer';
      wa.innerHTML = '<svg class="ico" aria-hidden="true"><use href="assets/img/sprite.svg#i-whatsapp"></use></svg>';
      wa.appendChild(doc.createTextNode('WhatsApp GLS'));
      actions.appendChild(wa);

      var call = doc.createElement('a');
      call.className = 'btn btn--call';
      call.href = 'tel:' + cfg.tel;
      call.innerHTML = '<svg class="ico" aria-hidden="true"><use href="assets/img/sprite.svg#i-phone"></use></svg>';
      call.appendChild(doc.createTextNode('Call\u00a0' + cfg.telDisplay));
      actions.appendChild(call);

      var more = doc.createElement('a');
      more.className = 'btn btn--ghost';
      more.href = it.page;
      more.textContent = it.pageLabel;
      actions.appendChild(more);

      out.appendChild(actions);
      out.hidden = false;
    }

    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var key = btn.getAttribute('data-issue');
        var already = btn.getAttribute('aria-pressed') === 'true';
        buttons.forEach(function (b) { b.setAttribute('aria-pressed', 'false'); });
        if (already) { out.hidden = true; out.textContent = ''; return; }
        btn.setAttribute('aria-pressed', 'true');
        render(key);
      });
    });
  }

  /* ----------------------------------------------- 4. Enquiry form -> WhatsApp */
  function initForm() {
    var form = doc.getElementById('enquiry-form');
    if (!form) return;
    var status = doc.getElementById('form-status');
    var fallbackWa = doc.getElementById('status-wa');
    var fallbackMail = doc.getElementById('status-mail');
    var f = {
      name: form.elements.name, phone: form.elements.phone, email: form.elements.email,
      service: form.elements.service, message: form.elements.message
    };

    // Pre-fill from links such as contact.html?issue=aircon or ?service=consultation
    var params = new URLSearchParams(window.location.search);
    var issue = params.get('issue');
    if (issue && ISSUES[issue]) {
      f.service.value = ISSUES[issue].service;
      if (!f.message.value) f.message.value = 'Hi GLS, ' + ISSUES[issue].say + '. ';
    }
    var svc = params.get('service');
    if (svc === 'consultation') f.service.value = 'Free site assessment';

    function err(field) { return doc.getElementById(field.id + '-error'); }
    function setError(field, msg) {
      var e = err(field);
      field.setAttribute('aria-invalid', 'true');
      if (e) { e.textContent = msg; e.hidden = false; }
    }
    function clearError(field) {
      var e = err(field);
      field.removeAttribute('aria-invalid');
      if (e) { e.textContent = ''; e.hidden = true; }
    }
    function validate() {
      var bad = [];
      [f.name, f.phone, f.email, f.message].forEach(clearError);
      if (!f.name.value.trim()) { setError(f.name, 'Enter your name.'); bad.push(f.name); }
      var digits = f.phone.value.replace(/\D/g, '');
      if (digits.length < 9) { setError(f.phone, 'Enter a phone number we can reach you on, with at least 9 digits.'); bad.push(f.phone); }
      var mail = f.email.value.trim();
      if (mail && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(mail)) { setError(f.email, 'That email address looks incomplete. Leave it blank if you prefer.'); bad.push(f.email); }
      if (!f.message.value.trim()) { setError(f.message, 'Tell us briefly what you need.'); bad.push(f.message); }
      return bad;
    }
    [f.name, f.phone, f.email, f.message].forEach(function (el) {
      el.addEventListener('input', function () { if (el.getAttribute('aria-invalid')) clearError(el); });
    });

    function buildText() {
      var t = '*New enquiry from glsrefrigeration.co.za*\n\n';
      t += '*Name:* ' + f.name.value.trim() + '\n';
      t += '*Phone:* ' + f.phone.value.trim() + '\n';
      if (f.email.value.trim()) t += '*Email:* ' + f.email.value.trim() + '\n';
      if (f.service.value) t += '*Service:* ' + f.service.value + '\n';
      t += '\n*Message:*\n' + f.message.value.trim();
      return t;
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var bad = validate();
      if (bad.length) { bad[0].focus(); if (status) status.hidden = true; return; }

      var text = buildText();
      var url = waLink(text);
      if (fallbackWa) fallbackWa.href = url;
      if (fallbackMail) {
        fallbackMail.href = 'mailto:' + cfg.email + '?subject=' + encodeURIComponent('Enquiry from glsrefrigeration.co.za') +
          '&body=' + encodeURIComponent(text.replace(/\*/g, ''));
      }
      // Hand off to WhatsApp. We do not claim the message was sent: only the person
      // pressing Send inside WhatsApp delivers it.
      var w = window.open(url, '_blank');
      if (w) { try { w.opener = null; } catch (x) { /* ignore */ } }
      if (status) {
        status.hidden = false;
        status.querySelector('[data-status-title]').textContent = w
          ? 'WhatsApp is opening with your message ready.'
          : 'Your browser blocked WhatsApp from opening.';
        status.focus();
      }
    });
  }

  /* ----------------------------------------------------------------- 5. Video */
  function initVideo() {
    var vids = [].slice.call(doc.querySelectorAll('.video video'));
    vids.forEach(function (v) {
      v.addEventListener('play', function () {
        vids.forEach(function (o) { if (o !== v && !o.paused) o.pause(); });
      });
    });
  }

  /* ------------------------------------------------------------- 6. Lightbox */
  function initLightbox() {
    var dlg = doc.getElementById('lightbox');
    var tiles = [].slice.call(doc.querySelectorAll('[data-lightbox]'));
    if (!dlg || !tiles.length || typeof dlg.showModal !== 'function') return;
    var img = dlg.querySelector('.lightbox__img');
    var cap = dlg.querySelector('.lightbox__cap');
    var index = 0, lastTrigger = null;

    function show(n) {
      index = (n + tiles.length) % tiles.length;
      var t = tiles[index];
      img.src = t.getAttribute('data-full');
      img.alt = t.getAttribute('data-alt') || '';
      cap.textContent = (index + 1) + ' of ' + tiles.length + '. ' + (t.getAttribute('data-caption') || '');
    }
    tiles.forEach(function (t, i) {
      t.addEventListener('click', function () {
        lastTrigger = t; show(i);
        if (!dlg.open) dlg.showModal();
      });
    });
    dlg.querySelector('[data-lb-prev]').addEventListener('click', function () { show(index - 1); });
    dlg.querySelector('[data-lb-next]').addEventListener('click', function () { show(index + 1); });
    dlg.querySelector('[data-lb-close]').addEventListener('click', function () { dlg.close(); });
    dlg.addEventListener('click', function (e) { if (e.target === dlg) dlg.close(); });
    dlg.addEventListener('keydown', function (e) {
      if (e.key === 'ArrowRight') { e.preventDefault(); show(index + 1); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); show(index - 1); }
    });
    dlg.addEventListener('close', function () { if (lastTrigger) lastTrigger.focus(); });
  }

  initNav();
  initMapChooser();
  initTriage();
  initForm();
  initVideo();
  initLightbox();
})();
