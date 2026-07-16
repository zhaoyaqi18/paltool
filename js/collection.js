/* ===== Collection — My Pal Box ===== */
const Collection = (() => {
  const STORAGE_KEY = 'paltool_collection';

  let _pals = [];

  function load() {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      _pals = raw ? JSON.parse(raw) : [];
    } catch (e) { _pals = []; }
    return _pals;
  }

  function save() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(_pals));
  }

  function add(palId) {
    if (_pals.includes(palId)) return false;
    _pals.push(palId);
    save();
    return true;
  }

  function remove(palId) {
    const idx = _pals.indexOf(palId);
    if (idx === -1) return false;
    _pals.splice(idx, 1);
    save();
    return true;
  }

  function has(palId) { return _pals.includes(palId); }

  function getAll() { return [..._pals]; }

  function count() { return _pals.length; }

  function clear() { _pals = []; save(); }

  // Find what target pals can be bred from collected parents
  function whatCanIBreed() {
    if (_pals.length < 2) return [];
    const result = [];
    const allPals = PalData.getAll();
    for (const pal of allPals) {
      if (_pals.includes(pal.id)) continue;
      const routes = Breeder.findRoutes(pal.id, 1); // Only direct (depth 1)
      if (!routes || !routes.routes) continue;
      for (const r of routes.routes) {
        if (r.type !== 'breed' || !r.steps || r.steps.length === 0) continue;
        const s = r.steps[0];
        const lpid = s.leftParent ? s.leftParent.id : null;
        const rpid = s.rightParent ? s.rightParent.id : null;
        if (lpid && rpid && _pals.includes(lpid) && _pals.includes(rpid)) {
          result.push({ pal, left: s.leftParent, right: s.rightParent });
          break;
        }
      }
    }
    return result;
  }

  return { load, add, remove, has, getAll, count, clear, whatCanIBreed };
})();
