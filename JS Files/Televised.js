console.log("Televised.js is loaded!");

// Image array for the series
const seriesImgs = [
    "ADiscoveryOfWitches.jpg",
    "AdventureTime.jpg",
    "AgathaAllAlong.jpg",
    "AmericanHorrorStory.jpg",
    "Arcane.jpg",
    "BelowDeck.jpg",
    "BlackMirror.jpg",
    "BojackHorseman.jpg",
    "BreakingBad.jpg",
    "Bridgerton.jpg",
    "Chernobyl.jpg",
    "ClarksonsFarm.jpg",
    "Community.jpg",
    "ConversationsWithFriends.jpg",
    "CriminalMinds.jpg",
    "DaughtersOfTheCult.jpg",
    "Dexter.jpg",
    "DoctorWho.jpg",
    "EveryWitchWay.jpg",
    "EvilLivesHere.jpg",
    "Friends.jpg",
    "Futurama.jpg",
    "GameOfThrones.jpg",
    "GossipGirl.jpg",
    "H2O.jpg",
    "JupitersLegacy.jpg",
    "LessonsInChemistry.jpg",
    "MissingYou.jpg",
    "ModernFamily.jpg",
    "NewGirl.jpg",
    "NormalPeople.jpg",
    "OnlyMurdersInTheBuilding.jpg",
    "Outlander.jpg",
    "PercyJackson.jpg",
    "PlanetEarth.jpg",
    "PrettyLittleLiars.jpg",
    "Reacher.jpg",
    "Ripley.jpg",
    "RuPaulsDragRace.jpg",
    "SharpObjects.jpg",
    "SmilingFriends.jpg",
    "Sprint.jpg",
    "SquidGame.jpg",
    "StarTrek.jpg",
    "StrangerThings.jpg",
    "Supacell.jpg",
    "SupermanAndLois.jpg",
    "Supernatural.jpg",
    "That70sShow.jpg",
    "The100.jpg",
    "TheBabySittersClub.jpg",
    "TheBachelor.jpg",
    "TheEndOfTheFWorld.jpg",
    "TheFallOfTheHouseOfUsher.jpg",
    "TheFlash.jpg",
    "TheGreat.jpg",
    "TheHauntingOfHillHouse.jpg",
    "TheHauntingOfBlyManor.jpg",
    "TheLastOfUs.jpg",
    "TheMandalorian.jpg",
    "TheManInTheHighCastle.jpg",
    "TheSandman.jpg",
    "TheSecretLivesOfMormonWives.jpg",
    "TheSummerITurnedPretty.jpg",
    "TheTudors.jpg",
    "TheUmbrellaAcademy.jpg",
    "TheWitcher.jpg",
    "Travelers.jpg",
    "WandaVision.jpg",
    "Wednesday.jpg",
    "WildWildCountry.jpg",
    "WizardsOfWaverlyPlace.jpg",
    "XOKitty.jpg",
    "You.jpg"
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
    populateCarousel("homePopular", seriesImgs);
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

    // Regular expression to check if the password contains:
    // 1. At least one uppercase letter
    // 2. At least one number
    // 3. At least one special character
    const passwordRegex = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*(),.?":{}|<>]).+$/;

    if (!passwordRegex.test(password)) {
        alert("Password must contain at least one capital letter, one number, and one symbol.");
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

    const username = localStorage.getItem("username");

    if (username) {  // Ensure username exists in localStorage
        usernameInput.placeholder = username;  // Set the username as the placeholder text
        displayNameInput.placeholder = username;  // Set the username as the placeholder text for display name
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
    slides[rowIndex - 1].style.display = "in-line block";
}
