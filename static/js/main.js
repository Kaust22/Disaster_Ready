// Disaster Preparedness Education Platform - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    'use strict';
    
    // Initialize the application
    initializeApp();
    
    // Initialize Feather Icons
    if (typeof feather !== 'undefined') {
        feather.replace();
    }
    
    // Initialize Bootstrap tooltips
    initializeTooltips();
    
    // Initialize smooth scrolling
    initializeSmoothScrolling();
    
    // Initialize form enhancements
    initializeFormEnhancements();
    
    // Initialize reading progress tracker
    initializeReadingProgress();
    
    // Initialize timer functionality
    initializeTimers();
    
    // Initialize notification system
    initializeNotifications();
    
    // Initialize accessibility features
    initializeAccessibility();
});

/**
 * Initialize the main application
 */
function initializeApp() {
    console.log('Disaster Preparedness Education Platform loaded');
    
    // Add loading states
    document.body.classList.add('loaded');
    
    // Initialize page-specific functionality
    const currentPage = getCurrentPage();
    switch(currentPage) {
        case 'dashboard':
            initializeDashboard();
            break;
        case 'module':
            initializeModuleDetail();
            break;
        case 'quiz':
            initializeQuiz();
            break;
        case 'drill':
            initializeDrill();
            break;
        case 'emergency':
            initializeEmergencyContacts();
            break;
        case 'admin':
            initializeAdminDashboard();
            break;
    }
}

/**
 * Get current page identifier
 */
function getCurrentPage() {
    const path = window.location.pathname;
    if (path.includes('dashboard')) return 'dashboard';
    if (path.includes('module')) return 'module';
    if (path.includes('quiz')) return 'quiz';
    if (path.includes('drill')) return 'drill';
    if (path.includes('emergency')) return 'emergency';
    if (path.includes('admin-dashboard')) return 'admin';
    return 'home';
}

/**
 * Initialize Bootstrap tooltips
 */
function initializeTooltips() {
    if (typeof bootstrap !== 'undefined') {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl, {
                delay: { "show": 500, "hide": 100 }
            });
        });
    }
}

/**
 * Initialize smooth scrolling for anchor links
 */
function initializeSmoothScrolling() {
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                e.preventDefault();
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

/**
 * Initialize form enhancements
 */
function initializeFormEnhancements() {
    // Add floating labels effect
    const formInputs = document.querySelectorAll('.form-control, .form-select');
    
    formInputs.forEach(input => {
        // Add focus/blur handlers for better UX
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
            if (this.value.trim() === '') {
                this.parentElement.classList.remove('filled');
            } else {
                this.parentElement.classList.add('filled');
            }
        });
        
        // Check initial state
        if (input.value.trim() !== '') {
            input.parentElement.classList.add('filled');
        }
    });
    
    // Add form validation enhancements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            // Add loading state to submit buttons
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.classList.add('loading');
                submitBtn.disabled = true;
                
                // Reset after 5 seconds if form doesn't submit
                setTimeout(() => {
                    submitBtn.classList.remove('loading');
                    submitBtn.disabled = false;
                }, 5000);
            }
        });
    });
}

/**
 * Initialize reading progress tracker
 */
function initializeReadingProgress() {
    const progressBar = document.getElementById('readingProgress');
    const content = document.getElementById('moduleContent');
    
    if (progressBar && content) {
        let startTime = Date.now();
        
        function updateProgress() {
            const contentHeight = content.scrollHeight;
            const windowHeight = window.innerHeight;
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            // Calculate progress based on scroll position
            const progress = Math.min(100, (scrollTop / (contentHeight - windowHeight + 100)) * 100);
            progressBar.style.width = progress + '%';
            
            // Update time spent
            const timeSpentInput = document.getElementById('timeSpent');
            if (timeSpentInput) {
                const timeSpent = Math.floor((Date.now() - startTime) / 1000);
                timeSpentInput.value = timeSpent;
            }
            
            // Show completion button when user reaches end
            if (progress >= 90) {
                const completeBtn = document.getElementById('completeBtn');
                if (completeBtn && !completeBtn.classList.contains('pulse')) {
                    completeBtn.classList.add('pulse');
                    showNotification('You\'ve almost finished reading! Click "Mark as Complete" when ready.', 'info');
                }
            }
        }
        
        // Throttled scroll handler
        let ticking = false;
        function throttledUpdateProgress() {
            if (!ticking) {
                requestAnimationFrame(updateProgress);
                ticking = true;
                setTimeout(() => { ticking = false; }, 100);
            }
        }
        
        window.addEventListener('scroll', throttledUpdateProgress);
        updateProgress(); // Initial call
    }
}

/**
 * Initialize timer functionality
 */
function initializeTimers() {
    const timeDisplay = document.getElementById('timeDisplay');
    const timeTakenInput = document.getElementById('timeTaken');
    
    if (timeDisplay) {
        const startTime = Date.now();
        
        function updateTimer() {
            const elapsed = Math.floor((Date.now() - startTime) / 1000);
            const minutes = Math.floor(elapsed / 60);
            const seconds = elapsed % 60;
            
            timeDisplay.textContent = 
                String(minutes).padStart(2, '0') + ':' + String(seconds).padStart(2, '0');
                
            if (timeTakenInput) {
                timeTakenInput.value = elapsed;
            }
        }
        
        // Update every second
        const timerInterval = setInterval(updateTimer, 1000);
        updateTimer(); // Initial call
        
        // Clear timer when page unloads
        window.addEventListener('beforeunload', () => {
            clearInterval(timerInterval);
        });
    }
}

/**
 * Initialize notification system
 */
function initializeNotifications() {
    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
    alerts.forEach(alert => {
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateY(-100%)';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }
        }, 5000);
    });
}

/**
 * Show notification to user
 */
function showNotification(message, type = 'info', duration = 4000) {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show notification-toast`;
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        max-width: 500px;
        animation: slideInRight 0.3s ease;
    `;
    
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after duration
    setTimeout(() => {
        if (notification.parentNode) {
            notification.style.animation = 'slideOutRight 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }
    }, duration);
}

/**
 * Initialize accessibility features
 */
function initializeAccessibility() {
    // Add keyboard navigation for cards
    const cards = document.querySelectorAll('.card[tabindex]');
    cards.forEach(card => {
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                const link = this.querySelector('a');
                if (link) {
                    e.preventDefault();
                    link.click();
                }
            }
        });
    });
    
    // Improve focus visibility
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('keyboard-navigation');
        }
    });
    
    document.addEventListener('mousedown', function() {
        document.body.classList.remove('keyboard-navigation');
    });
    
    // Skip to main content link
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'skip-link';
    skipLink.style.cssText = `
        position: absolute;
        top: -40px;
        left: 6px;
        background: #000;
        color: #fff;
        padding: 8px;
        text-decoration: none;
        z-index: 10000;
        border-radius: 4px;
    `;
    
    skipLink.addEventListener('focus', function() {
        this.style.top = '6px';
    });
    
    skipLink.addEventListener('blur', function() {
        this.style.top = '-40px';
    });
    
    document.body.insertBefore(skipLink, document.body.firstChild);
}

/**
 * Dashboard specific initialization
 */
function initializeDashboard() {
    // Animate progress bars
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach((bar, index) => {
        const width = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = width;
        }, 200 + (index * 100));
    });
    
    // Add hover effects to disaster cards
    const disasterCards = document.querySelectorAll('.disaster-card');
    disasterCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
}

/**
 * Module detail page initialization
 */
function initializeModuleDetail() {
    // Add reading time estimation
    const content = document.getElementById('moduleContent');
    if (content) {
        const wordCount = content.textContent.split(/\s+/).length;
        const readingTime = Math.ceil(wordCount / 200); // 200 WPM average
        
        const timeEstimate = document.querySelector('.reading-time');
        if (timeEstimate) {
            timeEstimate.textContent = `${readingTime} min read`;
        }
    }
    
    // Add smooth reveal animation for content sections
    const contentSections = content?.querySelectorAll('h3, h4, p, ul, ol');
    if (contentSections) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
                }
            });
        }, { threshold: 0.1 });
        
        contentSections.forEach(section => {
            section.style.opacity = '0';
            section.style.transform = 'translateY(20px)';
            observer.observe(section);
        });
    }
}

/**
 * Quiz page initialization
 */
function initializeQuiz() {
    const quizForm = document.getElementById('quizForm');
    if (!quizForm) return;
    
    const totalQuestions = document.querySelectorAll('.question-card').length;
    let startTime = Date.now();
    
    // Progress tracking function
    window.updateProgress = function() {
        const answeredQuestions = document.querySelectorAll('input[type="radio"]:checked').length;
        const progress = (answeredQuestions / totalQuestions) * 100;
        
        const progressBar = document.getElementById('quizProgress');
        const progressText = document.getElementById('progressText');
        const submitBtn = document.getElementById('submitBtn');
        
        if (progressBar) progressBar.style.width = progress + '%';
        if (progressText) progressText.textContent = `${answeredQuestions} of ${totalQuestions} answered`;
        
        // Enable submit button when all questions are answered
        if (submitBtn) {
            if (answeredQuestions === totalQuestions) {
                submitBtn.disabled = false;
                submitBtn.classList.add('pulse');
                showNotification('All questions answered! You can now submit your quiz.', 'success');
            } else {
                submitBtn.disabled = true;
                submitBtn.classList.remove('pulse');
            }
        }
    };
    
    // Add change listeners to all radio buttons
    const radioButtons = document.querySelectorAll('input[type="radio"]');
    radioButtons.forEach(radio => {
        radio.addEventListener('change', updateProgress);
    });
    
    // Form submission with confirmation
    quizForm.addEventListener('submit', function(e) {
        const answeredQuestions = document.querySelectorAll('input[type="radio"]:checked').length;
        
        if (answeredQuestions < totalQuestions) {
            e.preventDefault();
            showNotification('Please answer all questions before submitting.', 'warning');
            return;
        }
        
        if (!confirm('Are you sure you want to submit your quiz? You cannot change your answers after submission.')) {
            e.preventDefault();
            return;
        }
        
        // Update time taken
        const timeTakenInput = document.getElementById('timeTaken');
        if (timeTakenInput) {
            timeTakenInput.value = Math.floor((Date.now() - startTime) / 1000);
        }
    });
    
    // Add visual feedback for selected answers
    radioButtons.forEach(radio => {
        radio.addEventListener('change', function() {
            // Remove selection styling from all options in this question
            const questionCard = this.closest('.question-card');
            const allLabels = questionCard.querySelectorAll('.form-check-label');
            
            allLabels.forEach(label => {
                label.classList.remove('selected');
            });
            
            // Add selection styling to chosen option
            const selectedLabel = this.nextElementSibling;
            if (selectedLabel) {
                selectedLabel.classList.add('selected');
            }
        });
    });
}

/**
 * Drill page initialization
 */
function initializeDrill() {
    const drillForm = document.getElementById('drillForm');
    if (!drillForm) return;
    
    const totalSteps = document.querySelectorAll('.step-card').length;
    
    // Progress tracking function
    window.updateProgress = function() {
        const completedSteps = document.querySelectorAll('input[type="checkbox"]:checked').length;
        const progress = (completedSteps / totalSteps) * 100;
        
        const progressBar = document.getElementById('drillProgress');
        const progressText = document.getElementById('progressText');
        const submitBtn = document.getElementById('submitBtn');
        
        if (progressBar) progressBar.style.width = progress + '%';
        if (progressText) progressText.textContent = `${completedSteps} of ${totalSteps} steps completed`;
        
        // Add visual feedback for completed steps
        document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
            const stepCard = checkbox.closest('.step-card');
            if (checkbox.checked) {
                stepCard.classList.add('completed');
            } else {
                stepCard.classList.remove('completed');
            }
        });
        
        // Pulse submit button when drill is complete
        if (submitBtn) {
            if (completedSteps === totalSteps) {
                submitBtn.classList.add('pulse');
                showNotification('All steps completed! Great job on completing the drill.', 'success');
            } else {
                submitBtn.classList.remove('pulse');
            }
        }
    };
    
    // Add change listeners to all checkboxes
    const checkboxes = document.querySelectorAll('input[type="checkbox"]');
    checkboxes.forEach(checkbox => {
        checkbox.addEventListener('change', updateProgress);
        
        // Time limit warnings for critical steps
        if (checkbox.hasAttribute('data-time-limit')) {
            checkbox.addEventListener('change', function() {
                if (this.checked) {
                    const timeLimit = parseInt(this.getAttribute('data-time-limit'));
                    const stepCard = this.closest('.step-card');
                    
                    // Add time pressure visual effect
                    stepCard.style.animation = `timeLimit ${timeLimit}s ease-out`;
                    
                    // Show time warning
                    if (timeLimit <= 10) {
                        showNotification(`Quick! Complete this critical step within ${timeLimit} seconds.`, 'warning', 2000);
                    }
                }
            });
        }
    });
    
    // Form submission with completion summary
    drillForm.addEventListener('submit', function(e) {
        const completedSteps = document.querySelectorAll('input[type="checkbox"]:checked').length;
        const completionRate = Math.round((completedSteps / totalSteps) * 100);
        
        if (!confirm(`You completed ${completedSteps} out of ${totalSteps} steps (${completionRate}%). Submit your drill results?`)) {
            e.preventDefault();
        }
    });
}

/**
 * Emergency contacts page initialization
 */
function initializeEmergencyContacts() {
    // Copy to clipboard functionality
    window.copyToClipboard = function(text) {
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text).then(() => {
                showCopyToast();
            }).catch(err => {
                fallbackCopyToClipboard(text);
            });
        } else {
            fallbackCopyToClipboard(text);
        }
    };
    
    function fallbackCopyToClipboard(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.opacity = '0';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            showCopyToast();
        } catch (err) {
            console.error('Could not copy text: ', err);
            showNotification('Could not copy to clipboard. Please copy manually.', 'error');
        }
        
        document.body.removeChild(textArea);
    }
    
    function showCopyToast() {
        const toast = document.getElementById('copyToast');
        if (toast && typeof bootstrap !== 'undefined') {
            const bsToast = new bootstrap.Toast(toast);
            bsToast.show();
        } else {
            showNotification('Phone number copied to clipboard!', 'success', 2000);
        }
    }
    
    // Download contacts functionality
    window.downloadContacts = function() {
        let contactText = "EMERGENCY CONTACTS\n";
        contactText += "==================\n\n";
        contactText += "NATIONAL EMERGENCY NUMBERS (INDIA)\n";
        contactText += "National Emergency: 112\n";
        contactText += "Fire Department: 101\n";
        contactText += "Police: 100\n";
        contactText += "Medical Emergency: 108\n\n";
        
        // Add contact groups
        const contactGroups = document.querySelectorAll('.card');
        contactGroups.forEach(group => {
            const title = group.querySelector('.card-header h4');
            if (title && title.textContent.trim() !== 'Important Notes' && title.textContent.trim() !== 'Quick Actions') {
                contactText += title.textContent.trim().toUpperCase() + "\n";
                contactText += "=".repeat(title.textContent.trim().length) + "\n";
                
                const contacts = group.querySelectorAll('.contact-item');
                contacts.forEach(contact => {
                    const name = contact.querySelector('h6');
                    const org = contact.querySelector('.text-muted');
                    const phone = contact.querySelector('.phone-number');
                    const email = contact.querySelector('a[href^="mailto:"]');
                    
                    if (name && org && phone) {
                        contactText += `${name.textContent} - ${org.textContent}\n`;
                        contactText += `Phone: ${phone.textContent}\n`;
                        if (email) {
                            contactText += `Email: ${email.textContent}\n`;
                        }
                        contactText += "\n";
                    }
                });
                contactText += "\n";
            }
        });
        
        const blob = new Blob([contactText], { type: 'text/plain' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'emergency_contacts.txt';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        
        showNotification('Emergency contacts downloaded successfully!', 'success');
    };
}

/**
 * Admin dashboard initialization
 */
function initializeAdminDashboard() {
    // Animate statistics
    const statNumbers = document.querySelectorAll('.stat-item .h2, .stat-item .h4');
    statNumbers.forEach(stat => {
        const finalValue = parseInt(stat.textContent);
        if (!isNaN(finalValue)) {
            animateCounter(stat, 0, finalValue, 1000);
        }
    });
    
    // Animate progress bars with delay
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach((bar, index) => {
        const width = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.width = width;
        }, 500 + (index * 200));
    });
}

/**
 * Animate counter from start to end value
 */
function animateCounter(element, start, end, duration) {
    const startTime = performance.now();
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const current = Math.floor(progress * (end - start) + start);
        element.textContent = current;
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = end;
        }
    }
    
    requestAnimationFrame(updateCounter);
}

/**
 * Utility function to format time
 */
function formatTime(seconds) {
    const hours = Math.floor(seconds / 3600);
    const minutes = Math.floor((seconds % 3600) / 60);
    const secs = seconds % 60;
    
    if (hours > 0) {
        return `${hours}:${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    } else {
        return `${String(minutes).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }
}

/**
 * Utility function to debounce function calls
 */
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

/**
 * Utility function to throttle function calls
 */
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
    }
}

// Add CSS animations dynamically
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(100%);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideOutRight {
        from {
            opacity: 1;
            transform: translateX(0);
        }
        to {
            opacity: 0;
            transform: translateX(100%);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .notification-toast {
        animation: slideInRight 0.3s ease;
    }
    
    .form-check-label.selected {
        background-color: rgba(13, 110, 253, 0.2) !important;
        border: 2px solid var(--bs-primary) !important;
        font-weight: 600;
    }
    
    .keyboard-navigation *:focus {
        outline: 2px solid #0d6efd !important;
        outline-offset: 2px !important;
    }
    
    .btn.loading {
        position: relative;
        color: transparent !important;
    }
    
    .btn.loading::after {
        content: "";
        position: absolute;
        width: 16px;
        height: 16px;
        top: 50%;
        left: 50%;
        margin-left: -8px;
        margin-top: -8px;
        border: 2px solid #ffffff;
        border-radius: 50%;
        border-top-color: transparent;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
`;
document.head.appendChild(style);

// Export functions for global access
window.DisasterPrepApp = {
    showNotification,
    formatTime,
    debounce,
    throttle,
    animateCounter
};
