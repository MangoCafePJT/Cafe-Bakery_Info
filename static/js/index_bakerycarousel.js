class bakeryCarousel {
  constructor() {
    this.index = 0;
    this.$bakerycarousel = document.querySelector("#bakery-carousel");
    this.$prevButtonb = document.querySelector("#prevbtnb");
    this.$nextButtonb = document.querySelector("#nextbtnb");

    this.$prevButtonb.addEventListener("click", () => {
      this.prevb();
    });

    this.$nextButtonb.addEventListener("click", () => {
      this.nextb();
    });

  
    if (this.index === 0) {
      this.$prevButtonb.hidden = true;
    }
    
    if (this.$bakerycarousel.childElementCount <= 3) {
      this.$nextButtonb.hidden = true;
    }

    if (this.index === 0 && this.$bakerycarousel.childElementCount > 3) {
      this.$nextButtonb.hidden = false;
    }
  }

  prevb() {
    if (this.index <= 0) return;
    this.index -= 2;

    this.$bakerycarousel.style.transform = `translate3d(-${
      250 * this.index
    }px, 0, 0)`;

    if (this.index <= 0) {
      this.$prevButtonb.hidden = true;
    } else {
      this.$prevButtonb.hidden = false;
    }
    if (this.index >= this.$bakerycarousel.childElementCount - 2) {
      this.$nextButtonb.hidden = true;
    } else {
      this.$nextButtonb.hidden = false;
    }
  }

  nextb() {
    if (this.index >= this.$bakerycarousel.childElementCount - 2) return;
    this.index += 2;

    this.$bakerycarousel.style.transform = `translate3d(-${
      250 * this.index
    }px, 0, 0)`;
    if (this.index <= 0) {
      this.$prevButtonb.hidden = true;
    } else {
      this.$prevButtonb.hidden = false;
    }
    if (this.index >= this.$bakerycarousel.childElementCount - 2) {
      this.$nextButtonb.hidden = true;
    } else {
      this.$nextButtonb.hidden = false;
    }
  }
}

const bakerycarousel = new bakeryCarousel();

