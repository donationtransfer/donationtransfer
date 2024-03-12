function loginUser() {
    var usernameOrEmail = document.getElementById("usernameOrEmail").value;
    var password = document.getElementById("password").value;

    fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username_or_email: usernameOrEmail, password: password })
    })
        .then(response => {
            if (!response.ok) {
                throw new Error('Login failed');
            }
            return response.json();
        })
        .then(data => {
            console.log(data.message); 
            session.add('authenticated')
        })
        .catch(error => {
            console.error('Error during login:', error);
            alert('Login failed');
        });
}
