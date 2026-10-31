// The studio and design-system specimens share these native controls.
export const motionFromState = state => state.explodeHold ? 'loop' : state.explodeOnHover ? 'hover' : 'still';
export function motionState(mode) {
  if (!['still', 'hover', 'loop'].includes(mode)) throw new Error('Unknown motion mode');
  return {explodeOnHover: mode === 'hover', explodeHold: mode === 'loop'};
}

export function mountMotionControl(container, {name, value = 'hover', onChange = () => {}}) {
  container.classList.add('motion-control');
  container.setAttribute('role', 'radiogroup');
  container.setAttribute('aria-label', 'Motion');
  const caption = document.createElement('span');
  caption.className = 'badge motion-label';
  caption.textContent = 'Motion';
  caption.setAttribute('aria-hidden', 'true');
  const options = document.createElement('div');
  options.className = 'motion-options';
  for (const [mode, title] of [['still', 'Still'], ['hover', 'Hover'], ['loop', 'Loop']]) {
    const label = document.createElement('label');
    label.className = 'motion-choice';
    const input = document.createElement('input');
    input.type = 'radio'; input.name = name; input.value = mode;
    const text = document.createElement('span'); text.textContent = title;
    input.addEventListener('change', () => { if (input.checked) onChange(mode); });
    label.append(input, text); options.append(label);
  }
  container.replaceChildren(options);
  const set = mode => {
    motionState(mode);
    options.querySelectorAll('input').forEach(input => { input.checked = input.value === mode; });
  };
  set(value);
  return {set};
}

export function mountViewOptions(container, {spin = false, frame = false, onChange = () => {}} = {}) {
  container.classList.add('view-options');
  const inputs = new Map();
  for (const [key, title, checked] of [['spin', 'Turntable', spin], ['frame', 'Orbit frame', frame]]) {
    const label = document.createElement('label'); label.className = 'switch';
    const input = document.createElement('input'); input.type = 'checkbox'; input.checked = checked;
    const track = document.createElement('span'); track.className = 'switch-track';
    input.addEventListener('change', () => onChange(key, input.checked));
    label.append(input, track, document.createTextNode(title)); container.append(label); inputs.set(key, input);
  }
  return {set(values) { for (const [key, checked] of Object.entries(values)) if (inputs.has(key)) inputs.get(key).checked = checked; }};
}
