// Shared entry dialog for the introduction and guest lesson. The course owns
// enrollment, validation, and browser storage; this shell only opens its form.
(() => {
  const filePreview = location.protocol === 'file:';
  function knownLearner() {
    try { return !!localStorage.getItem('llm-user-name'); } catch (_) { return false; }
  }
  function updateCourseLabels() {
    const label = knownLearner() ? 'Continue the Course' : 'Start the Course';
    document.querySelectorAll('[data-course-entry-label]').forEach(node => { node.textContent = label; });
  }
  updateCourseLabels();
  window.addEventListener('pageshow', updateCourseLabels);
  window.addEventListener('focus', updateCourseLabels);
  window.addEventListener('storage', event => {
    if (event.key === 'llm-user-name' || event.key === null) updateCourseLabels();
  });
  // A file opened from Finder has no server to resolve the public course routes.
  // Use the real course document; avoid an iframe across opaque file origins.
  if (filePreview) {
    document.querySelectorAll('a[href="/course"]').forEach(link => { link.href = 'index.html'; });
    ['whats-an-llm', 'why-learn-ai', 'for-groups'].forEach(slug => {
      document.querySelectorAll('a[href="/course/' + slug + '"]').forEach(link => { link.href = 'index.html?sample=' + slug; });
    });
    return;
  }
  let dialog;
  let trigger;
  const phoneViewport = window.matchMedia('(max-width: 760px), (pointer: coarse) and (max-height: 500px)');
  // The iframe is narrow even on desktop. Use the parent viewport to opt in.
  function syncEntryViewport() {
    const frame = dialog && dialog.querySelector('iframe');
    if (frame && frame.contentDocument && frame.contentDocument.body) {
      frame.contentDocument.body.classList.toggle('entry-phone', phoneViewport.matches);
    }
  }
  phoneViewport.addEventListener('change', syncEntryViewport);
  function openEntry(button) {
    const requireEntry = button.hasAttribute('data-entry-required');
    if (!requireEntry && knownLearner()) { location.assign('/course'); return; }
    trigger = button;
    if (!dialog) {
      dialog = document.createElement('dialog');
      dialog.className = 'start-dialog';
      dialog.setAttribute('aria-label', 'Start the course');
      dialog.innerHTML = '<button type="button" class="start-dialog-close" aria-label="Close course entry">Close ×</button><iframe title="First name and country" src="/course?entry=dialog"></iframe>';
      if (requireEntry) dialog.querySelector('iframe').src = '/course?entry=dialog&enroll=1';
      dialog.querySelector('iframe').addEventListener('load', syncEntryViewport);
      document.body.append(dialog);
      dialog.querySelector('button').addEventListener('click', () => dialog.close());
      dialog.addEventListener('click', event => {
        if (event.target === dialog) {
          const r = dialog.getBoundingClientRect();
          if (event.clientX < r.left || event.clientX > r.right || event.clientY < r.top || event.clientY > r.bottom) dialog.close();
        }
      });
      dialog.addEventListener('close', () => {
        document.body.classList.remove('entry-dialog-open');
        if (trigger) trigger.focus();
      });
    }
    syncEntryViewport();
    document.body.classList.add('entry-dialog-open');
    dialog.showModal();
  }
  document.addEventListener('click', event => {
    const link = event.target.closest('[data-start-course]');
    if (!link || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    openEntry(link);
  });
  window.addEventListener('message', event => {
    if (!dialog || !dialog.open || event.origin !== location.origin || event.source !== dialog.querySelector('iframe').contentWindow) return;
    if (event.data && event.data.type === 'course-entry-size' && Number.isFinite(event.data.height)) {
      const frame = dialog.querySelector('iframe');
      frame.style.height = Math.max(280, Math.min(900, event.data.height)) + 'px';
      if (phoneViewport.matches) {
        const menu = frame.contentDocument && frame.contentDocument.querySelector('.gate-country-menu');
        if (menu) requestAnimationFrame(() => { if (dialog.open && menu.isConnected) menu.scrollIntoView({ block: 'nearest', inline: 'nearest' }); });
      }
    }
    if (event.data && event.data.type === 'course-entered') location.assign('/course');
    if (event.data && event.data.type === 'course-entry-close') dialog.close();
  });
})();
