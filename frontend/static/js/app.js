const token = localStorage.getItem("mavuno_access_token");

async function apiRequest(path, method = "GET", body = null) {
  const headers = { "Content-Type": "application/json" };
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

const dashboardBtn = document.getElementById("refresh-dashboard");
if (dashboardBtn) {
  dashboardBtn.addEventListener("click", async () => {
    const status = document.getElementById("dashboard-status");
    const table = document.getElementById("dashboard-table");
    const tbody = table.querySelector("tbody");
    status.textContent = "Loading metrics...";
    tbody.innerHTML = "";
    try {
      const data = await apiRequest("/api/v1/reports/dashboard");
      Object.entries(data).forEach(([key, value]) => {
        const row = document.createElement("tr");
        row.innerHTML = `<th style="text-align:left;padding:0.5rem 0.75rem;">${key}</th><td style="padding:0.5rem 0.75rem;">${value}</td>`;
        tbody.appendChild(row);
      });
      table.hidden = false;
      status.textContent = "Metrics loaded.";
    } catch (err) {
      status.textContent = err.message;
      table.hidden = true;
    }
  });
}

const harvestForm = document.getElementById("harvest-form");
if (harvestForm) {
  harvestForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = document.getElementById("harvest-message");
    const formData = new FormData(harvestForm);
    const payload = Object.fromEntries(formData.entries());
    payload.quantity_kg = Number(payload.quantity_kg);
    payload.asking_price_per_kg = Number(payload.asking_price_per_kg);
    payload.latitude = Number(payload.latitude);
    payload.longitude = Number(payload.longitude);
    payload.expected_harvest_datetime = toISO(payload.expected_harvest_datetime);
    message.textContent = "Creating harvest batch...";
    try {
      const data = await apiRequest("/api/v1/harvest-batches", "POST", payload);
      message.textContent = `Harvest created: ${data.id}`;
    } catch (err) {
      message.textContent = err.message;
    }
  });
}

const demandForm = document.getElementById("demand-form");
if (demandForm) {
  demandForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = document.getElementById("demand-message");
    const formData = new FormData(demandForm);
    const payload = Object.fromEntries(formData.entries());
    payload.quantity_kg = Number(payload.quantity_kg);
    payload.max_price_per_kg = Number(payload.max_price_per_kg);
    payload.delivery_latitude = Number(payload.delivery_latitude);
    payload.delivery_longitude = Number(payload.delivery_longitude);
    payload.required_delivery_datetime = toISO(payload.required_delivery_datetime);
    message.textContent = "Creating buyer demand...";
    try {
      const data = await apiRequest("/api/v1/buyer-demands", "POST", payload);
      message.textContent = `Demand created: ${data.id}`;
    } catch (err) {
      message.textContent = err.message;
    }
  });
}

const matchForm = document.getElementById("match-form");
if (matchForm) {
  matchForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const message = document.getElementById("match-message");
    const output = document.getElementById("match-output");
    const formData = new FormData(matchForm);
    const payload = Object.fromEntries(formData.entries());
    message.textContent = "Matching harvests...";
    output.textContent = "";
    try {
      const data = await apiRequest(`/api/v1/buyer-demands/${payload.buyer_demand_id}/match-harvests`, "POST", {});
      message.textContent = `Found ${data.matches.length} matches.`;
      output.textContent = JSON.stringify(data, null, 2);
    } catch (err) {
      message.textContent = err.message;
    }
  });
}
