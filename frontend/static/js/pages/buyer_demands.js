document.addEventListener("DOMContentLoaded", () => {
  if (!document.getElementById("demands-list")) return;
  loadTableData({
    endpoint: "/api/v1/buyer-demands?page=1&per_page=20",
    tbodyId: "demands-list",
    colspan: 6,
    emptyMessage: "No demands found.",
    errorMessage: "Unable to load demands.",
    includeMeta: true,
    rowRenderer: (d) => `
      <tr>
        <td>${d.crop_id || "-"}</td>
        <td>${d.quantity_kg || 0}</td>
        <td>${formatCurrency(d.max_price_per_kg)}</td>
        <td><span class="badge badge-info">${d.status || "UNKNOWN"}</span></td>
        <td>${formatDate(d.required_delivery_datetime)}</td>
        <td><a href="/buyer/demands/${d.id}" class="btn btn-sm btn-outline">View</a></td>
      </tr>
    `,
  });
});
