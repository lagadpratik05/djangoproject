document.addEventListener("DOMContentLoaded", () => {
  const revealElements = document.querySelectorAll(".reveal");

  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        const el = entry.target;
        const delay = el.dataset.delay || 0;

        if (entry.isIntersecting) {
          setTimeout(() => {
            el.classList.remove("opacity-0", "translate-y-8");
            el.classList.add("opacity-100", "translate-y-0");
          }, delay);

          observer.unobserve(el); // same as once=true
        }
      });
    },
    {
      threshold: 0.1,
      rootMargin: "0px 0px -50px 0px",
    }
  );

  revealElements.forEach((el) => {
    el.classList.add(
      "opacity-0",
      "translate-y-8",
      "transition-all",
      "duration-700",
      "ease-out"
    );
    observer.observe(el);
  });
});
