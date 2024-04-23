'use strict';
// console.log(tenorsJson);

function initialConditions() {
  for (let key in curveDefaultsJson) {
    document.getElementById(key).value = parseFloat(
      curveDefaultsJson[key]
    ).toFixed(2);
  }

  for (let key in swapDefaultsJson) {
    if (key == 'flow-years') {
      document.getElementById(key).value = parseFloat(
        swapDefaultsJson[key]
      ).toFixed(0);
    } else {
      document.getElementById(key).value = parseFloat(
        swapDefaultsJson[key]
      ).toFixed(2);
    }
  }

  // Simulo un evento input para rates
  let inputElement = document.getElementById('1D');
  inputElement.dispatchEvent(new Event('change'));

  // Simulo un evento input para swap_defaults
  let inputSwapDefault = document.getElementById('notional');
  inputSwapDefault.dispatchEvent(new Event('change'));
}

window.addEventListener('load', initialConditions);
