'use strict';

// The page is a local projection. The server independently replays and validates commands.
class BuilderWorkingPage {
  constructor(data) {
    this.data = data;
    this.history = [];
    this.cursor = 0;
    this.page = structuredClone(data.page);
  }

  definition(ref) {
    return this.data.definitions.find(d => d.scope === ref.scope && d.key === ref.key && d.version === ref.version);
  }

  rows() {
    const result = new Map();
    const visit = (node, siblings, parent, depth) => {
      const children = node.blocks || node.children;
      result.set(node.id, { node, siblings, parent, children, depth });
      children.forEach(child => visit(child, children, node, depth + 1));
    };
    this.page.sections.forEach(s => visit(s, this.page.sections, this.page, 0));
    return result;
  }

  label(node) {
    if (node.blocks) return 'Section ' + (this.page.sections.indexOf(node) + 1);
    const def = this.definition(node.definition);
    const value = node.props.text || node.props.label || node.props.alt || '';
    return (def?.label || node.definition.key) + (value ? ' · ' + value.slice(0, 64) : '');
  }

  container(node) {
    return Boolean(node.blocks || (this.definition(node.definition)?.renderer === 'container' && node.props.layout?.base));
  }

  drop(parentId, beforeId, movingId) {
    const rows = this.rows();
    const dest = rows.get(parentId);
    if (!dest || !this.container(dest.node)) throw Error('Choisissez une section ou un conteneur.');
    if (movingId) {
      let ancestor = dest;
      while (ancestor) {
        if (ancestor.node.id === movingId) throw Error('Un conteneur ne peut pas rejoindre sa descendance.');
        ancestor = rows.get(ancestor.parent.id);
      }
    }
    const i = beforeId ? dest.children.findIndex(n => n.id === beforeId) : dest.children.length;
    if (i < 0) throw Error('La position de dépôt a changé.');
    return {list:dest.children,index:i};
  }

  defaults(def) {
    const media = this.data.medias[0];
    switch (def.renderer) {
      case 'heading': return {level:2,text:'Nouveau titre'};
      case 'text': case 'signature': return {text:'Nouveau texte'};
      case 'button': return {label:'En savoir plus',url:'https://example.org/'};
      case 'container': return {layout:{base:{display:'stack'}}};
      case 'image':
        if (media) return {alt:media.label,media:{kind:'media',ref_id:media.id}};
        throw Error('Aucun média autorisé pour créer cette image.');
      default: throw Error('Ce composant demande une association dans Wagtail.');
    }
  }

  snapshot() { return this.history.slice(0, this.cursor).map(h => h.command); }

  preview(command) {
    const previous = this.page;
    this.page = structuredClone(previous);
    try { this.apply(command); }
    finally { this.page = previous; }
  }

  commit(command, selection) {
    const nextSize = this.snapshot().reduce((count, current) =>
      count + (current.action === 'gesture_group' && Array.isArray(current.steps)
        ? current.steps.length : 1), 0) +
      (command.action === 'gesture_group' && Array.isArray(command.steps)
        ? command.steps.length : 1);
    if (nextSize > 128) throw Error('Enregistrez vos modifications avant de continuer.');
    const original = this.page;
    this.page = structuredClone(original);
    try {
      this.apply(command);
    } catch (error) {
      this.page = original;
      throw error;
    }
    this.history.splice(this.cursor, this.history.length, {command,selection});
    this.cursor++;
    return selection;
  }

  step(direction) {
    this.cursor = Math.max(0,Math.min(this.history.length,this.cursor + direction));
    this.page = structuredClone(this.data.page);
    for (const command of this.snapshot()) this.apply(command);
    const undone = direction < 0 && this.history[this.cursor]?.command;
    if (undone && ['section_remove','block_remove'].includes(undone.action)) return undone.id;
    return this.history[this.cursor - 1]?.selection || null;
  }

  apply(cmd, { deferPlacementCheck = false } = {}) {
    if (cmd?.action === 'gesture_group') {
      if (!Array.isArray(cmd.steps) || cmd.steps.length < 2 || cmd.steps.length > 8 ||
          Object.keys(cmd).some(key => !['action', 'steps'].includes(key))) {
        throw Error('Le geste groupé doit comprendre entre 2 et 8 placements.');
      }
      const originals = new Map();
      for (const step of cmd.steps) {
        if (!step || step.action !== 'block_place' || step.overlap === true ||
            !step.id || originals.has(step.id)) {
          throw Error('Groupe incompatible ou occurrence dupliquée.');
        }
        const row = this.rows().get(step.id);
        if (!row || row.node.blocks) throw Error('Occurrence du groupe indisponible.');
        originals.set(step.id, this.collisions(row));
      }
      // Model only: intermediate overlap is allowed until all neighbours
      // reach their final positions. The backend independently revalidates.
      for (const step of cmd.steps) this.apply(step, { deferPlacementCheck: true });
      for (const [id, collisions] of originals) {
        this.checkPlacement(id, false, collisions);
      }
      return;
    }
    const rows = this.rows();
    const row = rows.get(cmd.id);
    const node = row?.node;
    const add = (item, movingId) => {
      const dest = this.drop(cmd.parent, cmd.before, movingId);
      dest.list.splice(dest.index,0,item);
    };
    const previous = ['block_move','block_place'].includes(cmd.action) ? this.collisions(row) : new Map();
    switch (cmd.action) {
      case 'section_add':
      case 'section_move': {
        const sections = this.page.sections;
        if (cmd.action === 'section_move') {
          if (!sections.includes(node)) throw Error('La section à déplacer est indisponible.');
          if (cmd.before === cmd.id) break;
        }
        const section = cmd.action === 'section_add'
          ? {id:cmd.local_id,layout:{base:{display:'stack'}},blocks:[]}
          : sections.splice(sections.indexOf(node),1)[0];
        const index = cmd.before ? sections.findIndex(s => s.id === cmd.before) : sections.length;
        if (index < 0) throw Error('La section de destination est indisponible.');
        sections.splice(index,0,section);
        break;
      }
      case 'block_add':
        add({id:cmd.local_id,definition:structuredClone(cmd.definition),props:structuredClone(cmd.props),children:[]});
        break;
      case 'block_move': {
        this.drop(cmd.parent,cmd.before,cmd.id);
        if (cmd.before === node.id) break;
        row.siblings.splice(row.siblings.indexOf(node),1);
        add(node,cmd.id);
        this.checkPlacement(node.id, false, previous);
        break;
      }
      case 'block_edit':
        node.props = structuredClone(cmd.props);
        if (cmd.appearance) node.appearance = structuredClone(cmd.appearance);
        break;
      case 'block_duplicate': {
        const copy = structuredClone(node);
        const remap = block => {
          const def = this.definition(block.definition);
          if (!def || def.retired || def.renderer === 'article') throw Error('La copie contient une référence indisponible pour une nouvelle occurrence.');
          block.id = cmd.local_ids[block.id];
          block.children.forEach(remap);
        };
        remap(copy);
        row.siblings.splice(row.siblings.indexOf(node)+1,0,copy);
        this.checkPlacement(copy.id);
        break;
      }
      case 'section_remove':
      case 'block_remove':
        row.siblings.splice(row.siblings.indexOf(node),1);
        break;
      case 'parent_layout': {
        const layout = node.layout || node.props.layout;
        Object.assign(layout[cmd.format] ||= {}, cmd.patch);
        for (const k of cmd.clear || []) delete layout[cmd.format][k];
        if (cmd.format!=='base' && !Object.keys(layout[cmd.format]).length) delete layout[cmd.format];
        for (const fmt of ['base','tablet','mobile']) {
          const rules = {...layout.base,...layout[fmt]};
          if ((rules.display || 'stack') === 'stack' && (rules.columns || 1) !== 1)
            throw Error('Une disposition en pile doit conserver une seule colonne.');
        }
        for (const child of row.children) this.checkPlacement(child.id, false, this.collisions(rows.get(child.id)));
        break;
      }
      case 'block_place': {
        const placement = node.placement ||= {base:{}};
        const delta = placement[cmd.format] ||= {};
        if (cmd.patch.mode && cmd.patch.mode !== this.placement(node,cmd.format).mode) {
          Object.keys(delta).forEach(k => delete delta[k]);
        }
        for (const k of cmd.clear || []) delete delta[k];
        Object.assign(delta,cmd.patch);
        if (cmd.format!=='base' && !Object.keys(delta).length) delete placement[cmd.format];
        if (placement.base.mode==='flow') delete placement.base.mode;
        if (!Object.keys(placement.base).length && Object.keys(placement).length===1) delete node.placement;
        if ('parent' in cmd) {
          // Preserve parity with Django block_place: the destination and
          // its before anchor are structural, not a DOM-only reordering.
          this.drop(cmd.parent, cmd.before, node.id);
          if (cmd.before !== node.id) {
            row.siblings.splice(row.siblings.indexOf(node), 1);
            const destination = this.drop(cmd.parent, cmd.before, node.id);
            destination.list.splice(destination.index, 0, node);
          }
        } else if ('before' in cmd) {
          throw Error('Choisissez le parent de destination.');
        }
        if (!deferPlacementCheck) this.checkPlacement(node.id, Boolean(cmd.overlap), previous);
        break;
      }
      default: throw Error('Commande inconnue.');
    }
  }

  placement(node, format) {
    const base = node.placement?.base || {};
    const local = node.placement?.[format] || {};
    const mode = local.mode || base.mode || 'flow';
    return {mode,span:1,z:0,...(mode === (base.mode || 'flow') ? base : {}),...local};
  }

  intersects(box, peer) {
    return box.mode==='free' && peer.mode==='free' && box.x<peer.x+peer.width && peer.x<box.x+box.width &&
      box.y<peer.y+peer.height && peer.y<box.y+box.height;
  }

  collisions(row) {
    const previous = new Map();
    for (const fmt of ['base','tablet','mobile']) {
      const box = this.placement(row.node,fmt);
      for (const peer of row.siblings) {
        const bounds=this.placement(peer,fmt);
        if(peer.id!==row.node.id && this.intersects(box,bounds))previous.set(fmt+'/'+peer.id,box.z===bounds.z);
      }
    }
    return previous;
  }

  checkPlacement(id, overlap = false, previous = new Map()) {
    const row = this.rows().get(id);
    const parent = row.parent;
    for (const fmt of ['base','tablet','mobile']) {
      const box = this.placement(row.node,fmt);
      const layout = parent.layout || parent.props?.layout || {};
      const columns = layout[fmt]?.columns ?? layout.base?.columns ?? 1;
      if (box.mode !== 'free') {
        if (box.span > columns) throw Error('La portée du bloc dépasse les colonnes du parent.');
        continue;
      }
      if (['x','y','width','height'].some(key => !Number.isInteger(box[key])))
        throw Error('Le placement libre requiert une position, une largeur et une hauteur.');
      const p = this.placement(parent,fmt);
      if (box.x + box.width > 100 || box.y + box.height > (p.mode === 'free' ? p.height : 4096))
        throw Error('Le bloc dépasse les limites de son parent.');
      for (const other of row.siblings) {
        if (other.id === id) continue;
        const b = this.placement(other,fmt);
        const key=fmt+'/'+other.id;
        const newCollision=!previous.has(key) && (!overlap || box.z===b.z);
        const lostOrder=previous.get(key)===false && box.z===b.z;
        if (this.intersects(box,b) && (newCollision || lostOrder))
          throw Error('Chevauchement avec ' + this.label(other) + ' (' + ({base:'bureau',tablet:'tablette',mobile:'mobile'})[fmt] + '). Autorisez la superposition avec des plans distincts.');
      }
    }
  }
}
