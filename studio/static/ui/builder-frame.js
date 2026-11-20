// Runs only inside the isolated, verified Wagtail document.
(() => {
  'use strict';
  const context = document.currentScript.dataset;
  const binding = location.hash.slice(1);
  if (parent === window || !/^[a-f0-9]{32}$/.test(binding)) return;

  const blocks = new Map(Array.from(document.querySelectorAll('[data-studio-block-id]'),
    node => [node.dataset.studioBlockId, node]));
  let channel;
  let selection;
  let pending = false;
  let layout = 0;
  const observer = new ResizeObserver(schedule);

  function schedule() {
    if (!channel || pending) return;
    pending = true;
    requestAnimationFrame(() => {
      pending = false;
      if (!channel) return;
      const rect = selection?.getBoundingClientRect();
      channel.postMessage({
        type: 'measure', layout, id: selection?.dataset.studioBlockId || null,
        rect: rect && rect.width > 0 && rect.height > 0
          ? [rect.left, rect.top, rect.width, rect.height] : null,
        overflowing: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1
      });
    });
  }

  function select(id, reveal) {
    const node = blocks.get(id);
    if (!node) return;
    if (selection) observer.unobserve(selection);
    selection = node;
    observer.observe(node);
    if (reveal) node.scrollIntoView({block: 'nearest', inline: 'nearest'});
    schedule();
  }

  function dropTarget(x, y) {
    const hit = document.elementFromPoint(x, y);
    const block = hit?.closest('[data-studio-block-id]');
    const section = hit?.closest('main > section[id]');
    if (!section) {
      return hit && !hit.closest('nav, header, footer') && !document.querySelector('main > section')
        ? {target: null, relation: 'empty', rect: [0, 0, innerWidth, 2]} : null;
    }
    const node = block || section;
    const rect = node.getBoundingClientRect();
    const ratio = (y - rect.top) / Math.max(1, rect.height);
    const inside = !block || (block.classList.contains('container') && ratio >= .25 && ratio <= .75);
    const relation = inside ? 'inside' : (ratio < .5 ? 'before' : 'after');
    return {target: block ? block.dataset.studioBlockId : section.id.slice(1), relation,
      rect: [rect.left, relation === 'after' ? rect.bottom : rect.top, rect.width, inside ? rect.height : 2]};
  }
  function connect(event) {
    if (event.source !== parent || event.data?.type !== 'studio-canvas-connect' ||
        event.data.binding !== binding || event.ports.length !== 1 || channel) return;
    channel = event.ports[0];
    window.removeEventListener('message', connect);
    channel.onmessage = ({data}) => {
      if (data?.type === 'drop-probe' && data.layout === layout && Number.isSafeInteger(data.seq) &&
          Number.isFinite(data.x) && Number.isFinite(data.y)) {
        channel.postMessage({type: 'drop-target', seq: data.seq, layout,
          result: dropTarget(data.x, data.y)});
      }
      if (data?.type === 'drop-scroll' && Number.isFinite(data.dy)) {
        window.scrollBy(0, Math.max(-160, Math.min(160, data.dy)));
      }
      if (data?.type === 'select' && typeof data.id === 'string') select(data.id, true);
      if (data?.type === 'layout' && Number.isSafeInteger(data.layout) && data.layout >= layout) {
        layout = data.layout;
        schedule();
      }
    };
    observer.observe(document.documentElement);
    channel.postMessage({type: 'connected'});
    schedule();
  }
  window.addEventListener('message', connect);
  document.addEventListener('click', event => {
    event.preventDefault();
    const target = event.target.closest?.('[data-studio-block-id]');
    if (channel && target) select(target.dataset.studioBlockId, false);
  }, true);
  document.addEventListener('dblclick', event => {
    const node = event.target.closest?.('[data-studio-block-id]');
    if (channel && node) channel.postMessage({type: 'edit', layout, id: node.dataset.studioBlockId});
  });
  document.addEventListener('scroll', schedule, true);
  window.addEventListener('resize', schedule);
  window.visualViewport?.addEventListener('resize', schedule);
  document.addEventListener('load', schedule, true);
  document.fonts?.ready.then(schedule);
  window.addEventListener('pagehide', () => {
    observer.disconnect();
    channel?.close();
    channel = null;
  });
  parent.postMessage({type: 'studio-canvas-ready', binding, instance: context.instance,
    revision: context.revision, page: context.page, fingerprint: context.fingerprint}, '*');
})();
