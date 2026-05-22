document.addEventListener("DOMContentLoaded", () => {
  const button = document.getElementById("refresh-dashboard");
  if (!button) return;

  button.addEventListener("click", async () => {
    const status = document.getElementById("dashboard-status");
    const table = document.getElementById("dashboard-table");
    const tbody = table ? table.querySelector("tbody") : null;
    if (!tbody || !status) return;

    status.textContent = "Loading metrics...";
    tbody.innerHTML = "";

    try {
      const data = await apiRequest("/api/v1/reports/dashboard");
      const entries = Object.entries(data || {});
      if (!entries.length) {
        tbody.innerHTML = '<tr class="table-empty"><td><p>No dashboard metrics available.</p></td></tr>';
      } else {
        entries.forEach(([key, value]) => {
          const row = document.createElement("tr");
          row.innerHTML = `<th style="text-align:left;padding:0.5rem 0.75rem;">${key}</th><td style="padding:0.5rem 0.75rem;">${value ?? "-"}</td>`;
          tbody.appendChild(row);
        });
      }
      table.hidden = false;
      status.textContent = "Metrics loaded.";
    } catch (err) {
      status.textContent = err.message || "Failed to load metrics";
      table.hidden = true;
    }
  });
});
