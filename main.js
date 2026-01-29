// ==========================================================================
// GLS Refrigeration and Air Conditioning - Main JavaScript
// Enhanced animation and interaction script
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {

  // ==========================================================================
  // Intersection Observer for Scroll Animations
  // ==========================================================================
  
  const observerOptions = {
    threshold: 0.15, // Trigger when 15% of element is visible
    rootMargin: '0px 0px -50px 0px' // Start animation slightly before element enters viewport
  };

  const animateOnScroll = (entries, observer) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        const el = entry.target;
        
        // Add staggered delay for multiple elements
        setTimeout(() => {
          el.classList.add('animate');
        }, index * 50); // 50ms stagger between elements
        
        // Stop observing once animated to improve performance
        observer.unobserve(el);
      }
    });
  };

  const observer = new IntersectionObserver(animateOnScroll, observerOptions);

  // Register elements to observe
  const animatedElements = document.querySelectorAll('[data-animate]');
  
  if (animatedElements.length > 0) {
    animatedElements.forEach((el) => {
      observer.observe(el);
    });
  }

  // ==========================================================================
  // Parallax Image Effect (Optimized with RequestAnimationFrame)
  // ==========================================================================
  
  const parallaxImgs = document.querySelectorAll('[data-parallax]');

  if (parallaxImgs.length > 0) {
    let scrollPos = window.scrollY;
    let ticking = false;

    const updateParallax = () => {
      parallaxImgs.forEach(img => {
        const speed = parseFloat(img.getAttribute('data-parallax')) || 0.5;
        const yPos = scrollPos * speed;
        img.style.transform = `translateY(${yPos}px)`;
      });
      ticking = false;
    };

    window.addEventListener('scroll', () => {
      scrollPos = window.scrollY;
      
      if (!ticking) {
        window.requestAnimationFrame(updateParallax);
        ticking = true;
      }
    }, { passive: true }); // Passive listener for better scroll performance

    // Initialize parallax on load
    updateParallax();
  }

  // ==========================================================================
  // Smooth Scroll for Anchor Links
  // ==========================================================================
  
  const anchorLinks = document.querySelectorAll('a[href^="#"]');
  
  anchorLinks.forEach(link => {
    link.addEventListener('click', (e) => {
      const href = link.getAttribute('href');
      
      // Skip if href is just '#' or empty
      if (href === '#' || href === '') return;
      
      const target = document.querySelector(href);
      
      if (target) {
        e.preventDefault();
        
        target.scrollIntoView({
          behavior: 'smooth',
          block: 'start'
        });
        
        // Update URL without jumping
        if (history.pushState) {
          history.pushState(null, null, href);
        }
      }
    });
  });

  // ==========================================================================
  // Navbar Scroll Effect (Optional Enhancement)
  // ==========================================================================
  
  const navbar = document.querySelector('.navbar');
  let lastScroll = 0;
  
  if (navbar) {
    window.addEventListener('scroll', () => {
      const currentScroll = window.scrollY;
      
      // Add subtle background when scrolled down
      if (currentScroll > 100) {
        navbar.style.background = 'rgba(10, 15, 26, 0.95)';
        navbar.style.backdropFilter = 'blur(10px)';
        navbar.style.padding = '1rem 0';
        navbar.style.transition = 'all 0.3s ease';
      } else {
        navbar.style.background = 'transparent';
        navbar.style.backdropFilter = 'none';
        navbar.style.padding = '0';
      }
      
      lastScroll = currentScroll;
    }, { passive: true });
  }

  // ==========================================================================
  // Loading Performance Optimization
  // ==========================================================================
  
  // Lazy load images when they come into viewport
  const lazyImages = document.querySelectorAll('img[data-src]');
  
  if (lazyImages.length > 0 && 'IntersectionObserver' in window) {
    const imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          img.src = img.dataset.src;
          img.removeAttribute('data-src');
          imageObserver.unobserve(img);
        }
      });
    });

    lazyImages.forEach(img => imageObserver.observe(img));
  }

  // ==========================================================================
  // Form Enhancement (if forms are added later)
  // ==========================================================================
  
  const forms = document.querySelectorAll('form');
  
  forms.forEach(form => {
    form.addEventListener('submit', (e) => {
      // Add loading state to submit button
      const submitBtn = form.querySelector('button[type="submit"]');
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.textContent = 'Sending...';
      }
    });
  });

  // ==========================================================================
  // Accessibility Enhancements
  // ==========================================================================
  
  // Add keyboard navigation for interactive cards
  const interactiveCards = document.querySelectorAll('.service-box, .why-card');
  
  interactiveCards.forEach(card => {
    // Make cards keyboard accessible
    card.setAttribute('tabindex', '0');
    
    // Allow Enter key to trigger click
    card.addEventListener('keypress', (e) => {
      if (e.key === 'Enter' || e.key === ' ') {
        e.preventDefault();
        card.click();
      }
    });
  });

  // ==========================================================================
  // Console Message (Optional - Remove in Production)
  // ==========================================================================
  
  console.log('%c🔧 GLS Refrigeration & Air Conditioning', 
    'font-size: 16px; font-weight: bold; color: #14b8a6;');
  console.log('%cWebsite crafted with care by JAY_K', 
    'font-size: 12px; color: #9ca3af;');

});

// ==========================================================================
// Service Box Toggle Function (Global)
// ==========================================================================

function toggleService(clickedBox) {
  const allBoxes = document.querySelectorAll('.service-box');
  
  allBoxes.forEach((box) => {
    if (box !== clickedBox) {
      box.classList.remove('open');
    }
  });
  
  clickedBox.classList.toggle('open');
  
  // Announce change to screen readers
  const isOpen = clickedBox.classList.contains('open');
  const heading = clickedBox.querySelector('h3');
  if (heading) {
    heading.setAttribute('aria-expanded', isOpen);
  }
}

// ==========================================================================
// Why Card Toggle Function (Global)
// ==========================================================================

function toggleWhyCard(clickedCard) {
  clickedCard.classList.toggle('open');
  
  // Announce change to screen readers
  const isOpen = clickedCard.classList.contains('open');
  const heading = clickedCard.querySelector('h4');
  if (heading) {
    heading.setAttribute('aria-expanded', isOpen);
  }
}

// ==========================================================================
// Utility Functions
// ==========================================================================

// Debounce function for performance optimization
function debounce(func, wait) {
  let timeout;
  return function executedFunction(...args) {
    const later = () => {
      clearTimeout(timeout);
      func(...args);
    };
    clearTimeout(timeout);
    timeout = setTimeout(later, wait);
  };
}

// Throttle function for scroll events
function throttle(func, limit) {
  let inThrottle;
  return function(...args) {
    if (!inThrottle) {
      func.apply(this, args);
      inThrottle = true;
      setTimeout(() => inThrottle = false, limit);
    }
  };
}