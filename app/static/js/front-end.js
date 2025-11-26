// static/js/front-end.js
// Vanilla JS to handle navigation, modal behavior, filters, character counters and pill groups.

document.addEventListener("DOMContentLoaded", () => {
  initMobileNavToggle();
  initModalSystem();
  initFiltering();
  initCharacterCounters();
  initPillGroups();
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

// Simple modal system driven by data-modal-open / data-modal / data-modal-close / data-modal-overlay
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

// Filtering initiatives on the dashboard by search, category and status
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
    const category = categorySelect ? categorySelect.value : "";
    const status = statusSelect ? statusSelect.value : "";

    cards.forEach((card) => {
      const title = normalize(card.getAttribute("data-initiative-title"));
      const cardCategory = card.getAttribute("data-initiative-category") || "";
      const cardStatus = card.getAttribute("data-initiative-status") || "";

      let matches = true;

      if (term && !title.includes(term)) {
        matches = false;
      }

      if (category && cardCategory !== category) {
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
  if (categorySelect) {
    categorySelect.addEventListener("change", applyFilters);
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

// Character counters for inputs / textareas with data-character-count
function initCharacterCounters() {
  const inputs = document.querySelectorAll("[data-character-count]");
  if (!inputs.length) return;

  inputs.forEach((input) => {
    const id = input.getAttribute("data-counter-id");
    if (!id) return;
    const counter = document.querySelector(`[data-character-counter][data-counter-for='${id}']`);
    if (!counter) return;

    const max = parseInt(counter.getAttribute("data-max-length") || input.getAttribute("maxlength") || "0", 10);

    const update = () => {
      const length = input.value.length;
      if (max > 0) {
        counter.textContent = `${length}/${max}`;
      } else {
        counter.textContent = `${length}`;
      }
    };

    input.addEventListener("input", update);
    update();
  });
}

// Pill radio / multi-select groups used in the submission modal
function initPillGroups() {
  const options = document.querySelectorAll("[data-pill-option]");
  if (!options.length) return;

  function updateHiddenInput(name, values) {
    const input = document.querySelector(`[data-pill-input='${name}']`);
    if (!input) return;
    input.value = Array.isArray(values) ? values.join(",") : values;
  }

  options.forEach((option) => {
    option.addEventListener("click", () => {
      const name = option.getAttribute("data-pill-name");
      const value = option.getAttribute("data-pill-value");
      const isSingle = option.hasAttribute("data-pill-single");
      if (!name || !value) return;

      const groupOptions = document.querySelectorAll(`[data-pill-option][data-pill-name='${name}']`);

      if (isSingle) {
        groupOptions.forEach((opt) => {
          const isCurrent = opt === option;
          if (isCurrent) {
            const currentlyChecked = opt.getAttribute("data-checked") === "true";
            const newState = !currentlyChecked;
            opt.setAttribute("data-checked", newState ? "true" : "false");
            updateHiddenInput(name, newState ? value : "");
          } else {
            opt.setAttribute("data-checked", "false");
          }
        });
      } else {
        const checked = option.getAttribute("data-checked") === "true";
        option.setAttribute("data-checked", checked ? "false" : "true");

        const selectedValues = Array.from(groupOptions)
          .filter((opt) => opt.getAttribute("data-checked") === "true")
          .map((opt) => opt.getAttribute("data-pill-value"));

        updateHiddenInput(name, selectedValues);
      }
    });
  });
}
