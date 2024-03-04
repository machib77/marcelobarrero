'use strict';
const inputs = document.querySelectorAll('#swap-inputs-form input');

function handleInputChange(event) {
  console.log('Input changed:', event.target.value);
  // Simulo un evento input para rates
  let inputElement = document.getElementById('1D');
  inputElement.dispatchEvent(new Event('change'));
}

inputs.forEach(input => {
  input.addEventListener('change', handleInputChange);
});
