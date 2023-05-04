const stars = document.querySelectorAll('.star-rating label');
const ratingInput = document.querySelector('input[name="rating"]');

ratingInput.value = 5;
stars.forEach(star => star.classList.add('rating--orange'));

stars.forEach((star, index) => {
  star.addEventListener('click', () => {
    ratingInput.value = index + 1;
    for (let i = 0; i < stars.length; i++) {
      if (i <= index) {
        stars[i].classList.remove('rating--gray');
        stars[i].classList.add('rating--orange');
      } else {
        stars[i].classList.remove('rating--orange');
        stars[i].classList.add('rating--gray');
      }
    }
  });
});

const emojis = document.querySelectorAll('.emoji-rating label');
const emotionInput = document.querySelector('input[name="emotion"]');

emojis.forEach(emoji => emoji.addEventListener('click', () => {
  emotionInput.value = emoji.getAttribute('for').split('-')[1];
  emojis.forEach(e => e.classList.remove('selected'));
  emoji.classList.add('selected');
}));