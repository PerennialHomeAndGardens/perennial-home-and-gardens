'use strict';

const menu = document.querySelector('.cleanMenu');
const menuLinks = document.getElementById('navlinks');

window.toggleMenu = () => {
  const open = menuLinks.classList.toggle('open');
  menu.setAttribute('aria-expanded', String(open));
};

window.toggleShare = async () => {
  const url = window.location.href;
  try {
    if (navigator.share) {
      await navigator.share({ title: document.title, url });
      return;
    }
    await navigator.clipboard.writeText(url);
    window.alert('Page link copied.');
  } catch (error) {
    if (error.name !== 'AbortError') window.prompt('Copy this page link:', url);
  }
};

window.openJoin = () => window.location.assign('/?join=1');

const kit = document.querySelector('.ep-kit');
if (kit) {
  const boxes = [...kit.querySelectorAll('input[type="checkbox"]')];
  const progress = document.getElementById('ep-kit-progress');
  const storageKey = 'phg-emergency-supplies-v1';

  function updateProgress() {
    const checked = boxes.filter(box => box.checked);
    progress.textContent = `${checked.length} of ${boxes.length} ready`;
    return checked.map(box => box.value);
  }

  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || '[]');
    if (Array.isArray(saved)) {
      for (const box of boxes) box.checked = saved.includes(box.value);
    }
  } catch {
    // The checklist still works when the browser blocks storage.
  }

  updateProgress();
  kit.addEventListener('change', () => {
    const checked = updateProgress();
    try {
      localStorage.setItem(storageKey, JSON.stringify(checked));
    } catch {
      // Leave the current checks in place for this visit.
    }
  });
}

for (const button of document.querySelectorAll('[data-print]')) {
  button.hidden = false;
  button.addEventListener('click', () => window.print());
}

const listen = document.querySelector('[data-listen]');
if (listen) {
  const status = document.getElementById('ep-audio-status');
  const audio = new Audio('/emergency-preparation/first-moves.mp3');
  audio.preload = 'none';

  function showPlayback(playing) {
    listen.textContent = playing ? 'Stop audio' : 'Listen';
    listen.setAttribute('aria-pressed', String(playing));
  }

  listen.hidden = false;
  audio.addEventListener('ended', () => showPlayback(false));
  listen.addEventListener('click', async () => {
    if (!audio.paused) {
      audio.pause();
      audio.currentTime = 0;
      showPlayback(false);
      return;
    }

    status.textContent = '';
    try {
      await audio.play();
      showPlayback(!audio.paused);
    } catch (error) {
      showPlayback(false);
      if (error.name !== 'AbortError') {
        status.textContent = 'Audio playback is unavailable. The first moves are listed below.';
      }
    }
  });
  window.addEventListener('pagehide', () => {
    audio.pause();
    showPlayback(false);
  });
}
