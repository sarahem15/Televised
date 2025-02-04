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
    if (createAccountBtn) {
        createAccountBtn.addEventListener("click", () => {
            showCreateAccountModal();
            bindCreateAccountButton();
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
    const signIntModalEl = document.getElementById("SignIn");
    const signInModal = bootstrap.Modal.getOrCreateInstance(signIntModalEl);
    signInModal.show();
}

// Updated function to handle account creation
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
        createBtn.addEventListener("click", handleAccountCreation);
    }
}

function bindSignInButton() {
    const signInBtn = document.getElementById("signInBtn");
    if (signInBtn) {
        signInBtn.addEventListener("click", handleSigningIn);
    }
}

function autofillProfileSettings() {
    const usernameInput = document.getElementById("userName");
    const displayNameInput = document.getElementById("displayName");

    const username = localStorage.getItem("username");

    if (username) {
        if (usernameInput) usernameInput.value = username;
        if (displayNameInput) displayNameInput.value = username;
    }

    // Set the text color to off-white for the inputs
    const inputs = [usernameInput, displayNameInput, document.getElementById("bio"), document.getElementById("pronouns"), document.getElementById("replies")];
    inputs.forEach(input => {
        if (input) {
            input.style.color = "#D8D8D8"; // Off-white text color
        }
    });
}


document.addEventListener("DOMContentLoaded", () => {
    updateNavbar();
    updateWelcomeMessage();

    if (document.body.id === "profileSettings") {
        autofillProfileSettings();
    }
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