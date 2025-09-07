// Emdad Global - Enhanced Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavbar();
    initForms();
    initGallery();
    initScrollEffects();
    initTooltips();
    initLoadingStates();
    initAnimations();
    initCounters();
    initParallax();
    initSmoothScrolling();

    // Initialize advanced features
    initGSAPAnimations();
    initIntersectionObserver();
});

// Navbar functionality
function initNavbar() {
    const navbar = document.querySelector('.navbar');

    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        if (window.scrollY > 50) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }
    });

    // Mobile menu close on link click (only for large screens where collapse is used)
    const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    navLinks.forEach(link => {
        link.addEventListener('click', () => {
            // Do not touch collapse when offcanvas (hamburger visible) is used
            const togglerEl = document.querySelector('.navbar .navbar-toggler');
            const isTogglerVisible = togglerEl && window.getComputedStyle(togglerEl).display !== 'none';
            if (isTogglerVisible) return;
            if (navbarCollapse && navbarCollapse.classList.contains('show')) {
                const bsCollapse = new bootstrap.Collapse(navbarCollapse);
                bsCollapse.hide();
            }
        });
    });

    // Mobile dropdowns offcanvas (RTL/LTR aware)
    try {
        const offcanvasEl = document.getElementById('mobileDropdownOffcanvas');
        // If legacy offcanvas is hidden or not present, do nothing
        if (!offcanvasEl || offcanvasEl.classList.contains('d-none')) return;
        const offcanvasBody = offcanvasEl.querySelector('.offcanvas-body');
        const bsOffcanvas = new bootstrap.Offcanvas(offcanvasEl, { backdrop: true, scroll: true });

        // Delegated click handler on dropdown toggles
        document.addEventListener('click', function(e) {
            const toggle = e.target.closest('.navbar-nav .dropdown-toggle');
            if (!toggle) return;

            // Only intercept on mobile widths (matches our CSS breakpoint <= 1399.98)
            if (window.innerWidth >= 1400) return;

            // Prevent default dropdown behavior on mobile
            e.preventDefault();
            e.stopPropagation();

            if (!offcanvasBody) return;

            // Find the related dropdown-menu content
            const dropdown = toggle.closest('.dropdown');
            const menu = dropdown ? dropdown.querySelector('.dropdown-menu') : null;
            if (!menu) return;

            // Clone menu into offcanvas body
            offcanvasBody.innerHTML = '';

            // Add header title from toggle text
            const title = document.getElementById('mobileDropdownLabel');
            if (title) {
                title.textContent = toggle.textContent.trim() || toggle.getAttribute('aria-label') || 'Menu';
            }

            // Create a simple list to host items
            const list = document.createElement('div');
            list.className = 'list-group list-group-flush';

            menu.querySelectorAll('.dropdown-item, .dropdown-divider').forEach(node => {
                if (node.classList.contains('dropdown-divider')) {
                    const hr = document.createElement('div');
                    hr.className = 'list-group-item py-1';
                    hr.innerHTML = '<hr class=\"my-1\">';
                    list.appendChild(hr);
                } else {
                    const a = document.createElement('a');
                    a.className = 'list-group-item list-group-item-action py-3';
                    a.href = node.getAttribute('href');
                    a.textContent = node.textContent.trim();
                    a.addEventListener('click', () => {
                        // Close offcanvas after navigation
                        bsOffcanvas.hide();
                    });
                    list.appendChild(a);
                }
            });

            offcanvasBody.appendChild(list);

            // Open offcanvas
            bsOffcanvas.show();
        });
    } catch(err) {
        console.warn('Offcanvas mobile dropdown init failed:', err);
    }

// Turn entire navbar menu into side offcanvas on mobile
(function initMobileOffcanvasNav() {
  try {
    const offcanvasEl = document.getElementById('mobileOffcanvasNav');
    const offcanvasBody = offcanvasEl ? offcanvasEl.querySelector('#mobileOffcanvasBody') : null;
    if (!offcanvasEl || !offcanvasBody) return;

    const bsOffcanvas = new bootstrap.Offcanvas(offcanvasEl, { backdrop: true, scroll: true });
    const navbar = document.querySelector('nav.navbar');
    const collapse = document.getElementById('navbarNav');
    const toggler = document.querySelector('.navbar .navbar-toggler');

    // Ensure offcanvas has correct dir for alignment
    try { offcanvasEl.setAttribute('dir', document.documentElement.getAttribute('dir') || 'ltr'); } catch(_) {}

    // Do not require collapse to exist to initialize
    if (!navbar || !toggler) return;

    // Helper to open mobile offcanvas with full nav
    function buildOffcanvasContent() {
      // If already has server-rendered content, keep it
      if (offcanvasBody && offcanvasBody.children && offcanvasBody.children.length > 0) return;
      // Build content (brand + nav + language + CTA) dynamically as fallback
      offcanvasBody.innerHTML = '';

      let source = collapse;
      if (!source) {
        // Fallback: reconstruct from navbar markup if collapse missing
        source = document.createElement('div');
        const original = document.querySelector('nav.navbar .navbar-collapse');
        if (original) source.appendChild(original.cloneNode(true));
      }

      const cloned = source ? source.cloneNode(true) : null;
      if (cloned) {
        // Ensure cloned collapse is visible as a vertical list inside offcanvas
        cloned.classList.remove('collapse');
        cloned.classList.remove('navbar-collapse');
        cloned.classList.add('p-2');

        // Normalize styles inside
        cloned.querySelectorAll('.dropdown-menu').forEach(m => { m.classList.add('w-100'); m.style.position = 'static'; });

        offcanvasBody.appendChild(cloned);

        // Toggle dropdowns inside offcanvas
        offcanvasBody.querySelectorAll('.dropdown-toggle').forEach(function(tgl){
          tgl.addEventListener('click', function(ev){
            ev.preventDefault();
            const menu = tgl.nextElementSibling;
            if (menu && menu.classList.contains('dropdown-menu')) {
              menu.classList.toggle('show');
            }
          });
        });
      // If still empty by any chance, add a fallback basic list
      if (!offcanvasBody.children.length) {
        const fallback = document.createElement('ul');
        fallback.className = 'list-group list-group-flush';
        document.querySelectorAll('nav.navbar .navbar-nav > li > a.nav-link').forEach(a => {
          const li = document.createElement('li');
          li.className = 'list-group-item';
          const link = document.createElement('a');
          link.href = a.getAttribute('href');
          link.textContent = a.textContent.trim();
          li.appendChild(link);
          fallback.appendChild(li);
        });
        offcanvasBody.appendChild(fallback);
      }

      }
    }

    function openMobileNav(e) {
      // Prefer checking actual visibility of the toggler for robustness
      const togglerVisible = toggler && window.getComputedStyle(toggler).display !== 'none';
      if (!togglerVisible) return false;
      if (e) { e.preventDefault(); }

      // Make sure any bootstrap collapse state is closed
      if (collapse) collapse.classList.remove('show');

      // Build content just-in-time and show
      buildOffcanvasContent();
      // If still empty (unlikely), use server-rendered fallback list
      if (!offcanvasBody.children.length) {
        const fallback = document.getElementById('__server_nav_fallback');
        if (fallback) {
          const clone = fallback.cloneNode(true);
          clone.classList.remove('d-none');
          offcanvasBody.appendChild(clone);
        }
      }
    // Absolute final fallback: if body still empty on shown, inject simple list
    offcanvasEl.addEventListener('shown.bs.offcanvas', function(){
      if (offcanvasBody && offcanvasBody.children && offcanvasBody.children.length === 0) {
        const simple = document.createElement('ul');
        simple.className = 'list-group list-group-flush';
        const items = [
          {href: '{{ url_for("main.index") }}', text: '{{ _("Home") }}'},
          {href: '{{ url_for("main.about") }}', text: '{{ _("About Us") }}'},
          {href: '{{ url_for("main.certifications") }}', text: '{{ _("Certifications") }}'},
          {href: '{{ url_for("main.services") }}', text: '{{ _("Services") }}'},
          {href: '{{ url_for("main.gallery") }}', text: '{{ _("Gallery") }}'},
          {href: '{{ url_for("main.calendar") }}', text: '{{ _("Calendar") }}'},
          {href: '{{ url_for("main.news") }}', text: '{{ _("News") }}'},
          {href: '{{ url_for("main.contact") }}', text: '{{ _("Contact") }}'},
        ];
        items.forEach(it => {
          const li = document.createElement('li');
          li.className = 'list-group-item';
          const a = document.createElement('a');
          a.className = 'nav-link';
          a.href = it.href; a.textContent = it.text;
          li.appendChild(a);
          simple.appendChild(li);
        });
        offcanvasBody.appendChild(simple);
      }
    });
      bsOffcanvas.show();
      return true;
    }

    // Populate content whenever offcanvas is about to show (covers data-bs triggers)
    offcanvasEl.addEventListener('show.bs.offcanvas', function(){
      buildOffcanvasContent();
    });

    // Attach to the toggler if present (for non data-bs flows)
    if (toggler) {
      toggler.addEventListener('click', openMobileNav);
    }
    // Fallback: delegate on document in case the toggler is re-rendered
    document.addEventListener('click', function(ev) {
      const btn = ev.target.closest('.navbar .navbar-toggler');
      if (!btn) return;
      openMobileNav(ev);
    });

    // Close offcanvas when any nav link is clicked
    offcanvasEl.addEventListener('click', function(e) {
      const link = e.target.closest('a.nav-link, a.dropdown-item, .btn');
      if (link) bsOffcanvas.hide();
    });

    // Hide bootstrap collapse if it was open
    document.addEventListener('shown.bs.offcanvas', function(evt){ if (evt.target === offcanvasEl) collapse.classList.remove('show'); });
  } catch(err) {
    console.warn('initMobileOffcanvasNav failed:', err);
  }
})();


}

// Form enhancements
function initForms() {
    // RFQ Form dynamic product loading
    const categorySelect = document.getElementById('category_key');
    const productInput = document.getElementById('product_name');

    if (categorySelect && productInput) {
        categorySelect.addEventListener('change', function() {
            const categoryKey = this.value;

            if (categoryKey) {
                // Show loading state
                productInput.placeholder = 'Loading products...';
                productInput.disabled = true;

                // Fetch products for selected category
                fetch(`/api/products/${categoryKey}`)
                    .then(response => response.json())
                    .then(products => {
                        // Create datalist for autocomplete
                        let datalist = document.getElementById('product-list');
                        if (!datalist) {
                            datalist = document.createElement('datalist');
                            datalist.id = 'product-list';
                            productInput.parentNode.appendChild(datalist);
                        }

                        // Clear existing options
                        datalist.innerHTML = '';

                        // Add product options
                        products.forEach(product => {
                            const option = document.createElement('option');
                            option.value = product.name;
                            datalist.appendChild(option);
                        });

                        // Set datalist attribute
                        productInput.setAttribute('list', 'product-list');
                        productInput.placeholder = 'Type or select a product...';
                        productInput.disabled = false;
                    })
                    .catch(error => {
                        console.error('Error loading products:', error);
                        productInput.placeholder = 'Enter product name...';
                        productInput.disabled = false;
                    });
            } else {
                productInput.placeholder = 'Select a category first...';
                productInput.disabled = true;
                productInput.removeAttribute('list');
            }
        });
    }

    // Form validation feedback
    const forms = document.querySelectorAll('.needs-validation');
    forms.forEach(form => {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });

    // File upload preview
    const fileInputs = document.querySelectorAll('input[type="file"]');
    fileInputs.forEach(input => {
        input.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const preview = this.parentNode.querySelector('.file-preview');
                if (preview) {
                    preview.textContent = `Selected: ${file.name} (${formatFileSize(file.size)})`;
                    preview.classList.remove('d-none');
                }
            }
        });
    });
}

// Gallery functionality
function initGallery() {
    const galleryItems = document.querySelectorAll('.gallery-item');

    galleryItems.forEach(item => {
        item.addEventListener('click', function() {
            const imgSrc = this.querySelector('img').src;
            const title = this.querySelector('.gallery-overlay h6')?.textContent || '';

            // Create modal for image preview
            showImageModal(imgSrc, title);
        });
    });

    // Gallery filter functionality
    const filterButtons = document.querySelectorAll('.gallery-filter');
    filterButtons.forEach(button => {
        button.addEventListener('click', function() {
            const filter = this.dataset.filter;

            // Update active button
            filterButtons.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');

            // Filter gallery items
            galleryItems.forEach(item => {
                if (filter === 'all' || item.dataset.category === filter) {
                    item.style.display = 'block';
                    item.classList.add('fade-in');
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
}

// Scroll effects
function initScrollEffects() {
    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
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

    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in-up');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements for animation
    const animateElements = document.querySelectorAll('.card, .feature-icon, .news-card');
    animateElements.forEach(el => observer.observe(el));
}

// Initialize tooltips and popovers
function initTooltips() {
    // Bootstrap tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Bootstrap popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Loading states
function initLoadingStates() {
    // Show loading spinner on form submit
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                const originalText = submitBtn.innerHTML;
                const isRTL = document.documentElement.dir === 'rtl' || document.documentElement.lang === 'ar';
                const processingText = isRTL ? 'جاري المعالجة...' : 'Processing...';
                submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>' + processingText;
                submitBtn.disabled = true;

                // Re-enable after 5 seconds (fallback)
                setTimeout(() => {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });
}

// Utility functions
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

function showImageModal(imgSrc, title) {
    // Create modal HTML
    const modalHTML = `
        <div class="modal fade" id="imageModal" tabindex="-1">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body text-center">
                        <img src="${imgSrc}" class="img-fluid" alt="${title}">
                    </div>
                </div>
            </div>
        </div>
    `;

    // Remove existing modal
    const existingModal = document.getElementById('imageModal');
    if (existingModal) {
        existingModal.remove();
    }

    // Add new modal
    document.body.insertAdjacentHTML('beforeend', modalHTML);

    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('imageModal'));
    modal.show();

    // Remove modal from DOM when hidden
    document.getElementById('imageModal').addEventListener('hidden.bs.modal', function() {
        this.remove();
    });
}

function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    // Add to page
    document.body.appendChild(notification);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// AJAX helper function
function makeRequest(url, options = {}) {
    const defaultOptions = {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    };

    return fetch(url, { ...defaultOptions, ...options })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        });
}

// Advanced Animation Functions
function initAnimations() {
    // Stagger animation for elements
    const staggerElements = document.querySelectorAll('.stagger-animation');
    staggerElements.forEach(container => {
        const children = container.children;
        Array.from(children).forEach((child, index) => {
            child.style.animationDelay = `${index * 0.1}s`;
        });
    });

    // Hover effects for cards
    const cards = document.querySelectorAll('.card, .category-card, .product-card, .news-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-10px) scale(1.02)';
            this.style.boxShadow = '0 20px 40px rgba(0, 0, 0, 0.15)';
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '';
        });
    });
}

function initCounters() {
    const counters = document.querySelectorAll('.stat-number[data-count]');

    const animateCounter = (counter) => {
        const target = parseInt(counter.dataset.count);
        const duration = 2000;
        const step = target / (duration / 16);
        let current = 0;

        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                counter.textContent = target + '+';
                clearInterval(timer);
            } else {
                counter.textContent = Math.floor(current) + '+';
            }
        }, 16);
    };

    // Intersection Observer for counters
    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, { threshold: 0.5 });

    counters.forEach(counter => counterObserver.observe(counter));
}

function initParallax() {
    const parallaxElements = document.querySelectorAll('[data-parallax]');

    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;

        parallaxElements.forEach(element => {
            const rate = scrolled * -0.5;
            element.style.transform = `translateY(${rate}px)`;
        });
    });
}

function initSmoothScrolling() {
    // Smooth scroll for anchor links
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

    // Scroll indicator
    const scrollIndicator = document.querySelector('.scroll-indicator');
    if (scrollIndicator) {
        scrollIndicator.addEventListener('click', () => {
            window.scrollTo({
                top: window.innerHeight,
                behavior: 'smooth'
            });
        });
    }
}

function initGSAPAnimations() {
    // Check if GSAP is loaded
    if (typeof gsap === 'undefined') return;

    // Hero animations
    gsap.timeline()
        .from('.hero-content .badge', { duration: 1, y: 50, opacity: 0, ease: 'back.out(1.7)' })
        .from('.hero-content h1', { duration: 1, y: 50, opacity: 0, ease: 'back.out(1.7)' }, '-=0.5')
        .from('.hero-content p', { duration: 1, y: 30, opacity: 0 }, '-=0.5')
        .from('.hero-buttons .btn', { duration: 0.8, y: 30, opacity: 0, stagger: 0.2 }, '-=0.3')
        .from('.trust-indicators > *', { duration: 0.6, x: -30, opacity: 0, stagger: 0.1 }, '-=0.3');

    // Floating shapes animation
    gsap.to('.shape', {
        duration: 'random(4, 8)',
        y: 'random(-50, 50)',
        x: 'random(-30, 30)',
        rotation: 'random(-180, 180)',
        repeat: -1,
        yoyo: true,
        ease: 'sine.inOut',
        stagger: {
            amount: 2,
            from: 'random'
        }
    });

    // ScrollTrigger animations
    gsap.registerPlugin(ScrollTrigger);

    // Category cards animation
    gsap.from('.category-card', {
        duration: 1,
        y: 100,
        opacity: 0,
        stagger: 0.2,
        ease: 'back.out(1.7)',
        scrollTrigger: {
            trigger: '.category-card',
            start: 'top 80%',
            end: 'bottom 20%',
            toggleActions: 'play none none reverse'
        }
    });
}

function initIntersectionObserver() {
    // Enhanced intersection observer for animations
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');

                // Add specific animations based on element type
                if (entry.target.classList.contains('card')) {
                    entry.target.style.animation = 'fadeInUp 0.8s ease-out forwards';
                }

                if (entry.target.classList.contains('stat-item')) {
                    entry.target.style.animation = 'scaleIn 0.6s ease-out forwards';
                }

                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Observe elements
    document.querySelectorAll('.card, .stat-item, .feature-icon').forEach(el => {
        observer.observe(el);
    });
}

// Enhanced scroll effects
function initScrollEffects() {
    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    let lastScrollTop = 0;

    window.addEventListener('scroll', function() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

        if (scrollTop > 100) {
            navbar.classList.add('navbar-scrolled');
        } else {
            navbar.classList.remove('navbar-scrolled');
        }

        // Hide/show navbar on scroll
        if (scrollTop > lastScrollTop && scrollTop > 200) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }

        lastScrollTop = scrollTop;
    });

    // Parallax effect for hero section
    const hero = document.querySelector('.hero-section');
    if (hero) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.3;
            hero.style.transform = `translateY(${rate}px)`;
        });
    }

    // Progress bar
    const progressBar = document.createElement('div');
    progressBar.className = 'scroll-progress';
    progressBar.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 0%;
        height: 3px;
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        z-index: 9999;
        transition: width 0.3s ease;
    `;
    document.body.appendChild(progressBar);

    window.addEventListener('scroll', () => {
        const scrollPercent = (window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100;
        progressBar.style.width = scrollPercent + '%';
    });
}

// Export functions for use in other scripts
window.EmdadGlobal = {
    showNotification,
    makeRequest,
    formatFileSize,
    showImageModal,
    initAnimations,
    initCounters,
    initParallax,
    initGSAPAnimations
};
