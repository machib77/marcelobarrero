'use strict';
document.addEventListener('DOMContentLoaded', function () {
  const items = document.querySelectorAll('.item-container');

  items.forEach(item => {
    const title = item.querySelector('.grid-container');

    title.addEventListener('click', function () {
      const ul = item.querySelector('ul');
      const hTwo = item.querySelector('h2');
      const svgElement = hTwo.querySelector('svg');
      if (ul.style.display === 'none' || ul.style.display === '') {
        ul.style.display = 'block';
        if (svgElement) {
          svgElement.remove();
          const template = document.getElementById('dash-svg').content;
          const svgClone = template.cloneNode(true);
          hTwo.appendChild(svgClone);
        }
      } else {
        ul.style.display = 'none';
        if (svgElement) {
          svgElement.remove();
          const template = document.getElementById('plus-svg').content;
          const svgClone = template.cloneNode(true);
          hTwo.appendChild(svgClone);
        }
      }
    });
  });
});
