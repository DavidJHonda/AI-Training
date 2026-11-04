(() => {
  const root = document.getElementById('group-session');
  const activities = window.COURSE_GROUP_ACTIVITIES;
  const id = new URLSearchParams(location.search).get('id');
  const activity = activities.find(a => a.id === id);
  const node = (tag, text, className) => {
    const el = document.createElement(tag);
    if (text) el.textContent = text;
    if (className) el.className = className;
    return el;
  };
  root.replaceChildren();
  const back = node('a', 'All group activities', 'back-link');
  back.href = 'group-session.html';
  if (!activity) {
    root.append(node('h1', 'Group Activities'), node('p', 'Activities and discussions to try with your club or class. No course registration needed.'));
    if (id) root.append(node('p', 'That activity wasn’t found. Choose one from the list below.'));
    const list = node('ol', '', 'questions');
    activities.forEach(a => {
      const li = node('li');
      const link = node('a', a.title);
      link.href = '../' + a.href;
      li.append(node('p', a.type + ' · ' + a.section + ' · ' + a.lessonTitle, 'eyebrow'), link, node('p', a.note));
      list.append(li);
    });
    root.append(list);
    return;
  }
  const typeLabel = activity.type === 'Discussion' ? 'Discussion Questions' : activity.type;
  document.title = activity.title + ' · ' + (activity.type === 'Discussion' ? typeLabel : 'Group Activities');
  root.append(back, node('p', typeLabel + ' · ' + activity.section, 'eyebrow'), node('h1', activity.title), node('p', 'Related lesson: ' + activity.lessonTitle, 'group-session-meta'), node('p', activity.note));
  if (activity.questions) {
    root.append(node('p', 'Choose a question to discuss. Use the follow-ups if they help the conversation.'));
    const panel = node('div', '', 'discussion-panel');
    const list = node('ol', '', 'questions discussion-questions');
    list.setAttribute('role', 'list');
    activity.questions.forEach((q, i) => {
      const li = node('li', '', 'discussion-question');
      const number = node('span', String(i + 1), 'discussion-question-number');
      number.setAttribute('aria-hidden', 'true');
      const copy = node('div', '', 'discussion-question-copy');
      if (q.context) copy.append(node('p', q.context));
      copy.append(node('h2', q.title));
      if (q.followUp) {
        const followUp = node('p', '', 'discussion-question-follow-up');
        const arrow = node('span', '↳', 'discussion-question-follow-up-arrow');
        arrow.setAttribute('aria-hidden', 'true');
        followUp.append(arrow, node('span', q.followUp));
        copy.append(followUp);
      }
      li.append(number, copy);
      list.append(li);
    });
    panel.append(list);
    root.append(panel);
  } else if (activity.id === 'studying') {
    root.append(node('p', 'Your group leader can use a shared screen or let smaller groups try their own combinations.'));
    const steps = node('ol');
    activity.instructions.forEach(text => steps.append(node('li', text)));
    root.append(steps);
    const builder = node('div', '', 'study-builder');
    function field(id, labelText, placeholder) {
      const label = node('label', labelText); label.htmlFor = id;
      const input = node('input'); input.id = id; input.placeholder = placeholder; input.maxLength = 300;
      builder.append(label, input);
      return input;
    }
    const subject = field('study-subject', 'What do you want to learn?', 'For example, gravity or negotiation');
    const situation = field('study-situation', 'What’s the ridiculous situation?', 'For example, penguins running a theme park');
    const prompt = node('textarea'); prompt.readOnly = true; prompt.setAttribute('aria-label', 'Prompt to copy');
    const copy = node('button', 'Copy Prompt'); copy.type = 'button'; copy.disabled = true;
    const launch = node('a', 'Open Study Mode ↗', 'launch'); launch.href = 'https://chatgpt.com/studymode'; launch.target = '_blank'; launch.rel = 'noopener noreferrer';
    const feedback = node('p'); feedback.setAttribute('role', 'status');
    function update() {
      prompt.value = 'Teach us ' + (subject.value.trim() || '[subject]') + ' using ' + (situation.value.trim() || '[ridiculous situation]') + '.\nWe’re high school students. Ask us one question at a time and wait for our answer.';
      copy.disabled = !subject.value.trim() || !situation.value.trim();
      feedback.textContent = '';
    }
    subject.addEventListener('input', update); situation.addEventListener('input', update);
    copy.addEventListener('click', async () => {
      try { await navigator.clipboard.writeText(prompt.value); feedback.textContent = 'Prompt copied. Open Study Mode and paste it into the chat.'; }
      catch (_) { prompt.focus(); prompt.select(); feedback.textContent = 'Select and copy the prompt above.'; }
    });
    update(); builder.append(prompt, copy, launch, feedback); root.append(builder);
    root.append(node('h2', 'Afterward'), node('p', 'What can you explain now that you couldn’t explain before?'));
  } else {
    const link = node('a', 'Open activity →', 'launch'); link.href = '../' + activity.href; root.append(link);
  }
  root.append(node('p', 'Close this tab to return to the page you came from.', 'session-footer'));
})();
