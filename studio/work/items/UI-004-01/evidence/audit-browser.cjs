const {chromium}=require('/home/admincsd/.npm/_npx/9833c18b2d85bc59/node_modules/playwright');
const {spawnSync}=require('child_process');
const fs=require('fs'),path=require('path'),assert=require('assert/strict'),crypto=require('crypto');
const out=path.resolve('studio/work/items/UI-004-01/evidence');
function django(source){
 const r=spawnSync('docker',['compose','-f','studio/compose.yaml','exec','-T','web','python','manage.py','shell','-c',source],{encoding:'utf8',maxBuffer:4*1024*1024});
 if(r.status!==0)throw Error('Lecture Django impossible : '+r.stderr.slice(0,400));
 return JSON.parse(r.stdout.trim().split('\n').at(-1));
}
const bootstrap=String.raw`
import json,hashlib
from django.test import Client
from django.urls import reverse
from composition.models import CompositionRevision
from registre.models import Site
from registre.services import can_manage
s=Site.objects.get(pk='59177d82-095d-4e5b-b095-7b73c220de4b')
u=next(g.user for g in s.grants.select_related('user').filter(level='manage') if can_manage(g.user,s))
r=CompositionRevision.objects.filter(site=s).order_by('-number').first()
c=Client();c.force_login(u)
print(json.dumps({'session':c.cookies['sessionid'].value,'site':str(s.pk),'operator':u.pk,'revision':str(r.pk),'number':r.number,'document':r.document,'digest':hashlib.sha256(json.dumps(r.document,sort_keys=True).encode()).hexdigest(),'url':reverse('registre:site-builder',args=[s.pk])}))
`;
(async()=>{
 let session=null,browser=null,report={started_at:new Date().toISOString(),command:'node studio/work/items/UI-004-01/evidence/audit-browser.cjs',node:process.version,steps:[],errors:[],blocked_writes:[]};
 try{
  const initial=django(bootstrap);session=initial.session;
  const reference=initial.document.pages.find(p=>p.sections.length);
  assert(reference,'Page de référence absente');
  const selected={site:initial.site,revision:initial.revision,number:initial.number,schema_version:initial.document.schema_version,page:reference,theme:initial.document.theme,document_sha256:initial.digest};
  fs.writeFileSync(path.join(out,'page-reference.json'),JSON.stringify(selected,null,2)+'\n');
  report.context={site:initial.site,operator:initial.operator,revision:initial.revision,number:initial.number,page:reference.id,title:reference.title,document_sha256:initial.digest};
  browser=await chromium.launch({executablePath:'/home/admincsd/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell',args:['--no-sandbox']});
  report.browser=browser.version();
  const context=await browser.newContext({viewport:{width:1440,height:1100}});
  await context.addCookies([{name:'sessionid',value:session,url:'http://127.0.0.1:8000',httpOnly:true,sameSite:'Lax'}]);
  const page=await context.newPage();
  page.on('pageerror',e=>report.errors.push(e.message));
  page.on('dialog',d=>d.accept());
  await context.route('**/*',route=>{
   const r=route.request(),url=new URL(r.url());
   if(!['127.0.0.1','localhost'].includes(url.hostname)){return route.abort();}
   if(r.method()==='POST'&&!url.pathname.endsWith('/atelier/visuel/')){
    report.blocked_writes.push({path:url.pathname,method:r.method()});return route.abort();
   }
   return route.continue();
  });
  const origin='http://127.0.0.1:8000';
  await page.goto(origin+initial.url+'?revision='+initial.revision+'&page='+reference.id);
  await page.locator('#be-open').waitFor();
  await page.locator('#canvas-opening button').click();
  await page.locator('#canvas-frame').waitFor({state:'visible',timeout:60000});
  await page.waitForFunction(()=>document.querySelector('#canvas-frame')?.contentWindow&&document.querySelectorAll('#canvas-layers button').length>0);
  await page.screenshot({path:path.join(out,'installe-wagtail-1440.png'),fullPage:true});
  const frame=page.frames().find(f=>f.parentFrame());
  assert(frame,'Frame Wagtail absente');
  const rendered=await frame.evaluate(()=>{const d=document.documentElement.cloneNode(true);d.querySelectorAll('script').forEach(s=>s.remove());return '<!doctype html>'+d.outerHTML;});
  assert(!rendered.includes('<script'),'Script dans instantané de référence');
  fs.writeFileSync(path.join(out,'rendu-wagtail-r18.html'),rendered);
  report.render_snapshot_sha256=crypto.createHash('sha256').update(rendered).digest('hex');

  report.steps.push({action:'Ouvrir aperçu installé',result:'iframe Wagtail visible',revision:initial.number,url:page.url().replace(/\/[0-9a-f-]{36}\//g,'/<id>/')});
  const editable=page.locator('#canvas-layers button[data-renderer="text"]').first();
  const editableId=await editable.getAttribute('data-block-id');await editable.click();
  await page.waitForFunction(id=>document.querySelector('#canvas-uuid')?.textContent===id,editableId);
  await page.locator('#be-open').click();
  await page.locator('#be-work').waitFor({state:'visible'});
  report.steps.push({action:'Sélectionner par UUID puis modifier',editable:editableId,wagtail_hidden:await page.locator('.cb-layout').isHidden(),local_nodes:await page.locator('#be-paper .be-node').count()});
  await page.screenshot({path:path.join(out,'installe-edition-1440.png'),fullPage:true});
  await page.screenshot({path:path.join(out,'installe-edition-1440.jpg'),type:'jpeg',quality:72,fullPage:true});
  const editableRow=page.locator('#be-paper [data-node="'+editableId+'"]');
  const originalText=await editableRow.locator('.be-content').innerText();
  await editableRow.locator(':scope > .be-title').click();await page.locator('#be-edit').click();
  const long='Le tennis, à votre rythme : une rencontre près de chez vous, pour jouer ensemble et progresser au fil des échanges.';
  await page.locator('#be-fields textarea[name="text"]').fill(long);
  await page.locator('#be-fields').getByRole('button',{name:'Confirmer',exact:true}).click();
  assert((await page.locator('#be-paper').innerText()).includes(long));
  assert(await page.locator('#be-undo').isEnabled());
  await page.screenshot({path:path.join(out,'installe-texte-long-local.png'),fullPage:true});
  await page.locator('#be-undo').click();
  assert((await page.locator('#be-paper').innerText()).includes(originalText));
  assert(await page.locator('#be-save').isDisabled());
  report.steps.push({action:'Texte long local confirmé puis undo',result:'texte initial retrouvé, aucune sauvegarde',text_length:long.length});
  await page.locator('#be-format').selectOption('mobile');assert.equal(await page.locator('#be-width').inputValue(),'390');
  await page.setViewportSize({width:390,height:1000});
  await page.screenshot({path:path.join(out,'installe-edition-390.png'),fullPage:true});
  report.steps.push({action:'Format mobile',result:'390 px dans projection locale'});
  await page.locator('#be-close').click();
  for(const width of [1200,820,390]){
   await page.setViewportSize({width:1440,height:1100});
   await page.locator('#canvas-custom-width').fill(String(width));
   await page.locator('#canvas-custom-width').dispatchEvent('change');
   await page.waitForTimeout(150);
   await page.screenshot({path:path.join(out,'installe-wagtail-format-'+width+'.png'),fullPage:true});
   const frameWidth=await page.locator('#canvas-frame').evaluate(e=>Math.round(e.getBoundingClientRect().width));assert.equal(frameWidth,width);report.steps.push({action:'Largeur du rendu Wagtail',width,measured_width:frameWidth});
  }
  const docs=initial.document.pages;
  report.pages=docs.map(p=>({id:p.id,title:p.title,sections:p.sections.length}));
  report.original_text=originalText;
  const end=django("import json,hashlib; from composition.models import CompositionRevision; r=CompositionRevision.objects.filter(site_id='"+initial.site+"').order_by('-number').first(); print(json.dumps({'revision':str(r.pk),'number':r.number,'digest':hashlib.sha256(json.dumps(r.document,sort_keys=True).encode()).hexdigest()}))");
  assert.equal(end.revision,initial.revision);assert.equal(end.digest,initial.digest);
  report.after=end;report.result='passed';
 }catch(e){report.result='failed';report.failure=e.message;process.exitCode=1;}
 finally{
  if(browser)await browser.close();
  if(session){django("import json; from django.contrib.sessions.models import Session; n,_=Session.objects.filter(session_key="+JSON.stringify(session)+").delete(); print(json.dumps({'deleted':n}))");report.session_cleanup=true;}
  report.finished_at=new Date().toISOString();fs.writeFileSync(path.join(out,'audit-browser.json'),JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));
 }
})();
