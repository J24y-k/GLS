// main.js – Global Animation Script

document.addEventListener('DOMContentLoaded', () => {

    // --- Intersection Observer for Scroll Animations ---
    const observerOptions = {
        // Adjust threshold as needed; 0.2 means 20% of the element must be visible
        threshold: 0.2
    };

    const animateOnScroll = (entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const el = entry.target;
                el.classList.add('animate');
                // Stop observing once the animation is triggered
                observer.unobserve(el);
            }
        });
    };

    const observer = new IntersectionObserver(animateOnScroll, observerOptions);

    // Register elements to observe
    const animatedElements = document.querySelectorAll('[data-animate]');
    if (animatedElements.length > 0) { // Check if elements exist before iterating
        animatedElements.forEach((el, index) => {
            // Apply staggered delay (optional)
            el.style.transitionDelay = `${index * 100}ms`;
            observer.observe(el);
        });
    }

    // --- Parallax Image Effect (using requestAnimationFrame for performance) ---
    const parallaxImgs = document.querySelectorAll('[data-parallax]');

    if (parallaxImgs.length > 0) { // Check if parallax elements exist
        let scrollPos = window.scrollY; // Store initial scroll position
        let ticking = false; // Flag to prevent multiple rAF calls

        const updateParallax = () => {
            parallaxImgs.forEach(img => {
                const speed = parseFloat(img.getAttribute('data-parallax')) || 0.7;
                // Apply transform based on current scroll position
                img.style.transform = `translateY(${scrollPos * speed}px)`;
            });
            ticking = false; // Reset the flag
        };

        window.addEventListener('scroll', () => {
            scrollPos = window.scrollY; // Update scroll position
            if (!ticking) {
                // Request animation frame only if not already pending
                window.requestAnimationFrame(updateParallax);
                ticking = true;
            }
        });

        // Initialize parallax effect on page load
        updateParallax();
    }
});