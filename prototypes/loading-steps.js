/**
 * AI 生成页：总进度 0–100% 驱动四步 ①②③④
 * 0–25% → ①检索 | 25–50% → ②出题 | 50–75% → ③排版 | 75–100% → ④准备
 */
(function () {
  var STEP_TEXT = [
    '① 正在检索考点…',
    '② 正在出题校验…',
    '③ 正在排版选项…',
    '④ 准备进入闯关…'
  ];

  function activeStepIndex(p) {
    if (p >= 100) return -1;
    if (p >= 75) return 3;
    if (p >= 50) return 2;
    if (p >= 25) return 1;
    return 0;
  }

  function applyProgress(root, progress) {
    var p = Math.max(0, Math.min(100, progress));
    var idx = activeStepIndex(p);
    var fillBar = root.querySelector('[data-gen-progress-fill]');
    var lineFill = root.querySelector('.nb-gen-stepper__fill');
    var sub = root.querySelector('[data-gen-sub]');
    var pencil = root.querySelector('.nb-pencil-bar > span')
      || root.querySelector('[data-gen-progress-fill] > span')
      || root.querySelector('.bt-progress-line > span');
    var steps = root.querySelectorAll('.nb-gen-step, .bt-step');

    if (pencil) pencil.style.width = p + '%';
    if (fillBar) {
      fillBar.setAttribute('aria-valuenow', String(Math.round(p)));
    }
    if (lineFill) {
      var trackW = 76;
      lineFill.style.width = (p / 100) * trackW + '%';
    }
    if (sub) {
      sub.textContent = p >= 100 ? '生成完成，即将进入闯关…' : STEP_TEXT[idx];
    }

    steps.forEach(function (el, i) {
      el.classList.remove('is-pending', 'is-active', 'is-done');
      if (p >= 100) {
        el.classList.add('is-done');
        return;
      }
      if (i < idx) el.classList.add('is-done');
      else if (i === idx) el.classList.add('is-active');
      else el.classList.add('is-pending');
    });
  }

  function runDemo(root) {
    var prog = 0;
    var timer = null;

    function tick() {
      var bump = prog < 40 ? 8 + Math.random() * 10 : prog < 80 ? 5 + Math.random() * 8 : 3 + Math.random() * 5;
      prog = Math.min(100, prog + bump);
      applyProgress(root, prog);

      if (prog >= 100) {
        timer = setTimeout(function () {
          prog = 0;
          applyProgress(root, 0);
          timer = setTimeout(tick, 400);
        }, 1800);
        return;
      }
      timer = setTimeout(tick, prog < 40 ? 550 : 750);
    }

    applyProgress(root, 0);
    timer = setTimeout(tick, 350);

    root._loadingStepsCleanup = function () {
      if (timer) clearTimeout(timer);
    };
  }

  function initRoot(root) {
    if (root.dataset.loadingStepsInit === '1') return;
    root.dataset.loadingStepsInit = '1';

    var mode = root.getAttribute('data-loading-mode') || 'demo';
    if (mode === 'static') {
      var p = Number(root.getAttribute('data-progress') || 62);
      applyProgress(root, p);
      return;
    }
    runDemo(root);
  }

  function initAll() {
    document.querySelectorAll('[data-gen-stepper]').forEach(initRoot);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
