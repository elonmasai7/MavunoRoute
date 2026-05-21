document.addEventListener("DOMContentLoaded", function () {
    handleFormSubmit("vehicle-form", "/api/v1/vehicles", function (p) {
        p.capacity_kg = Number(p.capacity_kg);
        return p;
    });
});
