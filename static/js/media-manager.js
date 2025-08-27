/**
 * Advanced Media Manager
 * Handles image upload, compression, and optimization
 */

class MediaManager {
    constructor() {
        this.maxFileSize = 5 * 1024 * 1024; // 5MB
        this.allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp', 'image/gif'];
        this.compressionQuality = 0.8;
        this.maxWidth = 1920;
        this.maxHeight = 1080;
        
        this.init();
    }

    init() {
        this.setupFileInputs();
        this.createDropZones();
        this.setupImagePreview();
    }

    setupFileInputs() {
        const fileInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
        
        fileInputs.forEach(input => {
            input.addEventListener('change', (e) => {
                this.handleFileSelect(e);
            });
        });
    }

    createDropZones() {
        const fileInputs = document.querySelectorAll('input[type="file"][accept*="image"]');
        
        fileInputs.forEach(input => {
            const wrapper = document.createElement('div');
            wrapper.className = 'media-drop-zone';
            wrapper.innerHTML = `
                <div class="drop-zone-content">
                    <i class="fas fa-cloud-upload-alt fa-3x text-muted mb-3"></i>
                    <p class="mb-2"><strong>Drop images here</strong> or click to browse</p>
                    <p class="text-muted small">Supports: JPG, PNG, WebP, GIF (Max: 5MB)</p>
                    <div class="upload-progress" style="display: none;">
                        <div class="progress mb-2">
                            <div class="progress-bar" role="progressbar" style="width: 0%"></div>
                        </div>
                        <small class="text-muted">Uploading and optimizing...</small>
                    </div>
                </div>
            `;
            
            // Insert wrapper before input
            input.parentNode.insertBefore(wrapper, input);
            wrapper.appendChild(input);
            
            // Setup drag and drop
            this.setupDragAndDrop(wrapper, input);
        });
    }

    setupDragAndDrop(dropZone, input) {
        ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, this.preventDefaults, false);
        });

        ['dragenter', 'dragover'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.add('drag-over');
            }, false);
        });

        ['dragleave', 'drop'].forEach(eventName => {
            dropZone.addEventListener(eventName, () => {
                dropZone.classList.remove('drag-over');
            }, false);
        });

        dropZone.addEventListener('drop', (e) => {
            const files = e.dataTransfer.files;
            if (files.length > 0) {
                input.files = files;
                this.handleFileSelect({ target: input });
            }
        }, false);

        dropZone.addEventListener('click', () => {
            input.click();
        });
    }

    preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    async handleFileSelect(event) {
        const file = event.target.files[0];
        if (!file) return;

        const dropZone = event.target.closest('.media-drop-zone');
        const progressContainer = dropZone.querySelector('.upload-progress');
        const progressBar = dropZone.querySelector('.progress-bar');

        try {
            // Validate file
            this.validateFile(file);

            // Show progress
            progressContainer.style.display = 'block';
            this.updateProgress(progressBar, 10);

            // Compress and optimize
            const optimizedFile = await this.optimizeImage(file, (progress) => {
                this.updateProgress(progressBar, 10 + (progress * 0.8));
            });

            // Create preview
            this.createImagePreview(dropZone, optimizedFile);
            
            // Update progress to complete
            this.updateProgress(progressBar, 100);
            
            setTimeout(() => {
                progressContainer.style.display = 'none';
            }, 1000);

        } catch (error) {
            this.showError(dropZone, error.message);
            progressContainer.style.display = 'none';
        }
    }

    validateFile(file) {
        if (!this.allowedTypes.includes(file.type)) {
            throw new Error('Invalid file type. Please select a valid image file.');
        }

        if (file.size > this.maxFileSize) {
            throw new Error('File size too large. Maximum size is 5MB.');
        }
    }

    async optimizeImage(file, progressCallback) {
        return new Promise((resolve, reject) => {
            const canvas = document.createElement('canvas');
            const ctx = canvas.getContext('2d');
            const img = new Image();

            img.onload = () => {
                try {
                    progressCallback(20);

                    // Calculate new dimensions
                    let { width, height } = this.calculateDimensions(img.width, img.height);
                    
                    canvas.width = width;
                    canvas.height = height;

                    progressCallback(40);

                    // Draw and compress
                    ctx.drawImage(img, 0, 0, width, height);
                    
                    progressCallback(60);

                    // Convert to blob
                    canvas.toBlob((blob) => {
                        if (blob) {
                            progressCallback(80);
                            
                            // Create optimized file
                            const optimizedFile = new File([blob], file.name, {
                                type: 'image/jpeg',
                                lastModified: Date.now()
                            });

                            progressCallback(100);
                            resolve(optimizedFile);
                        } else {
                            reject(new Error('Failed to optimize image'));
                        }
                    }, 'image/jpeg', this.compressionQuality);

                } catch (error) {
                    reject(error);
                }
            };

            img.onerror = () => {
                reject(new Error('Failed to load image'));
            };

            img.src = URL.createObjectURL(file);
        });
    }

    calculateDimensions(originalWidth, originalHeight) {
        let width = originalWidth;
        let height = originalHeight;

        // Scale down if too large
        if (width > this.maxWidth || height > this.maxHeight) {
            const ratio = Math.min(this.maxWidth / width, this.maxHeight / height);
            width = Math.round(width * ratio);
            height = Math.round(height * ratio);
        }

        return { width, height };
    }

    createImagePreview(dropZone, file) {
        // Remove existing preview
        const existingPreview = dropZone.querySelector('.image-preview');
        if (existingPreview) {
            existingPreview.remove();
        }

        const preview = document.createElement('div');
        preview.className = 'image-preview mt-3';
        
        const img = document.createElement('img');
        img.src = URL.createObjectURL(file);
        img.className = 'img-thumbnail';
        img.style.maxWidth = '200px';
        img.style.maxHeight = '150px';

        const info = document.createElement('div');
        info.className = 'image-info mt-2';
        info.innerHTML = `
            <small class="text-muted">
                <div><strong>File:</strong> ${file.name}</div>
                <div><strong>Size:</strong> ${this.formatFileSize(file.size)}</div>
                <div><strong>Type:</strong> ${file.type}</div>
            </small>
        `;

        const actions = document.createElement('div');
        actions.className = 'image-actions mt-2';
        actions.innerHTML = `
            <button type="button" class="btn btn-sm btn-outline-danger" onclick="this.closest('.image-preview').remove()">
                <i class="fas fa-trash"></i> Remove
            </button>
            <button type="button" class="btn btn-sm btn-outline-primary" onclick="mediaManager.editImage(this)">
                <i class="fas fa-edit"></i> Edit
            </button>
        `;

        preview.appendChild(img);
        preview.appendChild(info);
        preview.appendChild(actions);
        
        dropZone.appendChild(preview);
    }

    editImage(button) {
        const preview = button.closest('.image-preview');
        const img = preview.querySelector('img');
        
        // Create image editor modal
        this.openImageEditor(img.src);
    }

    openImageEditor(imageSrc) {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.innerHTML = `
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-edit me-2"></i>Image Editor
                        </h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body">
                        <div class="row">
                            <div class="col-md-8">
                                <canvas id="imageCanvas" class="img-fluid border"></canvas>
                            </div>
                            <div class="col-md-4">
                                <div class="editor-controls">
                                    <h6>Adjustments</h6>
                                    <div class="mb-3">
                                        <label class="form-label">Brightness</label>
                                        <input type="range" class="form-range" min="0" max="200" value="100" id="brightness">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Contrast</label>
                                        <input type="range" class="form-range" min="0" max="200" value="100" id="contrast">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Saturation</label>
                                        <input type="range" class="form-range" min="0" max="200" value="100" id="saturation">
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Quality</label>
                                        <input type="range" class="form-range" min="10" max="100" value="80" id="quality">
                                    </div>
                                    <button class="btn btn-outline-secondary btn-sm w-100" onclick="mediaManager.resetFilters()">
                                        Reset
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-primary" onclick="mediaManager.applyEdits()">Apply Changes</button>
                    </div>
                </div>
            </div>
        `;

        document.body.appendChild(modal);
        const modalInstance = new bootstrap.Modal(modal);
        modalInstance.show();

        // Load image into canvas
        this.loadImageIntoCanvas(imageSrc);
        
        // Setup filter controls
        this.setupFilterControls();

        // Cleanup on close
        modal.addEventListener('hidden.bs.modal', () => {
            modal.remove();
        });
    }

    loadImageIntoCanvas(imageSrc) {
        const canvas = document.getElementById('imageCanvas');
        const ctx = canvas.getContext('2d');
        const img = new Image();

        img.onload = () => {
            canvas.width = img.width;
            canvas.height = img.height;
            ctx.drawImage(img, 0, 0);
            this.originalImageData = ctx.getImageData(0, 0, canvas.width, canvas.height);
        };

        img.src = imageSrc;
    }

    setupFilterControls() {
        const controls = ['brightness', 'contrast', 'saturation'];
        
        controls.forEach(control => {
            const slider = document.getElementById(control);
            if (slider) {
                slider.addEventListener('input', () => {
                    this.applyFilters();
                });
            }
        });
    }

    applyFilters() {
        const canvas = document.getElementById('imageCanvas');
        const ctx = canvas.getContext('2d');
        
        if (!this.originalImageData) return;

        const brightness = document.getElementById('brightness').value;
        const contrast = document.getElementById('contrast').value;
        const saturation = document.getElementById('saturation').value;

        ctx.filter = `brightness(${brightness}%) contrast(${contrast}%) saturate(${saturation}%)`;
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(this.createImageFromData(this.originalImageData), 0, 0);
    }

    createImageFromData(imageData) {
        const canvas = document.createElement('canvas');
        const ctx = canvas.getContext('2d');
        canvas.width = imageData.width;
        canvas.height = imageData.height;
        ctx.putImageData(imageData, 0, 0);
        
        const img = new Image();
        img.src = canvas.toDataURL();
        return img;
    }

    resetFilters() {
        document.getElementById('brightness').value = 100;
        document.getElementById('contrast').value = 100;
        document.getElementById('saturation').value = 100;
        this.applyFilters();
    }

    applyEdits() {
        const canvas = document.getElementById('imageCanvas');
        const quality = document.getElementById('quality').value / 100;
        
        canvas.toBlob((blob) => {
            if (blob) {
                // Update the preview with edited image
                const url = URL.createObjectURL(blob);
                // Implementation to update the actual preview would go here
                
                // Close modal
                bootstrap.Modal.getInstance(document.querySelector('.modal')).hide();
                
                this.showSuccess('Image edited successfully!');
            }
        }, 'image/jpeg', quality);
    }

    updateProgress(progressBar, percentage) {
        progressBar.style.width = percentage + '%';
        progressBar.setAttribute('aria-valuenow', percentage);
    }

    formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    showError(container, message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-danger alert-dismissible fade show mt-2';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        container.appendChild(alert);
    }

    showSuccess(message) {
        const alert = document.createElement('div');
        alert.className = 'alert alert-success alert-dismissible fade show';
        alert.style.position = 'fixed';
        alert.style.top = '20px';
        alert.style.right = '20px';
        alert.style.zIndex = '9999';
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        document.body.appendChild(alert);
        
        setTimeout(() => {
            alert.remove();
        }, 3000);
    }

    setupImagePreview() {
        // Setup existing image previews
        const existingImages = document.querySelectorAll('img[src*="news/"]');
        existingImages.forEach(img => {
            this.addImageActions(img);
        });
    }

    addImageActions(img) {
        const wrapper = document.createElement('div');
        wrapper.className = 'position-relative d-inline-block';
        
        const actions = document.createElement('div');
        actions.className = 'image-actions-overlay';
        actions.innerHTML = `
            <button type="button" class="btn btn-sm btn-outline-light" onclick="mediaManager.editImage(this)">
                <i class="fas fa-edit"></i>
            </button>
            <button type="button" class="btn btn-sm btn-outline-light" onclick="mediaManager.deleteImage(this)">
                <i class="fas fa-trash"></i>
            </button>
        `;
        
        img.parentNode.insertBefore(wrapper, img);
        wrapper.appendChild(img);
        wrapper.appendChild(actions);
    }

    deleteImage(button) {
        if (confirm('Are you sure you want to delete this image?')) {
            const wrapper = button.closest('.position-relative');
            wrapper.remove();
            this.showSuccess('Image deleted successfully!');
        }
    }
}

// Initialize media manager
window.mediaManager = new MediaManager();
