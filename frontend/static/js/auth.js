const API_BASE = "/api/v1/auth";

const ROLE_DASHBOARD_ROUTES = {
  FARMER: "/farmer/dashboard",
  BUYER: "/buyer/dashboard",
  TRANSPORTER: "/transporter/dashboard",
  COLD_HUB_OPERATOR: "/cold-hub/dashboard",
  COOPERATIVE_ADMIN: "/cooperative/dashboard",
  SUPER_ADMIN: "/admin/dashboard",
  OPS_ADMIN: "/admin/dashboard",
  FINANCE_PARTNER: "/admin/dashboard",
};

function setCookie(name, value, days) {
  const expires = new Date(Date.now() + days * 864e5).toUTCString();
  document.cookie = `${name}=${encodeURIComponent(value)}; expires=${expires}; path=/; SameSite=Lax`;
}

async function postJSON(url, payload) {
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  let body;
  try {
    body = await response.json();
  } catch {
    throw new Error("Unable to parse server response");
  }

  if (!response.ok || body.success === false) {
    throw new Error(body.message || "Request failed");
  }
  return body.data || {};
}

function setFormBusy(form, isBusy) {
  const submitBtn = form.querySelector('button[type="submit"]');
  if (submitBtn) {
    submitBtn.disabled = isBusy;
  }
}

function setMessage(element, text, isError = false) {
  if (!element) {
    return;
  }
  element.className = isError ? "form-message error" : "form-message";
  element.textContent = text;
}

const loginForm = document.getElementById("login-form");
if (loginForm) {
  loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(loginForm);
    const payload = Object.fromEntries(formData.entries());
    const message = document.getElementById("login-message");

    setFormBusy(loginForm, true);
    setMessage(message, "Signing in...");

    try {
      const data = await postJSON(`${API_BASE}/login`, payload);
      localStorage.setItem("mavuno_access_token", data.access_token || "");
      localStorage.setItem("mavuno_refresh_token", data.refresh_token || "");
      if (data.access_token) {
        setCookie("mavuno_access_token", data.access_token, 1);
      }
      if (data.refresh_token) {
        setCookie("mavuno_refresh_token", data.refresh_token, 14);
      }

      const target = ROLE_DASHBOARD_ROUTES[data.role] || "/dashboard";
      window.location.assign(target);
    } catch (err) {
      setMessage(message, err.message || "Login failed", true);
    } finally {
      setFormBusy(loginForm, false);
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

    setFormBusy(registerForm, true);
    setMessage(message, "Creating account...");

    try {
      await postJSON(`${API_BASE}/register`, payload);
      setMessage(message, "Registration successful. Redirecting to login...");
      window.setTimeout(() => {
        window.location.assign("/login");
      }, 800);
    } catch (err) {
      setMessage(message, err.message || "Registration failed", true);
    } finally {
      setFormBusy(registerForm, false);
    }
  });
}
