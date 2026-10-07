/**
 * ==========================================================================
 * GOOGLE ADSENSE COMPLIANCE & AUTO-ADS ENGINE (ADS.JS)
 * Complies 100% with Google AdSense Program Policies
 * ==========================================================================
 */

const ADSENSE_CONFIG = {
  // 공식 발급 구글 애드센스 게시자 ID
  publisherId: 'ca-pub-7807868644631223', 
  
  // 자동 광고(Auto Ads) 활성화
  autoAds: true,

  // 심사 단계에서는 미승인 더미 슬롯 요청 방지
  testMode: false
};

class AdSenseEngine {
  constructor(config) {
    this.config = config;
    this.init();
  }

  init() {
    this.ensureGoogleScript();
    this.cleanEmptyAdSlots();
    this.renderAdSlots();
  }

  ensureGoogleScript() {
    if (document.querySelector('script[src*="adsbygoogle.js"]')) return;
    const script = document.createElement('script');
    script.async = true;
    script.src = `https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${this.config.publisherId}`;
    script.crossOrigin = 'anonymous';
    document.head.appendChild(script);
  }

  cleanEmptyAdSlots() {
    // 승인 전 빈 광고 영역이 페이지 가독성을 해치거나 심사 감점 요인이 되지 않도록 완전 은닉
    const wrappers = document.querySelectorAll('.ad-slot-wrapper, .ad-container, .mobile-anchor-ad, .ads-status-bar');
    wrappers.forEach(wrap => {
      const ins = wrap.querySelector('ins.adsbygoogle');
      if (!ins || ins.getAttribute('data-ad-status') === 'unfilled') {
        wrap.style.setProperty('display', 'none', 'important');
      }
    });
  }

  renderAdSlots() {
    const slots = document.querySelectorAll('.ad-container[data-ad-slot]');
    slots.forEach(slot => {
      const slotId = slot.getAttribute('data-ad-slot');
      
      // 실제 유효한 10자리 이상의 슬롯 ID가 부여된 경우에만 광고 태그 생성
      if (slotId && /^[0-9]{10,}$/.test(slotId)) {
        slot.innerHTML = `
          <ins class="adsbygoogle"
               style="display:block"
               data-ad-client="${this.config.publisherId}"
               data-ad-slot="${slotId}"
               data-ad-format="auto"
               data-full-width-responsive="true"></ins>
        `;
        try {
          (window.adsbygoogle = window.adsbygoogle || []).push({});
        } catch (e) {
          console.warn('AdSense notice:', e);
        }
      }
    });
  }
}

// Global AdSense Engine Initialization
document.addEventListener('DOMContentLoaded', () => {
  window.adEngine = new AdSenseEngine(ADSENSE_CONFIG);
});
