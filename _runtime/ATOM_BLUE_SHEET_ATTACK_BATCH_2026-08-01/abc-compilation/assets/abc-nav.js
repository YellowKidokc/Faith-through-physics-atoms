function setFilter(mode) {
  document.querySelectorAll("[data-topic-row]").forEach((row) => {
    const hasGap = row.dataset.hasGap === "true";
    const hasLocked = row.dataset.hasLocked === "true";
    row.style.display =
      mode === "all" ||
      (mode === "gaps" && hasGap) ||
      (mode === "locked" && hasLocked)
        ? ""
        : "none";
  });
}

window.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll("[data-filter]").forEach((button) => {
    button.addEventListener("click", () => setFilter(button.dataset.filter));
  });
});
