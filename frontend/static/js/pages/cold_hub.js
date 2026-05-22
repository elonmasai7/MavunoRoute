document.addEventListener("DOMContentLoaded", async function () {
    let hub = null;
    try {
        hub = await fetchFirstFromList("/api/v1/cold-hubs?page=1&per_page=1");
    } catch {
        hub = null;
    }

    if (!hub || !hub.id) {
        const checkinMessage = document.getElementById("checkin-message");
        const checkoutMessage = document.getElementById("checkout-message");
        if (checkinMessage) {
            checkinMessage.className = "form-message error";
            checkinMessage.textContent = "No cold hub profile is available for this account.";
        }
        if (checkoutMessage) {
            checkoutMessage.className = "form-message error";
            checkoutMessage.textContent = "No cold hub profile is available for this account.";
        }
        return;
    }

    handleFormSubmit("checkin-form", `/api/v1/cold-hubs/${hub.id}/check-in`, function (p) {
        p.quantity_kg = Number(p.quantity_kg);
        return p;
    });

    handleFormSubmit("checkout-form", `/api/v1/cold-hubs/${hub.id}/check-out`, function (p) {
        p.quantity_kg = Number(p.quantity_kg);
        return p;
    });
});
