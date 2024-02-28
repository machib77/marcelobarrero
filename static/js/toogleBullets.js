'use strict';
document.addEventListener('DOMContentLoaded', function () {
  const items = document.querySelectorAll('.item-container');

  items.forEach(item => {
    const title = item.querySelector('.grid-container');

    title.addEventListener('click', function () {
      const ul = item.querySelector('ul');
      if (ul.style.display === 'none' || ul.style.display === '') {
        ul.style.display = 'block';
      } else {
        ul.style.display = 'none';
      }
    });
  });
});
