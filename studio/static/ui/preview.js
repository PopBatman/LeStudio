const statusLine = document.getElementById('preview-status');
for (const form of document.querySelectorAll('[data-preview-prepare]')) {
  form.addEventListener('submit', event => {
    if (form.getAttribute('aria-busy') === 'true') { event.preventDefault(); return; }
    form.setAttribute('aria-busy', 'true');
    statusLine.textContent = 'Préparation de l’aperçu Wagtail en cours…';
  });
}
window.addEventListener('pageshow', () => {
  for (const form of document.querySelectorAll('[data-preview-prepare]')) form.removeAttribute('aria-busy');
});

const panel = document.getElementById('preview-panel');
if (panel) {
  const frame = document.getElementById('preview-frame');
  const url = frame.src;
  const deadline = Number(panel.dataset.expires);
  let serial = 0;
  let suspended = false;
  const buttons = panel.querySelectorAll('[data-width]');
  function select(button) {
    for (const item of buttons) item.setAttribute('aria-pressed', String(item === button));
    frame.style.width = button.dataset.width === '390' ? 'min(390px, 100%)' : button.dataset.width + 'px';
  }
  select(buttons[window.innerWidth <= 600 ? 2 : window.innerWidth <= 950 ? 1 : 0]);
  for (const button of buttons) button.addEventListener('click', () => select(button));

  function hide() {
    serial++;
    frame.removeAttribute('src');
    frame.hidden = true;
  }
  function suspend(message) {
    suspended = true;
    hide();
    panel.hidden = true;
    document.getElementById('preview-retry').hidden = false;
    statusLine.textContent = message;
  }
  async function check() {
    if (suspended || document.hidden) return;
    if (Date.now() >= deadline) { suspend('L’aperçu a expiré.'); return; }
    const checkId = ++serial;
    try {
      const response = await fetch(url, {method: 'HEAD', cache: 'no-store', redirect: 'error',
        signal: AbortSignal.timeout(15000)});
      if (checkId !== serial) return;
      if (!response.ok || !response.headers.has('X-Studio-Head')) {
        suspend(response.status === 410 ? 'L’aperçu a expiré.' : 'Le rendu ne peut plus être vérifié.');
        return;
      }
      const head = response.headers.get('X-Studio-Head');
      if (head !== panel.dataset.revision) {
        document.getElementById('preview-head').textContent = head;
        document.getElementById('preview-stale').hidden = false;
      }
      if (!frame.hasAttribute('src')) frame.src = url;
      frame.hidden = false;
    } catch {
      if (checkId === serial) suspend('Connexion interrompue. Repréparez l’aperçu après rétablissement.');
    }
  }
  window.addEventListener('offline', () => suspend('Connexion interrompue. Repréparez l’aperçu après rétablissement.'));
  document.addEventListener('visibilitychange', () => { if (document.hidden) hide(); else check(); });
  window.addEventListener('pagehide', hide);
  window.addEventListener('pageshow', event => { if (event.persisted) check(); });
  setTimeout(() => suspend('L’aperçu a expiré.'), Math.max(0, deadline - Date.now()));
  setInterval(check, 15000);
}
