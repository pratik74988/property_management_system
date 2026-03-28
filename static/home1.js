/* ============================================================
   home.js  —  Shivtej Real Estate
   ------------------------------------------------------------
   Sections:
     1. State
     2. Navigation
     3. Search
     4. Property Filter + Load More
     5. Property Modal + Carousel
     6. Contact Actions
     7. Scroll Reveal
     8. Hamburger / Mobile Nav
     9. Announcement Popup  (Django template block)
   ============================================================ */


/* ============================================================
   1. STATE
   ============================================================ */

let searchType    = "rent";   // active tab in the hero search box
let currentFilter = "all";    // active filter passed to filterProperties()
let visibleCount  = 0;        // how many cards are currently shown
let filteredCards = [];       // DOM nodes matching the current filter

const PAGE_SIZE = 5;          // cards revealed per "Load More" click


/* ============================================================
   2. NAVIGATION
   ─ showSection() is called from the Home nav-link only.
   ─ Rent / Buy links call filterProperties() directly.
   ============================================================ */

/**
 * Toggle between the hero/home view and the properties or users section.
 *
 * @param {string} section - "home" | "rent" | "sale" | "commercial" | "users"
 * @param {Event}  [evt]   - click event forwarded from the inline onclick attr
 *
 * FIX #1: Added `evt` parameter — previously the function read the implicit
 * global `event`, which is unreliable and throws when called programmatically
 * (e.g. from logout()).
 */
function showSection(section, evt) {
  const homeEl       = document.getElementById("homeSection");
  const propsEl      = document.getElementById("propertiesSection");
  const usersEl      = document.getElementById("usersSection");

  homeEl.style.display  = section === "home"  ? "block" : "none";
  propsEl.style.display = ["rent", "sale", "commercial"].includes(section) ? "block" : "none";
  usersEl.style.display = section === "users" ? "block" : "none";

  // Update active nav link highlight
  document.querySelectorAll(".nav-link").forEach(l => l.classList.remove("active"));
  if (evt?.target) evt.target.classList.add("active");

  // When switching to a property view, run the filter so cards are visible
  if (section !== "home" && section !== "users") {
    filterProperties(section, null);
  }
}


/* ============================================================
   3. SEARCH
   ─ setSearchType() tracks which tab (Rent / Buy / Commercial)
     is active in the hero search box.
   ─ handleSearch() filters the DOM cards by text query.
   ============================================================ */

/**
 * Set the active search-type tab in the hero search box.
 *
 * @param {string} type - "rent" | "buy" | "commercial"
 * @param {Event}  evt  - click event forwarded from the inline onclick attr
 *
 * FIX #1 (same root cause): Added `evt` parameter instead of relying on the
 * implicit global `event`.
 */
function setSearchType(type, evt) {
  searchType = type;
  document.querySelectorAll(".search-tab").forEach(t => t.classList.remove("active"));
  if (evt?.target) evt.target.classList.add("active");
}

/**
 * Handle the hero search form submission.
 * Filters the Django-rendered .property-card-wrapper DOM nodes by text content.
 *
 * FIX #2: The old implementation called renderProperties() which operated on
 * the JS `allProperties` array (always empty in production — data comes from
 * Django templates).  This meant search NEVER returned results.  Now we filter
 * the real DOM cards, consistent with how filterProperties() works.
 *
 * @param {Event} e - form submit event
 */
function handleSearch(e) {
  e.preventDefault();
  const query = document.getElementById("searchInput").value.toLowerCase().trim();

  // Map the search-box tab to the correct listing type
  const typeMap = { rent: "rent", buy: "sale", commercial: "commercial" };
  const listingType = typeMap[searchType] || "rent";

  // First apply the type filter (sets up section heading, resets cards, etc.)
  filterProperties(listingType, null);

  // If there's an actual query, further narrow filteredCards by text match
  if (query) {
    filteredCards = filteredCards.filter(card =>
      card.textContent.toLowerCase().includes(query)
    );

    // Hide all cards then reveal only the matching batch
    document.querySelectorAll("#propertiesGrid .property-card-wrapper")
      .forEach(c => { c.style.display = "none"; });

    visibleCount = 0;
    renderNextBatch();
  }
}


/* ============================================================
   4. PROPERTY FILTER + LOAD MORE
   ─ filterProperties() reads the Django-rendered card wrappers,
     hides/shows them by data-listing attribute, and paginates.
   ─ renderNextBatch() reveals the next PAGE_SIZE cards with a
     staggered fade-in animation.
   ============================================================ */

/**
 * Show the properties section filtered by listing type and update headings.
 *
 * @param {string}      type - "rent" | "sale" | "commercial" | "all"
 * @param {Event|null}  evt  - optional click event (can be null)
 */
function filterProperties(type, evt) {
  if (evt) evt.preventDefault();

  currentFilter = type;
  visibleCount  = 0;

  // Switch view: hide hero, show properties section
  document.getElementById("homeSection").style.display       = "none";
  document.getElementById("propertiesSection").style.display = "block";

  // Update section heading text
  const kicker   = document.getElementById("propertiesKicker");
  const title    = document.getElementById("propertiesTitle");
  const subtitle = document.getElementById("propertiesSubtitle");

  const headings = {
    rent:        ["For Rent",   "Rental Properties",        "Homes available for monthly rent"],
    sale:        ["For Sale",   "Properties for Sale",      "Own your dream home"],
    commercial:  ["Commercial", "Commercial Properties",    "Shops & offices for rent or sale"],
  };
  const [k, t, s] = headings[type] || ["Explore", "All Available Properties", "Every listing in one place"];
  kicker.textContent   = k;
  title.textContent    = t;
  subtitle.textContent = s;

  // Gather all Django-rendered card wrappers
  const all = Array.from(document.querySelectorAll("#propertiesGrid .property-card-wrapper"));

  // Filter by data-listing attribute (set in the Django template)
  filteredCards = (type === "all")
    ? all
    : all.filter(c => c.dataset.listing === type);

  // Reset visibility for all cards before revealing the first batch
  all.forEach(c => {
    c.style.display   = "none";
    c.style.opacity   = "0";
    c.style.transform = "translateY(16px)";
  });

  renderNextBatch();

  document.getElementById("propertiesSection").scrollIntoView({ behavior: "smooth", block: "start" });
  document.querySelectorAll(".nav-link").forEach(l => l.classList.remove("active"));
}

/**
 * Reveal the next PAGE_SIZE cards with a staggered fade-in animation.
 * Also shows/hides the "Load More" button.
 */
function renderNextBatch() {
  const batch = filteredCards.slice(visibleCount, visibleCount + PAGE_SIZE);

  batch.forEach((card, i) => {
    card.style.display = "";
    // Small delay per card creates a cascade / stagger effect
    setTimeout(() => {
      card.style.transition = "opacity 0.35s ease, transform 0.35s ease";
      card.style.opacity    = "1";
      card.style.transform  = "none";
    }, i * 80);
  });

  visibleCount += batch.length;

  // Show "Load More" only when there are still hidden cards
  const wrap = document.getElementById("loadMoreWrap");
  if (wrap) wrap.style.display = visibleCount < filteredCards.length ? "flex" : "none";
}

/** Public handler wired to the "Load More" button in the template. */
function loadMoreProperties() {
  renderNextBatch();
}

/** "Back" button on the properties section returns the user to the hero. */
function goBackToChooser() {
  document.getElementById("propertiesSection").style.display = "none";
  document.getElementById("homeSection").style.display       = "block";
  document.getElementById("homeSection").scrollIntoView({ behavior: "smooth" });
}


/* ============================================================
   5. PROPERTY MODAL + CAROUSEL
   ─ openPropertyModal() reads a <template class="property-data">
     embedded inside each card and populates the modal.
   ─ The carousel supports images & videos, dot navigation,
     arrow buttons, keyboard arrow keys, and touch swipe.
   ============================================================ */

let carouselIndex = 0;
let carouselTotal = 0;

/**
 * Open the property detail modal and populate it from the card's
 * embedded <template class="property-data"> element.
 *
 * @param {HTMLElement} card - the .property-card-wrapper element that was clicked
 */
function openPropertyModal(card) {
  const tmpl = card.querySelector("template.property-data");
  if (!tmpl) return;
  const doc = tmpl.content;

  // ── Populate text fields ──
  document.getElementById("modalTitle").textContent = doc.querySelector("data-title")?.textContent  || "";
  document.getElementById("modalArea").textContent  = doc.querySelector("data-area")?.textContent   || "";
  document.getElementById("modalRent").textContent  = doc.querySelector("data-price")?.textContent  || "";

  const mediaEl  = doc.querySelector("data-media");
  const descEl   = doc.querySelector("data-desc");
  const firstImg = doc.querySelector("data-img")?.textContent?.trim();

  // ── Build carousel ──
  const track    = document.getElementById("carouselTrack");
  const dots     = document.getElementById("carouselDots");
  const carousel = document.getElementById("modalCarousel");

  track.innerHTML = "";
  dots.innerHTML  = "";
  carouselIndex   = 0;

  // Collect media nodes; fall back to the legacy single data-img element
  const mediaNodes = mediaEl ? Array.from(mediaEl.children) : [];
  if (mediaNodes.length === 0 && firstImg) {
    mediaNodes.push(Object.assign(document.createElement("img"), { src: firstImg }));
  }

  carouselTotal = mediaNodes.length;

  mediaNodes.forEach((node, i) => {
    // ── Slide ──
    const slide = document.createElement("div");
    slide.className = "carousel-slide";

    if (node.tagName === "VIDEO") {
      const vid = document.createElement("video");
      vid.controls  = true;
      vid.innerHTML = node.innerHTML;   // copies <source> children
      slide.appendChild(vid);
    } else {
      const img = document.createElement("img");
      img.src     = node.src || node.getAttribute("src");
      img.alt     = "";
      img.loading = "lazy";
      slide.appendChild(img);
    }
    track.appendChild(slide);

    // ── Dot ──
    const dot = document.createElement("button");
    dot.className = "carousel-dot" + (i === 0 ? " active" : "");
    dot.setAttribute("aria-label", `Slide ${i + 1}`);
    dot.onclick = () => goToSlide(i);
    dots.appendChild(dot);
  });

  // Hide arrows / dots when there's only one media item
  carousel.classList.toggle("single", carouselTotal <= 1);
  updateCarousel();

  document.getElementById("modalBody").innerHTML = `<p>${descEl?.textContent || ""}</p>`;
  document.getElementById("propertyModal").classList.add("open");
  document.body.style.overflow = "hidden";
}

/**
 * Move the carousel by `dir` steps (+1 forward, -1 back).
 * Clamps to valid range — does not wrap around.
 *
 * @param {number} dir - direction: 1 or -1
 */
function carouselMove(dir) {
  carouselIndex = Math.max(0, Math.min(carouselIndex + dir, carouselTotal - 1));
  updateCarousel();
}

/**
 * Jump directly to a specific slide by index.
 *
 * @param {number} i - zero-based slide index
 */
function goToSlide(i) {
  carouselIndex = i;
  updateCarousel();
}

/**
 * Sync the carousel track position, counter text, dot highlights,
 * and prev/next arrow visibility to the current carouselIndex.
 */
function updateCarousel() {
  document.getElementById("carouselTrack").style.transform =
    `translateX(-${carouselIndex * 100}%)`;

  document.getElementById("carouselCounter").textContent =
    `${carouselIndex + 1} / ${carouselTotal}`;

  document.querySelectorAll(".carousel-dot").forEach((d, i) => {
    d.classList.toggle("active", i === carouselIndex);
  });

  document.getElementById("carouselPrev").classList.toggle("hidden", carouselIndex === 0);
  document.getElementById("carouselNext").classList.toggle("hidden", carouselIndex === carouselTotal - 1);
}

/** Close the property detail modal and restore page scrolling. */
function closeModal() {
  document.getElementById("propertyModal").classList.remove("open");
  document.body.style.overflow = "";
}


/* ============================================================
   6. CONTACT ACTIONS
   ─ All contact helpers read phone/email text from the DOM so
     a single edit to the HTML propagates everywhere.
   ============================================================ */

/**
 * Open WhatsApp with a pre-filled message referencing the property title.
 *
 * @param {string} title - property title used in the message body
 */
function contactForProperty(title) {
  const phone = document.getElementById("contactPhone").textContent.replace(/\D/g, "");
  const msg   = `Hi, I'm interested in ${title}`;
  window.open(`https://wa.me/${phone}?text=${encodeURIComponent(msg)}`, "_blank");
}

/**
 * Initiate a phone call to the contact number.
 *
 * FIX #6: Strip whitespace from the phone string before constructing the
 * tel: URI — spaces in tel: URIs cause failures on some mobile browsers.
 */
function makePhoneCall() {
  const phone = document.getElementById("contactPhone").textContent.replace(/\s/g, "");
  window.location.href = `tel:${phone}`;
}

/** Open WhatsApp for the general contact number (no pre-filled message). */
function openWhatsApp() {
  const phone = document.getElementById("whatsappNumber").textContent.replace(/\D/g, "");
  window.open(`https://wa.me/${phone}`, "_blank");
}

/** Open the default mail client addressed to the contact email. */
function sendEmail() {
  const email = document.getElementById("contactEmail").textContent.trim();
  window.location.href = `mailto:${email}`;
}


/* ============================================================
   7. DOM-READY INIT
   ─ All DOM queries that were previously at the top level
     are now wrapped in DOMContentLoaded.

   FIX #3: Top-level DOM queries (header scroll, modal click-
   outside, IntersectionObservers, swipe listener, hamburger)
   previously ran as soon as the <script> tag was parsed.
   Although the <script> is at the bottom of <body> this is
   still fragile.  Wrapping in DOMContentLoaded is the correct
   pattern and removes the timing dependency entirely.
   ============================================================ */

document.addEventListener("DOMContentLoaded", () => {

  /* ── Sticky header shadow on scroll ── */
  const header = document.getElementById("siteHeader");
  if (header) {
    window.addEventListener("scroll", () => {
      header.classList.toggle("scrolled", window.scrollY > 8);
    }, { passive: true });
  }

  /* ── Close modal when clicking the dark overlay backdrop ── */
  const modal = document.getElementById("propertyModal");
  if (modal) {
    modal.addEventListener("click", function (e) {
      if (e.target === this) closeModal();
    });
  }

  /* ── Keyboard arrow navigation for the carousel ── */
  document.addEventListener("keydown", e => {
    const isOpen = document.getElementById("propertyModal")?.classList.contains("open");
    if (!isOpen) return;
    if (e.key === "ArrowLeft")  carouselMove(-1);
    if (e.key === "ArrowRight") carouselMove(1);
    if (e.key === "Escape")     closeModal();
  });

  /* ── Touch swipe support on the modal carousel ── */
  const carouselEl = document.getElementById("modalCarousel");
  if (carouselEl) {
    let startX = 0;
    carouselEl.addEventListener("touchstart", e => {
      startX = e.touches[0].clientX;
    }, { passive: true });
    carouselEl.addEventListener("touchend", e => {
      const diff = startX - e.changedTouches[0].clientX;
      if (Math.abs(diff) > 40) carouselMove(diff > 0 ? 1 : -1);
    });
  }

  /* ── Scroll-reveal: fade in sections marked with .reveal ── */
  const revealIO = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        revealIO.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08, rootMargin: "0px 0px -40px 0px" });

  document.querySelectorAll(".reveal").forEach(el => revealIO.observe(el));

  /* ── Stagger-reveal: animate direct children of .stagger containers ── */
  const staggerIO = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        Array.from(entry.target.children).forEach((child, i) => {
          setTimeout(() => {
            child.style.opacity   = "1";
            child.style.transform = "none";
          }, i * 90);
        });
        staggerIO.unobserve(entry.target);
      }
    });
  }, { threshold: 0.05 });

  document.querySelectorAll(".stagger").forEach(el => staggerIO.observe(el));

  /* ── Close mobile nav when any nav-link is clicked ── */
  document.querySelectorAll(".nav-link").forEach(link => {
    link.addEventListener("click", () => {
      document.querySelector(".nav-menu")?.classList.remove("open");
    });
  });

  /* ── Set initial hamburger visibility ── */
  updateHamburger();
});


/* ============================================================
   8. HAMBURGER / MOBILE NAV
   ─ updateHamburger() is called on DOMContentLoaded and on
     every resize to show/hide the ☰ button.
   ============================================================ */

/** Toggle the mobile nav drawer open/closed. */
function toggleNav() {
  document.querySelector(".nav-menu")?.classList.toggle("open");
}

/** Show the hamburger button below 680 px, hide it above. */
function updateHamburger() {
  const btn = document.getElementById("hamburgerBtn");
  if (btn) btn.style.display = window.innerWidth <= 680 ? "flex" : "none";
}

window.addEventListener("resize", updateHamburger);


/* ============================================================
   9. ANNOUNCEMENT POPUP  (Django template block)
   ─ Uses sessionStorage so the popup only appears once per
     browser session, not on every page load.
   ─ The {% if %} / {% endif %} block ensures this code is
     completely omitted from the page when there is no active
     announcement.
   ============================================================ */