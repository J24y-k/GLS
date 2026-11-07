/* ==========================================================================
   GLS Refrigeration & Air Conditioning - motion layer (GSAP 3 + ScrollTrigger)
   Designed and developed by COR3 Haus Production

   Principles
   - Restrained: quiet scroll reveals and image clip reveals (the hero entrance is CSS-only). No parallax,
     no scroll-jacking, no looping or decorative motion.
   - Safe: the hidden start states live in CSS under html.anim. That class is
     never added for prefers-reduced-motion users, and it is removed here (or by
     the 4s timer in <head>) if GSAP is unavailable, so content is never stuck hidden.
   - Loaded after the window 'load' event (see page() in _build/build.py) so it never delays first paint.
   - Behaviour (nav, forms, maps, triage, video) stays in main.js. Nothing here
     touches the hamburger menu.
   ========================================================================== */
(function () {
  'use strict';
  var root = document.documentElement;

  if (!window.gsap || !window.ScrollTrigger || !root.classList.contains('anim')) {
    root.classList.remove('anim');
    return;
  }
  window.__glsMotion = true;
  gsap.registerPlugin(ScrollTrigger);

  var mm = gsap.matchMedia();

  mm.add('(prefers-reduced-motion: no-preference)', function () {
    /* ---- Text and block reveals ---- */
    ScrollTrigger.batch('[data-reveal]', {
      start: 'top 90%',
      once: true,
      onEnter: function (batch) {
        gsap.to(batch, { opacity: 1, y: 0, duration: 0.85, ease: 'power3.out', stagger: 0.1 });
      }
    });

    /* ---- Image reveals: clip opens from the top while the photo settles ---- */
    gsap.utils.toArray('[data-reveal-img]').forEach(function (el) {
      var frame = el.classList.contains('tile') ? el : el.querySelector('.ph__frame');
      var img = el.querySelector('img');
      if (!frame) return;
      var tl = gsap.timeline({ scrollTrigger: { trigger: el, start: 'top 90%', once: true } });
      // Do not clearProps here: the hidden start state is a CSS rule, so clearing the inline value would re-hide the image.
      tl.to(frame, { clipPath: 'inset(0% 0% 0% 0%)', duration: 1.1, ease: 'power3.inOut', onComplete: function () { frame.style.clipPath = 'none'; } }, 0);
      if (img) {
        // CSS hover transitions on images would smooth (and lag) a tween, so pause them while it runs.
        tl.fromTo(img, { scale: 1.14 }, {
          scale: 1, duration: 1.5, ease: 'power2.out',
          onStart: function () { img.style.transition = 'none'; },
          onComplete: function () { img.style.transition = ''; gsap.set(img, { clearProps: 'transform' }); }
        }, 0);
      }
    });

    window.addEventListener('load', function () { ScrollTrigger.refresh(); });

    // Cleanup if the media query stops matching (user turns reduced motion on mid-session).
    return function () {
      root.classList.remove('anim');
      gsap.set('[data-reveal], .hero__copy > *', { clearProps: 'all' });
      gsap.set('[data-reveal-img], [data-reveal-img] .ph__frame, [data-reveal-img] img', { clearProps: 'all' });
    };
  });
})();
