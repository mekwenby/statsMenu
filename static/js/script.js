let selectedDots = [];
const lockScreen = document.getElementById('lockScreen');
const message = document.getElementById('message');

function selectDot(dot) {
  if (selectedDots.indexOf(dot) === -1) {
    selectedDots.push(dot);
    updateLockDots();
  }
}

function updateLockDots() {
  const dots = document.querySelectorAll('.dot');
  dots.forEach(dot => {
    const index = dot.getAttribute('data-index');
    if (selectedDots.indexOf(index) !== -1) {
      dot.classList.add('selected');
    } else {
      dot.classList.remove('selected');
    }
  });
  if (selectedDots.length === 4) {
    // Send the password to the backend
    const password = selectedDots.join('');
    sendPasswordToBackend(password);
  }
}

function resetLock() {
  selectedDots = [];
  updateLockDots();
  message.style.display = 'none';
}

function sendPasswordToBackend(password) {
  // Replace this with your actual backend API endpoint
  const endpoint = '/api/checkPassword';
  // Replace 'YOUR_BACKEND_SECRET_KEY' with your actual secret key for authentication on the backend
  const secretKey = 'YOUR_BACKEND_SECRET_KEY';

  // Simulate sending the password to the backend for verification
  // In a real application, you would use AJAX or fetch to send the data securely to the backend
  // and handle the response accordingly.
  $.post(endpoint, { password: password, secretKey: secretKey }, function (data) {
    if (data.isValid) {
      message.innerHTML = '<div class="alert alert-success">Password is correct!</div>';
      message.style.display = 'block';
    } else {
      message.innerHTML = '<div class="alert alert-danger">Password is incorrect!</div>';
      message.style.display = 'block';
    }
  });
}
