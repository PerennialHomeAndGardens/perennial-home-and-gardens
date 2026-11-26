(() => {
  'use strict';

  const peopleInput = document.querySelector('#meal-people');
  const status = document.querySelector('#meal-scale-status');
  const water = document.querySelector('#meal-water');
  const amounts = document.querySelectorAll('[data-quantity]');
  const number = new Intl.NumberFormat('en-US', { maximumFractionDigits: 2 });
  let lastValidCount = 1;

  function updateList() {
    if (!peopleInput.validity.valid) {
      status.textContent = 'Enter a whole number from 1 to 50. Showing the list for ' +
        lastValidCount + (lastValidCount === 1 ? ' person.' : ' people.');
      return;
    }

    const count = peopleInput.valueAsNumber;
    lastValidCount = count;
    const household = count + (count === 1 ? ' person' : ' people');
    for (const entry of amounts) {
      const total = Number(entry.dataset.quantity) * count;
      const unit = total === 1 ? entry.dataset.unit : entry.dataset.plural;
      entry.textContent = number.format(total) + ' ' + unit;
    }
    status.textContent = 'List for ' + household + '.';
    water.textContent = number.format(count * 7) + ' gallons for ' + household;
  }

  peopleInput.addEventListener('input', updateList);
  window.addEventListener('pageshow', updateList);
  document.querySelector('#meal-scale').hidden = false;
})();
