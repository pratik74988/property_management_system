let currentSection = "home";
let searchType = "rent";
let isAdmin = false;
let currentUser = null;
let allProperties = [];

/* ================= NAV ================= */

function showSection(section) {
  currentSection = section;

  document.getElementById("homeSection").style.display =
    section === "home" ? "block" : "none";

  document.getElementById("propertiesSection").style.display =
    ["rent", "sale", "commercial"].includes(section) ? "block" : "none";

  document.getElementById("usersSection").style.display =
    section === "users" ? "block" : "none";

  document.querySelectorAll(".nav-link").forEach(link =>
    link.classList.remove("active")
  );

  if (event?.target) event.target.classList.add("active");

  if (section !== "home") renderProperties();
}

/* ================= SEARCH ================= */

function setSearchType(type) {
  searchType = type;
  document.querySelectorAll(".search-tab").forEach(tab =>
    tab.classList.remove("active")
  );
  event.target.classList.add("active");
}

function handleSearch(e) {
  e.preventDefault();
  const query = document.getElementById("searchInput").value.toLowerCase();
  showSection(searchType);

  const filtered = allProperties.filter(p =>
    (p.title + p.location).toLowerCase().includes(query)
  );

  renderProperties(filtered);
}

/* ================= PROPERTIES ================= */

function renderProperties(data = null) {
  const grid = document.getElementById("propertiesGrid");
  grid.innerHTML = "";

  const list = data || allProperties.filter(p => {
    if (currentSection === "rent") return p.type === "rent";
    if (currentSection === "sale") return p.type === "sale";
    if (currentSection === "commercial")
      return ["shop-rent", "shop-sale"].includes(p.type);
    return false;
  });

  if (list.length === 0) {
    grid.innerHTML = "<p>No properties found.</p>";
    return;
  }

  list.forEach(p => grid.appendChild(createPropertyCard(p)));
}

function createPropertyCard(p) {
  const div = document.createElement("div");
  div.className = "property-card";
  div.innerHTML = `
    <div class="property-image">🏠</div>
    <div class="property-content">
      <div class="property-price">₹${p.price}</div>
      <div class="property-title">${p.title}</div>
      <div class="property-location">📍 ${p.location}</div>
      <button class="btn-contact" onclick="contactForProperty('${p.title}')">
        Contact Now
      </button>
    </div>
  `;
  return div;
}

/* ================= AUTH ================= */

function openLoginModal() {
  alert("Hook login modal here");
}

function openSignupModal() {
  alert("Hook signup modal here");
}

function logout() {
  currentUser = null;
  isAdmin = false;
  showSection("home");
}

/* ================= CONTACT ================= */

function contactForProperty(title) {
  const phone = document.getElementById("contactPhone").textContent;
  const msg = `Hi, I'm interested in ${title}`;
  window.open(
    `https://wa.me/${phone.replace(/\D/g, "")}?text=${encodeURIComponent(msg)}`,
    "_blank"
  );
}

function makePhoneCall() {
  const phone = document.getElementById("contactPhone").textContent;
  window.location.href = `tel:${phone}`;
}

function openWhatsApp() {
  const phone = document.getElementById("whatsappNumber").textContent;
  window.open(`https://wa.me/${phone.replace(/\D/g, "")}`, "_blank");
}

function sendEmail() {
  const email = document.getElementById("contactEmail").textContent;
  window.location.href = `mailto:${email}`;
}

/* ================= INIT ================= */

document.addEventListener("DOMContentLoaded", () => {
  // dummy data for now
  allProperties = [];
});
