'use strict';

document.getElementById('start_date').addEventListener('change', function () {
  updateDateRange();
});

document.getElementById('end_date').addEventListener('change', function () {
  updateDateRange();
});

function updateDateRange() {
  let runCalculationsBtn = document.getElementById('run-calculations-btn');
  let selectedTickersDiv = document.getElementById('selected-tickers');

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
  }).then(html => {
    let selectedTickers = selectedTickersDiv.querySelectorAll('.ticker-item');
    console.log(`Number of selected tickers: ${selectedTickers.length}`);
    console.log(`Start: ${startDate}; End: ${endDate}`);
    checkButtonState(runCalculationsBtn, selectedTickers, endDate, startDate);
  });
}

function checkButtonState(
  runCalculationsBtn,
  selectedTickers,
  endDate,
  startDate
) {
  if (selectedTickers.length >= 3 && endDate > startDate) {
    runCalculationsBtn.disabled = false;
  } else {
    runCalculationsBtn.disabled = true;
  }
}
