function getToken() {
    return localStorage.getItem("mavuno_access_token") || "";
}

async function apiRequest(path, method = "GET", body = null) {
    const headers = { "Content-Type": "application/json" };
    const token = getToken();
    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }
    const response = await fetch(path, {
        method,
        headers,
        body: body ? JSON.stringify(body) : null,
    });
    const payload = await response.json();
    if (!response.ok || payload.success === false) {
        throw new Error(payload.message || "Request failed");
    }
    return payload.data;
}

function toISO(datetimeLocalValue) {
    if (!datetimeLocalValue) return datetimeLocalValue;
    return new Date(datetimeLocalValue).toISOString();
}

function formatDate(isoString) {
    if (!isoString) return "-";
    return new Date(isoString).toLocaleDateString("en-KE", {
        year: "numeric", month: "short", day: "numeric",
    });
}

function formatDateTime(isoString) {
    if (!isoString) return "-";
    return new Date(isoString).toLocaleString("en-KE", {
        year: "numeric", month: "short", day: "numeric",
        hour: "2-digit", minute: "2-digit",
    });
}

function formatCurrency(amount) {
    return "KES " + Number(amount).toLocaleString("en-KE", {
        minimumFractionDigits: 2, maximumFractionDigits: 2,
    });
}
