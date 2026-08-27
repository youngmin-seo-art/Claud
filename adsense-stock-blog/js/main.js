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
    // 1. 주요 지수 및 환율
    { cat: '지수', name: 'KOSPI', base: '2,685.40', diff: '+0.85%' },
    { cat: '지수', name: 'KOSDAQ', base: '872.15', diff: '+1.20%' },
    { cat: '지수', name: 'S&P 500', base: '5,630.80', diff: '+1.15%' },
    { cat: '지수', name: 'NASDAQ 100', base: '19,832.70', diff: '+3.05%' },
    { cat: '지수', name: '다우존스', base: '41,250.50', diff: '+0.72%' },
    { cat: '지수', name: '필라델피아반도체', base: '5,120.40', diff: '+4.20%' },
    { cat: '환율', name: 'USD/KRW', base: '1,335.20', diff: '-0.32%' },

    // 2. 국내 KOSPI 시총 상위 5개 종목
    { cat: '코스피', name: '삼성전자', base: '78,500', diff: '+1.42%' },
    { cat: '코스피', name: 'SK하이닉스', base: '196,000', diff: '+3.85%' },
    { cat: '코스피', name: 'LG에너지솔루션', base: '389,000', diff: '+2.10%' },
    { cat: '코스피', name: '삼성바이오로직스', base: '985,000', diff: '+1.86%' },
    { cat: '코스피', name: '현대차', base: '264,000', diff: '+2.33%' },

    // 3. 국내 KOSDAQ 시총 상위 10개 종목
    { cat: '코스닥', name: '알테오젠', base: '315,000', diff: '+4.65%' },
    { cat: '코스닥', name: '에코프로비엠', base: '172,000', diff: '+3.12%' },
    { cat: '코스닥', name: '에코프로', base: '84,500', diff: '+2.42%' },
    { cat: '코스닥', name: 'HLB', base: '88,200', diff: '+1.96%' },
    { cat: '코스닥', name: '리가켐바이오', base: '96,400', diff: '+3.87%' },
    { cat: '코스닥', name: '엔켐', base: '215,000', diff: '+2.87%' },
    { cat: '코스닥', name: '삼천당제약', base: '148,500', diff: '+3.12%' },
    { cat: '코스닥', name: '클래시스', base: '54,200', diff: '+1.50%' },
    { cat: '코스닥', name: '휴젤', base: '268,000', diff: '+2.29%' },
    { cat: '코스닥', name: '리노공업', base: '204,000', diff: '+3.55%' },

    // 4. 미국 S&P 500 / NASDAQ 상위 10개 대형주
    { cat: '미국주식', name: '마이크로소프트 (MSFT)', base: '$448.50', diff: '+1.85%' },
    { cat: '미국주식', name: '애플 (AAPL)', base: '$228.40', diff: '+1.42%' },
    { cat: '미국주식', name: '엔비디아 (NVDA)', base: '$128.80', diff: '+5.25%' },
    { cat: '미국주식', name: '알파벳 (GOOGL)', base: '$176.20', diff: '+1.95%' },
    { cat: '미국주식', name: '아마존 (AMZN)', base: '$182.50', diff: '+2.10%' },
    { cat: '미국주식', name: '메타 (META)', base: '$524.30', diff: '+3.15%' },
    { cat: '미국주식', name: '버크셔해서웨이 (BRK.B)', base: '$452.00', diff: '+0.65%' },
    { cat: '미국주식', name: '일라이릴리 (LLY)', base: '$945.00', diff: '+2.40%' },
    { cat: '미국주식', name: '브로드컴 (AVGO)', base: '$168.20', diff: '+4.80%' },
    { cat: '미국주식', name: '테슬라 (TSLA)', base: '$224.50', diff: '+3.80%' },

    // 5. 가상화폐 4종 (비트코인, 이더리움, 리플, 솔라나)
    { cat: '코인', name: '비트코인 (BTC)', base: '$64,250', diff: '+3.45%' },
    { cat: '코인', name: '이더리움 (ETH)', base: '$2,780', diff: '+2.90%' },
    { cat: '코인', name: '리플 (XRP)', base: '$0.585', diff: '+4.12%' },
    { cat: '코인', name: '솔라나 (SOL)', base: '$158.40', diff: '+6.20%' }
  ];

  const track = document.getElementById('tickerTrack');
  if (!track) return;

  const html = tickerItems.concat(tickerItems).map(item => {
    const isUp = item.diff.startsWith('+');
    return `
      <div class="ticker-item">
        <span class="ticker-cat" style="font-size:0.68rem; padding:1px 5px; border-radius:4px; background:rgba(255,255,255,0.08); color:var(--text-muted);">${item.cat}</span>
        <span class="ticker-name">${item.name}</span>
        <span class="ticker-val">${item.base}</span>
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
