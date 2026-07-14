/* ===== Reverse Breeding Algorithm v6 - Official Game Data ===== */
const Breeder = (() => {
  const MAX_DEPTH = 5;
  const MAX_ROUTES = 10;

  // Breed data loaded from breed_data.json
  // f: { "parent1|parent2": "child_id" } - forward lookup
  // r: { "child_id": [["p1","p2"], ...] } - reverse lookup
  let breedData = null;

  const SPECIAL_BREEDS = {
    orserk: { parents: ['grizzbolt', 'relaxaurus'], note: 'Grizzbolt + Relaxaurus = Orserk' },
    frostallion_noct: { parents: ['frostallion', 'helzephyr'], note: 'Frostallion + Helzephyr = Frostallion Noct' },
  };

  async function load() {
    const resp = await fetch('breed_data.json');
    breedData = await resp.json();
    return true;
  }

  function isLoaded() { return breedData !== null; }

  function getChild(parentAId, parentBId) {
    if (!breedData) return null;
    const key = [parentAId, parentBId].sort().join('|');
    return breedData.f[key] || null;
  }

  function findRoutes(targetPalId, maxDepth = MAX_DEPTH) {
    if (!breedData) return { error: 'Breed data not loaded.' };

    const target = PalData.getById(targetPalId);
    if (!target) return { error: `Pal "${targetPalId}" not found.` };

    // Check special breeds
    if (SPECIAL_BREEDS[target.id]) {
      const s = SPECIAL_BREEDS[target.id];
      return { target, routes: [{ type: 'special', steps: s.parents.map(p => PalData.getById(p)).filter(Boolean), note: s.note }], total: 1 };
    }

    // For wild-catchable Pals, still compute breeding routes but
    // filter out routes that use the target as a parent (circular)
    const showWildFallback = target.isWild;

    const reverse = breedData.r[targetPalId] || [];
    if (reverse.length === 0) {
      if (target.isWild) {
        return { target, routes: [{ type: 'wild', pal: target, note: 'Can be caught directly in the wild (no breeding route found)' }], total: 1 };
      }
      return { target, routes: [], total: 0, error: 'No breeding route found for this Pal.' };
    }

    const results = [];

    function allWild(tree) {
      if (!tree.left && !tree.right) return tree.leafWild === true;
      return allWild(tree.left) && allWild(tree.right);
    }

    function tkey(t) {
      if (!t.left && !t.right) return `W${t.bp}`;
      return `N${t.bp}(${tkey(t.left)},${tkey(t.right)})`;
    }

    function tdepth(t) {
      if (!t.left || !t.right) return 0;
      return 1 + Math.max(tdepth(t.left), tdepth(t.right));
    }

    function dfs(targetId, depth, visited) {
      const target = PalData.getById(targetId);
      if (!target) return null;
      const bp = target.bp;

      if (depth > 0 && target.isWild) return { bp, palId: targetId, leafWild: true };
      if (depth >= maxDepth) return null;

      const parentPairs = breedData.r[targetId] || [];
      let best = null;

      for (const [aId, bId] of parentPairs) {
        if (results.length >= MAX_ROUTES * 3) break;
        const key = `${targetId}|${aId},${bId}`;
        if (visited.has(key)) continue;
        visited.add(key);

        const aPal = PalData.getById(aId);
        const bPal = PalData.getById(bId);
        if (!aPal || !bPal) continue;

        const left = dfs(aId, depth + 1, new Set(visited));
        if (!left) continue;
        const right = dfs(bId, depth + 1, new Set(visited));
        if (!right) continue;

        const tree = { bp, palId: targetId, left, right };
        if (!best) best = tree;
        if (allWild(tree)) results.push(tree);
      }
      return best;
    }

    dfs(targetPalId, 0, new Set());

    // Deduplicate and sort
    const seen = new Set();
    const uniq = [];
    for (const t of results) {
      const k = tkey(t);
      if (!seen.has(k)) { seen.add(k); uniq.push(t); }
    }
    uniq.sort((a, b) => tdepth(a) - tdepth(b));

    // Filter out routes that use the target as a parent (circular)
    function hasTargetAsLeaf(node, targetId) {
      if (!node.left && !node.right) return node.palId === targetId;
      if (node.left && hasTargetAsLeaf(node.left, targetId)) return true;
      if (node.right && hasTargetAsLeaf(node.right, targetId)) return true;
      return false;
    }
    const filtered = showWildFallback
      ? uniq.filter(t => !hasTargetAsLeaf(t, targetPalId))
      : uniq;

    const selectedTrees = filtered.length > 0 ? filtered.slice(0, MAX_ROUTES) : [];

    if (selectedTrees.length > 0) {
      return { target, routes: selectedTrees.map((t, i) => ({ type: 'breed', routeIndex: i + 1, steps: treeToSteps(t, target), tree: t })), total: selectedTrees.length };
    }

    if (showWildFallback) {
      return { target, routes: [{ type: 'wild', pal: target, note: 'Can be caught directly in the wild' }], total: 1 };
    }

    return { target, routes: [], total: 0, error: 'No breeding route found within ' + maxDepth + ' generations.' };
  }

  function treeToSteps(tree, targetPal) {
    const steps = [];
    function walk(node) {
      if (!node.left || !node.right) return;
      if (node.left.left || node.left.right) walk(node.left);
      if (node.right.left || node.right.right) walk(node.right);

      const leftP = PalData.getById(node.left.palId) || PalData.getNonVariantByBP(node.left.bp) || { name: '?', id: '?' };
      const rightP = PalData.getById(node.right.palId) || PalData.getNonVariantByBP(node.right.bp) || { name: '?', id: '?' };
      const childP = PalData.getNonVariantByBP(node.bp) || { name: '?', id: '?' };

      steps.push({ leftParent: leftP, rightParent: rightP, leftIsWild: node.left.leafWild === true, rightIsWild: node.right.leafWild === true, childPal: childP, childBP: node.bp });
    }

    if (tree.left && tree.right) walk(tree);
    if (steps.length > 0) steps[steps.length - 1].childPal = targetPal;
    return steps;
  }

  return { load, isLoaded, getChild, findRoutes, SPECIAL_BREEDS };
})();
