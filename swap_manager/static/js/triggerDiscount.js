'use strict';

document.addEventListener('htmx:afterSwap', function (event) {
  if (event.target.id === 'chart-container') {
    let inputElement = document.getElementById('discount-trigger');
    inputElement.dispatchEvent(new Event('change'));
  }
});
