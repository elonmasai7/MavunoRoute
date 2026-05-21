document.addEventListener("DOMContentLoaded", function () {
    handleFormSubmit("farmer-form", "/api/v1/farmers", function (p) {
        return p;
    });
});
