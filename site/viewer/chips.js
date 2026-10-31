// Chip builders shared by the studio and the design system page, so both render identical markup.

// A small lit sphere that previews a light preset: the highlight sits where the light comes from,
// and its colour follows the preset's warmth (cool blue-white → warm amber).
export function lightSwatch(values) {
  const az = values.azimuth ?? 0, el = values.elevation ?? 45, warm = Math.max(-1, Math.min(1, values.warmth ?? 0));
  const x = 50 + Math.sin(az * Math.PI / 180) * 32;
  const y = 50 - (el / 90 - 0.35) * 55;
  const mix = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t));
  const cool = [225, 236, 255], neutral = [255, 252, 244], amber = [255, 205, 140];
  const hl = warm >= 0 ? mix(neutral, amber, warm) : mix(neutral, cool, -warm);
  const fill = Math.max(0, Math.min(1, values.fill ?? 0.5));
  const swatch = document.createElement('span');
  swatch.className = 'light-swatch';
  swatch.setAttribute('aria-hidden', 'true');
  swatch.style.background = `radial-gradient(circle at ${x.toFixed(0)}% ${y.toFixed(0)}%, rgb(${hl}) 0%, rgb(${mix(hl, [196, 190, 178], .45)}) 28%, rgb(${mix([150, 146, 138], [205, 200, 190], fill)}) 70%, rgb(${mix([96, 92, 86], [150, 146, 138], fill)}) 100%)`;
  return swatch;
}

// A selectable light-preset chip (variant of .chip-option).
export function lightChip(name, values, pressed) {
  const b = document.createElement('button');
  b.type = 'button';
  b.className = 'chip-option light-option';
  b.dataset.light = name;
  b.setAttribute('aria-pressed', String(!!pressed));
  const label = document.createElement('span');
  label.className = 'chip-label';
  label.textContent = name;
  b.append(lightSwatch(values), label);
  return b;
}
