/* ===== Data Layer ===== */
const PalData = (() => {
  let pals = [];
  let palsById = {};
  let palsByBP = {};  // BP → pals[]
  let bpSet = new Set();
  let sortedBPs = [];
  let wildPals = [];

  const ELEMENT_CLASS = {
    neutral: 'elem-neutral', fire: 'elem-fire', water: 'elem-water',
    grass: 'elem-grass', electric: 'elem-electric', ice: 'elem-ice',
    ground: 'elem-ground', dark: 'elem-dark', dragon: 'elem-dragon'
  };

  async function load() {
    const resp = await fetch('/pals.json');
    pals = await resp.json();
    buildIndices();
    return pals;
  }

  function buildIndices() {
    palsById = {};
    palsByBP = {};
    bpSet = new Set();
    wildPals = [];

    for (const p of pals) {
      palsById[p.id] = p;
      if (!palsByBP[p.bp]) palsByBP[p.bp] = [];
      palsByBP[p.bp].push(p);
      bpSet.add(p.bp);
      if (p.isWild) wildPals.push(p);
    }

    sortedBPs = [...bpSet].sort((a, b) => b - a);
  }

  function search(query) {
    if (!query || query.trim() === '') return [];
    const q = query.toLowerCase().trim();
    return pals.filter(p =>
      (p.name.toLowerCase().includes(q) ||
      p.id.toLowerCase().includes(q) ||
      String(p.dex) === q) &&
      p.dex < 10000  // Exclude special crossover pals
    ).slice(0, 20);
  }

  function getById(id) { return palsById[id] || null; }

  function getByBP(bp) { return palsByBP[bp] || []; }

  function getBPRange(min, max) {
    return pals.filter(p => p.bp >= min && p.bp <= max);
  }

  function getSortedBPs() { return sortedBPs; }

  function getWildPals() { return wildPals; }

  function getBPSet() { return bpSet; }

  function getTotal() { return pals.length; }

  function getAll() { return pals; }

  function getNonVariantByBP(bp) {
    const candidates = palsByBP[bp] || [];
    // Prefer non-variant with wild catch; then non-variant; then any
    const sorted = [...candidates].sort((a, b) => {
      const aScore = (a.isVariant ? 2 : 0) - (a.isWild ? 1 : 0);
      const bScore = (b.isVariant ? 2 : 0) - (b.isWild ? 1 : 0);
      return aScore - bScore;
    });
    return sorted[0] || null;
  }

  function getElementClass(element) { return ELEMENT_CLASS[element] || 'elem-neutral'; }

  function elementBadgeHTML(p, size = 'normal') {
    const cls = ELEMENT_CLASS[p.element] || 'elem-neutral';
    const cls2 = p.element2 ? (ELEMENT_CLASS[p.element2] || 'elem-neutral') : '';
    let html = `<span class="element-badge ${cls}">${p.element}</span>`;
    if (p.element2) {
      html += ` <span class="element-badge ${cls2}">${p.element2}</span>`;
    }
    return html;
  }

  return { load, search, getById, getByBP, getBPRange, getSortedBPs, getWildPals, getBPSet, getTotal, getAll, getNonVariantByBP, getElementClass, elementBadgeHTML };
})();
