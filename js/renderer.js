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
    // Two-column layout
    h += '<div class="rcols">';
    h += '<div class="rcol-l">' + profile(t, r) + '</div>';
    h += '<div class="rcol-r">' + steps(r) + infoSection(r) + '</div>';
    h += '</div>';
    c.innerHTML = h;
    bindActs();
  }

  function topBar(t) {
    return `<div class="rbar"><div class="rbar-l"><span class="rbar-lbl">Breeding</span><strong>${t ? t.name : ''}</strong></div><div class="rbar-r"><button id="bk-btn" class="bk-btn">← Back</button><button id="su-btn" class="bk-btn" title="Copy share link">🔗</button></div></div>`;
  }

  /* ===== Left: Pal Profile ===== */
  function profile(t, r) {
    if (!t) return '';
    const n = r.type === 'wild' ? 0 : r.type === 'special' ? 1 : (r.steps ? r.steps.length : 0);
    const tp = r.type === 'wild' ? 'Wild Capture' : r.type === 'special' ? 'Special Combo' : 'Breeding';
    const diff = n <= 1 ? 'Easy' : n <= 3 ? 'Medium' : 'Hard';
    // Work data
    const works = t.work || {};
    const workList = Object.keys(works).length ? Object.entries(works).map(([k,v]) => `${k} Lv${v}`).join(', ') : '';
    // Egg
    const egg = t.egg || '';
    const food = t.food || 7;
    return `
      <div class="profile">
        <div class="profile-img">${pimg(t, 120)}</div>
        <div class="profile-tags">${PalData.elementBadgeHTML(t)}</div>
        <div class="profile-name">#${t.dex} ${t.name}</div>
        <div class="profile-bp">BP: ${t.bp}</div>
        <div class="profile-stats">
          <div class="pstat"><span class="psl">Steps</span><span class="psv">${n}</span></div>
          <div class="pstat"><span class="psl">Egg</span><span class="psv" style="font-size:11px">${egg}</span></div>
          <div class="pstat"><span class="psl">Food</span><span class="psv">${food}</span></div>
          <div class="pstat"><span class="psl">Difficulty</span><span class="psv ${diff.toLowerCase()}">${diff}</span></div>
        </div>
        ${workList ? `<div class="profile-works">🔧 ${workList}</div>` : ''}
        ${t.isWild ? '<div class="profile-wild">✅ Found in the wild</div>' : ''}
        <div class="profile-tip">Each egg needs 1 Cake.<br>~10 eggs per step for desired passives.</div>
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

  /* ===== Share & Tabs ===== */
  function share() {
    return `<div class="sbar"><button id="su-btn">🔗 Copy Link</button></div>`;
  }
  function sw(res, idx) {
    const el = document.getElementById('route-tabs');
    if (!el) return;
    el.innerHTML = res.routes.map((r, i) => {
      let label = `Route ${i+1}`;
      if (r.type === 'breed' && r.steps && r.steps.length > 0) {
        const s = r.steps[0];
        label = `${s.leftParent ? s.leftParent.name : '?'} + ${s.rightParent ? s.rightParent.name : '?'}`;
      }
      return `<button class="${i===idx?'rtab act':'rtab'}" data-r="${i}">${label}</button>`;
    }).join('');
    el.querySelectorAll('.rtab').forEach(b => {
      b.addEventListener('click', () => {
        if (b.classList.contains('act')) return;
        el.querySelectorAll('.rtab').forEach(x => x.classList.remove('act'));
        b.classList.add('act');
        if (window._lastResult) Renderer.renderRoute(window._lastResult, 'result-container', parseInt(b.dataset.r));
      });
    });
  }
  function bindActs() {
    const ub = document.getElementById('su-btn');
    if (ub) ub.addEventListener('click', () => {
      navigator.clipboard.writeText(Share.getShareURL()).then(() => { ub.textContent = '✅ Copied!'; setTimeout(() => { ub.textContent = '🔗 Copy Link'; }, 2000); });
    });
    document.getElementById('bk-btn')?.addEventListener('click', () => history.back());
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

  return { renderRoute, renderTreeSVG: () => {}, renderDropdown };
})();
