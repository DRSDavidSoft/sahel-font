# Migration Guide: Switching to Enhanced Sahel Variable Font

This guide helps you migrate from the old Sahel font setup (multiple static files) to the new enhanced Sahel Variable Font.

## Why Migrate?

### Before (Old Setup)
- 🔴 **42+ separate font files** for different variants
- 🔴 Required switching between font families for Farsi digits
- 🔴 Limited to 5 fixed weights
- 🔴 Larger total download size
- 🔴 Complex CSS with multiple @font-face rules

### After (New Variable Font)
- ✅ **1 file** (Sahel-VF.woff2) for all variants
- ✅ CSS feature toggle for Farsi digits
- ✅ Any weight from 400-900
- ✅ 51.8 KB total download
- ✅ Simple, modern CSS

## Migration Steps

### Step 1: Replace Font Files

**Old structure:**
```
fonts/
├── Sahel.woff2
├── Sahel-Bold.woff2
├── Sahel-Light.woff2
├── Farsi-Digits/
│   ├── Sahel-FD.woff2
│   └── Sahel-Bold-FD.woff2
└── Without-Latin/
    └── ...
```

**New structure:**
```
fonts/
└── Sahel-VF.woff2  ← Just one file!
```

### Step 2: Update CSS

#### Old CSS
```css
/* Regular Sahel */
@font-face {
  font-family: 'Sahel';
  src: url('fonts/Sahel.woff2');
  font-weight: normal;
}

@font-face {
  font-family: 'Sahel';
  src: url('fonts/Sahel-Bold.woff2');
  font-weight: bold;
}

/* Farsi Digits version */
@font-face {
  font-family: 'SahelF';
  src: url('fonts/Farsi-Digits/Sahel-FD.woff2');
  font-weight: normal;
}

/* Usage */
body {
  font-family: 'Sahel', sans-serif;
}

.farsi-numbers {
  font-family: 'SahelF', sans-serif;  /* Different font family! */
}
```

#### New CSS
```css
/* Single variable font */
@font-face {
  font-family: 'Sahel VF';
  src: url('fonts/Sahel-VF.woff2') format('woff2-variations');
  font-weight: 400 900;  /* Supports all weights in this range */
  font-display: swap;
}

/* Usage */
body {
  font-family: 'Sahel VF', sans-serif;
  font-weight: 400;  /* Can be any value from 400-900 */
}

.farsi-numbers {
  font-family: 'Sahel VF', sans-serif;  /* Same font family! */
  font-feature-settings: "ss01" 1;  /* Just enable the feature */
}
```

### Step 3: Update HTML (Optional Performance Boost)

Add preloading for better performance:

```html
<head>
  <link rel="preload" 
        href="fonts/Sahel-VF.woff2" 
        as="font" 
        type="font/woff2" 
        crossorigin>
</head>
```

## Common Migration Scenarios

### Scenario 1: Basic Persian Text

**Before:**
```css
.persian-text {
  font-family: 'Sahel', sans-serif;
  font-weight: normal;
}

.persian-text-bold {
  font-family: 'Sahel', sans-serif;
  font-weight: bold;
}
```

**After:**
```css
.persian-text {
  font-family: 'Sahel VF', sans-serif;
  font-weight: 400;
}

.persian-text-bold {
  font-family: 'Sahel VF', sans-serif;
  font-weight: 700;
}
```

### Scenario 2: Farsi Digits

**Before:**
```css
.date-display {
  font-family: 'SahelF', sans-serif;  /* Separate font! */
}
```

**After:**
```css
.date-display {
  font-family: 'Sahel VF', sans-serif;
  font-feature-settings: "ss01" 1;  /* Enable Farsi digits */
}
```

### Scenario 3: Mixed Content (Some Western, Some Farsi)

**Before:**
```html
<!-- Required different font families -->
<p class="western-numbers">Price: 1000</p>  <!-- font-family: Sahel -->
<p class="farsi-numbers">Date: 1403/09/12</p>  <!-- font-family: SahelF -->
```

```css
.western-numbers { font-family: 'Sahel'; }
.farsi-numbers { font-family: 'SahelF'; }
```

**After:**
```html
<!-- Same font family, just toggle feature -->
<p class="western-numbers">Price: 1000</p>
<p class="farsi-numbers">Date: 1403/09/12</p>
```

```css
.western-numbers {
  font-family: 'Sahel VF', sans-serif;
  /* ss01 disabled by default */
}

.farsi-numbers {
  font-family: 'Sahel VF', sans-serif;
  font-feature-settings: "ss01" 1;
}
```

### Scenario 4: Weight Variations

**Before (Limited to 5 weights):**
```css
.light { font-weight: 300; }    /* Sahel-Light.woff2 */
.regular { font-weight: 400; }  /* Sahel.woff2 */
.semibold { font-weight: 600; } /* Sahel-SemiBold.woff2 */
.bold { font-weight: 700; }     /* Sahel-Bold.woff2 */
.black { font-weight: 900; }    /* Sahel-Black.woff2 */
```

**After (Any weight 400-900):**
```css
.light { font-weight: 400; }     /* Works */
.regular { font-weight: 450; }   /* Works! */
.medium { font-weight: 550; }    /* Works! */
.semibold { font-weight: 600; }  /* Works */
.bold { font-weight: 750; }      /* Works! */
.black { font-weight: 900; }     /* Works */

/* Even animated weights! */
@keyframes pulse {
  from { font-weight: 400; }
  to { font-weight: 700; }
}
```

## Advanced Features

### Responsive Weight

Take advantage of variable font for responsive design:

```css
/* Lighter on mobile for readability */
@media (max-width: 767px) {
  body {
    font-weight: 350;
  }
}

/* Normal on tablet */
@media (min-width: 768px) and (max-width: 1023px) {
  body {
    font-weight: 400;
  }
}

/* Slightly bolder on desktop */
@media (min-width: 1024px) {
  body {
    font-weight: 450;
  }
}
```

### Dark Mode Optimization

```css
/* Lighter weight in dark mode for better readability */
@media (prefers-color-scheme: dark) {
  body {
    font-weight: 375;
  }
  
  h1, h2, h3 {
    font-weight: 650;
  }
}
```

## Backward Compatibility

If you need to support very old browsers:

```css
/* Fallback for browsers without variable font support */
@supports not (font-variation-settings: normal) {
  /* Load static fonts as fallback */
  @font-face {
    font-family: 'Sahel';
    src: url('fonts/legacy/Sahel.woff2');
    font-weight: 400;
  }
  
  body {
    font-family: 'Sahel', sans-serif;
  }
}

/* Modern browsers with variable font support */
@supports (font-variation-settings: normal) {
  @font-face {
    font-family: 'Sahel VF';
    src: url('fonts/Sahel-VF.woff2') format('woff2-variations');
    font-weight: 400 900;
  }
  
  body {
    font-family: 'Sahel VF', sans-serif;
  }
}
```

## Testing Checklist

After migration, test:

- [ ] All text renders correctly in Persian
- [ ] Latin characters display properly (if using mixed content)
- [ ] Farsi digits work with `font-feature-settings: "ss01" 1`
- [ ] Western digits work by default
- [ ] Different font weights render as expected
- [ ] No FOUT (Flash of Unstyled Text) on page load
- [ ] Font loads efficiently (check Network tab)
- [ ] Mobile devices render correctly

## Troubleshooting

### Issue: Farsi digits not switching

**Solution:** Make sure you're using the correct feature syntax:
```css
/* Correct */
font-feature-settings: "ss01" 1;

/* Wrong */
font-feature-settings: "ss01" true;  /* Must be 1 or 0 */
font-feature-settings: ss01 1;       /* Must be quoted */
```

### Issue: Font not loading

**Check:**
1. File path is correct
2. CORS headers allow font loading (if from different domain)
3. Browser supports variable fonts (97%+ do)
4. File is not corrupted

### Issue: Weights look wrong

**Solution:** Variable font weight range is 400-900, not 100-900. Update your CSS:
```css
/* Wrong */
font-weight: 300;  /* Outside range */

/* Correct */
font-weight: 400;  /* Minimum weight */
```

## Performance Comparison

### Old Setup (Loading Multiple Files)
```
Sahel.woff2:           ~22 KB
Sahel-Bold.woff2:      ~23 KB
Sahel-FD.woff2:        ~22 KB
Sahel-Bold-FD.woff2:   ~23 KB
Total:                 ~90 KB
```

### New Setup (Single File)
```
Sahel-VF.woff2:        51.8 KB
Total:                 51.8 KB

Savings:               ~38 KB (42% smaller!)
```

Plus:
- ✅ Fewer HTTP requests
- ✅ Better caching
- ✅ Faster page load
- ✅ Smoother animations

## Getting Help

- 📖 [Complete CSS Examples](../dist/sahel-vf-usage.css)
- 🧪 [Interactive Test Page](../dist/test-sahel-vf.html)
- 📊 [Technical Details](missing-glyphs.md)
- 💬 [GitHub Issues](https://github.com/DRSDavidSoft/sahel-font/issues)

## Summary

The migration to Sahel Variable Font brings:
- **Simpler code**: One font file, one @font-face rule
- **Better performance**: 42% smaller download
- **More flexibility**: Any weight 400-900
- **Modern features**: CSS feature toggles instead of font switching
- **Future-proof**: Variable fonts are the web standard

Start migrating today for a better, faster website! 🚀
