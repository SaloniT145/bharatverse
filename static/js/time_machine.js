// time_machine.js - handles the Time Machine activation animation

document.addEventListener("DOMContentLoaded", function () {
  const initiateBtn = document.getElementById("initiateBtn");
  const loading = document.getElementById("tmLoading");
  const status = document.getElementById("tmStatus");
  const loadingText = document.getElementById("tmLoadingText");

  if (!initiateBtn) return;

  initiateBtn.addEventListener("click", function () {
    const destinationUrl = initiateBtn.getAttribute("data-url");

    initiateBtn.disabled = true;
    initiateBtn.style.opacity = "0.5";
    status.textContent = "TIME TRAVEL INITIATED";
    loading.hidden = false;

    const messages = [
      "TIME TRAVEL INITIATED...",
      "CALIBRATING TEMPORAL COORDINATES...",
      "ENTERING THE INDUS VALLEY...",
    ];
    let i = 0;
    const interval = setInterval(function () {
      i++;
      if (i < messages.length) {
        loadingText.textContent = messages[i];
      }
    }, 700);

    setTimeout(function () {
      clearInterval(interval);
      window.location.href = destinationUrl;
    }, 2200);
  });
});
