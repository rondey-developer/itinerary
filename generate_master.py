import json
import os

# Complete Master Generator with Full Hour-by-Hour Parallel Planning, Side-by-Side Comparison, and Map
html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Tokyo & Kusatsu Onsen Romance | Master Couple's Itinerary</title>
  
  <!-- Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Playfair+Display:ital,wght@0,500;0,600;0,700;1,400;1,600&display=swap" rel="stylesheet">
  
  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
  
  <style>
    :root {
      --primary: #9e2a4b;
      --primary-dark: #781c34;
      --primary-light: #fdf2f4;
      --accent-gold: #c59b4c;
      --accent-gold-light: #fef9ed;
      --accent-rose: #e68087;
      --bg-body: #faf8f5;
      --bg-card: #ffffff;
      --bg-subtle: #f6f3ed;
      --text-main: #1f1d1b;
      --text-muted: #6e6a64;
      --border-color: #eee6db;
      --shadow-sm: 0 2px 8px rgba(31, 29, 27, 0.04);
      --shadow-md: 0 8px 24px rgba(31, 29, 27, 0.08);
      --radius-sm: 12px;
      --radius-md: 20px;
      --radius-lg: 30px;
      --font-display: 'Playfair Display', Georgia, serif;
      --font-body: 'Plus Jakarta Sans', system-ui, -apple-system, sans-serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: var(--font-body);
      background-color: var(--bg-body);
      color: var(--text-main);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
    }

    /* Hero Banner */
    .hero {
      position: relative;
      background: linear-gradient(135deg, #1f141a 0%, #3e192a 40%, #68233b 80%, #461424 100%);
      color: #fff;
      padding: 60px 24px 50px;
      text-align: center;
      border-radius: 0 0 var(--radius-lg) var(--radius-lg);
      box-shadow: 0 14px 40px rgba(45, 12, 26, 0.3);
      overflow: hidden;
    }

    .hero::before {
      content: "";
      position: absolute;
      inset: 0;
      background: radial-gradient(circle at 18% 25%, rgba(230, 128, 135, 0.3) 0%, transparent 50%),
                  radial-gradient(circle at 82% 75%, rgba(197, 155, 76, 0.25) 0%, transparent 45%);
      pointer-events: none;
    }

    .hero-badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 6px 18px;
      background: rgba(255, 255, 255, 0.14);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(255, 255, 255, 0.22);
      border-radius: 50px;
      font-size: 0.82rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 16px;
      color: #ffd8e0;
    }

    .hero h1 {
      font-family: var(--font-display);
      font-size: clamp(2.2rem, 5vw, 3.8rem);
      font-weight: 700;
      line-height: 1.15;
      margin-bottom: 14px;
      letter-spacing: -0.02em;
    }

    .hero-subtitle {
      font-size: clamp(1rem, 2vw, 1.25rem);
      color: rgba(255, 255, 255, 0.9);
      max-width: 680px;
      margin: 0 auto 28px;
      font-weight: 400;
    }

    .hero-stats {
      display: flex;
      justify-content: center;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 30px;
    }

    .stat-chip {
      background: rgba(255, 255, 255, 0.12);
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.18);
      padding: 8px 16px;
      border-radius: 50px;
      font-size: 0.86rem;
      display: flex;
      align-items: center;
      gap: 7px;
    }

    .stat-chip strong { color: #ffd996; }

    .hero-actions {
      display: flex;
      justify-content: center;
      gap: 14px;
      flex-wrap: wrap;
    }

    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 12px 26px;
      border-radius: 50px;
      font-size: 0.92rem;
      font-weight: 700;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.25s cubic-bezier(0.16, 1, 0.3, 1);
      border: none;
    }

    .btn-gold {
      background: linear-gradient(135deg, #d4a359 0%, #b88339 100%);
      color: #fff;
      box-shadow: 0 4px 16px rgba(184, 131, 57, 0.45);
    }
    .btn-gold:hover {
      transform: translateY(-2px);
      box-shadow: 0 8px 22px rgba(184, 131, 57, 0.55);
    }

    .btn-glass {
      background: rgba(255, 255, 255, 0.18);
      color: #fff;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.3);
    }
    .btn-glass:hover {
      background: rgba(255, 255, 255, 0.28);
      transform: translateY(-2px);
    }

    .container {
      max-width: 1440px;
      margin: 0 auto;
      padding: 24px 20px 80px;
    }

    /* Day Nav */
    .nav-sticky {
      position: sticky;
      top: 12px;
      z-index: 99;
      margin-bottom: 24px;
    }

    .day-tabs {
      display: flex;
      gap: 8px;
      background: rgba(255, 255, 255, 0.94);
      backdrop-filter: blur(20px);
      padding: 8px;
      border-radius: 60px;
      box-shadow: var(--shadow-md);
      border: 1px solid var(--border-color);
      overflow-x: auto;
      scrollbar-width: none;
    }
    .day-tabs::-webkit-scrollbar { display: none; }

    .tab-btn {
      flex: 1;
      min-width: 120px;
      padding: 10px 16px;
      border-radius: 40px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      cursor: pointer;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2px;
      transition: all 0.2s ease;
      white-space: nowrap;
    }

    .tab-btn .tab-date-label {
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      opacity: 0.85;
      font-weight: 700;
    }

    .tab-btn .tab-name-label {
      font-size: 0.88rem;
      font-weight: 700;
    }

    .tab-btn.active {
      background: var(--primary);
      color: #fff;
      box-shadow: 0 4px 14px rgba(158, 42, 75, 0.35);
    }

    .tab-btn:hover:not(.active) {
      background: var(--bg-subtle);
      color: var(--text-main);
    }

    /* Parallel Matrix Table */
    .matrix-section {
      background: #fff;
      border-radius: var(--radius-md);
      border: 1px solid var(--border-color);
      box-shadow: var(--shadow-sm);
      padding: 24px;
      margin-bottom: 30px;
      overflow-x: auto;
    }

    .matrix-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }

    .matrix-header h3 {
      font-family: var(--font-display);
      font-size: 1.3rem;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text-main);
    }

    .matrix-table {
      width: 100%;
      border-collapse: collapse;
      min-width: 800px;
      font-size: 0.85rem;
    }

    .matrix-table th {
      background: #fbf7f1;
      padding: 12px 14px;
      text-align: left;
      font-weight: 700;
      color: #333;
      border-bottom: 2px solid var(--border-color);
    }

    .matrix-table td {
      padding: 12px 14px;
      border-bottom: 1px solid #f2ede4;
      vertical-align: top;
    }

    .matrix-table tr:hover td {
      background: #fffcf8;
    }

    .pill-day {
      display: inline-block;
      padding: 3px 8px;
      border-radius: 6px;
      font-weight: 800;
      font-size: 0.75rem;
      color: #fff;
    }

    /* Grid Layout */
    .main-grid {
      display: grid;
      grid-template-columns: 1.05fr 0.95fr;
      gap: 30px;
      align-items: start;
    }

    @media (max-width: 1080px) {
      .main-grid { grid-template-columns: 1fr; }
    }

    /* Map Box */
    .map-wrapper {
      position: sticky;
      top: 96px;
    }

    .map-card-box {
      background: var(--bg-card);
      border-radius: var(--radius-md);
      border: 1px solid var(--border-color);
      box-shadow: var(--shadow-md);
      overflow: hidden;
    }

    .map-toolbar {
      padding: 14px 20px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      background: #faf7f2;
      border-bottom: 1px solid var(--border-color);
      flex-wrap: wrap;
      gap: 10px;
    }

    .map-header-title {
      font-size: 0.95rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--text-main);
    }

    .map-filters {
      display: flex;
      gap: 6px;
      font-size: 0.76rem;
    }

    .filter-chip {
      padding: 4px 12px;
      border-radius: 20px;
      background: #fff;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      cursor: pointer;
      font-weight: 700;
      transition: all 0.15s ease;
    }
    .filter-chip.active {
      background: var(--text-main);
      color: #fff;
      border-color: var(--text-main);
    }

    #trip-map {
      height: 580px;
      width: 100%;
      background: #eef2f5;
    }

    @media (max-width: 1080px) {
      #trip-map { height: 420px; }
      .map-wrapper {
        position: relative;
        top: 0;
        margin-bottom: 24px;
      }
    }

    .map-tip-bar {
      padding: 10px 18px;
      font-size: 0.8rem;
      color: var(--text-muted);
      background: #fff;
      border-top: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    /* Stream */
    .itinerary-stream {
      display: flex;
      flex-direction: column;
      gap: 28px;
    }

    .day-block {
      background: var(--bg-card);
      border-radius: var(--radius-md);
      border: 1px solid var(--border-color);
      box-shadow: var(--shadow-sm);
      padding: 26px;
      scroll-margin-top: 105px;
      transition: border-color 0.25s ease;
    }

    .day-block:hover { border-color: #dfd5c7; }

    .day-title-row {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      margin-bottom: 20px;
      padding-bottom: 16px;
      border-bottom: 2px dashed var(--border-color);
      gap: 12px;
      flex-wrap: wrap;
    }

    .day-badge-wrap {
      display: flex;
      align-items: center;
      gap: 14px;
    }

    .day-badge {
      width: 56px;
      height: 56px;
      border-radius: 18px;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      color: #fff;
      box-shadow: var(--shadow-sm);
      flex-shrink: 0;
    }

    .badge-d1 { background: linear-gradient(135deg, #e68087 0%, #c44750 100%); }
    .badge-d2 { background: linear-gradient(135deg, #a05be8 0%, #6f2eb5 100%); }
    .badge-d3 { background: linear-gradient(135deg, #348efc 0%, #155bc4 100%); }
    .badge-d4 { background: linear-gradient(135deg, #10b981 0%, #067a53 100%); }
    .badge-d5 { background: linear-gradient(135deg, #f59e0b 0%, #c47605 100%); }

    .day-badge .num { font-size: 1.25rem; line-height: 1; }
    .day-badge .sub { font-size: 0.62rem; text-transform: uppercase; letter-spacing: 0.08em; opacity: 0.9; }

    .day-headings h2 {
      font-family: var(--font-display);
      font-size: 1.45rem;
      font-weight: 700;
      color: var(--text-main);
      line-height: 1.2;
    }

    .day-headings p {
      font-size: 0.88rem;
      color: var(--text-muted);
      margin-top: 3px;
    }

    .day-theme-chip {
      font-size: 0.78rem;
      font-weight: 700;
      padding: 6px 14px;
      border-radius: 20px;
      background: var(--bg-subtle);
      color: var(--text-main);
      border: 1px solid var(--border-color);
      white-space: nowrap;
    }

    /* Hour-by-Hour Timeline Items */
    .timeline-schedule {
      display: flex;
      flex-direction: column;
      gap: 16px;
      position: relative;
    }

    .timeline-schedule::before {
      content: "";
      position: absolute;
      left: 21px;
      top: 18px;
      bottom: 24px;
      width: 2px;
      background: #eee8de;
      z-index: 0;
    }

    .timeline-entry {
      position: relative;
      margin-left: 50px;
      background: #fff;
      border: 1px solid var(--border-color);
      border-radius: var(--radius-sm);
      padding: 18px 20px;
      box-shadow: var(--shadow-sm);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
      cursor: pointer;
    }

    .timeline-entry:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-md);
      border-color: var(--accent-rose);
    }

    .entry-bullet {
      position: absolute;
      left: -50px;
      top: 18px;
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: #fff;
      border: 2.5px solid var(--primary);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.95rem;
      z-index: 1;
      box-shadow: 0 2px 6px rgba(0,0,0,0.08);
    }

    .entry-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 8px;
      flex-wrap: wrap;
      gap: 6px;
    }

    .entry-time {
      font-size: 0.82rem;
      font-weight: 800;
      color: var(--primary);
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: var(--primary-light);
      padding: 3px 10px;
      border-radius: 6px;
    }

    .entry-status {
      font-size: 0.72rem;
      font-weight: 700;
      padding: 3px 9px;
      border-radius: 6px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .status-confirmed { background: #e6f7ef; color: #0b784a; border: 1px solid #b3e6cc; }
    .status-transit { background: #e8f0fe; color: #1a73e8; border: 1px solid #aecbfa; }
    .status-highlight { background: #fdf5e6; color: #a86500; border: 1px solid #f9e2b3; }

    .entry-body h4 {
      font-size: 1.12rem;
      font-weight: 800;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 3px;
    }

    .entry-subtitle {
      font-size: 0.84rem;
      color: var(--text-muted);
      margin-bottom: 10px;
    }

    .entry-desc {
      font-size: 0.88rem;
      color: #45423f;
      margin-bottom: 12px;
      line-height: 1.55;
    }

    /* Sub-steps inside an activity */
    .mini-steps-list {
      background: var(--bg-subtle);
      border-radius: 8px;
      padding: 10px 14px;
      margin-bottom: 12px;
      font-size: 0.82rem;
      color: #4b4845;
      display: flex;
      flex-direction: column;
      gap: 6px;
      border-left: 3px solid var(--accent-gold);
    }

    .mini-step-item {
      display: flex;
      gap: 8px;
      align-items: baseline;
    }

    .mini-step-item strong {
      color: #1e1b19;
      white-space: nowrap;
    }

    .entry-footer {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-top: 12px;
      border-top: 1px solid #f4f0e9;
      font-size: 0.82rem;
      flex-wrap: wrap;
      gap: 10px;
    }

    .entry-location {
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 5px;
      font-size: 0.8rem;
    }

    .entry-actions {
      display: flex;
      gap: 8px;
    }

    .pill-link {
      color: var(--primary);
      text-decoration: none;
      font-weight: 700;
      font-size: 0.78rem;
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 4px 10px;
      border-radius: 6px;
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      transition: all 0.15s ease;
    }
    .pill-link:hover {
      background: var(--primary-light);
      border-color: var(--primary);
    }

    /* Transit Timetable Schedule Box */
    .transit-guide-box {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: var(--radius-sm);
      padding: 18px;
      margin: 16px 0;
      box-shadow: 0 2px 6px rgba(0,0,0,0.02);
    }

    .transit-guide-title {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding-bottom: 12px;
      margin-bottom: 14px;
      border-bottom: 1px solid #e2e8f0;
      flex-wrap: wrap;
      gap: 6px;
    }

    .transit-node {
      display: flex;
      align-items: flex-start;
      gap: 14px;
      position: relative;
      padding-bottom: 16px;
    }

    .transit-node:last-child { padding-bottom: 0; }

    .transit-node::after {
      content: "";
      position: absolute;
      left: 17px;
      top: 26px;
      bottom: -4px;
      width: 2px;
      background: #cbd5e1;
    }
    .transit-node:last-child::after { display: none; }

    .node-time-box {
      font-family: monospace;
      font-size: 0.88rem;
      font-weight: 800;
      color: #0f172a;
      width: 50px;
      text-align: right;
      line-height: 1.3;
    }
    .node-time-box small {
      font-size: 0.74rem;
      color: #64748b;
      font-weight: 600;
    }

    .node-dot {
      width: 14px;
      height: 14px;
      border-radius: 50%;
      background: #3b82f6;
      border: 2px solid #fff;
      box-shadow: 0 0 0 2px #3b82f6;
      margin-top: 4px;
      z-index: 1;
      flex-shrink: 0;
    }
    .node-dot.start { background: #10b981; box-shadow: 0 0 0 2px #10b981; }
    .node-dot.end { background: #ef4444; box-shadow: 0 0 0 2px #ef4444; }

    .node-content { flex: 1; }
    .node-name { font-weight: 800; font-size: 0.94rem; color: #1e293b; }
    .node-sub {
      font-size: 0.8rem;
      color: #64748b;
      margin-top: 3px;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
    }

    .tag-train {
      background: #e2e8f0;
      padding: 2px 7px;
      border-radius: 4px;
      font-size: 0.74rem;
      color: #334155;
      font-weight: 700;
    }

    .tag-price { font-size: 0.75rem; color: #047857; font-weight: 700; }

    /* Romantic Banner Inside Day */
    .romance-highlight-callout {
      background: linear-gradient(135deg, #fff8f0 0%, #feeddc 100%);
      border: 1px solid #fed7aa;
      border-radius: var(--radius-sm);
      padding: 16px 20px;
      margin-top: 18px;
      display: flex;
      gap: 14px;
      align-items: flex-start;
    }

    .romance-highlight-callout .icon-heart { font-size: 1.5rem; line-height: 1; }
    .romance-highlight-callout h4 { font-size: 0.9rem; font-weight: 800; color: #9a3412; margin-bottom: 3px; }
    .romance-highlight-callout p { font-size: 0.84rem; color: #7c2d12; line-height: 1.5; }

    /* Quick Survival Section */
    .survival-section {
      margin-top: 40px;
      background: var(--bg-card);
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      box-shadow: var(--shadow-sm);
      padding: 30px;
    }

    .survival-section h2 {
      font-family: var(--font-display);
      font-size: 1.45rem;
      margin-bottom: 22px;
      display: flex;
      align-items: center;
      gap: 10px;
      color: var(--text-main);
    }

    .survival-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
      gap: 20px;
    }

    .survival-card {
      background: var(--bg-subtle);
      border-radius: var(--radius-sm);
      padding: 20px;
      border: 1px solid #ece4d8;
    }

    .survival-card h3 {
      font-size: 1rem;
      font-weight: 800;
      margin-bottom: 12px;
      display: flex;
      align-items: center;
      gap: 8px;
      color: var(--primary);
    }

    .checklist {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 10px;
    }

    .checklist-row {
      display: flex;
      align-items: flex-start;
      gap: 10px;
      font-size: 0.86rem;
      color: #3b3835;
      cursor: pointer;
    }

    .checklist-row input[type="checkbox"] {
      width: 17px;
      height: 17px;
      margin-top: 2px;
      accent-color: var(--primary);
      cursor: pointer;
    }

    /* Floating mobile map */
    .mobile-map-float {
      display: none;
      position: fixed;
      bottom: 24px;
      right: 24px;
      z-index: 999;
      background: var(--primary);
      color: #fff;
      padding: 12px 22px;
      border-radius: 50px;
      box-shadow: 0 8px 24px rgba(158, 42, 75, 0.45);
      font-weight: 800;
      border: none;
      align-items: center;
      gap: 8px;
      cursor: pointer;
    }

    @media (max-width: 1080px) {
      .mobile-map-float { display: flex; }
    }

    /* Popup */
    .leaflet-popup-content-wrapper {
      border-radius: 16px;
      padding: 2px;
      box-shadow: 0 12px 30px rgba(0,0,0,0.18);
    }

    .map-popup-inner {
      font-family: var(--font-body);
      max-width: 250px;
    }

    .map-popup-inner h4 {
      font-size: 0.98rem;
      font-weight: 800;
      color: #1a1816;
      margin-bottom: 2px;
    }

    .map-popup-inner .pop-time {
      font-size: 0.78rem;
      color: var(--primary);
      font-weight: 800;
      margin-bottom: 6px;
      display: block;
    }

    .map-popup-inner p {
      font-size: 0.8rem;
      color: #555;
      line-height: 1.4;
      margin-bottom: 8px;
    }

    .map-popup-inner a {
      display: inline-block;
      font-size: 0.76rem;
      font-weight: 700;
      color: #fff;
      background: var(--primary);
      padding: 4px 12px;
      border-radius: 6px;
      text-decoration: none;
    }

    .toast-msg {
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: #1e293b;
      color: #fff;
      padding: 12px 24px;
      border-radius: 50px;
      box-shadow: 0 10px 30px rgba(0,0,0,0.25);
      font-size: 0.88rem;
      font-weight: 600;
      z-index: 1000;
      display: none;
      align-items: center;
      gap: 8px;
    }
  </style>
</head>
<body>

  <!-- Hero Banner -->
  <header class="hero">
    <div class="hero-badge">
      <span>✨ Our Tokyo & Kusatsu Onsen Escape ✨</span>
    </div>
    <h1>Romantic Japan Itinerary</h1>
    <p class="hero-subtitle">Five unforgettable days of world-class Michelin sushi, Disney dreams, scenic alpine hot springs, USDA prime steak, and cinematic skyline jazz.</p>
    
    <div class="hero-stats">
      <div class="stat-chip">
        <span>📅</span>
        <span>Sep 25 – Sep 29, 2026</span>
      </div>
      <div class="stat-chip">
        <span>🍣</span>
        <span>Sukiyabashi Jiro & Kura Sushi</span>
      </div>
      <div class="stat-chip">
        <span>🏰</span>
        <span>DisneySea & S.S. Columbia</span>
      </div>
      <div class="stat-chip">
        <span>♨️</span>
        <span>Hotel Sakurai Kusatsu Onsen</span>
      </div>
      <div class="stat-chip">
        <span>🥩</span>
        <span>Wolfgang's & New York Bar</span>
      </div>
    </div>

    <div class="hero-actions">
      <a href="#trip-map-container" class="btn btn-gold" onclick="focusAllPins()">
        <span>🗺️ Interactive Map</span>
      </a>
      <button class="btn btn-glass" onclick="downloadCalendarFile()">
        <span>📅 Add to Calendar (.ics)</span>
      </button>
      <button class="btn btn-glass" onclick="window.print()">
        <span>🖨️ Save as PDF / Print</span>
      </button>
      <button class="btn btn-glass" onclick="copyShareURL()">
        <span id="share-label">🔗 Share with Her</span>
      </button>
    </div>
  </header>

  <!-- Sticky Day Selector -->
  <div class="nav-sticky">
    <div class="container" style="padding-top:0; padding-bottom:0;">
      <nav class="day-tabs">
        <button class="tab-btn active" onclick="activateDay('all', this)">
          <span class="tab-date-label">Overview</span>
          <span class="tab-name-label">✨ All 5 Days</span>
        </button>
        <button class="tab-btn" onclick="activateDay('day1', this)">
          <span class="tab-date-label">Fri Sep 25</span>
          <span class="tab-name-label">Day 1 • Warm-up</span>
        </button>
        <button class="tab-btn" onclick="activateDay('day2', this)">
          <span class="tab-date-label">Sat Sep 26</span>
          <span class="tab-name-label">Day 2 • Jiro & Tower</span>
        </button>
        <button class="tab-btn" onclick="activateDay('day3', this)">
          <span class="tab-date-label">Sun Sep 27</span>
          <span class="tab-name-label">Day 3 • DisneySea</span>
        </button>
        <button class="tab-btn" onclick="activateDay('day4', this)">
          <span class="tab-date-label">Mon Sep 28</span>
          <span class="tab-name-label">Day 4 • Kusatsu Onsen</span>
        </button>
        <button class="tab-btn" onclick="activateDay('day5', this)">
          <span class="tab-date-label">Tue Sep 29</span>
          <span class="tab-name-label">Day 5 • Steak & Skyline</span>
        </button>
      </nav>
    </div>
  </div>

  <main class="container">

    <!-- Parallel Comparison Matrix -->
    <section class="matrix-section">
      <div class="matrix-header">
        <h3><span>📊</span> 5-Day Parallel Plan at a Glance</h3>
        <span style="font-size:0.8rem; color:var(--text-muted);">Side-by-side comparison across all days</span>
      </div>
      <table class="matrix-table">
        <thead>
          <tr>
            <th>Day / Date</th>
            <th>Morning</th>
            <th>Lunch / Early Afternoon</th>
            <th>Late Afternoon / Golden Hour</th>
            <th>Dinner (Bookings)</th>
            <th>Nightcap / Late</th>
            <th>Attire & Vibe</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td><span class="pill-day badge-d1">Day 1 • 9/25 (Fri)</span></td>
            <td>Arrival / City check-in</td>
            <td>Light lunch & settle in</td>
            <td>Freshen up & tea</td>
            <td><strong>19:00 Shane's Burg</strong> (Shinyuri Elmi Road)</td>
            <td>Relaxed evening walk</td>
            <td>Casual cozy comfort</td>
          </tr>
          <tr>
            <td><span class="pill-day badge-d2">Day 2 • 9/26 (Sat)</span></td>
            <td>Keyakizaka tree stroll</td>
            <td><strong>13:00 Sukiyabashi Jiro</strong> (Omakase Sushi)</td>
            <td>15:30 Tokyo Tower & <strong>17:30 VIRTÙ</strong> (39F)</td>
            <td><strong>20:00 Kura Sushi</strong> (Bikkura-Pon)</td>
            <td>Roppongi / Ginza nightlights</td>
            <td>Smart casual (collared / chic)</td>
          </tr>
          <tr>
            <td><span class="pill-day badge-d3">Day 3 • 9/27 (Sun)</span></td>
            <td><strong>09:00 DisneySea Entry</strong> & Priority Pass</td>
            <td>Fantasy Springs & Venetian Gondolas</td>
            <td>Soaring & American Waterfront</td>
            <td><strong>19:20 S.S. Columbia</strong> (Luxury liner)</td>
            <td>20:30 Believe! Fireworks & lasers</td>
            <td>Walking sneakers & Disney ears</td>
          </tr>
          <tr>
            <td><span class="pill-day badge-d4">Day 4 • 9/28 (Mon)</span></td>
            <td>08:55 Yurigaoka $\rightarrow$ Akabane Express</td>
            <td>12:53 Arrive Kusatsu & Ryokan Bento</td>
            <td>13:30 Hotel Sakurai onsen & 15:30 Yubatake</td>
            <td>18:30 Ryokan Kaiseki Banquet</td>
            <td>Rotenburo hot springs under stars</td>
            <td>Cozy travel wear & Yukata</td>
          </tr>
          <tr>
            <td><span class="pill-day badge-d5">Day 5 • 9/29 (Tue)</span></td>
            <td>09:20 Bus $\rightarrow$ Shinkansen to Tokyo</td>
            <td><strong>14:30 Wolfgang's Signature</strong> (Aoyama)</td>
            <td>Omotesando boutique stroll</td>
            <td><strong>19:30 Shibuya Scramble</strong> & Miyashita Park</td>
            <td><strong>21:30 New York Bar 52F</strong> (Live jazz)</td>
            <td>Smart upscale city wear</td>
          </tr>
        </tbody>
      </table>
    </section>

    <!-- Main Grid: Timeline + Map -->
    <div class="main-grid">
      
      <!-- Detailed Hour-by-Hour Timeline Stream -->
      <section class="itinerary-stream">
        
        <!-- DAY 1 -->
        <article class="day-block" id="day1">
          <div class="day-title-row">
            <div class="day-badge-wrap">
              <div class="day-badge badge-d1">
                <span class="num">01</span>
                <span class="sub">Day</span>
              </div>
              <div class="day-headings">
                <h2>Friday, September 25</h2>
                <p>Welcome Dinner & Cozy Kick-off</p>
              </div>
            </div>
            <span class="day-theme-chip">🍴 Handcrafted Hamburg</span>
          </div>

          <div class="timeline-schedule">
            <!-- 17:00 Prep -->
            <div class="timeline-entry">
              <div class="entry-bullet">🧳</div>
              <div class="entry-header">
                <span class="entry-time">17:00 – 18:30</span>
                <span class="entry-status status-highlight">Arrival & Prep</span>
              </div>
              <div class="entry-body">
                <h4>Unwind, Freshen Up & Settle In</h4>
                <div class="entry-subtitle">Base Accommodation • Easy Start</div>
                <p class="entry-desc">Unpack comfortably, take a warm shower after travel, and slip into comfortable casual chic attire.</p>
                <div class="mini-steps-list">
                  <div class="mini-step-item"><strong>18:35:</strong> Head towards Shinyurigaoka Station on the Odakyu Line.</div>
                  <div class="mini-step-item"><strong>18:50:</strong> Direct connection to Shinyuri Elmi Road shopping center, take elevator to 5F.</div>
                </div>
              </div>
            </div>

            <!-- 19:00 Shane's Burg -->
            <div class="timeline-entry" onclick="flyToSpot(35.6033, 139.5080, 'Shane\'s Burg Shinyurigaoka')">
              <div class="entry-bullet">🥩</div>
              <div class="entry-header">
                <span class="entry-time">19:00 – 20:30</span>
                <span class="entry-status status-confirmed">✓ Dinner Reserved</span>
              </div>
              <div class="entry-body">
                <h4>Shane's Burg (シェーンズバーグ 新百合ヶ丘店)</h4>
                <div class="entry-subtitle">Shinyuri Elmi Road 5F • Handcrafted Charcoal Hamburg Steak</div>
                <p class="entry-desc">
                  Handcrafted premium Japanese-American hamburger steaks prepared fresh daily in the kitchen and grilled over open flame. Juicy, comforting, and relaxed atmosphere to kick off the trip together.
                </p>
                <div class="mini-steps-list">
                  <div class="mini-step-item"><strong>Recommended Order:</strong> Signature Hamburg Steak with Demi-Glace or Garlic Onion Sauce, melted cheese topping, crispy wedges, and draft beer / highball.</div>
                  <div class="mini-step-item"><strong>Cost:</strong> Approx. ¥1,500 – ¥2,500 per person.</div>
                </div>
              </div>
              <div class="entry-footer">
                <span class="entry-location">📍 Shinyuri Elmi Road 5F (Shinyurigaoka Station)</span>
                <div class="entry-actions">
                  <a href="https://tabelog.com/kanagawa/A1405/A140508/14009641/" target="_blank" class="pill-link" onclick="event.stopPropagation()">📖 Tabelog</a>
                  <a href="https://maps.google.com/?q=Shane's+Burg+Shin-Yurigaoka" target="_blank" class="pill-link" onclick="event.stopPropagation()">🗺️ Google Maps</a>
                </div>
              </div>
            </div>

            <!-- 20:45 Evening Stroll -->
            <div class="timeline-entry">
              <div class="entry-bullet">🍇</div>
              <div class="entry-header">
                <span class="entry-time">20:45 – 21:30</span>
                <span class="entry-status status-highlight">Sweet Treat</span>
              </div>
              <div class="entry-body">
                <h4>Depachika Sweets & Early Rest</h4>
                <div class="entry-subtitle">Seasonal Fruit Treat • Good Night's Sleep</div>
                <p class="entry-desc">Pick up premium seasonal Japanese fruit (such as Shine Muscat grapes) or parfaits from the department store basement, then rest up for tomorrow's headline Jiro sushi omakase!</p>
              </div>
            </div>
          </div>

          <div class="romance-highlight-callout">
            <span class="icon-heart">✨</span>
            <div>
              <h4>Couple's Sweet Reminder</h4>
              <p>Keep tonight easy and unhurried. Tomorrow begins our Tokyo glamour series starting with Sukiyabashi Jiro at 13:00.</p>
            </div>
          </div>
        </article>

        <!-- DAY 2 -->
        <article class="day-block" id="day2">
          <div class="day-title-row">
            <div class="day-badge-wrap">
              <div class="day-badge badge-d2">
                <span class="num">02</span>
                <span class="sub">Day</span>
              </div>
              <div class="day-headings">
                <h2>Saturday, September 26</h2>
                <p>Michelin Omakase, Tokyo Tower & Sky Bar</p>
              </div>
            </div>
            <span class="day-theme-chip">🍣 Glamour & Skylines</span>
          </div>

          <div class="timeline-schedule">
            <!-- 12:00 Roppongi Hills Stroll -->
            <div class="timeline-entry">
              <div class="entry-bullet">📸</div>
              <div class="entry-header">
                <span class="entry-time">12:15 – 12:55</span>
                <span class="entry-status status-highlight">Keyakizaka Stroll</span>
              </div>
              <div class="entry-body">
                <h4>Roppongi Hills & Keyakizaka Dori Stroll</h4>
                <div class="entry-subtitle">Designer Avenue • Iconic Photo Angle</div>
                <p class="entry-desc">Arrive at Roppongi Hills early. Walk along Keyakizaka Dori — this tree-lined luxury boulevard offers a postcard view of Tokyo Tower framed between the buildings.</p>
              </div>
            </div>

            <!-- 13:00 Sukiyabashi Jiro -->
            <div class="timeline-entry" onclick="flyToSpot(35.6586978, 139.7291446, 'Sukiyabashi Jiro Roppongi Hills')">
              <div class="entry-bullet">🍣</div>
              <div class="entry-header">
                <span class="entry-time">13:00 – 14:15</span>
                <span class="entry-status status-confirmed">✓ Confirmed 1:00 PM Booking</span>
              </div>
              <div class="entry-body">
                <h4>Sukiyabashi Jiro Roppongi Hills (すきやばし 次郎)</h4>
                <div class="entry-subtitle">Roppongi Hills Keyakizaka Dori 3F • Legendary Edomae Sushi</div>
                <p class="entry-desc">
                  An unforgettable Edomae sushi omakase crafted by master chef Takashi Ono (son of legendary Jiro Ono). Masterful knife work, impeccable warm vinegared rice, and world-class intimacy.
                </p>
                <div class="mini-steps-list">
                  <div class="mini-step-item"><strong>Etiquette:</strong> Eat each piece of sushi within seconds of being served (by hand or chopstick). Chef brushes exact soy sauce glaze.</div>
                  <div class="mini-step-item"><strong>Atmosphere:</strong> Intimate 8-seat cedar counter.</div>
                </div>
              </div>
              <div class="entry-footer">
                <span class="entry-location">📍 Roppongi Hills Keyakizaka Dori 3F</span>
                <div class="entry-actions">
                  <a href="https://maps.app.goo.gl/Brh2wvb1fPBVpNn79" target="_blank" class="pill-link" onclick="event.stopPropagation()">🗺️ Google Maps</a>
                </div>
              </div>
            </div>

            <!-- 15:30 Tokyo Tower -->
            <div class="timeline-entry" onclick="flyToSpot(35.6585805, 139.7454329, 'Tokyo Tower')">
              <div class="entry-bullet">🗼</div>
              <div class="entry-header">
                <span class="entry-time">15:30 – 17:00</span>
                <span class="entry-status status-highlight">Romantic Sightseeing</span>
              </div>
              <div class="entry-body">
                <h4>Tokyo Tower Observatory (東京タワー)</h4>
                <div class="entry-subtitle">Main Deck 150m & Skywalk Glass Floors</div>
                <p class="entry-desc">
                  Take a 10-minute taxi from Roppongi Hills to Tokyo Tower. Experience 360-degree panoramic views of Tokyo Bay, step on the transparent glass floor looking 145m down, and visit the romantic Tower Shrine.
                </p>
              </div>
              <div class="entry-footer">
                <span class="entry-location">📍 Shiba-koen, Minato-ku</span>
                <div class="entry-actions">
                  <a href="https://www.tokyotower.co.jp/en/" target="_blank" class="pill-link" onclick="event.stopPropagation()">🌐 Official Site</a>
                </div>
              </div>
            </div>

            <!-- 17:30 VIRTU -->
            <div class="timeline-entry" onclick="flyToSpot(35.6872, 139.7645, 'VIRTÙ Cocktail Bar')">
              <div class="entry-bullet">🍸</div>
              <div class="entry-header">
                <span class="entry-time">17:30 – 19:15</span>
                <span class="entry-status status-highlight">Asia's 50 Best Bars</span>
              </div>
              <div class="entry-body">
                <h4>VIRTÙ (Four Seasons Hotel Tokyo at Otemachi 39F)</h4>
                <div class="entry-subtitle">1920s Parisian Salon Aesthetics Overlooking Imperial Palace</div>
                <p class="entry-desc">
                  Soaring floor-to-ceiling windows overlooking the Imperial Palace gardens and Tokyo skyline. Savor world-class cocktails blending French and Japanese sensibilities during Tokyo's golden sunset hour.
                </p>
                <div class="mini-steps-list">
                  <div class="mini-step-item"><strong>Signature Cocktails:</strong> <em>Smoked Ume Fashioned</em> (hinoki smoke, Japanese whisky, plum bitters), French cognac vintage collection.</div>
                  <div class="mini-step-item"><strong>Dress Code:</strong> Smart casual (collared shirt, no open sandals/shorts for gents).</div>
                </div>
              </div>
              <div class="entry-footer">
                <span class="entry-location">📍 1-2-1 Otemachi (Direct underground access)</span>
                <div class="entry-actions">
                  <a href="https://www.fourseasons.com/tokyo-otemachi/dining/lounges/virtu/" target="_blank" class="pill-link" onclick="event.stopPropagation()">🍸 Cocktail Menu</a>
                </div>
              </div>
            </div>

            <!-- 20:00 Kura Sushi -->
            <div class="timeline-entry" onclick="flyToSpot(35.6719, 139.7648, 'Muten Kura Sushi')">
              <div class="entry-bullet">🍣</div>
              <div class="entry-header">
                <span class="entry-time">20:00 – 21:30</span>
                <span class="entry-status status-confirmed">Fun Casual Dinner</span>
              </div>
              <div class="entry-body">
                <h4>Kura Sushi / Muten Kura (無添くら寿司)</h4>
                <div class="entry-subtitle">Additive-Free Conveyor-Belt Sushi & Bikkura-Pon Game!</div>
                <p class="entry-desc">
                  A delightful, lighthearted contrast to lunch! Enjoy fresh conveyor-belt sushi where slipping every 5 empty plates into the table slot triggers the animated Bikkura-Pon capsule lottery on your screen.
                </p>
              </div>
              <div class="entry-footer">
                <span class="entry-location">📍 Central Tokyo Flagship / Ginza</span>
                <div class="entry-actions">
                  <a href="https://www.kurasushi.co.jp/mutenkura/" target="_blank" class="pill-link" onclick="event.stopPropagation()">🌐 Official Site</a>
                </div>
              </div>
            </div>
          </div>
        </article>

        <!-- DAY 3 -->
        <article class="day-block" id="day3">
          <div class="day-title-row">
            <div class="day-badge-wrap">
              <div class="day-badge badge-d3">
                <span class="num">03</span>
                <span class="sub">Day</span>
              </div>
              <div class="day-headings">
                <h2>Sunday, September 27</h2>
                <p>Tokyo DisneySea & S.S. Columbia Dining</p>
              </div>
            </div>
            <span class="day-theme-chip">🏰 Disney Magic & Romance</span>
          </div>

          <div class="timeline-schedule">
            <!-- 08:30 Monorail & Entry -->
            <div class="timeline-entry" onclick="flyToSpot(35.6267, 139.8851, 'Tokyo DisneySea')">
              <div class="entry-bullet">🏰</div>
              <div class="entry-header">
                <span class="entry-time">09:00 AM Entry</span>
                <span class="entry-status status-confirmed">Full Day Pass</span>
              </div>
              <div class="entry-body">
                <h4>Tokyo DisneySea (東京ディズニーシー)</h4>
                <div class="entry-subtitle">Mediterranean Harbor • Fantasy Springs • Venetian Gondolas</div>
                <p class="entry-desc">
                  Universally hailed as the most romantic Disney park in the world. Experience the brand new Fantasy Springs, Soaring: Fantastic Flight, and gentle Venetian Gondolas.
                </p>
                <div class="mini-steps-list">
                  <div class="mini-step-item"><strong>Rope Drop Strategy (09:00):</strong> Immediately open Tokyo Disney Resort App $\rightarrow$ book Disney Premier Access (DPA) / Standby Pass for Fantasy Springs (Frozen / Rapunzel / Peter Pan).</div>
                  <div class="mini-step-item"><strong>Priority Pass:</strong> Grab 40th Anniversary Pass for Soaring: Fantastic Flight or Tower of Terror.</div>
                </div>
              </div>
              <div class="entry-footer">
                <span class="entry-location">📍 Maihama Station (Disney Resort Line)</span>
                <div class="entry-actions">
                  <a href="https://www.tokyodisneyresort.jp/en/tds/" target="_blank" class="pill-link" onclick="event.stopPropagation()">📱 Disney App</a>
                </div>
              </div>
            </div>

            <!-- 13:00 Fantasy Springs -->
            <div class="timeline-entry">
              <div class="entry-bullet">⛵</div>
              <div class="entry-header">
                <span class="entry-time">13:00 – 17:30</span>
                <span class="entry-status status-highlight">Fantasy Springs & Gondolas</span>
              </div>
              <div class="entry-body">
                <h4>Venetian Gondola & Fairy-Tale Lands</h4>
                <div class="entry-subtitle">Romantic Canals & Immersive Worlds</div>
                <p class="entry-desc">Take a scenic couple ride on the Venetian Gondolas with gondoliers singing Italian serenades, followed by magical fairy-tale adventures in Frozen Kingdom and Rapunzel's Lantern Festival.</p>
              </div>
            </div>

            <!-- 19:20 S.S. Columbia -->
            <div class="timeline-entry" onclick="flyToSpot(35.6238, 139.8860, 'S.S. Columbia Dining Room')">
              <div class="entry-bullet">🛳️</div>
              <div class="entry-header">
                <span class="entry-time">19:20 (7:20 PM)</span>
                <span class="entry-status status-confirmed">✓ Priority Seating Booked</span>
              </div>
              <div class="entry-body">
                <h4>S.S. Columbia Dining Room (S.S.コロンビア)</h4>
                <div class="entry-subtitle">Grand Edwardian Dining Salon aboard the Luxury 1912 Ocean Liner</div>
                <p class="entry-desc">
                  Step into the B-Deck grand dining room of the majestic luxury steamship docked at the American Waterfront. Enjoy prime roast beef course dinners, fine wine, chandelier glow, and romantic maritime nostalgia.
                </p>
                <div class="mini-steps-list">
                  <div class="mini-step-item"><strong>Recommended Menu:</strong> Roast Beef & Grilled Sirloin Course, seasonal appetizer platter, hot crusty rolls, paired with red wine.</div>
                  <div class="mini-step-item"><strong>Romantic Touch:</strong> Step onto the ship's outdoor promenade deck before dinner for panoramic sunset harbor photos.</div>
                </div>
              </div>
              <div class="entry-footer">
                <span class="entry-location">📍 American Waterfront S.S. Columbia 3F, DisneySea</span>
                <div class="entry-actions">
                  <a href="https://www.tokyodisneyresort.jp/en/tds/restaurant/detail/431/" target="_blank" class="pill-link" onclick="event.stopPropagation()">🍽️ Restaurant Details</a>
                </div>
              </div>
            </div>

            <!-- 20:30 Believe! -->
            <div class="timeline-entry">
              <div class="entry-bullet">🎆</div>
              <div class="entry-header">
                <span class="entry-time">20:30 – 21:00</span>
                <span class="entry-status status-highlight">Night Spectacular</span>
              </div>
              <div class="entry-body">
                <h4>Believe! Sea of Dreams (ビリーヴ！)</h4>
                <div class="entry-subtitle">Breathtaking Laser, Projection & Fireworks Show</div>
                <p class="entry-desc">Watch from Mediterranean Harbor as illuminated boats, lasers on Hotel MiraCosta, pyrotechnics, and stirring Disney music bring the day to a magical crescendo.</p>
              </div>
            </div>
          </div>
        </article>

        <!-- DAY 4 -->
        <article class="day-block" id="day4">
          <div class="day-title-row">
            <div class="day-badge-wrap">
              <div class="day-badge badge-d4">
                <span class="num">04</span>
                <span class="sub">Day</span>
              </div>
              <div class="day-headings">
                <h2>Monday, September 28</h2>
                <p>Scenic Alpine Transit & Kusatsu Onsen Ryokan</p>
              </div>
            </div>
            <span class="day-theme-chip">♨️ Traditional Ryokan Bliss</span>
          </div>

          <!-- Transit Timetable from Screenshot -->
          <div class="transit-guide-box">
            <div class="transit-guide-title">
              <span style="font-weight:800; font-size:0.92rem; color:#0f172a;">🚆 Scenic Transit: Tokyo → Kusatsu Onsen (Route 2)</span>
              <span class="tag-price">3h 58m • ¥6,353 • 198.8 km</span>
            </div>

            <div class="transit-node">
              <div class="node-time-box">08:55</div>
              <div class="node-dot start"></div>
              <div class="node-content">
                <div class="node-name">百合ヶ丘 (Yurigaoka) [Track 2]</div>
                <div class="node-sub">
                  <span class="tag-train">小田急小田原線 (新宿行)</span>
                  <span>Board front of 8-car train</span>
                  <span class="tag-price">¥293</span>
                </div>
              </div>
            </div>

            <div class="transit-node">
              <div class="node-time-box">09:39<br><small>09:51</small></div>
              <div class="node-dot"></div>
              <div class="node-content">
                <div class="node-name">新宿 (Shinjuku) [Arrive Tr.10 → Depart Tr.3]</div>
                <div class="node-sub">
                  <span class="tag-train">JR 埼京線 (武蔵浦和行・当駅始発)</span>
                  <span>12 min transfer</span>
                </div>
              </div>
            </div>

            <div class="transit-node">
              <div class="node-time-box">10:04<br><small>10:10</small></div>
              <div class="node-dot"></div>
              <div class="node-content">
                <div class="node-name">赤羽 (Akabane) [Arrive Tr.8 → Depart Tr.4]</div>
                <div class="node-sub">
                  <span class="tag-train">JR 特急草津・四万1号 (長野原草津口行)</span>
                  <span style="font-weight:800; color:#b91c1c;">Car 4 Reserved Seat (指定席)</span>
                  <span class="tag-price">Base ¥3,190 + Express ¥2,090</span>
                </div>
              </div>
            </div>

            <div class="transit-node">
              <div class="node-time-box">12:18<br><small>12:31</small></div>
              <div class="node-dot"></div>
              <div class="node-content">
                <div class="node-name">長野原草津口 (Naganoharakusatsuguchi)</div>
                <div class="node-sub">
                  <span>3 min walk across to Bus Stop</span>
                  <span class="tag-train">JRバス関東 (直通 草津温泉行)</span>
                  <span class="tag-price">¥780</span>
                </div>
              </div>
            </div>

            <div class="transit-node">
              <div class="node-time-box">12:53</div>
              <div class="node-dot end"></div>
              <div class="node-content">
                <div class="node-name">草津温泉バスターミナル (Kusatsu Onsen)</div>
                <div class="node-sub">
                  <span style="font-weight:700; color:#10b981;">Arrive at Japan's #1 Onsen Town! ✨</span>
                </div>
              </div>
            </div>
          </div>

          <div class="timeline-schedule">
            <!-- 13:30 Hotel Sakurai -->
            <div class="timeline-entry" onclick="flyToSpot(36.6212, 138.5996, 'Hotel Sakurai Kusatsu')">
              <div class="entry-bullet">♨️</div>
              <div class="entry-header">
                <span class="entry-time">13:30 Check-in</span>
                <span class="entry-status status-confirmed">✓ Premier Ryokan Stay</span>
              </div>
              <div class="entry-body">
                <h4>Hotel Sakurai (草津温泉 ホテル櫻井)</h4>
                <div class="entry-subtitle">Gunma's Flagship Hot Spring Ryokan • 3 Natural Mineral Sources</div>
                <p class="entry-desc">
                  Ranked among Japan's premier onsen ryokans. Features 3 distinct natural spring sources (Bandai, Sainokawara, and Yubatake), massive indoor and stone-lined outdoor rotenburo baths, traditional yukata robes, and soothing mountain hospitality.
                </p>
                <div class="mini-steps-list">
                  <div class="mini-step-item"><strong>Yukata Fitting:</strong> Choose matching yukata robes from the colorful corner in the lobby.</div>
                  <div class="mini-step-item"><strong>Afternoon Soak:</strong> Enjoy the outdoor rock pools before heading down to the town center.</div>
                </div>
              </div>
              <div class="entry-footer">
                <span class="entry-location">📍 Kusatsu-machi, Gunma (Free shuttle to Yubatake)</span>
                <div class="entry-actions">
                  <a href="https://www.hotel-sakurai.co.jp/" target="_blank" class="pill-link" onclick="event.stopPropagation()">♨️ Ryokan Website</a>
                </div>
              </div>
            </div>

            <!-- 15:30 Yubatake -->
            <div class="timeline-entry" onclick="flyToSpot(36.6208, 138.5960, 'Yubatake Hot Spring Field')">
              <div class="entry-bullet">🏮</div>
              <div class="entry-header">
                <span class="entry-time">15:30 – 18:00</span>
                <span class="entry-status status-highlight">Yukata Town Stroll</span>
              </div>
              <div class="entry-body">
                <h4>Yubatake & Town Center (湯畑)</h4>
                <div class="entry-subtitle">Steaming Emerald Thermal Spring & Lantern Illuminations</div>
                <p class="entry-desc">
                  Put on matching yukata and geta sandals! Stroll the wooden bridges surrounding the iconic gushing Yubatake field, taste fresh steamed onsen manju pastries, soak your feet in the warm outdoor footbaths (Yukemuri-tei), and watch the romantic lantern illuminations at dusk.
                </p>
              </div>
              <div class="entry-footer">
                <span class="entry-location">📍 Kusatsu Town Center (5 min shuttle from hotel)</span>
                <div class="entry-actions">
                  <a href="https://maps.google.com/?q=Yubatake+Kusatsu" target="_blank" class="pill-link" onclick="event.stopPropagation()">🗺️ Google Maps</a>
                </div>
              </div>
            </div>

            <!-- 18:30 Kaiseki & Night Bath -->
            <div class="timeline-entry">
              <div class="entry-bullet">🍱</div>
              <div class="entry-header">
                <span class="entry-time">18:30 – 21:30</span>
                <span class="entry-status status-confirmed">Kaiseki Feast & Show</span>
              </div>
              <div class="entry-body">
                <h4>Ryokan Kaiseki Feast & Wadaiko Drums</h4>
                <div class="entry-subtitle">Joshu Wagyu Beef • Yumomi Performance</div>
                <p class="entry-desc">Indulge in a multi-course dinner with local seasonal delicacies, followed by Hotel Sakurai's famous in-house *Yumomi* and Japanese drum show in the grand lobby, ending with a soothing midnight onsen soak.</p>
              </div>
            </div>
          </div>
        </article>

        <!-- DAY 5 -->
        <article class="day-block" id="day5">
          <div class="day-title-row">
            <div class="day-badge-wrap">
              <div class="day-badge badge-d5">
                <span class="num">05</span>
                <span class="sub">Day</span>
              </div>
              <div class="day-headings">
                <h2>Tuesday, September 29</h2>
                <p>Bullet Train, Wolfgang's Steak & Penthouse Jazz</p>
              </div>
            </div>
            <span class="day-theme-chip">🥩 Grand Finale</span>
          </div>

          <!-- Return Transit Timetable from Screenshot -->
          <div class="transit-guide-box">
            <div class="transit-guide-title">
              <span style="font-weight:800; font-size:0.92rem; color:#0f172a;">🚅 Return Transit: Kusatsu Onsen → Gaienmae (Aoyama)</span>
              <span class="tag-price">Arrive 13:35 • Ready for 14:30 Steak!</span>
            </div>

            <div class="transit-node">
              <div class="node-time-box">09:20</div>
              <div class="node-dot start"></div>
              <div class="node-content">
                <div class="node-name">草津温泉 (Kusatsu Onsen Bus Terminal)</div>
                <div class="node-sub">
                  <span class="tag-train">JRバス関東 (長野原草津口行)</span>
                  <span class="tag-price">¥780</span>
                </div>
              </div>
            </div>

            <div class="transit-node">
              <div class="node-time-box">09:48<br><small>10:08</small></div>
              <div class="node-dot"></div>
              <div class="node-content">
                <div class="node-name">長野原草津口 (Naganoharakusatsuguchi)</div>
                <div class="node-sub">
                  <span class="tag-train">JR 吾妻線 (高崎行・当駅始発)</span>
                  <span>Arrives Takasaki Track 7</span>
                </div>
              </div>
            </div>

            <div class="transit-node">
              <div class="node-time-box">11:35<br><small>12:04</small></div>
              <div class="node-dot"></div>
              <div class="node-content">
                <div class="node-name">高崎 (Takasaki) [Track 13]</div>
                <div class="node-sub">
                  <span class="tag-train">JR 新幹線たにがわ410号 (東京行)</span>
                  <span style="font-weight:700; color:#1d4ed8;">Shinkansen Bullet Train</span>
                  <span class="tag-price">Base ¥3,190 + Non-reserved ¥2,510</span>
                </div>
              </div>
            </div>

            <div class="transit-node">
              <div class="node-time-box">13:00<br><small>13:13</small></div>
              <div class="node-dot"></div>
              <div class="node-content">
                <div class="node-name">東京 (Tokyo Station) [Tr.21 → Tr.5]</div>
                <div class="node-sub">
                  <span class="tag-train">JR 山手線外回り (品川・渋谷方面)</span>
                </div>
              </div>
            </div>

            <div class="transit-node">
              <div class="node-time-box">13:17<br><small>13:26</small></div>
              <div class="node-dot"></div>
              <div class="node-content">
                <div class="node-name">新橋 (Shimbashi) [Track 4 → Track 1]</div>
                <div class="node-sub">
                  <span class="tag-train">東京メトロ 銀座線 (渋谷行)</span>
                  <span class="tag-price">¥178</span>
                </div>
              </div>
            </div>

            <div class="transit-node">
              <div class="node-time-box">13:35</div>
              <div class="node-dot end"></div>
              <div class="node-content">
                <div class="node-name">外苑前 (Gaienmae) [Exit 4a]</div>
                <div class="node-sub">
                  <span style="font-weight:700; color:#10b981;">Direct exit to THE ARGYLE AOYAMA! 🥩</span>
                </div>
              </div>
            </div>
          </div>

          <div class="timeline-schedule">
            <!-- 14:30 Wolfgang's -->
            <div class="timeline-entry" onclick="flyToSpot(35.6698, 139.7180, 'Wolfgang\'s Steakhouse Signature Aoyama')">
              <div class="entry-bullet">🥩</div>
              <div class="entry-header">
                <span class="entry-time">14:30 – 16:30</span>
                <span class="entry-status status-confirmed">✓ Confirmed 14:30 Booking</span>
              </div>
              <div class="entry-body">
                <h4>Wolfgang's Steakhouse Signature Aoyama (ウルフギャング)</h4>
                <div class="entry-subtitle">THE ARGYLE AOYAMA • USDA Prime Dry-Aged Beef</div>
                <p class="entry-desc">
                  World-renowned for its 28-day dry-aged USDA Prime Porterhouse steaks, flash-broiled at 1,500°F and brought to your table sizzling in rich butter. Indulge in jumbo lump crab cakes, creamed spinach, and warm pecan pie.
                </p>
                <div class="mini-steps-list">
                  <div class="mini-step-item"><strong>What to Order:</strong> Prime Porterhouse Steak for Two, Jumbo Lump Crab Cake, Wolfgang's Salad, Creamed Spinach, German Potatoes, and Apple Strudel with "Schlag".</div>
                  <div class="mini-step-item"><strong>Location Advantage:</strong> Steps right out of Gaienmae Exit 4a!</div>
                </div>
              </div>
              <div class="entry-footer">
                <span class="entry-location">📍 THE ARGYLE AOYAMA 1F/2F (Minami-Aoyama 2-5-8)</span>
                <div class="entry-actions">
                  <a href="https://wolfgangssteakhouse.jp/" target="_blank" class="pill-link" onclick="event.stopPropagation()">🥩 Official Site</a>
                  <a href="https://maps.google.com/?q=Wolfgang's+Steakhouse+Signature+Aoyama" target="_blank" class="pill-link" onclick="event.stopPropagation()">🗺️ Google Maps</a>
                </div>
              </div>
            </div>

            <!-- 19:30 Shibuya -->
            <div class="timeline-entry" onclick="flyToSpot(35.6595, 139.7005, 'Shibuya Crossing & Miyashita')">
              <div class="entry-bullet">🌆</div>
              <div class="entry-header">
                <span class="entry-time">19:30 – 21:00</span>
                <span class="entry-status status-highlight">Vibrant City Vibes</span>
              </div>
              <div class="entry-body">
                <h4>Shibuya Evening Stroll (渋谷)</h4>
                <div class="entry-subtitle">Shibuya Scramble • Miyashita Park • Shibuya Sky</div>
                <p class="entry-desc">
                  Tokyo's high-energy neon capital. Walk across the world-famous Shibuya Scramble Crossing, explore the chic rooftop greenery at Miyashita Park, pick up cute souvenirs, or take in the dazzling 360° illuminated views from Shibuya Sky.
                </p>
              </div>
              <div class="entry-footer">
                <span class="entry-location">📍 Shibuya Station Area</span>
                <div class="entry-actions">
                  <a href="https://maps.google.com/?q=Shibuya+Crossing" target="_blank" class="pill-link" onclick="event.stopPropagation()">🗺️ Google Maps</a>
                </div>
              </div>
            </div>

            <!-- 21:30 New York Bar -->
            <div class="timeline-entry" onclick="flyToSpot(35.6856, 139.6910, 'New York Bar at Park Hyatt Tokyo')">
              <div class="entry-bullet">🎷</div>
              <div class="entry-header">
                <span class="entry-time">21:30 – Late</span>
                <span class="entry-status status-confirmed">Iconic Nightcap</span>
              </div>
              <div class="entry-body">
                <h4>New York Bar (Park Hyatt Tokyo 52F)</h4>
                <div class="entry-subtitle">Newly Renovated & Reopened • Shinjuku Sky Penthouse</div>
                <p class="entry-desc">
                  The legendary jazz bar made world-famous by *Lost in Translation*, completely restored to timeless luxury. Floor-to-ceiling glass reveals breathtaking panoramic night views of Shinjuku's glittering skyscraper sea. Sip classic martinis, enjoy soulful live jazz, and toast to an unforgettable trip together.
                </p>
                <div class="mini-steps-list">
                  <div class="mini-step-item"><strong>Signature Cocktails:</strong> Cosmopolitan, Manhattan, Japanese single-malt whiskies.</div>
                  <div class="mini-step-item"><strong>Dress Code:</strong> Smart casual (collared shirt, closed shoes).</div>
                </div>
              </div>
              <div class="entry-footer">
                <span class="entry-location">📍 Shinjuku Park Tower 52F, Nishi-Shinjuku</span>
                <div class="entry-actions">
                  <a href="https://maps.google.com/?q=Park+Hyatt+Tokyo+New+York+Bar" target="_blank" class="pill-link" onclick="event.stopPropagation()">🗺️ Google Maps</a>
                </div>
              </div>
            </div>
          </div>
        </article>

      </section>

      <!-- Interactive Leaflet Map Column -->
      <aside class="map-wrapper" id="trip-map-container">
        <div class="map-card-box">
          <div class="map-toolbar">
            <div class="map-header-title">
              <span>📍</span>
              <span>Trip Route & Venues</span>
            </div>
            <div class="map-filters">
              <span class="filter-chip active" onclick="filterMapMarkers('all', this)">All</span>
              <span class="filter-chip" onclick="filterMapMarkers(1, this)">D1</span>
              <span class="filter-chip" onclick="filterMapMarkers(2, this)">D2</span>
              <span class="filter-chip" onclick="filterMapMarkers(3, this)">D3</span>
              <span class="filter-chip" onclick="filterMapMarkers(4, this)">D4</span>
              <span class="filter-chip" onclick="filterMapMarkers(5, this)">D5</span>
            </div>
          </div>
          <div id="trip-map"></div>
          <div class="map-tip-bar">
            <span>💡</span>
            <span>Click any location in the schedule to fly directly to it on the map!</span>
          </div>
        </div>
      </aside>

    </div>

    <!-- Couple's Survival Tips & Checklist -->
    <section class="survival-section">
      <h2><span>🎒</span> Couple's Travel Tips & Checklist</h2>
      <div class="survival-grid">
        
        <div class="survival-card">
          <h3>👗 Dress Code & Attire</h3>
          <ul class="checklist">
            <li class="checklist-row">
              <input type="checkbox" checked id="ck1">
              <label for="ck1"><strong>VIRTÙ & New York Bar:</strong> Smart casual (collared shirt or blazer for him, chic dress/smart separates for her; no flip-flops or sports shorts).</label>
            </li>
            <li class="checklist-row">
              <input type="checkbox" checked id="ck2">
              <label for="ck2"><strong>DisneySea:</strong> Ultra-comfortable walking sneakers & Disney ears / headbands!</label>
            </li>
            <li class="checklist-row">
              <input type="checkbox" checked id="ck3">
              <label for="ck3"><strong>Kusatsu Onsen:</strong> Mountain elevation (~1,200m) is brisk in late September (~14-17°C); pack a light jacket or cozy cardigan.</label>
            </li>
          </ul>
        </div>

        <div class="survival-card">
          <h3>📱 Transit & Tech Essentials</h3>
          <ul class="checklist">
            <li class="checklist-row">
              <input type="checkbox" checked id="ck4">
              <label for="ck4">Digital Suica / Pasmo card active on Apple Wallet for instant gate tapping.</label>
            </li>
            <li class="checklist-row">
              <input type="checkbox" checked id="ck5">
              <label for="ck5">Tokyo Disney Resort App logged in with credit card registered for Priority Pass.</label>
            </li>
            <li class="checklist-row">
              <input type="checkbox" checked id="ck6">
              <label for="ck6">Portable power bank & charger cord for a full day of Disney photos!</label>
            </li>
          </ul>
        </div>

        <div class="survival-card">
          <h3>♨️ Kusatsu Ryokan Etiquette</h3>
          <ul class="checklist">
            <li class="checklist-row">
              <input type="checkbox" checked id="ck7">
              <label for="ck7">Always wash and rinse thoroughly at the seated shower stalls before entering hot spring baths.</label>
            </li>
            <li class="checklist-row">
              <input type="checkbox" checked id="ck8">
              <label for="ck8">Keep the small modesty towel on your head or pool edge — never submerge it in the bath.</label>
            </li>
            <li class="checklist-row">
              <input type="checkbox" checked id="ck9">
              <label for="ck9">Slip into Hotel Sakurai's yukata (left side wrapped over right) for dinner and town walks!</label>
            </li>
          </ul>
        </div>

      </div>
    </section>
  </main>

  <!-- Mobile Floating Map Button -->
  <button class="mobile-map-float" onclick="scrollToMapBox()">
    <span>🗺️ View Map</span>
  </button>

  <div class="toast-msg" id="calendar-toast">
    <span>✓</span> <span>Calendar event file (.ics) downloaded!</span>
  </div>

  <!-- Leaflet Map JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  
  <script>
    // Venues Dataset
    const tripLocations = [
      {
        day: 1,
        title: "Shane's Burg (新百合ヶ丘)",
        time: "Sep 25 • 19:00",
        lat: 35.6033,
        lng: 139.5080,
        color: "#e68087",
        desc: "Cozy handcrafted hamburg steak dinner at Shinyuri Elmi Road 5F.",
        link: "https://tabelog.com/kanagawa/A1405/A140508/14009641/"
      },
      {
        day: 2,
        title: "Sukiyabashi Jiro Roppongi Hills",
        time: "Sep 26 • 13:00",
        lat: 35.6586978,
        lng: 139.7291446,
        color: "#a05be8",
        desc: "Legendary Michelin Edomae sushi omakase by chef Takashi Ono.",
        link: "https://maps.app.goo.gl/Brh2wvb1fPBVpNn79"
      },
      {
        day: 2,
        title: "Tokyo Tower (東京タワー)",
        time: "Sep 26 • 15:30",
        lat: 35.6585805,
        lng: 139.7454329,
        color: "#a05be8",
        desc: "360° observatory views, retro romance, and glass skywalk.",
        link: "https://www.tokyotower.co.jp/en/"
      },
      {
        day: 2,
        title: "VIRTÙ (Four Seasons Otemachi)",
        time: "Sep 26 • 17:30",
        lat: 35.6872,
        lng: 139.7645,
        color: "#a05be8",
        desc: "Asia's 50 Best Bars: 39th floor Parisian elegance & skyline cocktails.",
        link: "https://www.fourseasons.com/tokyo-otemachi/dining/lounges/virtu/"
      },
      {
        day: 2,
        title: "Muten Kura Sushi (くら寿司)",
        time: "Sep 26 • 20:00",
        lat: 35.6719,
        lng: 139.7648,
        color: "#a05be8",
        desc: "Fun conveyor-belt sushi & Bikkura-Pon gacha lottery game.",
        link: "https://www.kurasushi.co.jp/mutenkura/"
      },
      {
        day: 3,
        title: "Tokyo DisneySea",
        time: "Sep 27 • 09:00",
        lat: 35.6267,
        lng: 139.8851,
        color: "#348efc",
        desc: "World's most romantic Disney park: Fantasy Springs & Mediterranean Harbor.",
        link: "https://www.tokyodisneyresort.jp/en/tds/"
      },
      {
        day: 3,
        title: "S.S. Columbia Dining Room",
        time: "Sep 27 • 19:20",
        lat: 35.6238,
        lng: 139.8860,
        color: "#348efc",
        desc: "Grand Edwardian luxury ocean liner roast beef course dinner.",
        link: "https://www.tokyodisneyresort.jp/en/tds/restaurant/detail/431/"
      },
      {
        day: 4,
        title: "Hotel Sakurai Kusatsu (ホテル櫻井)",
        time: "Sep 28 • 13:30 Check-in",
        lat: 36.6212,
        lng: 138.5996,
        color: "#10b981",
        desc: "Kusatsu's premier ryokan with 3 hot spring sources & giant baths.",
        link: "https://www.hotel-sakurai.co.jp/"
      },
      {
        day: 4,
        title: "Yubatake (湯畑)",
        time: "Sep 28 • 15:30",
        lat: 36.6208,
        lng: 138.5960,
        color: "#10b981",
        desc: "Steaming emerald hot spring fields, foot baths & evening illuminations.",
        link: "https://maps.google.com/?q=Yubatake+Kusatsu"
      },
      {
        day: 5,
        title: "Wolfgang's Steakhouse Aoyama",
        time: "Sep 29 • 14:30",
        lat: 35.6698,
        lng: 139.7180,
        color: "#f59e0b",
        desc: "USDA Prime dry-aged porterhouse steaks at THE ARGYLE AOYAMA.",
        link: "https://wolfgangssteakhouse.jp/"
      },
      {
        day: 5,
        title: "Shibuya Crossing & Miyashita",
        time: "Sep 29 • 19:30",
        lat: 35.6595,
        lng: 139.7005,
        color: "#f59e0b",
        desc: "Iconic Scramble, rooftop park, shopping & evening city lights.",
        link: "https://maps.google.com/?q=Shibuya+Crossing"
      },
      {
        day: 5,
        title: "New York Bar (Park Hyatt 52F)",
        time: "Sep 29 • 21:30",
        lat: 35.6856,
        lng: 139.6910,
        color: "#f59e0b",
        desc: "Lost in Translation penthouse bar: live jazz & Shinjuku skyline.",
        link: "https://maps.google.com/?q=Park+Hyatt+Tokyo+New+York+Bar"
      }
    ];

    let map = L.map('trip-map', {
      center: [35.68, 139.75],
      zoom: 11,
      zoomControl: true
    });

    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://carto.com/">CARTO</a> & OSM',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(map);

    let mapMarkers = [];

    function makeMarkerPin(color, dayNum) {
      return L.divIcon({
        className: 'custom-pin-wrapper',
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

    tripLocations.forEach(spot => {
      const icon = makeMarkerPin(spot.color, spot.day);
      const marker = L.marker([spot.lat, spot.lng], { icon: icon }).addTo(map);
      
      const popupHtml = `
        <div class="map-popup-inner">
          <span class="pop-time">${spot.time}</span>
          <h4>${spot.title}</h4>
          <p>${spot.desc}</p>
          <a href="${spot.link}" target="_blank">Open Details & Map →</a>
        </div>
      `;
      marker.bindPopup(popupHtml);
      marker.spotMeta = spot;
      mapMarkers.push(marker);
    });

    // Connecting Route
    L.polyline([
      [35.6033, 139.5080],
      [35.6587, 139.7291],
      [35.6586, 139.7454],
      [35.6872, 139.7645],
      [35.6267, 139.8851],
      [36.3220, 139.0130],
      [36.5600, 138.6500],
      [36.6212, 138.5996]
    ], {
      color: '#9e2a4b',
      weight: 3,
      opacity: 0.55,
      dashArray: '6, 8'
    }).addTo(map);

    function flyToSpot(lat, lng, name) {
      if (window.innerWidth <= 1080) {
        scrollToMapBox();
      }
      map.flyTo([lat, lng], 15, {
        animate: true,
        duration: 1.2
      });

      mapMarkers.forEach(m => {
        if (Math.abs(m.getLatLng().lat - lat) < 0.001 && Math.abs(m.getLatLng().lng - lng) < 0.001) {
          setTimeout(() => { m.openPopup(); }, 700);
        }
      });
    }

    function scrollToMapBox() {
      const el = document.getElementById('trip-map-container');
      el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    function focusAllPins() {
      const group = new L.featureGroup(mapMarkers);
      map.fitBounds(group.getBounds().pad(0.12));
    }

    function filterMapMarkers(day, chipEl) {
      document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
      if (chipEl) chipEl.classList.add('active');

      const visible = [];
      mapMarkers.forEach(m => {
        if (day === 'all' || m.spotMeta.day === parseInt(day)) {
          m.addTo(map);
          visible.push(m);
        } else {
          map.removeLayer(m);
        }
      });

      if (visible.length > 0) {
        const group = new L.featureGroup(visible);
        map.fitBounds(group.getBounds().pad(0.18));
      }
    }

    function activateDay(dayKey, tabEl) {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      tabEl.classList.add('active');

      if (dayKey === 'all') {
        document.querySelectorAll('.day-block').forEach(b => b.style.display = 'block');
        filterMapMarkers('all', document.querySelector('.map-filters .filter-chip:first-child'));
      } else {
        document.querySelectorAll('.day-block').forEach(b => {
          if (b.id === dayKey) {
            b.style.display = 'block';
            b.scrollIntoView({ behavior: 'smooth', block: 'start' });
          } else {
            b.style.display = 'none';
          }
        });
        const dayNumber = dayKey.replace('day', '');
        const targetChip = Array.from(document.querySelectorAll('.filter-chip')).find(el => el.textContent.includes('D' + dayNumber));
        filterMapMarkers(dayNumber, targetChip);
      }
    }

    function copyShareURL() {
      navigator.clipboard.writeText(window.location.href);
      const label = document.getElementById('share-label');
      label.textContent = '✓ Copied Link!';
      setTimeout(() => { label.textContent = '🔗 Share with Her'; }, 2500);
    }

    function downloadCalendarFile() {
      const icsData = `BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Couple Japan Romance Trip//EN
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
SUMMARY:Dinner at Shane's Burg
DTSTART;TZID=Asia/Tokyo:20260925T190000
DTEND;TZID=Asia/Tokyo:20260925T210000
DESCRIPTION:Kick-off dinner at Shane's Burg Shinyurigaoka Elmi Road 5F
LOCATION:Shinyurigaoka Station, Kanagawa
STATUS:CONFIRMED
END:VEVENT
BEGIN:VEVENT
SUMMARY:Sukiyabashi Jiro Roppongi Hills (Omakase Sushi)
DTSTART;TZID=Asia/Tokyo:20260926T130000
DTEND;TZID=Asia/Tokyo:20260926T143000
DESCRIPTION:Edomae sushi omakase reservation at Roppongi Hills Keyakizaka Dori 3F
LOCATION:Roppongi Hills Keyakizaka Dori 3F, Tokyo
STATUS:CONFIRMED
END:VEVENT
BEGIN:VEVENT
SUMMARY:Tokyo Tower & VIRTÙ Lounge
DTSTART;TZID=Asia/Tokyo:20260926T153000
DTEND;TZID=Asia/Tokyo:20260926T193000
DESCRIPTION:Tokyo Tower observatory views followed by cocktails at VIRTÙ (Four Seasons Otemachi 39F)
LOCATION:Tokyo Tower & Four Seasons Otemachi, Tokyo
END:VEVENT
BEGIN:VEVENT
SUMMARY:Dinner at Kura Sushi
DTSTART;TZID=Asia/Tokyo:20260926T200000
DTEND;TZID=Asia/Tokyo:20260926T213000
DESCRIPTION:Fun conveyor sushi & Bikkura-Pon game
LOCATION:Tokyo
END:VEVENT
BEGIN:VEVENT
SUMMARY:Tokyo DisneySea & S.S. Columbia Dinner
DTSTART;TZID=Asia/Tokyo:20260927T090000
DTEND;TZID=Asia/Tokyo:20260927T210000
DESCRIPTION:DisneySea adventure (enter 09:00), S.S. Columbia luxury liner dinner booked at 19:20
LOCATION:Tokyo DisneySea, Maihama
STATUS:CONFIRMED
END:VEVENT
BEGIN:VEVENT
SUMMARY:Kusatsu Onsen Getaway & Hotel Sakurai
DTSTART;TZID=Asia/Tokyo:20260928T085500
DTEND;TZID=Asia/Tokyo:20260928T220000
DESCRIPTION:Train travel to Kusatsu Onsen (Depart 08:55), Hotel Sakurai check-in, Yubatake hot springs stroll
LOCATION:Hotel Sakurai, Kusatsu Onsen, Gunma
STATUS:CONFIRMED
END:VEVENT
BEGIN:VEVENT
SUMMARY:Wolfgang's Steakhouse Signature Aoyama
DTSTART;TZID=Asia/Tokyo:20260929T143000
DTEND;TZID=Asia/Tokyo:20260929T163000
DESCRIPTION:USDA Prime dry-aged porterhouse steak lunch (arrive 14:30)
LOCATION:THE ARGYLE AOYAMA, Gaienmae, Tokyo
STATUS:CONFIRMED
END:VEVENT
BEGIN:VEVENT
SUMMARY:Shibuya Stroll & New York Bar (Park Hyatt)
DTSTART;TZID=Asia/Tokyo:20260929T193000
DTEND;TZID=Asia/Tokyo:20260929T233000
DESCRIPTION:Shibuya evening stroll at 19:30, followed by live jazz cocktails at New York Bar (Park Hyatt Tokyo 52F)
LOCATION:Shibuya & Park Hyatt Tokyo, Shinjuku
END:VEVENT
END:VCALENDAR`;

      const blob = new Blob([icsData], { type: 'text/calendar;charset=utf-8' });
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.setAttribute('download', 'japan_romantic_itinerary_2026.ics');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      const toast = document.getElementById('calendar-toast');
      toast.style.display = 'flex';
      setTimeout(() => { toast.style.display = 'none'; }, 3000);
    }

    setTimeout(() => { focusAllPins(); }, 400);
  </script>
</body>
</html>
'''

with open('/Users/rondey/japan-trip-itinerary/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('/Users/rondey/tokyo-kusatsu-itinerary.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Master Itinerary HTML written successfully!")
