'use strict';
document.addEventListener('DOMContentLoaded', function () {
  let messages = document.querySelectorAll('.message.success-fadeout');
  messages.forEach(function (message) {
    setTimeout(function () {
      message.style.display = 'none';
    }, 8000);
  });
});

console.log('javascript in tha house!');
