/**
 * ==========================================================================
 * MAIN BLOG LOGIC (MAIN.JS)
 * Theme Manager, Search/Filter, Stock Ticker & UI Enhancements
 * ==========================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initTicker();
  initCategoryFilter();
  initSearch();
  initSidebarMiniCalc();
  initMobileMenu();
});

/* ==========================================================================
   THEME TOGGLE (DARK / LIGHT MODE)
   ========================================================================== */
function initTheme() {
  const themeToggleBtn = document.getElementById('themeToggleBtn');
  const savedTheme = localStorage.getItem('blog_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const currentTheme = document.documentElement.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', newTheme);
      localStorage.setItem('blog_theme', newTheme);
      updateThemeIcon(newTheme);
    });
  }
}

function updateThemeIcon(theme) {
  const icon = document.querySelector('#themeToggleBtn i, #themeToggleBtn span');
  if (icon) {
    icon.textContent = theme === 'dark' ? '☀️' : '🌙';
  }
}

/* ==========================================================================
   STOCK MARKET REALISTIC TICKER SIMULATION
   ========================================================================== */
function initTicker() {
  const tickerItems = [
    { name: 'KOSPI', base: 2685.40, diff: '+0.85%' },
    { name: 'KOSDAQ', base: 872.15, diff: '+1.20%' },
    { name: 'S&P 500', base: 5491.20, diff: '+2.18%' },
    { name: 'NASDAQ 100', base: 19832.70, diff: '+3.05%' },
    { name: 'USD/KRW', base: 1335.20, diff: '-0.32%' },
    { name: '삼성전자', base: 78500, diff: '+1.42%' },
    { name: 'SK하이닉스', base: 196000, diff: '+3.85%' },
    { name: '현대차', base: 264000, diff: '+2.10%' }
  ];

  const track = document.getElementById('tickerTrack');
  if (!track) return;

  const html = tickerItems.concat(tickerItems).map(item => {
    const isUp = item.diff.startsWith('+');
    return `
      <div class="ticker-item">
        <span class="ticker-name">${item.name}</span>
        <span class="ticker-val">${typeof item.base === 'number' && item.base > 1000 ? item.base.toLocaleString() : item.base}</span>
        <span class="${isUp ? 'ticker-up' : 'ticker-down'}">${item.diff} ${isUp ? '▲' : '▼'}</span>
      </div>
    `;
  }).join('');

  track.innerHTML = html;
}

/* ==========================================================================
   CATEGORY & SEARCH FILTER
   ========================================================================== */
function initCategoryFilter() {
  const tabs = document.querySelectorAll('.cat-tab');
  const cards = document.querySelectorAll('.post-card');

  tabs.forEach(tab => {
    tab.addEventListener('click', () => {
      tabs.forEach(t => t.classList.remove('active'));
      tab.classList.add('active');

      const category = tab.getAttribute('data-category');
      cards.forEach(card => {
        const cardCat = card.getAttribute('data-category');
        if (category === 'all' || cardCat === category) {
          card.style.display = 'flex';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

function initSearch() {
  const searchInput = document.getElementById('blogSearchInput');
  const cards = document.querySelectorAll('.post-card');

  if (!searchInput) return;

  searchInput.addEventListener('input', (e) => {
    const term = e.target.value.toLowerCase().trim();
    cards.forEach(card => {
      const title = card.querySelector('.post-title')?.textContent.toLowerCase() || '';
      const excerpt = card.querySelector('.post-excerpt')?.textContent.toLowerCase() || '';
      const badge = card.querySelector('.post-badge')?.textContent.toLowerCase() || '';

      if (title.includes(term) || excerpt.includes(term) || badge.includes(term)) {
        card.style.display = 'flex';
      } else {
        card.style.display = 'none';
      }
    });
  });
}

/* ==========================================================================
   SIDEBAR MINI STOCK AVERAGE CALCULATOR
   ========================================================================== */
function initSidebarMiniCalc() {
  const btn = document.getElementById('miniCalcBtn');
  if (!btn) return;

  btn.addEventListener('click', () => {
    const p1 = parseFloat(document.getElementById('miniP1')?.value) || 0;
    const q1 = parseFloat(document.getElementById('miniQ1')?.value) || 0;
    const p2 = parseFloat(document.getElementById('miniP2')?.value) || 0;
    const q2 = parseFloat(document.getElementById('miniQ2')?.value) || 0;

    const totalQty = q1 + q2;
    if (totalQty === 0) return;

    const avgPrice = Math.round(((p1 * q1) + (p2 * q2)) / totalQty);
    const resBox = document.getElementById('miniCalcRes');
    const valSpan = document.getElementById('miniCalcVal');

    if (resBox && valSpan) {
      valSpan.textContent = avgPrice.toLocaleString() + '원';
      resBox.classList.add('show');
    }
  });
}

/* ==========================================================================
   MOBILE MENU DRAWER
   ========================================================================== */
function initMobileMenu() {
  const menuBtn = document.getElementById('mobileMenuBtn');
  const nav = document.querySelector('.main-nav');
  if (menuBtn && nav) {
    menuBtn.addEventListener('click', () => {
      const isVisible = nav.style.display === 'flex';
      nav.style.display = isVisible ? 'none' : 'flex';
      nav.style.flexDirection = 'column';
      nav.style.position = 'absolute';
      nav.style.top = 'var(--header-height)';
      nav.style.left = '0';
      nav.style.right = '0';
      nav.style.background = 'var(--bg-secondary)';
      nav.style.padding = '20px';
      nav.style.borderBottom = '1px solid var(--border-color)';
    });
  }
}
