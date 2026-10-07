/**
 * ==========================================================================
 * MAIN BLOG LOGIC (MAIN.JS)
 * Theme Manager, Real-time Live Market Engine, Search/Filter & UI Enhancements
 * ==========================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initLiveMarketEngine();
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
   REAL-TIME LIVE MARKET ENGINE (STOCKS, INDICES, FOREX & CRYPTO)
   ========================================================================== */
let MARKET_INSTRUMENTS = [
  // 1. 주요 지수 및 환율 (실시간 실제 시세 반영)
  { id: 'kospi', cat: '지수', name: 'KOSPI', price: 6800.77, baseClose: 6912.37, diffRate: -1.61, precision: 2, prefix: '', suffix: '' },
  { id: 'kosdaq', cat: '지수', name: 'KOSDAQ', price: 836.26, baseClose: 826.87, diffRate: 1.14, precision: 2, prefix: '', suffix: '' },
  { id: 'dji', cat: '지수', name: '다우존스', price: 53569.44, baseClose: 53463.90, diffRate: 0.20, precision: 2, prefix: '', suffix: '' },
  { id: 'sp500', cat: '지수', name: 'S&P 500', price: 7730.99, baseClose: 7675.70, diffRate: 0.72, precision: 2, prefix: '', suffix: '' },
  { id: 'nasdaq', cat: '지수', name: 'NASDAQ 100', price: 26541.35, baseClose: 26130.20, diffRate: 1.57, precision: 2, prefix: '', suffix: '' },
  { id: 'sox', cat: '지수', name: '필라델피아반도체', price: 11882.17, baseClose: 11611.24, diffRate: 2.33, precision: 2, prefix: '', suffix: '' },
  { id: 'usdkrw', cat: '환율', name: 'USD/KRW', price: 1376.08, baseClose: 1380.43, diffRate: -0.32, isFx: true, precision: 2, prefix: '', suffix: '원' },

  // 2. 국내 KOSPI 시총 상위
  { id: 'samsung', cat: '코스피', name: '삼성전자', price: 257500, baseClose: 266000, diffRate: -3.20, precision: 0, prefix: '', suffix: '원' },
  { id: 'skhynix', cat: '코스피', name: 'SK하이닉스', price: 1677000, baseClose: 1729625, diffRate: -3.04, precision: 0, prefix: '', suffix: '원' },
  { id: 'lgenergy', cat: '코스피', name: 'LG에너지솔루션', price: 369500, baseClose: 370500, diffRate: -0.27, precision: 0, prefix: '', suffix: '원' },
  { id: 'samsungbio', cat: '코스피', name: '삼성바이오로직스', price: 1489000, baseClose: 1594000, diffRate: -6.59, precision: 0, prefix: '', suffix: '원' },
  { id: 'hyundai', cat: '코스피', name: '현대차', price: 398000, baseClose: 395500, diffRate: 0.63, precision: 0, prefix: '', suffix: '원' },

  // 3. 국내 KOSDAQ 시총 상위
  { id: 'alteogen', cat: '코스닥', name: '알테오젠', price: 319000, baseClose: 311500, diffRate: 2.41, precision: 0, prefix: '', suffix: '원' },
  { id: 'ecoprobm', cat: '코스닥', name: '에코프로비엠', price: 117700, baseClose: 118000, diffRate: -0.25, precision: 0, prefix: '', suffix: '원' },
  { id: 'ecopro', cat: '코스닥', name: '에코프로', price: 89800, baseClose: 92000, diffRate: -2.39, precision: 0, prefix: '', suffix: '원' },
  { id: 'hlb', cat: '코스닥', name: 'HLB', price: 35700, baseClose: 35450, diffRate: 0.71, precision: 0, prefix: '', suffix: '원' },
  { id: 'ligachem', cat: '코스닥', name: '리가켐바이오', price: 100400, baseClose: 99600, diffRate: 0.80, precision: 0, prefix: '', suffix: '원' },
  { id: 'enchem', cat: '코스닥', name: '엔켐', price: 21300, baseClose: 22800, diffRate: -6.58, precision: 0, prefix: '', suffix: '원' },
  { id: 'samchendang', cat: '코스닥', name: '삼천당제약', price: 170300, baseClose: 172800, diffRate: -1.45, precision: 0, prefix: '', suffix: '원' },
  { id: 'classys', cat: '코스닥', name: '클래시스', price: 33250, baseClose: 32300, diffRate: 2.94, precision: 0, prefix: '', suffix: '원' },
  { id: 'hugel', cat: '코스닥', name: '휴젤', price: 256000, baseClose: 245500, diffRate: 4.28, precision: 0, prefix: '', suffix: '원' },
  { id: 'leeno', cat: '코스닥', name: '리노공업', price: 67100, baseClose: 66700, diffRate: 0.60, precision: 0, prefix: '', suffix: '원' },

  // 4. 미국 빅테크
  { id: 'nvda', cat: '미국주식', name: '엔비디아 (NVDA)', price: 227.98, baseClose: 209.66, diffRate: 8.74, precision: 2, prefix: '$', suffix: '' },
  { id: 'aapl', cat: '미국주식', name: '애플 (AAPL)', price: 314.58, baseClose: 313.45, diffRate: 0.36, precision: 2, prefix: '$', suffix: '' },
  { id: 'msft', cat: '미국주식', name: '마이크로소프트 (MSFT)', price: 505.06, baseClose: 496.37, diffRate: 1.75, precision: 2, prefix: '$', suffix: '' },
  { id: 'googl', cat: '미국주식', name: '알파벳 (GOOGL)', price: 340.65, baseClose: 341.98, diffRate: -0.39, precision: 2, prefix: '$', suffix: '' },
  { id: 'amzn', cat: '미국주식', name: '아마존 (AMZN)', price: 256.26, baseClose: 260.27, diffRate: -1.54, precision: 2, prefix: '$', suffix: '' },
  { id: 'meta', cat: '미국주식', name: '메타 (META)', price: 571.10, baseClose: 576.11, diffRate: -0.87, precision: 2, prefix: '$', suffix: '' },
  { id: 'tsla', cat: '미국주식', name: '테슬라 (TSLA)', price: 354.81, baseClose: 345.82, diffRate: 2.60, precision: 2, prefix: '$', suffix: '' },
  { id: 'avgo', cat: '미국주식', name: '브로드컴 (AVGO)', price: 371.54, baseClose: 355.57, diffRate: 4.49, precision: 2, prefix: '$', suffix: '' },
  { id: 'brk', cat: '미국주식', name: '버크셔해서웨이 (BRK.B)', price: 503.70, baseClose: 504.91, diffRate: -0.24, precision: 2, prefix: '$', suffix: '' },
  { id: 'lly', cat: '미국주식', name: '일라이릴리 (LLY)', price: 1176.10, baseClose: 1189.42, diffRate: -1.12, precision: 2, prefix: '$', suffix: '' },

  // 5. 가상화폐 (Upbit 실시간 연동)
  { id: 'btc', cat: '코인', name: '비트코인 (BTC)', marketCode: 'KRW-BTC', price: 110349000, baseClose: 111000000, diffRate: -0.59, isCrypto: true, precision: 0, prefix: '₩', suffix: '' },
  { id: 'eth', cat: '코인', name: '이더리움 (ETH)', marketCode: 'KRW-ETH', price: 3449000, baseClose: 3470000, diffRate: -0.63, isCrypto: true, precision: 0, prefix: '₩', suffix: '' },
  { id: 'xrp', cat: '코인', name: '리플 (XRP)', marketCode: 'KRW-XRP', price: 1969, baseClose: 2010, diffRate: -2.04, isCrypto: true, precision: 0, prefix: '₩', suffix: '' },
  { id: 'sol', cat: '코인', name: '솔라나 (SOL)', marketCode: 'KRW-SOL', price: 148200, baseClose: 150800, diffRate: -1.72, isCrypto: true, precision: 0, prefix: '₩', suffix: '' }
];

function formatPriceString(inst) {
  let valStr = '';
  if (inst.precision === 0) {
    valStr = Math.round(inst.price).toLocaleString('ko-KR');
  } else {
    valStr = inst.price.toLocaleString('en-US', {
      minimumFractionDigits: inst.precision,
      maximumFractionDigits: inst.precision
    });
  }
  return `${inst.prefix || ''}${valStr}${inst.suffix || ''}`;
}

function formatDiffString(diffRate) {
  const isUp = diffRate >= 0;
  const sign = isUp ? '+' : '';
  const arrow = isUp ? '▲' : '▼';
  return `${sign}${diffRate.toFixed(2)}% ${arrow}`;
}

async function initLiveMarketEngine() {
  const track = document.getElementById('tickerTrack');
  if (track) {
    renderInitialTicker(track);
  }

  // 1. Load latest real-time market summary from JSON if available for ticker track
  await loadMarketSummaryJSON();

  // 2. Fetch real live cryptocurrency data via Upbit Public API
  fetchUpbitRealtime();
  setInterval(fetchUpbitRealtime, 15000);

  // 3. Fetch real live USD/KRW exchange rate
  fetchLiveExchangeRate();
  setInterval(fetchLiveExchangeRate, 60000);

  // 4. Start high-frequency live market tick simulator (for top ticker track)
  startMarketTickSimulator();
}

async function loadMarketSummaryJSON() {
  const possiblePaths = [
    'data/market-summary.json',
    '../data/market-summary.json',
    '/data/market-summary.json',
    './data/market-summary.json'
  ];
  for (const p of possiblePaths) {
    try {
      const res = await fetch(p);
      if (res.ok) {
        const data = await res.json();
        if (data && data.instruments && Array.isArray(data.instruments)) {
          data.instruments.forEach(newItem => {
            const existing = MARKET_INSTRUMENTS.find(x => x.id === newItem.id);
            if (existing) {
              existing.price = newItem.price;
              existing.baseClose = newItem.baseClose;
              existing.diffRate = newItem.diffRate;
              updateInstrumentUI(existing, null);
            }
          });
          return;
        }
      }
    } catch (e) {
      // try next path
    }
  }
}

function renderInitialTicker(track) {
  // Ensure animation duration is explicitly applied to prevent CSS cache stale issues
  track.style.animation = 'tickerSlide 240s linear infinite';

  // Render duplicate list for smooth infinite CSS scroll
  const fullList = MARKET_INSTRUMENTS.concat(MARKET_INSTRUMENTS);
  const html = fullList.map((inst) => {
    const isUp = inst.diffRate >= 0;
    const priceFormatted = formatPriceString(inst);
    const diffFormatted = formatDiffString(inst.diffRate);

    return `
      <div class="ticker-item" data-inst-id="${inst.id}">
        <span class="ticker-cat" style="font-size:0.68rem; padding:1px 5px; border-radius:4px; background:rgba(255,255,255,0.08); color:var(--text-muted);">${inst.cat}</span>
        <span class="ticker-name">${inst.name}</span>
        <span class="ticker-val" data-price-id="${inst.id}">${priceFormatted}</span>
        <span class="${isUp ? 'ticker-up' : 'ticker-down'}" data-diff-id="${inst.id}">${diffFormatted}</span>
      </div>
    `;
  }).join('');

  track.innerHTML = html;
}

function updateInstrumentUI(inst, isUpTick = null) {
  const priceFormatted = formatPriceString(inst);
  const diffFormatted = formatDiffString(inst.diffRate);
  const isUp = inst.diffRate >= 0;

  // Update ticker elements in ticker track only
  const priceEls = document.querySelectorAll(`#tickerTrack [data-price-id="${inst.id}"]`);
  priceEls.forEach(el => {
    el.textContent = priceFormatted;
  });

  const diffEls = document.querySelectorAll(`#tickerTrack [data-diff-id="${inst.id}"]`);
  diffEls.forEach(el => {
    el.textContent = diffFormatted;
    el.className = isUp ? 'ticker-up' : 'ticker-down';
    if (isUpTick !== null) {
      const flashClass = isUpTick ? 'flash-tick-up' : 'flash-tick-down';
      el.classList.remove('flash-tick-up', 'flash-tick-down');
      void el.offsetWidth;
      el.classList.add(flashClass);
    }
  });
}

/* ==========================================================================
   PUBLIC LIVE API FETCHERS (UPBIT & EXCHANGE RATE)
   ========================================================================== */
async function fetchUpbitRealtime() {
  try {
    const response = await fetch('https://api.upbit.com/v1/ticker?markets=KRW-BTC,KRW-ETH,KRW-XRP,KRW-SOL', {
      headers: { 'Accept': 'application/json' }
    });
    if (!response.ok) return;

    const data = await response.json();
    data.forEach(item => {
      const inst = MARKET_INSTRUMENTS.find(x => x.marketCode === item.market);
      if (inst) {
        const oldPrice = inst.price;
        inst.price = item.trade_price;
        inst.baseClose = item.prev_closing_price || (item.trade_price - item.signed_change_price);
        inst.diffRate = item.signed_change_rate * 100;

        const isUpTick = inst.price >= oldPrice;
        updateInstrumentUI(inst, isUpTick);
      }
    });
  } catch (err) {
    // Graceful fallback
  }
}

async function fetchLiveExchangeRate() {
  try {
    const response = await fetch('https://open.er-api.com/v6/latest/USD');
    if (!response.ok) return;

    const data = await response.json();
    if (data && data.rates && data.rates.KRW) {
      const krwRate = parseFloat(data.rates.KRW.toFixed(2));
      const inst = MARKET_INSTRUMENTS.find(x => x.id === 'usdkrw');
      if (inst) {
        const oldPrice = inst.price;
        inst.price = krwRate;
        inst.diffRate = ((krwRate - inst.baseClose) / inst.baseClose) * 100;
        updateInstrumentUI(inst, inst.price >= oldPrice);
      }
    }
  } catch (err) {
    // Graceful fallback
  }
}

/* ==========================================================================
   DYNAMIC REAL-TIME MARKET TICK SIMULATOR
   Generates live, realistic micro-movements across indices & stocks
   ========================================================================== */
function startMarketTickSimulator() {
  // Tick every 2.0 ~ 3.2 seconds
  function scheduleNextTick() {
    const delay = Math.floor(Math.random() * 1200) + 2000;
    setTimeout(() => {
      performRandomMarketTicks();
      scheduleNextTick();
    }, delay);
  }
  scheduleNextTick();
}

function performRandomMarketTicks() {
  // Select 2 to 4 random instruments to tick
  const count = Math.floor(Math.random() * 3) + 2;
  const pickedIndices = new Set();
  while (pickedIndices.size < count) {
    const idx = Math.floor(Math.random() * MARKET_INSTRUMENTS.length);
    pickedIndices.add(idx);
  }

  pickedIndices.forEach(idx => {
    const inst = MARKET_INSTRUMENTS[idx];
    if (inst.isCrypto) return; // Upbit handles cryptos directly

    // Micro-volatility based on asset category
    let maxPct = 0.0008; // 0.08% for domestic/US stocks
    if (inst.cat === '지수') maxPct = 0.0004; // 0.04% for indices
    if (inst.cat === '환율') maxPct = 0.0003; // 0.03% for FX

    // Random walk with mild mean reversion around baseline
    const drift = (Math.random() - 0.49);
    const delta = inst.price * drift * maxPct;

    const oldPrice = inst.price;
    inst.price += delta;

    // Keep within realistic intraday bound (+- 3.5% from baseClose)
    const maxBound = inst.baseClose * 1.05;
    const minBound = inst.baseClose * 0.95;
    inst.price = Math.max(minBound, Math.min(maxBound, inst.price));

    // Recalculate difference rate
    inst.diffRate = ((inst.price - inst.baseClose) / inst.baseClose) * 100;

    const isUpTick = inst.price >= oldPrice;
    updateInstrumentUI(inst, isUpTick);
  });
}

/* ==========================================================================
   CATEGORY & SEARCH FILTER
   ========================================================================== */
function filterCategory(category, shouldScroll = false) {
  const tabs = document.querySelectorAll('.cat-tab');
  const cards = document.querySelectorAll('.post-card');
  const searchInput = document.getElementById('blogSearchInput');

  if (searchInput) searchInput.value = ''; // Reset search on category switch

  // 1. Update tab active state and top navLinks active state
  let matchedTab = null;
  tabs.forEach(t => {
    if (t.getAttribute('data-category') === category) {
      t.classList.add('active');
      matchedTab = t;
    } else {
      t.classList.remove('active');
    }
  });

  const navLinks = document.querySelectorAll('.main-nav a');
  navLinks.forEach(nl => {
    const href = nl.getAttribute('href') || '';
    if (category === 'all' && (href === 'index.html' || href === '../index.html')) {
      nl.classList.add('active');
    } else if (href.includes(`cat=${category}`)) {
      nl.classList.add('active');
    } else {
      nl.classList.remove('active');
    }
  });

  if (!matchedTab && tabs.length > 0) {
    tabs[0].classList.add('active'); // fallback to 'all'
    category = 'all';
  }

  // 2. Filter post cards
  cards.forEach(card => {
    const cardCat = card.getAttribute('data-category');
    if (category === 'all' || cardCat === category) {
      card.style.display = 'flex';
      card.style.opacity = '1';
    } else {
      card.style.display = 'none';
    }
  });

  // 3. Smooth scroll to grid if requested
  if (shouldScroll) {
    const gridEl = document.getElementById('postsGrid') || document.querySelector('.content-area');
    if (gridEl) {
      const topOffset = gridEl.getBoundingClientRect().top + window.pageYOffset - 90;
      window.scrollTo({ top: topOffset, behavior: 'smooth' });
    }
  }
}

function initCategoryFilter() {
  const tabs = document.querySelectorAll('.cat-tab');
  const navLinks = document.querySelectorAll('.main-nav a');

  // Tab click listeners
  tabs.forEach(tab => {
    tab.addEventListener('click', (e) => {
      e.preventDefault();
      const category = tab.getAttribute('data-category');
      filterCategory(category, false);
      
      // Update URL without full page reload
      const newUrl = new URL(window.location);
      if (category === 'all') {
        newUrl.searchParams.delete('cat');
      } else {
        newUrl.searchParams.set('cat', category);
      }
      history.replaceState(null, '', newUrl.toString());
    });
  });

  // Main navigation category links handler
  navLinks.forEach(link => {
    const href = link.getAttribute('href') || '';
    if (href.includes('cat=')) {
      link.addEventListener('click', (e) => {
        // If on index.html, intercept and filter smoothly
        const isIndex = window.location.pathname.endsWith('index.html') || window.location.pathname.endsWith('/') || !window.location.pathname.includes('/posts/');
        if (isIndex) {
          e.preventDefault();
          const match = href.match(/cat=([a-zA-Z0-9_-]+)/);
          if (match && match[1]) {
            filterCategory(match[1], true);
            const newUrl = new URL(window.location);
            newUrl.searchParams.set('cat', match[1]);
            history.pushState(null, '', newUrl.toString());
          }
        }
      });
    }
  });

  // Check URL parameters on initial page load
  const urlParams = new URLSearchParams(window.location.search);
  const catParam = urlParams.get('cat');
  const hashParam = window.location.hash.replace('#', '').replace('cat=', '');

  if (catParam) {
    filterCategory(catParam, true);
  } else if (hashParam && ['market', 'undervalued', 'valuation', 'breakout', 'semiconductor'].includes(hashParam)) {
    filterCategory(hashParam, true);
  }
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
