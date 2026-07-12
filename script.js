// ===== YAATHRA - KERALA TRAVEL PLANNER =====
// Main JavaScript file for interactivity and animations

// ===== DOM CONTENT LOADED =====
document.addEventListener('DOMContentLoaded', function() {
    // Initialize AOS (Animate On Scroll)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            once: true,
            offset: 100
        });
    }

    // Initialize all components
    initNavigation();
    initAnimations();
    initFormValidation();
    initScrollEffects();
    initSearch();
    initFilters();
    initWishlist();
    initTripPlanner();
    initChecklist();
    initModals();
    initThemeToggle();
    initLazyLoading();
    initAnalytics();
});

// ===== NAVIGATION =====
function initNavigation() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    const navLinks = document.querySelectorAll('.nav-link');

    // Mobile menu toggle
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            this.classList.toggle('active');
            navMenu.classList.toggle('active');
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!hamburger.contains(e.target) && !navMenu.contains(e.target)) {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            }
        });
    }

    // Active link highlighting
    const currentPath = window.location.pathname;
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });

    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offset = 80; // Account for fixed navbar
                const targetPosition = target.offsetTop - offset;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ===== ANIMATIONS =====
function initAnimations() {
    // Scroll animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate');
            }
        });
    }, observerOptions);

    // Observe elements for animation
    document.querySelectorAll('.feature-card, .place-card, .tip-card, .stat-card').forEach(el => {
        observer.observe(el);
    });

    // Counter animations for stats
    animateCounters();
}

function animateCounters() {
    const counters = document.querySelectorAll('.stat-number');
    
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
                const counter = entry.target;
                const target = parseInt(counter.textContent.replace(/[^0-9]/g, ''));
                const duration = 2000;
                const step = target / (duration / 16);
                let current = 0;
                
                const updateCounter = () => {
                    current += step;
                    if (current < target) {
                        counter.textContent = Math.floor(current).toLocaleString();
                        requestAnimationFrame(updateCounter);
                    } else {
                        counter.textContent = target.toLocaleString();
                        counter.classList.add('counted');
                    }
                };
                
                updateCounter();
            }
        });
    }, { threshold: 0.5 });
    
    counters.forEach(counter => {
        counterObserver.observe(counter);
    });
}

// ===== FORM VALIDATION =====
function initFormValidation() {
    // Login form validation
    const loginForm = document.querySelector('.login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            const username = document.getElementById('username').value.trim();
            const password = document.getElementById('password').value;
            
            if (!username || !password) {
                e.preventDefault();
                showNotification('Please fill in all fields', 'error');
                return false;
            }
            
            if (username.length < 3) {
                e.preventDefault();
                showNotification('Username must be at least 3 characters', 'error');
                return false;
            }
        });
    }

    // Signup form validation
    const signupForm = document.querySelector('.signup-form');
    if (signupForm) {
        const passwordInput = document.getElementById('password');
        const confirmPasswordInput = document.getElementById('confirm_password');
        
        // Real-time password confirmation check
        if (confirmPasswordInput) {
            confirmPasswordInput.addEventListener('input', function() {
                const password = passwordInput.value;
                const confirmPassword = this.value;
                
                if (confirmPassword && password !== confirmPassword) {
                    this.setCustomValidity('Passwords do not match');
                } else {
                    this.setCustomValidity('');
                }
            });
        }
        
        signupForm.addEventListener('submit', function(e) {
            const username = document.getElementById('username').value.trim();
            const email = document.getElementById('email').value.trim();
            const password = passwordInput.value;
            const confirmPassword = confirmPasswordInput.value;
            const terms = document.querySelector('input[name="terms"]').checked;
            
            // Username validation
            if (username.length < 3) {
                e.preventDefault();
                showNotification('Username must be at least 3 characters long', 'error');
                return false;
            }
            
            // Email validation
            if (!isValidEmail(email)) {
                e.preventDefault();
                showNotification('Please enter a valid email address', 'error');
                return false;
            }
            
            // Password validation
            if (password.length < 6) {
                e.preventDefault();
                showNotification('Password must be at least 6 characters long', 'error');
                return false;
            }
            
            // Password confirmation
            if (password !== confirmPassword) {
                e.preventDefault();
                showNotification('Passwords do not match', 'error');
                return false;
            }
            
            // Terms validation
            if (!terms) {
                e.preventDefault();
                showNotification('You must agree to the Terms of Service', 'error');
                return false;
            }
        });
    }

    // Trip planner form validation
    const tripForm = document.querySelector('.trip-form');
    if (tripForm) {
        tripForm.addEventListener('submit', function(e) {
            const destination = document.getElementById('destination').value;
            const days = document.getElementById('days').value;
            const budget = document.getElementById('budget').value;
            
            if (!destination || !days || !budget) {
                e.preventDefault();
                showNotification('Please fill in all required fields', 'error');
                return false;
            }
        });
    }
}

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

// ===== SCROLL EFFECTS =====
function initScrollEffects() {
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');
    
    // Hide/show navbar on scroll
    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > lastScrollTop && scrollTop > 100) {
            // Scrolling down
            navbar.style.transform = 'translateY(-100%)';
        } else {
            // Scrolling up
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });

    // Parallax effect for hero images
    const heroImages = document.querySelectorAll('.hero img, .place-hero img');
    window.addEventListener('scroll', function() {
        const scrolled = window.pageYOffset;
        
        heroImages.forEach(img => {
            if (img) {
                img.style.transform = `translateY(${scrolled * 0.5}px)`;
            }
        });
    });

    // Back to top button
    createBackToTopButton();
}

function createBackToTopButton() {
    const backToTop = document.createElement('button');
    backToTop.innerHTML = 'â';
    backToTop.className = 'back-to-top';
    backToTop.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        background: var(--primary-color);
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 20px;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 999;
        box-shadow: var(--shadow-medium);
    `;
    
    document.body.appendChild(backToTop);
    
    window.addEventListener('scroll', function() {
        if (window.pageYOffset > 300) {
            backToTop.style.opacity = '1';
            backToTop.style.visibility = 'visible';
        } else {
            backToTop.style.opacity = '0';
            backToTop.style.visibility = 'hidden';
        }
    });
    
    backToTop.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// ===== SEARCH FUNCTIONALITY =====
function initSearch() {
    const searchInput = document.querySelector('.search-input');
    const searchResults = document.querySelector('.search-results');
    
    if (searchInput) {
        let searchTimeout;
        
        searchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            const query = this.value.trim();
            
            if (query.length > 2) {
                searchTimeout = setTimeout(() => {
                    performSearch(query);
                }, 300);
            } else {
                hideSearchResults();
            }
        });
        
        // Close search results on click outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && (!searchResults || !searchResults.contains(e.target))) {
                hideSearchResults();
            }
        });
    }
}

function performSearch(query) {
    // This would typically make an API call
    // For now, we'll simulate search results
    const mockResults = [
        { title: 'Munnar', category: 'hill', url: '/place/munnar' },
        { title: 'Alleppey', category: 'nature', url: '/place/alleppey' },
        { title: 'Kovalam', category: 'beach', url: '/place/kovalam' }
    ].filter(item => item.title.toLowerCase().includes(query.toLowerCase()));
    
    displaySearchResults(mockResults);
}

function displaySearchResults(results) {
    let searchResults = document.querySelector('.search-results');
    
    if (!searchResults) {
        searchResults = document.createElement('div');
        searchResults.className = 'search-results';
        searchResults.style.cssText = `
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background: white;
            border: 1px solid var(--border-color);
            border-top: none;
            max-height: 300px;
            overflow-y: auto;
            z-index: 1000;
            box-shadow: var(--shadow-medium);
        `;
        
        const searchContainer = document.querySelector('.search-bar');
        if (searchContainer) {
            searchContainer.style.position = 'relative';
            searchContainer.appendChild(searchResults);
        }
    }
    
    if (results.length === 0) {
        searchResults.innerHTML = '<div style="padding: 1rem; color: var(--text-secondary);">No results found</div>';
    } else {
        searchResults.innerHTML = results.map(result => `
            <a href="${result.url}" style="display: block; padding: 0.75rem 1rem; border-bottom: 1px solid var(--border-color); text-decoration: none; color: var(--text-primary); transition: background 0.2s;">
                <div style="font-weight: 500;">${result.title}</div>
                <div style="font-size: 0.875rem; color: var(--text-secondary);">${result.category}</div>
            </a>
        `).join('');
    }
    
    searchResults.style.display = 'block';
}

function hideSearchResults() {
    const searchResults = document.querySelector('.search-results');
    if (searchResults) {
        searchResults.style.display = 'none';
    }
}

// ===== FILTER FUNCTIONALITY =====
function initFilters() {
    const filterTabs = document.querySelectorAll('.filter-tab');
    const placesGrid = document.querySelector('.places-grid');
    
    filterTabs.forEach(tab => {
        tab.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Update active state
            filterTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');
            
            // Filter places (in a real app, this would filter from the server)
            const category = this.dataset.category || this.textContent.toLowerCase().trim();
            filterPlaces(category);
        });
    });
}

function filterPlaces(category) {
    const placeCards = document.querySelectorAll('.place-card');
    
    placeCards.forEach(card => {
        const cardCategory = card.querySelector('.place-category').textContent.toLowerCase();
        
        if (category === 'all' || cardCategory === category) {
            card.style.display = 'block';
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100);
        } else {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.display = 'none';
            }, 300);
        }
    });
}

// ===== WISHLIST FUNCTIONALITY =====
function initWishlist() {
    const wishlistButtons = document.querySelectorAll('.wishlist-icon, .btn-wishlist');
    
    wishlistButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            e.preventDefault();
            e.stopPropagation();
            
            const placeName = this.dataset.place;
            if (placeName) {
                toggleWishlist(placeName, this);
            }
        });
    });
}

function toggleWishlist(placeName, button) {
    // Check if user is logged in
    const isLoggedIn = document.querySelector('.nav-menu a[href="/logout"]');
    
    if (!isLoggedIn) {
        showNotification('Please login to add items to wishlist', 'warning');
        return;
    }
    
    // Toggle wishlist state
    const isInWishlist = button.classList.contains('active');
    
    if (isInWishlist) {
        button.classList.remove('active');
        showNotification('Removed from wishlist', 'info');
    } else {
        button.classList.add('active');
        showNotification('Added to wishlist', 'success');
    }
    
    // In a real app, this would make an API call
    updateWishlistCount();
}

function updateWishlistCount() {
    // Update wishlist count in navigation if it exists
    const wishlistCount = document.querySelector('.wishlist-count');
    if (wishlistCount) {
        const currentCount = parseInt(wishlistCount.textContent) || 0;
        wishlistCount.textContent = currentCount + 1;
    }
}

// ===== TRIP PLANNER FUNCTIONALITY =====
function initTripPlanner() {
    const interestTags = document.querySelectorAll('.interest-tag');
    const interestsTextarea = document.getElementById('interests');
    
    if (interestTags.length > 0 && interestsTextarea) {
        interestTags.forEach(tag => {
            tag.addEventListener('click', function() {
                const interest = this.dataset.interest;
                const currentInterests = interestsTextarea.value;
                
                if (currentInterests.includes(interest)) {
                    // Remove if already selected
                    interestsTextarea.value = currentInterests
                        .replace(interest + ', ', '')
                        .replace(', ' + interest, '')
                        .replace(interest, '');
                    this.classList.remove('selected');
                } else {
                    // Add if not selected
                    interestsTextarea.value = currentInterests ? 
                        currentInterests + ', ' + interest : interest;
                    this.classList.add('selected');
                }
                
                // Add ripple effect
                createRipple(this, event);
            });
        });
    }
    
    // Quick destination selection
    const selectButtons = document.querySelectorAll('.btn-select-destination');
    selectButtons.forEach(button => {
        button.addEventListener('click', function() {
            const destination = this.dataset.destination;
            const destinationSelect = document.getElementById('destination');
            
            if (destinationSelect) {
                destinationSelect.value = destination;
                
                // Scroll to form
                const form = document.querySelector('.trip-form');
                if (form) {
                    form.scrollIntoView({
                        behavior: 'smooth',
                        block: 'center'
                    });
                }
                
                // Visual feedback
                destinationSelect.classList.add('highlighted');
                setTimeout(() => {
                    destinationSelect.classList.remove('highlighted');
                }, 1000);
            }
        });
    });
}

// ===== CHECKLIST FUNCTIONALITY =====
function initChecklist() {
    const checklistItems = document.querySelectorAll('.checklist-item input[type="checkbox"]');
    
    checklistItems.forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const label = this.parentElement;
            if (this.checked) {
                label.classList.add('checked');
            } else {
                label.classList.remove('checked');
            }
            
            updateChecklistProgress();
        });
    });
}

function updateChecklistProgress() {
    const total = document.querySelectorAll('.checklist-item input[type="checkbox"]').length;
    const checked = document.querySelectorAll('.checklist-item input[type="checkbox"]:checked').length;
    const progress = (checked / total) * 100;
    
    // Update progress bar if it exists
    const progressBar = document.querySelector('.checklist-progress');
    if (progressBar) {
        progressBar.style.width = progress + '%';
    }
    
    // Save progress to localStorage
    localStorage.setItem('checklistProgress', progress);
}

// ===== MODALS =====
function initModals() {
    // Create modal container
    const modalContainer = document.createElement('div');
    modalContainer.className = 'modal-container';
    modalContainer.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: none;
        align-items: center;
        justify-content: center;
        z-index: 2000;
    `;
    
    document.body.appendChild(modalContainer);
    
    // Close modal on background click
    modalContainer.addEventListener('click', function(e) {
        if (e.target === modalContainer) {
            closeModal();
        }
    });
}

function openModal(content) {
    const modalContainer = document.querySelector('.modal-container');
    if (modalContainer) {
        modalContainer.innerHTML = content;
        modalContainer.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

function closeModal() {
    const modalContainer = document.querySelector('.modal-container');
    if (modalContainer) {
        modalContainer.style.display = 'none';
        modalContainer.innerHTML = '';
        document.body.style.overflow = '';
    }
}

// ===== THEME TOGGLE =====
function initThemeToggle() {
    // Check for saved theme preference
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        updateThemeToggle(true);
    }
    
    // Get the theme toggle button from navigation
    const themeToggle = document.querySelector('.dark-mode-toggle');
    if (themeToggle) {
        themeToggle.addEventListener('click', function() {
            toggleDarkMode();
        });
    }
    
    // Also check system preference
    if (!savedTheme) {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        if (prefersDark) {
            document.body.classList.add('dark-theme');
            updateThemeToggle(true);
        }
    }
}

// Global function for dark mode toggle
function toggleDarkMode() {
    const isDark = document.body.classList.toggle('dark-theme');
    localStorage.setItem('theme', isDark ? 'dark' : 'light');
    updateThemeToggle(isDark);
    
    // Add transition effect
    document.body.style.transition = 'background-color 0.3s ease, color 0.3s ease';
    
    // Show notification
    showNotification(`${isDark ? 'Dark' : 'Light'} mode activated`, 'info');
}

function updateThemeToggle(isDark) {
    const sunIcon = document.querySelector('.sun-icon');
    const moonIcon = document.querySelector('.moon-icon');
    
    if (sunIcon && moonIcon) {
        if (isDark) {
            sunIcon.style.display = 'none';
            moonIcon.style.display = 'block';
        } else {
            sunIcon.style.display = 'block';
            moonIcon.style.display = 'none';
        }
    }
}

// ===== LAZY LOADING =====
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => {
        img.classList.add('lazy');
        imageObserver.observe(img);
    });
}

// ===== ANALYTICS =====
function initAnalytics() {
    // Track page views
    trackPageView();
    
    // Track button clicks
    document.addEventListener('click', function(e) {
        const button = e.target.closest('.btn');
        if (button) {
            trackEvent('button_click', {
                button_text: button.textContent.trim(),
                button_class: button.className
            });
        }
    });
    
    // Track form submissions
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            trackEvent('form_submit', {
                form_id: form.id || 'unknown',
                form_class: form.className
            });
        });
    });
}

function trackPageView() {
    // In a real app, this would send data to analytics service
    console.log('Page view:', window.location.pathname);
}

function trackEvent(eventName, data) {
    // In a real app, this would send data to analytics service
    console.log('Event:', eventName, data);
}

// ===== NOTIFICATIONS =====
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotifications = document.querySelectorAll('.notification');
    existingNotifications.forEach(notification => notification.remove());
    
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.style.cssText = `
        position: fixed;
        top: 90px;
        right: 20px;
        padding: 1rem 1.5rem;
        background: ${getNotificationColor(type)};
        color: white;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-medium);
        z-index: 1001;
        max-width: 400px;
        animation: slideInRight 0.3s ease;
    `;
    
    notification.innerHTML = `
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span>${message}</span>
            <button onclick="this.parentElement.parentElement.remove()" style="background: none; border: none; color: white; font-size: 1.25rem; cursor: pointer; margin-left: 1rem;">×</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }
    }, 5000);
}

function getNotificationColor(type) {
    const colors = {
        success: '#4caf50',
        error: '#f44336',
        warning: '#ff9800',
        info: '#2196f3'
    };
    return colors[type] || colors.info;
}

// ===== RIPPLE EFFECT =====
function createRipple(element, event) {
    const ripple = document.createElement('span');
    ripple.className = 'ripple';
    
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.cssText = `
        position: absolute;
        width: ${size}px;
        height: ${size}px;
        left: ${x}px;
        top: ${y}px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 50%;
        transform: scale(0);
        animation: ripple 0.6s ease-out;
        pointer-events: none;
    `;
    
    element.style.position = 'relative';
    element.style.overflow = 'hidden';
    element.appendChild(ripple);
    
    setTimeout(() => ripple.remove(), 600);
}

// ===== UTILITY FUNCTIONS =====
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

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Add CSS for animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @keyframes ripple {
        to {
            transform: scale(4);
            opacity: 0;
        }
    }
    
    .highlighted {
        animation: highlight 1s ease;
    }
    
    @keyframes highlight {
        0%, 100% {
            background-color: transparent;
        }
        50% {
            background-color: rgba(46, 125, 50, 0.1);
        }
    }
    
    .lazy {
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .lazy.loaded {
        opacity: 1;
    }
    
    .dark-theme {
        --text-primary: #ffffff;
        --text-secondary: #b0b0b0;
        --bg-primary: #1a1a1a;
        --bg-secondary: #2d2d2d;
        --border-color: #404040;
    }
    
    .animate {
        animation: fadeInUp 0.6s ease forwards;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
`;

document.head.appendChild(style);

// ===== GLOBAL FUNCTIONS =====
window.showNotification = showNotification;
window.openModal = openModal;
window.closeModal = closeModal;
window.createRipple = createRipple;

// Print functionality
window.printPlan = function() {
    window.print();
};

// Trip management functions
window.viewTripDetails = function(tripId) {
    console.log('View trip details:', tripId);
    showNotification('Trip details feature coming soon!', 'info');
};

window.editTrip = function(tripId) {
    console.log('Edit trip:', tripId);
    showNotification('Edit trip feature coming soon!', 'info');
};

window.deleteTrip = function(tripId) {
    if (confirm('Are you sure you want to delete this trip plan?')) {
        console.log('Delete trip:', tripId);
        showNotification('Trip deleted successfully', 'success');
        // In a real app, this would make an API call
    }
};

// Password toggle functions
window.togglePassword = function(fieldId) {
    const passwordInput = document.getElementById(fieldId);
    const toggleContainer = passwordInput.nextElementSibling;
    const toggleIcons = toggleContainer.querySelectorAll('svg');
    
    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        toggleIcons[0].style.display = 'none';
        toggleIcons[1].style.display = 'block';
    } else {
        passwordInput.type = 'password';
        toggleIcons[0].style.display = 'block';
        toggleIcons[1].style.display = 'none';
    }
};

// Initialize on page load
console.log('Yaathra JavaScript initialized successfully!');
