'use strict';

document.getElementById('start_date').addEventListener('change', function () {
  updateDateRange();
});

document.getElementById('end_date').addEventListener('change', function () {
  updateDateRange();
});

let selectedTickersDiv = document.getElementById('selected-tickers');
selectedTickersDiv.addEventListener('click', handleRemoveBtnClick);

function updateDateRange() {
  let runCalculationsBtn = document.getElementById('run-calculations-btn');
  let selectedTickersDiv = document.getElementById('selected-tickers');

  let selectedTickers = selectedTickersDiv.querySelectorAll('.ticker-item');

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

  if (selectedTickers.length >= 3 && endDate > startDate) {
    console.log('condiciones se cumplen');
    runCalculationsBtn.disabled = false;
  } else {
    runCalculationsBtn.disabled = true;
    console.log('condiciones no se cumplen');
  }
}

function handleRemoveBtnClick(event) {
  if (event.target.classList.contains('remove-btn')) {
    updateDateRange();
    console.log('se pinchó algún botón remove');
  }
}
