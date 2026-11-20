const {chromium}=require('/home/admincsd/.npm/_npx/9833c18b2d85bc59/node_modules/playwright');
const fs=require('fs'),path=require('path'),crypto=require('crypto');
(async()=>{
  const root=path.resolve('studio/work/items/UI-004/evidence');
  const browser=await chromium.launch({
    executablePath:'/home/admincsd/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell',
    args:['--no-sandbox']
  });
  try {
    const page=await browser.newPage(),errors=[],captures=[];
    page.on('pageerror',e=>errors.push(e.message));
    await page.route('https://**',r=>r.abort());
    await page.route('http://**',r=>r.abort());
    for(const width of [1440,390]){
      await page.setViewportSize({width,height:1000});
      await page.goto('file://'+path.join(root,'prototype-adopte.html'));
      await page.evaluate(()=>document.fonts.ready);
      const name='reference-simulee-'+width+'.png';
      await page.screenshot({path:path.join(root,name),fullPage:true});
      captures.push({width,height:1000,path:name,title:await page.title(),
        nodes:await page.locator('.f-node').count(),sections:await page.locator('[data-board]').count()});
    }
    const report={
      observed_at:new Date().toISOString(),
      cwd:process.cwd(),command:'node studio/work/items/UI-004/evidence/inspect-reference.cjs',
      node:process.version,browser:browser.version(),artifact:'prototype-adopte.html',
      sha256:crypto.createHash('sha256').update(fs.readFileSync(path.join(root,'prototype-adopte.html'))).digest('hex'),
      scope:'Ouverture et inspection du prototype Notion en mode local sans réseau ; aucune recette du produit ni de gestes intégrés.',
      captures,page_errors:errors,exit_code:0
    };
    fs.writeFileSync(path.join(root,'inspection-reference.json'),JSON.stringify(report,null,2)+'\n');
    console.log(JSON.stringify(report));
  } finally {await browser.close();}
})().catch(e=>{console.error(e);process.exitCode=1});
