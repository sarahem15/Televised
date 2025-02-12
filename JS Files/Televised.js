console.log("Televised.js is loaded!");

// Image array for the series
const seriesImgs = [
    "../images/series/AdventureTimeMain.jpg",
    "../images/series/AgathaAllAlong.jpg",
    "../images/series/ArcaneMain.jpg",
    "../images/series/BlackMirror.jpg",
    "../images/series/BojackHorsemanMain.jpg",
    "../images/series/CommunityMain.jpg",
    "../images/series/CriminalMindsMain.jpg",
    "../images/series/DaughtersOfTheCultMain.jpg",
    "../images/series/DexterMain.jpg",
    "../images/series/EvilLivesHereMain.jpg",
    "../images/series/FriendsMain.jpg",
    "../images/series/FuturamaMain.jpg",
    "../images/series/H2OMain.jpg",
    "../images/series/MissingYouMain.jpg",
    "../images/series/ModernFamilyMain.jpg",
    "../images/series/NewGirlMain.jpg",
    "../images/series/OnlyMurdersInTheBuildingMain.jpg",
    "../images/series/PercyJackson.jpg",
    "../images/series/PlanetEarthMain.jpg",
    "../images/series/Reacher.jpg",
    "../images/series/RipleyMain.jpg",
    "../images/series/SmilingFriendsMain.jpg",
    "../images/series/SprintMain.jpg",
    "../images/series/SquidGameMain.jpg",
    "../images/series/Supacell.jpg",
    "../images/series/SupernaturalMainTitle.jpg",
    "../images/series/That70sShowMain.jpg",
    "../images/series/The100.jpg",
    "../images/series/TheUmbrellaAcademy.jpg",
    "../images/series/WandaVision.jpg",
    "../images/series/Wednesday.jpg",
    "../images/series/WildWildCountryMain.jpg"
];

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
        const items = carousel.querySelectorAll(".item img");
        const shuffledImages = shuffleArray([...imageArray]); // Shuffle a copy of the array
        items.forEach((img, index) => {
            img.src = shuffledImages[index % shuffledImages.length];
            img.alt = `Image ${index + 1}`;
        });
    }
}

// Function to initialize the homepage carousels
function initializeHomeCarousels() {
    // Populate carousels
    populateCarousel("homePopularSection", seriesImgs);
    populateCarousel("homeNewSection", seriesImgs);
}

// Initialize the homepage carousels on DOMContentLoaded
document.addEventListener("DOMContentLoaded", () => {
    initializeHomeCarousels();
});

// Existing navbar and account-related functionality
function updateNavbar() {
    const userSignedIn = localStorage.getItem("userSignedIn") === "true";
    const navbarContainer = document.getElementById("changingNav");

    if (userSignedIn) {
        fetchNavbar("LoggedIn_Header.html", attachLoggedInEvents);
    } else {
        fetchNavbar("LoggedOut_Header.html", attachLoggedOutEvents);
    }
}

function fetchNavbar(navbarFile, callback) {
    fetch(navbarFile)
        .then(response => response.text())
        .then(data => {
            document.getElementById("changingNav").innerHTML = data;
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

    if (username && displayName) {
        displayName.textContent = username;
    }

    if (logoutButton) {
        logoutButton.addEventListener("click", () => {
            window.location.href = "Home.html";
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

// Function to handle account creation
function handleAccountCreation() {
    const usernameInput = document.getElementById("unameCreateInput");
    let username = usernameInput.value.trim();
    const password = document.getElementById("passCreateInput").value.trim();
    const confirmPassword = document.getElementById("passConfirm").value.trim();

    if (!username || !password || !confirmPassword) {
        alert("Please fill in all fields.");
        return;
    }

    // Check if username already exists in localStorage
    const existingUser = userAccountsArray.some(account => account.username === username);
    if (existingUser) {
        alert("Username is already taken. Please choose a different one.");
        usernameInput.value = "";  // Clear input field for new entry
        usernameInput.focus();  // Refocus on the username input field
        return;
    }

    if (password !== confirmPassword) {
        alert("Passwords do not match!");
        return;
    }

    // Password validation: At least 12 characters, 1 uppercase, 1 number, 1 special character
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).{12,}$/;
    if (!passwordRegex.test(password)) {
        alert("Password must be at least 12 characters long and contain at least one capital letter, one number, and one special character.");
        return;
    }

    // Add new user account
    const userAccountInfo = { username: username, password: password };
    userAccountsArray.push(userAccountInfo);
    localStorage.setItem("userAccountsArray", JSON.stringify(userAccountsArray));

    // Set user as signed in
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
        createBtn.addEventListener("click", handleAccountCreation);
    }
}

function bindSignInButton() {
    const signInBtn = document.getElementById("signInBtn");
    if (signInBtn) {
        signInBtn.addEventListener("click", handleSigningIn);
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
//Autofill user information
function autofillProfileSettings() {
    const usernameInput = document.getElementById("userName");
    const displayNameInput = document.getElementById("displayName");
    const bioInput = document.getElementById("bio");
    const pronounsSelect = document.getElementById("pronouns");
    const repliesSelect = document.getElementById("replies");

    const username = localStorage.getItem("username");
    if (!username) return;

    usernameInput.value = username;

    let userAccounts = JSON.parse(localStorage.getItem("userAccountsArray") || "[]");
    let user = userAccounts.find(acc => acc.username === username);

    if (user) {
        displayNameInput.value = user.displayName || "";
        bioInput.value = user.bio || "";
        pronounsSelect.value = user.pronouns || "Prefer Not to Answer";
        repliesSelect.value = user.replies || "Public";
    }
}

// Profile Settings - Save changes
document.getElementById("saveProfile")?.addEventListener("click", function (event) {
    event.preventDefault();

    const username = localStorage.getItem("username");
    if (!username) {
        alert("User not found. Please sign in again.");
        return;
    }

    const displayName = document.getElementById("displayName").value;
    const bio = document.getElementById("bio").value.trim();
    const pronouns = document.getElementById("pronouns").value;
    const replies = document.getElementById("replies").value;

    let userAccounts = JSON.parse(localStorage.getItem("userAccountsArray") || "[]");
    let userIndex = userAccounts.findIndex(acc => acc.username === username);

    if (userIndex !== -1) {
        userAccounts[userIndex].displayName = displayName;
        userAccounts[userIndex].bio = bio;
        userAccounts[userIndex].pronouns = pronouns;
        userAccounts[userIndex].replies = replies;

        localStorage.setItem("userAccountsArray", JSON.stringify(userAccounts));
        alert("Profile updated successfully!");
    } else {
        alert("User account not found.");
    }
});

document.addEventListener("DOMContentLoaded", () => {
    // Check if we're on the Profile Settings page and autofill the fields
    if (document.body.id === "profileSettings") {
        autofillProfileSettings();
    }

    updateNavbar();
    updateWelcomeMessage();
});

/* Row/Slideshow Functionality */
let rowIndex = 1;
showNextSlide(rowIndex);

// Next/previous controls
function plusSlides(n) {
    showNextSlide(rowIndex += n);
}

function currentRow(n) {
    showNextSlide(rowIndex = n);
}

function showNextSlide(n) {
    let i;
    let slides = document.getElementsByClassName("row");
    if (n > slides.length) {
        rowIndex = 1;
    }
    if (n < 1) {
        rowIndex = slides.length;
    }
    for (i = 0; i < slides.length; i++) {
        slides[i].style.display = "none";
    }
    slides[rowIndex - 1].style.display = "block";
}
