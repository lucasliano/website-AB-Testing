// Vanilla JS to handle interaction of front-end components.

document.addEventListener("DOMContentLoaded", () => {
  initMobileNavToggle();
  initModalSystem();
  initFiltering();
  initContactForm();
});

// Toggle mobile navigation panel using data-toggle="mobile-nav" and data-mobile-nav-panel
function initMobileNavToggle() {
  const toggle = document.querySelector("[data-toggle='mobile-nav']");
  const panel = document.querySelector("[data-mobile-nav-panel]");
  if (!toggle || !panel) return;

  toggle.addEventListener("click", () => {
    panel.classList.toggle("hidden");
  });
}

// Popup form
function initModalSystem() {
  const openers = document.querySelectorAll("[data-modal-open]");
  const modals = document.querySelectorAll("[data-modal]");

  function findModal(id) {
    return Array.from(modals).find((m) => m.getAttribute("data-modal") === id);
  }

  function openModal(id) {
    const modal = findModal(id);
    if (!modal) return;
    modal.classList.remove("hidden");
    modal.setAttribute("aria-hidden", "false");
    document.body.classList.add("overflow-hidden");
  }

  function closeModal(modal) {
    if (!modal) return;
    modal.classList.add("hidden");
    modal.setAttribute("aria-hidden", "true");
    document.body.classList.remove("overflow-hidden");
  }

  openers.forEach((btn) => {
    btn.addEventListener("click", () => {
      const id = btn.getAttribute("data-modal-open");
      if (id) openModal(id);
    });
  });

  modals.forEach((modal) => {
    const closes = modal.querySelectorAll("[data-modal-close]");
    const overlay = modal.querySelector("[data-modal-overlay]");

    closes.forEach((btn) => {
      btn.addEventListener("click", () => closeModal(modal));
    });

    if (overlay) {
      overlay.addEventListener("click", () => closeModal(modal));
    }
  });

  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape") {
      const openModalEl = Array.from(modals).find((m) => !m.classList.contains("hidden"));
      if (openModalEl) {
        closeModal(openModalEl);
      }
    }
  });
}

// Search engine
function initFiltering() {
  const searchInput = document.querySelector("[data-filter-search]");
  const categorySelect = document.querySelector("[data-filter-category]");
  const statusSelect = document.querySelector("[data-filter-status]");
  const resetButtons = document.querySelectorAll("[data-filter-reset]");
  const cards = document.querySelectorAll("[data-initiative-card]");

  if (!cards.length) return;

  function normalize(text) {
    return (text || "").toString().toLowerCase().normalize("NFD").replace(/\p{Diacritic}/gu, "");
  }

  function applyFilters() {
    const term = normalize(searchInput ? searchInput.value : "");
    const status = statusSelect ? statusSelect.value : "";

    cards.forEach((card) => {
      const title = normalize(card.getAttribute("data-initiative-title"));
      const cardStatus = card.getAttribute("data-initiative-status") || "";

      let matches = true;

      if (term && !title.includes(term)) {
        matches = false;
      }

      if (status && cardStatus !== status) {
        matches = false;
      }

      if (matches) {
        card.classList.remove("hidden");
      } else {
        card.classList.add("hidden");
      }
    });
  }

  if (searchInput) {
    searchInput.addEventListener("input", applyFilters);
  }
  if (statusSelect) {
    statusSelect.addEventListener("change", applyFilters);
  }
  resetButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      if (searchInput) searchInput.value = "";
      if (categorySelect) categorySelect.value = "";
      if (statusSelect) statusSelect.value = "";
      applyFilters();
    });
  });
}

// Contact form
function initContactForm() {
  // El modal del formulario está marcado con data-modal="contact-form"
  const modal = document.querySelector('[data-modal="contact-form"]');
  if (!modal) return;

  const form = modal.querySelector("form");
  if (!form) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault(); // evitamos submit clásico (recarga de página)

    const submitButton = form.querySelector("button[type='submit']");
    if (submitButton) {
      submitButton.disabled = true;
    }

    try {
      // Usamos FormData para incluir también el archivo
      const formData = new FormData(form);

      // Por si en el HTML dejaste el campo iniciativa como disabled,
      // nos aseguramos de incluirlo igualmente:
      const iniciativaInput = modal.querySelector("#contact-iniciativa");
      if (iniciativaInput) {
        formData.set("iniciativa", iniciativaInput.value || "");
      }

      const response = await fetch("/api/contact-upload", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Error al enviar el formulario");
      }

      // Si querés leer la respuesta JSON:
      // const data = await response.json();

      // Feedback mínimo:
      form.reset();
      alert("¡Gracias! Hemos recibido tu envío.");

      // Si tenés lógica para cerrar el modal, la podés invocar acá.
      // Por ejemplo, si en initModalSystem tenés algo tipo closeModal(modal):
      // closeModal(modal);

    } catch (err) {
      console.error(err);
      alert("Hubo un problema al enviar el formulario. Intentá de nuevo.");
    } finally {
      if (submitButton) {
        submitButton.disabled = false;
      }
    }
  });
}
