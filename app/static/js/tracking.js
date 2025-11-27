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
});
