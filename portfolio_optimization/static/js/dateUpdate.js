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
  let runCalculationsBtn = document.getElementById('run-calculations-btn');

  // Get the current date
  const today = new Date();

  // Check if the years of startDate and endDate are greater than 2000
  const startDateYear = startDate.getFullYear();
  const endDateYear = endDate.getFullYear();

  // Calculate the difference in days between startDate and endDate
  const diffInDays = Math.abs((endDate - startDate) / (1000 * 60 * 60 * 24));

  if (
    selectedTickers >= 3 &&
    endDate > startDate &&
    startDateYear >= 2000 &&
    endDateYear >= 2000 &&
    startDate <= today &&
    endDate <= today &&
    diffInDays >= 360
  ) {
    runCalculationsBtn.disabled = false;
  } else {
    runCalculationsBtn.disabled = true;
  }
}

window.addEventListener('DOMContentLoaded', function () {
  const today = new Date();
  const fiveYearsAgo = new Date(
    today.getFullYear() - 5,
    today.getMonth(),
    today.getDate()
  );

  const endDateInput = document.getElementById('end_date');
  const startDateInput = document.getElementById('start_date');

  endDateInput.value = today.toISOString().split('T')[0];
  startDateInput.value = fiveYearsAgo.toISOString().split('T')[0];

  updateDateRange();
  logChanges();
});
