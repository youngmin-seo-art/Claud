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

  // 심사 단계에서는 존재하지 않는 더미 슬롯 요청을 방지
  testMode: false
};

class AdSenseEngine {
  constructor(config) {
    this.config = config;
    this.init();
  }

  init() {
    this.ensureGoogleScript();
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

  renderAdSlots() {
    const slots = document.querySelectorAll('.ad-container[data-ad-slot]');
    slots.forEach(slot => {
      const slotId = slot.getAttribute('data-ad-slot');
      
      // Only request manual ad units if a valid 10-digit Google AdSense slot ID is present
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
