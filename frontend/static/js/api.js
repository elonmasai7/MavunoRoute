function getToken() {
  return localStorage.getItem("mavuno_access_token") || "";
}

function getRefreshToken() {
  return localStorage.getItem("mavuno_refresh_token") || "";
}

function clearAuth() {
  localStorage.removeItem("mavuno_access_token");
  localStorage.removeItem("mavuno_refresh_token");
}

function normalizeEndpoint(path) {
  if (!path) {
    return "/";
  }
  return path.startsWith("/") ? path : `/${path}`;
}

async function parseResponseBody(response) {
  const contentType = response.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return response.json();
  }
  const text = await response.text();
  return { success: false, message: text || "Unexpected response format", data: null, meta: {} };
}

async function apiRequest(path, method = "GET", body = null, opts = {}) {
  const endpoint = normalizeEndpoint(path);
  const headers = { "Content-Type": "application/json", ...(opts.headers || {}) };
  const token = getToken();

  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const response = await fetch(endpoint, {
    method,
    headers,
    body: body ? JSON.stringify(body) : null,
  });

  const payload = await parseResponseBody(response);
  if (!response.ok || payload.success === false) {
    if (response.status === 401) {
      clearAuth();
      throw new Error("Your session expired. Please log in again.");
    }
    if (response.status === 403) {
      throw new Error("You do not have permission to access this resource.");
    }
    throw new Error(payload.message || "Request failed");
  }

  const data = payload.data ?? [];
  if (opts.includeMeta) {
    return { data, meta: payload.meta || {} };
  }
  return data;
}

function ensureArray(value) {
  if (Array.isArray(value)) {
    return value;
  }
  if (!value) {
    return [];
  }
  return [value];
}

function extractList(data) {
  if (Array.isArray(data)) {
    return data;
  }
  if (Array.isArray(data?.items)) {
    return data.items;
  }
  return [];
}

async function fetchFirstFromList(path) {
  const data = await apiRequest(path);
  const rows = extractList(data);
  return rows.length ? rows[0] : null;
}

function toISO(datetimeLocalValue) {
  if (!datetimeLocalValue) return datetimeLocalValue;
  return new Date(datetimeLocalValue).toISOString();
}

function formatDate(isoString) {
  if (!isoString) return "-";
  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) return "-";
  return date.toLocaleDateString("en-KE", {
    year: "numeric",
    month: "short",
    day: "numeric",
  });
}

function formatDateTime(isoString) {
  if (!isoString) return "-";
  const date = new Date(isoString);
  if (Number.isNaN(date.getTime())) return "-";
  return date.toLocaleString("en-KE", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatCurrency(amount) {
  const numeric = Number(amount);
  if (Number.isNaN(numeric)) {
    return "KES 0.00";
  }
  return `KES ${numeric.toLocaleString("en-KE", {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  })}`;
}

function setStatusText(elementId, message, isError = false) {
  const element = document.getElementById(elementId);
  if (!element) return;
  element.className = isError ? "form-message error" : "form-message";
  element.textContent = message;
}
