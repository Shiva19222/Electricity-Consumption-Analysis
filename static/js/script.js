// Mobile Navigation Toggle
const hamburger = document.querySelector('.hamburger');
const navMenu = document.querySelector('.nav-menu');
const navLinks = document.querySelectorAll('.nav-link');

hamburger.addEventListener('click', () => {
    hamburger.classList.toggle('active');
    navMenu.classList.toggle('active');
});

navLinks.forEach(link => {
    link.addEventListener('click', () => {
        hamburger.classList.remove('active');
        navMenu.classList.remove('active');
    });
});

// Smooth Scrolling
function scrollToSection(sectionId) {
    const section = document.getElementById(sectionId);
    if (section) {
        section.scrollIntoView({ behavior: 'smooth' });
    }
}

// Intersection Observer for Animations
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('fade-in-up');
        }
    });
}, observerOptions);

// Observe all cards and sections
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll(
        '.dashboard-card, .scenario-card, .insight-card, .feature-item'
    );
    
    animatedElements.forEach(el => {
        observer.observe(el);
    });
});

// Active Navigation Highlight
window.addEventListener('scroll', () => {
    const sections = document.querySelectorAll('section');
    const navLinks = document.querySelectorAll('.nav-link');
    
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (scrollY >= (sectionTop - 200)) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href').slice(1) === current) {
            link.classList.add('active');
        }
    });
});

// Parallax Effect for Hero Section
window.addEventListener('scroll', () => {
    const scrolled = window.pageYOffset;
    const hero = document.querySelector('.hero');
    if (hero) {
        hero.style.transform = `translateY(${scrolled * 0.5}px)`;
    }
});

// Counter Animation for Stats
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start);
        }
    }, 16);
}

// Initialize counters when visible
const statNumbers = document.querySelectorAll('.stat-card h3');
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.classList.contains('animated')) {
            const target = parseInt(entry.target.textContent);
            animateCounter(entry.target, target);
            entry.target.classList.add('animated');
        }
    });
}, { threshold: 0.5 });

statNumbers.forEach(stat => {
    counterObserver.observe(stat);
});

// Chart Placeholder Interactions
document.querySelectorAll('.chart-placeholder').forEach(placeholder => {
    placeholder.addEventListener('click', function() {
        this.innerHTML = `
            <div class="loading"></div>
            <p>Loading Tableau visualization...</p>
        `;
        
        // Simulate loading
        setTimeout(() => {
            this.innerHTML = `
                <i class="fas fa-chart-line"></i>
                <p>Tableau visualization embedded here</p>
                <small>Connect to Tableau Public for live data</small>
            `;
        }, 2000);
    });
});

// Dynamic Year Update
const currentYear = new Date().getFullYear();
document.querySelectorAll('.year').forEach(el => {
    el.textContent = currentYear;
});

// Form Validation (if contact form is added)
function validateForm(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// Tooltip Functionality
function createTooltip(element, text) {
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = text;
    document.body.appendChild(tooltip);
    
    element.addEventListener('mouseenter', (e) => {
        tooltip.style.display = 'block';
        tooltip.style.left = e.pageX + 'px';
        tooltip.style.top = (e.pageY - 30) + 'px';
    });
    
    element.addEventListener('mouseleave', () => {
        tooltip.style.display = 'none';
    });
}

// Performance Monitoring
function logPerformance() {
    if ('performance' in window) {
        const loadTime = performance.timing.loadEventEnd - performance.timing.navigationStart;
        console.log(`Page load time: ${loadTime}ms`);
    }
}

window.addEventListener('load', logPerformance);

// Error Handling
window.addEventListener('error', (e) => {
    console.error('JavaScript error:', e.error);
});

// Service Worker Registration (for PWA functionality)
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/sw.js')
            .then(registration => {
                console.log('SW registered: ', registration);
            })
            .catch(registrationError => {
                console.log('SW registration failed: ', registrationError);
            });
    });
}

// Dark Mode Toggle (optional enhancement)
function toggleDarkMode() {
    document.body.classList.toggle('dark-mode');
    localStorage.setItem('darkMode', document.body.classList.contains('dark-mode'));
}

// Load dark mode preference
if (localStorage.getItem('darkMode') === 'true') {
    document.body.classList.add('dark-mode');
}

// Export functions for external use
window.EnergyAnalytics = {
    scrollToSection,
    createTooltip,
    toggleDarkMode,
    validateForm
};
