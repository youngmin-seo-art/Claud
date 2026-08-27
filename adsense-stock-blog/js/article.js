/**
 * ==========================================================================
 * ARTICLE ENHANCEMENT SCRIPT (ARTICLE.JS)
 * Reading Progress, Table of Contents (TOC) ScrollSpy, Share & Engagement
 * ==========================================================================
 */

document.addEventListener('DOMContentLoaded', () => {
  initReadingProgressBar();
  initTableOfContents();
  initShareActions();
});

/* Reading Progress Bar at Top */
function initReadingProgressBar() {
  const bar = document.getElementById('readingProgress');
  if (!bar) return;

  window.addEventListener('scroll', () => {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    const progress = (window.scrollY / totalHeight) * 100;
    bar.style.width = Math.min(Math.max(progress, 0), 100) + '%';
  });
}

/* Table of Contents (TOC) Builder & ScrollSpy */
function initTableOfContents() {
  const content = document.querySelector('.article-content');
  const tocList = document.getElementById('tocList');
  if (!content || !tocList) return;

  const headings = content.querySelectorAll('h2, h3');
  if (headings.length === 0) {
    const tocBox = document.querySelector('.toc-box');
    if (tocBox) tocBox.style.display = 'none';
    return;
  }

  headings.forEach((heading, index) => {
    if (!heading.id) {
      heading.id = `heading-${index}`;
    }

    const li = document.createElement('li');
    li.className = `toc-item level-${heading.tagName === 'H2' ? '2' : '3'}`;
    
    const a = document.createElement('a');
    a.className = 'toc-link';
    a.href = `#${heading.id}`;
    a.textContent = heading.textContent.replace(/^[\s\S]*?\s/, ''); // Clean prefixes
    if (!a.textContent.trim()) a.textContent = heading.textContent;

    li.appendChild(a);
    tocList.appendChild(li);
  });

  // Intersection Observer for ScrollSpy
  const observerOptions = {
    rootMargin: '-80px 0px -60% 0px',
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        document.querySelectorAll('.toc-link').forEach(link => {
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('active');
          } else {
            link.classList.remove('active');
          }
        });
      }
    });
  }, observerOptions);

  headings.forEach(heading => observer.observe(heading));
}

/* Social Share & Link Copy with Notification */
function initShareActions() {
  const copyBtn = document.getElementById('shareCopyBtn');
  if (copyBtn) {
    copyBtn.addEventListener('click', () => {
      navigator.clipboard.writeText(window.location.href).then(() => {
        showToast('포스팅 링크가 클립보드에 복사되었습니다! ✨');
      }).catch(() => {
        showToast('링크 복사 실패');
      });
    });
  }

  const shareNativeBtn = document.getElementById('shareNativeBtn');
  if (shareNativeBtn) {
    shareNativeBtn.addEventListener('click', () => {
      if (navigator.share) {
        navigator.share({
          title: document.title,
          url: window.location.href
        }).catch(console.error);
      } else {
        copyBtn?.click();
      }
    });
  }
}

function showToast(message) {
  let toast = document.getElementById('blogToast');
  if (!toast) {
    toast = document.createElement('div');
    toast.id = 'blogToast';
    toast.style.cssText = `
      position: fixed;
      bottom: 40px;
      left: 50%;
      transform: translateX(-50%);
      background: var(--gradient-primary);
      color: #fff;
      padding: 12px 24px;
      border-radius: 99px;
      font-size: 0.9rem;
      font-weight: 700;
      box-shadow: 0 10px 30px rgba(0,0,0,0.5);
      z-index: 10000;
      opacity: 0;
      transition: opacity 0.3s, transform 0.3s;
      pointer-events: none;
    `;
    document.body.appendChild(toast);
  }
  toast.textContent = message;
  toast.style.opacity = '1';
  toast.style.transform = 'translateX(-50%) translateY(-10px)';
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(-50%) translateY(0)';
  }, 2500);
}
