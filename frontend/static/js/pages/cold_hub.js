document.addEventListener("DOMContentLoaded", function () {
    handleFormSubmit("checkin-form", "/api/v1/cold-hubs/check-in", function (p) {
        return p;
    });
    handleFormSubmit("checkout-form", "/api/v1/cold-hubs/check-out", function (p) {
        return p;
    });
});
