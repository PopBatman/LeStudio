(() => {
  'use strict';
  const byId = id => document.getElementById(id);
  const shell = byId('canvas-private');
  const status = byId('canvas-status');
  const surface = byId('canvas-surface');
  const frame = byId('canvas-frame');
  const paper = byId('canvas-paper');
  const outline = byId('canvas-outline');
  const inspector = byId('canvas-inspector');
  const closed = byId('canvas-closed');
  const layers = new Map(Array.from(shell.querySelectorAll('[data-block-id]'),
    b => [b.dataset.blockId, b]));
  let requestedSelection = shell.dataset.initialSelection;
  const drop = window.studioBuilderDrop?.(shell, layers, (message) => {
    if (!channel || stale || suspended || closedAccess) return false;
    channel.postMessage({...message, layout});
    return true;
  });
  const expiry = surface ? Number(surface.dataset.expires) : 0;
  let binding, channel, handshakeTimer, layout = 0, epoch = 0;
  let checking = null;
  let suspended = false, closedAccess = false, selected = null;
  let stale = surface && !byId('canvas-stale').hidden;
  const nav = shell.querySelector('.cb-nav');
  const navSummary = nav?.querySelector('summary');
  if (matchMedia('(max-width:620px)').matches && nav) nav.open = !surface;
  nav?.addEventListener('keydown', event => {
    if (event.key === 'Escape') { nav.open = false; navSummary.focus(); }
  });

  function inspect(id) {
    const button = layers.get(id);
    if (selected) layers.get(selected)?.setAttribute('aria-pressed', 'false');
    selected = button ? id : null;
    if (!inspector) return;
    byId('canvas-selection').textContent = button?.dataset.label || 'Aucun bloc sélectionné';
    byId('canvas-properties').hidden = !button;
    byId('canvas-definition').textContent = button ? button.dataset.key + ' · v' + button.dataset.version : '';
    byId('canvas-uuid').textContent = button ? id : '';
    if (button) button.setAttribute('aria-pressed', 'true');
    const article = byId('canvas-articles');
    if(article){
      const url=new URL(article.href);
      if(button && (button.dataset.container==='1' || button.dataset.renderer==='article'))url.searchParams.set('selection',id);
      else if(shell.dataset.section)url.searchParams.set('selection',shell.dataset.section);
      else url.searchParams.delete('selection');
      article.href=url;
    }
  }
  function resetChannel() {
    clearTimeout(handshakeTimer);
    drop?.cancel();
    binding = null;
    channel?.close();
    channel = null;
    if (outline) outline.hidden = true;
    inspect(null);
  }
  function clearFrame() {
    resetChannel();
    if (frame) { frame.hidden = true; frame.removeAttribute('src'); }
  }
  function lock(message) {
    closedAccess = true;
    shell.dispatchEvent(new Event("builder-access-revoked"));
    epoch++;
    clearFrame();
    shell.remove();
    document.title = 'Canvas fermé · Le Studio';
    closed.hidden = false;
    closed.textContent = message;
  }
  function suspend(message) {
    suspended = true;
    clearFrame();
    surface.hidden = true;
    for (const b of layers.values()) b.disabled = true;
    byId('canvas-diagnostic').hidden = true;
    status.textContent = message;
  }
  function tellLayout() {
    layout++;
    if (outline) outline.hidden = true;
    drop?.invalidate();
    channel?.postMessage({type: 'layout', layout});
  }
  function size() {
    const preset = byId('canvas-width');
    const custom = byId('canvas-custom-width');
    if (preset.value === 'custom' && !custom.value) {
      custom.value = Math.max(320,Math.min(1920,paper.clientWidth));
    }
    if (preset.value !== 'custom') custom.value = preset.value === 'auto' ? '' : preset.value;
    const value = preset.value === 'custom' ? custom.value : preset.value;
    paper.style.width = value === 'auto' ? '100%' : value + 'px';
    const opening=byId('canvas-opening');
    if(opening)opening.elements.largeur.value=value==='auto'?'':value;
    tellLayout();
  }
  function useMeasurement(data) {
    if (data.type !== 'measure' || data.layout !== layout || stale) return;
    if (data.id !== null && !layers.has(data.id)) return;
    const changed = selected !== data.id;
    if (changed) inspect(data.id);
    const rect = data.rect;
    const visible = data.id && Array.isArray(rect) && rect.length === 4 &&
      rect.every(n => Number.isFinite(n) && Math.abs(n) < 1e7) &&
      rect[2] > 0 && rect[3] > 0 && rect[0] < frame.clientWidth &&
      rect[1] < frame.clientHeight && rect[0]+rect[2] > 0 && rect[1]+rect[3] > 0;
    outline.hidden = !visible;
    if (visible) {
      const [x,y,w,h] = rect;
      Object.assign(outline.style,{left:x+'px',top:y+'px',width:w+'px',height:h+'px'});
    }
    const info = byId('canvas-selection-info');
    const feedback = selected ? (visible ? 'Bloc sélectionné · ' : 'Bloc hors de la zone visible · ') +
      layers.get(selected).textContent : '';
    if (info.textContent !== feedback) info.textContent = feedback;
    const diagnostic = byId('canvas-diagnostic');
    diagnostic.textContent = data.overflowing ? 'Le contenu dépasse la largeur de cette page.' : '';
    diagnostic.hidden = !data.overflowing;
  }

  function startFrame() {
    if (suspended || closedAccess || document.hidden || binding) return;
    resetChannel();
    binding = Array.from(crypto.getRandomValues(new Uint8Array(16)),
      byte => byte.toString(16).padStart(2,'0')).join('');
    const expected = binding;
    frame.src = surface.dataset.url + '#' + binding;
    frame.hidden = false;
    for (const b of layers.values()) b.disabled = true;
    status.textContent = 'Chargement du rendu Wagtail…';
    handshakeTimer = setTimeout(() => {
      if (binding === expected) suspend('La sélection dans la page est indisponible. Consultez la structure ou l’aperçu de référence.');
    }, 18000);
  }

  window.addEventListener('message', event => {
    const d = event.data;
    if (!frame || !binding || channel || event.source !== frame.contentWindow ||
        event.origin !== 'null' || d?.type !== 'studio-canvas-ready' || d.binding !== binding ||
        d.revision !== shell.dataset.revision || d.page !== shell.dataset.page ||
        d.instance !== surface.dataset.instance || d.fingerprint !== surface.dataset.fingerprint) return;
    const pair = new MessageChannel();
    channel = pair.port1;
    channel.onmessage = ({data}) => {
      if (channel !== pair.port1 || !binding || closedAccess || !data) return;
      if (data.type === 'connected') {
        clearTimeout(handshakeTimer);
        status.textContent = '';
        for (const b of layers.values()) b.disabled = stale;
        tellLayout();
        if (!stale && layers.has(requestedSelection)) {
          channel.postMessage({type: 'select', id: requestedSelection});
          requestedSelection = null;
        }
      } else if (!stale && data.layout === layout && data.type === 'drop-target') {
        drop?.receive(data);
      } else if (!stale && data.layout === layout && data.type === 'edit' && layers.has(data.id) &&
                 shell.querySelector('[data-edit-enabled]')) {
        shell.dispatchEvent(new CustomEvent('builder-edit-occurrence', {detail: {action: 'edit', id: data.id}}));
      } else {
        useMeasurement(data);
      }
    };
    frame.contentWindow.postMessage({type:'studio-canvas-connect',binding}, '*', [pair.port2]);
  });
  for (const [id,button] of layers) button.addEventListener('click', () => {
    if (surface) {
      if (!channel || stale) return;
      channel.postMessage({type:'select',id});
    } else {
      inspect(id);
      byId('canvas-selection-info').textContent = 'Sélection dans la structure du brouillon · ' + button.textContent;
    }
  });

  function markHistorical(response) {
    if (response.headers.get('X-Studio-Head') === surface.dataset.number) return;
    stale = true;
    drop?.cancel();
    byId('canvas-stale').hidden = false;
    if (byId('be-open')) byId('be-open').disabled = true;
    if (byId('canvas-palette')) byId('canvas-palette').hidden = true;
    byId('canvas-head').textContent = response.headers.get('X-Studio-Head');
    if (response.headers.get('X-Studio-Head-Has-Page') === '0') {
      byId('canvas-removed').hidden = false;
      byId('canvas-latest').href = shell.dataset.access;
    }
    outline.hidden = true;
    inspect(null);
    for (const b of layers.values()) b.disabled = true;
    byId('canvas-selection-info').textContent = 'Sélection suspendue sur le rendu historique.';
  }

  async function verify() {
    if (closedAccess || document.hidden || checking === epoch) return;
    const turn = ++epoch;
    checking = turn;
    const active = surface && !suspended;
    const url = active ? surface.dataset.url : shell.dataset.access;
    try {
      const response = await fetch(url,{method:'HEAD',cache:'no-store',redirect:'manual',signal:AbortSignal.timeout(15000)});
      if (turn !== epoch || closedAccess) return;
      if ([0,401,403,404].includes(response.status)) {
        lock('Le canvas est fermé. L’accès au site doit être vérifié à nouveau.');
        return;
      }
      if (response.status >= 500 || (!active && !response.ok)) {
        interrupt();
        return;
      }
      if (active) {
        if (!response.ok || !response.headers.has('X-Studio-Head')) {
          suspend(response.status === 410 ? 'Le reçu a expiré. Préparez de nouveau le rendu.' : 'Le rendu ne peut plus être vérifié. Actualisez ou consultez la structure.');
          checking = null;
          await verify();
          return;
        }
        markHistorical(response);
      }
      closed.hidden = true;
      shell.hidden = false;
      if (active) startFrame();
    } catch {
      if (turn === epoch) interrupt();
    } finally {
      if (checking === turn) checking = null;
    }
  }

  function conceal() {
    epoch++;
    shell.hidden = true;
    clearFrame();
  }
  function interrupt() {
    if (closedAccess) return;
    conceal();
    closed.hidden = false;
    closed.textContent = 'Connexion interrompue. Le canvas reprendra après vérification de votre accès.';
  }
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) conceal(); else verify();
  });
  window.addEventListener('pagehide', conceal);
  window.addEventListener('pageshow', event => { if (event.persisted) verify(); });
  window.addEventListener('offline', interrupt);
  window.addEventListener('online', verify);
  setInterval(verify, 15000);
  shell.querySelectorAll('form').forEach(form => form.addEventListener('submit', () => {
    if (surface) clearFrame();
    if (status) status.textContent = 'Préparation de la page…';
  }));
  const opening=byId('canvas-opening');
  opening?.elements.page.addEventListener('change',()=>{opening.elements.selection.value='';});
  if (!surface && requestedSelection && layers.has(requestedSelection)) inspect(requestedSelection);
  if (surface) {
    if(shell.dataset.width){
      const width=shell.dataset.width;
      byId('canvas-custom-width').value=width;
      byId('canvas-width').value=['390','820','1200'].includes(width)?width:'custom';
    }
    byId('canvas-width').addEventListener('change', size);
    byId('canvas-custom-width').addEventListener('change', event => {
      if (!event.target.reportValidity()) return;
      byId('canvas-width').value = event.target.value ? 'custom' : 'auto';
      size();
    });
    new ResizeObserver(() => {
      byId('canvas-size').textContent = ' · ' + paper.clientWidth + ' px';
      tellLayout();
    }).observe(paper);
    size();
    if (Date.now() >= expiry) suspend('Le reçu a expiré. Préparez de nouveau le rendu.');
    else {
      startFrame();
      setTimeout(() => {
        if (closedAccess || suspended) return;
        epoch++;
        suspend('Le reçu a expiré. Préparez de nouveau le rendu.');
        verify();
      }, Math.max(0, expiry - Date.now()));
    }
  }
})();
