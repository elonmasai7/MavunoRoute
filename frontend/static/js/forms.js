function handleFormSubmit(formId, endpoint, transformPayload, onSuccess, onError) {
    const form = document.getElementById(formId);
    if (!form) return;
    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const message = form.querySelector(".form-message");
        const submitBtn = form.querySelector("[type=submit]");
        const formData = new FormData(form);
        let payload = Object.fromEntries(formData.entries());
        if (transformPayload) {
            payload = transformPayload(payload);
        }
        if (message) message.textContent = "Processing...";
        if (submitBtn) submitBtn.disabled = true;
        try {
            const data = await apiRequest(endpoint, "POST", payload);
            if (message) {
                message.className = "form-message success";
                message.textContent = "Success!";
            }
            if (onSuccess) onSuccess(data, form);
        } catch (err) {
            if (message) {
                message.className = "form-message error";
                message.textContent = err.message;
            }
            if (onError) onError(err, form);
        } finally {
            if (submitBtn) submitBtn.disabled = false;
        }
    });
}
