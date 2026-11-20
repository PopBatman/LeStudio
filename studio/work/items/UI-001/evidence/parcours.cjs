const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
const axe = require.resolve('axe-core/axe.min.js');
const output = process.env.UI_OUTPUT || fs.mkdtempSync(path.join(require('node:os').tmpdir(), 'studio-ui-'));
const base = 'http://127.0.0.1:8000';
const report={observed_at:new Date().toISOString(),origin:base,checks:[],accessibility:{},errors:[]};
const record=(name,detail)=>{report.checks.push({name,detail}); console.log(name,JSON.stringify(detail));};
async function interactions(page,name,record){
   const mobile=name==='mobile';
   const menu=page.locator('details.mobile-nav');
   if(mobile){await menu.locator('summary').focus(); await page.keyboard.press('Enter');}
   const nav=page.locator((mobile?'.mobile-nav':'.desktop-nav')+' .nav-item[href="#formulaires"]');
   await nav.focus();await page.keyboard.press('Enter');
   await page.waitForFunction(()=>location.hash==='#formulaires');
   if(mobile)assert.equal(await menu.getAttribute('open'),null);
   const field=page.locator('#site-name'), submit=page.locator('#name-form button[type=submit]');
   await field.fill('');await submit.focus();await page.keyboard.press('Enter');
   assert.equal(await field.getAttribute('aria-invalid'),'true');
   assert.ok(await page.locator('#site-name-error').isVisible());
   assert.ok((await field.getAttribute('aria-describedby'))?.includes('site-name-error'));
   await field.fill('Atelier Lumière');await field.press('Enter');
   await page.waitForFunction(()=>document.querySelector('#name-result').textContent.trim().length>0);
   assert.notEqual(await field.getAttribute('aria-invalid'),'true');
   record(name+' formulaire',await page.locator('#name-result').innerText());
   await field.fill('W'.repeat(80));await field.press('Enter');
   assert.ok((await page.locator('#name-result').innerText()).includes('W'.repeat(80)));
   const widths=await page.evaluate(()=>[innerWidth,document.documentElement.scrollWidth]);
   assert.equal(widths[0],widths[1]);record(name+' nom de 80 lettres sans espace',widths);
   await page.locator('#demo-primary').focus();await page.keyboard.press('Space');
   await page.waitForFunction(()=>document.querySelector('#action-result').textContent.trim().length>0);
   record(name+' action',await page.locator('#action-result').innerText());
   await page.locator('#demo-reset').click();
   const filter=page.locator('#site-filter'), rows=page.locator('#site-table tbody tr:visible');
   assert.equal(await rows.count(),3);
   await filter.fill('Horizon');assert.equal(await rows.count(),1);
   await filter.fill('aucun-exemple-correspondant');assert.equal(await rows.count(),0);
   assert.ok(await page.locator('#table-empty').isVisible());
   await page.locator('#clear-filter').focus();await page.keyboard.press('Enter');assert.equal(await rows.count(),3);
   record(name+' tableau','3 → 1 → 0 puis 3 lignes, état vide vérifié');
}

(async()=>{
 const browser=await chromium.launch({headless:true,executablePath:process.env.CHROMIUM_PATH});
 report.browser=browser.version();
 try{
 for(const [name,width,height] of [['desktop',1440,960],['mobile',390,844]]){
   const context=await browser.newContext({viewport:{width,height},deviceScaleFactor:1,locale:'fr-FR',reducedMotion:'reduce'});
   const page=await context.newPage();
   const requests=[];
   page.on('pageerror',e=>report.errors.push(e.message));
   page.on('response',r=>{requests.push([r.url(),r.status()]);if(r.status()>=400)report.errors.push(r.status()+' '+r.url())});
   const response=await page.goto(base+'/ui/',{waitUntil:'networkidle'});
   assert.equal(response.status(),200);await page.evaluate(()=>document.fonts.ready);
   assert.equal(await page.locator('h1').count(),1);
   const bounds=await page.evaluate(()=>[window.innerWidth,document.documentElement.scrollWidth]);
   assert.ok(bounds[1]<=bounds[0],JSON.stringify(bounds));record(name+' largeur',bounds);
   const font=await page.evaluate(()=>[...document.fonts].map(f=>({family:f.family,status:f.status})));
   record(name+' polices',font);assert.ok(font.some(f=>f.status==='loaded'));
   assert.ok(requests.some(([p,s])=>p.endsWith('gallery.css')&&s===200));
   assert.ok(requests.some(([p,s])=>p.endsWith('gallery.js')&&s===200));
   assert.ok(requests.every(([u])=>new URL(u).origin===base));
   await page.screenshot({path:path.join(output,name+'.png'),animations:'disabled'});
   await page.screenshot({path:path.join(output,name+'-complet.png'),fullPage:true,animations:'disabled'});
   await page.addScriptTag({path:axe});
   const scan=await page.evaluate(()=>axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}}));
   report.accessibility[name]={version:scan.testEngine.version,pass:scan.passes.length,incomplete:scan.incomplete.map(x=>({id:x.id,targets:x.nodes.map(n=>n.target)})),violations:scan.violations.map(x=>({id:x.id,nodes:x.nodes.map(n=>[n.target,n.failureSummary])}))};
   console.log('axe',name,JSON.stringify(report.accessibility[name]));
   await page.keyboard.press('Tab');
   const first=await page.locator(':focus').evaluate(e=>({name:e.textContent.trim(),href:e.getAttribute('href'),outline:getComputedStyle(e).outlineStyle}));
   assert.ok(first.href?.startsWith('#'));assert.notEqual(first.outline,'none');record(name+' premier tab',first);
   await page.keyboard.press('Enter');
   assert.equal(await page.locator(':focus').getAttribute('id'),'contenu');
   record(name+' cible saut','MAIN#contenu');

   await interactions(page,name,record);
   await context.close();
 }
 assert.deepEqual(report.errors,[]);
 assert.ok(Object.values(report.accessibility).every(x=>x.violations.length===0));
 report.result='PASS';
 }finally{await browser.close();fs.writeFileSync(path.join(output,'browser.json'),JSON.stringify(report,null,2)+'\n');}
})().catch(e=>{console.error(e);process.exitCode=1});
