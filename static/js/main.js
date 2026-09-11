// main.js - shared behavior across all BharatVerse pages

document.addEventListener("DOMContentLoaded", function () {
  // ----- Mobile nav toggle -----
  const toggle = document.getElementById("navToggle");
  const links = document.getElementById("navLinks");
  if (toggle && links) {
    toggle.addEventListener("click", function () {
      links.classList.toggle("open");
    });
  }

  // ----- Animated number counters -----
  // Any element with data-count="123" will count up from 0 to 123.
  const counters = document.querySelectorAll("[data-count]");
  counters.forEach(function (el) {
    const target = parseInt(el.getAttribute("data-count"), 10) || 0;
    const duration = 800; // milliseconds
    const startTime = performance.now();

    function step(now) {
      const progress = Math.min((now - startTime) / duration, 1);
      const value = Math.round(progress * target);
      el.textContent = value;
      if (progress < 1) {
        requestAnimationFrame(step);
      } else {
        el.textContent = target;
      }
    }
    requestAnimationFrame(step);
  });

  // ----- Auto-dismiss flash messages after a few seconds -----
  const flashes = document.querySelectorAll(".flash");
  flashes.forEach(function (flash) {
    setTimeout(function () {
      flash.style.transition = "opacity 0.5s ease";
      flash.style.opacity = "0";
      setTimeout(function () { flash.remove(); }, 500);
    }, 4000);
  });
});
