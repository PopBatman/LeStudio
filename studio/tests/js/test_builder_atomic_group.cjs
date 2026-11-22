/* T02: JS local model must agree with the server's atomic group contract.
 * Runs with Node.js built-ins only. No browser, network, secrets or mutation.
 */
'use strict';

const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const modulePath = path.resolve(__dirname, '../../static/ui/builder-edit-model.js');
const context = vm.createContext({ structuredClone });
vm.runInContext(
  fs.readFileSync(modulePath, 'utf8') + '\nthis.ModelUnderTest = BuilderWorkingPage;',
  context,
  { filename: modulePath },
);
const Model = context.ModelUnderTest;

function block(id, x) {
  return {
    id, definition: { scope: 'global', key: 'text', version: 1 },
    props: { text: id }, children: [],
    placement: { base: { mode: 'free', x, y: 10, width: 40, height: 80, z: 0 } },
  };
}
function fixture() {
  return new Model({
    page: {
      id: 'page-1', sections: [
        { id: 'section-1', layout: { base: { display: 'stack' } },
          blocks: [block('a', 0), block('b', 55)] },
        { id: 'section-2', layout: { base: { display: 'stack' } }, blocks: [] },
      ],
    },
    definitions: [
      { scope: 'global', key: 'text', version: 1, renderer: 'text', label: 'Texte' },
    ],
    medias: [],
  });
}
const group = {
  action: 'gesture_group',
  steps: [
    { action: 'block_place', id: 'a', format: 'base', patch: { x: 55 } },
    { action: 'block_place', id: 'b', format: 'base', patch: { x: 0 } },
  ],
};
const m = fixture();
m.preview(group);
assert.equal(m.page.sections[0].blocks[0].placement.base.x, 0);
assert.equal(m.history.length, 0);
m.commit(group, 'b');
assert.deepEqual(m.page.sections[0].blocks.map(b => b.placement.base.x), [55, 0]);
assert.equal(m.history.length, 1);
assert.equal(m.cursor, 1);
m.step(-1);
assert.deepEqual(m.page.sections[0].blocks.map(b => b.placement.base.x), [0, 55]);
m.step(1);
assert.deepEqual(m.page.sections[0].blocks.map(b => b.placement.base.x), [55, 0]);

const invalid = fixture();
const bad = {
  action: 'gesture_group', steps: [
    { action: 'block_place', id: 'a', format: 'base', patch: { x: 55 } },
    { action: 'block_place', id: 'b', format: 'base', patch: { x: 55 } },
  ],
};
assert.throws(() => invalid.commit(bad, 'b'));
assert.deepEqual(invalid.page.sections[0].blocks.map(b => b.placement.base.x), [0, 55]);
assert.equal(invalid.history.length, 0);
assert.throws(() => invalid.commit({
  action: 'gesture_group', steps: [
    group.steps[0], { action: 'block_remove', id: 'b', confirmed: true },
  ],
}, 'a'));
assert.equal(invalid.history.length, 0);

const transfer = fixture();
transfer.commit({
  action: 'gesture_group', steps: [
    { action: 'block_place', id: 'a', format: 'base', patch: {},
      parent: 'section-2', before: null },
    { action: 'block_place', id: 'b', format: 'base', patch: {},
      parent: 'section-1', before: null },
  ],
}, 'b');
assert.deepEqual(transfer.page.sections[0].blocks.map(b => b.id), ['b']);
assert.deepEqual(transfer.page.sections[1].blocks.map(b => b.id), ['a']);
transfer.step(-1);
assert.deepEqual(transfer.page.sections[0].blocks.map(b => b.id), ['a', 'b']);

console.log('T02 JS atomic-gesture model: PASS');
