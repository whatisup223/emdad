# Hero Section Dark Overlay Instructions

## 📋 Overview
Added a black transparent overlay to the hero section background with multiple opacity options and easy rollback capability.

## 🎨 Available Overlay Options

### 1. Light Overlay (20% opacity)
```html
<section class="hero-section dark-overlay-light position-relative overflow-hidden min-vh-100 d-flex align-items-center">
```

### 2. Medium Overlay (25% opacity) - **Currently Applied**
```html
<section class="hero-section dark-overlay-medium position-relative overflow-hidden min-vh-100 d-flex align-items-center">
```

### 3. Heavy Overlay (60% opacity)
```html
<section class="hero-section dark-overlay-heavy position-relative overflow-hidden min-vh-100 d-flex align-items-center">
```

### 4. No Dark Overlay (Original)
```html
<section class="hero-section position-relative overflow-hidden min-vh-100 d-flex align-items-center">
```

## 🔄 How to Change/Remove Overlay

### To Remove Dark Overlay Completely:
1. Open `templates/main/index.html`
2. Find line 16 (approximately)
3. Change from:
   ```html
   <section class="hero-section dark-overlay-medium position-relative overflow-hidden min-vh-100 d-flex align-items-center">
   ```
   To:
   ```html
   <section class="hero-section position-relative overflow-hidden min-vh-100 d-flex align-items-center">
   ```

### To Change Overlay Intensity:
Replace `dark-overlay-medium` with:
- `dark-overlay-light` (lighter)
- `dark-overlay-heavy` (darker)

## 📁 Files Modified

### 1. `static/css/style.css`
- Added CSS classes for different overlay intensities
- Lines 484-500 (approximately)

### 2. `templates/main/index.html`
- Applied `dark-overlay-medium` class to hero section
- Line 16 (approximately)

## 🎯 CSS Classes Added

```css
/* Black transparent overlay - can be toggled on/off */
.hero-section.dark-overlay::before {
    background: linear-gradient(135deg, rgba(0, 0, 0, 0.4), rgba(0, 0, 0, 0.3));
}

/* Alternative black overlay with different opacity levels */
.hero-section.dark-overlay-light::before {
    background: linear-gradient(135deg, rgba(0, 0, 0, 0.2), rgba(0, 0, 0, 0.15));
}

.hero-section.dark-overlay-medium::before {
    background: linear-gradient(135deg, rgba(0, 0, 0, 0.25), rgba(0, 0, 0, 0.2));
}

.hero-section.dark-overlay-heavy::before {
    background: linear-gradient(135deg, rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.5));
}
```

## ⚡ Quick Rollback Commands

### Complete Rollback (Git):
```bash
git checkout HEAD~1 -- templates/main/index.html static/css/style.css
```

### Manual Rollback:
1. Remove `dark-overlay-medium` from the hero section class
2. Optionally remove the CSS classes from lines 484-500 in style.css

## 🎨 Visual Effect
- Adds a subtle black gradient overlay over the hero background
- Improves text readability
- Maintains the original background image visibility
- Smooth gradient from darker to lighter opacity

## 📝 Notes
- The overlay uses CSS `::before` pseudo-element
- Z-index is properly managed to not interfere with content
- Responsive design is maintained
- Easy to customize opacity levels
