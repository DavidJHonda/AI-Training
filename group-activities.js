// The splash page and For Groups read the same course-wide directory.
(() => {
  let dialog, trigger, previousOverflow;
  const node = (tag, text, className) => {
    const el = document.createElement(tag);
    if (text) el.textContent = text;
    if (className) el.className = className;
    return el;
  };
  function createDirectory() {
    dialog = node('dialog', '', 'group-directory-dialog');
    dialog.setAttribute('aria-labelledby', 'group-directory-title');
    const header = node('div', '', 'group-directory-header');
    const title = node('h2', 'Group Activities');
    title.id = 'group-directory-title';
    const close = node('button', 'Close');
    close.type = 'button';
    close.addEventListener('click', () => dialog.close());
    header.append(title, close);
    const intro = node('p', 'Learning with a club or class? Try these activities and discussions together. Each opens in a new tab, with no course registration needed.', 'group-directory-intro');
    const activities = window.COURSE_GROUP_ACTIVITIES;
    const sections = [...new Set(activities.map(activity => activity.section))];
    let selectedType = 'All';
    const controls = node('div', '', 'group-directory-controls');
    const types = node('div', '', 'group-directory-filters');
    types.setAttribute('role', 'group');
    types.setAttribute('aria-label', 'Activity type');
    ['All', 'Activity', 'Discussion'].forEach(type => {
      const count = activities.filter(activity => type === 'All' || activity.type === type).length;
      const label = type === 'All' ? 'All' : type === 'Activity' ? 'Activities' : 'Discussions';
      const button = node('button', label + ' ' + count);
      button.type = 'button';
      button.dataset.type = type;
      button.setAttribute('aria-pressed', String(type === selectedType));
      button.addEventListener('click', () => {
        selectedType = type;
        types.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
        render();
      });
      types.append(button);
    });
    const sectionSelect = node('select');
    sectionSelect.setAttribute('aria-label', 'Course section');
    const allSections = node('option', 'All sections');
    allSections.value = '';
    sectionSelect.append(allSections);
    sections.forEach(section => {
      const option = node('option', section);
      option.value = section;
      sectionSelect.append(option);
    });
    sectionSelect.addEventListener('change', render);
    const search = node('input');
    search.type = 'search';
    search.placeholder = 'Search activities';
    search.setAttribute('aria-label', 'Search activities');
    search.addEventListener('input', render);
    controls.append(types, sectionSelect, search);
    const status = node('p', '', 'group-directory-status');
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    const results = node('div', '', 'group-directory-results');
    function render() {
      const query = search.value.trim().toLocaleLowerCase();
      const matches = activities.filter(activity =>
        (selectedType === 'All' || activity.type === selectedType) &&
        (!sectionSelect.value || activity.section === sectionSelect.value) &&
        [activity.title, activity.note, activity.lessonTitle, activity.section, activity.type].join(' ').toLocaleLowerCase().includes(query)
      );
      results.replaceChildren();
      status.textContent = matches.length + ' of ' + activities.length + ' activities and discussions shown';
      if (!matches.length) {
        results.append(node('p', 'No activities match. Try another search or change the filters.', 'group-directory-empty'));
        return;
      }
      sections.forEach(section => {
        const entries = matches.filter(activity => activity.section === section);
        if (!entries.length) return;
        const group = node('section', '', 'group-directory-section');
        const heading = node('h3', section);
        heading.append(node('span', entries.length + ' in this section'));
        const list = node('ul', '', 'group-directory-rows');
        entries.forEach(activity => {
          const item = node('li');
          item.append(node('span', activity.type, 'group-directory-badge ' + (activity.type === 'Discussion' ? 'is-discussion' : 'is-activity')));
          const description = node('div', '', 'group-directory-description');
          description.append(node('h4', activity.title), node('p', activity.note));
          const related = node('p', '', 'group-directory-related');
          related.append(node('span', 'Related lesson:'), node('span', activity.lessonTitle));
          const link = node('a', activity.type === 'Discussion' ? 'Open discussion ↗' : 'Open activity ↗');
          link.href = activity.href;
          link.target = '_blank';
          link.rel = 'noopener noreferrer';
          link.setAttribute('aria-label', 'Open ' + activity.title + ' (opens in a new tab)');
          item.append(description, related, link);
          list.append(item);
        });
        group.append(heading, list);
        results.append(group);
      });
    }
    render();
    dialog.append(header, intro, controls, status, results);
    dialog.addEventListener('close', () => {
      document.body.style.overflow = previousOverflow;
      if (trigger && trigger.isConnected) trigger.focus();
    });
    document.body.append(dialog);
  }
  document.addEventListener('click', event => {
    const link = event.target.closest('[data-group-directory]');
    if (!link || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    if (!dialog) createDirectory();
    trigger = link;
    previousOverflow = document.body.style.overflow;
    dialog.showModal();
    document.body.style.overflow = 'hidden';
  });
})();
