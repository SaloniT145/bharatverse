// map.js - handles clicking on Civilization Map markers

document.addEventListener("DOMContentLoaded", function () {
  const markers = document.querySelectorAll(".map-marker");
  const panel = document.getElementById("sitePanel");
  const nameEl = document.getElementById("siteName");
  const regionEl = document.getElementById("siteRegion");
  const importanceEl = document.getElementById("siteImportance");
  const factEl = document.getElementById("siteFact");

  markers.forEach(function (marker) {
    marker.addEventListener("click", function () {
      nameEl.textContent = marker.getAttribute("data-name");
      regionEl.textContent = marker.getAttribute("data-region");
      importanceEl.textContent = marker.getAttribute("data-importance");
      factEl.textContent = marker.getAttribute("data-fact");
      panel.hidden = false;
      panel.scrollIntoView({ behavior: "smooth", block: "nearest" });
    });
  });
});
