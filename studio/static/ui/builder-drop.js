// First insertion on a verified Wagtail page. Only the Studio shell owns the gesture.
window.studioBuilderDrop = function (shell, layers, send) {
  const palette = shell.querySelector('#canvas-palette');
  if (!palette) return null;
  const sections = new Set(palette.dataset.sections.trim().split(/\s+/).filter(Boolean));
  const siblings = new Map();
  for (const [id, button] of layers) {
    const parent = button.dataset.parent;
    if (!siblings.has(parent)) siblings.set(parent, []);
    siblings.get(parent).push(id);
  }
  const frame = shell.querySelector('#canvas-frame');
  const plane = shell.querySelector('#canvas-drop-plane');
  const line = shell.querySelector('#canvas-drop-line');
  const start = palette.querySelector('#canvas-drop-start');
  const picker = palette.querySelector('select');
  const status = shell.querySelector('#canvas-status');
  let active = false;
  let pointer = null;
  let seq = 0;
  let committing = false;
  let suppressClick = false;
  let selectedKind;

  function invalidate() {
    seq++;
    line.hidden = true;
    committing = false;
  }
  function cancel() {
    active = false;
    pointer = null;
    plane.hidden = true;
    start.setAttribute('aria-pressed', 'false');
    invalidate();
  }
  function activate() {
    if (frame.hidden || !send({type: 'drop-scroll', dy: 0})) return false;
    active = true;
    selectedKind = picker.value;
    plane.hidden = false;
    start.setAttribute('aria-pressed', 'true');
    status.textContent = 'Choisissez une destination dans la page. Échap annule le placement.';
    return true;
  }
  function probe(event, commit) {
    if (!active || committing) return;
    const box = frame.getBoundingClientRect();
    const x = event.clientX - box.left, y = event.clientY - box.top;
    if (x < 0 || y < 0 || x >= box.width || y >= box.height) {
      invalidate();
      if (commit) cancel();
      return;
    }
    committing = commit;
    send({type: 'drop-probe', x, y, seq: ++seq});
  }
  function destination(result) {
    if (!result) return null;
    const {target, relation} = result;
    if (relation === 'empty' && !sections.size && target === null) return {parent: null, before: null};
    const layer = layers.get(target);
    if (relation === 'inside' && (sections.has(target) || layer?.dataset.container === '1')) {
      return {parent: target, before: null};
    }
    if (!layer || !['before', 'after'].includes(relation)) return null;
    const parent = layer.dataset.parent;
    const group = siblings.get(parent);
    return {parent, before: relation === 'before' ? target : group[group.indexOf(target) + 1] || null};
  }
  function receive(data) {
    if (!active || data.seq !== seq) return;
    const where = destination(data.result);
    const rect = data.result?.rect;
    if (!where || !Array.isArray(rect) || rect.length !== 4 ||
        !rect.every(n => Number.isFinite(n) && Math.abs(n) < 1e7)) {
      line.hidden = true;
      if (committing) {
        cancel();
        status.textContent = 'Dépôt refusé. Choisissez une section, un conteneur ou un bloc voisin.';
      }
      return;
    }
    if (committing) {
      cancel();
      shell.dispatchEvent(new CustomEvent('builder-edit-occurrence',
        {detail: {action: 'insert', kind: selectedKind, ...where}}));
      return;
    }
    const [x, y, w, h] = rect;
    Object.assign(line.style, {left:x+'px', top:y+'px', width:w+'px', height:Math.max(2,h)+'px'});
    line.hidden = false;
    const relation = {before:'Avant', after:'Après', inside:'Dans', empty:'Dans la page vide'};
    const label = layers.get(data.result.target)?.dataset.label || (where.parent ? 'la section' : '');
    status.textContent = [relation[data.result.relation], label].filter(Boolean).join(' ');
  }
  start.addEventListener('click', () => {
    if (suppressClick) { suppressClick = false; return; }
    if (active) { cancel(); status.textContent = ''; }
    else activate();
  });
  start.addEventListener('pointerdown', e => {
    if (e.button !== 0) return;
    suppressClick = false;
    pointer = {id:e.pointerId,x:e.clientX,y:e.clientY};
    start.setPointerCapture(e.pointerId);
  });
  start.addEventListener('pointermove', e => {
    if (pointer?.id !== e.pointerId || Math.hypot(e.clientX-pointer.x,e.clientY-pointer.y) < 6) return;
    if (!active && !activate()) return;
    suppressClick = true;
    probe(e,false);
  });
  start.addEventListener('pointerup', e => {
    if (pointer?.id === e.pointerId && suppressClick) probe(e,true);
    pointer = null;
  });
  start.addEventListener('pointercancel',cancel);
  plane.addEventListener('pointermove',e => probe(e,false));
  plane.addEventListener('click',e => probe(e,true));
  plane.addEventListener('wheel', e => {
    if (!active) return;
    e.preventDefault(); invalidate(); send({type:'drop-scroll', dy:e.deltaY});
  }, {passive:false});
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && active) { cancel(); status.textContent = 'Placement annulé.'; start.focus(); }
  });
  return {cancel, invalidate, receive};
};
