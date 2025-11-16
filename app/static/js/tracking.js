// Generic first-party analytics tracking.
// Attaches click listeners to any element with a `data-event-name` attribute
// and sends a lightweight POST to /api/track without blocking navigation.

document.addEventListener("DOMContentLoaded", function () {
  
  // Click tracker
  const trackable = document.querySelectorAll("[data-event-name]");
  trackable.forEach((el) => {
    el.addEventListener("click", () => {
      const eventName = el.dataset.eventName;
      if (!eventName) return;

      const payload = {
        event_name: eventName,       // Saves the string of the 'data-event-name' attribute
        page: window.location.pathname,
        variant: window.APP_VARIANT || null,
        metadata: {}                 // optional — If you add other attributes to the button, those will be saved here
      };

      try {
        const body = JSON.stringify(payload);

        if (navigator.sendBeacon) {
          const blob = new Blob([body], { type: "application/json" });
          navigator.sendBeacon("/api/track", blob);
        } else {
          fetch("/api/track", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body,
            keepalive: true,
          }).catch(() => {});
        }
      } catch (err) {
        console.error("Tracking error:", err);
      }
    });
  });

  // University quote form AJAX submission
  const form = document.getElementById("university-quote-form");
  if (form) {
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      const status = document.getElementById("university-quote-status");

      const formData = new FormData(form);
      const data = Object.fromEntries(formData.entries());

      fetch("/api/university-quote", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      })
        .then((res) => res.json())
        .then(() => {
          if (status) {
            status.textContent = "Thank you. We'll get back to you soon.";
          }
          form.reset();
        })
        .catch(() => {
          if (status) {
            status.textContent = "There was an error. Please try again.";
          }
        });
    });
  }

  // Simple applications tab switcher on homepage
  const tabButtons = document.querySelectorAll("[data-app-tab]");
  const panels = document.querySelectorAll("[data-app-panel]");

  if (tabButtons.length && panels.length) {
    tabButtons.forEach((btn) => {
      btn.addEventListener("click", () => {
        const target = btn.dataset.appTab;

        tabButtons.forEach((b) => {
          b.classList.remove("text-blue-900", "border-blue-900");
          b.classList.add("text-gray-600", "border-transparent");
        });
        btn.classList.add("text-blue-900", "border-blue-900");
        btn.classList.remove("text-gray-600", "border-transparent");

        panels.forEach((p) => {
          if (p.dataset.appPanel === target) {
            p.classList.remove("hidden");
          } else {
            p.classList.add("hidden");
          }
        });
      });
    });
  }
});
