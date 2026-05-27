/**
 * 参考首页：「换一批」轮换热门主题（仅 .ref-home）
 */
(function () {
  var ICONS = {
    layers:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>',
    sun:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.22 4.22l2.12 2.12M17.66 17.66l2.12 2.12M2 12h3M19 12h3M4.22 19.78l2.12-2.12M17.66 6.34l2.12-2.12"/></svg>',
    plus:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 12h16"/><path d="M12 4v16"/><path d="M8 8l8 8"/><path d="M16 8l-8 8"/></svg>',
    target:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v3"/><path d="M12 18v3"/><path d="M3 12h3"/><path d="M18 12h3"/><circle cx="12" cy="12" r="4"/></svg>',
    database:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.66 4.03 3 9 3s9-1.34 9-3V5"/><path d="M3 12c0 1.66 4.03 3 9 3s9-1.34 9-3"/></svg>',
    spark:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m12 3-1.9 5.8H4.2l4.9 3.6-1.9 5.8L12 14.6l4.8 3.6-1.9-5.8 4.9-3.6h-6.1L12 3z"/></svg>',
    box:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/></svg>',
    zap:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h9l-1 8 10-12h-9l1-8z"/></svg>',
    book:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>',
    git:
      '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><line x1="1.05" y1="12" x2="7" y2="12"/><line x1="17.01" y1="12" x2="22.96" y2="12"/></svg>'
  };

  var BATCHES = [
    [
      { title: 'RAG 基础概念', heat: '92%', tone: 'orange', icon: 'layers' },
      { title: '提示词工程', heat: '88%', tone: 'blue', icon: 'sun' },
      { title: 'TCP 三次握手', heat: '85%', tone: 'mint', icon: 'plus' },
      { title: 'Transformer', heat: '81%', tone: 'lavender', icon: 'target' },
      { title: 'Embedding 入门', heat: '78%', tone: 'blue', icon: 'database' }
    ],
    [
      { title: '向量数据库', heat: '90%', tone: 'blue', icon: 'database' },
      { title: 'LoRA 微调入门', heat: '86%', tone: 'lavender', icon: 'spark' },
      { title: 'Redis 缓存策略', heat: '83%', tone: 'orange', icon: 'box' },
      { title: 'Agent 工具调用', heat: '79%', tone: 'mint', icon: 'zap' },
      { title: 'MCP 协议速览', heat: '76%', tone: 'lavender', icon: 'spark' }
    ],
    [
      { title: 'Kotlin 协程', heat: '87%', tone: 'mint', icon: 'zap' },
      { title: '设计模式速记', heat: '84%', tone: 'blue', icon: 'book' },
      { title: 'Git 分支策略', heat: '82%', tone: 'orange', icon: 'git' },
      { title: '注意力机制', heat: '80%', tone: 'lavender', icon: 'target' },
      { title: 'Docker 网络', heat: '77%', tone: 'orange', icon: 'box' }
    ]
  ];

  var SWAP_MS = 200;

  function escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }

  function renderTopic(topic) {
    var icon = ICONS[topic.icon] || ICONS.layers;
    return (
      '<div class="ref-topic" role="listitem">' +
      '<div class="ref-topic-icon ref-topic-icon--' +
      escapeHtml(topic.tone) +
      '" aria-hidden="true">' +
      icon +
      '</div><strong>' +
      escapeHtml(topic.title) +
      '</strong><span class="heat">热度 ' +
      escapeHtml(topic.heat) +
      '</span></div>'
    );
  }

  function renderBatch(batch) {
    return batch.map(renderTopic).join('');
  }

  function readTitles(row) {
    return Array.prototype.map.call(row.querySelectorAll('.ref-topic strong'), function (el) {
      return el.textContent.trim();
    });
  }

  function findBatchIndex(titles) {
    var key = titles.join('\n');
    for (var i = 0; i < BATCHES.length; i++) {
      if (
        BATCHES[i]
          .map(function (t) {
            return t.title;
          })
          .join('\n') === key
      ) {
        return i;
      }
    }
    return 0;
  }

  function ensureTopicStrip(row) {
    var parent = row.parentElement;
    if (parent && parent.classList.contains('ref-topic-strip')) return parent;
    var strip = document.createElement('div');
    strip.className = 'ref-topic-strip';
    row.parentNode.insertBefore(strip, row);
    strip.appendChild(row);
    return strip;
  }

  function updateTopicStripEdges(strip, row) {
    var maxScroll = row.scrollWidth - row.clientWidth;
    if (maxScroll <= 2) {
      strip.classList.add('is-at-start', 'is-at-end');
      return;
    }
    strip.classList.toggle('is-at-start', row.scrollLeft <= 2);
    strip.classList.toggle('is-at-end', row.scrollLeft >= maxScroll - 2);
  }

  function initTopicSwipe(strip, row) {
    row.setAttribute('tabindex', '0');
    row.setAttribute('role', 'list');
    if (!row.getAttribute('aria-label')) {
      row.setAttribute('aria-label', '热门主题，可左右滑动');
    }

    var drag = { active: false, startX: 0, startScroll: 0, moved: false };

    function endDrag(e) {
      if (!drag.active) return;
      drag.active = false;
      row.classList.remove('is-dragging');
      try {
        if (e && e.pointerId != null) row.releasePointerCapture(e.pointerId);
      } catch (err) {
        /* ignore */
      }
      updateTopicStripEdges(strip, row);
    }

    row.addEventListener('scroll', function () {
      updateTopicStripEdges(strip, row);
    }, { passive: true });

    row.addEventListener('pointerdown', function (e) {
      if (e.button !== 0) return;
      drag.active = true;
      drag.moved = false;
      drag.startX = e.clientX;
      drag.startScroll = row.scrollLeft;
      row.classList.add('is-dragging');
      row.setPointerCapture(e.pointerId);
    });

    row.addEventListener('pointermove', function (e) {
      if (!drag.active) return;
      var dx = e.clientX - drag.startX;
      if (Math.abs(dx) > 4) drag.moved = true;
      row.scrollLeft = drag.startScroll - dx;
    });

    row.addEventListener('pointerup', endDrag);
    row.addEventListener('pointercancel', endDrag);
    row.addEventListener('lostpointercapture', function () {
      drag.active = false;
      row.classList.remove('is-dragging');
    });

    row.addEventListener('click', function (e) {
      if (drag.moved) {
        e.preventDefault();
        e.stopPropagation();
        drag.moved = false;
      }
    }, true);

    row.addEventListener('keydown', function (e) {
      var step = 160;
      if (e.key === 'ArrowRight') {
        row.scrollBy({ left: step, behavior: 'smooth' });
        e.preventDefault();
      } else if (e.key === 'ArrowLeft') {
        row.scrollBy({ left: -step, behavior: 'smooth' });
        e.preventDefault();
      }
    });

    row.addEventListener(
      'wheel',
      function (e) {
        if (row.scrollWidth <= row.clientWidth) return;
        if (Math.abs(e.deltaY) <= Math.abs(e.deltaX)) return;
        row.scrollLeft += e.deltaY;
        e.preventDefault();
        updateTopicStripEdges(strip, row);
      },
      { passive: false }
    );

    if (typeof ResizeObserver !== 'undefined') {
      var ro = new ResizeObserver(function () {
        updateTopicStripEdges(strip, row);
      });
      ro.observe(row);
    }

    updateTopicStripEdges(strip, row);
  }

  function initHome(home) {
    var row = home.querySelector('[data-ref-topic-row]');
    var btn = home.querySelector('[data-ref-topic-shuffle]');
    if (!row || !btn || home.dataset.refTopicsInit === '1') return;
    home.dataset.refTopicsInit = '1';

    var strip = ensureTopicStrip(row);
    initTopicSwipe(strip, row);

    var batchIndex = findBatchIndex(readTitles(row));

    btn.addEventListener('click', function () {
      if (row.classList.contains('is-swapping')) return;
      row.classList.add('is-swapping');
      window.setTimeout(function () {
        batchIndex = (batchIndex + 1) % BATCHES.length;
        row.innerHTML = renderBatch(BATCHES[batchIndex]);
        row.scrollLeft = 0;
        row.classList.remove('is-swapping');
        updateTopicStripEdges(strip, row);
        btn.setAttribute(
          'aria-label',
          '换一批热门主题，当前第 ' + (batchIndex + 1) + ' 组，共 ' + BATCHES.length + ' 组'
        );
      }, SWAP_MS);
    });

    btn.setAttribute(
      'aria-label',
      '换一批热门主题，当前第 ' + (batchIndex + 1) + ' 组，共 ' + BATCHES.length + ' 组'
    );
  }

  function initAll() {
    document.querySelectorAll('.ref-home').forEach(initHome);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
