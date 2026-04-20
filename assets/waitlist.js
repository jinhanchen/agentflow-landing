/* Shared Waitlist modal — openWaitlist + submitWaitlist + Esc close.
   Assumes the modal HTML block (see assets/waitlist-snippet.html) is
   present somewhere in the page before </body>. */
(function(){
  const WAITLIST_ENDPOINT = '/api/waitlist';

  window.openWaitlist = function openWaitlist() {
    if (localStorage.getItem('solarian_waitlist_joined')) {
      const toast = document.getElementById('wlToast');
      if (toast) {
        toast.classList.add('show');
        setTimeout(function(){ toast.classList.remove('show'); }, 3000);
      }
      return;
    }
    const modal = document.getElementById('waitlistModal');
    if (modal) modal.classList.add('open');
  };

  window.submitWaitlist = function submitWaitlist(e) {
    e.preventDefault();
    const form = document.getElementById('waitlistForm');
    const btn = document.getElementById('wlSubmitBtn');
    if (!form || !btn) return false;
    const data = Object.fromEntries(new FormData(form));

    btn.classList.add('loading');
    btn.querySelector('span').textContent = '提交中...';

    fetch(WAITLIST_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    }).then(r => {
      if (r.ok) {
        localStorage.setItem('solarian_waitlist_joined', '1');
        form.style.display = 'none';
        const header = document.querySelector('.wl-header');
        if (header) header.style.display = 'none';
        const success = document.getElementById('wlSuccess');
        if (success) success.style.display = 'block';
      } else { throw new Error('fail'); }
    }).catch(() => {
      btn.classList.remove('loading');
      btn.querySelector('span').textContent = '提交失败，请重试';
      setTimeout(() => {
        btn.classList.remove('loading');
        btn.querySelector('span').textContent = '提交申请';
      }, 3000);
    });

    return false;
  };

  document.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      const m = document.getElementById('waitlistModal');
      if (m) m.classList.remove('open');
    }
  });
})();
