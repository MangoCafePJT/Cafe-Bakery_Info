class cafeCarousel {
  constructor() {
    this.index = 0;
    this.$carousel = document.querySelector("#cafe-carousel");
    this.$prevButton = document.querySelector("#prevbtn");
    this.$nextButton = document.querySelector("#nextbtn");

    this.$prevButton.addEventListener("click", () => {
      this.prev();
    });

    this.$nextButton.addEventListener("click", () => {
      this.next();
    });

    if (this.index === 0) {
      this.$prevButton.hidden = true;
    }
    
    if (this.$carousel.childElementCount <= 3) {
      this.$nextButton.hidden = true;
    }

    if (this.index === 0 && this.$carousel.childElementCount > 3) {
      this.$nextButton.hidden = false;
    }
  }

  prev() {
    if (this.index <= 0) return;
    this.index -= 2;

    this.$carousel.style.transform = `translate3d(-${
      250 * this.index
    }px, 0, 0)`;

    if (this.index <= 0) {
      this.$prevButton.hidden = true;
    } else {
      this.$prevButton.hidden = false;
    }
    if (this.index >= this.$carousel.childElementCount - 2) {
      this.$nextButton.hidden = true;
    } else {
      this.$nextButton.hidden = false;
    }
  }

  next() {
    if (this.index >= this.$carousel.childElementCount - 2) return;
    this.index += 2;

    this.$carousel.style.transform = `translate3d(-${
      250 * this.index
    }px, 0, 0)`;
    if (this.index <= 0) {
      this.$prevButton.hidden = true;
    } else {
      this.$prevButton.hidden = false;
    }
    if (this.index >= this.$carousel.childElementCount - 2) {
      this.$nextButton.hidden = true;
    } else {
      this.$nextButton.hidden = false;
    }
  }
}

const cafecarousel = new cafeCarousel();