// ==UserScript==
// @name         Meta Create Auto VIP ❤️‍🔥
// @namespace    https://viayoo.com/
// @version      8.8 (Final Clean Edition)
// @run-at       document-end
// @match        *://auth.meta.com/*
// @match        *://*.meta.com/*
// @connect      *
// @connect      delicate-leaf-b322.mdmonirmia269.workers.dev
// @grant        GM_xmlhttpRequest
// @grant        GM.xmlHttpRequest
// @grant        GM_setValue
// @grant        GM_getValue
// ==/UserScript==

(async function() {
    'use strict';

    if (window.top !== window.self) return;
    if (!window.location.hostname.includes('meta.com')) return;

    // 👉 আপনার সঠিক ক্লাউডফ্লেয়ার ওয়ার্কারের ভেরিফাই লিংক
    const SERVER_URL = "https://delicate-leaf-b322.mdmonirmia269.workers.dev/api/verify";
    const TOOL_STORAGE_KEY = "META_AUTO_VIP_KEY_FINAL";

    function getStoredKey() {
        try {
            if (typeof GM_getValue !== 'undefined') {
                var k = GM_getValue(TOOL_STORAGE_KEY);
                if (k) return k;
            }
        } catch(e) {}
        try {
            return localStorage.getItem(TOOL_STORAGE_KEY) || "";
        } catch(e) { return ""; }
    }

    function setStoredKey(k) {
        try {
            if (typeof GM_setValue !== 'undefined') {
                GM_setValue(TOOL_STORAGE_KEY, k);
            }
        } catch(e) {}
        try {
            if (k) localStorage.setItem(TOOL_STORAGE_KEY, k);
            else localStorage.removeItem(TOOL_STORAGE_KEY);
        } catch(e) {}
    }

    async function getDeviceID() {
        var p = [];
        try {
            var w = screen.width || 360;
            var h = screen.height || 640;
            p.push(Math.min(w, h) + 'x' + Math.max(w, h));
        } catch(e) { p.push('360x640'); }

        try { p.push(window.devicePixelRatio || 1); } catch(e) { p.push('1'); }
        try { p.push(screen.colorDepth || 24); } catch(e) { p.push('24'); }
        try { p.push(navigator.hardwareConcurrency || 4); } catch(e) { p.push('4'); }
        try { p.push(navigator.deviceMemory || '4'); } catch(e) { p.push('4'); }

        try {
            var canvas = document.createElement('canvas');
            var gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            if (gl) {
                var dbg = gl.getExtension('WEBGL_debug_renderer_info');
                var vendor = dbg ? gl.getParameter(dbg.UNMASKED_VENDOR_WEBGL) : '';
                var renderer = dbg ? gl.getParameter(dbg.UNMASKED_RENDERER_WEBGL) : '';
                p.push(vendor + '~' + renderer);
                p.push(gl.getParameter(gl.MAX_TEXTURE_SIZE) || 0);
            } else { p.push('no-webgl~0'); }
        } catch(e) { p.push('no-webgl~0'); }

        var rawString = p.join('|||');

        try {
            if (window.crypto && crypto.subtle) {
                var msgBuffer = new TextEncoder().encode(rawString);
                var hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);
                var hashArray = Array.from(new Uint8Array(hashBuffer));
                var hashHex = hashArray.map(b => b.toString(16).padStart(2, '0')).join('').toUpperCase();
                return 'DEV-' + hashHex.substring(0, 4) + '-' + hashHex.substring(4, 8) + '-' + hashHex.substring(8, 12);
            }
        } catch(e) {}

        var h1 = 5381, h2 = 52711;
        for (var i = 0; i < rawString.length; i++) {
            var ch = rawString.charCodeAt(i);
            h1 = ((h1 << 5) + h1) ^ ch;
            h2 = ((h2 << 5) + h2) ^ ch;
        }
        var finalHex = (Math.abs(h1).toString(16) + Math.abs(h2).toString(16)).toUpperCase().padEnd(12, '0');
        return 'DEV-' + finalHex.substring(0, 4) + '-' + finalHex.substring(4, 8) + '-' + finalHex.substring(8, 12);
    }

    let licenseKey = getStoredKey();
    if (!licenseKey) {
        licenseKey = prompt("🔑 Meta Account Tool লাইসেন্স কি দিন (শুধুমাত্র ১ম বার দিতে হবে):", "MONIR-VIP-2026");
        if (!licenseKey) return;
        licenseKey = licenseKey.trim();
        setStoredKey(licenseKey);
    }

    const deviceId = await getDeviceID();

    function sendAuth(url, data, callback) {
        var xhr = (typeof GM_xmlhttpRequest !== 'undefined') ? GM_xmlhttpRequest : 
                  ((typeof GM !== 'undefined' && GM.xmlHttpRequest) ? GM.xmlHttpRequest : null);
        if (xhr) {
            xhr({
                method: "POST", 
                url: url, 
                data: JSON.stringify(data),
                headers: { "Content-Type": "application/json" },
                timeout: 10000,
                onload: function(r) {
                    try { callback(null, JSON.parse(r.responseText)); } 
                    catch(e) { callback("সার্ভার রেসপন্স বুঝতে সমস্যা হয়েছে"); }
                },
                onerror: function() { directFetchFallback(); },
                ontimeout: function() { callback("সার্ভার টাইমআউট (নেটওয়ার্ক চেক করুন)"); }
            });
        } else {
            directFetchFallback();
        }

        function directFetchFallback() {
            fetch(url, { 
                method: 'POST', 
                headers: { 'Content-Type': 'application/json' }, 
                body: JSON.stringify(data) 
            })
            .then(r => r.json())
            .then(d => callback(null, d))
            .catch(e => callback("কানেকশন এরর (সার্ভার বা লিংক চেক করুন)"));
        }
    }

    sendAuth(SERVER_URL, { key: licenseKey, device: deviceId }, function(err, data) {
        if (err) { alert("⚠️ " + err); return; }

        if (data.success && data.payload) {
            var existingScript = document.querySelector('script[nonce]');
            var nonce = existingScript ? (existingScript.nonce || existingScript.getAttribute('nonce')) : '';
            var scriptEl = document.createElement('script');
            if (nonce) scriptEl.setAttribute('nonce', nonce);
            scriptEl.textContent = data.payload;
            (document.head || document.documentElement).appendChild(scriptEl);
        } else {
            if (data.action === "PURGE") {
                setStoredKey("");
            }
            alert(data.message || "লাইসেন্স ভেরিফিকেশন ব্যর্থ হয়েছে!");
        }
    });
})();
