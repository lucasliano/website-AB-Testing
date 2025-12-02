// Basic, attribute-driven interactivity for the LaserMakers marketing site.

(function () {
  'use strict';

  document.addEventListener('DOMContentLoaded', function () {
    setupNavToggle();
    setupScrollButtons();
    setupHeroSlider();
  });

  /**
   * Toggle mobile navigation using data-toggle / data-toggle-target attributes.
   */
  function setupNavToggle() {
    var toggles = document.querySelectorAll('[data-toggle]');
    toggles.forEach(function (button) {
      var targetKey = button.getAttribute('data-toggle');
      if (!targetKey) return;

      var target = document.querySelector('[data-toggle-target="' + targetKey + '"]');
      if (!target) return;

      button.addEventListener('click', function () {
        target.classList.toggle('hidden');
      });
    });
  }

  /**
   * Smooth scrolling for elements that declare a data-scroll-target selector.
   */
  function setupScrollButtons() {
    var buttons = document.querySelectorAll('[data-scroll-target]');
    buttons.forEach(function (btn) {
      btn.addEventListener('click', function (event) {
        var selector = btn.getAttribute('data-scroll-target');
        if (!selector) return;
        var target = document.querySelector(selector);
        if (!target) return;

        event.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
    });
  }

  /**
   * Simple hero slider controlled via dots.
   * - Slides: elements with [data-hero-slide]
   * - Dots: elements with [data-hero-dot] and data-hero-index
   */
  function setupHeroSlider() {
    var dots = document.querySelectorAll('[data-hero-dot]');
    var slides = document.querySelectorAll('[data-hero-slide]');
    if (!dots.length || !slides.length) return;

    function activateSlide(index) {
      slides.forEach(function (slide, i) {
        if (String(i) === String(index)) {
          slide.classList.remove('hidden', 'opacity-0');
          slide.classList.add('opacity-100');
        } else {
          slide.classList.add('hidden', 'opacity-0');
          slide.classList.remove('opacity-100');
        }
      });

      dots.forEach(function (dot, i) {
        if (String(i) === String(index)) {
          dot.classList.remove('bg-slate-300');
          dot.classList.add('bg-[#ff5a30]', 'scale-110');
        } else {
          dot.classList.remove('bg-[#ff5a30]', 'scale-110');
          dot.classList.add('bg-slate-300');
        }
      });
    }

    // Bind click handlers
    dots.forEach(function (dot) {
      dot.addEventListener('click', function () {
        var index = dot.getAttribute('data-hero-index');
        if (index == null) return;
        activateSlide(index);
      });
    });

    // Ensure an initial state
    activateSlide(0);
  }
})();
