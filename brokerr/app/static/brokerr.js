//Used within tracker.html template to trigger manual screenshot capture of individual tracker
function captureProof(tracker) {
  // Disable the capture button while it works
  button = document.getElementById("captureButton");
  button.disabled = !button.disabled;

  //Show a status spinner
  var spans = button.children;
  for (var i = 0; i < spans.length; i++) {
    spans[i].classList.toggle("visually-hidden");
  }

  //Call the worker
  fetch("/captureProof", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ tracker: tracker }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Update the modal content with the data received from the server
      var modalBody = document.getElementById("captureModalMessage");
      modalBody.innerHTML = data.message;

      //Attach to close event to reload the page
      var modal = document.getElementById("captureModal");
      modal.addEventListener("hidden.bs.modal", function () {
        // Reload the page when the modal is closed
        location.reload();
      });

      // Show the modal
      var bsModal = new bootstrap.Modal(modal);
      bsModal.show();
    })
    .catch((error) => {
      console.log("Error capturing proof:", error);
    });
}

function showAddTrackerModal() {
  var modal = document.getElementById("trackerModal");
  var bsModal = new bootstrap.Modal(modal).show();
}

function addTracker() {
  var trackerName = document.getElementById("trackerName");
  var loginUrl = document.getElementById("loginUrl");
  var username = document.getElementById("username");
  var password = document.getElementById("password");
  var screenshotUrl = document.getElementById("screenshotUrl");

  // Call the backend
  fetch("/addTracker", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      "trackerName": trackerName.value,
      "loginUrl": loginUrl.value,
      "username": username.value,
      "password": password.value,
      "screenshot_url": screenshotUrl.value
    })
  })
  .then((response) => response.json())
  .then((data) => {
    if(data.success) {
      location.reload()
    }
  })
}

function showAddClientModal() {}

function checkPassword() {
  var password = document.getElementById("password").value;
  var passwordHelp = document.getElementById("passwordHelp");

  // Check password length
  if (password.length < 12) {
    passwordHelp.innerText = "Password must be at least 12 characters long.";
    passwordHelp.className = "form-text text-danger";
    return;
  }

  // Check password complexity
  var complexityRegex =
    /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*()_+{}\[\]:;<>,.?~\\/-]).{12,}$/;
  if (!complexityRegex.test(password)) {
    passwordHelp.innerText =
      "Password must include at least one uppercase letter, one lowercase letter, one digit, and one symbol (!@#$%^&*()_+{}[]:;<>,.?~/-).";
    passwordHelp.className = "form-text text-danger";
  } else {
    // Clear error message if password meets requirements
    passwordHelp.innerText = "";
    passwordHelp.className = "form-text text-muted";
  }
}

function validatePassword() {
  var currentPassword = document.getElementById("currentPassword");
  var password = document.getElementById("password").value;
  var confirmPassword = document.getElementById("confirmPassword").value;
  var passwordHelp = document.getElementById("passwordHelp");

  // Check if passwords match
  if (password !== confirmPassword) {
    passwordHelp.innerText = "Passwords don't match";
    passwordHelp.className = "form-text text-danger";
    return;
  } else {
    // Reset the password error message
    passwordHelp.innerText = "";
    passwordHelp.className = "form-text text-muted";

    // Call the change password API endpoint
    fetch("/updatePassword", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        old_password: currentPassword ? currentPassword.value : null,
        new_password: password,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        // TODO: Handle the response
        if (data.success) {
          
        }
        console.log(data);
      });
  }
}
