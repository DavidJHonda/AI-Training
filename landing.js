// Read only: use the same consent-aware public feed as the course.
const endpoint = "https://script.google.com/macros/s/AKfycbzk24DQcbSZ-QKgwCk_g8wQbtuQaTDgs0c31Gg8cD3oKOYp4_S4SWoIOAk3kjIerhbV/exec";
const list = document.getElementById('review-list');
const summary = document.getElementById('review-summary');
const retry = document.getElementById('review-retry');
const more = document.getElementById('review-more');
let nextCursor = null;
let retryCursor = null;
async function loadReviews(cursor = null) {
  list.querySelector('.review-load-error')?.remove();
  retry.hidden = true;
  more.disabled = true;
  list.setAttribute('aria-busy', 'true');
  if (!cursor) {
    list.textContent = 'Loading student reviews…';
    summary.hidden = true;
    more.hidden = true;
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 15000);
  try {
    const response = await fetch(endpoint + '?action=public_reviews' + (cursor ? '&cursor=' + encodeURIComponent(cursor) : ''), {signal: controller.signal, cache: 'no-store', credentials: 'omit'});
    if (!response.ok) throw new Error('Review feed unavailable');
    const data = await response.json();
    if (data.error || !Array.isArray(data.reviews)) throw new Error('Invalid feed');
    const reviews = data.reviews.filter(r => typeof r.text === 'string' && r.text.trim() && Number.isInteger(r.rating) && r.rating >= 1 && r.rating <= 5);
    if (!cursor || data.reset) { list.replaceChildren(); list.scrollTop = 0; }
    nextCursor = typeof data.nextCursor === 'string' ? data.nextCursor : null;
    more.hidden = !nextCursor;
    if (!reviews.length && !list.children.length) {
      const p = document.createElement('p');
      p.className = 'review-status';
      p.textContent = 'Student reviews will appear here as they’re shared.';
      list.append(p);
    }
    for (const review of reviews) {
      const quote = document.createElement('blockquote'); quote.className = 'review';
      const stars = document.createElement('div'); stars.className = 'stars'; stars.setAttribute('role', 'img'); stars.setAttribute('aria-label', review.rating + ' out of 5 stars'); stars.textContent = '★'.repeat(review.rating) + '☆'.repeat(5-review.rating);
      const text = document.createElement('p'); text.textContent = review.text;
      const name = document.createElement('cite'); name.textContent = review.name || 'Anonymous';
      const meta = document.createElement('div'); meta.className = 'review-meta'; meta.append(name);
      const submitted = new Date(review.submittedAt);
      if (review.submittedAt && Number.isFinite(submitted.getTime())) {
        const date = document.createElement('time');
        date.dateTime = submitted.toISOString();
        date.textContent = submitted.toLocaleDateString('en-US', {month:'short', day:'numeric', year:'numeric'});
        meta.append(date);
      }
      quote.append(stars, text, meta); list.append(quote);
    }
    const ratings = data.ratingSummary;
    if (ratings && Number.isSafeInteger(ratings.total) && ratings.total > 0 && Number.isFinite(ratings.average) && ratings.average >= 1 && ratings.average <= 5) {
      summary.textContent = ratings.average.toFixed(1) + ' out of 5 · ' + ratings.total + (ratings.total === 1 ? ' rating' : ' ratings');
      summary.hidden = false;
    }
  } catch (_) {
    const p = document.createElement('p'); p.className = 'review-status';
    retryCursor = cursor;
    if (cursor && list.querySelector('.review')) {
      p.classList.add('review-load-error');
      p.textContent = 'More reviews couldn’t be loaded right now. You can try again below.';
      list.append(p);
    } else {
      p.textContent = 'Student reviews couldn’t be loaded right now.';
      list.replaceChildren(p);
      summary.hidden = true;
    }
    retry.hidden = false;
    more.hidden = true;
  } finally { clearTimeout(timeout); more.disabled = false; list.setAttribute('aria-busy', 'false'); }
}
retry.addEventListener('click', () => loadReviews(retryCursor));
more.addEventListener('click', () => loadReviews(nextCursor));
loadReviews();
