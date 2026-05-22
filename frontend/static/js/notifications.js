document.addEventListener("DOMContentLoaded", () => {
  const tbodyId = "notifications-list";

  const reloadButton = document.getElementById("reload-notifications");
  if (reloadButton) {
    reloadButton.addEventListener("click", () => {
      loadNotifications();
    });
  }

  function rowRenderer(notification) {
    const statusClass = notification.status === "READ" ? "badge-info" : "badge-warning";
    return `
      <tr>
        <td>${notification.channel || "-"}</td>
        <td>${notification.subject || "No subject"}</td>
        <td><span class="badge ${statusClass}">${notification.status || "NEW"}</span></td>
        <td>${formatDateTime(notification.created_at)}</td>
        <td>
          <button class="btn btn-sm btn-outline" data-notification-id="${notification.id}" type="button">Mark Read</button>
        </td>
      </tr>
    `;
  }

  async function attachMarkReadHandlers() {
    const buttons = document.querySelectorAll("[data-notification-id]");
    if (!buttons.length) return;

    buttons.forEach((button) => {
      button.addEventListener("click", async () => {
        const id = button.getAttribute("data-notification-id");
        if (!id) return;
        button.disabled = true;
        try {
          await apiRequest(`/api/v1/notifications/${id}/read`, "PATCH", {});
          loadNotifications();
        } catch (err) {
          button.disabled = false;
        }
      });
    });
  }

  async function loadNotifications() {
    await loadTableData({
      endpoint: "/api/v1/notifications?page=1&per_page=20",
      tbodyId,
      colspan: 5,
      emptyMessage: "No notifications found.",
      errorMessage: "Unable to load notifications.",
      rowRenderer,
      includeMeta: true,
    });
    await attachMarkReadHandlers();
  }

  loadNotifications();
});
