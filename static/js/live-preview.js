/**
 * Live Preview System
 * Real-time preview of article content as user types
 */

class LivePreview {
    constructor() {
        this.previewWindow = null;
        this.previewContainer = null;
        this.isPreviewOpen = false;
        this.updateTimeout = null;
        this.currentLanguage = 'en';
        
        this.init();
    }

    init() {
        this.createPreviewButton();
        this.setupEventListeners();
        this.createPreviewModal();
    }

    createPreviewButton() {
        // Add preview button to the toolbar
        const toolbar = document.querySelector('.card-header .d-flex');
        if (toolbar) {
            const previewBtn = document.createElement('button');
            previewBtn.type = 'button';
            previewBtn.className = 'btn btn-outline-info ms-2';
            previewBtn.innerHTML = '<i class="fas fa-eye me-2"></i>Live Preview';
            previewBtn.onclick = () => this.togglePreview();
            
            toolbar.appendChild(previewBtn);
        }
    }

    createPreviewModal() {
        const modal = document.createElement('div');
        modal.className = 'modal fade';
        modal.id = 'livePreviewModal';
        modal.innerHTML = `
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">
                            <i class="fas fa-eye me-2"></i>Live Preview
                        </h5>
                        <div class="btn-group me-3">
                            <button type="button" class="btn btn-sm btn-outline-primary" onclick="livePreview.switchLanguage('en')">
                                English
                            </button>
                            <button type="button" class="btn btn-sm btn-outline-primary" onclick="livePreview.switchLanguage('ar')">
                                العربية
                            </button>
                        </div>
                        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                    </div>
                    <div class="modal-body p-0">
                        <div class="row g-0">
                            <div class="col-md-8">
                                <div class="preview-content p-4" id="preview-content">
                                    <div class="article-preview">
                                        <div class="article-meta mb-3">
                                            <span class="badge bg-primary" id="preview-category">News</span>
                                            <span class="text-muted ms-2" id="preview-date">${new Date().toLocaleDateString()}</span>
                                            <span class="text-muted ms-2" id="preview-reading-time">5 min read</span>
                                        </div>
                                        <h1 class="article-title mb-3" id="preview-title">Article Title</h1>
                                        <div class="article-excerpt mb-4" id="preview-excerpt">
                                            Article excerpt will appear here...
                                        </div>
                                        <div class="article-cover mb-4" id="preview-cover" style="display: none;">
                                            <img class="img-fluid rounded" alt="Cover Image">
                                        </div>
                                        <div class="article-content" id="preview-content-body">
                                            Article content will appear here...
                                        </div>
                                        <div class="article-tags mt-4" id="preview-tags"></div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-4 bg-light">
                                <div class="preview-sidebar p-3">
                                    <h6><i class="fas fa-chart-line me-2"></i>Content Analysis</h6>
                                    <div class="analysis-grid">
                                        <div class="analysis-item">
                                            <div class="analysis-value" id="preview-word-count">0</div>
                                            <div class="analysis-label">Words</div>
                                        </div>
                                        <div class="analysis-item">
                                            <div class="analysis-value" id="preview-reading-time-val">0</div>
                                            <div class="analysis-label">Min Read</div>
                                        </div>
                                        <div class="analysis-item">
                                            <div class="analysis-value" id="preview-seo-score">0</div>
                                            <div class="analysis-label">SEO Score</div>
                                        </div>
                                    </div>
                                    
                                    <h6 class="mt-4"><i class="fas fa-share-alt me-2"></i>Social Preview</h6>
                                    <div class="social-preview-card mb-3">
                                        <div class="social-preview-header">Facebook</div>
                                        <div class="social-preview-body">
                                            <div class="social-title" id="preview-fb-title">Title</div>
                                            <div class="social-url">yoursite.com/news/article</div>
                                            <div class="social-desc" id="preview-fb-desc">Description</div>
                                        </div>
                                    </div>
                                    
                                    <div class="social-preview-card">
                                        <div class="social-preview-header">Twitter</div>
                                        <div class="social-preview-body">
                                            <div class="social-title" id="preview-twitter-title">Title</div>
                                            <div class="social-url">yoursite.com/news/article</div>
                                            <div class="social-desc" id="preview-twitter-desc">Description</div>
                                        </div>
                                    </div>
                                    
                                    <h6 class="mt-4"><i class="fas fa-search me-2"></i>Search Preview</h6>
                                    <div class="search-preview">
                                        <div class="search-title" id="preview-search-title">Article Title</div>
                                        <div class="search-url">https://yoursite.com/news/article-slug</div>
                                        <div class="search-desc" id="preview-search-desc">Meta description appears here...</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                        <button type="button" class="btn btn-primary" onclick="livePreview.openInNewTab()">
                            <i class="fas fa-external-link-alt me-2"></i>Open in New Tab
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(modal);
        this.previewModal = new bootstrap.Modal(modal);
    }

    setupEventListeners() {
        // Listen for content changes
        const fieldsToWatch = [
            'title_en', 'title_ar', 'excerpt_en', 'excerpt_ar', 
            'content_en', 'content_ar', 'tags',
            'seo_title_en', 'seo_title_ar', 'seo_description_en', 'seo_description_ar',
            'og_title_en', 'og_title_ar', 'og_description_en', 'og_description_ar',
            'twitter_title_en', 'twitter_title_ar', 'twitter_description_en', 'twitter_description_ar'
        ];

        fieldsToWatch.forEach(fieldId => {
            const field = document.getElementById(fieldId);
            if (field) {
                field.addEventListener('input', () => {
                    if (this.isPreviewOpen) {
                        this.debounceUpdate();
                    }
                });
            }
        });

        // Listen for editor changes
        if (window.editorEn) {
            window.editorEn.quill.on('text-change', () => {
                if (this.isPreviewOpen) {
                    this.debounceUpdate();
                }
            });
        }

        if (window.editorAr) {
            window.editorAr.quill.on('text-change', () => {
                if (this.isPreviewOpen) {
                    this.debounceUpdate();
                }
            });
        }
    }

    debounceUpdate() {
        clearTimeout(this.updateTimeout);
        this.updateTimeout = setTimeout(() => {
            this.updatePreview();
        }, 500);
    }

    togglePreview() {
        if (this.isPreviewOpen) {
            this.previewModal.hide();
            this.isPreviewOpen = false;
        } else {
            this.previewModal.show();
            this.isPreviewOpen = true;
            this.updatePreview();
        }
    }

    switchLanguage(lang) {
        this.currentLanguage = lang;
        this.updatePreview();
        
        // Update button states
        document.querySelectorAll('#livePreviewModal .btn-group button').forEach(btn => {
            btn.classList.remove('active');
        });
        event.target.classList.add('active');
    }

    updatePreview() {
        const lang = this.currentLanguage;
        
        // Get form data
        const data = this.getFormData(lang);
        
        // Update preview content
        this.updatePreviewContent(data, lang);
        this.updateSocialPreviews(data, lang);
        this.updateSearchPreview(data, lang);
        this.updateAnalysis(data);
    }

    getFormData(lang) {
        const titleField = document.getElementById(`title_${lang}`);
        const excerptField = document.getElementById(`excerpt_${lang}`);
        const contentField = document.getElementById(`content_${lang}`);
        const tagsField = document.getElementById('tags');
        
        // Get content from editor if available
        let content = '';
        if (lang === 'en' && window.editorEn) {
            content = window.editorEn.getHTML();
        } else if (lang === 'ar' && window.editorAr) {
            content = window.editorAr.getHTML();
        } else if (contentField) {
            content = contentField.value;
        }

        return {
            title: titleField ? titleField.value : '',
            excerpt: excerptField ? excerptField.value : '',
            content: content,
            tags: tagsField ? tagsField.value : '',
            seoTitle: document.getElementById(`seo_title_${lang}`)?.value || '',
            seoDescription: document.getElementById(`seo_description_${lang}`)?.value || '',
            ogTitle: document.getElementById(`og_title_${lang}`)?.value || '',
            ogDescription: document.getElementById(`og_description_${lang}`)?.value || '',
            twitterTitle: document.getElementById(`twitter_title_${lang}`)?.value || '',
            twitterDescription: document.getElementById(`twitter_description_${lang}`)?.value || ''
        };
    }

    updatePreviewContent(data, lang) {
        const previewContent = document.getElementById('preview-content');
        if (lang === 'ar') {
            previewContent.style.direction = 'rtl';
            previewContent.style.textAlign = 'right';
        } else {
            previewContent.style.direction = 'ltr';
            previewContent.style.textAlign = 'left';
        }

        // Update title
        document.getElementById('preview-title').textContent = data.title || 'Article Title';
        
        // Update excerpt
        document.getElementById('preview-excerpt').textContent = data.excerpt || 'Article excerpt will appear here...';
        
        // Update content
        document.getElementById('preview-content-body').innerHTML = data.content || 'Article content will appear here...';
        
        // Update tags
        const tagsContainer = document.getElementById('preview-tags');
        if (data.tags) {
            const tags = data.tags.split(',').map(tag => tag.trim()).filter(tag => tag);
            tagsContainer.innerHTML = tags.map(tag => 
                `<span class="badge bg-secondary me-2">${tag}</span>`
            ).join('');
        } else {
            tagsContainer.innerHTML = '';
        }
    }

    updateSocialPreviews(data, lang) {
        // Facebook preview
        document.getElementById('preview-fb-title').textContent = 
            data.ogTitle || data.title || 'Article Title';
        document.getElementById('preview-fb-desc').textContent = 
            data.ogDescription || data.excerpt || 'Description';

        // Twitter preview
        document.getElementById('preview-twitter-title').textContent = 
            data.twitterTitle || data.title || 'Article Title';
        document.getElementById('preview-twitter-desc').textContent = 
            data.twitterDescription || data.excerpt || 'Description';
    }

    updateSearchPreview(data, lang) {
        document.getElementById('preview-search-title').textContent = 
            data.seoTitle || data.title || 'Article Title';
        document.getElementById('preview-search-desc').textContent = 
            data.seoDescription || data.excerpt || 'Meta description appears here...';
    }

    updateAnalysis(data) {
        // Word count
        const wordCount = this.getWordCount(data.content);
        document.getElementById('preview-word-count').textContent = wordCount;
        
        // Reading time
        const readingTime = Math.ceil(wordCount / 200);
        document.getElementById('preview-reading-time-val').textContent = readingTime;
        document.getElementById('preview-reading-time').textContent = `${readingTime} min read`;
        
        // SEO Score (simplified)
        const seoScore = this.calculateSimpleSEOScore(data);
        document.getElementById('preview-seo-score').textContent = seoScore;
    }

    getWordCount(content) {
        const text = content.replace(/<[^>]*>/g, '').trim();
        return text.split(/\s+/).filter(word => word.length > 0).length;
    }

    calculateSimpleSEOScore(data) {
        let score = 0;
        
        if (data.title && data.title.length >= 30 && data.title.length <= 60) score += 25;
        if (data.seoDescription && data.seoDescription.length >= 120 && data.seoDescription.length <= 160) score += 25;
        if (data.content && this.getWordCount(data.content) >= 300) score += 25;
        if (data.excerpt && data.excerpt.length > 0) score += 25;
        
        return score;
    }

    openInNewTab() {
        // Create a temporary preview page
        const previewData = this.getFormData(this.currentLanguage);
        const previewHTML = this.generatePreviewHTML(previewData, this.currentLanguage);
        
        const newWindow = window.open('', '_blank');
        newWindow.document.write(previewHTML);
        newWindow.document.close();
    }

    generatePreviewHTML(data, lang) {
        return `
            <!DOCTYPE html>
            <html lang="${lang}" dir="${lang === 'ar' ? 'rtl' : 'ltr'}">
            <head>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>${data.title || 'Article Preview'}</title>
                <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                <style>
                    body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
                    .article-content { line-height: 1.8; }
                    .article-content h1, .article-content h2, .article-content h3 { margin-top: 2rem; margin-bottom: 1rem; }
                    .preview-badge { position: fixed; top: 20px; right: 20px; z-index: 1000; }
                </style>
            </head>
            <body>
                <div class="preview-badge">
                    <span class="badge bg-warning text-dark">PREVIEW MODE</span>
                </div>
                <div class="container my-5">
                    <article class="mx-auto" style="max-width: 800px;">
                        <div class="mb-4">
                            <span class="badge bg-primary">News</span>
                            <span class="text-muted ms-2">${new Date().toLocaleDateString()}</span>
                        </div>
                        <h1 class="mb-4">${data.title || 'Article Title'}</h1>
                        <div class="lead mb-4">${data.excerpt || ''}</div>
                        <div class="article-content">
                            ${data.content || 'Article content will appear here...'}
                        </div>
                        ${data.tags ? `
                            <div class="mt-5">
                                <h6>Tags:</h6>
                                ${data.tags.split(',').map(tag => `<span class="badge bg-secondary me-2">${tag.trim()}</span>`).join('')}
                            </div>
                        ` : ''}
                    </article>
                </div>
            </body>
            </html>
        `;
    }
}

// Initialize live preview
window.livePreview = new LivePreview();
