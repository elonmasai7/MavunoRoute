function safeMapContainer(containerId) {
  return document.getElementById(containerId);
}

function renderCoordinates(containerId, latitude, longitude) {
  const container = safeMapContainer(containerId);
  if (!container) return;
  if (latitude == null || longitude == null) {
    container.textContent = "Location unavailable";
    return;
  }
  container.textContent = `Lat ${latitude}, Lng ${longitude}`;
}
