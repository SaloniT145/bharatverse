document.addEventListener("DOMContentLoaded", function () {
  const modal = document.createElement("div");
  modal.className = "level-modal";
  modal.hidden = true;
  modal.innerHTML = `
    <div class="level-modal-card" role="dialog" aria-modal="true" aria-labelledby="levelModalTitle">
      <button class="level-modal-close" type="button" aria-label="Close level details">&times;</button>
      <span class="modal-level"></span>
      <h2 id="levelModalTitle"></h2>
      <p class="modal-date"></p>
      <span class="modal-status"></span>
      <p class="modal-description"></p>
      <a class="btn btn-primary btn-small modal-action" href="#"></a>
    </div>`;
  document.body.appendChild(modal);

  const modalLevel = modal.querySelector(".modal-level");
  const modalTitle = modal.querySelector("h2");
  const modalDate = modal.querySelector(".modal-date");
  const modalStatus = modal.querySelector(".modal-status");
  const modalDescription = modal.querySelector(".modal-description");
  const modalAction = modal.querySelector(".modal-action");
  const closeButton = modal.querySelector(".level-modal-close");

  function closeModal() {
    modal.hidden = true;
  }

  function openModal(pin) {
    const status = pin.dataset.status;
    modalLevel.textContent = pin.dataset.level;
    modalTitle.textContent = pin.dataset.title;
    modalDate.textContent = pin.dataset.date;
    modalStatus.textContent = status === "completed" ? "Completed" : status === "unlocked" ? "Ready to play" : "Locked · Complete the previous level";
    modalDescription.textContent = pin.dataset.description;
    modalAction.hidden = !pin.dataset.actionUrl;
    if (pin.dataset.actionUrl) {
      modalAction.href = pin.dataset.actionUrl;
      modalAction.textContent = status === "completed" ? "View historical record" : "Play this level";
    }
    modal.hidden = false;
    closeButton.focus();
  }

  document.querySelectorAll(".map-pin").forEach(function (pin) {
    pin.addEventListener("click", function () {
      openModal(pin);
    });
  });

  closeButton.addEventListener("click", closeModal);
  modal.addEventListener("click", function (event) {
    if (event.target === modal) closeModal();
  });
  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape" && !modal.hidden) closeModal();
  });
});
