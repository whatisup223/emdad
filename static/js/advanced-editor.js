/**
 * Advanced Rich Text Editor with SEO Features
 * Using Quill.js with custom modules for SEO optimization
 */

class AdvancedEditor {
    constructor(selector, options = {}) {
        this.selector = selector;
        this.options = {
            theme: 'snow',
            modules: {
                toolbar: [
                    [{ 'header': [1, 2, 3, 4, 5, 6, false] }],
                    [{ 'font': [] }],
                    [{ 'size': ['small', false, 'large', 'huge'] }],
                    ['bold', 'italic', 'underline', 'strike'],
                    [{ 'color': [] }, { 'background': [] }],
                    [{ 'script': 'sub'}, { 'script': 'super' }],
                    [{ 'list': 'ordered'}, { 'list': 'bullet' }],
                    [{ 'indent': '-1'}, { 'indent': '+1' }],
                    [{ 'direction': 'rtl' }],
                    [{ 'align': [] }],
                    ['link', 'image', 'video'],
                    ['blockquote', 'code-block'],
                    ['clean'],
                    ['seo-analysis']
                ],
                imageResize: {
                    displaySize: true
                },
                imageDrop: true,
                seoAnalysis: true
            },
            placeholder: options.placeholder || 'Start writing your content...',
            ...options
        };
        
        this.quill = null;
        this.seoData = {
            wordCount: 0,
            readingTime: 0,
            headingStructure: [],
            keywordDensity: {},
            focusKeyword: '',
            seoScore: 0
        };
        
        this.init();
    }

    init() {
        // Register custom modules
        this.registerSEOModule();
        this.registerImageModule();
        
        // Initialize Quill
        this.quill = new Quill(this.selector, this.options);
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Initialize SEO panel
        this.initSEOPanel();
        
        // Setup auto-save
        this.setupAutoSave();
    }

    registerSEOModule() {
        const Inline = Quill.import('blots/inline');
        const Block = Quill.import('blots/block');
        
        // Custom SEO highlight blot
        class SEOHighlight extends Inline {
            static create(value) {
                let node = super.create();
                node.setAttribute('class', `seo-highlight seo-${value}`);
                return node;
            }
            
            static formats(node) {
                return node.getAttribute('class').replace('seo-highlight seo-', '');
            }
        }
        SEOHighlight.blotName = 'seo-highlight';
        SEOHighlight.tagName = 'span';
        
        Quill.register(SEOHighlight);
        
        // Register SEO toolbar button
        const toolbarOptions = Quill.import('modules/toolbar');
        toolbarOptions.DEFAULTS.handlers['seo-analysis'] = () => {
            this.toggleSEOPanel();
        };
    }

    registerImageModule() {
        // Enhanced image handling with SEO attributes
        const Image = Quill.import('formats/image');
        
        class SEOImage extends Image {
            static create(value) {
                let node = super.create(value);
                if (typeof value === 'object') {
                    node.setAttribute('alt', value.alt || '');
                    node.setAttribute('title', value.title || '');
                    node.setAttribute('loading', 'lazy');
                }
                return node;
            }
            
            static value(node) {
                return {
                    src: node.getAttribute('src'),
                    alt: node.getAttribute('alt'),
                    title: node.getAttribute('title')
                };
            }
        }
        
        Quill.register(SEOImage, true);
    }

    setupEventListeners() {
        // Content change listener for real-time SEO analysis
        this.quill.on('text-change', (delta, oldDelta, source) => {
            if (source === 'user') {
                this.debounce(() => {
                    this.analyzeSEO();
                    this.updateWordCount();
                    this.updateReadingTime();
                }, 500)();
            }
        });

        // Selection change for contextual SEO suggestions
        this.quill.on('selection-change', (range, oldRange, source) => {
            if (range) {
                this.updateSelectionSEO(range);
            }
        });
    }

    initSEOPanel() {
        const seoPanel = document.createElement('div');
        seoPanel.className = 'seo-analysis-panel';
        seoPanel.innerHTML = `
            <div class="seo-panel-header">
                <h4><i class="fas fa-search-plus"></i> SEO Analysis</h4>
                <button class="btn btn-sm btn-outline-secondary" onclick="this.parentElement.parentElement.style.display='none'">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            <div class="seo-panel-content">
                <div class="seo-score-circle">
                    <div class="score-value">0</div>
                    <div class="score-label">SEO Score</div>
                </div>
                
                <div class="seo-metrics">
                    <div class="metric">
                        <span class="metric-label">Word Count:</span>
                        <span class="metric-value" id="word-count">0</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Reading Time:</span>
                        <span class="metric-value" id="reading-time">0 min</span>
                    </div>
                    <div class="metric">
                        <span class="metric-label">Focus Keyword:</span>
                        <input type="text" id="focus-keyword" class="form-control form-control-sm" placeholder="Enter focus keyword">
                    </div>
                </div>
                
                <div class="seo-suggestions">
                    <h6>SEO Suggestions:</h6>
                    <ul id="seo-suggestions-list"></ul>
                </div>
                
                <div class="heading-structure">
                    <h6>Heading Structure:</h6>
                    <div id="heading-outline"></div>
                </div>
                
                <div class="keyword-density">
                    <h6>Keyword Density:</h6>
                    <div id="keyword-density-chart"></div>
                </div>
            </div>
        `;
        
        // Insert SEO panel after the editor
        const editorContainer = document.querySelector(this.selector).parentElement;
        editorContainer.appendChild(seoPanel);
        
        // Setup focus keyword listener
        document.getElementById('focus-keyword').addEventListener('input', (e) => {
            this.seoData.focusKeyword = e.target.value;
            this.analyzeSEO();
        });
    }

    analyzeSEO() {
        const content = this.quill.getText();
        const html = this.quill.root.innerHTML;
        
        // Update word count
        this.seoData.wordCount = content.trim().split(/\s+/).filter(word => word.length > 0).length;
        
        // Update reading time (average 200 words per minute)
        this.seoData.readingTime = Math.ceil(this.seoData.wordCount / 200);
        
        // Analyze heading structure
        this.analyzeHeadingStructure(html);
        
        // Calculate keyword density
        this.calculateKeywordDensity(content);
        
        // Calculate SEO score
        this.calculateSEOScore();
        
        // Update UI
        this.updateSEOUI();
    }

    analyzeHeadingStructure(html) {
        const headings = [];
        const headingRegex = /<h([1-6])[^>]*>(.*?)<\/h[1-6]>/gi;
        let match;
        
        while ((match = headingRegex.exec(html)) !== null) {
            headings.push({
                level: parseInt(match[1]),
                text: match[2].replace(/<[^>]*>/g, '').trim()
            });
        }
        
        this.seoData.headingStructure = headings;
    }

    calculateKeywordDensity(content) {
        const words = content.toLowerCase().split(/\s+/).filter(word => word.length > 2);
        const wordCount = {};
        
        words.forEach(word => {
            wordCount[word] = (wordCount[word] || 0) + 1;
        });
        
        // Calculate density as percentage
        const totalWords = words.length;
        this.seoData.keywordDensity = {};
        
        Object.keys(wordCount).forEach(word => {
            this.seoData.keywordDensity[word] = ((wordCount[word] / totalWords) * 100).toFixed(2);
        });
    }

    calculateSEOScore() {
        let score = 0;
        const suggestions = [];
        
        // Word count check (300-2000 words is optimal)
        if (this.seoData.wordCount >= 300 && this.seoData.wordCount <= 2000) {
            score += 20;
        } else if (this.seoData.wordCount < 300) {
            suggestions.push('Content is too short. Aim for at least 300 words.');
        } else {
            suggestions.push('Content might be too long. Consider breaking it into multiple articles.');
        }
        
        // Heading structure check
        if (this.seoData.headingStructure.length > 0) {
            score += 15;
            if (this.seoData.headingStructure.some(h => h.level === 1)) {
                score += 10;
            } else {
                suggestions.push('Add an H1 heading for better SEO.');
            }
        } else {
            suggestions.push('Add headings to improve content structure.');
        }
        
        // Focus keyword check
        if (this.seoData.focusKeyword) {
            const keyword = this.seoData.focusKeyword.toLowerCase();
            const content = this.quill.getText().toLowerCase();
            
            if (content.includes(keyword)) {
                score += 20;
                
                // Check keyword density (1-3% is optimal)
                const density = parseFloat(this.seoData.keywordDensity[keyword] || 0);
                if (density >= 1 && density <= 3) {
                    score += 15;
                } else if (density < 1) {
                    suggestions.push('Focus keyword density is too low. Use it more naturally in your content.');
                } else {
                    suggestions.push('Focus keyword density is too high. Avoid keyword stuffing.');
                }
                
                // Check if keyword is in headings
                if (this.seoData.headingStructure.some(h => h.text.toLowerCase().includes(keyword))) {
                    score += 10;
                } else {
                    suggestions.push('Include focus keyword in at least one heading.');
                }
            } else {
                suggestions.push('Focus keyword not found in content.');
            }
        } else {
            suggestions.push('Set a focus keyword for better SEO optimization.');
        }
        
        // Reading time check (2-10 minutes is optimal)
        if (this.seoData.readingTime >= 2 && this.seoData.readingTime <= 10) {
            score += 10;
        }
        
        this.seoData.seoScore = Math.min(score, 100);
        this.seoData.suggestions = suggestions;
    }

    updateSEOUI() {
        // Update score circle
        const scoreElement = document.querySelector('.score-value');
        if (scoreElement) {
            scoreElement.textContent = this.seoData.seoScore;
            scoreElement.parentElement.className = `seo-score-circle score-${this.getScoreClass(this.seoData.seoScore)}`;
        }
        
        // Update metrics
        document.getElementById('word-count').textContent = this.seoData.wordCount;
        document.getElementById('reading-time').textContent = `${this.seoData.readingTime} min`;
        
        // Update suggestions
        const suggestionsList = document.getElementById('seo-suggestions-list');
        if (suggestionsList) {
            suggestionsList.innerHTML = this.seoData.suggestions
                .map(suggestion => `<li class="suggestion-item">${suggestion}</li>`)
                .join('');
        }
        
        // Update heading outline
        const headingOutline = document.getElementById('heading-outline');
        if (headingOutline) {
            headingOutline.innerHTML = this.seoData.headingStructure
                .map(heading => `<div class="heading-item h${heading.level}">${'&nbsp;'.repeat((heading.level - 1) * 4)}H${heading.level}: ${heading.text}</div>`)
                .join('');
        }
        
        // Update keyword density chart
        this.updateKeywordDensityChart();
    }

    updateKeywordDensityChart() {
        const chartContainer = document.getElementById('keyword-density-chart');
        if (!chartContainer) return;
        
        const topKeywords = Object.entries(this.seoData.keywordDensity)
            .sort(([,a], [,b]) => b - a)
            .slice(0, 10);
        
        chartContainer.innerHTML = topKeywords
            .map(([word, density]) => `
                <div class="keyword-bar">
                    <span class="keyword-word">${word}</span>
                    <div class="keyword-bar-container">
                        <div class="keyword-bar-fill" style="width: ${Math.min(density * 10, 100)}%"></div>
                    </div>
                    <span class="keyword-density">${density}%</span>
                </div>
            `).join('');
    }

    getScoreClass(score) {
        if (score >= 80) return 'excellent';
        if (score >= 60) return 'good';
        if (score >= 40) return 'fair';
        return 'poor';
    }

    toggleSEOPanel() {
        const panel = document.querySelector('.seo-analysis-panel');
        if (panel) {
            panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        }
    }

    updateWordCount() {
        const wordCountElement = document.getElementById('word-count');
        if (wordCountElement) {
            wordCountElement.textContent = this.seoData.wordCount;
        }
    }

    updateReadingTime() {
        const readingTimeElement = document.getElementById('reading-time');
        if (readingTimeElement) {
            readingTimeElement.textContent = `${this.seoData.readingTime} min`;
        }
    }

    updateSelectionSEO(range) {
        // Provide contextual SEO suggestions based on selection
        const selectedText = this.quill.getText(range.index, range.length);
        if (selectedText.length > 0) {
            // Could add contextual suggestions here
        }
    }

    setupAutoSave() {
        let autoSaveTimer;
        this.quill.on('text-change', () => {
            clearTimeout(autoSaveTimer);
            autoSaveTimer = setTimeout(() => {
                this.autoSave();
            }, 30000); // Auto-save every 30 seconds
        });
    }

    autoSave() {
        // Implement auto-save functionality
        const content = this.quill.getContents();
        localStorage.setItem(`autosave_${this.selector}`, JSON.stringify(content));
        
        // Show auto-save indicator
        this.showAutoSaveIndicator();
    }

    showAutoSaveIndicator() {
        const indicator = document.createElement('div');
        indicator.className = 'auto-save-indicator';
        indicator.innerHTML = '<i class="fas fa-check"></i> Auto-saved';
        document.body.appendChild(indicator);
        
        setTimeout(() => {
            indicator.remove();
        }, 2000);
    }

    // Utility function for debouncing
    debounce(func, wait) {
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

    // Get content in different formats
    getHTML() {
        return this.quill.root.innerHTML;
    }

    getText() {
        return this.quill.getText();
    }

    getContents() {
        return this.quill.getContents();
    }

    setContents(contents) {
        this.quill.setContents(contents);
    }

    // SEO data getter
    getSEOData() {
        return this.seoData;
    }
}

// Export for use in other modules
window.AdvancedEditor = AdvancedEditor;
