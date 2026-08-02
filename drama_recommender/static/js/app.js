const cardsEl = document.getElementById("cards");
const loadingEl = document.getElementById("loading");
const errorPanelEl = document.getElementById("error-panel");
const errorMessageEl = document.getElementById("error-message");
const refreshBtn = document.getElementById("refresh-btn");
const retryBtn = document.getElementById("retry-btn");
const statusBadge = document.getElementById("status-badge");
const metaLine = document.getElementById("meta-line");

function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function formatDate(isoString) {
  if (!isoString) return "Unknown time";
  const date = new Date(isoString);
  return date.toLocaleString();
}

function setLoading(isLoading) {
    loadingEl.classList.toggle("hidden", !isLoading);
    refreshBtn.disabled = isLoading;
    if (isLoading) {
      cardsEl.classList.add("hidden");
    } else {
      cardsEl.classList.remove("hidden");
    }
}

function showError(message) {
  errorPanelEl.classList.remove("hidden");
  errorMessageEl.textContent = message;
}

function hideError() {
  errorPanelEl.classList.add("hidden");
}

function updateStatus(data) {
  statusBadge.classList.remove("live", "fallback");

  if (data.is_fallback) {
    statusBadge.textContent = "Offline fallback list";
    statusBadge.classList.add("fallback");
  } else {
    statusBadge.textContent = "Live from YouTube";
    statusBadge.classList.add("live");
  }

  const cacheNote = data.cached ? " (cached)" : "";
  metaLine.textContent = `${data.source}${cacheNote} - Updated ${formatDate(data.fetched_at)}`;
}

function placeholderThumb() {
  return "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='640' height='360' viewBox='0 0 640 360'%3E%3Crect width='640' height='360' fill='%2315121d'/%3E%3Ctext x='50%25' y='50%25' fill='%23b6adc8' font-family='Arial' font-size='24' text-anchor='middle' dominant-baseline='middle'%3EDrama%3C/text%3E%3C/svg%3E";
}

function renderCards(items) {
  cardsEl.innerHTML = items
    .map((item, index) => {
      const thumb = item.thumbnail || placeholderThumb();
      return `
        <article class="card">
          <div class="card-thumb-wrap">
            <span class="rank-badge">#${index + 1}</span>
            <img class="card-thumb" src="${escapeHtml(thumb)}" alt="${escapeHtml(item.title)}" loading="lazy">
          </div>
          <div class="card-body">
            <h2 class="card-title">${escapeHtml(item.title)}</h2>
            <div class="card-meta">
              <span>Channel: ${escapeHtml(item.channel)}</span>
              <span>Views: ${escapeHtml(item.views)}</span>
            </div>
            <a class="card-link" href="${escapeHtml(item.url)}" target="_blank" rel="noopener noreferrer">
              Watch on YouTube
            </a>
          </div>
        </article>
      `;
    })
    .join("");
}

async function loadRecommendations(refresh = false) {
  hideError();
  setLoading(true);
  cardsEl.innerHTML = "";

  try {
    const url = refresh ? "/api/recommendations?refresh=1" : "/api/recommendations";
    const response = await fetch(url);

    if (!response.ok) {
      throw new Error(`Server returned ${response.status}`);
    }

    const data = await response.json();
    updateStatus(data);
    renderCards(data.items || []);
  } catch (error) {
    showError(error.message || "Something went wrong while loading recommendations.");
  } finally {
    setLoading(false);
  }
}

refreshBtn.addEventListener("click", () => loadRecommendations(true));
retryBtn.addEventListener("click", () => loadRecommendations(true));

loadRecommendations(false);
