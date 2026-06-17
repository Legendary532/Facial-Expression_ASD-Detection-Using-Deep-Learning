const circles = document.querySelectorAll('.circle');
circles.forEach(elem => {
    const dots = parseInt(elem.getAttribute("data-dots"));
    const marked = parseInt(elem.getAttribute("data-percent"));
    const percent = Math.floor(dots * marked / 100);
    let points = "";
    const rotate = 360 / dots;

    // Create the points as div elements
    for (let i = 0; i < dots; i++) {
        points += `<div class="points" style="--i:${i}; --root:${rotate}deg"></div>`;
    }
    elem.innerHTML = points;

    const pointsMarked = elem.querySelectorAll('.points');

    // Mark the specified percentage of points
    for (let i = 0; i < percent; i++) {
        pointsMarked[i].classList.add('marked');
    }
});

// Active menu on scroll
const menuLi = document.querySelectorAll('header ul li a');
const section = document.querySelectorAll('section');
function activeMenu() {
    let len = section.length;
    while (--len && window.scrollY + 97 < section[len].offsetTop) { }
    menuLi.forEach(sec => sec.classList.remove("active"));
    menuLi[len].classList.add("active");
};
activeMenu();
window.addEventListener("scroll", activeMenu);

// Sticky header on scroll
const header = document.querySelector("header");
window.addEventListener("scroll", () => {
    header.classList.toggle("sticky", window.scrollY > 50);
});

// Menu Icon Toggle
const menuIcon = document.querySelector("#menu-icon");
const navlist = document.querySelector(".navlist");

menuIcon.onclick = () => {
    menuIcon.classList.toggle("bx-x"); // icon toggle
    navlist.classList.toggle("open");  // menu toggle
};

window.addEventListener("scroll", () => {
    navlist.classList.remove("open");
    menuIcon.classList.remove("bx-x");
});

// Intersection observer to reveal elements on scroll
const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
            entry.target.classList.add("show-items");
        } else {
            entry.target.classList.remove("show-items");
        }
    });
});

// Observe scroll-based animations
const scrollScale = document.querySelectorAll(".scroll-scale");
scrollScale.forEach((el) => observer.observe(el));

const scrollBottom = document.querySelectorAll(".scroll-bottom");
scrollBottom.forEach((el) => observer.observe(el));

const scrollTop = document.querySelectorAll(".scroll-top");
scrollTop.forEach((el) => observer.observe(el));

function validation() {
    const name = document.getElementById("name").value;
    const namePattern = /^[a-zA-Z\s]+$/;
    if (!namePattern.test(name)) {
        alert("Please enter a valid name (only alphabets allowed).");
        return false;
    }
    const email = document.getElementById("email").value;
    const emailPattern = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/;
    if (!emailPattern.test(email)) {
        alert("Please enter a valid email address.");
        return false;
    }
    const address = document.getElementById("address").value;
    const addressPattern = /^[a-zA-Z0-9\s-]+$/;
    if (!addressPattern.test(address)) {
        alert("Please enter a valid address (e.g., street 23-village).");
        return false;
    }
    const phone = document.getElementById("phone").value;
    const phonePattern = /^[0-9]{11}$/;
    if (!phonePattern.test(phone)) {
        alert("Please enter a valid phone number (11 digits).");
        return false;
    }
    const message = document.getElementById("message").value;
    const messagePattern = /^[a-zA-Z\s]+$/;
    if (!messagePattern.test(message)) {
        alert("Please enter a valid message (only alphabets and spaces allowed).");
        return false;
    }
    sendEmail(name, email, address, phone, message);
    return true;
}
function sendEmail(name, email, address, phone, message) {
    const subject = "New Message from Contact Form";
    const body = `Name: ${name}\nEmail: ${email}\nAddress: ${address}\nPhone: ${phone}\nMessage: ${message}`;
    const mailtoLink = `mailto:youremail@example.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
    window.location.href = mailtoLink;
    alert("Your message has been sent!");
}

function detect() {

    let valid = true

    const file = document.getElementById("file").files[0]

    document.getElementById("imageError").innerText = ""

    if(!file){
        document.getElementById("imageError").innerText="Upload image"
        valid=false
    }

    return valid
}