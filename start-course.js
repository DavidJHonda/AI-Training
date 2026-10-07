// Shared entry dialog for the introduction and guest lesson. The course owns
// enrollment, validation, and browser storage; this shell only opens its form.
(() => {
  const filePreview = location.protocol === 'file:';
  // A file opened from Finder has no server to resolve the public course routes.
  // Use the real course document; avoid an iframe across opaque file origins.
  if (filePreview) {
    document.querySelectorAll('a[href="/course"]').forEach(link => { link.href = 'index.html'; });
    document.querySelectorAll('a[href="/course/why-learn-ai"]').forEach(link => { link.href = 'index.html?sample=why-learn-ai'; });
    return;
  }
  let dialog;
  let trigger;
  function knownLearner() {
    try { return !!localStorage.getItem('llm-user-name'); } catch (_) { return false; }
  }
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
    if (event.data && event.data.type === 'course-entry-size' && Number.isFinite(event.data.height)) dialog.querySelector('iframe').style.height = Math.max(280, Math.min(900, event.data.height)) + 'px';
    if (event.data && event.data.type === 'course-entered') location.assign('/course');
    if (event.data && event.data.type === 'course-entry-close') dialog.close();
  });
})();
