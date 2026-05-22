document.addEventListener("DOMContentLoaded", () => {
  if (!document.getElementById("harvests-list")) return;
  loadTableData({
    endpoint: "/api/v1/harvest-batches?page=1&per_page=20",
    tbodyId: "harvests-list",
    colspan: 7,
    emptyMessage: "No harvests found.",
    errorMessage: "Unable to load harvests.",
    includeMeta: true,
    rowRenderer: (h) => `
      <tr>
        <td>${h.crop_id || "-"}</td>
        <td>${h.quantity_kg || 0}</td>
        <td>${h.grade || "-"}</td>
        <td>${formatCurrency(h.asking_price_per_kg)}</td>
        <td><span class="badge badge-info">${h.status || "UNKNOWN"}</span></td>
        <td>${formatDate(h.created_at)}</td>
        <td><a href="/farmer/harvests/${h.id}" class="btn btn-sm btn-outline">View</a></td>
      </tr>
    `,
  });
});
