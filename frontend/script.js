const state = { page: 1, limit: 12 };

const $ = (id) => document.getElementById(id);

async function loadStats() {
    const data = await fetch("/api/stats").then(r => r.json());
    $("stats").innerHTML = `
        <div class="stat">Total movies<strong>${data.total_movies}</strong></div>
        <div class="stat">Average rating<strong>${data.average_rating ?? "N/A"}</strong></div>
        <div class="stat">Latest year<strong>${data.latest_year ?? "N/A"}</strong></div>
    `;
}

async function loadGenres() {
    const genres = await fetch("/api/genres").then(r => r.json());
    $("genre").innerHTML = '<option value="">All genres</option>' +
        genres.map(g => `<option value="${escapeHtml(g)}">${escapeHtml(g)}</option>`).join("");
}

function escapeHtml(value) {
    return String(value ?? "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
}

function placeholder(title) {
    return `https://placehold.co/500x750/161b22/e6edf3?text=${encodeURIComponent(title)}`;
}

async function loadMovies() {
    const params = new URLSearchParams({
        page: state.page,
        limit: state.limit,
        sort: $("sort").value
    });

    const search = $("search").value.trim();
    const genre = $("genre").value;
    const year = $("year").value;
    const minRating = $("minRating").value;

    if (search) params.set("search", search);
    if (genre) params.set("genre", genre);
    if (year) params.set("year", year);
    if (minRating) params.set("min_rating", minRating);

    const movies = await fetch(`/api/movies?${params}`).then(r => r.json());
    $("resultText").textContent = `${movies.length} movie(s) shown`;
    $("pageText").textContent = `Page ${state.page}`;
    $("prevBtn").disabled = state.page === 1;
    $("nextBtn").disabled = movies.length < state.limit;

    $("movieGrid").innerHTML = movies.map(movie => `
        <article class="card" onclick="showMovie(${movie.id})">
            <img class="poster"
                 src="${escapeHtml(movie.poster_url || placeholder(movie.title))}"
                 alt="${escapeHtml(movie.title)}"
                 onerror="this.src='${placeholder(movie.title)}'">
            <div class="card-body">
                <h3>${escapeHtml(movie.title)}</h3>
                <div class="meta">${movie.year ?? "Year N/A"} • ${escapeHtml(movie.genre || "Genre N/A")}</div>
                <div class="rating">⭐ ${movie.rating ?? "N/A"}</div>
            </div>
        </article>
    `).join("") || "<p>No movies found.</p>";
}

async function showMovie(id) {
    const movie = await fetch(`/api/movies/${id}`).then(r => r.json());
    $("modalContent").innerHTML = `
        <h2>${escapeHtml(movie.title)}</h2>
        <p class="meta">${movie.year ?? "N/A"} • ${escapeHtml(movie.genre || "N/A")} • ⭐ ${movie.rating ?? "N/A"}</p>
        <p><strong>Director:</strong> ${escapeHtml(movie.director || "N/A")}</p>
        <p><strong>Cast:</strong> ${escapeHtml(movie.cast || "N/A")}</p>
        <p><strong>Runtime:</strong> ${escapeHtml(movie.runtime || "N/A")}</p>
        <p class="description">${escapeHtml(movie.description || "No description available.")}</p>
        ${movie.source_url ? `<p><a class="docs" target="_blank" href="${escapeHtml(movie.source_url)}">View source ↗</a></p>` : ""}
    `;
    $("modal").classList.remove("hidden");
}

$("searchBtn").addEventListener("click", () => { state.page = 1; loadMovies(); });
$("sort").addEventListener("change", () => { state.page = 1; loadMovies(); });
$("genre").addEventListener("change", () => { state.page = 1; loadMovies(); });
$("prevBtn").addEventListener("click", () => { if (state.page > 1) { state.page--; loadMovies(); } });
$("nextBtn").addEventListener("click", () => { state.page++; loadMovies(); });
$("resetBtn").addEventListener("click", () => {
    $("search").value = "";
    $("genre").value = "";
    $("year").value = "";
    $("minRating").value = "";
    $("sort").value = "title_asc";
    state.page = 1;
    loadMovies();
});
$("closeModal").addEventListener("click", () => $("modal").classList.add("hidden"));
$("modal").addEventListener("click", (e) => {
    if (e.target === $("modal")) $("modal").classList.add("hidden");
});

loadStats();
loadGenres();
loadMovies();
