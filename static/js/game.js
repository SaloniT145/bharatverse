// game.js - small interaction helpers for the game/result screens

document.addEventListener("DOMContentLoaded", function () {
  // Highlight the selected choice card and prevent double-submits
  const form = document.getElementById("choiceForm");
  if (form) {
    const cards = form.querySelectorAll(".choice-card");
    cards.forEach(function (card) {
      const input = card.querySelector("input");
      card.addEventListener("click", function () {
        cards.forEach(function (c) { c.classList.remove("selected"); });
        input.checked = true;
        card.classList.add("selected");
      });
    });

    form.addEventListener("submit", function () {
      const btn = document.getElementById("submitChoiceBtn");
      if (btn) {
        btn.disabled = true;
        btn.textContent = "Recording your decision...";
      }
    });
  }
});
