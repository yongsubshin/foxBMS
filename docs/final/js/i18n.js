/**
 * i18n Engine - Vanilla JavaScript Internationalization System
 *
 * Features:
 * - Singleton pattern for global instance
 * - Promise-based async language file loading
 * - Observer pattern for language change events
 * - localStorage persistence with in-memory fallback
 * - Support for nested translation keys
 * - Parameter interpolation
 * - Graceful fallback handling
 * - Comprehensive error handling with logging
 * - Input validation
 *
 * AC-001: Language file loading with fallback on error
 * AC-002: Language switching without page refresh
 * AC-003: Language persistence in localStorage
 * AC-004: Cross-page language consistency
 * AC-005: Translation key completeness with fallback
 * SR-003: Prevent unnecessary reload on same language selection
 * UB-001-004: Error handling with graceful degradation
 * SR-001-003: State management
 */

class I18n {
    constructor() {
        this._currentLanguage = 'ko';
        this._translations = {};
        this._fallbackTranslations = {};
        this._listeners = {};
        this._options = {
            defaultLanguage: 'ko',
            supportedLanguages: ['ko', 'en', 'ja'],
            languageFilePath: '/locales/',
            detectBrowserLanguage: true,
            persistLanguage: true,
            fallbackLanguage: 'ko'
        };
        this._isInitialized = false;
        this._loadingPromises = {};
        this._debug = false;
    }

    /**
     * Initialize the i18n engine
     * UR-001: Support all 3 languages
     * UR-002: Persist in localStorage
     * ER-001: Instant UI update
     * ER-002: Load saved language on page load
     * ER-003: Auto-detect browser language
     */
    async init(options = {}) {
        if (this._isInitialized) {
            this._log('i18n is already initialized, skipping init');
            return;
        }

        // Validate and merge options
        if (typeof options !== 'object') {
            console.warn('i18n.init: options must be an object');
            return;
        }

        this._options = {
            ...this._options,
            ...options
        };

        // Validate supported languages
        if (!Array.isArray(this._options.supportedLanguages) || this._options.supportedLanguages.length === 0) {
            console.warn('i18n.init: supportedLanguages must be a non-empty array');
            return;
        }

        // Determine initial language
        let initialLanguage = this._options.defaultLanguage;

        // Validate default language is supported
        if (!this._options.supportedLanguages.includes(initialLanguage)) {
            this._log(`Default language '${initialLanguage}' not in supported languages, using first supported language`);
            initialLanguage = this._options.supportedLanguages[0];
        }

        // ER-002: Load saved language on page load
        if (this._options.persistLanguage) {
            const savedLanguage = this._getFromStorage('i18n_language');
            if (savedLanguage && this._options.supportedLanguages.includes(savedLanguage)) {
                initialLanguage = savedLanguage;
                this._log(`Restored language from storage: ${initialLanguage}`);
            }
        }

        // ER-003: Auto-detect browser language
        if (this._options.detectBrowserLanguage && !this._getFromStorage('i18n_language')) {
            const browserLang = this._detectBrowserLanguage();
            if (browserLang) {
                initialLanguage = browserLang;
                this._log(`Auto-detected browser language: ${initialLanguage}`);
            }
        }

        this._currentLanguage = initialLanguage;

        // Pre-load fallback language
        if (this._options.fallbackLanguage !== this._options.defaultLanguage) {
            await this._loadLanguage(this._options.fallbackLanguage, true);
        }

        // Load initial language
        await this._loadLanguage(this._currentLanguage);
        this._isInitialized = true;

        this._log(`i18n initialized with language: ${this._currentLanguage}`);
    }

    /**
     * Translate a key with optional parameter interpolation
     * AC-005: Translation key completeness with fallback
     * UB-001-004: Error handling with graceful degradation
     */
    t(key, params = {}) {
        if (!this._isInitialized) {
            this._log(`Warning: i18n not initialized, returning key: ${key}`);
            return key;
        }

        if (typeof key !== 'string' || !key) {
            console.warn('i18n.t: key must be a non-empty string');
            return '';
        }

        let translation = this._getNestedValue(this._translations, key);

        // UR-003: Fallback to fallback language on missing keys
        if (!translation && this._currentLanguage !== this._options.fallbackLanguage) {
            translation = this._getNestedValue(this._fallbackTranslations, key);
        }

        // If still not found, return the key itself
        if (!translation) {
            this._log(`Translation key not found: ${key}`);
            translation = key;
        }

        // Handle non-string translations
        if (typeof translation !== 'string') {
            this._log(`Translation for '${key}' is not a string`);
            return key;
        }

        // Parameter interpolation
        if (params && typeof params === 'object') {
            Object.keys(params).forEach(param => {
                const value = params[param];
                if (value !== undefined && value !== null) {
                    translation = translation.replace(
                        new RegExp(`\\{${param}\\}`, 'g'),
                        String(value)
                    );
                }
            });
        }

        return translation;
    }

    /**
     * Change the current language
     * ER-001: Instant UI update
     * SR-003: Prevent unnecessary reload on same language selection
     * AC-002: Language switching without page refresh
     */
    async changeLanguage(lang) {
        // Input validation
        if (typeof lang !== 'string' || !lang) {
            console.warn('i18n.changeLanguage: language must be a non-empty string');
            return;
        }

        // SR-003: Prevent unnecessary reload on same language
        if (lang === this._currentLanguage) {
            this._log(`Language is already '${lang}', skipping change`);
            return;
        }

        // Validate language is supported
        if (!this._options.supportedLanguages.includes(lang)) {
            console.warn(`Language '${lang}' is not supported. Supported languages: ${this._options.supportedLanguages.join(', ')}`);
            return;
        }

        const previousLanguage = this._currentLanguage;
        this._currentLanguage = lang;

        // Load language if not already loaded
        try {
            await this._loadLanguage(lang);
        } catch (error) {
            // Restore previous language on load failure
            this._currentLanguage = previousLanguage;
            console.error(`Failed to load language '${lang}', restored to '${previousLanguage}'`);
            return;
        }

        // AC-003: Language persistence in localStorage
        if (this._options.persistLanguage) {
            this._saveToStorage('i18n_language', lang);
        }

        // ER-001: Instant UI update - notify listeners
        this._notifyListeners('languageChanged', lang);
        this._log(`Language changed to: ${lang}`);
    }

    /**
     * Get the current language code
     */
    getCurrentLanguage() {
        return this._currentLanguage;
    }

    /**
     * Get array of supported languages
     * UR-001: Support all 3 languages
     */
    getSupportedLanguages() {
        return [...this._options.supportedLanguages];
    }

    /**
     * Register an event listener
     */
    on(event, callback) {
        if (typeof event !== 'string' || !event) {
            console.warn('i18n.on: event must be a non-empty string');
            return;
        }

        if (typeof callback !== 'function') {
            console.warn('i18n.on: callback must be a function');
            return;
        }

        if (!this._listeners[event]) {
            this._listeners[event] = [];
        }

        // Prevent duplicate listeners
        if (!this._listeners[event].includes(callback)) {
            this._listeners[event].push(callback);
            this._log(`Event listener registered for: ${event}`);
        }
    }

    /**
     * Remove an event listener
     */
    off(event, callback) {
        if (typeof event !== 'string' || !event) {
            console.warn('i18n.off: event must be a non-empty string');
            return;
        }

        if (!this._listeners[event]) {
            return;
        }

        const originalLength = this._listeners[event].length;
        this._listeners[event] = this._listeners[event].filter(
            cb => cb !== callback
        );

        if (this._listeners[event].length < originalLength) {
            this._log(`Event listener removed for: ${event}`);
        }
    }

    /**
     * Enable debug logging
     */
    setDebug(enabled = true) {
        this._debug = enabled;
    }

    /**
     * Private: Load language file
     * AC-001: Language file loading with fallback on error
     * AC-004: Cross-page language consistency
     */
    async _loadLanguage(lang, isFallback = false) {
        // Avoid loading the same language multiple times simultaneously
        const cacheKey = `${lang}_${isFallback ? 'fallback' : 'main'}`;
        if (this._loadingPromises[cacheKey]) {
            return this._loadingPromises[cacheKey];
        }

        this._loadingPromises[cacheKey] = (async () => {
            try {
                const filePath = `${this._options.languageFilePath}${lang}.json`;
                const response = await fetch(filePath);

                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: Failed to load language file`);
                }

                const data = await response.json();

                // Validate data is an object
                if (typeof data !== 'object' || data === null) {
                    throw new Error('Language file must contain a JSON object');
                }

                // Update appropriate translation store
                if (isFallback) {
                    this._fallbackTranslations = data;
                    this._log(`Fallback language '${lang}' loaded`);
                } else {
                    // Only update if we're still on this language
                    if (lang === this._currentLanguage) {
                        this._translations = data;
                        this._log(`Language '${lang}' loaded`);
                    }
                }
            } catch (error) {
                // AC-001: Graceful fallback on error
                const errorMsg = error.message || 'Unknown error';
                console.warn(`Failed to load language '${lang}': ${errorMsg}`);

                // Clear translations to force fallback behavior
                if (!isFallback) {
                    if (lang === this._currentLanguage) {
                        this._translations = {};
                    }
                }
            } finally {
                delete this._loadingPromises[cacheKey];
            }
        })();

        return this._loadingPromises[cacheKey];
    }

    /**
     * Private: Get nested value from object using dot notation
     */
    _getNestedValue(obj, path) {
        if (!obj || typeof obj !== 'object') {
            return undefined;
        }

        if (typeof path !== 'string') {
            return undefined;
        }

        const keys = path.split('.');
        let current = obj;

        for (const key of keys) {
            if (!key) continue; // Skip empty parts

            if (current && typeof current === 'object' && key in current) {
                current = current[key];
            } else {
                return undefined;
            }
        }

        return current;
    }

    /**
     * Private: Notify all listeners of an event
     * SR-001-003: State management
     */
    _notifyListeners(event, data) {
        if (!this._listeners[event] || !Array.isArray(this._listeners[event])) {
            return;
        }

        this._listeners[event].forEach(callback => {
            try {
                callback(data);
            } catch (error) {
                console.error(`Error in event listener for '${event}':`, error);
            }
        });
    }

    /**
     * Private: Detect browser language
     */
    _detectBrowserLanguage() {
        try {
            const browserLang = navigator.language || navigator.userLanguage;

            if (!browserLang || typeof browserLang !== 'string') {
                return null;
            }

            // Get language code (e.g., 'en' from 'en-US')
            const langCode = browserLang.split('-')[0].toLowerCase();

            // Return if it's in supported languages
            if (this._options.supportedLanguages.includes(langCode)) {
                return langCode;
            }

            return null;
        } catch (error) {
            this._log(`Error detecting browser language: ${error.message}`);
            return null;
        }
    }

    /**
     * Private: Save to localStorage with fallback
     * ER-002: Load saved language on page load
     */
    _saveToStorage(key, value) {
        try {
            if (typeof localStorage !== 'undefined' && localStorage !== null) {
                localStorage.setItem(key, value);
                this._log(`Saved to storage: ${key} = ${value}`);
            }
        } catch (error) {
            // Fallback if localStorage is unavailable (quota exceeded, private mode, etc.)
            this._log(`localStorage not available: ${error.message}`);
        }
    }

    /**
     * Private: Get from localStorage with fallback
     */
    _getFromStorage(key) {
        try {
            if (typeof localStorage !== 'undefined' && localStorage !== null) {
                return localStorage.getItem(key);
            }
        } catch (error) {
            // Fallback if localStorage is unavailable
            this._log(`localStorage not available: ${error.message}`);
        }

        return null;
    }

    /**
     * Private: Log debug message
     */
    _log(message) {
        if (this._debug) {
            console.log(`[i18n] ${message}`);
        }
    }
}

// Create singleton instance
window.i18n = {
    _instance: null,

    /**
     * Get or create the i18n instance
     */
    _getInstance() {
        if (!this._instance) {
            this._instance = new I18n();
        }
        return this._instance;
    },

    /**
     * Initialize i18n
     */
    init(options) {
        return this._getInstance().init(options);
    },

    /**
     * Translate a key
     */
    t(key, params) {
        return this._getInstance().t(key, params);
    },

    /**
     * Change language
     */
    changeLanguage(lang) {
        return this._getInstance().changeLanguage(lang);
    },

    /**
     * Get current language
     */
    getCurrentLanguage() {
        return this._getInstance().getCurrentLanguage();
    },

    /**
     * Get supported languages
     */
    getSupportedLanguages() {
        return this._getInstance().getSupportedLanguages();
    },

    /**
     * Register event listener
     */
    on(event, callback) {
        return this._getInstance().on(event, callback);
    },

    /**
     * Remove event listener
     */
    off(event, callback) {
        return this._getInstance().off(event, callback);
    },

    /**
     * Enable/disable debug logging
     */
    setDebug(enabled) {
        return this._getInstance().setDebug(enabled);
    }
};
