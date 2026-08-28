/**
 * Value Stock Labs - Secret Admin Analytics & Daily Visitor Counter
 * (일일 방문자 수 및 통계 - 관리자 전용 비밀 대시보드)
 * 
 * 일반 방문자에게는 일체 노출되지 않으며, 블로그 소유자(관리자)만 비밀 단축키나 PIN 번호로 확인할 수 있습니다.
 * - 비밀 활성화 방법 1: 화면 좌상단/하단 로고를 5번 연속 클릭
 * - 비밀 활성화 방법 2: 키보드 단축키 'Ctrl + Shift + A'
 * - 비밀 활성화 방법 3: 주소창 뒤에 '?admin=1' 붙여서 접속
 * - 기본 관리자 PIN: 7777 (대시보드에서 변경 가능)
 */

(function() {
  'use strict';

  const STORAGE_KEY_ADMIN_PIN = 'vsl_admin_pin';
  const STORAGE_KEY_AUTH = 'vsl_admin_authenticated';
  const STORAGE_KEY_DATA = 'vsl_analytics_store';
  const NAMESPACE = 'valuestocklabs_prod_2026';
  const DEFAULT_PIN = '7777';

  // Format today string: YYYY-MM-DD
  function getTodayStr() {
    const d = new Date();
    const year = d.getFullYear();
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const day = String(d.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`;
  }

  // Get or initialize local analytics data
  function getAnalyticsData() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY_DATA);
      if (raw) return JSON.parse(raw);
    } catch(e) {}
    
    return {
      totalUV: 1,
      totalPV: 1,
      daily: {}, // { 'YYYY-MM-DD': { uv: 1, pv: 1 } }
      referrers: {}, // { 'Google': 10, 'Naver': 5, 'Direct': 20 }
      popularPages: {}, // { '/tools/fair-value-calculator.html': 15 }
      lastVisitTime: new Date().toISOString()
    };
  }

  function saveAnalyticsData(data) {
    try {
      localStorage.setItem(STORAGE_KEY_DATA, JSON.stringify(data));
    } catch(e) {}
  }

  // Determine Referrer category
  function getReferrerCategory() {
    const ref = document.referrer.toLowerCase();
    if (!ref) return '직접 유입 (Direct / 북마크)';
    if (ref.includes('naver.com')) return '네이버 (Naver)';
    if (ref.includes('google.com') || ref.includes('google.co.kr')) return '구글 (Google)';
    if (ref.includes('daum.net') || ref.includes('kakao.com')) return '다음 / 카카오';
    if (ref.includes('tistory.com')) return '티스토리';
    if (ref.includes('youtube.com')) return '유튜브 (YouTube)';
    return '기타 외부 사이트';
  }

  // Record Current Visit (Quiet Tracking)
  function recordVisit() {
    const today = getTodayStr();
    const currentPath = window.location.pathname || '/';
    const refCat = getReferrerCategory();
    
    // Check if device visited today (Daily UV deduplication)
    const sessionKey = `vsl_visited_${today}`;
    const isNewDailyVisitor = !localStorage.getItem(sessionKey);
    if (isNewDailyVisitor) {
      localStorage.setItem(sessionKey, '1');
    }

    const data = getAnalyticsData();
    
    if (!data.daily[today]) {
      data.daily[today] = { uv: 0, pv: 0 };
    }

    // Increment Pageview
    data.daily[today].pv += 1;
    data.totalPV = (data.totalPV || 0) + 1;

    // Increment Daily Unique Visitor
    if (isNewDailyVisitor) {
      data.daily[today].uv += 1;
      data.totalUV = (data.totalUV || 0) + 1;
    }

    // Track Referrer
    data.referrers[refCat] = (data.referrers[refCat] || 0) + 1;

    // Track Page
    data.popularPages[currentPath] = (data.popularPages[currentPath] || 0) + 1;
    data.lastVisitTime = new Date().toISOString();

    saveAnalyticsData(data);

    // Sync with Free Cloud Counter API (Asynchronous, silent)
    syncCloudCounter(today, isNewDailyVisitor);
  }

  async function syncCloudCounter(today, isNewUV) {
    try {
      // 1. Increment Today PV
      fetch(`https://api.counterapi.dev/v1/${NAMESPACE}/pv_${today.replace(/-/g, '')}/up`, { mode: 'no-cors' }).catch(()=>{});
      
      // 2. Increment Today UV if new
      if (isNewUV) {
        fetch(`https://api.counterapi.dev/v1/${NAMESPACE}/uv_${today.replace(/-/g, '')}/up`, { mode: 'no-cors' }).catch(()=>{});
        fetch(`https://api.counterapi.dev/v1/${NAMESPACE}/total_uv/up`, { mode: 'no-cors' }).catch(()=>{});
      }
    } catch(e) {}
  }

  async function fetchCloudStats(today) {
    try {
      const todayKey = today.replace(/-/g, '');
      const [resTodayUV, resTodayPV, resTotalUV] = await Promise.allSettled([
        fetch(`https://api.counterapi.dev/v1/${NAMESPACE}/uv_${todayKey}`).then(r => r.json()),
        fetch(`https://api.counterapi.dev/v1/${NAMESPACE}/pv_${todayKey}`).then(r => r.json()),
        fetch(`https://api.counterapi.dev/v1/${NAMESPACE}/total_uv`).then(r => r.json())
      ]);

      const cloudTodayUV = (resTodayUV.status === 'fulfilled' && resTodayUV.value?.count) ? resTodayUV.value.count : null;
      const cloudTodayPV = (resTodayPV.status === 'fulfilled' && resTodayPV.value?.count) ? resTodayPV.value.count : null;
      const cloudTotalUV = (resTotalUV.status === 'fulfilled' && resTotalUV.value?.count) ? resTotalUV.value.count : null;

      return { cloudTodayUV, cloudTodayPV, cloudTotalUV };
    } catch(e) {
      return { cloudTodayUV: null, cloudTodayPV: null, cloudTotalUV: null };
    }
  }

  // ==========================================
  // ADMIN DASHBOARD & AUTHENTICATION UI
  // ==========================================

  function getStoredPin() {
    return localStorage.getItem(STORAGE_KEY_ADMIN_PIN) || DEFAULT_PIN;
  }

  function setStoredPin(pin) {
    localStorage.setItem(STORAGE_KEY_ADMIN_PIN, pin);
  }

  function isAdminAuthenticated() {
    return sessionStorage.getItem(STORAGE_KEY_AUTH) === 'true';
  }

  function setAdminAuthenticated(val) {
    if (val) {
      sessionStorage.setItem(STORAGE_KEY_AUTH, 'true');
    } else {
      sessionStorage.removeItem(STORAGE_KEY_AUTH);
    }
  }

  // Prompt PIN Modal
  function showPinPrompt() {
    const existing = document.getElementById('vslAdminPinModal');
    if (existing) existing.remove();

    const modal = document.createElement('div');
    modal.id = 'vslAdminPinModal';
    modal.style.cssText = `
      position: fixed; inset: 0; background: rgba(0, 0, 0, 0.85);
      backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
      display: flex; align-items: center; justify-content: center;
      z-index: 999999; font-family: -apple-system, BlinkMacSystemFont, 'Pretendard', sans-serif;
    `;

    modal.innerHTML = `
      <div style="
        background: #0f172a; border: 1px solid #06b6d4; border-radius: 16px;
        padding: 32px 28px; width: 90%; max-width: 380px; box-shadow: 0 20px 50px rgba(0,0,0,0.8);
        text-align: center; color: #f8fafc;
      ">
        <div style="font-size: 2.2rem; margin-bottom: 8px;">👑</div>
        <h3 style="font-size: 1.25rem; font-weight: 800; margin-bottom: 6px; color: #38bdf8;">관리자 전용 통계 모드</h3>
        <p style="font-size: 0.85rem; color: #94a3b8; margin-bottom: 20px; line-height: 1.5;">
          방문자 통계는 블로그 소유자만 볼 수 있습니다.<br>
          <span style="color:#06b6d4; font-size:0.78rem;">(초기 기본 비밀번호: 7777)</span>
        </p>
        <div style="margin-bottom: 20px;">
          <input type="password" id="vslPinInput" maxlength="10" placeholder="PIN 비밀번호 입력" style="
            width: 100%; padding: 14px; background: #1e293b; border: 2px solid #334155;
            border-radius: 10px; color: #fff; font-size: 1.2rem; text-align: center;
            letter-spacing: 4px; font-weight: 700; outline: none; transition: border-color 0.2s;
          ">
          <div id="vslPinError" style="color: #f87171; font-size: 0.8rem; margin-top: 8px; display: none;">
            ❌ 비밀번호가 올바르지 않습니다.
          </div>
        </div>
        <div style="display: flex; gap: 10px;">
          <button id="vslBtnCancelPin" style="
            flex: 1; padding: 12px; background: #334155; border: none; border-radius: 8px;
            color: #cbd5e1; font-weight: 600; cursor: pointer; font-size: 0.9rem;
          ">닫기</button>
          <button id="vslBtnConfirmPin" style="
            flex: 2; padding: 12px; background: linear-gradient(135deg, #06b6d4, #3b82f6);
            border: none; border-radius: 8px; color: #fff; font-weight: 700; cursor: pointer; font-size: 0.95rem;
          ">통계 확인하기</button>
        </div>
      </div>
    `;

    document.body.appendChild(modal);

    const pinInput = document.getElementById('vslPinInput');
    const pinError = document.getElementById('vslPinError');
    const btnConfirm = document.getElementById('vslBtnConfirmPin');
    const btnCancel = document.getElementById('vslBtnCancelPin');

    pinInput.focus();

    const tryAuth = () => {
      const entered = pinInput.value.trim();
      const actual = getStoredPin();
      if (entered === actual) {
        setAdminAuthenticated(true);
        modal.remove();
        showAdminDashboard();
        renderAdminBadge();
      } else {
        pinError.style.display = 'block';
        pinInput.style.borderColor = '#ef4444';
        pinInput.value = '';
        pinInput.focus();
      }
    };

    btnConfirm.addEventListener('click', tryAuth);
    pinInput.addEventListener('keydown', (e) => {
      if (e.key === 'Enter') tryAuth();
    });
    btnCancel.addEventListener('click', () => modal.remove());
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.remove();
    });
  }

  // Floating Discreet Admin Badge (Only for Authenticated Admin)
  function renderAdminBadge() {
    if (!isAdminAuthenticated()) return;
    const existing = document.getElementById('vslAdminFloatingBadge');
    if (existing) return;

    const badge = document.createElement('div');
    badge.id = 'vslAdminFloatingBadge';
    badge.style.cssText = `
      position: fixed; bottom: 20px; right: 20px; z-index: 99999;
      background: rgba(15, 23, 42, 0.92); border: 1px solid #06b6d4;
      padding: 8px 14px; border-radius: 30px; color: #38bdf8;
      font-size: 0.82rem; font-weight: 700; cursor: pointer;
      display: flex; align-items: center; gap: 8px;
      box-shadow: 0 8px 24px rgba(0,0,0,0.6); backdrop-filter: blur(8px);
      transition: all 0.2s ease;
    `;
    badge.innerHTML = `
      <span style="display:inline-block; width:8px; height:8px; background:#10b981; border-radius:50%; box-shadow:0 0 8px #10b981;"></span>
      <span>👑 방문자 통계 HUD</span>
    `;

    badge.addEventListener('mouseenter', () => {
      badge.style.transform = 'translateY(-2px) scale(1.05)';
      badge.style.boxShadow = '0 12px 28px rgba(6, 182, 212, 0.4)';
    });
    badge.addEventListener('mouseleave', () => {
      badge.style.transform = 'translateY(0) scale(1)';
      badge.style.boxShadow = '0 8px 24px rgba(0,0,0,0.6)';
    });

    badge.addEventListener('click', showAdminDashboard);
    document.body.appendChild(badge);
  }

  // Full Admin Analytics Dashboard Modal
  async function showAdminDashboard() {
    const existing = document.getElementById('vslAdminDashboardModal');
    if (existing) existing.remove();

    const today = getTodayStr();
    const data = getAnalyticsData();
    const todayLocal = data.daily[today] || { uv: 1, pv: 1 };

    // Fetch cloud stats
    const { cloudTodayUV, cloudTodayPV, cloudTotalUV } = await fetchCloudStats(today);
    const displayTodayUV = cloudTodayUV !== null ? Math.max(cloudTodayUV, todayLocal.uv) : todayLocal.uv;
    const displayTodayPV = cloudTodayPV !== null ? Math.max(cloudTodayPV, todayLocal.pv) : todayLocal.pv;
    const displayTotalUV = cloudTotalUV !== null ? Math.max(cloudTotalUV, data.totalUV || 1) : (data.totalUV || 1);

    // Prepare 7-day daily trend
    const recentDays = [];
    for (let i = 6; i >= 0; i--) {
      const d = new Date();
      d.setDate(d.getDate() - i);
      const dayStr = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
      const dayData = data.daily[dayStr] || { uv: 0, pv: 0 };
      const label = i === 0 ? '오늘' : `${d.getMonth()+1}/${d.getDate()}`;
      recentDays.push({ date: dayStr, label, uv: dayData.uv, pv: dayData.pv });
    }

    const maxUv = Math.max(...recentDays.map(d => d.uv), 1);

    // Format Referrers
    const refEntries = Object.entries(data.referrers || {}).sort((a, b) => b[1] - a[1]).slice(0, 5);
    const pageEntries = Object.entries(data.popularPages || {}).sort((a, b) => b[1] - a[1]).slice(0, 5);

    const modal = document.createElement('div');
    modal.id = 'vslAdminDashboardModal';
    modal.style.cssText = `
      position: fixed; inset: 0; background: rgba(0, 0, 0, 0.88);
      backdrop-filter: blur(16px); -webkit-backdrop-filter: blur(16px);
      display: flex; align-items: center; justify-content: center;
      z-index: 999999; font-family: -apple-system, BlinkMacSystemFont, 'Pretendard', sans-serif;
      padding: 16px; overflow-y: auto;
    `;

    modal.innerHTML = `
      <div style="
        background: #0b1329; border: 1px solid #1e293b; border-radius: 20px;
        width: 100%; max-width: 680px; box-shadow: 0 25px 60px rgba(0,0,0,0.9);
        color: #f8fafc; overflow: hidden; max-height: 90vh; display: flex; flex-direction: column;
      ">
        <!-- Header -->
        <div style="
          padding: 20px 24px; background: rgba(30, 41, 59, 0.7);
          border-bottom: 1px solid #1e293b; display: flex; align-items: center; justify-content: space-between;
        ">
          <div style="display: flex; align-items: center; gap: 10px;">
            <span style="font-size: 1.4rem;">📊</span>
            <div>
              <h2 style="font-size: 1.15rem; font-weight: 800; color: #38bdf8; margin: 0;">Value Stock Labs 관리자 통계</h2>
              <div style="font-size: 0.75rem; color: #94a3b8;">비공개 실시간 방문자 분석 (소유자 전용)</div>
            </div>
          </div>
          <button id="vslBtnCloseDash" style="
            background: #1e293b; border: 1px solid #334155; color: #cbd5e1;
            width: 32px; height: 32px; border-radius: 8px; cursor: pointer; font-size: 1.1rem;
            display: flex; align-items: center; justify-content: center;
          ">✕</button>
        </div>

        <!-- Scrollable Body -->
        <div style="padding: 24px; overflow-y: auto; display: flex; flex-direction: column; gap: 20px;">
          
          <!-- Summary Cards -->
          <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px;">
            <div style="background: rgba(6, 182, 212, 0.08); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 12px; padding: 16px 12px; text-align: center;">
              <div style="font-size: 0.78rem; color: #06b6d4; font-weight: 700; margin-bottom: 6px;">🟢 오늘 순방문자 (UV)</div>
              <div style="font-size: 1.8rem; font-weight: 800; color: #fff;">${displayTodayUV.toLocaleString()}<span style="font-size:0.9rem; font-weight:600; color:#94a3b8;">명</span></div>
              <div style="font-size: 0.7rem; color: #64748b; margin-top: 4px;">기기 중복 제거</div>
            </div>

            <div style="background: rgba(59, 130, 246, 0.08); border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 12px; padding: 16px 12px; text-align: center;">
              <div style="font-size: 0.78rem; color: #60a5fa; font-weight: 700; margin-bottom: 6px;">👁️ 오늘 총 조회수 (PV)</div>
              <div style="font-size: 1.8rem; font-weight: 800; color: #fff;">${displayTodayPV.toLocaleString()}<span style="font-size:0.9rem; font-weight:600; color:#94a3b8;">회</span></div>
              <div style="font-size: 0.7rem; color: #64748b; margin-top: 4px;">페이지뷰 합계</div>
            </div>

            <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 16px 12px; text-align: center;">
              <div style="font-size: 0.78rem; color: #34d399; font-weight: 700; margin-bottom: 6px;">🏆 누적 총 방문자</div>
              <div style="font-size: 1.8rem; font-weight: 800; color: #fff;">${displayTotalUV.toLocaleString()}<span style="font-size:0.9rem; font-weight:600; color:#94a3b8;">명</span></div>
              <div style="font-size: 0.7rem; color: #64748b; margin-top: 4px;">오픈 이후 누적</div>
            </div>
          </div>

          <!-- 7-Day Chart -->
          <div style="background: #131d36; border: 1px solid #1e293b; border-radius: 14px; padding: 18px;">
            <div style="font-size: 0.85rem; font-weight: 700; color: #e2e8f0; margin-bottom: 14px; display: flex; justify-content: space-between; align-items: center;">
              <span>📈 최근 7일 일별 방문자 추이 (UV)</span>
              <span style="font-size: 0.75rem; color: #64748b;">기준: ${today}</span>
            </div>
            <div style="display: flex; align-items: flex-end; justify-content: space-between; height: 130px; gap: 8px; padding-top: 10px;">
              ${recentDays.map(d => {
                const heightPct = Math.max(12, Math.round((d.uv / maxUv) * 100));
                const isToday = d.label === '오늘';
                const barColor = isToday ? 'linear-gradient(180deg, #38bdf8, #06b6d4)' : 'linear-gradient(180deg, #334155, #1e293b)';
                const textColor = isToday ? '#38bdf8' : '#94a3b8';
                return `
                  <div style="flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%; justify-content: flex-end; gap: 6px;">
                    <span style="font-size: 0.72rem; font-weight: 700; color: ${textColor};">${d.uv}명</span>
                    <div style="width: 100%; max-width: 38px; height: ${heightPct}%; background: ${barColor}; border-radius: 6px 6px 2px 2px; transition: height 0.3s ease;"></div>
                    <span style="font-size: 0.72rem; color: ${textColor}; font-weight: ${isToday ? '800' : '500'};">${d.label}</span>
                  </div>
                `;
              }).join('')}
            </div>
          </div>

          <!-- Referrer & Top Pages -->
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
            <!-- Traffic Sources -->
            <div style="background: #131d36; border: 1px solid #1e293b; border-radius: 14px; padding: 16px;">
              <div style="font-size: 0.82rem; font-weight: 700; color: #e2e8f0; margin-bottom: 12px;">🧭 유입 경로 (Traffic Source)</div>
              ${refEntries.length > 0 ? refEntries.map(([ref, count]) => `
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.04); font-size: 0.78rem;">
                  <span style="color: #cbd5e1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;">${ref}</span>
                  <span style="font-weight: 700; color: #38bdf8;">${count}회</span>
                </div>
              `).join('') : '<div style="font-size:0.75rem; color:#64748b; padding:10px 0;">아직 수집된 유입 경로가 없습니다.</div>'}
            </div>

            <!-- Popular Pages -->
            <div style="background: #131d36; border: 1px solid #1e293b; border-radius: 14px; padding: 16px;">
              <div style="font-size: 0.82rem; font-weight: 700; color: #e2e8f0; margin-bottom: 12px;">📑 인기 페이지 TOP 5</div>
              ${pageEntries.length > 0 ? pageEntries.map(([page, count]) => `
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 6px 0; border-bottom: 1px solid rgba(255,255,255,0.04); font-size: 0.78rem;">
                  <span style="color: #cbd5e1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; max-width: 170px;" title="${page}">${page}</span>
                  <span style="font-weight: 700; color: #34d399;">${count}회</span>
                </div>
              `).join('') : '<div style="font-size:0.75rem; color:#64748b; padding:10px 0;">조회된 페이지 기록이 없습니다.</div>'}
            </div>
          </div>

          <!-- Admin Quick Tools -->
          <div style="background: #0f172a; border: 1px dashed #334155; border-radius: 12px; padding: 14px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px;">
            <div>
              <div style="font-size: 0.8rem; font-weight: 700; color: #cbd5e1;">🔒 관리자 설정</div>
              <div style="font-size: 0.72rem; color: #64748b;">PIN 변경 / 로그아웃</div>
            </div>
            <div style="display: flex; gap: 8px;">
              <button id="vslBtnChangePin" style="
                padding: 6px 12px; background: #1e293b; border: 1px solid #334155;
                color: #e2e8f0; border-radius: 6px; font-size: 0.75rem; cursor: pointer;
              ">PIN 변경</button>
              <button id="vslBtnLogout" style="
                padding: 6px 12px; background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.3);
                color: #f87171; border-radius: 6px; font-size: 0.75rem; cursor: pointer;
              ">통계 닫기 및 잠금</button>
            </div>
          </div>

        </div>
      </div>
    `;

    document.body.appendChild(modal);

    document.getElementById('vslBtnCloseDash')?.addEventListener('click', () => modal.remove());
    modal.addEventListener('click', (e) => {
      if (e.target === modal) modal.remove();
    });

    document.getElementById('vslBtnChangePin')?.addEventListener('click', () => {
      const newPin = prompt('새로운 관리자 PIN 번호 (4~10자리)를 입력하세요:');
      if (newPin && newPin.trim().length >= 4) {
        setStoredPin(newPin.trim());
        alert('PIN 번호가 성공적으로 변경되었습니다!');
      } else if (newPin !== null) {
        alert('PIN 번호는 4자리 이상이어야 합니다.');
      }
    });

    document.getElementById('vslBtnLogout')?.addEventListener('click', () => {
      setAdminAuthenticated(false);
      modal.remove();
      document.getElementById('vslAdminFloatingBadge')?.remove();
      alert('관리자 모드가 안전하게 잠겼습니다.');
    });
  }

  // ==========================================
  // SECRET TRIGGER LISTENERS
  // ==========================================

  let logoClickCount = 0;
  let logoClickTimer = null;

  function bindSecretTriggers() {
    // 1. Keyboard Shortcut: Ctrl + Shift + A
    document.addEventListener('keydown', (e) => {
      if (e.ctrlKey && e.shiftKey && (e.key === 'A' || e.key === 'a')) {
        e.preventDefault();
        if (isAdminAuthenticated()) {
          showAdminDashboard();
        } else {
          showPinPrompt();
        }
      }
    });

    // 2. Secret Logo Click (5 times within 3 seconds)
    document.querySelectorAll('.logo, .footer-logo, .logo-icon, .site-header .logo-text').forEach(el => {
      el.addEventListener('click', (e) => {
        logoClickCount++;
        clearTimeout(logoClickTimer);
        logoClickTimer = setTimeout(() => {
          logoClickCount = 0;
        }, 3000);

        if (logoClickCount >= 5) {
          logoClickCount = 0;
          e.preventDefault();
          if (isAdminAuthenticated()) {
            showAdminDashboard();
          } else {
            showPinPrompt();
          }
        }
      });
    });

    // 3. Secret URL query: ?admin=1 or ?admin=true
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('admin') === '1' || urlParams.get('admin') === 'true' || urlParams.get('admin') === 'vsl') {
      setTimeout(() => {
        if (isAdminAuthenticated()) {
          showAdminDashboard();
        } else {
          showPinPrompt();
        }
      }, 400);
    }
  }

  // ==========================================
  // INITIALIZATION
  // ==========================================
  function init() {
    // 1. Record visitor quietly
    recordVisit();

    // 2. Bind secret listeners
    bindSecretTriggers();

    // 3. If already authenticated, show the discreet badge
    if (isAdminAuthenticated()) {
      renderAdminBadge();
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
