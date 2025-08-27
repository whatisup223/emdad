/**
 * Advanced SEO Analyzer
 * Real-time SEO analysis and recommendations
 */

class SEOAnalyzer {
    constructor() {
        this.rules = {
            wordCount: { min: 300, max: 2000, weight: 20 },
            titleLength: { min: 30, max: 60, weight: 15 },
            descriptionLength: { min: 120, max: 160, weight: 15 },
            keywordDensity: { min: 1, max: 3, weight: 20 },
            headingStructure: { weight: 15 },
            keywordInTitle: { weight: 10 },
            keywordInHeadings: { weight: 5 }
        };
        
        this.suggestions = [];
        this.score = 0;
    }

    analyzeContent(content, focusKeyword, title, description) {
        this.suggestions = [];
        this.score = 0;
        
        const analysis = {
            wordCount: this.getWordCount(content),
            readingTime: this.calculateReadingTime(content),
            headings: this.extractHeadings(content),
            keywordDensity: this.calculateKeywordDensity(content, focusKeyword),
            titleAnalysis: this.analyzeTitle(title, focusKeyword),
            descriptionAnalysis: this.analyzeDescription(description, focusKeyword),
            readabilityScore: this.calculateReadability(content)
        };

        // Analyze each aspect
        this.analyzeWordCount(analysis.wordCount);
        this.analyzeTitle(title, focusKeyword);
        this.analyzeDescription(description, focusKeyword);
        this.analyzeKeywordUsage(content, focusKeyword);
        this.analyzeHeadingStructure(analysis.headings, focusKeyword);
        this.analyzeReadability(analysis.readabilityScore);

        return {
            score: Math.min(this.score, 100),
            suggestions: this.suggestions,
            analysis: analysis
        };
    }

    getWordCount(content) {
        // Remove HTML tags and count words
        const text = content.replace(/<[^>]*>/g, '').trim();
        return text.split(/\s+/).filter(word => word.length > 0).length;
    }

    calculateReadingTime(content) {
        const wordCount = this.getWordCount(content);
        return Math.ceil(wordCount / 200); // Average 200 words per minute
    }

    extractHeadings(content) {
        const headings = [];
        const headingRegex = /<h([1-6])[^>]*>(.*?)<\/h[1-6]>/gi;
        let match;

        while ((match = headingRegex.exec(content)) !== null) {
            headings.push({
                level: parseInt(match[1]),
                text: match[2].replace(/<[^>]*>/g, '').trim()
            });
        }

        return headings;
    }

    calculateKeywordDensity(content, keyword) {
        if (!keyword) return 0;
        
        const text = content.replace(/<[^>]*>/g, '').toLowerCase();
        const words = text.split(/\s+/);
        const keywordCount = words.filter(word => 
            word.includes(keyword.toLowerCase())
        ).length;
        
        return words.length > 0 ? (keywordCount / words.length) * 100 : 0;
    }

    analyzeWordCount(wordCount) {
        const rule = this.rules.wordCount;
        
        if (wordCount >= rule.min && wordCount <= rule.max) {
            this.score += rule.weight;
        } else if (wordCount < rule.min) {
            this.suggestions.push({
                type: 'warning',
                message: `Content is too short (${wordCount} words). Aim for at least ${rule.min} words for better SEO.`,
                priority: 'high'
            });
        } else {
            this.suggestions.push({
                type: 'info',
                message: `Content is quite long (${wordCount} words). Consider breaking it into multiple articles or sections.`,
                priority: 'medium'
            });
            this.score += rule.weight * 0.7; // Partial credit
        }
    }

    analyzeTitle(title, focusKeyword) {
        if (!title) {
            this.suggestions.push({
                type: 'error',
                message: 'Title is required for SEO.',
                priority: 'high'
            });
            return;
        }

        const titleLength = title.length;
        const rule = this.rules.titleLength;

        if (titleLength >= rule.min && titleLength <= rule.max) {
            this.score += rule.weight;
        } else if (titleLength < rule.min) {
            this.suggestions.push({
                type: 'warning',
                message: `Title is too short (${titleLength} characters). Aim for ${rule.min}-${rule.max} characters.`,
                priority: 'high'
            });
        } else {
            this.suggestions.push({
                type: 'warning',
                message: `Title is too long (${titleLength} characters). Keep it under ${rule.max} characters.`,
                priority: 'high'
            });
        }

        // Check if focus keyword is in title
        if (focusKeyword && title.toLowerCase().includes(focusKeyword.toLowerCase())) {
            this.score += this.rules.keywordInTitle.weight;
        } else if (focusKeyword) {
            this.suggestions.push({
                type: 'warning',
                message: 'Include your focus keyword in the title for better SEO.',
                priority: 'high'
            });
        }
    }

    analyzeDescription(description, focusKeyword) {
        if (!description) {
            this.suggestions.push({
                type: 'warning',
                message: 'Meta description is missing. Add one for better search results.',
                priority: 'high'
            });
            return;
        }

        const descLength = description.length;
        const rule = this.rules.descriptionLength;

        if (descLength >= rule.min && descLength <= rule.max) {
            this.score += rule.weight;
        } else if (descLength < rule.min) {
            this.suggestions.push({
                type: 'warning',
                message: `Meta description is too short (${descLength} characters). Aim for ${rule.min}-${rule.max} characters.`,
                priority: 'medium'
            });
        } else {
            this.suggestions.push({
                type: 'warning',
                message: `Meta description is too long (${descLength} characters). Keep it under ${rule.max} characters.`,
                priority: 'medium'
            });
        }

        // Check if focus keyword is in description
        if (focusKeyword && description.toLowerCase().includes(focusKeyword.toLowerCase())) {
            this.score += 5; // Bonus points
        } else if (focusKeyword) {
            this.suggestions.push({
                type: 'info',
                message: 'Consider including your focus keyword in the meta description.',
                priority: 'medium'
            });
        }
    }

    analyzeKeywordUsage(content, focusKeyword) {
        if (!focusKeyword) {
            this.suggestions.push({
                type: 'info',
                message: 'Set a focus keyword to get keyword-specific SEO recommendations.',
                priority: 'medium'
            });
            return;
        }

        const density = this.calculateKeywordDensity(content, focusKeyword);
        const rule = this.rules.keywordDensity;

        if (density >= rule.min && density <= rule.max) {
            this.score += rule.weight;
        } else if (density < rule.min) {
            this.suggestions.push({
                type: 'warning',
                message: `Keyword density is too low (${density.toFixed(2)}%). Use your focus keyword more naturally in the content.`,
                priority: 'medium'
            });
        } else {
            this.suggestions.push({
                type: 'warning',
                message: `Keyword density is too high (${density.toFixed(2)}%). Avoid keyword stuffing.`,
                priority: 'high'
            });
        }
    }

    analyzeHeadingStructure(headings, focusKeyword) {
        if (headings.length === 0) {
            this.suggestions.push({
                type: 'warning',
                message: 'Add headings (H1, H2, H3) to improve content structure and SEO.',
                priority: 'high'
            });
            return;
        }

        // Check for H1
        const hasH1 = headings.some(h => h.level === 1);
        if (hasH1) {
            this.score += 10;
        } else {
            this.suggestions.push({
                type: 'warning',
                message: 'Add an H1 heading for better SEO structure.',
                priority: 'high'
            });
        }

        // Check heading hierarchy
        let previousLevel = 0;
        let hierarchyIssues = 0;
        
        headings.forEach(heading => {
            if (heading.level > previousLevel + 1) {
                hierarchyIssues++;
            }
            previousLevel = heading.level;
        });

        if (hierarchyIssues === 0) {
            this.score += 5;
        } else {
            this.suggestions.push({
                type: 'info',
                message: 'Improve heading hierarchy. Avoid skipping heading levels (e.g., H1 to H3).',
                priority: 'low'
            });
        }

        // Check if focus keyword is in headings
        if (focusKeyword) {
            const keywordInHeadings = headings.some(h => 
                h.text.toLowerCase().includes(focusKeyword.toLowerCase())
            );
            
            if (keywordInHeadings) {
                this.score += this.rules.keywordInHeadings.weight;
            } else {
                this.suggestions.push({
                    type: 'info',
                    message: 'Include your focus keyword in at least one heading.',
                    priority: 'medium'
                });
            }
        }
    }

    calculateReadability(content) {
        // Simplified readability calculation
        const text = content.replace(/<[^>]*>/g, '');
        const sentences = text.split(/[.!?]+/).filter(s => s.trim().length > 0);
        const words = text.split(/\s+/).filter(w => w.length > 0);
        const syllables = this.countSyllables(text);

        if (sentences.length === 0 || words.length === 0) return 0;

        // Flesch Reading Ease approximation
        const avgWordsPerSentence = words.length / sentences.length;
        const avgSyllablesPerWord = syllables / words.length;
        
        const score = 206.835 - (1.015 * avgWordsPerSentence) - (84.6 * avgSyllablesPerWord);
        return Math.max(0, Math.min(100, score));
    }

    countSyllables(text) {
        // Simple syllable counting
        return text.toLowerCase()
            .replace(/[^a-z]/g, '')
            .replace(/[aeiou]{2,}/g, 'a')
            .replace(/[^aeiou]/g, '')
            .length || 1;
    }

    analyzeReadability(score) {
        if (score >= 60) {
            this.score += 5;
        } else if (score >= 30) {
            this.suggestions.push({
                type: 'info',
                message: 'Content readability could be improved. Use shorter sentences and simpler words.',
                priority: 'low'
            });
        } else {
            this.suggestions.push({
                type: 'warning',
                message: 'Content is difficult to read. Consider simplifying language and sentence structure.',
                priority: 'medium'
            });
        }
    }

    generateSEOReport(analysis) {
        return {
            score: analysis.score,
            grade: this.getGrade(analysis.score),
            suggestions: analysis.suggestions,
            metrics: {
                wordCount: analysis.analysis.wordCount,
                readingTime: analysis.analysis.readingTime,
                headingCount: analysis.analysis.headings.length,
                keywordDensity: analysis.analysis.keywordDensity,
                readabilityScore: analysis.analysis.readabilityScore
            }
        };
    }

    getGrade(score) {
        if (score >= 90) return { grade: 'A+', color: '#4caf50', description: 'Excellent SEO' };
        if (score >= 80) return { grade: 'A', color: '#8bc34a', description: 'Very Good SEO' };
        if (score >= 70) return { grade: 'B', color: '#ffeb3b', description: 'Good SEO' };
        if (score >= 60) return { grade: 'C', color: '#ff9800', description: 'Fair SEO' };
        if (score >= 50) return { grade: 'D', color: '#ff5722', description: 'Poor SEO' };
        return { grade: 'F', color: '#f44336', description: 'Very Poor SEO' };
    }
}

// Export for use in other modules
window.SEOAnalyzer = SEOAnalyzer;
