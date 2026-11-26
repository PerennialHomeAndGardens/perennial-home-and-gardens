(() => {
  'use strict';

  const calculator = document.querySelector('#pantry-calculator');
  const refillForm = document.querySelector('#refill-plan');
  const rotateForm = document.querySelector('#rotation-form');
  const itemInput = rotateForm.elements.namedItem('item');
  const rotationBody = document.querySelector('#rotation-items');
  const cancelEdit = document.querySelector('#cancel-edit');
  const storageMessage = document.querySelector('#pantry-storage');
  const logStatus = document.querySelector('#pantry-log-status');
  const storageKey = 'phg-pantry-water-planner-v1';
  const number = new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 });
  const dateLabel = new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' });
  const inputForms = { figures: calculator, refill: refillForm };

  let saved = {};
  let editing = null;
  let items = [];

  function showTemporaryNote() {
    storageMessage.textContent = 'Browser storage is unavailable. Print the planner to keep your entries.';
  }

  try {
    const restored = JSON.parse(localStorage.getItem(storageKey) || '{}');
    if (restored && typeof restored === 'object') saved = restored;
  } catch {
    showTemporaryNote();
  }

  for (const [key, form] of Object.entries(inputForms)) {
    for (const field of form.elements) {
      const value = saved[key]?.[field.name];
      if (typeof value === 'string') field.value = value;
    }
    form.hidden = false;
  }

  if (Array.isArray(saved.items)) {
    items = saved.items.filter(entry => typeof entry?.id === 'string' &&
      typeof entry.name === 'string' && entry.name.length > 0 &&
      typeof entry.review === 'string' && /^\d{4}-\d{2}-\d{2}$/.test(entry.review) &&
      Number.isFinite(new Date(entry.review + 'T12:00:00').getTime()));
  }

  function save() {
    const data = { items };
    for (const [key, form] of Object.entries(inputForms)) {
      data[key] = Object.fromEntries(new FormData(form));
    }
    try {
      localStorage.setItem(storageKey, JSON.stringify(data));
    } catch {
      showTemporaryNote();
    }
  }

  function estimate() {
    const valid = calculator.checkValidity();
    document.querySelector('#pantry-calc-error').hidden = valid;
    document.querySelector('#pantry-results').hidden = !valid;
    if (!valid) return;

    const { people, meals, stock, water } = calculator.elements;
    const household = people.valueAsNumber;
    const servings = household * Number(meals.value) * 30;
    const mealGap = Math.max(0, servings - stock.valueAsNumber);
    const waterTarget = household * 30;
    const waterGap = Math.max(0, waterTarget - water.valueAsNumber);
    const coverage = Math.floor(water.valueAsNumber / household);

    document.querySelector('#meal-target').value = number.format(servings) + ' meal servings for 30 days';
    document.querySelector('#meal-gap').textContent = mealGap
      ? number.format(mealGap) + ' servings still to stock'
      : 'Your recorded servings meet this target.';
    document.querySelector('#water-target').value = number.format(waterTarget) + ' gallons for 30 days at baseline';
    document.querySelector('#water-coverage').textContent = coverage
      ? 'On hand covers ' + number.format(coverage) + (coverage === 1 ? ' full day' : ' full days') +
        ' at baseline. Arrange a refill before that supply runs out.'
      : 'On hand covers less than one full day. Arrange a safe source now if water service is out.';
    document.querySelector('#water-gap').textContent = waterGap
      ? number.format(waterGap) + ' gallons still to store or arrange through safe refills'
      : 'Your recorded gallons meet this baseline target.';
  }

  function resetEditor() {
    editing = null;
    rotateForm.reset();
    rotateForm.querySelector('[type="submit"]').textContent = 'Add item';
    cancelEdit.hidden = true;
  }

  function action(label, entry, handler) {
    const button = document.createElement('button');
    button.type = 'button';
    button.className = 'ep-plain-button';
    button.textContent = label;
    button.setAttribute('aria-label', label + ' ' + entry.name);
    button.addEventListener('click', handler);
    return button;
  }

  function renderItems() {
    const rows = [...items].sort((a, b) => a.review.localeCompare(b.review) || a.name.localeCompare(b.name));
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    rotationBody.replaceChildren();

    for (const entry of rows) {
      const row = rotationBody.insertRow();
      row.insertCell().textContent = entry.name;
      const reviewDate = new Date(entry.review + 'T12:00:00');
      const due = new Date(reviewDate);
      due.setHours(0, 0, 0, 0);
      row.insertCell().textContent = dateLabel.format(reviewDate) + (due <= today ? ' · Review due' : '');
      row.insertCell().append(
        action('Edit', entry, () => {
          editing = entry.id;
          itemInput.value = entry.name;
          rotateForm.elements.review.value = entry.review;
          rotateForm.querySelector('[type="submit"]').textContent = 'Save item';
          cancelEdit.hidden = false;
          itemInput.focus();
        }),
        action('Remove', entry, () => {
          items = items.filter(current => current.id !== entry.id);
          if (editing === entry.id) resetEditor();
          renderItems();
          save();
          logStatus.textContent = entry.name + ' removed.';
          itemInput.focus();
        })
      );
    }

    document.querySelector('#pantry-log-empty').hidden = rows.length > 0;
    rotationBody.closest('.pantry-table-wrap').hidden = rows.length === 0;
  }

  function updatePrintFields() {
    document.querySelectorAll('.pantry-printed-value').forEach(node => node.remove());
    for (const form of Object.values(inputForms)) {
      for (const field of form.elements) {
        const span = document.createElement('span');
        span.className = 'pantry-printed-value';
        span.textContent = field.selectedOptions?.[0]?.textContent || field.value || '________________';
        field.after(span);
      }
    }
  }

  for (const form of Object.values(inputForms)) {
    form.addEventListener('submit', event => event.preventDefault());
    form.addEventListener('input', () => {
      if (form === calculator) estimate();
      save();
    });
  }

  window.addEventListener('beforeprint', updatePrintFields);

  rotateForm.addEventListener('submit', event => {
    event.preventDefault();
    const name = itemInput.value.trim();
    const review = rotateForm.elements.review.value;
    if (!name) {
      logStatus.textContent = 'Enter an item name.';
      itemInput.focus();
      return;
    }

    if (editing) {
      const entry = items.find(item => item.id === editing);
      entry.name = name;
      entry.review = review;
    } else {
      items.push({ id: crypto.randomUUID(), name, review });
    }
    logStatus.textContent = name + ' saved.';
    resetEditor();
    renderItems();
    save();
    itemInput.focus();
  });

  cancelEdit.addEventListener('click', () => {
    resetEditor();
    itemInput.focus();
  });

  estimate();
  renderItems();
  document.querySelector('#pantry-log').hidden = false;
})();
