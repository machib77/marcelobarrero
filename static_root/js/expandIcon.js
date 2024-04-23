'use strict';
const template = document.getElementById('plus-svg').content;
const svgContainers = document.querySelectorAll('.svg-container');

svgContainers.forEach(svgContainer => {
  const svgClone = template.cloneNode(true);
  svgContainer.appendChild(svgClone);
});
