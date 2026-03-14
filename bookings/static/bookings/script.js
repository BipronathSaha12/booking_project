// bookings/static/bookings/script.js

// Stripe loading screen
function startPayment() {
    const loader = document.getElementById("payment-loader");
    if (loader) {
        loader.style.display = "flex";
    }
}

// booking progress step animation (safe)
document.addEventListener("DOMContentLoaded", function () {
    const steps = document.querySelectorAll(".step");
    if (steps.length > 0) {
        steps.forEach((step) => {
            step.addEventListener("click", function () {
                steps.forEach((s) => s.classList.remove("active"));
                step.classList.add("active");
            });
        });
    }

    // simple card hover effect (safe)
    const cards = document.querySelectorAll(".service-card");
    if (cards.length > 0) {
        cards.forEach((card) => {
            card.addEventListener("mouseenter", () => {
                card.style.transform = "translateY(-10px)";
                card.style.transition = "transform 0.3s ease";
            });
            card.addEventListener("mouseleave", () => {
                card.style.transform = "translateY(0px)";
            });
        });
    }
});

// animated success page redirect (safe)
function redirectDashboard() {
    const dashboard = document.querySelector("body");
    if (dashboard) {
        setTimeout(function () {
            window.location.href = "/dashboard/";
        }, 3000);
    }
}