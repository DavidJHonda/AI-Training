// Shared contact dialog for the landing page and course. Drafts stay in memory.
(() => {
  const endpoint = 'https://script.google.com/macros/s/AKfycbzk24DQcbSZ-QKgwCk_g8wQbtuQaTDgs0c31Gg8cD3oKOYp4_S4SWoIOAk3kjIerhbV/exec';
  let dialog, trigger, form, status, fields, sendButton;
  let reportId, busy = false, previousOverflow = '';
  function createDialog() {
    dialog = document.createElement('dialog');
    dialog.className = 'course-contact-dialog';
    dialog.setAttribute('aria-labelledby', 'course-contact-title');
    dialog.innerHTML = `
      <div class="course-contact-heading"><h2 id="course-contact-title">Contact Us</h2><button type="button" class="course-contact-close">Close</button></div>
      <p class="course-contact-intro">Have a question, an idea, or something to share? We’d love to hear from you.</p>
      <form>
        <fieldset>
          <label for="course-contact-name">Name <span>(optional)</span></label>
          <input id="course-contact-name" name="name" autocomplete="name" maxlength="100">
          <label for="course-contact-email">Email address</label>
          <input id="course-contact-email" name="email" type="email" autocomplete="email" maxlength="254" required aria-describedby="course-contact-privacy">
          <p id="course-contact-privacy" class="course-contact-hint">We’ll only use your email address to reply to your message.</p>
          <label for="course-contact-message">Message</label>
          <textarea id="course-contact-message" name="message" rows="5" maxlength="5000" required></textarea>
          <div class="course-contact-trap" aria-hidden="true"><label>Leave this empty<input name="website" tabindex="-1" autocomplete="off"></label></div>
          <button class="course-contact-send" type="submit">Send message</button>
        </fieldset>
      </form>
      <p class="course-contact-status" role="status" aria-live="polite" tabindex="-1" hidden></p>
      <button class="course-contact-another" type="button" hidden>Send another message</button>
      <p class="course-contact-alternative">Or email <a href="mailto:besmarterthanthetool@gmail.com">besmarterthanthetool@gmail.com</a>.</p>`;
    document.body.append(dialog);
    form = dialog.querySelector('form');
    fields = dialog.querySelector('fieldset');
    status = dialog.querySelector('.course-contact-status');
    sendButton = dialog.querySelector('.course-contact-send');
    dialog.querySelector('.course-contact-close').addEventListener('click', () => dialog.close());
    dialog.addEventListener('close', () => {
      document.body.style.overflow = previousOverflow;
      if (trigger && trigger.isConnected) trigger.focus();
    });
    form.addEventListener('input', () => {
      if (busy) return;
      reportId = null;
      status.hidden = true;
    });
    dialog.querySelector('.course-contact-another').addEventListener('click', () => {
      form.hidden = false;
      dialog.querySelector('.course-contact-intro').hidden = false;
      status.hidden = true;
      dialog.querySelector('.course-contact-another').hidden = true;
      form.elements.name.focus();
    });
    form.addEventListener('submit', async event => {
      event.preventDefault();
      if (busy) return;
      const email = form.elements.email.value.trim();
      const message = form.elements.message.value.trim();
      form.elements.message.setCustomValidity(message ? '' : 'Please enter your message.');
      if (!form.reportValidity()) return;
      const controller = new AbortController();
      const timeout = setTimeout(() => controller.abort(), 20000);
      busy = true;
      fields.disabled = true;
      form.setAttribute('aria-busy', 'true');
      sendButton.textContent = 'Sending…';
      status.hidden = false;
      status.classList.remove('is-error');
      status.textContent = 'Sending your message…';
      try {
        if (!reportId) reportId = crypto.randomUUID();
        let clientId = reportId;
        try {
          clientId = localStorage.getItem('llm-contact-client') || crypto.randomUUID();
          localStorage.setItem('llm-contact-client', clientId);
        } catch (_) {}
        // Older deployments treat unknown events as enrollments. Never POST first.
        const ready = await fetch(endpoint + '?action=contact_status', { signal: controller.signal, cache: 'no-store', credentials: 'omit' });
        if (!ready.ok || (await ready.text()).trim() !== 'contact-ready') throw new Error('Contact unavailable');
        const response = await fetch(endpoint, {
          method: 'POST', headers: { 'Content-Type': 'text/plain;charset=utf-8' },
          credentials: 'omit', signal: controller.signal,
          body: JSON.stringify({ eventType: 'course_contact', reportId, clientId,
            name: form.elements.name.value.trim(), email, message, website: form.elements.website.value })
        });
        if (!response.ok || (await response.text()).trim() !== 'contact-ok') throw new Error('Contact not confirmed');
        form.reset();
        form.hidden = true;
        dialog.querySelector('.course-contact-intro').hidden = true;
        reportId = null;
        status.textContent = 'Thanks! Your message has been sent. We can reply to the email address you provided.';
        dialog.querySelector('.course-contact-another').hidden = false;
      } catch (_) {
        status.classList.add('is-error');
        status.textContent = 'We couldn’t confirm that your message was sent. Your message is still here. Please try again shortly, or email us directly below.';
      } finally {
        clearTimeout(timeout);
        busy = false;
        fields.disabled = false;
        form.removeAttribute('aria-busy');
        sendButton.textContent = 'Send message';
        if (dialog.open) status.focus();
      }
    });
    form.elements.message.addEventListener('input', () => form.elements.message.setCustomValidity(''));
  }
  document.addEventListener('click', event => {
    const link = event.target.closest('[data-course-contact]');
    if (!link || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    if (!dialog) createDialog();
    if (dialog.open) return;
    trigger = link;
    previousOverflow = document.body.style.overflow;
    dialog.showModal();
    document.body.style.overflow = 'hidden';
  });
})();
