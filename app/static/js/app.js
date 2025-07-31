// Custom JavaScript for Flask Blog

document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    var popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    var popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);
    
    // Confirm delete actions
    var deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
                e.preventDefault();
            }
        });
    });
    
    // Search functionality
    var searchForm = document.querySelector('#searchForm');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            var searchInput = document.querySelector('#searchInput');
            if (searchInput && searchInput.value.trim() === '') {
                e.preventDefault();
                alert('Please enter a search term.');
            }
        });
    }
    
    // Form validation
    var forms = document.querySelectorAll('.needs-validation');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Auto-resize textareas
    var textareas = document.querySelectorAll('textarea');
    textareas.forEach(function(textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = this.scrollHeight + 'px';
        });
    });
    
    // Lazy loading for images
    var images = document.querySelectorAll('img[data-src]');
    if ('IntersectionObserver' in window) {
        var imageObserver = new IntersectionObserver(function(entries, observer) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    var img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        images.forEach(function(img) {
            imageObserver.observe(img);
        });
    }
    
    // Smooth scrolling for anchor links
    var anchorLinks = document.querySelectorAll('a[href^="#"]');
    anchorLinks.forEach(function(link) {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            var target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Copy to clipboard functionality
    var copyButtons = document.querySelectorAll('.btn-copy');
    copyButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            var textToCopy = this.getAttribute('data-clipboard-text');
            if (navigator.clipboard) {
                navigator.clipboard.writeText(textToCopy).then(function() {
                    showToast('Copied to clipboard!', 'success');
                }).catch(function() {
                    showToast('Failed to copy to clipboard', 'error');
                });
            } else {
                // Fallback for older browsers
                var textArea = document.createElement('textarea');
                textArea.value = textToCopy;
                document.body.appendChild(textArea);
                textArea.select();
                document.execCommand('copy');
                document.body.removeChild(textArea);
                showToast('Copied to clipboard!', 'success');
            }
        });
    });
    
    // Toast notification function
    function showToast(message, type = 'info') {
        var toastContainer = document.querySelector('#toastContainer');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toastContainer';
            toastContainer.className = 'position-fixed top-0 end-0 p-3';
            toastContainer.style.zIndex = '1050';
            document.body.appendChild(toastContainer);
        }
        
        var toastId = 'toast-' + Date.now();
        var toastHtml = `
            <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header">
                    <strong class="me-auto">${type.charAt(0).toUpperCase() + type.slice(1)}</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHtml);
        var toastElement = document.querySelector('#' + toastId);
        var toast = new bootstrap.Toast(toastElement);
        toast.show();
        
        // Remove toast element after it's hidden
        toastElement.addEventListener('hidden.bs.toast', function() {
            toastElement.remove();
        });
    }
    
    // API request helper
    window.apiRequest = function(url, options = {}) {
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        const finalOptions = Object.assign({}, defaultOptions, options);
        
        return fetch(url, finalOptions)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .catch(error => {
                console.error('API request failed:', error);
                throw error;
            });
    };
    
    // Loading spinner
    window.showLoading = function(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        if (element) {
            element.innerHTML = '<div class="text-center"><div class="spinner-border" role="status"><span class="visually-hidden">Loading...</span></div></div>';
        }
    };
    
    window.hideLoading = function(element) {
        if (typeof element === 'string') {
            element = document.querySelector(element);
        }
        if (element) {
            element.innerHTML = '';
        }
    };
    
    // Debounce function for search
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
    
    // Live search functionality
    var searchInput = document.querySelector('#liveSearch');
    if (searchInput) {
        var debouncedSearch = debounce(function(query) {
            if (query.length >= 2) {
                showLoading('#searchResults');
                apiRequest(`/api/v1/search?q=${encodeURIComponent(query)}`)
                    .then(data => {
                        updateSearchResults(data);
                    })
                    .catch(error => {
                        console.error('Search failed:', error);
                        hideLoading('#searchResults');
                    });
            } else {
                hideLoading('#searchResults');
            }
        }, 300);
        
        searchInput.addEventListener('input', function() {
            debouncedSearch(this.value);
        });
    }
    
    function updateSearchResults(data) {
        var resultsContainer = document.querySelector('#searchResults');
        if (resultsContainer && data.posts) {
            var html = '';
            data.posts.forEach(post => {
                html += `
                    <div class="card mb-3">
                        <div class="card-body">
                            <h5 class="card-title">
                                <a href="/post/${post.slug}" class="text-decoration-none">${post.title}</a>
                            </h5>
                            <p class="card-text">${post.excerpt || post.content.substring(0, 150)}...</p>
                            <div class="text-muted small">
                                By ${post.author.username} • ${new Date(post.created_at).toLocaleDateString()}
                            </div>
                        </div>
                    </div>
                `;
            });
            resultsContainer.innerHTML = html;
        }
    }
    
    // Initialize any additional functionality
    console.log('Flask Blog JavaScript loaded successfully!');
}); 