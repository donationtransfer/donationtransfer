function registerUser() {
    var regEmail = document.getElementById("regEmail").value;
    var regPassword = document.getElementById("regPassword").value;
    var confirmPassword = document.getElementById("regConfirmPassword").value;

    var emailPattern = /\S+@\S+\.\S+/;
    if (!emailPattern.test(regEmail)) {
        alert("Invalid email address");
        return false;
    }

    var passwordPattern = /^(?=.*[A-Z])(?=.*\d).{8,}$/;
    if (!passwordPattern.test(regPassword)) {
        alert("Password must contain at least 8 characters with one uppercase letter and one numeric value");
        return false;
    }

    if (regPassword !== confirmPassword) {
        alert("Passwords do not match");
        return false;
    }

    // Assuming the server endpoint /register handles the registration logic
    fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email: regEmail, password: regPassword })
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log("Registration successful");
                // Redirect or update UI accordingly
            } else {
                alert("Registration failed: " + data.message);
            }
        })
        .catch(error => {
            console.error('Error during registration:', error);
        });
}
