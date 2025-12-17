# PARVIS i18n Templates Skill

## Skill Identity

name: parvis-i18n-templates
version: 1.0.0
description: Self-contained i18n infrastructure templates for PARVIS documentation generation
category: documentation
languages: ko, en, ja

## Purpose

Provides complete internationalization (i18n) infrastructure templates for generating multilingual documentation portals. This skill contains:
- i18n.js JavaScript engine for runtime language switching
- Pre-translated locale files for Korean, English, and Japanese
- Ready-to-use templates that work out-of-the-box

## When to Use

Use this skill when:
- Generating multilingual HTML documentation with PARVIS
- Creating new documentation portals that need i18n support
- Building automotive-grade documentation with Korean, Japanese, and English support

## Asset Structure

```
parvis-i18n-templates/
├── SKILL.md                 # This file
├── templates/
│   └── i18n.js             # Complete i18n engine (JavaScript)
└── locales/
    ├── ko.json             # Korean translations
    ├── en.json             # English translations
    └── ja.json             # Japanese translations
```

## Integration Guide

### Loading i18n Engine

```
Read .claude/skills/parvis-i18n-templates/templates/i18n.js
Write to {output_path}/js/i18n.js
```

### Loading Locale Files

```
Read .claude/skills/parvis-i18n-templates/locales/ko.json
Write to {output_path}/locales/ko.json

Read .claude/skills/parvis-i18n-templates/locales/en.json
Write to {output_path}/locales/en.json

Read .claude/skills/parvis-i18n-templates/locales/ja.json
Write to {output_path}/locales/ja.json
```

### HTML Integration Pattern

Include in main portal (index.html):
```html
<script src="js/i18n.js"></script>
<script>
    await i18n.init({
        defaultLanguage: 'ko',
        supportedLanguages: ['ko', 'en', 'ja'],
        languageFilePath: 'locales/',
        detectBrowserLanguage: true,
        persistLanguage: true,
        fallbackLanguage: 'ko'
    });
</script>
```

Include in subpages (html/process/index.html, etc.):
```html
<script src="../../js/i18n.js"></script>
<script>
    await i18n.init({
        languageFilePath: '../../locales/',
        ...
    });
</script>
```

## i18n Engine Features

The i18n.js engine provides:
- Singleton pattern for global instance
- Promise-based async language file loading
- Observer pattern for language change events
- localStorage persistence with fallback
- Nested translation key support (e.g., "common.nav.home")
- Parameter interpolation (e.g., "{count} items")
- Graceful fallback handling
- Browser language auto-detection

## Locale Data Structure

All locale files follow the same key structure:

Top-level keys:
- common: Shared UI elements (title, navigation, badges)
- cards: Dashboard card content
- vModel: V-Model diagram labels
- sections: Documentation section titles
- footer: Footer content
- language: Language selector labels
- process: Process documentation page
- misraPage: MISRA compliance page
- metricsPage: Quality metrics page
- viewer: Document viewer page

## Extending Translations

To add new translation keys:
1. Add the key to all three locale files
2. Add data-i18n attribute to HTML element
3. Call translatePage() to apply

Example:
```json
// In locales/en.json
{
  "mySection": {
    "title": "My New Section",
    "description": "Section description"
  }
}
```

```html
<h2 data-i18n="mySection.title">My New Section</h2>
<p data-i18n="mySection.description">Section description</p>
```

## Compliance

This skill supports automotive documentation standards:
- ISO 26262:2018 documentation requirements
- ASPICE 3.1 work product formatting
- MISRA C:2012 compliance reporting

## Version History

Version 1.0.0 (2025-12-17):
- Initial release
- Complete i18n.js engine
- Korean, English, Japanese locale files
- Integration documentation
