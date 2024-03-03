'use strict';
// console.log(tenorsJson);

function initialRates() {
  for (let key in tenorsJson) {
    // console.log(`Key: ${key}, Value: ${parseFloat(tenorsJson[key]).toFixed(2)}`);
    document.getElementById(key).value = parseFloat(tenorsJson[key]).toFixed(2);
  }

  document.getElementById('notional').value = 10000000;
  document.getElementById('fix-rate').value =
    document.getElementById('5Y').value;
  document.getElementById('flow-years').value = 5;

  let inputElement = document.getElementById('1D');
  // Simulo un evento input
  inputElement.dispatchEvent(new Event('change'));
}

window.addEventListener('load', initialRates);
