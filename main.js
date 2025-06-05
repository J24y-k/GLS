// main.js – Global Animation Script

// Intersection Observer Config
const observerOptions = {
  threshold: 0.2
};

const observer = new IntersectionObserver((entries, observer) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const el = entry.target;
      el.classList.add('animate');
      observer.unobserve(el);
    }
  });
}, observerOptions);

// Register elements to observe
const animatedElements = document.querySelectorAll('[data-animate]');
animatedElements.forEach(el => observer.observe(el));

// Optional: Delay animations for staggered effect
animatedElements.forEach((el, index) => {
  el.style.transitionDelay = `${index * 100}ms`;
});

// Optional: Parallax image effect (like ColombonDT homepage)
window.addEventListener('scroll', () => {
  const parallaxImgs = document.querySelectorAll('[data-parallax]');
  parallaxImgs.forEach(img => {
    const speed = parseFloat(img.getAttribute('data-parallax')) || 0.7;
    img.style.transform = `translateY(${window.scrollY * speed}px)`;
  });
});