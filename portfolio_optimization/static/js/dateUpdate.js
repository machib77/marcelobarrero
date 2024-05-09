'use strict';

document.getElementById('start_date').addEventListener('change', function () {
  updateDateRange();
  logChanges();
});

document.getElementById('end_date').addEventListener('change', function () {
  updateDateRange();
  logChanges();
});

function updateDateRange() {
  let startDate = document.getElementById('start_date').value;
  let endDate = document.getElementById('end_date').value;

  let formattedStartDate = new Date(startDate).toISOString().split('T')[0];
  let formattedEndDate = new Date(endDate).toISOString().split('T')[0];

  let formData = new FormData();
  formData.append('start_date', formattedStartDate);
  formData.append('end_date', formattedEndDate);

  // Fetch the CSRF token from the meta tag
  let csrfToken = document
    .querySelector('meta[name="csrf-token"]')
    .getAttribute('content');

  fetch('update-date-range', {
    method: 'POST',
    body: formData,
    headers: {
      'X-CSRFToken': csrfToken,
    },
  });
}

// Create a new MutationObserver instance
const observer = new MutationObserver(() => {
  logChanges();
});

// Observe changes to the 'selected-tickers' div
const selectedTickersDiv = document.getElementById('selected-tickers');
observer.observe(selectedTickersDiv, { childList: true, subtree: true });

const startDateInput = document.getElementById('start_date');
startDateInput.addEventListener('input', logChanges);

const endDateInput = document.getElementById('end_date');
endDateInput.addEventListener('input', logChanges);

function logChanges() {
  const startDate = new Date(startDateInput.value);
  const endDate = new Date(endDateInput.value);
  const selectedTickers = document.querySelectorAll(
    '#selected-tickers .ticker-item'
  ).length;
  console.log(
    `startDate: ${startDate}, endDate: ${endDate}, selectedTickers: ${selectedTickers}`
  );
}
