// Counts download clicks (GoatCounter, when set up) and offers an optional email box after a download.
// The download always starts right away; the email box never blocks it.
(() => {
  const cfg = window.LC_CFG || {};
  const count = name => { try { window.goatcounter && window.goatcounter.count({ path: name, title: name, event: true }); } catch {} };
  const kind = a => {
    const h = a.getAttribute('href') || '';
    if (/LoopCast-Setup\.exe/i.test(h)) return 'download-windows';
    if (/LoopCast-Mac\.dmg/i.test(h)) return 'download-mac';
    if (/^\/app\/?$/.test(h)) return 'open-in-browser';
    return null;
  };
  let asked = false;
  try { asked = localStorage.getItem('lc-email-asked') === '1'; } catch {}

  function emailBox(platform) {
    if (!cfg.form || asked) return;
    asked = true; try { localStorage.setItem('lc-email-asked', '1'); } catch {}
    const wrap = document.createElement('div');
    wrap.className = 'lc-modal';
    wrap.innerHTML = `
      <div class="lc-box" role="dialog" aria-modal="true" aria-labelledby="lcT">
        <p class="lc-k">Your download has started</p>
        <h2 id="lcT">Want launch news and tips?</h2>
        <p>Leave your email and we’ll send the occasional update: new features, and a heads-up before anything about pricing changes. No spam.</p>
        <form method="post" target="lc-sink">
          <label class="sr" for="lcE">Email</label>
          <input id="lcE" type="email" required autocomplete="email" placeholder="you@example.com">
          <div class="lc-act"><button type="button" class="btn ghost sm lc-no">No thanks</button><button type="submit" class="btn solid sm">Send</button></div>
        </form>
        <p class="lc-done" hidden>Thanks! You’re on the list.</p>
      </div>
      <iframe name="lc-sink" title="" hidden></iframe>`;
    const form = wrap.querySelector('form'), input = wrap.querySelector('input');
    form.action = cfg.form.action;
    input.name = cfg.form.field || 'email';
    const close = () => { wrap.remove(); document.removeEventListener('keydown', esc); };
    const esc = e => { if (e.key === 'Escape') close(); };
    document.addEventListener('keydown', esc);
    wrap.addEventListener('click', e => { if (e.target === wrap) close(); });
    wrap.querySelector('.lc-no').onclick = () => { count('email-declined'); close(); };
    form.addEventListener('submit', () => {
      count('email-signup-' + platform);
      setTimeout(() => { form.hidden = true; wrap.querySelector('.lc-done').hidden = false; setTimeout(close, 2200); }, 300);
    });
    document.body.appendChild(wrap);
    setTimeout(() => input.focus(), 50);
  }

  document.addEventListener('click', e => {
    const a = e.target.closest('a[href]'); if (!a) return;
    const k = kind(a); if (!k) return;
    count(k);
    if (k !== 'open-in-browser') setTimeout(() => emailBox(k.replace('download-', '')), 600);
  });
})();
