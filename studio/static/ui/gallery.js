"use strict";

const navigation = document.querySelectorAll(".section-nav a");
const sections = Array.from(document.querySelectorAll(".gallery-section"));
const mobileNav = document.querySelector(".mobile-nav");

function markSection(id) {
  for (const link of navigation) {
    if (link.hash === "#" + id) link.setAttribute("aria-current", "location");
    else link.removeAttribute("aria-current");
  }
}

function markVisibleSection() {
  let section = sections[0];
  const threshold = Math.min(170, window.innerHeight / 3);
  for (const candidate of sections) {
    if (candidate.getBoundingClientRect().top > threshold) break;
    section = candidate;
  }
  if (window.scrollY + window.innerHeight >= document.documentElement.scrollHeight - 2) {
    section = sections[sections.length - 1];
  }
  markSection(section.id);
}

let pendingScroll = false;
window.addEventListener("scroll", () => {
  if (pendingScroll) return;
  pendingScroll = true;
  window.requestAnimationFrame(() => {
    pendingScroll = false;
    markVisibleSection();
  });
}, { passive: true });

for (const link of navigation) {
  link.addEventListener("click", () => {
    if (mobileNav.open) mobileNav.open = false;
    const target = document.getElementById(link.hash.slice(1));
    if (target) {
      markSection(target.id);
      target.focus({ preventScroll: true });
    }
  });
}
mobileNav.addEventListener("keydown", (event) => {
  if (event.key === "Escape" && mobileNav.open) {
    mobileNav.open = false;
    mobileNav.querySelector("summary").focus();
  }
});
markVisibleSection();

const actionResult = document.getElementById("action-result");
document.getElementById("demo-primary").addEventListener("click", () => {
  actionResult.textContent = "Action exécutée dans la galerie.";
});
document.getElementById("demo-reset").addEventListener("click", () => {
  actionResult.textContent = "Démonstration réinitialisée.";
});

const nameInput = document.getElementById("site-name");
const nameError = document.getElementById("site-name-error");
const nameResult = document.getElementById("name-result");
document.getElementById("name-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const value = nameInput.value.trim();
  if (value.length < 2 || value.length > 80) {
    nameResult.textContent = "";
    nameInput.setAttribute("aria-invalid", "true");
    nameError.textContent = "Le nom doit contenir entre 2 et 80 caractères.";
    nameError.hidden = false;
    nameInput.focus();
    return;
  }
  nameInput.removeAttribute("aria-invalid");
  nameError.hidden = true;
  nameError.textContent = "";
  nameResult.textContent = "Nom valide : " + value + ".";
});
nameInput.addEventListener("input", () => {
  nameInput.removeAttribute("aria-invalid");
  nameError.hidden = true;
  nameError.textContent = "";
  nameResult.textContent = "";
});

function searchKey(text) {
  return text.toLocaleLowerCase("fr").normalize("NFD").replace(/[\u0300-\u036f]/g, "").trim();
}

const filter = document.getElementById("site-filter");
const table = document.getElementById("site-table");
const rows = Array.from(table.tBodies[0].rows);
const empty = document.getElementById("table-empty");
const count = document.getElementById("filter-count");

function filterTable() {
  const term = searchKey(filter.value);
  let matches = 0;
  for (const row of rows) {
    const terms = Array.from(row.cells, cell => cell.textContent).join(" ");
    row.hidden = !searchKey(terms).includes(term);
    if (!row.hidden) matches++;
  }
  table.hidden = matches === 0;
  empty.hidden = matches !== 0;
  count.textContent = matches + (matches > 1 ? " sites" : " site");
}

filter.addEventListener("input", filterTable);
document.getElementById("clear-filter").addEventListener("click", () => {
  filter.value = "";
  filterTable();
  filter.focus();
});
