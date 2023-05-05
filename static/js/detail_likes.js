// Post like
const form = document.querySelector('#likes-form')
const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
form.addEventListener('submit', function (event) {
  event.preventDefault()
  const postId = event.target.dataset.postId
  axios({
    method: 'post',
    url: `/posts/${postId}/likes/`,
    headers: {'X-CSRFToken': csrftoken},
  })
    .then((response) => {
      const isLiked = response.data.is_liked
      const likeBtn = document.querySelector('#post-heart')
      
      if (isLiked === true) {
        likeBtn.classList.remove('bi-suit-heart');
        likeBtn.classList.add('bi-suit-heart-fill');
      } else {
        likeBtn.classList.remove('bi-suit-heart-fill');
        likeBtn.classList.add('bi-suit-heart');
      }
      const likesCountTag = document.querySelector('#likes-count')
      const likesCountData = response.data.likes_count
      likesCountTag.textContent = likesCountData
    })
})

// Review like
const forms = document.querySelectorAll('[id^="review-like-form-"]');
const r_csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
forms.forEach(function (form) {
  form.addEventListener('submit', function (event) {
    event.preventDefault();
    const postId = event.target.dataset.postId;
    const reviewId = event.target.dataset.reviewId;
    axios({
      method: 'post',
      url: `/posts/${postId}/reviews/${reviewId}/likes/`,
      headers: {'X-CSRFToken': r_csrftoken},
    })
    .then((response) => {
      const risLiked = response.data.r_is_liked;
      const reviewlikesCountSpan = form.nextElementSibling;
      reviewlikesCountSpan.textContent = response.data.review_likes_count;
      const heartIcon = form.querySelector('#review-heart');
      if (risLiked) {
        heartIcon.classList.remove('bi-suit-heart');
        heartIcon.classList.add('bi-suit-heart-fill');
      } else {
        heartIcon.classList.remove('bi-suit-heart-fill');
        heartIcon.classList.add('bi-suit-heart');
      }
    })
    .catch((error) => {
      console.error(error);
    });
  });
});
