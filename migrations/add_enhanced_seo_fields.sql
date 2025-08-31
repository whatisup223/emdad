-- Migration: Add Enhanced SEO Fields to News Table
-- Date: 2024-12-19
-- Description: Adds advanced SEO fields including Open Graph, Twitter Card, and enhanced metadata

-- Add Enhanced Keywords
ALTER TABLE news ADD COLUMN focus_keyword_en VARCHAR(100);
ALTER TABLE news ADD COLUMN focus_keyword_ar VARCHAR(100);

-- Update existing SEO fields to proper lengths
ALTER TABLE news ALTER COLUMN seo_title_en TYPE VARCHAR(70);
ALTER TABLE news ALTER COLUMN seo_title_ar TYPE VARCHAR(70);
ALTER TABLE news ALTER COLUMN seo_description_en TYPE VARCHAR(160);
ALTER TABLE news ALTER COLUMN seo_description_ar TYPE VARCHAR(160);

-- Add Open Graph fields
ALTER TABLE news ADD COLUMN og_title_en VARCHAR(95);
ALTER TABLE news ADD COLUMN og_title_ar VARCHAR(95);
ALTER TABLE news ADD COLUMN og_description_en VARCHAR(200);
ALTER TABLE news ADD COLUMN og_description_ar VARCHAR(200);
ALTER TABLE news ADD COLUMN og_image VARCHAR(255);

-- Add Twitter Card fields
ALTER TABLE news ADD COLUMN twitter_title_en VARCHAR(70);
ALTER TABLE news ADD COLUMN twitter_title_ar VARCHAR(70);
ALTER TABLE news ADD COLUMN twitter_description_en VARCHAR(200);
ALTER TABLE news ADD COLUMN twitter_description_ar VARCHAR(200);

-- Add Schema.org structured data
ALTER TABLE news ADD COLUMN article_type VARCHAR(50) DEFAULT 'Article';

-- Add content metadata
ALTER TABLE news ADD COLUMN estimated_reading_time INTEGER;
ALTER TABLE news ADD COLUMN content_difficulty VARCHAR(20) DEFAULT 'intermediate';

-- Update status field to include 'scheduled'
-- Note: This might need to be adjusted based on your database system
-- For PostgreSQL:
-- ALTER TABLE news DROP CONSTRAINT IF EXISTS news_status_check;
-- ALTER TABLE news ADD CONSTRAINT news_status_check CHECK (status IN ('draft', 'published', 'scheduled', 'archived'));

-- Add indexes for better performance
CREATE INDEX IF NOT EXISTS idx_news_focus_keyword_en ON news(focus_keyword_en);
CREATE INDEX IF NOT EXISTS idx_news_focus_keyword_ar ON news(focus_keyword_ar);
CREATE INDEX IF NOT EXISTS idx_news_article_type ON news(article_type);
CREATE INDEX IF NOT EXISTS idx_news_content_difficulty ON news(content_difficulty);
CREATE INDEX IF NOT EXISTS idx_news_estimated_reading_time ON news(estimated_reading_time);

-- Add comments for documentation
COMMENT ON COLUMN news.focus_keyword_en IS 'Primary SEO keyword for English content';
COMMENT ON COLUMN news.focus_keyword_ar IS 'Primary SEO keyword for Arabic content';
COMMENT ON COLUMN news.og_title_en IS 'Open Graph title for Facebook sharing (English)';
COMMENT ON COLUMN news.og_title_ar IS 'Open Graph title for Facebook sharing (Arabic)';
COMMENT ON COLUMN news.og_description_en IS 'Open Graph description for Facebook sharing (English)';
COMMENT ON COLUMN news.og_description_ar IS 'Open Graph description for Facebook sharing (Arabic)';
COMMENT ON COLUMN news.og_image IS 'Open Graph image for social media sharing';
COMMENT ON COLUMN news.twitter_title_en IS 'Twitter Card title (English)';
COMMENT ON COLUMN news.twitter_title_ar IS 'Twitter Card title (Arabic)';
COMMENT ON COLUMN news.twitter_description_en IS 'Twitter Card description (English)';
COMMENT ON COLUMN news.twitter_description_ar IS 'Twitter Card description (Arabic)';
COMMENT ON COLUMN news.article_type IS 'Schema.org article type for structured data';
COMMENT ON COLUMN news.estimated_reading_time IS 'Estimated reading time in minutes';
COMMENT ON COLUMN news.content_difficulty IS 'Content difficulty level (beginner, intermediate, advanced, expert)';

-- Optional: Update existing records with default values
UPDATE news SET 
    article_type = 'Article',
    content_difficulty = 'intermediate',
    estimated_reading_time = CASE 
        WHEN LENGTH(COALESCE(content_en, '')) > 0 THEN 
            GREATEST(1, ROUND(LENGTH(REGEXP_REPLACE(COALESCE(content_en, ''), '<[^>]*>', '', 'g')) / 1000.0))
        ELSE 1 
    END
WHERE article_type IS NULL OR content_difficulty IS NULL OR estimated_reading_time IS NULL;
