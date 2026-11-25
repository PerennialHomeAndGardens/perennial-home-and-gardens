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
if (listen && window.speechSynthesis && window.SpeechSynthesisUtterance) {
  const status = document.getElementById('ep-audio-status');
  const steps = document.getElementById(listen.dataset.listen);
  let reading = null;

  function finish() {
    reading = null;
    listen.textContent = 'Listen';
    listen.setAttribute('aria-pressed', 'false');
  }

  listen.hidden = false;
  listen.addEventListener('click', () => {
    if (reading) {
      finish();
      window.speechSynthesis.cancel();
      return;
    }

    const urgent = document.querySelector('.ep-urgent');
    const spokenText = [
      `${urgent.querySelector('a').textContent.replace('911', 'nine one one')} ${urgent.querySelector('span').textContent}.`,
      ...Array.from(steps.children, (step, index) => `Step ${index + 1}. ${step.textContent.trim()}`),
    ].join(' ');
    const utterance = new SpeechSynthesisUtterance(spokenText);
    utterance.lang = 'en-US';
    utterance.onend = () => { if (reading === utterance) finish(); };
    utterance.onerror = () => {
      if (reading !== utterance) return;
      finish();
      status.textContent = 'Audio playback is unavailable. The first moves are listed below.';
    };
    reading = utterance;
    status.textContent = '';
    listen.textContent = 'Stop audio';
    listen.setAttribute('aria-pressed', 'true');
    window.speechSynthesis.speak(utterance);
  });
  window.addEventListener('pagehide', () => {
    if (reading) {
      finish();
      window.speechSynthesis.cancel();
    }
  });
}
