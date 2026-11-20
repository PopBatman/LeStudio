/* Run from studio/ with node --test work/items/UI-003-05/evidence/parite-sections.cjs */
const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const Model = vm.runInThisContext(fs.readFileSync('static/ui/builder-edit-model.js','utf8') + '\nBuilderWorkingPage;');
test('Insertion avant, déplacement et annulation du retrait de toute la branche', () => {
  const branch = {id:'a',layout:{base:{display:'stack'}},blocks:[
    {id:'titre',children:[],props:{text:'Été'},definition:{key:'heading'}}]};
  const model = new Model({page:{id:'p',sections:[branch]}});
  model.commit({action:'section_add',local_id:'b',before:'a'},'b');
  assert.deepEqual(model.page.sections.map(s=>s.id),['b','a']);
  model.commit({action:'section_move',id:'a',before:'b'},'a');
  assert.deepEqual(model.page.sections.map(s=>s.id),['a','b']);
  model.commit({action:'section_add',local_id:'c'},'c');
  model.commit({action:'section_remove',id:'a',confirmed:true},'b');
  assert.deepEqual([...model.rows().keys()],['b','c']);
  assert.equal(model.step(-1),'a');
  assert.deepEqual(model.page.sections[0],branch);
  model.step(1);
  assert.deepEqual([...model.rows().keys()],['b','c']);
});
