import json
import os

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Tokyo & Kusatsu Onsen Romance | 5-Day Itinerary</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400;1,600&display=swap" rel="stylesheet">
  
  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
  
  <style>
    :root {
      --primary: #9b2c47;
      --primary-light: #fcecef;
      --primary-hover: #801f37;
      --accent-gold: #c6924b;
      --accent-gold-light: #fdf6ec;
      --accent-rose: #e07a7e;
      --bg-main: #fcfbfa;
      --bg-surface: #ffffff;
      --bg-subtle: #f6f5f3;
      --text-main: #242220;
      --text-muted: #6a6764;
      --border-color: #ede9e3;
      --shadow-sm: 0 2px 8px rgba(36, 34, 32, 0.04);
      --shadow-md: 0 8px 24px rgba(36, 34, 32, 0.08);
      --shadow-lg: 0 16px 40px rgba(36, 34, 32, 0.12);
      --radius-sm: 10px;
      --radius-md: 18px;
      --radius-lg: 26px;
      --font-display: 'Playfair Display', Georgia, serif;
      --font-body: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
    }

    body {
      font-family: var(--font-body);
      background-color: var(--bg-main);
      color: var(--text-main);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
    }

    /* Hero Header */
    .hero {
      position: relative;
      background: linear-gradient(135deg, #2b1d24 0%, #4a2133 45%, #6e273f 100%);
      color: #fff;
      padding: 50px 24px 40px;
      text-align: center;
      border-radius: 0 0 var(--radius-lg) var(--radius-lg);
      box-shadow: 0 12px 30px rgba(60, 20, 36, 0.25);
      overflow: hidden;
    }

    .hero::before {
      content: "";
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: radial-gradient(circle at 20% 30%, rgba(224, 122, 126, 0.25) 0%, transparent 60%),
                  radial-gradient(circle at 80% 70%, rgba(198, 146, 75, 0.25) 0%, transparent 50%);
      pointer-events: none;
    }

    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 16px;
      background: rgba(255, 255, 255, 0.15);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.25);
      border-radius: 50px;
      font-size: 0.82rem;
      font-weight: 600;
      letter-spacing: 0.06em;
      text-transform: uppercase;
      margin-bottom: 16px;
      color: #ffd8df;
    }

    .hero h1 {
      font-family: var(--font-display);
      font-size: clamp(2rem, 4.5vw, 3.2rem);
      font-weight: 700;
      line-height: 1.2;
      margin-bottom: 12px;
      color: #fff;
      letter-spacing: -0.02em;
    }

    .hero-subtitle {
      font-size: clamp(1rem, 2vw, 1.2rem);
      color: rgba(255, 255, 255, 0.88);
      max-width: 620px;
      margin: 0 auto 24px;
      font-weight: 400;
    }

    .hero-stats {
      display: flex;
      justify-content: center;
      gap: 18px;
      flex-wrap: wrap;
      margin-bottom: 24px;
    }

    .stat-pill {
      background: rgba(255, 255, 255, 0.12);
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.2);
      padding: 8px 18px;
      border-radius: 50px;
      font-size: 0.88rem;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .stat-pill strong {
      color: #ffd79e;
    }

    .hero-actions {
      display: flex;
      justify-content: center;
      gap: 12px;
      flex-wrap: wrap;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 10px 22px;
      border-radius: 50px;
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s ease;
      border: none;
    }

    .btn-gold {
      background: linear-gradient(135deg, #d49f57 0%, #b8813a 100%);
      color: #fff;
      box-shadow: 0 4px 14px rgba(184, 129, 58, 0.4);
    }
    .btn-gold:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 18px rgba(184, 129, 58, 0.5);
    }

    .btn-white-glass {
      background: rgba(255, 255, 255, 0.2);
      color: #fff;
      backdrop-filter: blur(8px);
      border: 1px solid rgba(255, 255, 255, 0.35);
    }
    .btn-white-glass:hover {
      background: rgba(255, 255, 255, 0.3);
      transform: translateY(-2px);
    }

    /* Main Container */
    .app-container {
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px 16px 80px;
    }

    /* Day Navigation Bar */
    .day-nav-wrapper {
      position: sticky;
      top: 12px;
      z-index: 100;
      margin-bottom: 24px;
    }

    .day-nav {
      display: flex;
      gap: 10px;
      background: rgba(255, 255, 255, 0.92);
      backdrop-filter: blur(16px);
      padding: 8px 12px;
      border-radius: 60px;
      box-shadow: var(--shadow-md);
      border: 1px solid var(--border-color);
      overflow-x: auto;
      scrollbar-width: none;
    }
    .day-nav::-webkit-scrollbar { display: none; }

    .day-tab {
      flex: 1;
      min-width: 110px;
      padding: 10px 16px;
      border-radius: 40px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      font-size: 0.88rem;
      font-weight: 600;
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
      transition: all 0.2s ease;
      white-space: nowrap;
    }

    .day-tab .tab-date {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.05em;
      opacity: 0.8;
    }

    .day-tab.active {
      background: var(--primary);
      color: #fff;
      box-shadow: 0 4px 12px rgba(155, 44, 71, 0.35);
    }

    .day-tab:hover:not(.active) {
      background: var(--bg-subtle);
      color: var(--text-main);
    }

    /* Split Layout */
    .itinerary-layout {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 28px;
      align-items: start;
    }

    @media (max-width: 1024px) {
      .itinerary-layout {
        grid-template-columns: 1fr;
      }
    }

    /* Map Column */
    .map-column {
      position: sticky;
      top: 96px;
    }

    .map-card {
      background: var(--bg-surface);
      border-radius: var(--radius-md);
      border: 1px solid var(--border-color);
      box-shadow: var(--shadow-md);
      overflow: hidden;
    }

    .map-header {
      padding: 14px 18px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #faf8f5;
      border-bottom: 1px solid var(--border-color);
    }

    .map-title {
      font-size: 0.95rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text-main);
    }

    .map-filter-tags {
      display: flex;
      gap: 6px;
      font-size: 0.78rem;
    }

    .map-tag {
      padding: 4px 10px;
      border-radius: 20px;
      background: #fff;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      cursor: pointer;
      font-weight: 600;
      transition: all 0.15s ease;
    }
    .map-tag.active {
      background: var(--text-main);
      color: #fff;
      border-color: var(--text-main);
    }

    #trip-map {
      height: 520px;
      width: 100%;
      background: #e8ecef;
      z-index: 1;
    }

    @media (max-width: 1024px) {
      #trip-map {
        height: 380px;
      }
      .map-column {
        position: relative;
        top: 0;
        margin-bottom: 20px;
      }
    }

    .map-footer-tip {
      padding: 10px 16px;
      font-size: 0.78rem;
      color: var(--text-muted);
      background: #fff;
      border-top: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      gap: 6px;
    }

    /* Content Stream */
    .timeline-stream {
      display: flex;
      flex-direction: column;
      gap: 24px;
    }

    .day-section {
      background: var(--bg-surface);
      border-radius: var(--radius-md);
      border: 1px solid var(--border-color);
      box-shadow: var(--shadow-sm);
      padding: 24px;
      scroll-margin-top: 100px;
      transition: border-color 0.2s ease;
    }

    .day-section:hover {
      border-color: #dfd6cb;
    }

    .day-section-header {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 20px;
      padding-bottom: 14px;
      border-bottom: 2px dashed var(--border-color);
    }

    .day-header-left {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .day-number-badge {
      width: 52px;
      height: 52px;
      border-radius: 16px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      color: #fff;
      box-shadow: var(--shadow-sm);
    }

    .day-badge-1 { background: linear-gradient(135deg, #e07a7e 0%, #c44f53 100%); }
    .day-badge-2 { background: linear-gradient(135deg, #9b51e0 0%, #6c31a7 100%); }
    .day-badge-3 { background: linear-gradient(135deg, #2f80ed 0%, #1752a1 100%); }
    .day-badge-4 { background: linear-gradient(135deg, #27ae60 0%, #1b7340 100%); }
    .day-badge-5 { background: linear-gradient(135deg, #f2994a 0%, #d46f1e 100%); }

    .day-number-badge .d-num {
      font-size: 1.15rem;
      line-height: 1;
    }
    .day-number-badge .d-lbl {
      font-size: 0.6rem;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      opacity: 0.9;
    }

    .day-titles h2 {
      font-family: var(--font-display);
      font-size: 1.35rem;
      font-weight: 700;
      color: var(--text-main);
      line-height: 1.25;
    }

    .day-titles p {
      font-size: 0.85rem;
      color: var(--text-muted);
      margin-top: 2px;
    }

    .day-theme-pill {
      font-size: 0.75rem;
      font-weight: 600;
      padding: 5px 12px;
      border-radius: 20px;
      background: var(--bg-subtle);
      color: var(--text-main);
      border: 1px solid var(--border-color);
      align-self: center;
    }

    /* Timeline Items */
    .timeline-cards {
      display: flex;
      flex-direction: column;
      gap: 16px;
      position: relative;
    }

    .timeline-cards::before {
      content: "";
      position: absolute;
      left: 20px;
      top: 15px;
      bottom: 25px;
      width: 2px;
      background: #f0ebe4;
      z-index: 0;
    }

    .activity-card {
      position: relative;
      margin-left: 48px;
      background: #fff;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 16px 18px;
      box-shadow: 0 2px 6px rgba(0,0,0,0.02);
      transition: all 0.2s ease;
      cursor: pointer;
    }

    .activity-card:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-sm);
      border-color: var(--accent-rose);
    }

    .activity-icon-bullet {
      position: absolute;
      left: -48px;
      top: 16px;
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: #fff;
      border: 2px solid var(--primary);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.88rem;
      z-index: 1;
      box-shadow: 0 2px 5px rgba(0,0,0,0.06);
    }

    .activity-meta {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
      flex-wrap: wrap;
      gap: 6px;
    }

    .activity-time {
      font-size: 0.82rem;
      font-weight: 700;
      color: var(--primary);
      display: flex;
      align-items: center;
      gap: 5px;
      background: var(--primary-light);
      padding: 2px 8px;
      border-radius: 6px;
    }

    .activity-badge {
      font-size: 0.72rem;
      font-weight: 600;
      padding: 2px 8px;
      border-radius: 6px;
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .badge-booking {
      background: #e6f4ea;
      color: #137333;
      border: 1px solid #b7e1cd;
    }

    .badge-transit {
      background: #e8f0fe;
      color: #1a73e8;
      border: 1px solid #aecbfa;
    }

    .badge-highlight {
      background: #fef7e0;
      color: #b06000;
      border: 1px solid #fce8b2;
    }

    .activity-title-group h3 {
      font-size: 1.05rem;
      font-weight: 700;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 6px;
      margin-bottom: 2px;
    }

    .activity-subname {
      font-size: 0.82rem;
      color: var(--text-muted);
      margin-bottom: 8px;
    }

    .activity-desc {
      font-size: 0.88rem;
      color: #484542;
      margin-bottom: 12px;
      line-height: 1.5;
    }

    .activity-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 10px;
      border-top: 1px solid #f3efea;
      font-size: 0.8rem;
      flex-wrap: wrap;
      gap: 8px;
    }

    .activity-location {
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .card-actions {
      display: flex;
      gap: 8px;
    }

    .action-link {
      color: var(--primary);
      text-decoration: none;
      font-weight: 600;
      font-size: 0.78rem;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 8px;
      border-radius: 4px;
      background: var(--bg-subtle);
      transition: background 0.15s ease;
    }
    .action-link:hover {
      background: var(--primary-light);
    }

    /* Transit Timetable Visual Card */
    .transit-schedule-box {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: var(--radius-sm);
      padding: 16px;
      margin: 12px 0;
    }

    .transit-step {
      display: flex;
      align-items: flex-start;
      gap: 12px;
      position: relative;
      padding-bottom: 14px;
    }

    .transit-step:last-child {
      padding-bottom: 0;
    }

    .transit-step::after {
      content: "";
      position: absolute;
      left: 17px;
      top: 24px;
      bottom: -2px;
      width: 2px;
      background: #cbd5e1;
    }

    .transit-step:last-child::after {
      display: none;
    }

    .transit-time-badge {
      font-family: monospace;
      font-size: 0.85rem;
      font-weight: 700;
      color: #0f172a;
      width: 48px;
      text-align: right;
    }

    .transit-icon-dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: #3b82f6;
      border: 2px solid #fff;
      box-shadow: 0 0 0 2px #3b82f6;
      margin-top: 4px;
      z-index: 1;
    }

    .transit-icon-dot.start { background: #10b981; box-shadow: 0 0 0 2px #10b981; }
    .transit-icon-dot.end { background: #ef4444; box-shadow: 0 0 0 2px #ef4444; }

    .transit-details {
      flex: 1;
    }

    .transit-station {
      font-weight: 700;
      font-size: 0.92rem;
      color: #1e293b;
    }

    .transit-line-info {
      font-size: 0.8rem;
      color: #64748b;
      margin-top: 2px;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
    }

    .line-tag {
      background: #e2e8f0;
      padding: 1px 6px;
      border-radius: 4px;
      font-size: 0.75rem;
      color: #334155;
      font-weight: 600;
    }

    .fare-tag {
      font-size: 0.75rem;
      color: #047857;
      font-weight: 600;
    }

    /* Romantic Highlights Box */
    .couple-tips-banner {
      background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
      border: 1px solid #fed7aa;
      border-radius: var(--radius-sm);
      padding: 14px 18px;
      margin-top: 14px;
      display: flex;
      gap: 12px;
      align-items: flex-start;
    }

    .couple-tips-banner .tip-icon {
      font-size: 1.4rem;
      line-height: 1;
    }

    .couple-tips-banner h4 {
      font-size: 0.88rem;
      font-weight: 700;
      color: #9a3412;
      margin-bottom: 3px;
    }

    .couple-tips-banner p {
      font-size: 0.82rem;
      color: #7c2d12;
      line-height: 1.45;
    }

    /* Couple Checklist & Tips Section */
    .essentials-section {
      margin-top: 40px;
      background: var(--bg-surface);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-sm);
      padding: 28px;
    }

    .essentials-section h2 {
      font-family: var(--font-display);
      font-size: 1.4rem;
      margin-bottom: 20px;
      display: flex;
      align-items: center;
      gap: 10px;
      color: var(--text-main);
    }

    .essentials-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 20px;
    }

    .essential-card {
      background: var(--bg-subtle);
      border-radius: var(--radius-sm);
      padding: 18px;
      border: 1px solid #eee8e0;
    }

    .essential-card h3 {
      font-size: 0.98rem;
      font-weight: 700;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--primary);
    }

    .checklist-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .checklist-item {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.85rem;
      color: #444;
      cursor: pointer;
    }

    .checklist-item input[type="checkbox"] {
      width: 16px;
      height: 16px;
      accent-color: var(--primary);
      cursor: pointer;
    }

    /* Custom Leaflet Marker Popup */
    .leaflet-popup-content-wrapper {
      border-radius: 14px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.15);
      padding: 4px;
    }

    .popup-custom {
      font-family: var(--font-body);
      max-width: 240px;
    }

    .popup-custom h4 {
      font-size: 0.95rem;
      font-weight: 700;
      color: #222;
      margin-bottom: 2px;
    }

    .popup-custom .popup-time {
      font-size: 0.76rem;
      color: var(--primary);
      font-weight: 700;
      margin-bottom: 6px;
      display: block;
    }

    .popup-custom p {
      font-size: 0.78rem;
      color: #666;
      line-height: 1.4;
      margin-bottom: 8px;
    }

    .popup-custom a {
      display: inline-block;
      font-size: 0.75rem;
      font-weight: 600;
      color: #fff;
      background: var(--primary);
      padding: 4px 10px;
      border-radius: 4px;
      text-decoration: none;
    }

    /* Floating Navigation Controls on Mobile */
    .floating-map-btn {
      display: none;
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 999;
      background: var(--primary);
      color: #fff;
      padding: 12px 22px;
      border-radius: 50px;
      box-shadow: 0 6px 20px rgba(155, 44, 71, 0.4);
      font-weight: 700;
      border: none;
      align-items: center;
      gap: 8px;
      cursor: pointer;
    }

    @media (max-width: 1024px) {
      .floating-map-btn {
        display: flex;
      }
    }

    /* Print Optimizations */
    @media print {
      .hero-actions, .day-nav-wrapper, .floating-map-btn, .map-column, .card-actions {
        display: none !important;
      }
      .itinerary-layout {
        display: block !important;
      }
      .day-section {
        box-shadow: none !important;
        border: 1px solid #ccc !important;
        page-break-inside: avoid;
        margin-bottom: 20px;
      }
    }
  </style>
</head>
<body>

  <!-- Hero Banner -->
  <header class="hero">
    <div class="hero-badge">
      <span>✨ Our Tokyo & Kusatsu Getaway ✨</span>
    </div>
    <h1>Romantic Escape to Japan</h1>
    <p class="hero-subtitle">Five unforgettable days of world-class dining, Disney romance, private hot springs, and Tokyo panoramic skies.</p>
    
    <div class="hero-stats">
      <div class="stat-pill">
        <span>📅</span>
        <span>Sep 25 – Sep 29, 2026</span>
      </div>
      <div class="stat-pill">
        <span>🍣</span>
        <span>Sukiyabashi Jiro & Wolfgang's</span>
      </div>
      <div class="stat-pill">
        <span>♨️</span>
        <span>Hotel Sakurai Kusatsu</span>
      </div>
      <div class="stat-pill">
        <span>🍸</span>
        <span>VIRTÙ & New York Bar</span>
      </div>
    </div>

    <div class="hero-actions">
      <a href="#trip-map-container" class="btn btn-gold" onclick="focusMapAll()">
        <span>🗺️ Explore Map</span>
      </a>
      <button class="btn btn-white-glass" onclick="window.print()">
        <span>🖨️ Save as PDF / Print</span>
      </button>
      <button class="btn btn-white-glass" onclick="copyShareLink()">
        <span id="share-btn-text">🔗 Share with Her</span>
      </button>
    </div>
  </header>

  <!-- Sticky Day Selector -->
  <div class="day-nav-wrapper">
    <div class="app-container" style="padding-top:0; padding-bottom:0;">
      <nav class="day-nav">
        <button class="day-tab active" onclick="switchDay('all', this)">
          <span class="tab-date">Overview</span>
          <span>✨ All Days</span>
        </button>
        <button class="day-tab" onclick="switchDay('day1', this)">
          <span class="tab-date">Fri Sep 25</span>
          <span>Day 1 • Warm-up</span>
        </button>
        <button class="day-tab" onclick="switchDay('day2', this)">
          <span class="tab-date">Sat Sep 26</span>
          <span>Day 2 • Jiro & Tower</span>
        </button>
        <button class="day-tab" onclick="switchDay('day3', this)">
          <span class="tab-date">Sun Sep 27</span>
          <span>Day 3 • DisneySea</span>
        </button>
        <button class="day-tab" onclick="switchDay('day4', this)">
          <span class="tab-date">Mon Sep 28</span>
          <span>Day 4 • Kusatsu Onsen</span>
        </button>
        <button class="day-tab" onclick="switchDay('day5', this)">
          <span class="tab-date">Tue Sep 29</span>
          <span>Day 5 • Steak & Skyline</span>
        </button>
      </nav>
    </div>
  </div>

  <main class="app-container">
    <div class="itinerary-layout">
      
      <!-- Interactive Leaflet Map Column -->
      <aside class="map-column" id="trip-map-container">
        <div class="map-card">
          <div class="map-header">
            <div class="map-title">
              <span>📍</span>
              <span>Interactive Trip Map</span>
            </div>
            <div class="map-filter-tags">
              <span class="map-tag active" onclick="filterMapByDay('all', this)">All</span>
              <span class="map-tag" onclick="filterMapByDay(1, this)">D1</span>
              <span class="map-tag" onclick="filterMapByDay(2, this)">D2</span>
              <span class="map-tag" onclick="filterMapByDay(3, this)">D3</span>
              <span class="map-tag" onclick="filterMapByDay(4, this)">D4</span>
              <span class="map-tag" onclick="filterMapByDay(5, this)">D5</span>
            </div>
          </div>
          <div id="trip-map"></div>
          <div class="map-footer-tip">
            <span>💡</span>
            <span>Click any location in the schedule to highlight & fly to it on the map.</span>
          </div>
        </div>
      </aside>

      <!-- Day by Day Timelines -->
      <section class="timeline-stream">
        
        <!-- DAY 1 -->
        <article class="day-section" id="day1">
          <div class="day-section-header">
            <div class="day-header-left">
              <div class="day-number-badge day-badge-1">
                <span class="d-num">01</span>
                <span class="d-lbl">Day</span>
              </div>
              <div class="day-titles">
                <h2>Friday, September 25</h2>
                <p>Welcome Dinner & Cozy Evening</p>
              </div>
            </div>
            <span class="day-theme-pill">🍴 Casual Gourmet</span>
          </div>

          <div class="timeline-cards">
            <!-- Shane's Burg Shinyurigaoka -->
            <div class="activity-card" onclick="flyToSpot(35.6033, 139.5080, 'Shane\'s Burg Shinyurigaoka')">
              <div class="activity-icon-bullet">🥩</div>
              <div class="activity-meta">
                <span class="activity-time">⏰ 19:00 (7:00 PM)</span>
                <span class="activity-badge badge-booking">✓ Dinner Reserved</span>
              </div>
              <div class="activity-title-group">
                <h3>Shane's Burg (シェーンズバーグ 新百合ヶ丘店)</h3>
                <div class="activity-subname">Shinyuri Elmi Road 5F • Hamburg Steak House</div>
              </div>
              <p class="activity-desc">
                Handcrafted premium Japanese-American hamburger steaks prepared fresh daily and grilled over open flame. Juicy, comforting, and relaxed atmosphere to kick off the trip together.
              </p>
              <div class="activity-footer">
                <span class="activity-location">📍 Shinyurigaoka Station (Odakyu Line)</span>
                <div class="card-actions">
                  <a href="https://tabelog.com/kanagawa/A1405/A140508/14009641/" target="_blank" class="action-link" onclick="event.stopPropagation()">📖 Tabelog</a>
                  <a href="https://maps.google.com/?q=Shane's+Burg+Shin-Yurigaoka" target="_blank" class="action-link" onclick="event.stopPropagation()">🗺️ Google Maps</a>
                </div>
              </div>
            </div>
          </div>

          <div class="couple-tips-banner">
            <span class="tip-icon">✨</span>
            <div>
              <h4>Couple's Evening Note</h4>
              <p>Get a good night's rest after dinner! Tomorrow is our big Tokyo glam day featuring world-renowned Jiro sushi at 13:00.</p>
            </div>
          </div>
        </article>

        <!-- DAY 2 -->
        <article class="day-section" id="day2">
          <div class="day-section-header">
            <div class="day-header-left">
              <div class="day-number-badge day-badge-2">
                <span class="d-num">02</span>
                <span class="d-lbl">Day</span>
              </div>
              <div class="day-titles">
                <h2>Saturday, September 26</h2>
                <p>Jiro Omakase, Tokyo Tower & Sky Bar</p>
              </div>
            </div>
            <span class="day-theme-pill">🍣 Icon & Skyline</span>
          </div>

          <div class="timeline-cards">
            <!-- Sukiyabashi Jiro Roppongi Hills -->
            <div class="activity-card" onclick="flyToSpot(35.6586978, 139.7291446, 'Sukiyabashi Jiro Roppongi Hills')">
              <div class="activity-icon-bullet">🍣</div>
              <div class="activity-meta">
                <span class="activity-time">⏰ 13:00 (1:00 PM)</span>
                <span class="activity-badge badge-booking">✓ VIP Reservation</span>
              </div>
              <div class="activity-title-group">
                <h3>Sukiyabashi Jiro Roppongi Hills (すきやばし 次郎)</h3>
                <div class="activity-subname">Roppongi Hills Keyakizaka Dori 3F • Legendary Edomae Sushi</div>
              </div>
              <p class="activity-desc">
                An unforgettable Edomae sushi omakase crafted by master chef Takashi Ono (son of legendary Jiro Ono). Flawless fish temperature, perfect vinegared rice, and world-class intimacy.
              </p>
              <div class="activity-footer">
                <span class="activity-location">📍 Roppongi Hills, Minato-ku</span>
                <div class="card-actions">
                  <a href="https://maps.app.goo.gl/Brh2wvb1fPBVpNn79" target="_blank" class="action-link" onclick="event.stopPropagation()">🗺️ Google Maps</a>
                </div>
              </div>
            </div>

            <!-- Tokyo Tower -->
            <div class="activity-card" onclick="flyToSpot(35.6585805, 139.7454329, 'Tokyo Tower')">
              <div class="activity-icon-bullet">🗼</div>
              <div class="activity-meta">
                <span class="activity-time">⏰ 15:30 – 17:00</span>
                <span class="activity-badge badge-highlight">Romantic Sightseeing</span>
              </div>
              <div class="activity-title-group">
                <h3>Tokyo Tower (東京タワー)</h3>
                <div class="activity-subname">Main Deck & Skywalk Window • Shiba-koen</div>
              </div>
              <p class="activity-desc">
                Tokyo's most romantic vintage icon! Panoramic 360° views across the metropolis, glass floor look-down windows, and cute couple photo-ops.
              </p>
              <div class="activity-footer">
                <span class="activity-location">📍 10-15 min taxi from Roppongi Hills</span>
                <div class="card-actions">
                  <a href="https://www.tokyotower.co.jp/en/" target="_blank" class="action-link" onclick="event.stopPropagation()">🌐 Official Site</a>
                </div>
              </div>
            </div>

            <!-- VIRTU at Four Seasons -->
            <div class="activity-card" onclick="flyToSpot(35.6872, 139.7645, 'VIRTÙ Cocktail Bar')">
              <div class="activity-icon-bullet">🍸</div>
              <div class="activity-meta">
                <span class="activity-time">⏰ 17:30 – 19:15</span>
                <span class="activity-badge badge-highlight">Asia's 50 Best Bars</span>
              </div>
              <div class="activity-title-group">
                <h3>VIRTÙ (Four Seasons Hotel Otemachi 39F)</h3>
                <div class="activity-subname">Sky-high Parisian Salon meets Tokyo Mixology</div>
              </div>
              <p class="activity-desc">
                Sip exquisite aperitifs while watching the sun dip behind the Imperial Palace gardens and Tokyo skyline. Sumptuous Art Deco decor and signature Japanese-French cocktails like the Smoked Ume Fashioned.
              </p>
              <div class="activity-footer">
                <span class="activity-location">📍 Otemachi (Direct underground access)</span>
                <div class="card-actions">
                  <a href="https://www.fourseasons.com/tokyo-otemachi/dining/lounges/virtu/" target="_blank" class="action-link" onclick="event.stopPropagation()">🍸 Menu & Dress Code</a>
                </div>
              </div>
            </div>

            <!-- Kura Sushi -->
            <div class="activity-card" onclick="flyToSpot(35.6719, 139.7648, 'Muten Kura Sushi')">
              <div class="activity-icon-bullet">🍣</div>
              <div class="activity-meta">
                <span class="activity-time">⏰ 20:00 (8:00 PM)</span>
                <span class="activity-badge badge-booking">Fun Casual Dinner</span>
              </div>
              <div class="activity-title-group">
                <h3>Kura Sushi / Muten Kura (無添くら寿司)</h3>
                <div class="activity-subname">Additive-Free Conveyor-Belt Sushi & Bikkura-Pon!</div>
              </div>
              <p class="activity-desc">
                Playful, delicious conveyor sushi where every 5 empty plates triggers the Bikkura-Pon capsule lottery game on your table screen. A super fun, lighthearted contrast to lunch!
              </p>
              <div class="activity-footer">
                <span class="activity-location">📍 Central Tokyo Flagship / Ginza</span>
                <div class="card-actions">
                  <a href="https://www.kurasushi.co.jp/mutenkura/" target="_blank" class="action-link" onclick="event.stopPropagation()">🌐 Official Site</a>
                </div>
              </div>
            </div>
          </div>
        </article>

        <!-- DAY 3 -->
        <article class="day-section" id="day3">
          <div class="day-section-header">
            <div class="day-header-left">
              <div class="day-number-badge day-badge-3">
                <span class="d-num">03</span>
                <span class="d-lbl">Day</span>
              </div>
              <div class="day-titles">
                <h2>Sunday, September 27</h2>
                <p>Tokyo DisneySea & S.S. Columbia Dinner</p>
              </div>
            </div>
            <span class="day-theme-pill">🌊 Disney Magic</span>
          </div>

          <div class="timeline-cards">
            <!-- Tokyo DisneySea Entry -->
            <div class="activity-card" onclick="flyToSpot(35.6267, 139.8851, 'Tokyo DisneySea')">
              <div class="activity-icon-bullet">🏰</div>
              <div class="activity-meta">
                <span class="activity-time">⏰ 09:00 AM Entry</span>
                <span class="activity-badge badge-booking">Full Day Park Pass</span>
              </div>
              <div class="activity-title-group">
                <h3>Tokyo DisneySea (東京ディズニーシー)</h3>
                <div class="activity-subname">Mediterranean Harbor • Fantasy Springs • American Waterfront</div>
              </div>
              <p class="activity-desc">
                The world's most romantic theme park! Wander Mediterranean ports, Venice gondolas, Aladdin's Arabian Coast, and Fantasy Springs (Frozen, Peter Pan, Rapunzel's Lanterns).
              </p>
              <div class="activity-footer">
                <span class="activity-location">📍 Maihama Station (Disney Resort Line)</span>
                <div class="card-actions">
                  <a href="https://www.tokyodisneyresort.jp/en/tds/" target="_blank" class="action-link" onclick="event.stopPropagation()">📱 Tokyo Disney App</a>
                </div>
              </div>
            </div>

            <!-- S.S. Columbia Dinner -->
            <div class="activity-card" onclick="flyToSpot(35.6238, 139.8860, 'S.S. Columbia Dining Room')">
              <div class="activity-icon-bullet">🛳️</div>
              <div class="activity-meta">
                <span class="activity-time">⏰ 19:20 (7:20 PM)</span>
                <span class="activity-badge badge-booking">✓ Priority Seating Confirmed</span>
              </div>
              <div class="activity-title-group">
                <h3>S.S. Columbia Dining Room (S.S.コロンビア)</h3>
                <div class="activity-subname">Inside the Luxury 1912 Ocean Liner • 3rd Deck</div>
              </div>
              <p class="activity-desc">
                Dine in grand 20th-century luxury liner elegance with chandeliers, crystal glassware, prime roast beef, and tender sirloin course dinner. Romantic nautical ambiance at its finest.
              </p>
              <div class="activity-footer">
                <span class="activity-location">📍 American Waterfront (DisneySea)</span>
                <div class="card-actions">
                  <a href="https://www.tokyodisneyresort.jp/en/tds/restaurant/detail/431/" target="_blank" class="action-link" onclick="event.stopPropagation()">🍽️ Restaurant Details</a>
                </div>
              </div>
            </div>

            <!-- Believe Night Spectacular -->
            <div class="activity-card" onclick="flyToSpot(35.6267, 139.8851, 'Believe! Sea of Dreams')">
              <div class="activity-icon-bullet">🎆</div>
              <div class="activity-meta">
                <span class="activity-time">⏰ 20:30 PM</span>
                <span class="activity-badge badge-highlight">Night Show</span>
              </div>
              <div class="activity-title-group">
                <h3>Believe! Sea of Dreams (ビリーヴ！〜シー・オブ・ドリームス〜)</h3>
                <div class="activity-subname">Mediterranean Harbor Water & Fireworks Spectacle</div>
              </div>
              <p class="activity-desc">
                Spectacular light projections across Hotel MiraCosta, soaring laser boats, stirring music, and fireworks to conclude an enchanting day.
              </p>
            </div>
          </div>
        </article>

        <!-- DAY 4 -->
        <article class="day-section" id="day4">
          <div class="day-section-header">
            <div class="day-header-left">
              <div class="day-number-badge day-badge-4">
                <span class="d-num">04</span>
                <span class="d-lbl">Day</span>
              </div>
              <div class="day-titles">
                <h2>Monday, September 28</h2>
                <p>Scenic Train to Kusatsu Onsen & Hotel Sakurai</p>
              </div>
            </div>
            <span class="day-theme-pill">♨️ Hot Springs & Ryokan</span>
          </div>

          <!-- Transit Timetable from Screenshot -->
          <div class="transit-schedule-box">
            <div style="font-weight:700; font-size:0.9rem; margin-bottom:12px; display:flex; justify-content:space-between;">
              <span>🚆 Travel Schedule: Route 2 (As per your Screenshot)</span>
              <span style="color:#047857;">Total: 3h 58m • ¥6,353 (198.8 km)</span>
            </div>

            <div class="transit-step">
              <span class="transit-time-badge">08:55</span>
              <div class="transit-icon-dot start"></div>
              <div class="transit-details">
                <div class="transit-station">百合ヶ丘 (Yurigaoka) [Track 2]</div>
                <div class="transit-line-info">
                  <span class="line-tag">小田急小田原線 (新宿行)</span>
                  <span>Board Car 8 front</span>
                  <span class="fare-tag">¥293</span>
                </div>
              </div>
            </div>

            <div class="transit-step">
              <span class="transit-time-badge">09:39<br><span style="font-size:0.75rem; color:#64748b;">09:51</span></span>
              <div class="transit-icon-dot"></div>
              <div class="transit-details">
                <div class="transit-station">新宿 (Shinjuku) [Arrive Tr.10 → Depart Tr.3]</div>
                <div class="transit-line-info">
                  <span class="line-tag">JR 埼京線 (武蔵浦和行・当駅始発)</span>
                  <span>12 min transfer</span>
                </div>
              </div>
            </div>

            <div class="transit-step">
              <span class="transit-time-badge">10:04<br><span style="font-size:0.75rem; color:#64748b;">10:10</span></span>
              <div class="transit-icon-dot"></div>
              <div class="transit-details">
                <div class="transit-station">赤羽 (Akabane) [Arrive Tr.8 → Depart Tr.4]</div>
                <div class="transit-line-info">
                  <span class="line-tag">JR 特急草津・四万1号 (長野原草津口行)</span>
                  <span style="font-weight:700; color:#b91c1c;">Car 4 Reserved Seat (指定席)</span>
                  <span class="fare-tag">Base ¥3,190 + Express ¥2,090</span>
                </div>
              </div>
            </div>

            <div class="transit-step">
              <span class="transit-time-badge">12:18<br><span style="font-size:0.75rem; color:#64748b;">12:31</span></span>
              <div class="transit-icon-dot"></div>
              <div class="transit-details">
                <div class="transit-station">長野原草津口 (Naganoharakusatsuguchi)</div>
                <div class="transit-line-info">
                  <span>3 min walk from train to Bus Stop</span>
                  <span class="line-tag">JRバス関東 (直通 草津温泉行)</span>
                  <span class="fare-tag">¥780</span>
                </div>
              </div>
            </div>

            <div class="transit-step">
              <span class="transit-time-badge">12:53</span>
              <div class="transit-icon-dot end"></div>
              <div class="transit-details">
                <div class="transit-station">草津温泉バスターミナル (Kusatsu Onsen)</div>
                <div class="transit-line-info">
                  <span style="font-weight:600; color:#10b981;">Arrival at Onsen Paradise! ✨</span>
                </div>
              </div>
            </div>
          </div>

          <div class="timeline-cards">
            <!-- Hotel Sakurai Checkin -->
            <div class="activity-card" onclick="flyToSpot(36.6212, 138.5996, 'Hotel Sakurai Kusatsu')">
              <div class="activity-icon-bullet">🏨</div>
              <div class="activity-meta">
                <span class="activity-time">⏰ 13:30 Check-in</span>
                <span class="activity-badge badge-booking">✓ Luxury Ryokan Stay</span>
              </div>
              <div class="activity-title-group">
                <h3>Hotel Sakurai (草津温泉 ホテル櫻井)</h3>
                <div class="activity-subname">Gunma's Best Onsen Ryokan • 3 Natural Springs</div>
              </div>
              <p class="activity-desc">
                Kusatsu's premier ryokan with 3 distinct mineral spring sources, one of Japan's largest hot spring baths, outdoor stone pools, yukata robes, and soothing mountain hospitality.
              </p>
              <div class="activity-footer">
                <span class="activity-location">📍 Kusatsu-machi, Agatsuma-gun</span>
                <div class="card-actions">
                  <a href="https://www.hotel-sakurai.co.jp/" target="_blank" class="action-link" onclick="event.stopPropagation()">♨️ Official Hotel Site</a>
                </div>
              </div>
            </div>

            <!-- Yubatake Stroll -->
            <div class="activity-card" onclick="flyToSpot(36.6208, 138.5960, 'Yubatake Hot Spring Field')">
              <div class="activity-icon-bullet">♨️</div>
              <div class="activity-meta">
                <span class="activity-time">⏰ 15:30 – 18:00</span>
                <span class="activity-badge badge-highlight">Must-Do Experience</span>
              </div>
              <div class="activity-title-group">
                <h3>Yubatake & Town Stroll (湯畑)</h3>
                <div class="activity-subname">Steaming Thermal Springs & Free Foot Baths</div>
              </div>
              <p class="activity-desc">
                Stroll the wooden boardwalks around the steaming emerald-green hot water fields in your yukata. Taste warm onsen manju (sweet red bean buns), soak your feet in the outdoor foot baths (Ashiyu), and enjoy the magical dusk illuminations.
              </p>
            </div>
          </div>
        </article>

        <!-- DAY 5 -->
        <article class="day-section" id="day5">
          <div class="day-section-header">
            <div class="day-header-left">
              <div class="day-number-badge day-badge-5">
                <span class="d-num">05</span>
                <span class="d-lbl">Day</span>
              </div>
              <div class="day-titles">
                <h2>Tuesday, September 29</h2>
                <p>Shinkansen, Wolfgang's Steak & Skyline Jazz</p>
              </div>
            </div>
            <span class="day-theme-pill">🥩 Grand Finale</span>
          </div>

          <!-- Return Transit Timetable from Screenshot -->
          <div class="transit-schedule-box">
            <div style="font-weight:700; font-size:0.9rem; margin-bottom:12px; display:flex; justify-content:space-between;">
              <span>🚅 Return Travel: Kusatsu → Gaienmae (From Screenshot)</span>
              <span style="color:#047857;">Arrives 13:35 • Plenty of time for 14:30 Steak!</span>
            </div>

            <div class="transit-step">
              <span class="transit-time-badge">09:20</span>
              <div class="transit-icon-dot start"></div>
              <div class="transit-details">
                <div class="transit-station">草津温泉 (Kusatsu Onsen Bus Terminal)</div>
                <div class="transit-line-info">
                  <span class="line-tag">JRバス関東 (長野原草津口行)</span>
                  <span class="fare-tag">¥780</span>
                </div>
              </div>
            </div>

            <div class="transit-step">
              <span class="transit-time-badge">09:48<br><span style="font-size:0.75rem; color:#64748b;">10:08</span></span>
              <div class="transit-icon-dot"></div>
              <div class="transit-details">
                <div class="transit-station">長野原草津口 (Naganoharakusatsuguchi)</div>
                <div class="transit-line-info">
                  <span class="line-tag">JR 吾妻線 (高崎行・当駅始発)</span>
                  <span>Arrives Takasaki Track 7</span>
                </div>
              </div>
            </div>

            <div class="transit-step">
              <span class="transit-time-badge">11:35<br><span style="font-size:0.75rem; color:#64748b;">12:04</span></span>
              <div class="transit-icon-dot"></div>
              <div class="transit-details">
                <div class="transit-station">高崎 (Takasaki) [Track 13]</div>
                <div class="transit-line-info">
                  <span class="line-tag">JR 新幹線たにがわ410号 (東京行)</span>
                  <span style="font-weight:600;">Shinkansen Bullet Train</span>
                  <span class="fare-tag">Base ¥3,190 + Non-reserved ¥2,510</span>
                </div>
              </div>
            </div>

            <div class="transit-step">
              <span class="transit-time-badge">13:00<br><span style="font-size:0.75rem; color:#64748b;">13:13</span></span>
              <div class="transit-icon-dot"></div>
              <div class="transit-details">
                <div class="transit-station">東京 (Tokyo Station) [Tr.21 → Tr.5]</div>
                <div class="transit-line-info">
                  <span class="line-tag">JR 山手線外回り (品川・渋谷方面)</span>
                </div>
              </div>
            </div>

            <div class="transit-step">
              <span class="transit-time-badge">13:17<br><span style="font-size:0.75rem; color:#64748b;">13:26</span></span>
              <div class="transit-icon-dot"></div>
              <div class="transit-details">
                <div class="transit-station">新橋 (Shimbashi) [Track 4 → Track 1]</div>
                <div class="transit-line-info">
                  <span class="line-tag">東京メトロ銀座線 (渋谷行)</span>
                  <span class="fare-tag">¥178</span>
                </div>
              </div>
            </div>

            <div class="transit-step">
              <span class="transit-time-badge">13:35</span>
              <div class="transit-icon-dot end"></div>
              <div class="transit-details">
                <div class="transit-station">外苑前 (Gaienmae) [Exit 4a]</div>
                <div class="transit-line-info">
                  <span style="font-weight:600; color:#10b981;">Step out directly to Wolfgang's Steakhouse! 🥩</span>
                </div>
              </div>
            </div>
          </div>

          <div class="timeline-cards">
            <!-- Wolfgang's Steakhouse Aoyama -->
            <div class="activity-card" onclick="flyToSpot(35.6698, 139.7180, 'Wolfgang\'s Steakhouse Signature Aoyama')">
              <div class="activity-icon-bullet">🥩</div>
              <div class="activity-meta">
                <span class="activity-time">⏰ 14:30 (2:30 PM)</span>
                <span class="activity-badge badge-booking">✓ Must Arrive 14:30</span>
              </div>
              <div class="activity-title-group">
                <h3>Wolfgang's Steakhouse Signature Aoyama</h3>
                <div class="activity-subname">THE ARGYLE AOYAMA • USDA Prime Dry-Aged Beef</div>
              </div>
              <p class="activity-desc">
                Celebrated for sizzling 28-day dry-aged USDA Prime Porterhouse served on piping-hot platters with melted butter, jumbo lump crab cakes, creamed spinach, and warm pecan pie.
              </p>
              <div class="activity-footer">
                <span class="activity-location">📍 Gaienmae Station Exit 4a</span>
                <div class="card-actions">
                  <a href="https://wolfgangssteakhouse.jp/" target="_blank" class="action-link" onclick="event.stopPropagation()">🥩 Official Site</a>
                </div>
              </div>
            </div>

            <!-- Shibuya Stroll -->
            <div class="activity-card" onclick="flyToSpot(35.6595, 139.7005, 'Shibuya Crossing & Miyashita')">
              <div class="activity-icon-bullet">🌆</div>
              <div class="activity-meta">
                <span class="activity-time">⏰ 19:30 (7:30 PM)</span>
                <span class="activity-badge badge-highlight">Vibrant City Vibes</span>
              </div>
              <div class="activity-title-group">
                <h3>Shibuya Evening (渋谷)</h3>
                <div class="activity-subname">Shibuya Scramble • Miyashita Park • Shibuya Sky</div>
              </div>
              <p class="activity-desc">
                Feel Tokyo's electric heartbeat: cross the famous Scramble, browse boutiques and rooftop park at Miyashita Park, grab a sweet treat, or marvel at the 360° neon city lights.
              </p>
            </div>

            <!-- New York Bar at Park Hyatt -->
            <div class="activity-card" onclick="flyToSpot(35.6856, 139.6910, 'New York Bar at Park Hyatt Tokyo')">
              <div class="activity-icon-bullet">🎷</div>
              <div class="activity-meta">
                <span class="activity-time">⏰ 21:30 – Late</span>
                <span class="activity-badge badge-booking">Iconic Nightcap</span>
              </div>
              <div class="activity-title-group">
                <h3>New York Bar (Park Hyatt Tokyo 52F)</h3>
                <div class="activity-subname">Newly Renovated & Reopened • Shinjuku Penthouse</div>
              </div>
              <p class="activity-desc">
                The cinematic rooftop jazz sanctuary made famous in *Lost in Translation*, completely restored to timeless glamour. Sip craft martinis to live jazz against the dazzling Tokyo skyline lights. The most romantic toast to conclude our journey!
              </p>
              <div class="activity-footer">
                <span class="activity-location">📍 Shinjuku Park Tower 52F</span>
                <div class="card-actions">
                  <a href="https://maps.google.com/?q=New+York+Bar+Park+Hyatt+Tokyo" target="_blank" class="action-link" onclick="event.stopPropagation()">🗺️ Google Maps</a>
                </div>
              </div>
            </div>
          </div>
        </article>

      </section>
    </div>

    <!-- Couple's Essentials & Checklist -->
    <section class="essentials-section">
      <h2><span>🎒</span> Couple's Travel Essentials & Tips</h2>
      <div class="essentials-grid">
        
        <div class="essential-card">
          <h3>👗 Dress Code & Attire</h3>
          <ul class="checklist-list">
            <li class="checklist-item">
              <input type="checkbox" checked id="c1">
              <label for="c1"><strong>VIRTÙ & New York Bar:</strong> Smart casual (collared shirt/chic dress, closed shoes for gents, no flip-flops/athletic shorts).</label>
            </li>
            <li class="checklist-item">
              <input type="checkbox" checked id="c2">
              <label for="c2"><strong>DisneySea:</strong> Ultra-comfortable walking shoes & couple Disney headbands!</label>
            </li>
            <li class="checklist-item">
              <input type="checkbox" checked id="c3">
              <label for="c3"><strong>Kusatsu Onsen:</strong> Mountain evening air is crisp (~15°C); bring light cozy jackets or cardigans.</label>
            </li>
          </ul>
        </div>

        <div class="essential-card">
          <h3>📱 Apps & Tickets Checklist</h3>
          <ul class="checklist-list">
            <li class="checklist-item">
              <input type="checkbox" checked id="c4">
              <label for="c4">Tokyo Disney Resort App loaded & logged in for DisneySea Priority Pass.</label>
            </li>
            <li class="checklist-item">
              <input type="checkbox" checked id="c5">
              <label for="c5">Suica / Pasmo card loaded on Apple Wallet (or IC card) for seamless subway transfers.</label>
            </li>
            <li class="checklist-item">
              <input type="checkbox" checked id="c6">
              <label for="c6">JR Limited Express & Shinkansen ticket QR/confirmations ready on phone.</label>
            </li>
          </ul>
        </div>

        <div class="essential-card">
          <h3>♨️ Kusatsu Ryokan Etiquette</h3>
          <ul class="checklist-list">
            <li class="checklist-item">
              <input type="checkbox" checked id="c7">
              <label for="c7">Wash thoroughly at washing stations before entering the onsen baths.</label>
            </li>
            <li class="checklist-item">
              <input type="checkbox" checked id="c8">
              <label for="c8">Fold modesty towel on your head, never soak it in the bath water.</label>
            </li>
            <li class="checklist-item">
              <input type="checkbox" checked id="c9">
              <label for="c9">Wear your provided ryokan yukata for dinner & Yubatake evening strolls!</label>
            </li>
          </ul>
        </div>

      </div>
    </section>

  </main>

  <!-- Mobile Floating Map Button -->
  <button class="floating-map-btn" onclick="scrollToMap()">
    <span>🗺️ Map</span>
  </button>

  <!-- Leaflet Map JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  
  <script>
    // Spots Data
    const spots = [
      {
        day: 1,
        title: "Shane's Burg (シェーンズバーグ 新百合ヶ丘店)",
        category: "Dinner",
        time: "19:00",
        lat: 35.6033,
        lng: 139.5080,
        color: "#e07a7e",
        desc: "Cozy hamburg steak kick-off dinner at Shinyuri Elmi Road 5F.",
        link: "https://tabelog.com/kanagawa/A1405/A140508/14009641/"
      },
      {
        day: 2,
        title: "Sukiyabashi Jiro Roppongi Hills",
        category: "Omakase Lunch",
        time: "13:00",
        lat: 35.6586978,
        lng: 139.7291446,
        color: "#9b51e0",
        desc: "World-class Edomae sushi omakase reservation at Roppongi Hills 3F.",
        link: "https://maps.app.goo.gl/Brh2wvb1fPBVpNn79"
      },
      {
        day: 2,
        title: "Tokyo Tower",
        category: "Sightseeing",
        time: "15:30",
        lat: 35.6585805,
        lng: 139.7454329,
        color: "#9b51e0",
        desc: "Iconic red tower observatory with romantic 360° Tokyo views.",
        link: "https://www.tokyotower.co.jp/en/"
      },
      {
        day: 2,
        title: "VIRTÙ (Four Seasons Otemachi 39F)",
        category: "Cocktails",
        time: "17:30",
        lat: 35.6872,
        lng: 139.7645,
        color: "#9b51e0",
        desc: "Asia's 50 Best Bars: 1920s Parisian salon overlooking Imperial Palace.",
        link: "https://www.fourseasons.com/tokyo-otemachi/dining/lounges/virtu/"
      },
      {
        day: 2,
        title: "Kura Sushi (無添くら寿司)",
        category: "Dinner",
        time: "20:00",
        lat: 35.6719,
        lng: 139.7648,
        color: "#9b51e0",
        desc: "Fun high-tech conveyor sushi & capsule gacha games.",
        link: "https://www.kurasushi.co.jp/mutenkura/"
      },
      {
        day: 3,
        title: "Tokyo DisneySea",
        category: "Theme Park",
        time: "09:00",
        lat: 35.6267,
        lng: 139.8851,
        color: "#2f80ed",
        desc: "World's most romantic Disney park: Mediterranean Harbor & Fantasy Springs.",
        link: "https://www.tokyodisneyresort.jp/en/tds/"
      },
      {
        day: 3,
        title: "S.S. Columbia Dining Room",
        category: "Dinner",
        time: "19:20",
        lat: 35.6238,
        lng: 139.8860,
        color: "#2f80ed",
        desc: "Prime roast beef dining inside the grand luxury ocean liner.",
        link: "https://www.tokyodisneyresort.jp/en/tds/restaurant/detail/431/"
      },
      {
        day: 4,
        title: "Hotel Sakurai Kusatsu (ホテル櫻井)",
        category: "Onsen Ryokan",
        time: "13:30 Check-in",
        lat: 36.6212,
        lng: 138.5996,
        color: "#27ae60",
        desc: "Premier hot spring ryokan with 3 distinct sources and giant outdoor baths.",
        link: "https://www.hotel-sakurai.co.jp/"
      },
      {
        day: 4,
        title: "Yubatake (湯畑)",
        category: "Hot Springs",
        time: "15:30",
        lat: 36.6208,
        lng: 138.5960,
        color: "#27ae60",
        desc: "Steaming hot spring fields, foot baths, and charming yukata strolls.",
        link: "https://maps.google.com/?q=Yubatake+Kusatsu"
      },
      {
        day: 5,
        title: "Wolfgang's Steakhouse Signature Aoyama",
        category: "Steak Lunch",
        time: "14:30",
        lat: 35.6698,
        lng: 139.7180,
        color: "#f2994a",
        desc: "USDA Prime dry-aged porterhouse steaks at THE ARGYLE AOYAMA.",
        link: "https://wolfgangssteakhouse.jp/"
      },
      {
        day: 5,
        title: "Shibuya Crossing & Sky",
        category: "Evening Stroll",
        time: "19:30",
        lat: 35.6595,
        lng: 139.7005,
        color: "#f2994a",
        desc: "Iconic Shibuya Crossing, Miyashita Park, shopping & city lights.",
        link: "https://maps.google.com/?q=Shibuya+Crossing"
      },
      {
        day: 5,
        title: "New York Bar (Park Hyatt Tokyo 52F)",
        category: "Jazz Bar",
        time: "21:30",
        lat: 35.6856,
        lng: 139.6910,
        color: "#f2994a",
        desc: "Iconic Lost in Translation penthouse bar with live jazz & glittering Tokyo views.",
        link: "https://maps.google.com/?q=Park+Hyatt+Tokyo+New+York+Bar"
      }
    ];

    // Initialize Map
    let map = L.map('trip-map', {
      center: [35.68, 139.75],
      zoom: 11,
      zoomControl: true
    });

    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://carto.com/">CARTO</a> & OpenStreetMap',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(map);

    let markers = [];

    // Custom colored pin factory
    function createCustomIcon(color, dayNum) {
      return L.divIcon({
        className: 'custom-map-pin',
        html: `<div style="
          background-color: ${color};
          width: 32px;
          height: 32px;
          border-radius: 50% 50% 50% 0;
          transform: rotate(-45deg);
          border: 2px solid #ffffff;
          box-shadow: 0 4px 10px rgba(0,0,0,0.3);
          display: flex;
          align-items: center;
          justify-content: center;
        ">
          <span style="
            transform: rotate(45deg);
            color: #ffffff;
            font-size: 11px;
            font-weight: 800;
            font-family: var(--font-body);
          ">${dayNum}</span>
        </div>`,
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32]
      });
    }

    // Add Markers
    spots.forEach((spot, idx) => {
      const icon = createCustomIcon(spot.color, spot.day);
      const marker = L.marker([spot.lat, spot.lng], { icon: icon }).addTo(map);
      
      const popupContent = `
        <div class="popup-custom">
          <span class="popup-time">Day ${spot.day} • ${spot.time}</span>
          <h4>${spot.title}</h4>
          <p>${spot.desc}</p>
          <a href="${spot.link}" target="_blank">View Details & Map →</a>
        </div>
      `;
      marker.bindPopup(popupContent);
      marker.spotData = spot;
      markers.push(marker);
    });

    // Kusatsu & Tokyo Route Polylines
    const tokyoCenter = [35.685, 139.75];
    const kusatsuCenter = [36.621, 138.60];
    const tripRoute = L.polyline([
      [35.6033, 139.5080], // Shinyurigaoka
      [35.6587, 139.7291], // Roppongi
      [35.6586, 139.7454], // Tokyo Tower
      [35.6872, 139.7645], // Otemachi
      [35.6267, 139.8851], // DisneySea
      [36.3220, 139.0130], // Takasaki
      [36.5600, 138.6500], // Naganohara
      [36.6212, 138.5996]  // Kusatsu
    ], {
      color: '#9b2c47',
      weight: 3,
      opacity: 0.5,
      dashArray: '6, 8'
    }).addTo(map);

    // Fly to spot
    function flyToSpot(lat, lng, name) {
      if (window.innerWidth <= 1024) {
        scrollToMap();
      }
      map.flyTo([lat, lng], 15, {
        animate: true,
        duration: 1.2
      });

      markers.forEach(m => {
        if (Math.abs(m.getLatLng().lat - lat) < 0.001 && Math.abs(m.getLatLng().lng - lng) < 0.001) {
          setTimeout(() => { m.openPopup(); }, 700);
        }
      });
    }

    function scrollToMap() {
      const el = document.getElementById('trip-map-container');
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    function focusMapAll() {
      const group = new L.featureGroup(markers);
      map.fitBounds(group.getBounds().pad(0.12));
    }

    // Filter markers by Day
    function filterMapByDay(day, btnEl) {
      document.querySelectorAll('.map-tag').forEach(t => t.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');

      const activeMarkers = [];
      markers.forEach(m => {
        if (day === 'all' || m.spotData.day === parseInt(day)) {
          m.addTo(map);
          activeMarkers.push(m);
        } else {
          map.removeLayer(m);
        }
      });

      if (activeMarkers.length > 0) {
        const group = new L.featureGroup(activeMarkers);
        map.fitBounds(group.getBounds().pad(0.2));
      }
    }

    // Switch Day in Timeline
    function switchDay(dayId, tabEl) {
      document.querySelectorAll('.day-tab').forEach(t => t.classList.remove('active'));
      tabEl.classList.add('active');

      if (dayId === 'all') {
        document.querySelectorAll('.day-section').forEach(s => s.style.display = 'block');
        filterMapByDay('all', document.querySelector('.map-filter-tags .map-tag:first-child'));
      } else {
        document.querySelectorAll('.day-section').forEach(s => {
          if (s.id === dayId) {
            s.style.display = 'block';
            s.scrollIntoView({ behavior: 'smooth', block: 'start' });
          } else {
            s.style.display = 'none';
          }
        });
        const dayNum = dayId.replace('day', '');
        const targetTag = Array.from(document.querySelectorAll('.map-tag')).find(el => el.textContent.includes('D' + dayNum));
        filterMapByDay(dayNum, targetTag);
      }
    }

    // Share link copy
    function copyShareLink() {
      navigator.clipboard.writeText(window.location.href);
      const btn = document.getElementById('share-btn-text');
      btn.textContent = '✓ Link Copied!';
      setTimeout(() => {
        btn.textContent = '🔗 Share with Her';
      }, 2500);
    }

    // Fit map initial
    setTimeout(() => {
      focusMapAll();
    }, 400);

  </script>
</body>
</html>
'''

with open('/Users/rondey/japan-trip-itinerary/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('/Users/rondey/tokyo-kusatsu-itinerary.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML files generated successfully!")
