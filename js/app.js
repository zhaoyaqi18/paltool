/* ===== App - Main Entry Point ===== */
(async function () {
  // --- State ---
  let state = {
    loaded: false,
    currentResult: null,
    currentTargetId: null
  };

  // --- DOM refs ---
  const $searchInput = document.getElementById('search-input');
  const $searchBtn = document.getElementById('search-btn');
  const $dropdown = document.getElementById('dropdown');
  const $resultSection = document.getElementById('result-section');
  const $resultContainer = document.getElementById('result-container');
  const $loader = document.getElementById('loader');
  const $welcome = document.getElementById('hero');
  const $features = document.getElementById('features');

  // --- Load data ---
  try {
    await PalData.load();
    await Breeder.load();
    Collection.load();
    // Load passives
    try {
      const pr = await fetch('passives.json');
      window._passives = await pr.json();
    } catch(e) { window._passives = []; }
    state.loaded = true;
    console.log(`Loaded ${PalData.getTotal()} pals, ${Breeder.isLoaded() ? 'breed data ready' : 'breed data failed'}.`);

    // Show My Box button
    updateMyBox();
  } catch (e) {
    console.error('Data load failed:', e);
    $welcome.innerHTML = `<div class="error-banner" style="margin:40px auto;max-width:600px;text-align:center;padding:20px;">
      <h3>Data load failed</h3>
      <p>${e.message}</p>
      <p style="margin-top:12px;font-size:13px;color:var(--text-dim);">
        Make sure you access via <code>http://localhost:8765</code>, not by opening the HTML file directly.<br>
        Then press Ctrl+Shift+R to force refresh.
      </p>
    </div>`;
    $searchInput.disabled = false;
    $searchInput.placeholder = 'Data load failed, refresh and try again...';
    return;
  }

  // --- Enable search ---
  $searchInput.disabled = false;
  $searchBtn.disabled = false;
  $searchInput.placeholder = 'Search by Pal name or number...';

  // --- Search input ---
  $searchInput.addEventListener('input', () => {
    const query = $searchInput.value;
    if (query.length < 1) {
      $dropdown.innerHTML = '';
      return;
    }
    const results = PalData.search(query);
    Renderer.renderDropdown(results, $searchInput, $dropdown, selectPal);
  });

  // Close dropdown on outside click
  document.addEventListener('click', (e) => {
    if (!$dropdown.contains(e.target) && e.target !== $searchInput) {
      $dropdown.innerHTML = '';
    }
  });

  // --- Search button ---
  $searchBtn.addEventListener('click', () => {
    const query = $searchInput.value.trim();
    if (!query) return;

    const results = PalData.search(query);
    if (results.length === 0) {
      $resultSection.classList.remove('hidden');
      $resultContainer.innerHTML = '<div class="no-route"><h3>Pal Not Found</h3><p>Check the name or number and try again.</p></div>';
      return;
    }

    selectPal(results[0].id);
  });

  // --- Enter key ---
  $searchInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') {
      const query = $searchInput.value.trim();
      if (!query) return;

      const results = PalData.search(query);
      if (results.length > 0) {
        selectPal(results[0].id);
      }
      $dropdown.innerHTML = '';
    }
  });

  // --- Select pal ---
  function selectPal(palId) {
    state.currentTargetId = palId;

    // Update hash
    Share.setHash(palId);

    // Hide welcome, features, show loader
    $welcome.classList.add('hidden');
    $features?.classList.add('hidden');
    $resultSection.classList.remove('hidden');
    $resultContainer.innerHTML = '';
    $loader.classList.remove('hidden');

    // Show route tabs (moved outside topbar)
    document.querySelectorAll('.route-tabs').forEach(el => el.classList.remove('hidden'));

    // Small delay to allow browser to repaint
    setTimeout(() => {
      const result = Breeder.findRoutes(palId);
      state.currentResult = result;

      $loader.classList.add('hidden');

      if (result.error && result.routes.length === 0) {
        $resultContainer.innerHTML = `
          <div class="no-route">
            <h3>No Breeding Route Found</h3>
            <p>${result.error}</p>
          </div>`;
        return;
      }

      Renderer.renderRoute(result, 'result-container');

      // Render SVG tree after DOM update
      if (result.routes.length > 0 && result.routes[0].type === 'breed') {
        setTimeout(() => Renderer.renderTreeSVG(result.routes[0]), 100);
      }
    }, 50);
  }

  // --- Hash routing (restore from URL) ---
  function restoreFromHash() {
    const parsed = Share.parseHash();
    if (parsed.q) {
      // Try to find pal by id or name
      let pal = PalData.getById(parsed.q);
      if (!pal) {
        const results = PalData.search(parsed.q);
        if (results.length > 0) pal = results[0];
      }
      if (pal) {
        $searchInput.value = `#${pal.dex} ${pal.name}`;
        selectPal(pal.id);
      }
    }
  }

  // --- Reset to search ---
  function resetSearch() {
    state.currentResult = null;
    state.currentTargetId = null;
    $searchInput.value = '';
    $searchInput.focus();
    $welcome.classList.remove('hidden');
    $features?.classList.remove('hidden');
    $resultSection.classList.add('hidden');
    $resultContainer.innerHTML = '';
    Share.clearHash();
    document.getElementById('topbar')?.classList.add('hidden');
    // Hide route tabs
    document.getElementById('route-tabs')?.classList.add('hidden');
    document.getElementById('route-tabs')?.classList.remove('act');
    // Clear topbar route tabs
    const rt = document.getElementById('route-tabs');
    if (rt) rt.innerHTML = '';
    window._lastResult = null;
  }

  // Logo click → back to search
  document.querySelector('.logo')?.addEventListener('click', (e) => {
    e.preventDefault();
    resetSearch();
  });

  // Expose for renderer button binding
  window.resetSearchFn = resetSearch;

  // --- My Box ---
  function updateMyBox() {
    const btn = document.getElementById('mybox-btn');
    const cnt = document.getElementById('mybox-count');
    if (!btn || !cnt) return;
    const n = Collection.count();
    cnt.textContent = n;
    btn.classList.toggle('hidden', n === 0 && !state.currentResult);
  }
  window.updateMyBox = updateMyBox;
  window.addToCollection = function(palId) {
    if (Collection.add(palId)) updateMyBox();
  };

  document.getElementById('mybox-btn')?.addEventListener('click', () => {
    Renderer.renderCollection();
  });

  Share.onHashChange((parsed) => {
    if (parsed.q) {
      let pal = PalData.getById(parsed.q);
      if (!pal) {
        const results = PalData.search(parsed.q);
        if (results.length > 0) pal = results[0];
      }
      if (pal && pal.id !== state.currentTargetId) {
        $searchInput.value = `#${pal.dex} ${pal.name}`;
        selectPal(pal.id);
      }
    }
  });

  // Init
  restoreFromHash();
})();
