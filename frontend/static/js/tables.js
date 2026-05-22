function renderEmptyRow(tbody, colspan, message) {
  if (!tbody) return;
  tbody.innerHTML = `<tr class="table-empty"><td colspan="${colspan}"><p>${message}</p></td></tr>`;
}

function renderErrorRow(tbody, colspan, message) {
  if (!tbody) return;
  tbody.innerHTML = `<tr class="table-empty"><td colspan="${colspan}"><p class="text-danger">${message}</p></td></tr>`;
}

async function loadTableData(config) {
  const {
    endpoint,
    tbodyId,
    colspan,
    emptyMessage,
    errorMessage,
    rowRenderer,
    includeMeta = false,
  } = config;

  const tbody = document.getElementById(tbodyId);
  if (!tbody) return;

  renderEmptyRow(tbody, colspan, "Loading...");
  try {
    const payload = await apiRequest(endpoint, "GET", null, { includeMeta });
    const rows = includeMeta ? ensureArray(payload.data) : ensureArray(payload);
    if (!rows.length) {
      renderEmptyRow(tbody, colspan, emptyMessage || "No records found.");
      return;
    }
    tbody.innerHTML = rows.map((item) => rowRenderer(item)).join("");
  } catch (err) {
    renderErrorRow(tbody, colspan, errorMessage || err.message || "Failed to load records.");
  }
}
