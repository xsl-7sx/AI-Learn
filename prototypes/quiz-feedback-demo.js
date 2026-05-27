/**
 * 答题反馈屏：循环演示「选题 → 对错反馈 → 解析」动效
 * 仅作用于 [data-feedback-demo]，进入视口时播放，离开视口暂停
 */
(function () {
  var TIMING = {
    correct: { select: 450, result: 750, bar: 1050, note: 1450, hold: 4200 },
    wrong: { wrong: 450, answer: 850, bar: 1150, note: 1550, hold: 4500 }
  };

  function replayAnimation(el) {
    if (!el) return;
    el.style.animation = 'none';
    void el.offsetHeight;
    el.style.animation = '';
  }

  function clearTimers(root) {
    (root._feedbackTimers || []).forEach(clearTimeout);
    root._feedbackTimers = [];
  }

  function schedule(root, fn, delay) {
    root._feedbackTimers = root._feedbackTimers || [];
    root._feedbackTimers.push(setTimeout(fn, delay));
  }

  function resetRoot(root) {
    root.querySelectorAll('[data-feedback-opt]').forEach(function (opt) {
      opt.classList.remove('is-selected', 'is-correct', 'is-wrong', 'bt-opt--reveal', 'bt-opt--reveal-delay');
    });
    root.querySelectorAll('[data-feedback-part]').forEach(function (part) {
      part.classList.add('is-feedback-idle');
      part.classList.remove('bt-teacher-note--reveal');
    });
  }

  function playCorrect(root) {
    var answer = root.querySelector('[data-feedback-opt="answer"]');
    var bar = root.querySelector('[data-feedback-part="bar"]');
    var note = root.querySelector('[data-feedback-part="note"]');
    var t = TIMING.correct;

    clearTimers(root);
    resetRoot(root);

    schedule(root, function () {
      if (answer) answer.classList.add('is-selected');
    }, t.select);

    schedule(root, function () {
      if (answer) {
        answer.classList.remove('is-selected');
        answer.classList.add('is-correct', 'bt-opt--reveal');
        replayAnimation(answer);
      }
    }, t.result);

    schedule(root, function () {
      if (bar) {
        bar.classList.remove('is-feedback-idle');
        replayAnimation(bar);
        replayAnimation(bar.querySelector('.bt-feedback-bar__icon'));
      }
    }, t.bar);

    schedule(root, function () {
      if (note) {
        note.classList.remove('is-feedback-idle');
        note.classList.add('bt-teacher-note--reveal');
        replayAnimation(note);
      }
    }, t.note);

    schedule(root, function () {
      playCorrect(root);
    }, t.hold);
  }

  function playWrong(root) {
    var wrong = root.querySelector('[data-feedback-opt="wrong"]');
    var answer = root.querySelector('[data-feedback-opt="answer"]');
    var bar = root.querySelector('[data-feedback-part="bar"]');
    var note = root.querySelector('[data-feedback-part="note"]');
    var t = TIMING.wrong;

    clearTimers(root);
    resetRoot(root);

    schedule(root, function () {
      if (wrong) {
        wrong.classList.add('is-wrong', 'bt-opt--reveal');
        replayAnimation(wrong);
      }
    }, t.wrong);

    schedule(root, function () {
      if (answer) {
        answer.classList.add('is-correct', 'bt-opt--reveal-delay');
        replayAnimation(answer);
      }
    }, t.answer);

    schedule(root, function () {
      if (bar) {
        bar.classList.remove('is-feedback-idle');
        replayAnimation(bar);
        replayAnimation(bar.querySelector('.bt-feedback-bar__icon'));
      }
    }, t.bar);

    schedule(root, function () {
      if (note) {
        note.classList.remove('is-feedback-idle');
        note.classList.add('bt-teacher-note--reveal');
        replayAnimation(note);
      }
    }, t.note);

    schedule(root, function () {
      playWrong(root);
    }, t.hold);
  }

  function stopDemo(root) {
    clearTimers(root);
    root._feedbackRunning = false;
    resetRoot(root);
  }

  function startDemo(root) {
    if (root._feedbackRunning) return;
    root._feedbackRunning = true;
    var mode = root.getAttribute('data-feedback-demo');
    if (mode === 'wrong') playWrong(root);
    else playCorrect(root);
  }

  function initRoot(root) {
    resetRoot(root);
    if (root.dataset.feedbackDemoInit === '1') return;
    root.dataset.feedbackDemoInit = '1';

    if ('IntersectionObserver' in window) {
      var observer = new IntersectionObserver(
        function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) startDemo(entry.target);
            else stopDemo(entry.target);
          });
        },
        { threshold: 0.35, rootMargin: '0px 0px -8% 0px' }
      );
      observer.observe(root);
      root._feedbackObserver = observer;
    } else {
      startDemo(root);
    }
  }

  function initAll() {
    document.querySelectorAll('[data-feedback-demo]').forEach(initRoot);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAll);
  } else {
    initAll();
  }
})();
