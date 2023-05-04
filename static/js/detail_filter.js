const ratingBtns = document.querySelectorAll('.rating-btn');
if (ratingBtns.length) {
  ratingBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const ratingFilter = btn.dataset.value;
      const url = new URL(window.location.href);
      let params = new URLSearchParams(url.search.slice(1));
      const ratingFilters = params.getAll('rating-filter');
      params.delete('rating-filter');
      if (Array.isArray(ratingFilters) && ratingFilters.length) {
        for (let i = 0; i < ratingFilters.length; i++) {
          if (ratingFilters[i] !== ratingFilter) {
            params.append('rating-filter', ratingFilters[i]);
          }
        }
      }
      if (!ratingFilters.includes(ratingFilter)) {
        params.append('rating-filter', ratingFilter);
      }
      url.search = params.toString();
      window.location.href = url.toString();
    });
  });
}

const emotionBtns = document.querySelectorAll('.emotion-btn');
if (emotionBtns.length) {
  emotionBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const emotionFilter = btn.dataset.value;
      const url = new URL(window.location.href);
      let params = new URLSearchParams(url.search.slice(1));
      const emotionFilters = params.getAll('emotion-filter');
      params.delete('emotion-filter');
      if (Array.isArray(emotionFilters) && emotionFilters.length) {
        for (let i = 0; i < emotionFilters.length; i++) {
          if (emotionFilters[i] !== emotionFilter) {
            params.append('emotion-filter', emotionFilters[i]);
          }
        }
      }
      if (!emotionFilters.includes(emotionFilter)) {
        params.append('emotion-filter', emotionFilter);
      }
      url.search = params.toString();
      window.location.href = url.toString();
    });
  });
}

const allRatingsBtn = document.querySelector('#rating-filter > button[data-value=""]');
allRatingsBtn.addEventListener('click', () => {
  const url = new URL(window.location.href);
  url.searchParams.delete('rating-filter');
  window.location.href = url.toString();
});

const allEmotionsBtn = document.querySelector('#emotion-filter > button[data-value=""]');
allEmotionsBtn.addEventListener('click', () => {
  const url = new URL(window.location.href);
  url.searchParams.delete('emotion-filter');
  window.location.href = url.toString();
});