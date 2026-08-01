(function () {
  "use strict";

  const THEME_KEY = "url-shortener-theme";
  const root = document.documentElement;
  const themeToggle = document.getElementById("theme-toggle");
  const themeIcon = document.getElementById("theme-icon");

  function applyTheme(theme) {
    root.setAttribute("data-theme", theme);
    themeIcon.textContent = theme === "dark" ? "☀️" : "🌙";
  }

  function initTheme() {
    const stored = localStorage.getItem(THEME_KEY);
    if (stored) {
      applyTheme(stored);
      return;
    }
    const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches;
    applyTheme(prefersDark ? "dark" : "light");
  }

  themeToggle.addEventListener("click", function () {
    const current = root.getAttribute("data-theme");
    const next = current === "dark" ? "light" : "dark";
    localStorage.setItem(THEME_KEY, next);
    applyTheme(next);
  });

  initTheme();

  const form = document.getElementById("shorten-form");
  const urlInput = document.getElementById("url-input");
  const submitBtn = document.getElementById("submit-btn");
  const errorEl = document.getElementById("form-error");
  const resultEl = document.getElementById("result");
  const resultLink = document.getElementById("result-link");
  const copyBtn = document.getElementById("copy-btn");
  const statClicks = document.getElementById("stat-clicks");
  const statCreated = document.getElementById("stat-created");
  const statLastAccessed = document.getElementById("stat-last-accessed");

  function showError(message) {
    errorEl.textContent = message;
    errorEl.hidden = false;
    resultEl.hidden = true;
  }

  function hideError() {
    errorEl.hidden = true;
  }

  function formatDate(iso) {
    if (!iso) return "Never";
    const date = new Date(iso);
    return date.toLocaleString();
  }

  function showResult(data) {
    resultLink.textContent = data.short_url;
    resultLink.href = data.short_url;
    statClicks.textContent = String(data.total_clicks);
    statCreated.textContent = formatDate(data.created_at);
    statLastAccessed.textContent = formatDate(data.last_accessed_at);
    resultEl.hidden = false;
  }

  form.addEventListener("submit", async function (event) {
    event.preventDefault();
    hideError();

    const url = urlInput.value.trim();
    if (!url) {
      showError("Please enter a URL.");
      return;
    }

    submitBtn.disabled = true;
    submitBtn.textContent = "Shortening...";

    try {
      const response = await fetch("https://cloud-url-shortner.onrender.com/api/shorten", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: url }),
      });

      const data = await response.json();

      if (!response.ok) {
        showError(data.error || "Something went wrong. Please try again.");
        return;
      }

      showResult(data);
    } catch (err) {
      showError("Could not reach the server. Please try again.");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Shorten";
    }
  });

  copyBtn.addEventListener("click", async function () {
    const text = resultLink.textContent;
    if (!text) return;

    try {
      await navigator.clipboard.writeText(text);
      const original = copyBtn.textContent;
      copyBtn.textContent = "Copied!";
      setTimeout(function () {
        copyBtn.textContent = original;
      }, 1500);
    } catch (err) {
      showError("Could not copy to clipboard.");
    }
  });
})();
