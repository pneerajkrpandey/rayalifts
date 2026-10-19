(() => {
  const header = document.getElementById('siteHeader');
  const menuToggle = document.getElementById('menuToggle');
  const nav = document.getElementById('mainNav');
  const backTop = document.getElementById('backTop');
  const updateScroll = () => {
    const y = window.scrollY || 0;
    if (header) header.classList.toggle('scrolled', y > 55);
    if (backTop) backTop.classList.toggle('visible', y > 420);
  };
  window.addEventListener('scroll', updateScroll, { passive: true }); updateScroll();
  if (menuToggle && nav) {
    menuToggle.addEventListener('click', () => {
      const open = nav.classList.toggle('open');
      menuToggle.setAttribute('aria-expanded', String(open));
    });
    nav.querySelectorAll('a').forEach(a => a.addEventListener('click', () => {
      nav.classList.remove('open'); menuToggle.setAttribute('aria-expanded', 'false');
    }));
  }
  if (backTop) backTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));
  const slides = [...document.querySelectorAll('.hero-bg')];
  const dots = [...document.querySelectorAll('[data-slide]')];
  const current = document.getElementById('heroCurrent');
  let active = 0, timer;
  const showSlide = n => {
    if (!slides.length) return;
    active = (n + slides.length) % slides.length;
    slides.forEach((s, i) => s.classList.toggle('active', i === active));
    dots.forEach((d, i) => d.classList.toggle('active', i === active));
    if (current) current.textContent = String(active + 1).padStart(2, '0');
  };
  const restart = () => { clearInterval(timer); timer = setInterval(() => showSlide(active + 1), 6500); };
  dots.forEach(dot => dot.addEventListener('click', () => { showSlide(Number(dot.dataset.slide)); restart(); }));
  const next = document.getElementById('heroNext');
  if (next) next.addEventListener('click', () => { showSlide(active + 1); restart(); });
  if (slides.length > 1) restart();
  const revealEls = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => entries.forEach(entry => {
      if (entry.isIntersecting) { entry.target.classList.add('is-visible'); observer.unobserve(entry.target); }
    }), { threshold: .12, rootMargin: '0px 0px -35px 0px' });
    revealEls.forEach((el, i) => { el.style.transitionDelay = `${(i % 4) * 70}ms`; observer.observe(el); });
  } else revealEls.forEach(el => el.classList.add('is-visible'));
  const counters = document.querySelectorAll('[data-count]');
  if ('IntersectionObserver' in window && counters.length) {
    const counterObserver = new IntersectionObserver(entries => entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const el = entry.target, target = Number(el.dataset.count), start = performance.now(), duration = 1200;
      const tick = now => { const p = Math.min(1, (now - start) / duration); el.textContent = `${Math.floor(target * (1 - Math.pow(1 - p, 3)))}+`; if (p < 1) requestAnimationFrame(tick); };
      requestAnimationFrame(tick); counterObserver.unobserve(el);
    }), { threshold: .5 });
    counters.forEach(el => counterObserver.observe(el));
  }
})();
