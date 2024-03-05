'use strict';

document.addEventListener('htmx:afterSwap', function (event) {
  if (event.target.id === 'discount-container') {
    let inputElement = document.getElementById('fix-leg-trigger');
    inputElement.dispatchEvent(new Event('change'));
  }
});
