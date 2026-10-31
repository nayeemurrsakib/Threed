// Verify that saved legacy settings and the new exclusive control keep export semantics.
import assert from 'node:assert/strict';
import {motionFromState, motionState} from '../viewer/motion-controls.js';

for (const [state, expected] of [
  [{explodeOnHover:false, explodeHold:false}, 'still'],
  [{explodeOnHover:true, explodeHold:false}, 'hover'],
  [{explodeOnHover:false, explodeHold:true}, 'loop'],
  [{explodeOnHover:true, explodeHold:true}, 'loop'],
]) {
  assert.equal(motionFromState(state), expected);
  const next = {...state, ...motionState(expected)};
  assert.equal(motionFromState(next), expected);
  assert.ok(!(next.explodeOnHover && next.explodeHold), 'Only one motion mode can be active');
  // The existing Framer/portable export mapping must match the visible control.
  assert.equal(next.explodeHold ? 'loop' : next.explodeOnHover ? 'hover' : 'still', expected);
}
assert.throws(() => motionState('unknown'), /Unknown motion mode/);
console.log('PASS: legacy motion migration, exclusive modes, and embed semantics');
