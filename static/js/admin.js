/**
 * Enhanced Admin Panel JavaScript
 * Emdad Global - Admin Dashboard Functionality
 */

class AdminDashboard {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupAnimations();
        this.setupLanguageToggle();
        this.setupSidebar();
        this.setupTooltips();
        this.setupConfirmations();
    }

    setupEventListeners() {
        // Sidebar toggle functionality
        this.setupSidebarToggle();

        // Form submissions with loading states
        const forms = document.querySelectorAll('form');
        forms.forEach(form => {
            form.addEventListener('submit', this.handleFormSubmit.bind(this));
        });

        // Table row actions
        const actionButtons = document.querySelectorAll('[data-action]');
        actionButtons.forEach(button => {
            button.addEventListener('click', this.handleAction.bind(this));
        });

        // Search functionality
        const searchInputs = document.querySelectorAll('[data-search]');
        searchInputs.forEach(input => {
            input.addEventListener('input', this.handleSearch.bind(this));
        });

        // Window resize handler
        window.addEventListener('resize', this.handleResize.bind(this));

        // Handle clicks outside sidebar on mobile
        document.addEventListener('click', this.handleOutsideClick.bind(this));
    }

    setupSidebarToggle() {
        const sidebarToggle = document.getElementById('sidebarToggle');
        const sidebarClose = document.getElementById('sidebarClose');
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.getElementById('sidebarOverlay');

        if (sidebarToggle && sidebar && overlay) {
            // Toggle button click
            sidebarToggle.addEventListener('click', (e) => {
                e.stopPropagation();
                this.toggleSidebar();
            });

            // Close button click
            if (sidebarClose) {
                sidebarClose.addEventListener('click', (e) => {
                    e.stopPropagation();
                    this.closeSidebar();
                });
            }

            // Overlay click to close
            overlay.addEventListener('click', () => {
                this.closeSidebar();
            });

            // Escape key to close
            document.addEventListener('keydown', (e) => {
                if (e.key === 'Escape' && this.isSidebarOpen()) {
                    this.closeSidebar();
                }
            });
        }
    }

    setupAnimations() {
        // Animate cards on load
        const cards = document.querySelectorAll('.card, .stat-card');
        cards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });

        // Animate navigation items
        const navItems = document.querySelectorAll('.nav-link');
        navItems.forEach((item, index) => {
            item.style.opacity = '0';
            item.style.transform = 'translateX(-20px)';
            
            setTimeout(() => {
                item.style.transition = 'all 0.4s ease';
                item.style.opacity = '1';
                item.style.transform = 'translateX(0)';
            }, index * 50);
        });
    }

    setupLanguageToggle() {
        const languageButtons = document.querySelectorAll('.language-btn');
        languageButtons.forEach(button => {
            button.addEventListener('click', (e) => {
                e.preventDefault();
                
                // Add loading state
                const originalText = button.innerHTML;
                button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
                button.disabled = true;
                
                // Navigate after short delay for visual feedback
                setTimeout(() => {
                    window.location.href = button.href;
                }, 300);
            });
        });
    }

    setupSidebar() {
        // Active navigation highlighting
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link');

        navLinks.forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active');

                // If this is a submenu item, expand its parent
                const parentCollapse = link.closest('.collapse');
                if (parentCollapse) {
                    parentCollapse.classList.add('show');
                    const toggleButton = document.querySelector(`[data-bs-target="#${parentCollapse.id}"]`);
                    if (toggleButton) {
                        toggleButton.classList.remove('collapsed');
                        toggleButton.setAttribute('aria-expanded', 'true');
                    }
                }
            }
        });

        // Handle collapsible menu state persistence
        this.setupCollapsibleMenus();

        // Sidebar collapse on mobile
        this.handleResponsiveSidebar();
        window.addEventListener('resize', this.handleResponsiveSidebar.bind(this));
    }

    setupCollapsibleMenus() {
        // Handle collapse state persistence
        const collapseElements = document.querySelectorAll('.collapse');

        collapseElements.forEach(collapse => {
            const collapseId = collapse.id;
            const isExpanded = localStorage.getItem(`sidebar-${collapseId}`) === 'true';

            if (isExpanded) {
                collapse.classList.add('show');
                const toggleButton = document.querySelector(`[data-bs-target="#${collapseId}"]`);
                if (toggleButton) {
                    toggleButton.classList.remove('collapsed');
                    toggleButton.setAttribute('aria-expanded', 'true');
                }
            }

            // Save state when toggled
            collapse.addEventListener('shown.bs.collapse', () => {
                localStorage.setItem(`sidebar-${collapseId}`, 'true');
            });

            collapse.addEventListener('hidden.bs.collapse', () => {
                localStorage.setItem(`sidebar-${collapseId}`, 'false');
            });
        });
    }

    setupTooltips() {
        // Initialize Bootstrap tooltips
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    setupConfirmations() {
        // Setup delete confirmations
        const deleteButtons = document.querySelectorAll('[data-action="delete"]');
        deleteButtons.forEach(button => {
            button.addEventListener('click', this.confirmDelete.bind(this));
        });
    }

    toggleSidebar() {
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.getElementById('sidebarOverlay');

        if (this.isSidebarOpen()) {
            this.closeSidebar();
        } else {
            this.openSidebar();
        }
    }

    openSidebar() {
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.getElementById('sidebarOverlay');
        const body = document.body;

        sidebar.classList.add('show');
        overlay.classList.add('show');

        // Prevent body scroll on mobile when sidebar is open
        if (window.innerWidth <= 768) {
            body.style.overflow = 'hidden';
        }

        // Save state
        localStorage.setItem('sidebar-open', 'true');
    }

    closeSidebar() {
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.getElementById('sidebarOverlay');
        const body = document.body;

        sidebar.classList.remove('show');
        overlay.classList.remove('show');
        body.style.overflow = '';

        // Save state
        localStorage.setItem('sidebar-open', 'false');
    }

    isSidebarOpen() {
        const sidebar = document.querySelector('.sidebar');
        return sidebar.classList.contains('show');
    }

    handleResponsiveSidebar() {
        const sidebar = document.querySelector('.sidebar');
        const overlay = document.getElementById('sidebarOverlay');
        const isMobile = window.innerWidth <= 768;
        const wasOpen = localStorage.getItem('sidebar-open') === 'true';

        if (isMobile) {
            // On mobile, close sidebar by default unless explicitly opened
            if (!this.isSidebarOpen()) {
                sidebar.classList.remove('show');
                if (overlay) overlay.classList.remove('show');
                document.body.style.overflow = '';
            }
        } else {
            // On desktop, restore previous state or keep open by default
            if (wasOpen !== false) { // If never set or was true
                sidebar.classList.add('show');
            }
            // Always remove overlay on desktop
            if (overlay) {
                overlay.classList.remove('show');
            }
            document.body.style.overflow = '';
        }
    }

    handleResize() {
        // Debounce resize events
        clearTimeout(this.resizeTimeout);
        this.resizeTimeout = setTimeout(() => {
            this.handleResponsiveSidebar();
        }, 150);
    }

    handleOutsideClick(e) {
        const sidebar = document.querySelector('.sidebar');
        const sidebarToggle = document.getElementById('sidebarToggle');
        const isMobile = window.innerWidth <= 768;

        // Only handle outside clicks on mobile
        if (isMobile && this.isSidebarOpen()) {
            // Check if click is outside sidebar and not on toggle button
            if (!sidebar.contains(e.target) && !sidebarToggle.contains(e.target)) {
                this.closeSidebar();
            }
        }
    }

    handleFormSubmit(e) {
        const form = e.target;
        const submitButton = form.querySelector('button[type="submit"]');
        
        if (submitButton) {
            // Add loading state
            const originalText = submitButton.innerHTML;
            submitButton.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
            submitButton.disabled = true;
            
            // Restore button state if form validation fails
            setTimeout(() => {
                if (!form.checkValidity()) {
                    submitButton.innerHTML = originalText;
                    submitButton.disabled = false;
                }
            }, 100);
        }
    }

    handleAction(e) {
        const button = e.target.closest('[data-action]');
        const action = button.dataset.action;
        
        switch (action) {
            case 'edit':
                this.handleEdit(button);
                break;
            case 'view':
                this.handleView(button);
                break;
            case 'toggle':
                this.handleToggle(button);
                break;
        }
    }

    handleEdit(button) {
        const id = button.dataset.id;
        const editUrl = button.dataset.url || button.href;
        
        if (editUrl) {
            window.location.href = editUrl;
        }
    }

    handleView(button) {
        const id = button.dataset.id;
        const viewUrl = button.dataset.url || button.href;
        
        if (viewUrl) {
            window.open(viewUrl, '_blank');
        }
    }

    handleToggle(button) {
        const id = button.dataset.id;
        const field = button.dataset.field || 'is_active';
        
        // Add loading state
        button.disabled = true;
        const icon = button.querySelector('i');
        const originalClass = icon.className;
        icon.className = 'fas fa-spinner fa-spin';
        
        // Simulate API call (replace with actual implementation)
        setTimeout(() => {
            // Toggle button state
            button.classList.toggle('btn-success');
            button.classList.toggle('btn-secondary');
            
            // Restore icon
            icon.className = originalClass;
            button.disabled = false;
            
            // Show success message
            this.showToast('Status updated successfully', 'success');
        }, 500);
    }

    confirmDelete(e) {
        e.preventDefault();
        
        const button = e.target.closest('[data-action="delete"]');
        const itemName = button.dataset.name || 'this item';
        
        if (confirm(`Are you sure you want to delete ${itemName}? This action cannot be undone.`)) {
            // Add loading state
            button.disabled = true;
            button.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            
            // Proceed with deletion (replace with actual implementation)
            const deleteUrl = button.dataset.url || button.href;
            if (deleteUrl) {
                window.location.href = deleteUrl;
            }
        }
    }

    handleSearch(e) {
        const input = e.target;
        const searchTerm = input.value.toLowerCase();
        const targetSelector = input.dataset.search;
        const targets = document.querySelectorAll(targetSelector);
        
        targets.forEach(target => {
            const text = target.textContent.toLowerCase();
            const shouldShow = text.includes(searchTerm);
            
            target.style.display = shouldShow ? '' : 'none';
            
            // Add highlight effect
            if (shouldShow && searchTerm) {
                target.style.background = 'rgba(104, 155, 138, 0.1)';
            } else {
                target.style.background = '';
            }
        });
    }

    showToast(message, type = 'info') {
        // Create toast element
        const toast = document.createElement('div');
        toast.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        toast.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        toast.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(toast);
        
        // Auto remove after 3 seconds
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    // Utility methods
    formatNumber(num) {
        return new Intl.NumberFormat().format(num);
    }

    formatDate(date) {
        return new Intl.DateTimeFormat('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        }).format(new Date(date));
    }

    // Chart helpers (if using charts)
    initializeCharts() {
        // Initialize any charts here
        console.log('Charts initialized');
    }

    // Export functionality
    exportData(format = 'csv') {
        console.log(`Exporting data as ${format}`);
        // Implement export functionality
    }
}

// Initialize dashboard when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new AdminDashboard();
});

// Global utility functions
window.AdminUtils = {
    showLoading: (element) => {
        element.classList.add('loading');
    },
    
    hideLoading: (element) => {
        element.classList.remove('loading');
    },
    
    confirmAction: (message) => {
        return confirm(message);
    },
    
    formatCurrency: (amount, currency = 'USD') => {
        return new Intl.NumberFormat('en-US', {
            style: 'currency',
            currency: currency
        }).format(amount);
    }
};

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AdminDashboard;
}
