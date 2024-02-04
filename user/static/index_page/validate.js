function validateForm(event){
    
    let name = document.forms["user_register"]["name"].value;
    let email = document.forms["user_register"]["email"].value;
    let phone = document.forms["user_register"]["phone"].value;
    let username = document.forms["user_register"]["username"].value;
    let password1 = document.forms["user_register"]["password1"].value;
    let password2 = document.forms["user_register"]["password2"].value;


    // Validate email format using a regular expression
    let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
        alert("Invalid email format");
        event.preventDefault();
        return false;
    }

    // Check if the phone number has exactly 10 digits
    let phoneRegex = /^\d{10}$/;
    if (!phoneRegex.test(phone)) {
        alert("Phone number must have exactly 10 digits");
        event.preventDefault();
        return false;
    }

    // Validate username with a regular expression
    let usernameRegex = /^[a-zA-Z0-9@/./+/-/_]{1,150}$/;
    if (!usernameRegex.test(username)) {
        alert("Invalid username format. It should be 150 characters or fewer, including letters, digits, and @/./+/-/_.");
        event.preventDefault();
        return false;
    }

    if (password1.length < 8){
        alert("Password must be filled out and Password must be at least 8 characters long");
        event.preventDefault();
        return false;
    }

    // Check for similarity to personal information
    if (password1.toLowerCase().includes(name.toLowerCase()) || password1.toLowerCase().includes(username.toLowerCase()) || password1.toLowerCase().includes(email.toLowerCase())) {
        alert("Your password can't be too similar to your other personal information.");
        event.preventDefault();
        return false;
    }

    // Check if the password is a commonly used password (you can customize the list)
    let commonPasswords = ["password", "123456", "qwerty", "abc123"];
    if (commonPasswords.includes(password1.toLowerCase())) {
        alert("Your password can't be a commonly used password.");
        event.preventDefault();
        return false;
    }

    // Check if the password is entirely numeric
    if (/^\d+$/.test(password1)) {
        alert("Your password can't be entirely numeric.");
        event.preventDefault();
        return false;
    }

    // Check if the passwords match
    if (password1 !== password2) {
        alert("Passwords do not match. Please enter the same password as before, for verification.");
        event.preventDefault();
        return false;
    }
    
    return true;

}