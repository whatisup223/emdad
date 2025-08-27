#!/usr/bin/env python3
"""Find untranslated text in templates"""

import re
import os

def find_untranslated_text(file_path):
    """Find English text that's not wrapped in _() function"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.split('\n')
    untranslated = []
    
    for i, line in enumerate(lines, 1):
        # Skip lines that are comments, imports, or already translated
        if (line.strip().startswith('<!--') or 
            line.strip().startswith('{%') or 
            line.strip().startswith('{{') or
            '_(' in line or
            not line.strip()):
            continue
        
        # Look for English text in HTML content
        # Find text between > and < that contains English words
        text_matches = re.findall(r'>([^<>]*[a-zA-Z][^<>]*)<', line)
        for match in text_matches:
            text = match.strip()
            if (text and 
                len(text) > 2 and 
                not text.startswith('{{') and 
                not text.startswith('{%') and
                not text.isdigit() and
                not text.startswith('fa-') and
                not text.startswith('btn') and
                not text.startswith('class') and
                not text.startswith('id') and
                not text.startswith('href') and
                not text.startswith('src') and
                not text.startswith('alt') and
                not text.startswith('data-') and
                not text.startswith('aria-') and
                not text.startswith('style') and
                not text.startswith('role') and
                not text.startswith('type') and
                not text.startswith('name') and
                not text.startswith('value') and
                not text.startswith('placeholder') and
                not text.startswith('title') and
                not text.startswith('content') and
                not text.startswith('property') and
                not text.startswith('rel') and
                not text.startswith('crossorigin') and
                not text.startswith('integrity') and
                not text.startswith('defer') and
                not text.startswith('async') and
                not text.startswith('loading') and
                not text.startswith('decoding') and
                not text.startswith('sizes') and
                not text.startswith('srcset') and
                not text.startswith('media') and
                not text.startswith('preload') and
                not text.startswith('prefetch') and
                not text.startswith('dns-prefetch') and
                not text.startswith('preconnect') and
                not text.startswith('modulepreload') and
                not text.startswith('prerender') and
                not text.startswith('manifest') and
                not text.startswith('icon') and
                not text.startswith('apple-touch-icon') and
                not text.startswith('mask-icon') and
                not text.startswith('theme-color') and
                not text.startswith('msapplication') and
                not text.startswith('application-name') and
                not text.startswith('msvalidate') and
                not text.startswith('google-site-verification') and
                not text.startswith('yandex-verification') and
                not text.startswith('bing-verification') and
                not text.startswith('alexa-verification') and
                not text.startswith('norton-safeweb-verification') and
                not text.startswith('p:domain_verify') and
                not text.startswith('fb:app_id') and
                not text.startswith('fb:admins') and
                not text.startswith('twitter:') and
                not text.startswith('og:') and
                not text.startswith('article:') and
                not text.startswith('book:') and
                not text.startswith('profile:') and
                not text.startswith('video:') and
                not text.startswith('music:') and
                not text.startswith('website') and
                not text.startswith('article') and
                not text.startswith('book') and
                not text.startswith('profile') and
                not text.startswith('video') and
                not text.startswith('music') and
                not text.startswith('summary') and
                not text.startswith('summary_large_image') and
                not text.startswith('app') and
                not text.startswith('player') and
                not text.startswith('photo') and
                not text.startswith('gallery') and
                not text.startswith('product') and
                not text.startswith('place') and
                not text.startswith('restaurant') and
                not text.startswith('business') and
                not text.startswith('contact') and
                not text.startswith('event') and
                not text.startswith('organization') and
                not text.startswith('person') and
                not text.startswith('review') and
                not text.startswith('recipe') and
                not text.startswith('software') and
                not text.startswith('game') and
                not text.startswith('movie') and
                not text.startswith('tv_show') and
                not text.startswith('book') and
                not text.startswith('music') and
                not text.startswith('video') and
                not text.startswith('image') and
                not text.startswith('audio') and
                not text.startswith('document') and
                not text.startswith('spreadsheet') and
                not text.startswith('presentation') and
                not text.startswith('form') and
                not text.startswith('drawing') and
                not text.startswith('map') and
                not text.startswith('folder') and
                not text.startswith('site') and
                not text.startswith('shortcut') and
                not text.startswith('unknown') and
                re.search(r'[a-zA-Z]', text)):
                untranslated.append((i, text))
        
        # Also check for text in attributes like placeholder, title, alt
        attr_matches = re.findall(r'(?:placeholder|title|alt)=["\']([^"\']*)["\']', line)
        for match in attr_matches:
            text = match.strip()
            if (text and 
                len(text) > 2 and 
                re.search(r'[a-zA-Z]', text) and
                not text.startswith('{{') and
                not text.startswith('fa-')):
                untranslated.append((i, f"[ATTR] {text}"))
    
    return untranslated

def main():
    """Main function"""
    file_path = 'templates/main/index.html'
    
    if not os.path.exists(file_path):
        print(f"File {file_path} not found!")
        return
    
    untranslated = find_untranslated_text(file_path)
    
    print(f"Found {len(untranslated)} potentially untranslated text strings in {file_path}:")
    print("=" * 80)
    
    for line_num, text in untranslated:
        print(f"Line {line_num:4d}: {text}")
    
    print("=" * 80)
    print(f"Total: {len(untranslated)} strings")

if __name__ == "__main__":
    main()
