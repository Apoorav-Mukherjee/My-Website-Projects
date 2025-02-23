// Initialize Lucide icons
lucide.createIcons();

// Navbar scroll effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.1)';
        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
    } else {
        navbar.style.boxShadow = 'none';
        navbar.style.background = 'var(--white)';
    }
});

// Smooth scroll for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Intersection Observer for scroll animations
const observerOptions = {
    threshold: 0.2,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('visible');
        }
    });
}, observerOptions);

// Observe elements for animation
document.addEventListener('DOMContentLoaded', () => {
    // Observe section headers
    document.querySelectorAll('.section-header').forEach(el => observer.observe(el));
    
    // Observe feature cards
    document.querySelectorAll('.feature-card').forEach(el => observer.observe(el));
    
    // Observe stat items
    document.querySelectorAll('.stat-item').forEach(el => observer.observe(el));
    
    // Observe project cards
    document.querySelectorAll('.project-card').forEach(el => observer.observe(el));
    
    // Observe testimonial cards
    document.querySelectorAll('.testimonial-card').forEach(el => observer.observe(el));
    
    // Observe CTA content
    document.querySelectorAll('.cta-content').forEach(el => observer.observe(el));
    
    // Observe footer content
    document.querySelectorAll('.footer-content').forEach(el => observer.observe(el));
});

// Counter animation for stats
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    function updateCounter() {
        start += increment;
        if (start < target) {
            element.textContent = Math.floor(start);
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = target;
        }
    }
    
    updateCounter();
}

// Animate stats when they become visible
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const statValue = entry.target.querySelector('h3');
            const targetValue = parseInt(statValue.textContent);
            animateCounter(statValue, targetValue);
            statsObserver.unobserve(entry.target);
        }
    });
}, observerOptions);

document.querySelectorAll('.stat-item').forEach(el => statsObserver.observe(el));