document.addEventListener('DOMContentLoaded', function () {
  // Footer year
  var yearEl = document.getElementById('year');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

  // Header scroll state
  var header = document.getElementById('siteHeader');
  var onScroll = function () {
    if (window.scrollY > 40) header.classList.add('scrolled');
    else header.classList.remove('scrolled');
  };
  onScroll();
  window.addEventListener('scroll', onScroll);

  // Mobile nav toggle
  var navToggle = document.getElementById('navToggle');
  var mainNav = document.getElementById('mainNav');
  navToggle.addEventListener('click', function () {
    navToggle.classList.toggle('open');
    mainNav.classList.toggle('open');
  });
  mainNav.querySelectorAll('a').forEach(function (link) {
    link.addEventListener('click', function () {
      navToggle.classList.remove('open');
      mainNav.classList.remove('open');
    });
  });

  // Scroll reveal animations
  var revealTargets = document.querySelectorAll(
    '.about-text, .about-stats, .biz-card, .value-item, .news-card, .contact-info, .contact-form'
  );
  revealTargets.forEach(function (el) { el.classList.add('reveal'); });

  var observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.classList.add('in-view');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.15 });

  revealTargets.forEach(function (el) { observer.observe(el); });

  // Contact form (submits to Netlify Forms)
  var form = document.getElementById('contactForm');
  var status = document.getElementById('formStatus');
  if (form) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();
      var data = new URLSearchParams(new FormData(form)).toString();
      fetch('/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: data
      }).then(function () {
        status.textContent = '문의가 접수되었습니다. 빠른 시일 내에 답변드리겠습니다.';
        form.reset();
      }).catch(function () {
        status.textContent = '전송 중 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.';
      });
    });
  }
});
