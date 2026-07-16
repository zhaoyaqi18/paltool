/* ===== Renderer - Profile + Steps Layout ===== */
const Renderer = (() => {
  function pimg(pal, sz = 48) {
    const u = pal.image || '';
    const i = pal.name ? pal.name.charAt(0).toUpperCase() : '?';
    return `<div class="pthumb" style="width:${sz}px;height:${sz}px">
      <img src="${u}" alt="${pal.name}" loading="lazy" onerror="this.parentElement.classList.add('pfail');this.style.display='none'" onload="this.parentElement.classList.add('plod')">
      <span class="pthumb-fb"><span class="pthumb-letter">${i}</span></span>
    </div>`;
  }

  function renderRoute(result, cid, ri = 0) {
    const c = document.getElementById(cid);
    if (!c) return;
    if (!result || !result.routes || result.routes.length === 0) {
      c.innerHTML = `<div class="estate"><h3>No Route Found</h3><p>${result.error || 'Try another Pal.'}</p></div>`;
      return;
    }
    const r = result.routes[ri];
    const t = result.target;
    let h = '';
    h += topBar(t);
    document.getElementById('topbar')?.classList.remove('hidden');
    if (result.routes.length > 1) { window._lastResult = result; sw(result, ri); }
    h += '<div class="rcols">';
    h += '<div class="rcol-l">' + profile(t, r) + '</div>';
    h += '<div class="rcol-r">' + (ri === 0 && r.type === 'breed' ? bestBanner(r) : '') + steps(r) + infoSection(r) + passivesSection(t) + '</div>';
    h += '</div>';
    c.innerHTML = h;
    bindActs();
  }

  function topBar(t) {
    return `<div class="rbar"><div class="rbar-l"><span class="rbar-lbl">Breeding</span><strong>${t ? t.name : ''}</strong></div><div class="rbar-r"><button id="bk-btn" class="bk-btn">← Back</button><button id="card-btn" class="bk-btn" title="Download share card">📷</button><button id="su-btn" class="bk-btn" title="Copy share link">🔗</button></div></div>`;
  }

  /* ===== Profile Card ===== */
  function profile(t, r) {
    if (!t) return '';
    const n = r.type === 'wild' ? 0 : r.type === 'special' ? 1 : (r.steps ? r.steps.length : 0);
    const tp = r.type === 'wild' ? 'Wild Capture' : r.type === 'special' ? 'Special Combo' : 'Breeding';
    const diff = n <= 1 ? 'Easy' : n <= 3 ? 'Medium' : 'Hard';
    const works = t.work || {};
    const workList = Object.keys(works).length ? Object.entries(works).map(([k,v]) => `${k} Lv${v}`).join(', ') : '';
    const egg = t.egg || '';
    const food = t.food || 7;
    const inBox = Collection.has(t.id);
    return `
      <div class="profile">
        <div class="profile-card">
          <div class="profile-main">
            <div class="profile-left">
              <div class="profile-img">${pimg(t, 120)}</div>
              <div class="profile-tags">${PalData.elementBadgeHTML(t)}</div>
              <div class="profile-name">#${t.dex} ${t.name}</div>
              <div class="profile-bp">BP: ${t.bp}</div>
            </div>
            <div class="profile-right">
              <div class="profile-stats-panel">
                <div class="pstat"><span class="psl">STEPS</span><span class="psv">${n}</span></div>
                <div class="pstat"><span class="psl">EGG</span><span class="psv">${egg}</span></div>
                <div class="pstat"><span class="psl">FOOD</span><span class="psv">${food}</span></div>
                <div class="pstat"><span class="psl">DIFFICULTY</span><span class="psv ${diff.toLowerCase()}">${diff}</span></div>
              </div>
            </div>
          </div>
          <div class="profile-footer">
            ${workList ? `<div class="profile-works">🔧 ${workList}</div>` : ''}
            ${t.isWild ? '<div class="profile-wild">✅ Found in the wild</div>' : ''}
            <div class="profile-tip">Each egg needs 1 Cake. ~10 eggs per step for desired passives.</div>
            <button class="addbox-btn" onclick="window.addToCollection('${t.id}');this.textContent='✅ In Box';this.classList.add('inbox')" ${inBox ? 'disabled style="opacity:0.5;cursor:default"' : ''}>${inBox ? '✅ In Box' : '📦 Add to Box'}</button>
          </div>
        </div>
      </div>`;
  }

  /* ===== Right Top: Breeding Steps ===== */
  function steps(r) {
    if (r.type === 'wild') return `<div class="estate"><h3>No Breeding Needed</h3><p>${r.note}</p></div>`;
    if (r.type === 'special') {
      return `<div class="slist"><div class="scard"><div class="spars">${r.steps.map(p =>
        `<div class="spal">${pimg(p, 60)}<div><div class="stags">${PalData.elementBadgeHTML(p)}</div><div class="sn">${p.name}</div></div></div>`
      ).join('')}</div></div></div>`;
    }
    if (!r.steps || r.steps.length === 0) return '';
    let h = '<div class="slist">';
    r.steps.forEach((s, i) => {
      const cn = s.childPal ? s.childPal.name : '?';
      h += `
        <div class="scard">
          <div class="srow">
            <div class="spal clickable" onclick="window.location.hash='q=${s.leftParent.id}'">${pimg(s.leftParent, 76)}
              <div class="stags">${PalData.elementBadgeHTML(s.leftParent)}</div>
              <div class="sn">${s.leftParent.name}</div>
              ${s.leftIsWild ? '<span class="st">Wild</span>' : ''}
            </div>
            <div class="sop">+</div>
            <div class="spal clickable" onclick="window.location.hash='q=${s.rightParent.id}'">${pimg(s.rightParent, 76)}
              <div class="stags">${PalData.elementBadgeHTML(s.rightParent)}</div>
              <div class="sn">${s.rightParent.name}</div>
              ${s.rightIsWild ? '<span class="st">Wild</span>' : ''}
            </div>
            <div class="sop">=</div>
            <div class="spal">${pimg(s.childPal, 76)}
              <div class="stags">${PalData.elementBadgeHTML(s.childPal)}</div>
              <div class="sn">${cn}</div>
            </div>
          </div>
          <div class="sbp">floor((${s.leftParent.bp}+${s.rightParent.bp}+1)/2) = <strong>${s.childBP}</strong></div>
        </div>`;
    });
    h += '</div>';
    return h;
  }

  /* ===== Right Bottom: Info ===== */
  function infoSection(r) {
    if (!r.steps || r.steps.length === 0) return '';
    let wildCount = 0;
    r.steps.forEach(s => {
      if (s.leftIsWild) wildCount++;
      if (s.rightIsWild) wildCount++;
    });
    const steps = r.steps.length;
    const eggs = steps * 10;
    let h = '<div class="info">';
    h += '<div class="info-grid">';
    h += `<div class="info-item"><span class="il">Steps</span><span class="iv">${steps}</span></div>`;
    h += `<div class="info-item"><span class="il">Est. Eggs</span><span class="iv">~${eggs}</span></div>`;
    h += `<div class="info-item"><span class="il">Wild</span><span class="iv">${wildCount}</span></div>`;
    h += `<div class="info-item"><span class="il">Cakes</span><span class="iv">~${eggs}</span></div>`;
    h += '</div>';
    h += '</div>';
    return h;
  }

  /* ===== Passives Section ===== */
  function passivesSection(t) {
    if (!t || !window._passives) return '';
    const el = t.element || 'neutral';
    const bps = window._passives || [];

    // Recommend based on element + generic combat/worker
    const combat = bps.filter(p => p.type === 'combat').slice(0, 6);
    const worker = bps.filter(p => p.type === 'worker').slice(0, 4);
    const elem = bps.filter(p => p.type === 'element' && p.id.includes(el.substring(0,4))).slice(0, 2);
    const all = [...combat.slice(0, 4), ...elem, ...worker.slice(0, 2)].slice(0, 8);

    if (all.length === 0) return '';

    let h = '<div class="passives-section"><h4>🎯 Recommended Passives</h4><div class="passives-grid">';
    for (const p of all) {
      const rcls = 'rarity-' + (p.rarity || 'uncommon');
      h += `<span class="passive-tag ${rcls}" title="${p.effect}">${p.name}</span>`;
    }
    h += '</div>';
    h += '<p class="passives-hint">Parent passives can be inherited by offspring. Breed parents with desired passives to pass them down.</p>';
    h += '</div>';
    return h;
  }

  /* ===== Best Route Banner ===== */
  function bestBanner(r) {
    if (!r.steps || r.steps.length === 0) return '';
    let wild = 0;
    r.steps.forEach(s => { if (s.leftIsWild) wild++; if (s.rightIsWild) wild++; });
    return `<div class="best-banner">⭐ Best Route — ${r.steps.length} generation${r.steps.length>1?'s':''}, ${wild} wild catch${wild>1?'es':''} needed</div>`;
  }

  /* ===== Share & Tabs ===== */
  function share() {
    return `<div class="sbar"><button id="su-btn">🔗 Copy Link</button></div>`;
  }
  function sw(res, idx) {
    document.querySelectorAll('.route-tabs').forEach(el => {
      el.innerHTML = res.routes.map((r, i) => {
        let label = `Route ${i+1}`;
        if (r.type === 'breed' && r.steps && r.steps.length > 0) {
          const s = r.steps[0];
          label = `${s.leftParent ? s.leftParent.name : '?'} + ${s.rightParent ? s.rightParent.name : '?'}`;
        } else if (r.type === 'wild') label = 'Wild Capture';
        else if (r.type === 'special') label = 'Special Combo';
        const act = i === idx ? ' act' : '';
        const best = (i === 0 && r.type === 'breed') ? '⭐ ' : '';
        return `<button class="rtab${act}" data-r="${i}">${best}${label}</button>`;
      }).join('');
      el.classList.remove('hidden');
      el.querySelectorAll('.rtab').forEach(b => {
        b.addEventListener('click', () => {
          if (b.classList.contains('act')) return;
          document.querySelectorAll('.route-tabs .rtab').forEach(x => x.classList.remove('act'));
          b.classList.add('act');
          if (window._lastResult) Renderer.renderRoute(window._lastResult, 'result-container', parseInt(b.dataset.r));
        });
      });
    });
  }
  function bindActs() {
    const ub = document.getElementById('su-btn');
    if (ub) ub.addEventListener('click', () => {
      navigator.clipboard.writeText(Share.getShareURL()).then(() => { ub.textContent = '✅ Copied!'; setTimeout(() => { ub.textContent = '🔗 Copy Link'; }, 2000); });
    });
    document.getElementById('bk-btn')?.addEventListener('click', () => history.back());
    document.getElementById('card-btn')?.addEventListener('click', () => {
      if (window._lastResult) Share.generateCard(window._lastResult);
    });
  }

  function renderDropdown(pals, inputEl, containerEl, onSelect) {
    if (!pals || pals.length === 0) { containerEl.innerHTML = ''; return; }
    containerEl.innerHTML = pals.map(p =>
      `<div class="dropdown-item" data-id="${p.id}">${pimg(p, 28)}<span class="dex-num">#${p.dex}</span>${PalData.elementBadgeHTML(p)}<span>${p.name}</span></div>`
    ).join('');
    containerEl.querySelectorAll('.dropdown-item').forEach(item => {
      item.addEventListener('click', () => { onSelect(item.dataset.id); containerEl.innerHTML = ''; if (inputEl) inputEl.value = ''; });
    });
  }

  /* ===== Collection Panel ===== */
  function renderCollection() {
    const pals = Collection.getAll();
    const canBreed = Collection.whatCanIBreed();
    let h = '<div class="collection-overlay" onclick="this.remove()"><div class="collection-panel" onclick="event.stopPropagation()">';
    h += '<h3>📦 My Pal Box</h3>';
    if (pals.length === 0) {
      h += '<p class="collection-empty">No pals collected yet. Search a pal and click "Add to Box".</p>';
    } else {
      h += '<div class="collection-grid">';
      for (const pid of pals) {
        const p = PalData.getById(pid);
        if (!p) continue;
        h += `<div class="collection-item"><div class="collection-img">${pimg(p, 52)}</div><div class="collection-name">${p.name}</div><button class="collection-rm" onclick="Collection.remove('${pid}');window.updateMyBox();this.closest('.collection-item').remove()">✕</button></div>`;
      }
      h += '</div>';
    }
    if (canBreed.length > 0) {
      h += '<h4 style="margin-top:16px">🧬 You Can Breed:</h4><div class="collection-grid">';
      for (const {pal, left, right} of canBreed.slice(0, 12)) {
        h += `<div class="collection-item breedable" onclick="window.location.hash='q=${pal.id}'" title="${left.name} + ${right.name}">${pimg(pal, 44)}<div class="collection-name">${pal.name}</div></div>`;
      }
      h += '</div>';
    }
    h += '<button class="collection-close" onclick="this.closest(\'.collection-overlay\').remove()">Close</button>';
    h += '</div></div>';
    document.body.insertAdjacentHTML('beforeend', h);
  }

  return { renderRoute, renderTreeSVG: () => {}, renderDropdown, renderCollection };
})();
