'use strict';
// console.log(tenorsJson);

function initialRates() {
  for (let key in tenorsJson) {
    // console.log(`Key: ${key}, Value: ${parseFloat(tenorsJson[key]).toFixed(2)}`);
    document.getElementById(key).value = parseFloat(tenorsJson[key]).toFixed(2);
  }

  let inputElement = document.getElementById('1D');
  // Simulo un evento input
  inputElement.dispatchEvent(new Event('change'));
}

window.addEventListener('load', initialRates);
