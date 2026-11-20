(() => {
  'use strict';
  const el = id => document.getElementById('be-' + id);
  const root = el('root');
  if (!root) return;
  const data = JSON.parse(el('data').textContent);
  el('data').remove();
  const shell = root.closest('#canvas-private');
  const model = new BuilderWorkingPage(data);
  const definitions = new Map(data.definitions.map(d => [d.id,d]));
  const category = renderer => ({button:'Action',container:'Structure'})[renderer] || 'Contenu';
  const glyph = renderer => ({heading:'H',text:'¶',image:'▧',button:'▰',container:'▦',signature:'✎',article:'≡'})[renderer] || '◇';
  const formats = {base:'Bureau',tablet:'Tablette',mobile:'Mobile'};
  let selected = null, editing = false, pending = null, guide = null, active = false;
  let locked = false, denied = false, conflicted = false, retry = null, saving = false, leaving = false;
  let accessCheck = 0, accessPending = false;
  const paused = document.createElement('p');
  paused.hidden = true;
  paused.setAttribute('role','status');
  paused.textContent = 'La vérification de l’accès à l’éditeur reprendra avec la connexion.';
  root.before(paused);
  function pauseAccess(pause) {
    accessPending=pause;
    root.hidden=pause;
    paused.hidden=!pause;
  }
  const current = () => model.rows().get(selected);
  const node = (tag,text,cls) => {
    const n = document.createElement(tag);
    if (text !== undefined) n.textContent = text;
    if (cls) n.className = cls;
    return n;
  };
  const opt = (value,label) => new Option(label,value);
  const button = (text,act) => {
    const b = node('button',text); b.type = 'button'; b.addEventListener('click',act); return b;
  };
  function tell(message) { el('status').textContent = message; }
  function canChange() { return !denied && !locked && !accessPending && !saving && !retry; }
  function gesture(cmd, next, message) {
    if (!canChange()) return false;
    try {
      model.commit(cmd,next);
      selected = next; editing = false; stopPlacement(); draw(); focusSelection(); tell(message);
      return true;
    } catch (err) { tell(err.message); return false; }
  }
  function focusSelection() {
    (el('paper').querySelector('[data-node="' + selected + '"] > .be-title') || el('paper')).focus({preventScroll:true});
  }
  function actionFormat() { return el('format').value; }
  function makeField(parent,label,name,value,options) {
    const field = node('label',label);
    const input = options ? node('select') : node('input');
    if (options) for (const [val,txt] of options) input.add(opt(val,txt));
    input.name = name;
    input.value = value ?? '';
    field.append(input); parent.append(field); return input;
  }
  function makeNumber(parent,label,name,value,min,max) {
    const input = makeField(parent,label,name,value);
    Object.assign(input,{type:'number',min,max,required:true,step:1}); return input;
  }

  function catalog() {
    const term = el('search').value.trim().toLocaleLowerCase('fr');
    const filter = el('category').value;
    const list = el('catalog'); list.replaceChildren();
    for (const def of data.definitions) {
      if (filter && category(def.renderer) !== filter) continue;
      if (!((def.label+' '+def.key).toLocaleLowerCase('fr').includes(term))) continue;
      const b = button('',() => startPlacement({definition:def.id},true));
      b.className = 'be-card'; b.dataset.def = def.id;
      const unavailable = def.retired ? 'Version retirée' : def.renderer === 'article' ? 'Association éditoriale requise' :
        !['heading','text','button','container','image','signature'].includes(def.renderer) ? 'Incompatible' :
        def.renderer === 'image' && !data.medias.length ? 'Aucun média disponible' : '';
      const icon = node('span',glyph(def.renderer),'be-sample'); icon.setAttribute('aria-hidden','true');
      const label = node('span',def.label); label.append(node('small',(def.scope === 'global' ? 'Global' : 'Site')+' · v'+def.version+(unavailable ? ' · '+unavailable : '')));
      b.append(icon,label);b.disabled = Boolean(unavailable) || !canChange();b.draggable = !b.disabled;
      list.append(b);
    }
    if (!list.children.length) list.append(node('p',data.definitions.length ? 'Aucun composant ne correspond à cette recherche.' : 'Le catalogue est vide.'));
  }
  function layerList(rows) {
    const list = el('layers');list.replaceChildren();
    for (const {node:item,depth} of rows.values()) {
      const b = button(model.label(item),() => pick(item.id,true));
      b.setAttribute('aria-pressed',String(item.id===selected));b.dataset.select = item.id;
      b.style.paddingInlineStart = (.5 + Math.min(3,depth*.55))+'rem';list.append(b);
    }
  }
  function pick(id,focus=false) {
    if (editing && id===selected) return;
    if (editing && !window.confirm('Abandonner la saisie de ce bloc ?')) return;
    selected=id;editing=false;stopPlacement();draw();if(focus)focusSelection();
  }
  function startPlacement(source, focus) {
    if (!canChange()) return;
    if (editing) { tell('Confirmez ou annulez le champ en cours.'); return; }
    pending=source;
    const target=el('target');target.replaceChildren();
    if (source.section) {
      for (const section of model.page.sections.filter(item => item.id !== source.section))
        target.add(opt(section.id,'Avant '+model.label(section)));
      target.add(opt('','À la fin de la page'));
      el('destination').hidden=false;el('place').disabled=false;
      tell('Choisissez la position de la section.');target.focus();return;
    }
    for (const {node:item} of model.rows().values()) {
      if (!model.container(item)) continue;
      const children=item.blocks || item.children;
      for (const b of [...children,null]) {
        try {model.drop(item.id,b?.id,source.moving);} catch {continue;}
        if (b?.id===source.moving && source.moving) continue;
        const label=model.label(item)+' · '+(b?'avant '+model.label(b):'à la fin');
        target.add(opt(item.id+'/'+(b?.id||''),label));
      }
    }
    el('destination').hidden=!focus;el('place').disabled=!target.options.length;
    tell(target.options.length ? 'Choisissez le parent et la position.' : 'Ajoutez une section pour accueillir le premier bloc.');
    if(focus)target.focus();
  }
  function unmark() {
    if (guide) delete guide.dataset.guide;
    guide=null;
  }
  function stopPlacement() {
    unmark();pending=null;el('destination').hidden=true;
  }
  function commitDrop(parent,before) {
    if (!pending) return;
    const moving=pending.moving;
    if (moving) {
      const cmd={action:'block_move',id:moving,parent};
      if(before)cmd.before=before;
      gesture(cmd,moving,'Bloc déplacé.');return;
    }
    const def=definitions.get(pending.definition);
    if(!def || def.retired) {tell('Cette version est indisponible.');return;}
    const id=crypto.randomUUID();
    let props;try{props=model.defaults(def);}catch(e){tell(e.message);return;}
    const cmd={action:'block_add',parent,local_id:id,definition:{scope:def.scope,key:def.key,version:def.version},props};
    if(before)cmd.before=before;
    gesture(cmd,id,'Composant inséré.');
  }
  function dropAt(element,y) {
    const hit=element?.closest('[data-node]');
    unmark();
    if(!pending || !hit || !el('paper').contains(hit))return null;
    const row=model.rows().get(hit.dataset.node);
    if(!row)return null;
    const box=hit.getBoundingClientRect(), fraction=(y-box.top)/Math.max(1,box.height);
    const inside=Boolean(row.node.blocks || model.container(row.node)&&fraction>.22&&fraction<.78);
    const after=!inside && fraction>=.5;
    const parent=inside?row.node.id:row.parent.id;
    const before=inside?null:after?row.siblings[row.siblings.indexOf(row.node)+1]?.id:row.node.id;
    guide=hit;
    try{model.drop(parent,before,pending.moving);}catch(e){guide.dataset.guide='refus';tell(e.message);return null;}
    guide.dataset.guide=inside?'dans':after?'après':'avant';
    tell('Déposer '+guide.dataset.guide+' '+model.label(row.node)+'.');
    return {parent,before};
  }
  function sourceFor(target) {
    if(target.closest('[disabled]'))return null;
    const b=target.closest('[data-def],[data-move-id]');
    return b ? b.dataset.def ? {definition:b.dataset.def} : {moving:b.dataset.moveId} : null;
  }
  root.addEventListener('dragstart',e=>{
    const src=sourceFor(e.target);if(!src || !canChange() || editing){e.preventDefault();return;}
    startPlacement(src,false); e.dataTransfer.effectAllowed=src.moving?'move':'copy'; e.dataTransfer.setData('text/plain','Composant Studio');
  });
  el('paper').addEventListener('dragover',e=>{if(pending){e.preventDefault();dropAt(e.target,e.clientY);}});
  el('paper').addEventListener('drop',e=>{if(!pending)return;e.preventDefault();const dest=dropAt(e.target,e.clientY);if(dest)commitDrop(dest.parent,dest.before);});
  root.addEventListener('dragend',stopPlacement);
  let touch=null, suppressClickOn=null;
  root.addEventListener('pointerdown',e=>{
    const src=sourceFor(e.target);if(e.pointerType==='mouse'||!src||!canChange()||editing)return;
    touch={id:e.pointerId,src,x:e.clientX,y:e.clientY,drag:false,trigger:e.target.closest('button')};
    touch.trigger.setPointerCapture(e.pointerId);
  });
  root.addEventListener('pointermove',e=>{
    if(!touch||e.pointerId!==touch.id)return;
    if(!touch.drag && Math.hypot(e.clientX-touch.x,e.clientY-touch.y)>7){touch.drag=true;startPlacement(touch.src,false);}
    if(touch.drag){
      e.preventDefault();
      if(e.clientY<65 || e.clientY>innerHeight-65)window.scrollBy(0,e.clientY<65?-22:22);
      dropAt(document.elementFromPoint(e.clientX,e.clientY),e.clientY);
    }
  });
  root.addEventListener('pointerup',e=>{
    if(!touch||e.pointerId!==touch.id)return;
    if(touch.drag){
      const dest=dropAt(document.elementFromPoint(e.clientX,e.clientY),e.clientY);
      if(dest)commitDrop(dest.parent,dest.before);stopPlacement();suppressClickOn=touch.trigger;setTimeout(()=>suppressClickOn=null,200);
    }
    touch=null;
  });
  root.addEventListener('pointercancel',e=>{if(touch && touch.id===e.pointerId){touch=null;stopPlacement();}});
  root.addEventListener('click',e=>{if(suppressClickOn?.contains(e.target)){e.preventDefault();e.stopPropagation();} },true);

  function validDestination(value) {
    if(/[\s\\\x00-\x1f\x7f-\x9f]/u.test(value))return false;
    const host=value.match(/^https:\/\/([a-z0-9.-]+)(?::([0-9]+))?(?:[/?#]|$)/i);
    if(!host || host[2] && (+host[2]===0 || +host[2]>65535))return false;
    const name=host[1].replace(/\.$/,'');
    return name.length<=253 && name.split('.').every(s=>/^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?$/i.test(s));
  }
  function entryForm(item,def) {
    const form=node('form');form.id='be-fields';form.setAttribute('aria-label','Modifier '+def.label);
    const fields={};
    const labels={text:'Texte',label:'Libellé du bouton',url:'Destination HTTPS',alt:'Texte alternatif',media:'Média du site',level:'Niveau de titre'};
    for(const [key,type] of Object.entries(def.props)) {
      let input;
      if(key==='level') input=makeField(form,labels[key],key,item.props[key],Array.from({length:6},(_,i)=>[i+1,'H'+(i+1)]));
      else if(key==='media') input=makeField(form,labels[key],key,item.props.media?.ref_id,data.medias.map(m=>[m.id,m.label]));
      else if(type==='text'){
        const label=node('label',labels[key]||key);input=node('textarea');input.name=key;input.value=item.props[key]||'';label.append(input);form.append(label);
      } else input=makeField(form,labels[key]||key,key,item.props[key]);
      if(type==='https'){input.type='url';input.pattern='https://.+';input.maxLength=2048;}
      input.oninput=()=>input.setCustomValidity('');
      if(['text','label','alt'].includes(type))input.maxLength=type==='text'?4000:type==='label'?120:300;
      input.required=true;fields[key]=input;
    }
    const apply=node('button','Confirmer');apply.className='be-primary';apply.type='submit';form.append(apply,button('Annuler la saisie',endEntry));
    form.onsubmit=e=>{
      e.preventDefault();
      for(const [key,field] of Object.entries(fields)) {
        if(!field.value.trim() || field.value.includes('\0'))field.setCustomValidity('Renseignez un contenu valide.');
        if(def.props[key]==='https' && !validDestination(field.value))field.setCustomValidity('Saisissez une destination HTTPS avec un nom d’hôte valide, sans identifiants.');
        if(!field.reportValidity())return;
      }
      const props=structuredClone(item.props);
      for(const [name,f] of Object.entries(fields)) props[name]=name==='media'?{kind:'media',ref_id:f.value}:name==='level'?Number(f.value):f.value;
      gesture({action:'block_edit',id:item.id,definition:item.definition,props},item.id,'Contenu modifié dans la vue de travail.');
    };
    return form;
  }
  function endEntry(){editing=false;draw();focusSelection();}
  function editItem(id) {
    const row=model.rows().get(id),d=row&&!row.node.blocks&&model.definition(row.node.definition);
    if (!canChange()||!d||!['heading','text','signature','button','image'].includes(d.renderer))return;
    if(editing && (selected===id || !window.confirm('Abandonner la saisie de ce bloc ?'))) return;
    selected=id;editing=true;stopPlacement();draw();
    el('paper').querySelector('#be-fields input,#be-fields textarea,#be-fields select')?.focus();
  }
  function renderPage() {
    const paper=el('paper');paper.replaceChildren();
    const fmt=actionFormat();paper.dataset.format=fmt;paper.style.width=el('width').value+'px';
    function display(item,wrap) {
      const def=item.definition&&model.definition(item.definition);
      const container=Boolean(item.blocks || def?.renderer==='container');
      const card=node('div',undefined,'be-node');card.dataset.node=item.id;
      card.dataset.selected=String(item.id===selected);
      const title=button(item.blocks?model.label(item):def?.label||item.definition.key,()=>pick(item.id,true));title.className='be-title';
      card.append(title);
      if(!item.blocks){
        const grip=button('⠿',()=>startPlacement({moving:item.id},true));grip.className='be-grip';grip.dataset.moveId=item.id;grip.draggable=true;grip.setAttribute('aria-label','Déplacer '+model.label(item));card.append(grip);
      }
      if(item.id===selected&&editing)card.append(entryForm(item,def));
      else if(container){
        const layout=item.layout||item.props.layout;
        const rules={...layout?.base,...layout?.[fmt]};
        const children=node('div',undefined,'be-children');
        if(rules.display==='grid'){children.style.display='grid';children.style.gridTemplateColumns='repeat('+rules.columns+',minmax(0,1fr))';}
        children.style.gap=(rules.gap||0)+'px';
        const contents=item.blocks||item.children;
        for(const child of contents)display(child,children);
        const bottom=Math.max(0,...contents.map(c=>model.placement(c,fmt)).filter(p=>p.mode==='free').map(p=>p.y+p.height));
        if(bottom)children.style.minHeight=bottom+'px';
        if(!contents.length)children.append(node('p','Déposer dans '+model.label(item),'be-empty'));
        card.append(children);
      } else {
        const props=item.props;
        const content=node('div',undefined,'be-content');
        if(def?.renderer==='image'){
          const media=data.medias.find(m=>m.id===props.media?.ref_id);
          if(media?.url){const image=node('img');image.alt=props.alt;image.src=media.url;content.append(image);}
          else content.append(node('span','Média indisponible'));
        } else {
          const tag=def?.renderer==='heading'?'h'+Math.min(6,Math.max(1,props.level||2)):def?.renderer==='button'?'span':'p';
          content.append(node(tag,props.text||props.label||def?.label||'Référence indisponible',def?.renderer==='button'?'be-preview-button':''));
        }
        content.onclick=()=>editItem(item.id);card.append(content);
      }
      const placement=model.placement(item,fmt);
      if(placement.mode==='free'){
        Object.assign(card.style,{position:'absolute',left:placement.x+'%',top:placement.y+'px',width:placement.width+'%',height:placement.height+'px',zIndex:placement.z,overflow:'auto'});
      } else {
        if(placement.span>1)card.style.gridColumn='span '+placement.span;
        if(placement.width)card.style.width=placement.width+'%';
        if(placement.height){card.style.height=placement.height+'px';card.style.overflow='auto';}
      }
      if(def) {
        const ref=item.definition;
        const preset=data.theme?.components?.find(s=>s.definition.scope===ref.scope && s.definition.key===ref.key && s.definition.version===ref.version);
        const style={ink:'#202020',background:'#ffffff',accent:'#304860',...data.theme,...preset?.tokens,...item.appearance?.tokens};
        card.style.color=style.ink;card.style.backgroundColor=style.background;
        card.style.setProperty('--be-accent',style.accent);card.style.setProperty('--be-background',style.background);
        card.style.fontFamily=style.font==='dm-sans'?'"DM Sans", sans-serif':'system-ui, sans-serif';
        card.dataset.variant=item.appearance?.variant||preset?.variant||def.variants?.[0]||'';
      }
      wrap.append(card);
    }
    model.page.sections.forEach(s=>display(s,paper));
    if(!model.page.sections.length)paper.append(node('p','Cette page est vide. Ajoutez une section pour y placer un composant.','be-empty'));
  }

  function settings(row) {
    const panel=el('style');panel.replaceChildren();
    if (!row || editing || !canChange()) return;
    const item=row.node,fmt=actionFormat(),def=item.definition&&model.definition(item.definition);
    function section(title) {
      const details=node('details');details.append(node('summary',title));panel.append(details);
      const form=node('form');details.append(form);return form;
    }
    function submit(form,label,handler){
      const b=node('button',label);b.type='submit';form.append(b);
      form.onsubmit=e=>{e.preventDefault();handler();};
    }
    if(def && def.renderer!=='article'){
      const form=section('Apparence');
      const variant=makeField(form,'Variante','variant',item.appearance?.variant||'',['',...(def.variants||[])].map(v=>[v,v||'Héritée']));
      const tokens={};
      for(const key of ['ink','background','accent'].filter(k=>def.tokens?.includes(k))){
        const input=makeField(form,({ink:'Texte',background:'Fond',accent:'Accent'})[key]+' · couleur hexadécimale',key,item.appearance?.tokens?.[key]||'');
        input.pattern='#[a-fA-F0-9]{6}';input.placeholder='#334455';tokens[key]=input;
      }
      if(def.tokens?.includes('font'))tokens.font=makeField(form,'Police','font',item.appearance?.tokens?.font||'',[['','Héritée'],['system','Système'],['dm-sans','DM Sans']]);
      if(def.tokens?.includes('gap')){
        tokens.gap=makeNumber(form,'Espacement du composant (px)','gap',item.appearance?.tokens?.gap??'',0,128);
        tokens.gap.required=false;tokens.gap.placeholder='Hérité';
      }
      submit(form,'Appliquer le style',()=>{
        const appearance=structuredClone(item.appearance||{});
        if(variant.value)appearance.variant=variant.value;else delete appearance.variant;
        const values=appearance.tokens||{};
        Object.entries(tokens).forEach(([key,input])=>{if(input.value!=='')values[key]=key==='gap'?Number(input.value):input.value;else delete values[key];});
        if(Object.keys(values).length)appearance.tokens=values;else delete appearance.tokens;
        gesture({action:'block_edit',id:item.id,definition:item.definition,props:item.props,appearance},item.id,'Apparence modifiée.');
      });
    }
    function inheritance(form,action,local,labels) {
      if (!local || !Object.keys(local).length) return;
      const fields=node('fieldset');fields.append(node('legend',fmt==='base'?'Valeurs par défaut':'Héritage du bureau'));
      for(const key of Object.keys(local)){
        const label=labels[key]||key;
        fields.append(button((fmt==='base'?'Réinitialiser':'Hériter')+' · '+label,()=>{
          gesture({action,id:item.id,format:fmt,patch:{},clear:[key]},item.id,label+' réinitialisé.');
        }));
      }
      form.append(fields);
    }
    if(model.container(item)){
      const form=section('Disposition du parent · '+formats[fmt]);
      const layout=item.layout||item.props.layout;
      const value={display:'stack',columns:1,gap:0,...layout.base,...layout[fmt]};
      const mode=makeField(form,'Disposition','display',value.display,[['stack','Pile'],['grid','Grille']]);
      const cols=makeNumber(form,'Colonnes','columns',value.columns,1,12);
      const gap=makeNumber(form,'Espacement (px)','gap',value.gap,0,128);
      submit(form,'Appliquer la disposition',()=>{
        const patch={};
        if(mode.value!==value.display)patch.display=mode.value;
        const columns=mode.value==='grid'?Number(cols.value):1;
        if(columns!==value.columns)patch.columns=columns;
        if(Number(gap.value)!==value.gap)patch.gap=Number(gap.value);
        gesture({action:'parent_layout',id:item.id,format:fmt,patch},item.id,'Disposition modifiée.');
      });
      inheritance(form,'parent_layout',layout[fmt],{display:'Disposition',columns:'Colonnes',gap:'Espacement (px)'});
      if(fmt!=='base')form.append(button('Hériter du bureau',()=>gesture({action:'parent_layout',id:item.id,format:fmt,patch:{},clear:['display','columns','gap']},item.id,'Disposition héritée du bureau.')));
    }
    if(item.blocks)return;
    const form=section('Placement · '+formats[fmt]);
    const value=model.placement(item,fmt);
    const mode=makeField(form,'Mode','mode',value.mode,[['flow','Flux'],['free','Libre']]);
    const flow=node('fieldset');flow.append(node('legend','Taille en flux'));form.append(flow);
    const flowWidth=makeNumber(flow,'Largeur (%)','flowWidth',value.width??'',1,100);
    const flowHeight=makeNumber(flow,'Hauteur (px)','flowHeight',value.height??'',1,4096);
    flowWidth.required=flowHeight.required=false;
    const span=makeNumber(flow,'Portée en colonnes','span',value.span||1,1,12);
    const free=node('fieldset');free.append(node('legend','Position dans le parent'));form.append(free);
    const coords={};
    for(const [key,label,initial,min,max] of [
      ['x','X (%)',0,0,99],['y','Y (px)',0,0,4095],['width','Largeur (%)',50,1,100],['height','Hauteur (px)',100,1,4096],['z','Plan',0,0,100]
    ])coords[key]=makeNumber(free,label,key,value[key]??initial,min,max);
    const overlap=makeField(free,'Autoriser cette superposition','overlap','');overlap.type='checkbox';
    const modeChanged=()=>{free.hidden=free.disabled=mode.value!=='free';flow.hidden=flow.disabled=mode.value==='free';};
    mode.onchange=modeChanged;modeChanged();
    function placementCommand(){
      const switching=mode.value!==value.mode,patch={},clear=[];
      if(switching)patch.mode=mode.value;
      const inputs=mode.value==='flow'?{span,width:flowWidth,height:flowHeight}:coords;
      for(const [key,input] of Object.entries(inputs)){
        if(input.value===''){
          if(Object.hasOwn(item.placement?.[fmt]||{},key))clear.push(key);
        } else if(switching || Number(input.value)!==value[key] || key==='z' && overlap.checked){
          patch[key]=Number(input.value);
        }
      }
      const cmd={action:'block_place',id:item.id,format:fmt,patch,clear};
      if(mode.value==='free'&&overlap.checked)cmd.overlap=true;
      return cmd;
    }
    const feedback=node('p');feedback.setAttribute('role','status');form.append(feedback);
    const validate=()=>{
      if(!form.checkValidity()){feedback.textContent='Renseignez les coordonnées dans les bornes indiquées.';return;}
      try{model.preview(placementCommand());feedback.textContent=mode.value==='free'?'Placement dans les bornes du parent.':'';}
      catch(err){feedback.textContent=err.message;}
    };
    form.addEventListener('input',validate);form.addEventListener('change',validate);
    submit(form,'Appliquer le placement',()=>gesture(placementCommand(),item.id,'Placement mis à jour en vue '+formats[fmt]+'.'));
    inheritance(form,'block_place',item.placement?.[fmt],{mode:'Mode',span:'Portée',width:'Largeur (%)',height:'Hauteur (px)',x:'X (%)',y:'Y (px)',z:'Plan'});
    if(fmt!=='base')form.append(button('Hériter du bureau',()=>gesture({action:'block_place',id:item.id,format:fmt,patch:{},clear:Object.keys(item.placement?.[fmt]||{})},item.id,'Placement hérité du bureau.')));
  }
  function draw(){
    const rows=model.rows();
    if(!rows.has(selected)){selected=null;editing=false;}
    const row=rows.get(selected),item=row?.node;
    const def=item?.definition&&model.definition(item.definition);
    const allow=canChange();
    el('page').textContent=model.page.title;
    el('rev').textContent='Base R'+data.number+' · '+(model.cursor?'Modifications non enregistrées':'Page enregistrée');
    el('undo').disabled=!allow||editing||!model.cursor;
    el('redo').disabled=!allow||editing||model.cursor>=model.history.length;
    el('save').disabled=denied||locked||saving||conflicted||editing||!model.cursor;
    el('save').textContent=saving?'Enregistrement…':retry?'Réessayer la sauvegarde':'Enregistrer';
    el('close').disabled=saving||Boolean(retry);
    el('tools').hidden=!row;
    el('selection').textContent=item?model.label(item):'Sélectionnez un bloc.';
    el('edit').disabled=!allow||editing||!def||def.renderer==='article'||def.renderer==='container';
    el('copy').disabled=!allow||editing||!def;
    for(const id of ['move','remove','before'])el(id).disabled=!allow||editing||!row;
    el('before').hidden=!item?.blocks;
    const related=el('related');related.replaceChildren();
    if(item){
      const article=model.container(item)||def?.renderer==='article';
      const label=article?'Gérer les articles Wagtail':'Changer la définition ou la version';
      if(model.cursor||editing)related.append(node('p','Enregistrez la page pour accéder à « '+label+' ».'));
      else {
        const link=node('a',label);
        link.href=article?data.articles_url+'?page='+model.page.id+'&selection='+selected:data.catalogue_url+'?block='+selected;
        related.append(link);
      }
      if(def?.renderer==='container'&&!model.cursor&&!editing){
        const link=node('a','Changer la définition ou la version');link.href=data.catalogue_url+'?block='+selected;
        related.append(node('br'),link);
      }
    }
    el('section').disabled=!allow||editing;
    catalog();layerList(rows);renderPage();settings(row);
  }
  function open(id) {
    if(locked||denied||accessPending||el('open').disabled)return false;
    active=true;shell.classList.add('be-active');el('work').hidden=false;el('open').hidden=true;
    if(id&&model.rows().has(id))selected=id;
    draw();if(selected)focusSelection();else el('search').focus();
    if(id && !model.rows().has(id))tell('La sélection demandée est absente de cette page. Choisissez un calque.');
    return true;
  }
  function abandon(){return (!model.cursor&&!editing)||window.confirm('Abandonner les modifications locales et revenir à la version enregistrée ?');}
  function close() {
    if(saving||retry||!abandon())return;
    active=false;editing=false;model.cursor=0;model.history=[];model.page=structuredClone(data.page);
    selected=null;stopPlacement();conflicted=false;el('conflict').hidden=true;
    el('work').hidden=true;el('open').hidden=false;shell.classList.remove('be-active');tell('');el('open').focus();
  }
  function collectCopy(item,ids){ids[item.id]=crypto.randomUUID();item.children.forEach(c=>collectCopy(c,ids));}
  function openFromCanvas(e){
    const detail=e.detail||{};
    if(!open(detail.id))return;
    if(detail.action==='edit'&&detail.id)editItem(detail.id);
    if(detail.action==='insert' && definitions.has(detail.kind)){
      let parent=detail.parent;
      if(!parent && !model.page.sections.length){
        parent=crypto.randomUUID();
        if(!gesture({action:'section_add',local_id:parent},parent,'Section ajoutée.'))return;
      }
      pending={definition:detail.kind};commitDrop(parent,detail.before);
    }
  }
  shell.addEventListener('builder-edit-occurrence',openFromCanvas);
  el('open').onclick=()=>open(document.getElementById('canvas-uuid')?.textContent);
  el('close').onclick=close;
  el('search').oninput=catalog;el('category').onchange=catalog;
  el('section').onclick=()=>{const id=crypto.randomUUID();gesture({action:'section_add',local_id:id},id,'Section ajoutée.');};
  el('edit').onclick=()=>editItem(selected);
  el('before').onclick=()=>{
    const id=crypto.randomUUID();gesture({action:'section_add',local_id:id,before:selected},id,'Section insérée.');
  };
  el('move').onclick=()=>startPlacement(current().node.blocks?{section:selected}:{moving:selected},true);
  el('cancel-drop').onclick=()=>{stopPlacement();focusSelection();};
  el('place').onclick=()=>{
    if(pending?.section){
      const cmd={action:'section_move',id:pending.section};
      if(el('target').value)cmd.before=el('target').value;
      gesture(cmd,cmd.id,'Section déplacée.');return;
    }
    const [parent,before]=el('target').value.split('/');if(parent)commitDrop(parent,before);
  };
  el('copy').onclick=()=>{
    const ids={};collectCopy(current().node,ids);
    gesture({action:'block_duplicate',id:selected,local_ids:ids},ids[selected],'Copie créée.');
  };
  el('remove').onclick=()=>{
    const row=current(),descendants=[];
    function visit(children){for(const child of children){descendants.push(model.label(child));visit(child.children);}}
    visit(row.children);
    const impact=descendants.length?'\n'+descendants.length+' descendant(s) : '+descendants.slice(0,8).join(', ')+(descendants.length>8?'…':''):'';
    if(!window.confirm('Supprimer '+model.label(row.node)+' ?'+impact))return;
    const index=row.siblings.indexOf(row.node),next=row.siblings[index+1]||row.siblings[index-1]||row.parent;
    gesture({action:row.node.blocks?'section_remove':'block_remove',id:selected,confirmed:true},next===model.page?null:next.id,'Suppression effectuée. Annuler permet de restaurer la branche.');
  };
  function history(direction){
    if(!canChange()||editing)return;
    selected=model.step(direction);stopPlacement();draw();focusSelection();tell(direction<0?'Geste annulé.':'Geste rétabli.');
  }
  el('undo').onclick=()=>history(-1);el('redo').onclick=()=>history(1);
  const widths={base:1200,tablet:820,mobile:390};
  function changeFormat(width,format){
    if(editing && !window.confirm('Abandonner la saisie du champ pour changer de format ?')){
      el('format').value=el('paper').dataset.format;el('width').value=parseInt(el('paper').style.width,10);return;
    }
    el('format').value=format;el('width').value=width;
    editing=false;stopPlacement();draw();tell('Vue '+formats[format]+' · '+width+' px.');
  }
  el('width').onchange=()=>{
    if(!el('width').reportValidity())return;
    const width=el('width').valueAsNumber;
    changeFormat(width,width<768?'mobile':width<1024?'tablet':'base');
  };
  el('format').onchange=()=>changeFormat(widths[actionFormat()],actionFormat());
  root.addEventListener('keydown',e=>{
    if(e.key==='Escape'){
      if(pending){stopPlacement();focusSelection();tell('Placement annulé.');}
      else if(editing)endEntry();
    }
    if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='z'&&!e.target.closest('input,textarea,select')&&active){e.preventDefault();history(e.shiftKey?1:-1);}
  });
  function conflict(title,message,canReload){
    el('conflict').hidden=false;el('conflict-label').textContent=title;el('conflict-text').textContent=message;
    el('resume').hidden=!canReload;
    el('compare').hidden=!canReload;
    el('compare').href=data.prepare_url+'?page='+encodeURIComponent(model.page.id);
    el('journal').hidden=!canReload;
    const names={block_add:'Insérer',block_move:'Déplacer',block_remove:'Supprimer',block_edit:'Modifier',block_duplicate:'Dupliquer',block_place:'Régler le placement',parent_layout:'Régler la disposition',section_add:'Ajouter une section',section_move:'Déplacer une section',section_remove:'Retirer une section'};
    const rows=model.rows();
    el('journal').querySelector('ol').replaceChildren(...model.snapshot().map(c=>{
      const target=rows.get(c.id||c.local_id);
      return node('li',names[c.action]+(target?' · '+model.label(target.node):''));
    }));
  }
  el('resume').onclick=()=>{
    if(!window.confirm('Abandonner les gestes locaux et ouvrir la dernière révision ?'))return;
    leaving=true;location.assign(data.prepare_url+'?page='+encodeURIComponent(model.page.id));
  };
  function revoke(readLost, navigate=true) {
    denied=true;
    if(readLost) {
      locked=true;leaving=true;retry=null;model.history=[];model.cursor=0;model.page=null;selected=null;
      if(navigate)location.replace(data.prepare_url);return;
    }
    conflict('Droit de gestion retiré','Vos gestes ne peuvent plus être enregistrés.',false);
    if(active)draw();else el('open').hidden=true;
  }
  shell.addEventListener('builder-access-revoked',()=>revoke(true,false));
  async function verify(){
    if(!active||document.hidden||locked)return;
    const turn=++accessCheck;
    try{
      const r=await fetch(data.access_url,{method:'HEAD',cache:'no-store',redirect:'manual',signal:AbortSignal.timeout(12000)});
      if(turn!==accessCheck||!active||locked)return;
      if(r.status===204)pauseAccess(false);
      else if(r.status===403){pauseAccess(false);revoke(false);}
      else if([0,401,404].includes(r.status))revoke(true);
      else pauseAccess(true);
    }catch{if(turn===accessCheck&&active)pauseAccess(true);}
  }
  function postPreview(reply){
    const form=node('form');form.method='post';form.action=data.prepare_url;
    const token=document.querySelector('[name=csrfmiddlewaretoken]').value;
    for(const [name,value] of Object.entries({csrfmiddlewaretoken:token,revision:reply.revision,page:model.page.id,saved:'1',selection:reply.selection||'',largeur:el('width').value})){
      const i=node('input');i.type='hidden';i.name=name;i.value=value;form.append(i);
    }
    document.body.append(form);leaving=true;form.submit();
  }
  async function save() {
    if(!active||accessPending||saving||denied||locked||conflicted||editing||!model.cursor)return;
    if(!retry)retry={base:data.revision,page:model.page.id,key:crypto.randomUUID(),commands:model.snapshot(),selection:selected};
    saving=true;stopPlacement();draw();tell('Enregistrement du brouillon…');
    let reply,response;
    try{
      response=await fetch(data.save_url,{method:'POST',headers:{'Content-Type':'application/json','X-CSRFToken':document.querySelector('[name=csrfmiddlewaretoken]').value},body:JSON.stringify(retry),cache:'no-store',redirect:'manual',signal:AbortSignal.timeout(25000)});
      if([0,401,404].includes(response.status)){revoke(true);return;}
      if(response.status===403){retry=null;revoke(false);return;}
      reply=await response.json().catch(()=>({}));
      if(response.ok && reply.revision){postPreview(reply);return;}
      if([400,409,413,415,422].includes(response.status)){
        retry=null; conflicted=response.status===409;
        if(conflicted) conflict('Conflit de révision',reply.error||'La page a changé. Votre saisie locale est conservée.',true);
        tell(reply.error||'La sauvegarde a été refusée. Vos modifications sont conservées.');
        return;
      }
      throw Error('unknown');
    } catch {tell('Résultat de sauvegarde inconnu. Réessayez la même sauvegarde pour vérifier son résultat.');}
    finally {saving=false;if(active&&!leaving)draw();}
  }
  el('save').onclick=save;
  el('format').value=data.format||'base';el('width').value=data.width||1200;
  if (data.open_editor) open(data.selection);
  window.addEventListener('beforeunload',e=>{if(!leaving && active && (model.cursor||editing||retry)){e.preventDefault();e.returnValue='';}});
  document.addEventListener('visibilitychange',()=>{if(!document.hidden)verify();});
  window.addEventListener('offline',()=>{if(active){accessCheck++;pauseAccess(true);}});
  window.addEventListener('online',verify);
  setInterval(verify,15000);
})();
