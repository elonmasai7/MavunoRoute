document.addEventListener("DOMContentLoaded", () => {
  if (!document.getElementById("jobs-list")) return;
  loadTableData({
    endpoint: "/api/v1/transport-jobs?page=1&per_page=20",
    tbodyId: "jobs-list",
    colspan: 6,
    emptyMessage: "No transport jobs found.",
    errorMessage: "Unable to load transport jobs.",
    includeMeta: true,
    rowRenderer: (j) => `
      <tr>
        <td>${(j.id || "").slice(0, 8)}</td>
        <td>${j.route_plan_id || "-"}</td>
        <td>${j.vehicle_id || "-"}</td>
        <td><span class="badge badge-info">${j.delivery_status || "UNKNOWN"}</span></td>
        <td>${formatDate(j.scheduled_pickup_time)}</td>
        <td><a href="/transporter/jobs/${j.id}" class="btn btn-sm btn-outline">View</a></td>
      </tr>
    `,
  });
});
