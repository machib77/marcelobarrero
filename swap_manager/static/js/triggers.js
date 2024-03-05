'use strict';

document.addEventListener('htmx:afterSwap', function (event) {
  if (event.target.id === 'chart-container') {
    let inputElement = document.getElementById('discount-trigger');
    inputElement.dispatchEvent(new Event('change'));
  }
});

document.addEventListener('htmx:afterSwap', function (event) {
  if (event.target.id === 'discount-container') {
    let inputElement = document.getElementById('fix-leg-trigger');
    inputElement.dispatchEvent(new Event('change'));
  }
});

document.addEventListener('htmx:afterSwap', function (event) {
  if (event.target.id === 'fix-leg-container') {
    let inputElement = document.getElementById('float-leg-trigger');
    inputElement.dispatchEvent(new Event('change'));
  }
});
