/* ===== Share - URL Hash + Card Generator ===== */
const Share = (() => {
  function getShareURL() {
    const params = new URLSearchParams(window.location.hash.slice(1));
    const q = params.get('q');
    if (q) {
      return `${window.location.origin}${window.location.pathname}#q=${encodeURIComponent(q)}`;
    }
    return window.location.href;
  }

  function parseHash() {
    const hash = window.location.hash.slice(1);
    const params = new URLSearchParams(hash);
    return { q: params.get('q') || null };
  }

  function setHash(targetPalId) {
    window.location.hash = `q=${encodeURIComponent(targetPalId)}`;
  }

  function clearHash() {
    history.replaceState(null, '', window.location.pathname);
  }

  function onHashChange(callback) {
    window.addEventListener('hashchange', () => {
      const parsed = parseHash();
      callback(parsed);
    });
  }

  /* ===== Share Card Generator ===== */
  function generateCard(result) {
    if (!result || !result.target || !result.routes || result.routes.length === 0) return;
    const r = result.routes[0];
    const t = result.target;

    const W = 600, H = 400;
    const canvas = document.createElement('canvas');
    canvas.width = W; canvas.height = H;
    const ctx = canvas.getContext('2d');

    // Background
    const grad = ctx.createLinearGradient(0, 0, W, H);
    grad.addColorStop(0, '#0a0e17');
    grad.addColorStop(1, '#111827');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, W, H);

    // Accent bar
    ctx.fillStyle = 'rgba(59,130,246,0.2)';
    ctx.fillRect(0, 0, W, 3);

    // Brand
    ctx.fillStyle = '#3b82f6';
    ctx.font = 'bold 20px sans-serif';
    ctx.fillText('PalTool', 30, 45);
    ctx.fillStyle = '#64748b';
    ctx.font = '12px sans-serif';
    ctx.fillText('paltool.cc', 120, 45);

    // Target pal name
    ctx.fillStyle = '#e2e8f0';
    ctx.font = 'bold 28px sans-serif';
    ctx.fillText(t.name, 30, 100);

    // Stats row
    ctx.fillStyle = '#94a3b8';
    ctx.font = '14px sans-serif';
    const bp = `BP: ${t.bp}`;
    const element = t.element || '?';
    ctx.fillText(`${bp}  ·  ${element}  ·  ${t.egg || ''}`, 30, 125);

    // Breeding route
    if (r.type === 'breed' && r.steps && r.steps.length > 0) {
      const s = r.steps[0];
      ctx.fillStyle = '#64748b';
      ctx.font = '12px sans-serif';
      ctx.fillText('BREEDING ROUTE', 30, 170);

      const lname = s.leftParent ? s.leftParent.name : '?';
      const rname = s.rightParent ? s.rightParent.name : '?';

      ctx.fillStyle = '#e2e8f0';
      ctx.font = 'bold 22px sans-serif';
      const comboText = `${lname}  +  ${rname}  →  ${t.name}`;
      ctx.fillText(comboText, 30, 210);

      // Steps info
      const steps = r.steps.length;
      let wild = 0;
      r.steps.forEach(st => { if (st.leftIsWild) wild++; if (st.rightIsWild) wild++; });
      ctx.fillStyle = '#64748b';
      ctx.font = '13px sans-serif';
      ctx.fillText(`${steps} generation${steps>1?'s':''} · ${wild} wild catches · ${steps*10} cakes est.`, 30, 250);
    } else if (r.type === 'wild') {
      ctx.fillStyle = '#22c55e';
      ctx.font = 'bold 18px sans-serif';
      ctx.fillText('Can be caught in the wild!', 30, 200);
    }

    // Footer
    ctx.fillStyle = '#334155';
    ctx.fillRect(0, H - 50, W, 50);
    ctx.fillStyle = '#64748b';
    ctx.font = '11px sans-serif';
    ctx.fillText('44,552 verified breeding recipes · Updated for Palworld 1.0', 30, H - 20);
    ctx.fillText('Made with PalTool.cc', W - 170, H - 20);

    // Download
    canvas.toBlob(blob => {
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `paltool-${t.id}.png`;
      a.click();
      URL.revokeObjectURL(url);
    });
  }

  return { getShareURL, parseHash, setHash, clearHash, onHashChange, generateCard };
})();
