'use strict';
console.log('java script here!!!!pepe');

document.getElementById('start_date').addEventListener('change', function () {
  updateDateRange();
});

document.getElementById('end_date').addEventListener('change', function () {
  updateDateRange();
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
