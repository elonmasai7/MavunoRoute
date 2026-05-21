document.addEventListener("DOMContentLoaded", function () {
    var toggle = document.querySelector(".mobile-menu-toggle");
    if (toggle) {
        toggle.addEventListener("click", function () {
            var nav = document.querySelector(".nav-links");
            if (nav) nav.style.display = nav.style.display === "flex" ? "none" : "flex";
        });
    }
});
