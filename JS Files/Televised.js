console.log("Televised.js is loaded!");


// Initialize the array to store user account info
let userAccountsArray = JSON.parse(localStorage.getItem("userAccountsArray") || "[]");

// Shuffle function to randomize the array
function shuffleArray(array) {
    return array.sort(() => Math.random() - 0.5);
}

// Function to populate specific carousels
function populateCarousel(carouselId, imageArray) {
    const carousel = document.getElementById(carouselId);
    if (carousel) {
        const itemx = carousel.querySelectorAll(".item input");
        const shuffledImages = shuffleArray([...imageArray]); // Shuffle a copy of the array
        itemx.forEach((input, index) => {
            input.src = shuffledImages[index % shuffledImages.length];
            input.alt = `Image ${index + 1}`;
            input.value = shuffledImages[(index - 1) % shuffledImages.length];  
        });
    }
}

// Initialize the homepage carousels on DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
    initializeHomeCarousels();
});

// Existing navbar and account-related functionality
function updateNavbar() {
    const userSignedIn = localStorage.getItem("userSignedIn") === "true";
    const navbarContainer = document.getElementById("changingNav");

    console.log(userSignedIn);
    if (userSignedIn) {
      //        fetchNavbar("LoggedIn_Header.html", attachLoggedInEvents);
      fetch("LoggedIn_Header.html")
        .then(response => response.text())
        .then(data => {
        document.getElementById("changingNav").innerHTML = data;
        //loadData(data, '#changingNav');
            attachLoggedInEvents();
              })
        .catch(error => console.error("Error loading navbar:", error));

    } else {
        fetchNavbar("LoggedOut_Header.cgi", attachLoggedOutEvents);
    console.log("Why!!!!!!!!! to save the day")
    }
}

function fetchNavbar(navbarFile, callback) {
    fetch(navbarFile)
        .then(response => response.text())
        .then(data => {
            //document.getElementById("changingNav").innerHTML = data;
            loadData(data, '#changingNav')
            if (callback) callback();
        })
        .catch(error => console.error("Error loading navbar:", error));
}

function attachLoggedOutEvents() {
    const createAccountBtn = document.getElementById("createAcc");
    const signInBtn = document.getElementById("SignIn");
    if (createAccountBtn) {
        createAccountBtn.addEventListener("click", () => {
            showCreateAccountModal();
            bindCreateAccountButton();
        });
    }
    if (signInBtn) {
        signInBtn.addEventListener("click", () => {
            showSignInModal();
            bindSignInButton();
        });
    }
}

function attachLoggedInEvents() {
    const username = localStorage.getItem("username");
    const displayName = document.getElementById("displayName");
    const logoutButton = document.querySelector(".dropdown-item[href='#']");
    //const displayNameS = document.getElementById("displayNameS");

    console.log("****> " + displayName); 
    console.log("****> " + username);

    if (username && displayName) {
        displayName.textContent = username;
    }

    if (logoutButton) {
        logoutButton.addEventListener("click", () => {
            window.location.href = "Home.cgi";
            localStorage.removeItem("username");
            localStorage.setItem("userSignedIn", "false");
            updateNavbar();
            updateWelcomeMessage();
        });
    }
}

function updateWelcomeMessage() {
    const userSignedIn = localStorage.getItem("userSignedIn") === "true";
    const welcomeMessage = document.getElementById("chaningWelcome");

    if (userSignedIn) {
        const username = localStorage.getItem("username") || "User";
        welcomeMessage.textContent = `Welcome back, ${username}!`;
    } else {
        welcomeMessage.textContent = "Welcome to Televised!";
    }
}

function showCreateAccountModal() {
    const createAccountModalEl = document.getElementById("CreateAccount");
    const createAccountModal = bootstrap.Modal.getOrCreateInstance(createAccountModalEl);
    createAccountModal.show();
}

function showSignInModal() {
    const signInModalEl = document.getElementById("signIn");
    const signInModal = bootstrap.Modal.getOrCreateInstance(signInModalEl);
    signInModal.show();
}

function validateAccountCreation() {
  const username = document.getElementById("unameCreateInput").value.trim();
  const password = document.getElementById("passCreateInput").value.trim();
  const confirmPassword = document.getElementById("passConfirm").value.trim();

  console.log("Yeppers");
  if (!username || !password || !confirmPassword) {
    alert("Please fill in all fields.");
    return false;
  }
  
  if (password !== confirmPassword) {
    alert("Passwords do not match!");
    return false;
  }

  const atSymbol = "@";
    if (!(username.includes(atSymbol))) {
        alert("Username must be a valid email address.");
        return false;
    }

  // Password validation: At least 12 characters, 1 uppercase, 1 number, 1 special character
  const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{12,}$/;
  if (!passwordRegex.test(password)) {
      alert("Password must be at least 12 characters long and contain at least one capital letter, one number, and one special character.");
      return false;
  }

  localStorage.setItem("FalseFlag", "false");
  return true;
}

// Updated function to handle account creation
function handleAccountCreation() {
    const username = document.getElementById("unameCreateInput").value.trim();
    const password = document.getElementById("passCreateInput").value.trim();
    const confirmPassword = document.getElementById("passConfirm").value.trim();

    // REMEMBER TO ADD BACK
    // Password validation: At least 12 characters, 1 uppercase, 1 number, 1 special character
    //const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{12,}$/;
    //if (!passwordRegex.test(password)) {
    //    alert("Password must be at least 12 characters long and contain at least one capital letter, one number, and one special character.");
    //    return;
    //}


    // Define the user account info object
    const userAccountInfo = { username: username, password: password };

    // Add the new user account to the userAccountsArray
    userAccountsArray.push(userAccountInfo);

    // Store the updated array in localStorage
    localStorage.setItem("userAccountsArray", JSON.stringify(userAccountsArray));

    // Set the user as signed in
    localStorage.setItem("userSignedIn", "true");
    localStorage.setItem("username", username);

    alert("Account created successfully!");

    // Hide the create account modal
    const createAccountModalEl = document.getElementById("CreateAccount");
    const createAccountModal = bootstrap.Modal.getOrCreateInstance(createAccountModalEl);
    createAccountModal.hide();

    // Update navbar and welcome message
    updateNavbar();
    updateWelcomeMessage();
}

// Bind buttons for account creation and sign-in
function bindCreateAccountButton() {
    const createBtn = document.getElementById("createBtn");
    if (createBtn) {
        //createBtn.addEventListener("click", handleAccountCreation);
    }
}

function bindSignInButton() {
    const signInBtn = document.getElementById("signInBtn");
    if (signInBtn) {
        //signInBtn.addEventListener("click", handleSigningIn);
    }
}

// Handle sign-in
function handleSigningIn() {
    const username = document.getElementById("unameSignInInput").value.trim();
    const password = document.getElementById("passSignInInput").value.trim();

    if (!username || !password) {
        alert("Please fill in all fields.");
        return;
    }

    const storedUserAccounts = JSON.parse(localStorage.getItem("userAccountsArray") || "[]");

    // Check if the entered credentials match any stored account
    const userAccount = storedUserAccounts.find(account => account.username === username && account.password === password);

    if (userAccount) {
        // If credentials match, set the user as signed in
        localStorage.setItem("userSignedIn", "true");
        localStorage.setItem("username", username);

        alert("Signed in successfully!");

        // Hide the sign-in modal
        const signInModalEl = document.getElementById("signIn");
        const signInModal = bootstrap.Modal.getOrCreateInstance(signInModalEl);
        signInModal.hide();

        // Update navbar and welcome message
        updateNavbar();
        updateWelcomeMessage();
    } else {
        alert("Invalid username or password!");
    }
}

// Autofill profile settings
function autofillProfileSettings() {
    const usernameInput = document.getElementById("userName");
    const displayNameInput = document.getElementById("displayName");
    //const userInput = document.getElementsById("userName");

    const username = localStorage.getItem("username");

    if (username) {  // Ensure username exists in localStorage
        usernameInput.placeholder = username;  // Set the username as the placeholder text
        displayNameInput.placeholder = username;  // Set the username as the placeholder text for display name
        //userInput = username;
    } else {
        console.log("No username found in localStorage.");
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // Check if we're on the Profile Settings page and autofill the fields
    if (document.body.id === "profileSettings") {
        autofillProfileSettings();
    }

    updateNavbar();
    updateWelcomeMessage();
});

// change eye icon color
document.addEventListener("DOMContentLoaded", function() {
    document.querySelectorAll(".watchedButton").forEach(button => {
        let icon = button.querySelector(".eye-icon");
        icon.style.fontSize = "35px";
        icon.style.color = "white";

        button.addEventListener("click", function () {
            if(icon.style.color == "white"){
                icon.style.color = "#6bdf10";
            } else{
                icon.style.color = "white"
            }
        });
    });
});
