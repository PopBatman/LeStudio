(() => {
  const stage = document.getElementById('cv-stage');
  if (!stage) return;
  const frame = document.getElementById('cv-frame');
  const form = document.getElementById('cv-gesture');
  const status = document.getElementById('ed-status');
  const issues = document.querySelector('.cv-issues');
  const zoom = document.getElementById('cv-zoom');
  let scale = 1;
  let active;
  let animation;
  let blockClick = false;

  function fit() {
    scale = zoom.getAttribute('aria-pressed') === 'true' ? 1 : Math.min(1, frame.clientWidth / stage.offsetWidth);
    if (scale <= 0) return;
    stage.style.transform = 'scale(' + scale + ')';
    frame.style.height = Math.ceil(stage.offsetHeight * scale) + 'px';
  }
  zoom.addEventListener('click', () => {
    const exact = zoom.getAttribute('aria-pressed') !== 'true';
    zoom.setAttribute('aria-pressed', String(exact));
    frame.style.width = exact ? stage.offsetWidth + 'px' : '100%';
    fit();
  });
  new ResizeObserver(fit).observe(stage);
  new ResizeObserver(fit).observe(frame);
  fit();

  function diagnostics() {
    const entries = [];
    for (const node of stage.querySelectorAll('.cv-node[data-mode="free"]')) {
      const parent = node.parentElement;
      const fixedParent = parent.closest('.cv-node[data-mode="free"]');
      const exceedsParent = fixedParent && node.getBoundingClientRect().bottom > fixedParent.getBoundingClientRect().bottom + 1;
      const overflowing = node.scrollHeight > node.clientHeight + 1 || node.scrollWidth > node.clientWidth + 1 || exceedsParent;
      node.classList.toggle('cv-overflow', Boolean(overflowing));
      if (overflowing) {
        const link = node.querySelector('.cv-select').cloneNode(false);
        link.textContent = node.dataset.label + ' · ' + node.querySelector('.cv-select').innerText.trim().slice(0, 72);
        const row = document.createElement('li');
        row.append(link);
        entries.push(row);
      }
    }
    issues.querySelector('ul').replaceChildren(...entries);
    issues.hidden = !entries.length;
  }
  if (document.readyState === 'complete') diagnostics();
  else window.addEventListener('load', diagnostics, {once:true});
  if (!form) return;

  // The pointer may be captured by its handle. Hit-testing at viewport coordinates
  // still finds the actual container underneath, including inside nested layouts.
  function destination(g) {
    const element = document.elementFromPoint(g.x, g.y);
    if (!element || !stage.contains(element)) return null;
    let parent = element.closest('[data-parent]');
    if (!parent) return null;
    if (g.node.contains(parent)) parent = g.node.parentElement;
    let sibling = element.closest('[data-node]');
    while (sibling && sibling.parentElement !== parent) sibling = sibling.parentElement.closest('[data-node]');
    if (sibling === g.node) return {parent, before:g.node.nextElementSibling?.dataset.node || '', target:g.node, edge:'inside'};
    if (!sibling) return {parent, before:'', target:parent, edge:'inside'};
    const rect = sibling.getBoundingClientRect();
    const after = parent.dataset.layout === 'grid' && Number(parent.dataset.columns) > 1
      ? g.x > rect.left + rect.width / 2 : g.y > rect.top + rect.height / 2;
    return {parent, before:after ? sibling.nextElementSibling?.dataset.node || '' : sibling.dataset.node,
      target:sibling, edge:after ? 'after' : 'before'};
  }

  function mark(g, element, edge) {
    if (g.mark === element && g.edge === edge) return;
    g.mark?.classList.remove('cv-drop-' + g.edge);
    g.mark = element;
    g.edge = edge;
    if (element) element.classList.add('cv-drop-' + edge);
  }
  function clamp(value, min, max) {return Math.min(max, Math.max(min, value));}
  function preview(g) {
    const rect = g.node.getBoundingClientRect();
    const parent = g.node.parentElement;
    const original = parent.getBoundingClientRect();
    const width = Math.max(1, original.width);
    const startW = g.initial.width;
    const startH = g.initial.height;
    g.command = null;
    let caption, box;
    if (g.resize) {
      if (!frame.contains(document.elementFromPoint(g.x, g.y))) {mark(g,null,'');g.ghost.hidden=true;return;}
      const pixels = Math.max(1, startW + g.x - g.startX);
      const height = clamp(Math.round((startH + g.y - g.startY) / scale), 1, 4096 - (g.free ? Number(g.node.dataset.y) : 0));
      let widthPct = clamp(Math.round(100 * pixels / width), 1, 100 - (g.free ? Number(g.node.dataset.x) : 0));
      const patch = {};
      if (height !== Math.round(startH / scale)) patch.height = height;
      let imageWidth = width * widthPct / 100;
      if (!g.free && parent.dataset.layout === 'grid') {
        const cols = Number(parent.dataset.columns);
        const gap = parseFloat(getComputedStyle(parent).columnGap) || 0;
        const stride = (width + gap * scale) / cols;
        const span = clamp(Math.round((pixels + gap * scale) / stride),1,cols);
        if (span !== Math.round((startW + gap * scale) / stride)) patch.span = span;
        imageWidth = stride * span - gap * scale;
        caption = span + ' col. × ' + height + ' px';
      } else {
        if (widthPct !== Math.round(100 * startW / width)) patch.width = widthPct;
        caption = widthPct + ' % × ' + height + ' px';
      }
      if (Object.keys(patch).length) g.command = {action:'block_place', ...patch};
      box = {left:rect.left,top:rect.top,width:imageWidth,height:height*scale};
    } else {
      const target = destination(g);
      if (!target) {mark(g,null,'');g.ghost.hidden=true;return;}
      const same = target.parent === parent;
      if (g.free) {
        const to = target.parent.getBoundingClientRect();
        const widthPct = parseFloat(g.node.style.width);
        const x = clamp(Math.round((g.x - g.offsetX - to.left) * 100 / to.width), 0, 100 - widthPct);
        const y = clamp(Math.round((g.y - g.offsetY - to.top) / scale), 0, 4096 - parseFloat(g.node.style.height));
        const patch = {};
        if (x !== Number(g.node.dataset.x)) patch.x = x;
        if (y !== Number(g.node.dataset.y)) patch.y = y;
        if (!same) Object.assign(patch, {parent:target.parent.dataset.parent,before:target.before});
        if (Object.keys(patch).length) g.command = {action:'block_place', ...patch};
        caption = 'X ' + x + ' % · Y ' + y + ' px';
        box = {left:to.left + x * to.width / 100, top:to.top + y * scale, width:widthPct * to.width / 100, height:startH};
        mark(g, same ? null : target.parent, 'inside');
      } else {
        g.command = {action:'block_move',parent:target.parent.dataset.parent,before:target.before};
        if (same && (target.before === g.node.dataset.node || target.before === (g.node.nextElementSibling?.dataset.node || ''))) g.command = null;
        mark(g, target.target, target.edge);
        caption = target.edge === 'inside' ? 'Dans la destination' : target.edge === 'after' ? 'Après le bloc' : 'Avant le bloc';
        box = {left:g.x+10, top:g.y+10,width:120,height:24};
      }
    }
    g.ghost.hidden = false;
    for (const [property,value] of Object.entries(box)) g.ghost.style[property] = value + 'px';
    g.ghost.firstChild.textContent = caption;
  }

  function autoscroll() {
    if (!active?.moving) return;
    const g = active;
    const pane = frame.parentElement;
    const r = pane.getBoundingClientRect();
    const step = (value, low, high) => value < low + 36 ? -10 : value > high - 36 ? 10 : 0;
    const dy = step(g.y, 0, innerHeight);
    if (dy) window.scrollBy(0,dy);
    const dx = step(g.x,r.left,r.right);
    if (dx && pane.scrollWidth > pane.clientWidth) pane.scrollBy(dx,0);
    if (dy || dx) preview(g);
    animation = requestAnimationFrame(autoscroll);
  }
  function cancel(announce) {
    if (!active) return;
    const g = active;
    active = null;
    cancelAnimationFrame(animation);
    mark(g,null,'');
    g.ghost?.remove();
    g.node.classList.remove('cv-active');
    if (stage.hasPointerCapture(g.id)) stage.releasePointerCapture(g.id);
    if (announce && g.moving) status.textContent = 'Geste annulé. Le brouillon est conservé.';
  }
  stage.addEventListener('dragstart', e => e.preventDefault());
  stage.addEventListener('pointerdown', e => {
    if (active || e.button !== 0 || !e.isPrimary) return;
    const control = e.target.closest('.cv-select,.cv-drag,.cv-resize');
    if (!control || (e.pointerType !== 'mouse' && control.matches('.cv-select'))) return;
    const node = control.closest('[data-node]');
    const initial = node.getBoundingClientRect();
    active = {id:e.pointerId,node,initial,resize:control.matches('.cv-resize'),free:node.dataset.mode==='free',
      startX:e.clientX,startY:e.clientY,offsetX:e.clientX-initial.left,offsetY:e.clientY-initial.top};
  });
  window.addEventListener('pointermove', e => {
    const g = active;
    if (!g || g.id !== e.pointerId) return;
    g.x = e.clientX; g.y = e.clientY;
    if (!g.moving) {
      if (Math.hypot(g.x - g.startX,g.y - g.startY) < 4) return;
      g.moving = true;
      stage.setPointerCapture(g.id);
      g.node.classList.add('cv-active');
      g.ghost = document.createElement('div');
      g.ghost.className = 'cv-ghost';
      g.ghost.setAttribute('aria-hidden','true');
      g.ghost.append(document.createElement('span'));
      document.body.append(g.ghost);
      animation = requestAnimationFrame(autoscroll);
    }
    preview(g);
  });
  window.addEventListener('pointerup', e => {
    const g = active;
    if (!g || g.id !== e.pointerId) return;
    if (g.moving) {g.x = e.clientX;g.y = e.clientY;preview(g);}
    const data = g.command;
    blockClick = Boolean(g.moving);
    setTimeout(()=>{blockClick=false;},0);
    cancel(false);
    if (!data) return;
    const values = {...data,node:g.node.dataset.node,section:g.node.closest('[data-section]').dataset.section};
    for (const [name,value] of Object.entries(values)) {
      const input = document.createElement('input');
      input.type = 'hidden';input.name=name;input.value=value;form.append(input);
    }
    form.requestSubmit();
  });
  window.addEventListener('pointercancel', () => cancel(true));
  stage.addEventListener('lostpointercapture', e => {
    // Touch first captures the handle implicitly. Its loss bubbles when the stage
    // takes capture, so only loss of the stage's own capture cancels the gesture.
    if (e.target === stage && active?.id === e.pointerId) cancel(true);
  });
  window.addEventListener('blur', () => cancel(true));
  window.addEventListener('keydown', e => {if (active && e.key === 'Escape') {e.preventDefault();cancel(true);}});
  stage.addEventListener('click', e => {if (blockClick) e.preventDefault();},true);
})();
