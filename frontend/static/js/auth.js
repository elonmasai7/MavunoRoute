const API_BASE = "/api/v1/auth";

async function setCookie(name, value, days) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax`;
}

function postJSON(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const body = await response.json();
  if (!response.ok || body.success === false) {
    throw new Error(body.message || "Request failed");
  }
  return body.data;
}

const loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(loginForm);
    const payload = Object.fromEntries(formData.entries());
    const message = document.getElementById("login-message");
    message.textContent = "Signing in...";

    try {
      const data = await postJSON(`${API_BASE}/login`, payload);
      localStorage.setItem("mavuno_access_token", data.access_token);
      localStorage.setItem("mavuno_refresh_token", data.refresh_token);
      setCookie("mavuno_access_token", data.access_token, 1);
      setCookie("mavuno_refresh_token", data.refresh_token, 14);
      message.innerHTML = 'Login successful. <a href="/dashboard">Go to dashboard</a>.';
    } catch (err) {
      message.textContent = err.message;
    }
  });
}

const registerForm = document.getElementById("register-form");
if (registerForm) {
  registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(registerForm);
    const payload = Object.fromEntries(formData.entries());
    const message = document.getElementById("register-message");
    message.textContent = "Creating account...";

    try {
      await postJSON(`${API_BASE}/register`, payload);
      message.textContent = "Registration successful. You can now log in.";
    } catch (err) {
      message.textContent = err.message;
    }
  });
}
