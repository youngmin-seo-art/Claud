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
// 가격은 data/market-summary.json(배포 시 수집한 실제 시세)과 Upbit 공개 API에서만 채웁니다.
// 데이터가 없는 종목은 표시하지 않습니다(임의 숫자 표시 금지).
let MARKET_INSTRUMENTS = [
  // 1. 주요 지수 및 환율 (data/market-summary.json 종가 기준)
  { id: 'kospi', cat: '지수', name: 'KOSPI', precision: 2, prefix: '', suffix: '' },
  { id: 'kosdaq', cat: '지수', name: 'KOSDAQ', precision: 2, prefix: '', suffix: '' },
  { id: 'dji', cat: '지수', name: '다우존스', precision: 2, prefix: '', suffix: '' },
  { id: 'sp500', cat: '지수', name: 'S&P 500', precision: 2, prefix: '', suffix: '' },
  { id: 'nasdaq', cat: '지수', name: 'NASDAQ 100', precision: 2, prefix: '', suffix: '' },
  { id: 'sox', cat: '지수', name: '필라델피아반도체', precision: 2, prefix: '', suffix: '' },
  { id: 'usdkrw', cat: '환율', name: 'USD/KRW', isFx: true, precision: 2, prefix: '', suffix: '원' },

  // 2. 국내 KOSPI 시총 상위
  { id: 'samsung', cat: '코스피', name: '삼성전자', precision: 0, prefix: '', suffix: '원' },
  { id: 'skhynix', cat: '코스피', name: 'SK하이닉스', precision: 0, prefix: '', suffix: '원' },
  { id: 'lgenergy', cat: '코스피', name: 'LG에너지솔루션', precision: 0, prefix: '', suffix: '원' },
  { id: 'samsungbio', cat: '코스피', name: '삼성바이오로직스', precision: 0, prefix: '', suffix: '원' },
  { id: 'hyundai', cat: '코스피', name: '현대차', precision: 0, prefix: '', suffix: '원' },

  // 3. 국내 KOSDAQ 시총 상위
  { id: 'alteogen', cat: '코스닥', name: '알테오젠', precision: 0, prefix: '', suffix: '원' },
  { id: 'ecoprobm', cat: '코스닥', name: '에코프로비엠', precision: 0, prefix: '', suffix: '원' },
  { id: 'ecopro', cat: '코스닥', name: '에코프로', precision: 0, prefix: '', suffix: '원' },
  { id: 'hlb', cat: '코스닥', name: 'HLB', precision: 0, prefix: '', suffix: '원' },
  { id: 'ligachem', cat: '코스닥', name: '리가켐바이오', precision: 0, prefix: '', suffix: '원' },
  { id: 'enchem', cat: '코스닥', name: '엔켐', precision: 0, prefix: '', suffix: '원' },
  { id: 'samchendang', cat: '코스닥', name: '삼천당제약', precision: 0, prefix: '', suffix: '원' },
  { id: 'classys', cat: '코스닥', name: '클래시스', precision: 0, prefix: '', suffix: '원' },
  { id: 'hugel', cat: '코스닥', name: '휴젤', precision: 0, prefix: '', suffix: '원' },
  { id: 'leeno', cat: '코스닥', name: '리노공업', precision: 0, prefix: '', suffix: '원' },

  // 4. 미국 빅테크
  { id: 'nvda', cat: '미국주식', name: '엔비디아 (NVDA)', precision: 2, prefix: '$', suffix: '' },
  { id: 'aapl', cat: '미국주식', name: '애플 (AAPL)', precision: 2, prefix: '$', suffix: '' },
  { id: 'msft', cat: '미국주식', name: '마이크로소프트 (MSFT)', precision: 2, prefix: '$', suffix: '' },
  { id: 'googl', cat: '미국주식', name: '알파벳 (GOOGL)', precision: 2, prefix: '$', suffix: '' },
  { id: 'amzn', cat: '미국주식', name: '아마존 (AMZN)', precision: 2, prefix: '$', suffix: '' },
  { id: 'meta', cat: '미국주식', name: '메타 (META)', precision: 2, prefix: '$', suffix: '' },
  { id: 'tsla', cat: '미국주식', name: '테슬라 (TSLA)', precision: 2, prefix: '$', suffix: '' },
  { id: 'avgo', cat: '미국주식', name: '브로드컴 (AVGO)', precision: 2, prefix: '$', suffix: '' },
  { id: 'brk', cat: '미국주식', name: '버크셔해서웨이 (BRK.B)', precision: 2, prefix: '$', suffix: '' },
  { id: 'lly', cat: '미국주식', name: '일라이릴리 (LLY)', precision: 2, prefix: '$', suffix: '' },

  // 5. 가상화폐 (Upbit 실시간 연동)
  { id: 'btc', cat: '코인', name: '비트코인 (BTC)', marketCode: 'KRW-BTC', isCrypto: true, precision: 0, prefix: '₩', suffix: '' },
  { id: 'eth', cat: '코인', name: '이더리움 (ETH)', marketCode: 'KRW-ETH', isCrypto: true, precision: 0, prefix: '₩', suffix: '' },
  { id: 'xrp', cat: '코인', name: '리플 (XRP)', marketCode: 'KRW-XRP', isCrypto: true, precision: 0, prefix: '₩', suffix: '' },
  { id: 'sol', cat: '코인', name: '솔라나 (SOL)', marketCode: 'KRW-SOL', isCrypto: true, precision: 0, prefix: '₩', suffix: '' }
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
  if (!track) return;

  // 1. 배포 시 수집한 실제 시세(종가 기준) 불러오기
  const updatedAt = await loadMarketSummaryJSON();

  // 2. 실제 데이터가 있는 종목만 표시
  MARKET_INSTRUMENTS = MARKET_INSTRUMENTS.filter(inst => inst.hasData);
  const label = document.querySelector('.market-ticker-wrap .ticker-label span');
  if (!MARKET_INSTRUMENTS.length) {
    const wrap = document.querySelector('.market-ticker-wrap');
    if (wrap) wrap.style.display = 'none';
    return;
  }
  if (label && updatedAt) {
    const m = String(updatedAt).match(/^(\d{4})-(\d{2})-(\d{2})/);
    label.textContent = m ? `${m[2]}/${m[3]} 기준` : '마켓 지표';
    label.title = `주가·지수는 ${updatedAt} 수집 시세, 코인은 Upbit 실시간 시세`;
  }
  renderInitialTicker(track);

  // 3. 가상화폐만 Upbit 공개 API로 실시간 갱신
  fetchUpbitRealtime();
  setInterval(fetchUpbitRealtime, 15000);
}

async function loadMarketSummaryJSON() {
  const possiblePaths = [
    'data/market-summary.json',
    '../data/market-summary.json',
    '/data/market-summary.json'
  ];
  for (const p of possiblePaths) {
    try {
      const res = await fetch(p, { cache: 'no-cache' });
      if (!res.ok) continue;
      const data = await res.json();
      if (data && Array.isArray(data.instruments)) {
        data.instruments.forEach(newItem => {
          const existing = MARKET_INSTRUMENTS.find(x => x.id === newItem.id);
          if (existing && typeof newItem.price === 'number') {
            existing.price = newItem.price;
            existing.baseClose = newItem.baseClose;
            existing.diffRate = newItem.diffRate;
            existing.hasData = true;
          }
        });
        return data.updatedAt || '';
      }
    } catch (e) {
      // try next path
    }
  }
  return '';
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
  } else if (hashParam && ['market', 'undervalued', 'valuation', 'breakout'].includes(hashParam)) {
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
