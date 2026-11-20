(() => {
  'use strict';
  const shell = document.getElementById('fc-private');
  if (!shell) return;
  const closed = document.getElementById('fc-closed');
  const compact = matchMedia('(max-width:620px)');
  const switcher = document.getElementById('fc-switch');
  let view = 'reference';
  function chooseView() {
    switcher.hidden = !compact.matches;
    for (const button of switcher.querySelectorAll('button')) {
      const active = button.dataset.view === view;
      button.setAttribute('aria-pressed',String(active));
      document.getElementById('fc-' + button.dataset.view).hidden = compact.matches && !active;
    }
  }
  for (const button of switcher.querySelectorAll('button')) button.onclick = () => {
    view = button.dataset.view;
    chooseView();
  };
  compact.addEventListener('change',chooseView);
  chooseView();
  const raster = shell.querySelector('.fc-raster');
  if (raster) raster.style.maxWidth = Number(shell.querySelector('.fc-pair').dataset.width) + 'px';
  const box = shell.querySelector('.fc-framebox');
  if (box) {
    const iframe = box.querySelector('iframe');
    const width = Number(box.dataset.width);
    const observer = new ResizeObserver(() => {
      if (!(width > 0) || !box.clientWidth) return;
      const scale = Math.min(1,box.clientWidth / width);
      const height = Math.min(640,Math.max(290,box.clientWidth * .92));
      iframe.style.width = width + 'px';
      iframe.style.height = Math.round(height / scale) + 'px';
      iframe.style.transform = 'scale(' + scale + ')';
      box.style.height = height + 'px';
    });
    observer.observe(box);
  }

  const file = shell.querySelector('[name=image]');
  const preview = document.getElementById('fc-file-preview');
  let localUrl;
  function clearUpload() {
    if (localUrl) URL.revokeObjectURL(localUrl);
    localUrl = null;
    preview?.removeAttribute('src');
    if (preview) preview.hidden = true;
  }
  if (file) file.addEventListener('change',() => {
    clearUpload();
    const selected = file.files[0];
    if (!selected || selected.type !== 'image/png') return;
    localUrl = URL.createObjectURL(selected);
    preview.src = localUrl;
    preview.hidden = false;
  });
  const decision = document.getElementById('fc-decision');
  if (decision) {
    const kind = decision.elements.kind, note = decision.elements.note;
    const requireNote = () => { note.required = kind.value !== 'matched'; };
    kind.addEventListener('change',requireNote);
    requireNote();
  }
  let checking = 0;
  let terminal = false;
  const reload = document.createElement('a');
  const restart = new URL(location.href);
  restart.searchParams.delete('ticket');
  restart.searchParams.delete('frame');
  restart.searchParams.delete('target');
  reload.href = restart;
  reload.textContent = 'Recharger la comparaison';
  function mask(message) {
    shell.hidden = true;
    closed.hidden = false;
    closed.replaceChildren(document.createTextNode(message + ' '),reload);
  }
  function discard(message) {
    terminal = true;
    clearUpload();
    mask(message);
    shell.remove();
  }
  async function verify() {
    if (terminal || document.hidden || !shell.dataset.access) return;
    const epoch = ++checking;
    try {
      const reply = await fetch(shell.dataset.access,{method:'HEAD',cache:'no-store',redirect:'manual',credentials:'same-origin'});
      if (epoch !== checking || terminal || document.hidden) return;
      if (reply.type === 'opaqueredirect' || [401,403,404,410].includes(reply.status)) {
        discard('L’accès à cette comparaison a pris fin.');
      } else if (!reply.ok) {
        mask('La comparaison est masquée pendant la vérification de l’accès.');
      } else if (shell.dataset.state && reply.headers.get('X-Compare-State') !== shell.dataset.state) {
        discard('La source, le brouillon ou le rendu a changé.');
      } else {
        closed.hidden = true;
        shell.hidden = false;
      }
    } catch {
      if (epoch === checking && !terminal) mask('La connexion au Studio est interrompue.');
    }
  }
  document.addEventListener('visibilitychange',() => {
    if (terminal) return;
    if (document.hidden) { checking++; mask('Vérification de l’accès à la comparaison.'); }
    else verify();
  });
  window.addEventListener('pageshow',verify);
  window.addEventListener('online',verify);
  window.addEventListener('focus',verify);
  window.addEventListener('offline',() => { if (!terminal) { checking++; mask('La connexion au Studio est interrompue.'); } });
  window.addEventListener('pagehide',() => { if (!terminal) { checking++; mask('Vérification de l’accès à la comparaison.'); } });
  const expiry = Number(shell.dataset.expires);
  if (expiry > 0) setTimeout(() => discard('Le reçu du rendu privé a expiré.'),Math.max(0,expiry-Date.now()));
  setInterval(verify,15000);
})();
