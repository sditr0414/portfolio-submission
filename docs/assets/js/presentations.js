(() => {
  'use strict';
  const $ = id => document.getElementById(id);
  const key = new URLSearchParams(location.search).get('project');
  function returnUrl() {
    const raw = new URLSearchParams(location.search).get('return');
    if (raw) {
      try {
        const url = new URL(raw, location.href);
        const home = new URL('index.html', location.href);
        if (url.origin === home.origin && url.pathname === home.pathname) return url.href;
      } catch {}
    }
    return `index.html#${encodeURIComponent(key || 'projects')}`;
  }
  $('back').href = returnUrl();
  let deck, current = 1, requested = 0;
  const source = n => `assets/presentations/${key}/${String(n).padStart(2, '0')}.webp?v=20261014trim`;
  const pageFromHash = () => Number(location.hash.match(/^#slide-(\d+)$/)?.[1] || 1);
  function show(number, updateHash = true) {
    const n = Math.max(1, Math.min(deck.count, Math.trunc(number) || 1));
    current = n;
    $('page').value = n;
    $('prev').disabled = n === 1;
    $('next').disabled = n === deck.count;
    $('position').textContent = `${n} / ${deck.count}`;
    $('slide-text').textContent = deck.pages[n - 1].text || '이미지로 구성된 슬라이드입니다.';
    $('slide').alt = `${deck.title} · ${n}번째 슬라이드`;
    $('slide').width = deck.pages[n - 1].width;
    $('slide').height = deck.pages[n - 1].height;
    $('canvas').setAttribute('aria-busy', 'true');
    $('image-error').hidden = true;
    $('canvas').scrollTo(0, 0);
    const token = ++requested;
    const img = new Image();
    img.onload = () => {
      if (token !== requested) return;
      $('slide').src = img.src;
      $('canvas').setAttribute('aria-busy', 'false');
      if (n < deck.count) { const next = new Image(); next.src = source(n + 1); }
    };
    img.onerror = () => {
      if (token !== requested) return;
      $('canvas').setAttribute('aria-busy', 'false');
      $('image-error').hidden = false;
    };
    img.src = source(n);
    if (updateHash) history.replaceState(null, '', `#slide-${n}`);
  }
  async function init() {
    try {
      const response = await fetch('assets/presentations/manifest.json?v=20261014trim');
      if (!response.ok) throw new Error('manifest');
      const decks = await response.json();
      if (!Object.hasOwn(decks, key)) {
        $('title').textContent = '발표자료를 찾을 수 없습니다';
        $('message').textContent = '포트폴리오로 돌아가 프로젝트의 전체 발표자료 링크를 선택해 주세요.';
        return;
      }
      deck = decks[key];
      document.title = `${deck.title} · 전체 발표자료 | 정승호`;
      $('title').textContent = deck.title;
      if (deck.sourceNote) { $('source-note').textContent = deck.sourceNote; $('source-note').hidden = false; }
      $('back').href = returnUrl();
      $('download').href = `assets/presentations/${key}/slides.pdf?v=20261014trim`;
      $('download').download = `${deck.title}_전체발표자료.pdf`;
      $('download').hidden = false;
      $('total').textContent = `/ ${deck.count}`;
      $('page').max = deck.count;
      $('viewer').hidden = false;
      $('message').hidden = true;
      $('prev').addEventListener('click', () => show(current - 1));
      $('next').addEventListener('click', () => show(current + 1));
      $('retry').addEventListener('click', () => show(current));
      $('jump').addEventListener('submit', event => { event.preventDefault(); show(Number($('page').value)); });
      $('zoom').addEventListener('click', () => {
        const zoomed = $('canvas').classList.toggle('zoomed');
        $('zoom').setAttribute('aria-pressed', String(zoomed));
        $('zoom').textContent = zoomed ? '화면에 맞추기' : '확대 보기';
      });
      document.addEventListener('keydown', event => {
        if (event.target.matches('input,textarea,select') || event.ctrlKey || event.metaKey || event.altKey) return;
        if (event.target === $('canvas') && $('canvas').classList.contains('zoomed')) return;
        const moves = { ArrowLeft: current - 1, ArrowRight: current + 1, Home: 1, End: deck.count };
        if (Object.hasOwn(moves, event.key)) { event.preventDefault(); show(moves[event.key]); }
      });
      window.addEventListener('hashchange', () => show(pageFromHash(), false));
      show(pageFromHash());
    } catch (error) {
      $('title').textContent = '전체 발표자료';
      $('message').textContent = '자료를 불러오지 못했습니다. 연결을 확인하고 페이지를 새로고침해 주세요.';
    }
  }
  init();
})();
