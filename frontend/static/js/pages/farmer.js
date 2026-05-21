document.addEventListener("DOMContentLoaded", function () {
    handleFormSubmit("harvest-form", "/api/v1/harvest-batches", function (p) {
        p.quantity_kg = Number(p.quantity_kg);
        p.asking_price_per_kg = Number(p.asking_price_per_kg);
        p.latitude = Number(p.latitude);
        p.longitude = Number(p.longitude);
        p.expected_harvest_datetime = toISO(p.expected_harvest_datetime);
        return p;
    });
});
