document.addEventListener("DOMContentLoaded", function () {
    handleFormSubmit("demand-form", "/api/v1/buyer-demands", function (p) {
        p.quantity_kg = Number(p.quantity_kg);
        p.max_price_per_kg = Number(p.max_price_per_kg);
        p.delivery_latitude = Number(p.delivery_latitude);
        p.delivery_longitude = Number(p.delivery_longitude);
        p.required_delivery_datetime = toISO(p.required_delivery_datetime);
        return p;
    });
});
