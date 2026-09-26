/**
 * ==========================================================================
 * REAL-TIME INVESTOR COMMUNITY & COMMENTS ENGINE (COMMENTS.JS)
 * LocalStorage Persistent Comment System with Sentiment, Likes & Replies
 * Value Stock Labs (VSL)
 * ==========================================================================
 */

(function () {
  'use strict';

  // Seed / Default Sample Discussions tailored to specific topics for rich engagement
  const DEFAULT_DISCUSSIONS = {
    'stock-valuation': [
      {
        id: 'c_val_1',
        author: '가치투자10년차',
        role: 'VIP 회원',
        sentiment: 'bull',
        date: '2026.09.26 10:15',
        likes: 18,
        liked: false,
        text: 'S-RIM 초과이익모델과 DCF 비교 설명이 매우 명쾌하네요! 특히 ROE가 주주요구수익률(Ke)보다 높게 유지될 때와 할인율 민감도 분석 테이블이 실전 투자에서 적정 밸류에이션을 산정할 때 큰 도움이 됩니다. 계산기 툴도 잘 쓰고 있습니다.',
        replies: [
          {
            id: 'c_val_1_r1',
            author: '퀀트밸류팀',
            role: '리서치팀',
            sentiment: 'neutral',
            date: '2026.09.26 10:40',
            likes: 9,
            liked: false,
            text: '감사합니다! S-RIM 산정 시 BBB- 5년 국채금리 스프레드를 기준으로 안전마진 20~30%를 적용하시면 더욱 보수적이고 안전한 매수가를 도출하실 수 있습니다.'
          }
        ]
      },
      {
        id: 'c_val_2',
        author: '스노우볼개미',
        role: '독자',
        sentiment: 'bull',
        date: '2026.09.26 11:22',
        likes: 12,
        liked: false,
        text: '저평가 우량주 4단계 스크리닝과 결합해서 포트폴리오를 구성해보니 확실히 하방 지지력이 단단해지네요. 적정가치 계산기와 평단가 계산기 링크도 바로 연결되어 있어서 유용합니다.',
        replies: []
      },
      {
        id: 'c_val_3',
        author: '차트와가치사이',
        role: '독자',
        sentiment: 'neutral',
        date: '2026.09.26 13:05',
        likes: 7,
        liked: false,
        text: 'PER 10배 이하이면서 순현금 비중이 30% 이상인 종목 중에서 거래량 골든크로스가 터지는 상승초입 타이밍에 분할 진입하는 전략을 테스트 중입니다. 좋은 인사이트 감사합니다!',
        replies: []
      }
    ],
    'market-briefing': [
      {
        id: 'c_mkt_1',
        author: '모닝루틴트레이더',
        role: 'VIP 회원',
        sentiment: 'bull',
        date: '2026.09.26 08:20',
        likes: 15,
        liked: false,
        text: '매일 아침 8시 출근길에 모닝 브리핑으로 환율이랑 미 증시 마감 지표 한눈에 체크하고 있습니다. 실시간 티커 지표랑 연동되어 있어서 시장 파악이 정말 빠르네요.',
        replies: []
      },
      {
        id: 'c_mkt_2',
        author: '환율과수급',
        role: '독자',
        sentiment: 'neutral',
        date: '2026.09.26 09:10',
        likes: 8,
        liked: false,
        text: '원/달러 환율이 1,350원대 안착하면서 외국인 선물 순매수가 유입되는 흐름이 긍정적입니다. 반도체 톱픽 위주 분할 매수 전략 참고하겠습니다.',
        replies: []
      }
    ],
    'default': [
      {
        id: 'c_def_1',
        author: '스마트인베스터',
        role: 'VIP 회원',
        sentiment: 'bull',
        date: '2026.09.26 09:30',
        likes: 14,
        liked: false,
        text: '데이터와 팩트에 기반한 리서치 리포트 잘 읽었습니다. 퀀트 밸류에이션 모델과 실전 매매 전략이 균형 있게 정리되어 있어 투자 판단에 큰 도움이 됩니다.',
        replies: []
      },
      {
        id: 'c_def_2',
        author: '가치성장투자자',
        role: '독자',
        sentiment: 'neutral',
        date: '2026.09.26 11:45',
        likes: 9,
        liked: false,
        text: '핵심 지표와 리스크 요인까지 짚어주셔서 객관적인 시각을 유지할 수 있네요. 다음 분석 리포트도 기대하겠습니다.',
        replies: []
      }
    ]
  };

  // Helper: Get Post Slug Key
  function getPostKey() {
    const path = window.location.pathname;
    const filename = path.substring(path.lastIndexOf('/') + 1).replace('.html', '');
    if (!filename || filename === 'index') return 'main';
    return filename;
  }

  // Helper: Select Topic Sample
  function getTopicDefaults(postKey) {
    if (postKey.includes('valuation') || postKey.includes('fair-value')) {
      return JSON.parse(JSON.stringify(DEFAULT_DISCUSSIONS['stock-valuation']));
    }
    if (postKey.includes('morning') || postKey.includes('briefing') || postKey.includes('market')) {
      return JSON.parse(JSON.stringify(DEFAULT_DISCUSSIONS['market-briefing']));
    }
    return JSON.parse(JSON.stringify(DEFAULT_DISCUSSIONS['default']));
  }

  // Storage Manager
  function loadComments(postKey) {
    const storageKey = `vsl_comments_${postKey}`;
    const stored = localStorage.getItem(storageKey);
    if (stored) {
      try {
        return JSON.parse(stored);
      } catch (e) {
        console.error('Failed to parse comments from storage', e);
      }
    }
    const initial = getTopicDefaults(postKey);
    localStorage.setItem(storageKey, JSON.stringify(initial));
    return initial;
  }

  function saveComments(postKey, comments) {
    const storageKey = `vsl_comments_${postKey}`;
    localStorage.setItem(storageKey, JSON.stringify(comments));
  }

  // Get user likes map
  function getUserLikes(postKey) {
    const storageKey = `vsl_likes_${postKey}`;
    const stored = localStorage.getItem(storageKey);
    return stored ? JSON.parse(stored) : {};
  }

  function saveUserLikes(postKey, likesMap) {
    const storageKey = `vsl_likes_${postKey}`;
    localStorage.setItem(storageKey, JSON.stringify(likesMap));
  }

  // Avatar color generator based on name
  function getAvatarColor(name) {
    const colors = [
      'linear-gradient(135deg, #06b6d4, #3b82f6)',
      'linear-gradient(135deg, #10b981, #059669)',
      'linear-gradient(135deg, #8b5cf6, #6366f1)',
      'linear-gradient(135deg, #f59e0b, #d97706)',
      'linear-gradient(135deg, #ec4899, #be185d)',
      'linear-gradient(135deg, #14b8a6, #0d9488)'
    ];
    let hash = 0;
    for (let i = 0; i < name.length; i++) {
      hash = name.charCodeAt(i) + ((hash << 5) - hash);
    }
    return colors[Math.abs(hash) % colors.length];
  }

  // Format Date String
  function getFormattedNow() {
    const d = new Date();
    const pad = (n) => String(n).padStart(2, '0');
    return `${d.getFullYear()}.${pad(d.getMonth() + 1)}.${pad(d.getDate())} ${pad(d.getHours())}:${pad(d.getMinutes())}`;
  }

  // Sentiment Helper
  function getSentimentBadge(sentiment) {
    if (sentiment === 'bull') {
      return '<span class="comment-sentiment-badge bull">🐂 매수 관점</span>';
    } else if (sentiment === 'bear') {
      return '<span class="comment-sentiment-badge bear">🐻 신중/관망</span>';
    } else if (sentiment === 'neutral') {
      return '<span class="comment-sentiment-badge neutral">⚖️ 분석/질문</span>';
    }
    return '';
  }

  // Main Render Function
  function renderComments(container, postKey) {
    const comments = loadComments(postKey);
    const userLikes = getUserLikes(postKey);

    // Calculate total comments including replies
    let totalCount = 0;
    comments.forEach((c) => {
      totalCount += 1 + (c.replies ? c.replies.length : 0);
    });

    const markup = `
      <section class="comments-section" id="commentsSection" aria-label="투자 토론 및 댓글">
        <div class="comments-header">
          <h3 class="comments-title">
            <span>💬 실시간 투자 토론 &amp; 독자 댓글</span>
            <span class="comments-count-badge" id="commentsCountBadge">${totalCount}개</span>
          </h3>
          <div class="comments-guide-text" style="font-size: 0.82rem; color: var(--text-muted);">
            💡 건전하고 품격 있는 투자 의견 교환을 환영합니다.
          </div>
        </div>

        <!-- Comment Write Form -->
        <div class="comment-form-card" id="commentMainForm">
          <div class="comment-form-header">
            <input type="text" id="commentAuthorInput" class="comment-input-name" placeholder="닉네임 (예: 가치투자자)" maxlength="20">
            <input type="password" id="commentPasswordInput" class="comment-input-pw" placeholder="비밀번호 4자리 (삭제용)" maxlength="10">
          </div>

          <!-- Sentiment Select -->
          <div class="comment-sentiment-group">
            <span class="sentiment-label">📊 투자 포지션:</span>
            <button type="button" class="sentiment-btn active" data-sentiment="bull">🐂 매수/낙관</button>
            <button type="button" class="sentiment-btn" data-sentiment="neutral">⚖️ 분석/중립</button>
            <button type="button" class="sentiment-btn" data-sentiment="bear">🐻 신중/관망</button>
          </div>

          <!-- Textarea -->
          <textarea id="commentContentInput" class="comment-textarea" placeholder="포스팅에 대한 질문이나 투자 인사이트, 적정주가 의견을 자유롭게 남겨주세요..."></textarea>

          <!-- Form Footer -->
          <div class="comment-form-footer">
            <div class="quick-emojis">
              <span style="font-size: 0.78rem; color: var(--text-muted); margin-right: 4px;">빠른 반응:</span>
              <button type="button" class="emoji-btn" title="로켓">🚀</button>
              <button type="button" class="emoji-btn" title="불꽃">🔥</button>
              <button type="button" class="emoji-btn" title="상승">📈</button>
              <button type="button" class="emoji-btn" title="다이아">💎</button>
              <button type="button" class="emoji-btn" title="추천">👍</button>
              <button type="button" class="emoji-btn" title="전구">💡</button>
            </div>

            <div style="display: flex; align-items: center; gap: 14px;">
              <span class="comment-char-count" id="commentCharCount">0 / 500자</span>
              <button type="button" class="comment-submit-btn" id="commentSubmitBtn">
                <span>댓글 등록</span>
                <span>✍️</span>
              </button>
            </div>
          </div>
        </div>

        <!-- Comments List -->
        <div class="comments-list" id="commentsListContainer">
          ${renderCommentsList(comments, userLikes, postKey)}
        </div>
      </section>
    `;

    container.innerHTML = markup;
    bindCommentEvents(container, postKey);
  }

  // Render List of Comment HTML
  function renderCommentsList(comments, userLikes, postKey) {
    if (!comments || comments.length === 0) {
      return `
        <div style="text-align: center; padding: 40px; background: var(--bg-secondary); border-radius: 12px; border: 1px solid var(--border-color); color: var(--text-muted);">
          <span style="font-size: 2rem; display: block; margin-bottom: 8px;">💭</span>
          첫 번째 투자 인사이트 댓글을 남겨보세요!
        </div>
      `;
    }

    return comments
      .map((c) => {
        const isLiked = !!userLikes[c.id];
        const initial = c.author.charAt(0) || 'U';
        const bgGrad = getAvatarColor(c.author);
        const roleBadge = c.role ? `<span class="comment-badge-role ${c.role.includes('리서치') ? 'staff' : ''}">${c.role}</span>` : '';
        const sentimentBadge = getSentimentBadge(c.sentiment);

        const repliesHtml = (c.replies || [])
          .map((r) => {
            const rLiked = !!userLikes[r.id];
            const rInitial = r.author.charAt(0) || 'U';
            const rGrad = getAvatarColor(r.author);
            const rRoleBadge = r.role ? `<span class="comment-badge-role ${r.role.includes('리서치') ? 'staff' : ''}">${r.role}</span>` : '';
            return `
              <div class="comment-item reply-item" id="${r.id}" style="background: rgba(255, 255, 255, 0.02); padding: 14px 16px;">
                <div class="comment-top-bar">
                  <div class="comment-user-info">
                    <div class="comment-avatar" style="background: ${rGrad}; width: 28px; height: 28px; font-size: 0.8rem;">${rInitial}</div>
                    <span class="comment-user-name" style="font-size: 0.88rem;">${escapeHtml(r.author)} ${rRoleBadge}</span>
                  </div>
                  <span class="comment-date" style="font-size: 0.75rem;">${r.date}</span>
                </div>
                <div class="comment-text" style="font-size: 0.9rem; margin-bottom: 8px;">${escapeHtml(r.text)}</div>
                <div class="comment-actions-bar" style="padding-top: 6px;">
                  <button type="button" class="comment-action-btn like-btn ${rLiked ? 'liked' : ''}" data-id="${r.id}" data-parent="${c.id}">
                    <span>👍</span> 추천 <span class="like-count">${r.likes || 0}</span>
                  </button>
                  ${r.isCustom ? `<button type="button" class="comment-action-btn delete-btn" data-id="${r.id}" data-parent="${c.id}" style="color:#ef4444;"><span>🗑️</span> 삭제</button>` : ''}
                </div>
              </div>
            `;
          })
          .join('');

        return `
          <div class="comment-item" id="${c.id}">
            <div class="comment-top-bar">
              <div class="comment-user-info">
                <div class="comment-avatar" style="background: ${bgGrad};">${initial}</div>
                <div>
                  <div class="comment-user-name">
                    ${escapeHtml(c.author)}
                    ${roleBadge}
                    ${sentimentBadge}
                  </div>
                </div>
              </div>
              <span class="comment-date">${c.date}</span>
            </div>

            <div class="comment-text">${escapeHtml(c.text)}</div>

            <div class="comment-actions-bar">
              <button type="button" class="comment-action-btn like-btn ${isLiked ? 'liked' : ''}" data-id="${c.id}">
                <span>👍</span> 추천 <span class="like-count">${c.likes || 0}</span>
              </button>
              <button type="button" class="comment-action-btn reply-btn" data-id="${c.id}">
                <span>💬</span> 답글 달기
              </button>
              ${c.isCustom ? `<button type="button" class="comment-action-btn delete-btn" data-id="${c.id}" style="color:#ef4444;"><span>🗑️</span> 삭제</button>` : ''}
            </div>

            <!-- Nested Replies Area -->
            ${
              c.replies && c.replies.length > 0
                ? `<div class="comment-replies">${repliesHtml}</div>`
                : `<div class="comment-replies" style="display:none;"></div>`
            }

            <!-- Inline Reply Box Container -->
            <div class="reply-form-slot" id="replySlot_${c.id}" style="display:none; margin-top: 14px;"></div>
          </div>
        `;
      })
      .join('');
  }

  // HTML Escape Helper
  function escapeHtml(str) {
    if (!str) return '';
    return str
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }

  // Bind UI Events
  function bindCommentEvents(container, postKey) {
    let selectedSentiment = 'bull';

    // Sentiment Selector Buttons
    const sentimentBtns = container.querySelectorAll('.sentiment-btn');
    sentimentBtns.forEach((btn) => {
      btn.addEventListener('click', () => {
        sentimentBtns.forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        selectedSentiment = btn.getAttribute('data-sentiment');
      });
    });

    // Character Counter & Auto Resize
    const textarea = container.querySelector('#commentContentInput');
    const charCount = container.querySelector('#commentCharCount');
    if (textarea && charCount) {
      textarea.addEventListener('input', () => {
        const len = textarea.value.length;
        charCount.textContent = `${len} / 500자`;
        if (len > 500) {
          charCount.style.color = '#ef4444';
        } else {
          charCount.style.color = 'var(--text-muted)';
        }
      });
    }

    // Quick Emoji Insert Buttons
    const emojiBtns = container.querySelectorAll('.quick-emojis .emoji-btn');
    emojiBtns.forEach((ebtn) => {
      ebtn.addEventListener('click', () => {
        if (!textarea) return;
        textarea.value += ebtn.textContent + ' ';
        textarea.focus();
        if (charCount) charCount.textContent = `${textarea.value.length} / 500자`;
      });
    });

    // Main Comment Submit
    const submitBtn = container.querySelector('#commentSubmitBtn');
    if (submitBtn) {
      submitBtn.addEventListener('click', () => {
        const author = container.querySelector('#commentAuthorInput').value.trim();
        const password = container.querySelector('#commentPasswordInput').value.trim();
        const content = textarea.value.trim();

        if (!author) {
          alert('작성자 닉네임을 입력해주세요.');
          container.querySelector('#commentAuthorInput').focus();
          return;
        }
        if (!content) {
          alert('댓글 내용을 입력해주세요.');
          textarea.focus();
          return;
        }

        const newComment = {
          id: 'c_user_' + Date.now(),
          author: author,
          password: password || '1234',
          role: '독자',
          sentiment: selectedSentiment,
          date: getFormattedNow(),
          likes: 1,
          liked: true,
          text: content,
          isCustom: true,
          replies: []
        };

        const comments = loadComments(postKey);
        comments.unshift(newComment);
        saveComments(postKey, comments);

        // Auto mark user like
        const userLikes = getUserLikes(postKey);
        userLikes[newComment.id] = true;
        saveUserLikes(postKey, userLikes);

        // Clear Form
        textarea.value = '';
        if (charCount) charCount.textContent = '0 / 500자';

        // Re-render
        renderComments(container, postKey);

        // Show toast
        if (window.showToast) {
          window.showToast('투자 의견 댓글이 등록되었습니다! 🚀');
        } else {
          alert('댓글이 등록되었습니다! ✨');
        }

        // Highlight new comment
        const newEl = document.getElementById(newComment.id);
        if (newEl) {
          newEl.classList.add('new-comment');
          newEl.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
      });
    }

    // Delegate Likes, Replies & Deletes
    const listContainer = container.querySelector('#commentsListContainer');
    if (listContainer) {
      listContainer.addEventListener('click', (e) => {
        const likeBtn = e.target.closest('.like-btn');
        const replyBtn = e.target.closest('.reply-btn');
        const deleteBtn = e.target.closest('.delete-btn');

        // 1. LIKE ACTION
        if (likeBtn) {
          const cid = likeBtn.getAttribute('data-id');
          const parentId = likeBtn.getAttribute('data-parent');
          toggleLike(postKey, cid, parentId, container);
          return;
        }

        // 2. REPLY ACTION
        if (replyBtn) {
          const cid = replyBtn.getAttribute('data-id');
          openReplyBox(postKey, cid, container);
          return;
        }

        // 3. DELETE ACTION
        if (deleteBtn) {
          const cid = deleteBtn.getAttribute('data-id');
          const parentId = deleteBtn.getAttribute('data-parent');
          deleteComment(postKey, cid, parentId, container);
          return;
        }
      });
    }
  }

  // Toggle Like Handler
  function toggleLike(postKey, cid, parentId, container) {
    const comments = loadComments(postKey);
    const userLikes = getUserLikes(postKey);
    const hasLiked = !!userLikes[cid];

    let targetItem = null;
    if (parentId) {
      const parent = comments.find((c) => c.id === parentId);
      if (parent && parent.replies) {
        targetItem = parent.replies.find((r) => r.id === cid);
      }
    } else {
      targetItem = comments.find((c) => c.id === cid);
    }

    if (!targetItem) return;

    if (hasLiked) {
      targetItem.likes = Math.max((targetItem.likes || 1) - 1, 0);
      delete userLikes[cid];
    } else {
      targetItem.likes = (targetItem.likes || 0) + 1;
      userLikes[cid] = true;
    }

    saveComments(postKey, comments);
    saveUserLikes(postKey, userLikes);
    renderComments(container, postKey);
  }

  // Open Inline Reply Box
  function openReplyBox(postKey, parentId, container) {
    const slot = container.querySelector(`#replySlot_${parentId}`);
    if (!slot) return;

    if (slot.style.display === 'block') {
      slot.style.display = 'none';
      slot.innerHTML = '';
      return;
    }

    slot.style.display = 'block';
    slot.innerHTML = `
      <div class="reply-form-box">
        <div style="display: flex; gap: 10px; margin-bottom: 10px; flex-wrap: wrap;">
          <input type="text" id="replyAuthor_${parentId}" class="comment-input-name" placeholder="답글 닉네임" style="font-size: 0.85rem; padding: 8px;">
          <input type="password" id="replyPw_${parentId}" class="comment-input-pw" placeholder="비밀번호" style="font-size: 0.85rem; padding: 8px;">
        </div>
        <textarea id="replyContent_${parentId}" class="comment-textarea" placeholder="답글 내용을 작성해주세요..." style="min-height: 60px; font-size: 0.88rem;"></textarea>
        <div style="display: flex; justify-content: flex-end; gap: 8px; margin-top: 8px;">
          <button type="button" class="sentiment-btn cancel-reply-btn" data-parent="${parentId}">취소</button>
          <button type="button" class="comment-submit-btn submit-reply-btn" data-parent="${parentId}" style="padding: 6px 14px; font-size: 0.85rem;">답글 등록</button>
        </div>
      </div>
    `;

    // Cancel Button
    slot.querySelector('.cancel-reply-btn').addEventListener('click', () => {
      slot.style.display = 'none';
      slot.innerHTML = '';
    });

    // Submit Reply Button
    slot.querySelector('.submit-reply-btn').addEventListener('click', () => {
      const rAuthor = slot.querySelector(`#replyAuthor_${parentId}`).value.trim();
      const rPw = slot.querySelector(`#replyPw_${parentId}`).value.trim();
      const rText = slot.querySelector(`#replyContent_${parentId}`).value.trim();

      if (!rAuthor) {
        alert('닉네임을 입력해주세요.');
        return;
      }
      if (!rText) {
        alert('답글 내용을 입력해주세요.');
        return;
      }

      const newReply = {
        id: 'r_user_' + Date.now(),
        author: rAuthor,
        password: rPw || '1234',
        role: '독자',
        date: getFormattedNow(),
        likes: 0,
        text: rText,
        isCustom: true
      };

      const comments = loadComments(postKey);
      const parent = comments.find((c) => c.id === parentId);
      if (parent) {
        if (!parent.replies) parent.replies = [];
        parent.replies.push(newReply);
        saveComments(postKey, comments);
        renderComments(container, postKey);

        if (window.showToast) {
          window.showToast('답글이 등록되었습니다! 💬');
        }
      }
    });
  }

  // Delete Comment Handler
  function deleteComment(postKey, cid, parentId, container) {
    const inputPw = prompt('댓글 작성 시 설정한 비밀번호를 입력해주세요:');
    if (inputPw === null) return;

    const comments = loadComments(postKey);

    if (parentId) {
      const parent = comments.find((c) => c.id === parentId);
      if (parent && parent.replies) {
        const rIndex = parent.replies.findIndex((r) => r.id === cid);
        if (rIndex !== -1) {
          const r = parent.replies[rIndex];
          if (r.password && r.password !== inputPw) {
            alert('비밀번호가 일치하지 않습니다.');
            return;
          }
          parent.replies.splice(rIndex, 1);
          saveComments(postKey, comments);
          renderComments(container, postKey);
          alert('답글이 삭제되었습니다.');
        }
      }
    } else {
      const cIndex = comments.findIndex((c) => c.id === cid);
      if (cIndex !== -1) {
        const c = comments[cIndex];
        if (c.password && c.password !== inputPw) {
          alert('비밀번호가 일치하지 않습니다.');
          return;
        }
        comments.splice(cIndex, 1);
        saveComments(postKey, comments);
        renderComments(container, postKey);
        alert('댓글이 삭제되었습니다.');
      }
    }
  }

  // Initialize on DOM Load
  document.addEventListener('DOMContentLoaded', () => {
    const commentTarget = document.getElementById('articleCommentsTarget') || document.querySelector('.article-comments-wrap');
    if (commentTarget) {
      const postKey = getPostKey();
      renderComments(commentTarget, postKey);
    }
  });

  // Export for global access if needed
  window.VSLComments = {
    render: renderComments,
    load: loadComments
  };
})();
