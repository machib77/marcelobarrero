'use strict';
document.addEventListener('DOMContentLoaded', function () {
  // Get the current URL path
  const slider = document.querySelector('.tab-slider');
  let path = window.location.pathname;

  // Determine the page based on the path
  let page = '';
  if (path === '/') {
    page = 'home';
  } else if (path === '/about/') {
    page = 'about';
  } else if (path === '/contact/') {
    page = 'contact';
  } else if (path === '/portfolio/') {
    page = 'portfolio';
  }

  // Now 'page' contains the name of the current page
  let tabId = `tab-${page}`;

  let activeTab = document.getElementById(tabId);
  let tabRect = activeTab.getBoundingClientRect();
  slider.style.width = `${tabRect.width}px`;
  slider.style.left = `${tabRect.left}px`;
});
