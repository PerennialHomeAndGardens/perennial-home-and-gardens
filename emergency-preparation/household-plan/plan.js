'use strict';

const planFields = document.querySelectorAll('.plan-field');

function updatePrintValues() {
  for (const field of planFields) {
    field.querySelector('.plan-print-value').textContent =
      field.querySelector('textarea').value.replace(/\s+/g, ' ').trim();
  }
}

window.addEventListener('beforeprint', updatePrintValues);
document.querySelector('.plan-sheet').addEventListener('input', updatePrintValues);
