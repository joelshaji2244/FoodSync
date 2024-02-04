function validateForm(event){


    let name = document.forms["rest_registration"]["name"].value;

    let email = document.forms["rest_registration"]["email"].value;
    // Validate email format using a regular expression
    let emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    let phone = document.forms["rest_registration"]["phone"].value;
    // Check if the phone number has exactly 10 digits
    let phoneRegex = /^\d{10}$/;

    let image = document.forms["rest_registration"]["image"].value;

    let licenceno = document.forms["rest_registration"]["licence_number"].value;
    // Check if the licence number has exactly 14 digits
    let licenceRegex = /^\d{14}$/;

    username = document.forms["rest_registration"]["username"].value;
    // Validate username with a regular expression
    let usernameRegex = /^[a-zA-Z0-9@/./+/-/_]{1,150}$/;

    let password1 = document.forms["rest_registration"]["password1"].value;
    let password2 = document.forms["rest_registration"]["password2"].value;


    if (!emailRegex.test(email)) {
        alert("Invalid email format");
        // Prevent form submission
        if (event.preventDefault) {
            event.preventDefault();
        } else {
            event.returnValue = false; // For IE compatibility
        }
        
        return false;
    }
    if (!phoneRegex.test(phone)) {
        alert("Phone number must have exactly 10 digits");
        // Prevent form submission
        if (event.preventDefault) {
            event.preventDefault();
        } else {
            event.returnValue = false; // For IE compatibility
        }
        
        return false;
    }
    if (image) {
        let allowedExtensions = /(\.jpg|\.jpeg|\.png)$/i;
        let maxFileSizeMB = 5; // Maximum allowed file size in megabytes

        if (!allowedExtensions.test(image)) {
            alert("Invalid image file type. Please upload a JPEG or PNG file.");
            // Prevent form submission
            if (event.preventDefault) {
                event.preventDefault();
            } else {
                event.returnValue = false; // For IE compatibility
            }

            return false;
        }

        let fileSizeMB = (document.getElementById("image").files[0].size / (1024 * 1024)).toFixed(2);
        if (fileSizeMB > maxFileSizeMB) {
            alert("Image file size exceeds the maximum allowed size (5MB).");
            // Prevent form submission
            if (event.preventDefault) {
                event.preventDefault();
            } else {
                event.returnValue = false; // For IE compatibility
            }

            return false;
            
        }
    }
    if (!licenceRegex.test(licenceno)) {
        alert("Licence number must have exactly 14 digits");
        // Prevent form submission
        if (event.preventDefault) {
            event.preventDefault();
        } else {
            event.returnValue = false; // For IE compatibility
        }
        
        return false;
    }
    if (!usernameRegex.test(username)) {
        alert("Invalid username format. It should be 150 characters or fewer, including letters, digits, and @/./+/-/_.");
        // Prevent form submission
        if (event.preventDefault) {
            event.preventDefault();
        } else {
            event.returnValue = false; // For IE compatibility
        }
        
        return false;
    }
    if (password1.length < 8){
        alert("Password must be filled out and Password must be at least 8 characters long");
        // Prevent form submission
        if (event.preventDefault) {
            event.preventDefault();
        } else {
            event.returnValue = false; // For IE compatibility
        }
        
        return false;
    }

    // Check for similarity to personal information
    if (password1.toLowerCase().includes(name.toLowerCase()) || password1.toLowerCase().includes(username.toLowerCase()) || password1.toLowerCase().includes(email.toLowerCase())) {
        alert("Your password can't be too similar to your other personal information.");
        // Prevent form submission
        if (event.preventDefault) {
            event.preventDefault();
        } else {
            event.returnValue = false; // For IE compatibility
        }
        
        return false;
    }

    // Check if the password is a commonly used password (you can customize the list)
    let commonPasswords = ["password", "123456", "qwerty", "abc123"];
    if (commonPasswords.includes(password1.toLowerCase())) {
        alert("Your password can't be a commonly used password.");
        // Prevent form submission
        if (event.preventDefault) {
            event.preventDefault();
        } else {
            event.returnValue = false; // For IE compatibility
        }
        
        return false;
    }

    // Check if the password is entirely numeric
    if (/^\d+$/.test(password1)) {
        alert("Your password can't be entirely numeric.");
        // Prevent form submission
        if (event.preventDefault) {
            event.preventDefault();
        } else {
            event.returnValue = false; // For IE compatibility
        }
        
        return false;
    }

    // Check if the passwords match
    if (password1 !== password2) {
        alert("Passwords do not match. Please enter the same password as before, for verification.");
        // Prevent form submission
        if (event.preventDefault) {
            event.preventDefault();
        } else {
            event.returnValue = false; // For IE compatibility
        }
        
        return false;
    }
    
    return true;    
    
}


// function userNamehelpText(){
//     htmlData=`
//     Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.
//     `
//     document.querySelector("#username_helptext").innerHTML = htmlData
// }

// function password1HelpText(){
//     htmlData = `
//     <ul>
//         <li>Your password can't be too similar to your other personal information.</li>
//         <li>Your password must contain at least 8 characters.</li>
//         <li>Your password can't be a commonly used password.</li>
//         <li>Your password can't be entirely numeric.</li>
//     </ul>
//     `
//     document.querySelector("#password1_helptext").innerHTML = htmlData
// }

// function password2HelpText(){
//     htmlData = `
//     Enter the same password as before, for verification.
//     `
//     document.querySelector("#password2_helptext").innerHTML = htmlData
// }

