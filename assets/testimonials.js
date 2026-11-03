// "What people say" on the home page.
// Real quotes only: add one to QUOTES below after the person has said it's OK to share.
//   { quote: 'What they said.', name: 'Their name', role: 'Role, Organization' }
// While the list is empty the section only shows the "Share your experience" invitation.
(() => {
  const QUOTES = [
  ];

  const sec = document.getElementById('words');
  if (!sec) return;
  const esc = s => String(s || '').replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' })[c]);
  const list = sec.querySelector('.quotes');
  if (QUOTES.length) {
    sec.classList.add('has');
    list.innerHTML = QUOTES.map(q => `<figure class="quote"><blockquote>“${esc(q.quote)}”</blockquote><figcaption><b>${esc(q.name)}</b>${q.role ? `<span>${esc(q.role)}</span>` : ''}</figcaption></figure>`).join('');
    list.hidden = false;
  }

  // The share form: a LoopCast-styled dialog. Messages are emailed to hello@loopcast.space;
  // nothing appears on the site until it's added to QUOTES above.
  const ENDPOINT = 'https://formsubmit.co/ajax/hello@loopcast.space';
  const count = name => { try { window.goatcounter && window.goatcounter.count({ path: name, title: name, event: true }); } catch {} };

  function open() {
    const wrap = document.createElement('div');
    wrap.className = 'lc-modal';
    wrap.innerHTML = `
      <div class="lc-box share" role="dialog" aria-modal="true" aria-labelledby="shT">
        <p class="lc-k">Share your experience</p>
        <h2 id="shT">How did LoopCast work for you?</h2>
        <p>A sentence or two is plenty. We read every one.</p>
        <form novalidate>
          <label for="shMsg">What you used it for, and how it went</label>
          <textarea id="shMsg" name="message" rows="4" required maxlength="1200" placeholder="We ran our walk-in slides at a 300-person conference…"></textarea>
          <div class="sh-two">
            <div><label for="shName">Your name</label><input id="shName" name="name" required maxlength="80" autocomplete="name"></div>
            <div><label for="shRole">Role and organization <small>(optional)</small></label><input id="shRole" name="role" maxlength="120" placeholder="Media director, First Church"></div>
          </div>
          <label for="shEmail">Email <small>(optional, never shown)</small></label>
          <input id="shEmail" name="email" type="email" maxlength="120" autocomplete="email">
          <label class="sh-ok"><input type="checkbox" name="ok_to_share" value="yes" checked> It’s OK to show my words and name on loopcast.space</label>
          <input type="text" name="_honey" class="sr" tabindex="-1" autocomplete="off" aria-hidden="true">
          <p class="sh-err" role="alert" hidden></p>
          <div class="lc-act"><button type="button" class="btn ghost sm sh-no">Cancel</button><button type="submit" class="btn solid sm">Send</button></div>
        </form>
        <div class="sh-done" hidden><h2>Thank you!</h2><p>Your note is on its way. If you said it’s OK to share, it may show up on the site soon.</p><div class="lc-act"><button type="button" class="btn solid sm sh-no">Close</button></div></div>
      </div>`;
    const form = wrap.querySelector('form'), err = wrap.querySelector('.sh-err'), send = form.querySelector('[type=submit]');
    const close = () => { wrap.remove(); document.removeEventListener('keydown', esc2); btn.focus(); };
    const esc2 = e => { if (e.key === 'Escape') close(); };
    document.addEventListener('keydown', esc2);
    wrap.addEventListener('click', e => { if (e.target === wrap || e.target.closest('.sh-no')) close(); });
    form.addEventListener('submit', async e => {
      e.preventDefault();
      const f = new FormData(form);
      const msg = (f.get('message') || '').trim(), name = (f.get('name') || '').trim();
      if (!msg || !name) { err.textContent = !msg ? 'Write a sentence or two first.' : 'Add your name, please.'; err.hidden = false; (msg ? form.name : form.message).focus(); return; }
      const email = (f.get('email') || '').trim();
      if (email && !form.email.checkValidity()) { err.textContent = 'That email doesn’t look right. You can also leave it empty.'; err.hidden = false; form.email.focus(); return; }
      err.hidden = true; send.disabled = true; send.textContent = 'Sending…';
      try {
        const r = await fetch(ENDPOINT, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
          body: JSON.stringify({
            _subject: 'LoopCast testimonial from ' + name,
            _template: 'table', _captcha: 'false', _honey: f.get('_honey') || '',
            name, role: (f.get('role') || '').trim(), email, message: msg,
            ok_to_share: f.get('ok_to_share') ? 'Yes' : 'No', page: location.href,
          }),
        });
        if (!r.ok) throw new Error(r.status);
        count('testimonial-sent');
        form.hidden = true; wrap.querySelector('.share > .lc-k').hidden = true; wrap.querySelector('#shT').hidden = true;
        wrap.querySelector('.share > p:not(.lc-k)').hidden = true;
        const done = wrap.querySelector('.sh-done'); done.hidden = false; done.querySelector('button').focus();
      } catch {
        err.textContent = 'That didn’t go through. Try again in a moment, or email hello@loopcast.space.';
        err.hidden = false; send.disabled = false; send.textContent = 'Send';
      }
    });
    document.body.appendChild(wrap);
    form.message.focus();
  }
  const btn = sec.querySelector('.share-btn');
  btn.addEventListener('click', open);
})();
