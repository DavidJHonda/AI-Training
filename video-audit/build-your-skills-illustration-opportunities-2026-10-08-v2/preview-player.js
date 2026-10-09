// Keep decoded video surfaces out of idle previews. Recreate playback on demand.
const players = [...document.querySelectorAll('.preview-player')].map(root => {
  const video = root.querySelector('video');
  const button = root.querySelector('button');
  const picture = button.querySelector('img');
  const caption = button.querySelector('span');
  const status = root.querySelector('[role="status"]');
  const originalPoster = picture.src;
  let position = 0, active = false, loading = false;
  function park(reset = false) {
    if (!active) return;
    active = false;
    loading = false;
    position = reset ? 0 : video.currentTime;
    if (!reset && video.readyState >= 2) {
      try {
        const canvas = document.createElement('canvas');
        canvas.width = video.videoWidth; canvas.height = video.videoHeight;
        canvas.getContext('2d').drawImage(video, 0, 0);
        picture.src = canvas.toDataURL('image/jpeg', .9);
      } catch (_) { picture.src = originalPoster; }
    } else picture.src = originalPoster;
    video.pause();
    video.hidden = true; button.hidden = false;
    button.disabled = false;
    caption.textContent = position > 0 ? '▶ Resume current excerpt' : '▶ Play current excerpt';
    button.setAttribute('aria-label', (position > 0 ? 'Resume ' : 'Play ') + root.dataset.label + ' current excerpt');
    video.removeAttribute('src'); video.load();
  }
  button.addEventListener('click', () => {
    players.forEach(p => p.park());
    active = true; loading = true;
    status.textContent = ''; button.disabled = true;
    caption.textContent = 'Loading excerpt…';
    video.src = root.dataset.src;
    video.load();
  });
  video.addEventListener('loadedmetadata', () => {
    if (!active) return;
    if (position > 0 && position < video.duration) video.currentTime = position;
    video.play().catch(() => { park(); status.textContent = 'Playback could not start. Try again, or open the excerpt separately below.'; });
  });
  video.addEventListener('playing', () => {
    loading = false; button.hidden = true; button.disabled = false; video.hidden = false;
  });
  video.addEventListener('pause', () => { if (active && !loading) park(video.ended); });
  video.addEventListener('ended', () => { if (active) park(true); });
  video.addEventListener('error', () => {
    if (!active) return;
    park(); status.textContent = 'Playback could not load. Open the excerpt separately below.';
  });
  return {park};
});
document.addEventListener('visibilitychange', () => {
  if (document.hidden) players.forEach(p => p.park());
});
window.addEventListener('pagehide', () => players.forEach(p => p.park()));
