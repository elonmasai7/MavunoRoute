document.addEventListener("DOMContentLoaded", function () {
    var refreshBtn = document.getElementById("refresh-dashboard");
    if (refreshBtn) {
        refreshBtn.addEventListener("click", async function () {
            var status = document.getElementById("dashboard-status");
            var table = document.getElementById("dashboard-table");
            var tbody = table ? table.querySelector("tbody") : null;
            if (status) status.textContent = "Loading metrics...";
            if (tbody) tbody.innerHTML = "";
            try {
                var data = await apiRequest("/api/v1/reports/dashboard");
                if (tbody) {
                    Object.entries(data).forEach(function (_a) {
                        var key = _a[0], value = _a[1];
                        var row = document.createElement("tr");
                        row.innerHTML = "<th style=\"text-align:left;padding:0.5rem 0.75rem;\">" + key + "</th><td style=\"padding:0.5rem 0.75rem;\">" + value + "</td>";
                        tbody.appendChild(row);
                    });
                }
                if (table) table.hidden = false;
                if (status) status.textContent = "Metrics loaded.";
            } catch (err) {
                if (status) status.textContent = err.message;
                if (table) table.hidden = true;
            }
        });
    }
});
