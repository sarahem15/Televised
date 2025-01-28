console.log("Televised.js is loaded!");

// Function to update the navbar based on login state
function updateNavbar() {
    const userSignedIn = localStorage.getItem("userSignedIn") === "true";
    const navbarContainer = document.getElementById("changingNav");

    if (userSignedIn) {
        fetchNavbar("LoggedIn_Header.html", attachLoggedInEvents);
    } else {
        fetchNavbar("LoggedOut_Header.html", attachLoggedOutEvents);
    }
}

// Function to fetch and replace the navbar content
function fetchNavbar(navbarFile, callback) {
    fetch(navbarFile)
        .then(response => response.text())
        .then(data => {
            document.getElementById("changingNav").innerHTML = data;
            if (callback) callback(); // Attach events after loading navbar
        })
        .catch(error => console.error("Error loading navbar:", error));
}

// Function to attach events specific to the logged-out navbar
function attachLoggedOutEvents() {
    const createAccountBtn = document.getElementById("createAcc");
    if (createAccountBtn) {
        createAccountBtn.addEventListener("click", () => {
            showCreateAccountModal();
            bindCreateAccountButton(); // Re-bind the modal's Create Account button
        });
    }
}

// Function to attach events specific to the logged-in navbar
function attachLoggedInEvents() {
    const username = localStorage.getItem("username");
    const displayName = document.getElementById("displayName");
    const logoutButton = document.querySelector(".dropdown-item[href='#']");

    if (username && displayName) {
        displayName.textContent = username; // Display the username
    }

    if (logoutButton) {
        logoutButton.addEventListener("click", () => {
            localStorage.removeItem("username");
            localStorage.setItem("userSignedIn", "false");
            updateNavbar(); // Refresh navbar to logged-out state
        });
    }
}

// Function to display the "Create Account" modal
function showCreateAccountModal() {
    const createAccountModalEl = document.getElementById("CreateAccount");
    const createAccountModal = bootstrap.Modal.getOrCreateInstance(createAccountModalEl);
    createAccountModal.show();
}

// Function to handle the account creation process
function handleAccountCreation() {
    const username = document.getElementById("unameCreateInput").value.trim();
    const password = document.getElementById("passCreateInput").value.trim();
    const confirmPassword = document.getElementById("passConfirm").value.trim();

    if (!username || !password || !confirmPassword) {
        alert("Please fill in all fields.");
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    // Save user details in localStorage (for simplicity)
    localStorage.setItem("userSignedIn", "true");
    localStorage.setItem("username", username);

    // Hide the modal
    const createAccountModalEl = document.getElementById("CreateAccount");
    const createAccountModal = bootstrap.Modal.getOrCreateInstance(createAccountModalEl);
    createAccountModal.hide();

    // Refresh the navbar to show the logged-in state
    updateNavbar();
}

// Function to bind event listener to the Create Account button
function bindCreateAccountButton() {
    const createBtn = document.getElementById("createBtn");
    if (createBtn) {
        createBtn.addEventListener("click", handleAccountCreation);
    }
}

// Autofill profile settings
function autofillProfileSettings() {
    const usernameInput = document.getElementById("userName");
    const displayNameInput = document.getElementById("displayName");

    const username = localStorage.getItem("username");

    if (username) {
        if (usernameInput) usernameInput.value = username;
        if (displayNameInput) displayNameInput.value = username;
    }
}

// Event listener to initialize the navbar, account creation logic, and autofill profile settings
document.addEventListener("DOMContentLoaded", () => {
    updateNavbar(); // Initialize the navbar on page load

    // Autofill profile settings if on the Profile Settings page
    if (document.body.id === "profileSettings") {
        autofillProfileSettings();
    }
});
