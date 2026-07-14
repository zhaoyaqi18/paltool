/* ===== Share - URL Hash Serialization ===== */
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
    return {
      q: params.get('q') || null
    };
  }

  function setHash(targetPalId) {
    window.location.hash = `q=${encodeURIComponent(targetPalId)}`;
  }

  function clearHash() {
    history.replaceState(null, '', window.location.pathname);
  }

  // Watch for hash changes and browser back/forward
  function onHashChange(callback) {
    window.addEventListener('hashchange', () => {
      const parsed = parseHash();
      callback(parsed);
    });
  }

  return { getShareURL, parseHash, setHash, clearHash, onHashChange };
})();
