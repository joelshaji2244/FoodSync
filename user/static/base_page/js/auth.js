document.addEventListener('DOMContentLoaded', function() {
    // Get the button element by its ID
    var signInButton = document.getElementById("signInButton");

    // Check if the button element exists and the user is authenticated
    if (signInButton && isAuthenticated) {
        // Set the button's style to hide it
        signInButton.style.display = "none";
    }
});