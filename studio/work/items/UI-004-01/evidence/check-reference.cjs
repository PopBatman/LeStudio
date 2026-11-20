const {chromium}=require('/home/admincsd/.npm/_npx/9833c18b2d85bc59/node_modules/playwright');
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
(async()=>{
 const root=path.resolve('studio/work/items/UI-004-01/evidence'),errors=[],network=[];
 const browser=await chromium.launch({executablePath:'/home/admincsd/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell',args:['--no-sandbox']});
 try{
 const page=await browser.newPage({viewport:{width:1440,height:1100}});
 page.on('pageerror',e=>errors.push(e.message));
 await page.route(/^https?:/,r=>{network.push(r.request().url());return r.abort();});
 await page.goto('file://'+path.join(root,'comparaison-reference.html'));
 await page.frameLocator('#render').locator('[data-studio-block-id="884f1547-70f2-4abb-b075-8a3a30cf4020"]').waitFor();
 assert.equal(await page.frameLocator('#render').locator('[data-studio-block-id="884f1547-70f2-4abb-b075-8a3a30cf4020"] p').innerText(),'xqqsx');
 await page.screenshot({path:path.join(root,'comparaison-bureau.png'),fullPage:true});
 await page.locator('[data-width="390"]').click();
 assert.equal(await page.locator('#render').evaluate(e=>e.offsetWidth),390);
 await page.locator('#long').focus();await page.keyboard.press('Enter');
 await page.waitForFunction(()=>document.getElementById('long').getAttribute('aria-pressed')==='true');
 assert((await page.frameLocator('#render').locator('[data-studio-block-id="884f1547-70f2-4abb-b075-8a3a30cf4020"] p').innerText()).length>100);
 await page.locator('[data-panel="gestures"]').focus();await page.keyboard.press('Enter');
 assert(await page.locator('#gestures').isVisible());assert(await page.locator('#compare').isHidden());
 await page.locator('[data-panel="pilot"]').click();assert(await page.locator('#pilot').isVisible());
 await page.screenshot({path:path.join(root,'reference-pilote.png'),fullPage:true});
 await page.locator('[data-panel="compare"]').click();await page.locator('#long').click();
 await page.setViewportSize({width:390,height:1000});
 await page.frameLocator('#render').locator('[data-studio-block-id="884f1547-70f2-4abb-b075-8a3a30cf4020"] p').waitFor();
 assert.equal(await page.frameLocator('#render').locator('[data-studio-block-id="884f1547-70f2-4abb-b075-8a3a30cf4020"] p').innerText(),'xqqsx');
 await page.screenshot({path:path.join(root,'comparaison-mobile.png'),fullPage:true});
 assert.equal(errors.length,0);assert.equal(network.length,0);
 const r={observed_at:new Date().toISOString(),command:'node studio/work/items/UI-004-01/evidence/check-reference.cjs',node:process.version,browser:browser.version(),result:'passed',assertions:['contenu initial R18 identique','largeur mobile 390','variante longue locale >100 caractères','onglets et bouton accessibles via Enter','aucune requête réseau','aucune erreur JS'],errors,network,scope:'Rapport de référence simulé ; pas un test du nouvel éditeur'};
 fs.writeFileSync(path.join(root,'check-reference.json'),JSON.stringify(r,null,2)+'\n');console.log(JSON.stringify(r));
 }finally{await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
