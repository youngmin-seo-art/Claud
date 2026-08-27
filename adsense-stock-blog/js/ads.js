/**
 * ==========================================================================
 * ADSENSE PROFIT ENGINE (ADS.JS)
 * Google AdSense Centralized Configuration & CTR Placement Engine
 * ==========================================================================
 */

const ADSENSE_CONFIG = {
  // [공식 발급] 구글 애드센스 게시자 ID
  publisherId: 'ca-pub-7807868644631223', 
  
  // testMode: false로 설정하여 실제 구글 애드센스 심사 및 광고 로더 활성화
  testMode: false, 

  // 자동 광고(Auto Ads) 활성화 여부
  autoAds: true
};

class AdSenseEngine {
  constructor(config) {
    this.config = config;
    this.init();
  }

  init() {
    if (!this.config.testMode && this.config.publisherId !== 'ca-pub-XXXXXXXXXXXXXXXX') {
      this.loadGoogleScript();
    }
    this.renderAdSlots();
    this.setupAnchorAd();
  }

  loadGoogleScript() {
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
      const slotType = slot.getAttribute('data-ad-type') || 'display';
      const slotName = slot.getAttribute('data-ad-name') || '광고 슬롯';
      const slotSize = slot.getAttribute('data-ad-size') || 'Responsive';

      if (this.config.testMode) {
        slot.innerHTML = `
          <div class="ad-placeholder">
            <div class="ad-placeholder-icon">⚡</div>
            <div class="ad-placeholder-title">${slotName}</div>
            <div class="ad-placeholder-desc">구글 애드센스 골든 슬롯 (${slotType})</div>
            <span class="ad-placeholder-badge">${slotSize} • CTR 최적화</span>
          </div>
        `;
      } else {
        const slotId = slot.getAttribute('data-ad-slot');
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
          console.warn('AdSense render notice:', e);
        }
      }
    });
  }

  setupAnchorAd() {
    const anchor = document.getElementById('mobileAnchorAd');
    if (!anchor) return;

    const isClosed = sessionStorage.getItem('anchor_ad_closed');
    if (isClosed) {
      anchor.style.display = 'none';
      return;
    }

    const closeBtn = anchor.querySelector('.anchor-close-btn');
    if (closeBtn) {
      closeBtn.addEventListener('click', () => {
        anchor.style.display = 'none';
        sessionStorage.setItem('anchor_ad_closed', 'true');
      });
    }
  }
}

// Global AdSense Engine Instance
document.addEventListener('DOMContentLoaded', () => {
  window.adEngine = new AdSenseEngine(ADSENSE_CONFIG);
});
