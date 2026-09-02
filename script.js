const filterButtons = document.querySelectorAll(".filter-button");
const projectCards = document.querySelectorAll(".project-card");
const carousel = document.querySelector("[data-project-carousel]");
const revealSections = document.querySelectorAll(".reveal-section");

filterButtons.forEach((button) => {
  button.addEventListener("click", () => {
    const filter = button.dataset.filter;

    filterButtons.forEach((item) => item.classList.remove("active"));
    button.classList.add("active");

    projectCards.forEach((card) => {
      const tags = card.dataset.tags.split(" ");
      card.classList.toggle("is-hidden", filter !== "all" && !tags.includes(filter));
    });
  });
});

if (carousel) {
  const AUTO_ROTATE_MS = 3600;
  const track = carousel.querySelector("[data-carousel-track]");
  const cards = Array.from(track.querySelectorAll(".main-project-card"));
  const previousButton = carousel.querySelector("[data-carousel-prev]");
  const nextButton = carousel.querySelector("[data-carousel-next]");
  const dotsWrap = carousel.querySelector("[data-carousel-dots]");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  let activeIndex = 0;
  let timer;

  cards.forEach((card, index) => {
    const dot = document.createElement("button");
    dot.className = "carousel-dot";
    dot.type = "button";
    dot.setAttribute("aria-label", `Show project ${index + 1}`);
    dot.addEventListener("click", () => {
      setActive(index);
      restart();
    });
    dotsWrap.appendChild(dot);
  });

  const dots = Array.from(dotsWrap.querySelectorAll(".carousel-dot"));

  function setActive(index) {
    activeIndex = (index + cards.length) % cards.length;
    const activeCard = cards[activeIndex];
    const viewport = carousel.querySelector(".carousel-viewport");
    const viewportCenter = viewport.clientWidth / 2;
    const cardCenter = activeCard.offsetLeft + activeCard.offsetWidth / 2;

    track.style.transform = `translateX(${viewportCenter - cardCenter}px)`;

    cards.forEach((card, cardIndex) => {
      const isActive = cardIndex === activeIndex;
      card.classList.toggle("is-active", isActive);
      card.setAttribute("aria-hidden", String(!isActive));
    });

    dots.forEach((dot, dotIndex) => {
      dot.classList.toggle("is-active", dotIndex === activeIndex);
      dot.setAttribute("aria-current", dotIndex === activeIndex ? "true" : "false");
    });

    if (carousel.classList.contains("is-running") && !reduceMotion.matches) {
      carousel.classList.remove("is-running");
      void carousel.offsetWidth;
      carousel.classList.add("is-running");
    }
  }

  function next() {
    setActive(activeIndex + 1);
  }

  function restart() {
    window.clearInterval(timer);
    carousel.classList.remove("is-running");

    if (reduceMotion.matches) return;

    window.requestAnimationFrame(() => {
      carousel.classList.add("is-running");
      timer = window.setInterval(next, AUTO_ROTATE_MS);
    });
  }

  previousButton.addEventListener("click", () => {
    setActive(activeIndex - 1);
    restart();
  });

  nextButton.addEventListener("click", () => {
    next();
    restart();
  });

  carousel.addEventListener("mouseenter", () => {
    window.clearInterval(timer);
    carousel.classList.remove("is-running");
  });
  carousel.addEventListener("mouseleave", restart);
  carousel.addEventListener("focusin", () => {
    window.clearInterval(timer);
    carousel.classList.remove("is-running");
  });
  carousel.addEventListener("focusout", restart);
  window.addEventListener("resize", () => setActive(activeIndex));

  setActive(0);
  restart();
}

if ("IntersectionObserver" in window) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("in-view");
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.14 }
  );

  revealSections.forEach((section) => observer.observe(section));
} else {
  revealSections.forEach((section) => section.classList.add("in-view"));
}
