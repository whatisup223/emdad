/**
 * Enhanced Login Page JavaScript
 * Emdad Global - Admin Login Functionality
 */

class LoginManager {
    constructor() {
        this.init();
    }

    init() {
        this.setupEventListeners();
        this.setupAnimations();
        this.setupValidation();
        this.setupAccessibility();
    }

    setupEventListeners() {
        // Password toggle
        const togglePassword = document.getElementById('togglePassword');
        if (togglePassword) {
            togglePassword.addEventListener('click', this.togglePasswordVisibility.bind(this));
        }

        // Form submission
        const loginForm = document.querySelector('.needs-validation');
        if (loginForm) {
            loginForm.addEventListener('submit', this.handleFormSubmit.bind(this));
        }

        // Input focus effects
        const formControls = document.querySelectorAll('.form-control');
        formControls.forEach(control => {
            control.addEventListener('focus', this.handleInputFocus.bind(this));
            control.addEventListener('blur', this.handleInputBlur.bind(this));
            control.addEventListener('input', this.handleInputChange.bind(this));
        });

        // Keyboard navigation
        document.addEventListener('keydown', this.handleKeyNavigation.bind(this));

        // Language toggle animation
        const languageBtn = document.querySelector('.language-btn');
        if (languageBtn) {
            languageBtn.addEventListener('mouseenter', this.animateLanguageBtn.bind(this));
            languageBtn.addEventListener('mouseleave', this.resetLanguageBtn.bind(this));
        }
    }

    setupAnimations() {
        // Entrance animation
        const loginCard = document.querySelector('.login-card');
        if (loginCard) {
            loginCard.style.opacity = '0';
            loginCard.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                loginCard.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                loginCard.style.opacity = '1';
                loginCard.style.transform = 'translateY(0)';
            }, 100);
        }

        // Staggered animation for form elements
        const formElements = document.querySelectorAll('.mb-4, .d-grid');
        formElements.forEach((element, index) => {
            element.style.opacity = '0';
            element.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                element.style.transition = 'all 0.4s ease';
                element.style.opacity = '1';
                element.style.transform = 'translateY(0)';
            }, 200 + (index * 100));
        });

        // Security notice pulse animation
        setTimeout(() => {
            const securityNotice = document.querySelector('.text-center .d-inline-flex');
            if (securityNotice) {
                securityNotice.style.animation = 'pulse 2s infinite';
            }
        }, 2000);
    }

    setupValidation() {
        const form = document.querySelector('.needs-validation');
        if (!form) return;

        // Real-time validation
        const inputs = form.querySelectorAll('input[required]');
        inputs.forEach(input => {
            input.addEventListener('blur', () => this.validateField(input));
            input.addEventListener('input', () => this.clearFieldError(input));
        });
    }

    setupAccessibility() {
        // Focus management
        const emailField = document.getElementById('email');
        if (emailField) {
            emailField.focus();
        }

        // ARIA labels
        const togglePassword = document.getElementById('togglePassword');
        if (togglePassword) {
            togglePassword.setAttribute('aria-label', 'Toggle password visibility');
        }

        // Update current year
        const currentYear = document.getElementById('currentYear');
        if (currentYear) {
            currentYear.textContent = new Date().getFullYear();
        }
    }

    togglePasswordVisibility(e) {
        const passwordField = document.getElementById('password');
        const icon = e.target.querySelector('i') || e.target;
        
        if (passwordField.type === 'password') {
            passwordField.type = 'text';
            icon.classList.remove('fa-eye');
            icon.classList.add('fa-eye-slash');
            e.target.setAttribute('title', 'Hide password');
            e.target.setAttribute('aria-label', 'Hide password');
        } else {
            passwordField.type = 'password';
            icon.classList.remove('fa-eye-slash');
            icon.classList.add('fa-eye');
            e.target.setAttribute('title', 'Show password');
            e.target.setAttribute('aria-label', 'Show password');
        }
    }

    handleFormSubmit(e) {
        const form = e.target;
        
        if (!form.checkValidity()) {
            e.preventDefault();
            e.stopPropagation();
            
            // Animate invalid fields
            const invalidFields = form.querySelectorAll(':invalid');
            invalidFields.forEach(field => {
                this.animateFieldError(field);
            });
        } else {
            // Show loading state
            this.showLoadingState(form);
        }
        
        form.classList.add('was-validated');
    }

    handleInputFocus(e) {
        const inputGroup = e.target.closest('.input-group');
        if (inputGroup) {
            inputGroup.classList.add('focused');
        }
    }

    handleInputBlur(e) {
        const inputGroup = e.target.closest('.input-group');
        if (inputGroup && !e.target.value) {
            inputGroup.classList.remove('focused');
        }
    }

    handleInputChange(e) {
        if (e.target.value) {
            const inputGroup = e.target.closest('.input-group');
            if (inputGroup) {
                inputGroup.classList.add('focused');
            }
        }
    }

    handleKeyNavigation(e) {
        if (e.key === 'Enter') {
            const activeElement = document.activeElement;
            if (activeElement.id === 'email') {
                document.getElementById('password').focus();
                e.preventDefault();
            }
        }
    }

    animateLanguageBtn(e) {
        e.target.style.transform = 'translateY(-2px) scale(1.05)';
    }

    resetLanguageBtn(e) {
        e.target.style.transform = 'translateY(0) scale(1)';
    }

    validateField(field) {
        if (!field.checkValidity()) {
            this.showFieldError(field);
        } else {
            this.clearFieldError(field);
        }
    }

    showFieldError(field) {
        field.classList.add('is-invalid');
        this.animateFieldError(field);
    }

    clearFieldError(field) {
        field.classList.remove('is-invalid');
        field.classList.add('is-valid');
    }

    animateFieldError(field) {
        field.style.animation = 'shake 0.5s ease-in-out';
        setTimeout(() => {
            field.style.animation = '';
        }, 500);
    }

    showLoadingState(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn) {
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Signing in...';
            submitBtn.disabled = true;
            submitBtn.classList.add('btn-loading');
            
            // Store original text for potential restoration
            submitBtn.dataset.originalText = originalText;
        }
    }

    // Utility method to restore button state (if needed)
    restoreButtonState(form) {
        const submitBtn = form.querySelector('button[type="submit"]');
        if (submitBtn && submitBtn.dataset.originalText) {
            submitBtn.innerHTML = submitBtn.dataset.originalText;
            submitBtn.disabled = false;
            submitBtn.classList.remove('btn-loading');
        }
    }
}

// Initialize when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new LoginManager();
});

// Export for potential external use
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LoginManager;
}
