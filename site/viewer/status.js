// Footer status: green while everything works, red (with the reason) as soon as something breaks.
// Watches script errors, failed loads (models, images, styles, scripts, data), WebGL support,
// the studio's own load state and connectivity. Only elements marked data-live are updated.
const issues = new Map();
// Optional files are allowed to be missing without raising an alarm.
const OPTIONAL = ['assets/brand/nayeemur-r-s-3d.png'];
const optional = url => OPTIONAL.some(o => String(url).includes(o));
const els = () => document.querySelectorAll('.site-status[data-live]');

function render() {
  const list = [...issues.values()];
  for (const el of els()) {
    const ok = list.length === 0;
    el.dataset.status = ok ? 'ok' : 'error';
    el.querySelector('.status-text').textContent = ok ? 'ALL SYSTEMS OPERATIONAL' : (navigator.onLine ? 'SOMETHING WENT WRONG' : 'YOU ARE OFFLINE');
    el.title = ok ? 'Everything is loading and running normally.' : list.join('\n');
    el.setAttribute('aria-label', ok ? 'Status: all systems operational' : `Status: problem detected. ${list.join('. ')}`);
  }
}
const flag = (key, message) => { if (!issues.has(key)) { issues.set(key, message); render(); } };
const clear = key => { if (issues.delete(key)) render(); };
const short = url => { try { const u = new URL(url, location.href); return u.pathname.split('/').pop() || u.pathname; } catch { return String(url); } };

// Script errors and rejected promises (ignore aborted view transitions, which are harmless).
addEventListener('error', e => {
  const t = e.target;
  if (t && t !== window && (t.src || t.href)) { if (optional(t.src || t.href)) return; flag(`load:${t.src || t.href}`, `Could not load ${short(t.src || t.href)}`); return; }
  if (e.message) flag(`js:${e.message}`, `Script error: ${e.message}`);
}, true);
addEventListener('unhandledrejection', e => {
  const r = e.reason; const msg = r?.message || String(r);
  if (r?.name === 'AbortError' || /Transition was aborted/i.test(msg)) return;
  flag(`promise:${msg}`, `Error: ${msg}`);
});

// Failed network requests (fetches of models, catalog, presets), including ones made before this script ran.
const checkEntry = e => { if (e.responseStatus >= 400 && !optional(e.name)) flag(`http:${e.name}`, `Could not load ${short(e.name)} (${e.responseStatus})`); };
try { performance.getEntriesByType('resource').forEach(checkEntry); new PerformanceObserver(l => l.getEntries().forEach(checkEntry)).observe({ type: 'resource', buffered: true }); } catch {}

// WebGL 2 is required for the live 3D view.
if (document.querySelector('#canvas, little-object')) {
  try { if (!document.createElement('canvas').getContext('webgl2')) flag('webgl', 'This browser cannot show live 3D (WebGL 2 unavailable)'); } catch { flag('webgl', 'This browser cannot show live 3D (WebGL 2 unavailable)'); }
}

// The studio reports its own load state on <html data-ready>.
const watchReady = () => { const s = document.documentElement.dataset.ready; if (s === 'error') flag('studio', `The 3D object could not load: ${document.getElementById('loading')?.textContent || 'unknown error'}`); else if (s === 'true') clear('studio'); };
new MutationObserver(watchReady).observe(document.documentElement, { attributes: true, attributeFilter: ['data-ready'] });
watchReady();

// Connectivity.
const net = () => navigator.onLine ? clear('offline') : flag('offline', 'No internet connection');
addEventListener('online', net); addEventListener('offline', net); net();

render();

// Credit avatar: use the generated PNG when it exists, otherwise keep the drawn SVG.
fetch('assets/brand/nayeemur-r-s-3d.png', { method: 'HEAD', cache: 'no-cache' }).then(r => {
  if (r.ok) document.documentElement.style.setProperty('--credit-avatar', 'url(assets/brand/nayeemur-r-s-3d.png)');
}).catch(() => {});
