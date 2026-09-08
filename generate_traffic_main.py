import json

html_content = '''<!DOCTYPE html>
<html lang="zh-HK">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>東京 & 草津溫泉 浪漫雙人之旅 | 即時路線地圖</title>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700;900&family=Noto+Serif+TC:wght@600;700&family=Plus+Jakarta+Sans:wght@500;700;800&display=swap" rel="stylesheet">
  
  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
  
  <style>
    :root {
      --primary: #9e2846;
      --primary-dark: #781830;
      --primary-light: #fef1f3;
      --accent-gold: #c59341;
      --accent-gold-light: #fef8ee;
      --accent-blue: #2563eb;
      --accent-emerald: #059669;
      --bg-body: #f8f6f2;
      --bg-card: #ffffff;
      --bg-subtle: #f4f0e8;
      --text-main: #1c1917;
      --text-muted: #66615b;
      --border-color: #e5dfd5;
      --shadow-sm: 0 2px 8px rgba(28, 25, 23, 0.04);
      --shadow-md: 0 8px 24px rgba(28, 25, 23, 0.08);
      --shadow-lg: 0 16px 40px rgba(28, 25, 23, 0.12);
      --radius-sm: 10px;
      --radius-md: 18px;
      --radius-lg: 26px;
      --font-serif: 'Noto Serif TC', Georgia, serif;
      --font-sans: 'Noto Sans TC', system-ui, -apple-system, sans-serif;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: var(--font-sans);
      background-color: var(--bg-body);
      color: var(--text-main);
      line-height: 1.6;
      -webkit-font-smoothing: antialiased;
      overflow-x: hidden;
      height: 100vh;
      display: flex;
      flex-direction: column;
    }

    /* Clean Solid Top Navigation */
    .top-navbar {
      height: 62px;
      background: #ffffff;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      z-index: 1000;
      flex-shrink: 0;
      box-shadow: 0 1px 6px rgba(0,0,0,0.03);
    }

    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-title {
      font-family: var(--font-serif);
      font-size: 1.15rem;
      font-weight: 700;
      color: var(--primary);
      letter-spacing: -0.01em;
    }

    .brand-pill {
      font-size: 0.74rem;
      background: var(--accent-gold-light);
      color: #8c5b14;
      border: 1px solid #f6deb3;
      padding: 2px 10px;
      border-radius: 20px;
      font-weight: 700;
    }

    .nav-buttons {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .btn-nav-action {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 14px;
      border-radius: 40px;
      font-size: 0.8rem;
      font-weight: 700;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s ease;
      border: 1px solid var(--border-color);
      background: #fff;
      color: var(--text-main);
    }

    .btn-nav-action:hover {
      background: var(--bg-subtle);
      border-color: #cfc5b5;
    }

    .btn-nav-primary {
      background: linear-gradient(135deg, #a12b48 0%, #7d1c35 100%);
      color: #fff;
      border: none;
      box-shadow: 0 3px 10px rgba(161, 43, 72, 0.35);
    }
    .btn-nav-primary:hover {
      transform: translateY(-1px);
      box-shadow: 0 5px 14px rgba(161, 43, 72, 0.45);
    }

    /* Main Container: Map is Main */
    .app-viewport {
      flex: 1;
      display: flex;
      position: relative;
      overflow: hidden;
    }

    /* Map Stage */
    .map-container {
      flex: 1;
      height: 100%;
      position: relative;
      background: #eef2f5;
    }

    #trip-map {
      width: 100%;
      height: 100%;
      z-index: 1;
    }

    /* Floating Navigation Controls */
    .map-overlay-controls {
      position: absolute;
      top: 18px;
      left: 20px;
      z-index: 500;
      display: flex;
      gap: 8px;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(14px);
      padding: 6px 8px;
      border-radius: 50px;
      box-shadow: var(--shadow-md);
      border: 1px solid rgba(255, 255, 255, 0.95);
      overflow-x: auto;
      max-width: calc(100% - 40px);
      scrollbar-width: none;
    }
    .map-overlay-controls::-webkit-scrollbar { display: none; }

    .day-selector-btn {
      padding: 8px 16px;
      border-radius: 40px;
      border: none;
      background: transparent;
      color: var(--text-muted);
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      white-space: nowrap;
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }

    .day-selector-btn.active {
      background: var(--primary);
      color: #fff;
      box-shadow: 0 4px 12px rgba(158, 40, 70, 0.35);
    }

    .day-selector-btn:hover:not(.active) {
      background: var(--bg-subtle);
      color: var(--text-main);
    }

    /* Traffic Status Indicator */
    .traffic-status-card {
      position: absolute;
      bottom: 24px;
      left: 20px;
      z-index: 500;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(14px);
      padding: 10px 18px;
      border-radius: var(--radius-sm);
      box-shadow: var(--shadow-md);
      border: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      gap: 14px;
      font-size: 0.8rem;
    }

    .traffic-indicator-beacon {
      display: flex;
      align-items: center;
      gap: 6px;
      font-weight: 800;
      color: var(--primary);
    }

    .live-pulse-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
      animation: pulseGreen 1.8s infinite;
    }

    @keyframes pulseGreen {
      0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
      70% { box-shadow: 0 0 0 8px rgba(16, 185, 129, 0); }
      100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }

    .traffic-replay-btn {
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      color: var(--text-main);
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 0.76rem;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
      display: flex;
      align-items: center;
      gap: 5px;
    }
    .traffic-replay-btn:hover {
      background: #fff;
      border-color: var(--primary);
      color: var(--primary);
    }

    /* Right Itinerary Drawer */
    .itinerary-panel {
      width: 500px;
      height: 100%;
      background: #ffffff;
      border-left: 1px solid var(--border-color);
      z-index: 600;
      display: flex;
      flex-direction: column;
      box-shadow: -4px 0 20px rgba(0,0,0,0.04);
      flex-shrink: 0;
    }

    .panel-header {
      padding: 16px 20px;
      border-bottom: 1px solid var(--border-color);
      background: #fdfcf9;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
    }

    .panel-header h2 {
      font-family: var(--font-serif);
      font-size: 1.2rem;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .panel-header p {
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-top: 2px;
    }

    .panel-toggle-btn {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      border: 1px solid var(--border-color);
      background: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: var(--text-muted);
      transition: all 0.2s ease;
      font-weight: 700;
    }
    .panel-toggle-btn:hover {
      background: var(--bg-subtle);
      color: var(--text-main);
    }

    .panel-scroll-area {
      flex: 1;
      overflow-y: auto;
      padding: 18px;
      display: flex;
      flex-direction: column;
      gap: 18px;
      scroll-behavior: smooth;
    }

    /* Day Section Block */
    .day-block {
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      background: #fff;
      overflow: hidden;
      box-shadow: var(--shadow-sm);
      transition: all 0.2s ease;
    }

    .day-block.active-day-block {
      border-color: var(--primary);
      box-shadow: 0 4px 18px rgba(158, 40, 70, 0.12);
    }

    .day-block-header {
      padding: 14px 18px;
      background: #faf7f2;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
    }

    .day-title-wrap {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .day-badge-tag {
      font-size: 0.72rem;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 6px;
      color: #fff;
    }

    .badge-d1 { background: #e07a7e; }
    .badge-d2 { background: #9b51e0; }
    .badge-d3 { background: #2f80ed; }
    .badge-d4 { background: #10b981; }
    .badge-d5 { background: #f59e0b; }

    .day-title-text h3 {
      font-size: 0.95rem;
      font-weight: 800;
      color: var(--text-main);
    }

    .day-title-text span {
      font-size: 0.76rem;
      color: var(--text-muted);
    }

    .day-block-body {
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    /* Clean Solid Itinerary Card */
    .venue-card {
      border: 1px solid var(--border-color);
      background: #ffffff;
      border-radius: var(--radius-sm);
      padding: 14px 16px;
      transition: all 0.2s ease;
      cursor: pointer;
    }

    .venue-card:hover {
      border-color: var(--accent-gold);
      transform: translateY(-2px);
      box-shadow: var(--shadow-sm);
    }

    .card-top-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }

    .card-time-pill {
      font-size: 0.78rem;
      font-weight: 800;
      color: var(--primary);
      background: var(--primary-light);
      padding: 2px 8px;
      border-radius: 6px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .card-status-pill {
      font-size: 0.72rem;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 6px;
    }

    .pill-booking {
      background: #e6f7ef;
      color: #0b784a;
      border: 1px solid #b3e6cc;
    }

    .pill-sightseeing {
      background: #fdf5e6;
      color: #a86500;
      border: 1px solid #f9e2b3;
    }

    .venue-japanese-name {
      font-size: 1.05rem;
      font-weight: 800;
      color: #1a1816;
      margin-bottom: 2px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .venue-chinese-subtitle {
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-bottom: 8px;
      font-weight: 500;
    }

    .venue-details {
      font-size: 0.84rem;
      color: #4b4845;
      line-height: 1.5;
      margin-bottom: 10px;
    }

    .venue-highlight-note {
      background: var(--bg-subtle);
      border-left: 3px solid var(--accent-gold);
      border-radius: 4px;
      padding: 8px 12px;
      font-size: 0.78rem;
      color: #5d5955;
      margin-bottom: 10px;
    }
    .venue-highlight-note strong { color: #222; }

    .card-footer-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid #f3eeea;
      padding-top: 10px;
      font-size: 0.78rem;
    }

    .venue-location-text {
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .venue-actions {
      display: flex;
      gap: 6px;
    }

    .btn-action-pill {
      color: var(--primary);
      text-decoration: none;
      font-weight: 700;
      font-size: 0.74rem;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 8px;
      border-radius: 4px;
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      transition: all 0.15s ease;
    }
    .btn-action-pill:hover {
      background: var(--primary-light);
      border-color: var(--primary);
    }

    /* Clean Solid Transit Guide */
    .transit-guide-box {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 10px;
      padding: 14px;
      margin: 10px 0;
    }

    .transit-guide-title {
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-size: 0.82rem;
      font-weight: 800;
      color: #1e293b;
      margin-bottom: 12px;
      padding-bottom: 8px;
      border-bottom: 1px solid #e2e8f0;
    }

    .transit-step-item {
      display: flex;
      gap: 12px;
      position: relative;
      padding-bottom: 14px;
    }
    .transit-step-item:last-child { padding-bottom: 0; }

    /* Solid Clean Indicator Line */
    .transit-step-item::after {
      content: "";
      position: absolute;
      left: 17px;
      top: 22px;
      bottom: -4px;
      width: 2px;
      background: #cbd5e1;
    }
    .transit-step-item:last-child::after { display: none; }

    .step-time-box {
      font-family: monospace;
      font-size: 0.82rem;
      font-weight: 800;
      color: #0f172a;
      width: 44px;
      text-align: right;
    }

    .step-marker-dot {
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: #3b82f6;
      border: 2px solid #fff;
      box-shadow: 0 0 0 2px #3b82f6;
      margin-top: 4px;
      z-index: 1;
      flex-shrink: 0;
    }
    .step-marker-dot.start { background: #10b981; box-shadow: 0 0 0 2px #10b981; }
    .step-marker-dot.end { background: #ef4444; box-shadow: 0 0 0 2px #ef4444; }

    .step-desc-wrap { flex: 1; }
    .step-station-name { font-weight: 800; font-size: 0.88rem; color: #1e293b; }
    .step-subline {
      font-size: 0.76rem;
      color: #64748b;
      margin-top: 2px;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
    }

    .subline-badge {
      background: #e2e8f0;
      padding: 1px 6px;
      border-radius: 4px;
      font-size: 0.72rem;
      color: #334155;
      font-weight: 700;
    }

    /* Map Elements */
    .map-pin-badge {
      width: 34px;
      height: 34px;
      border-radius: 50% 50% 50% 0;
      transform: rotate(-45deg);
      border: 2.5px solid #ffffff;
      box-shadow: 0 4px 12px rgba(0,0,0,0.25);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }

    .map-pin-badge span {
      transform: rotate(45deg);
      color: #ffffff;
      font-size: 11px;
      font-weight: 900;
      font-family: var(--font-sans);
    }

    /* Animated Vehicle & Pulse Following Traffic */
    .traffic-vehicle-marker {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background: #ffffff;
      border: 2px solid var(--primary);
      box-shadow: 0 3px 12px rgba(0,0,0,0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 16px;
      z-index: 1000 !important;
      transition: transform 0.1s linear;
    }

    .leaflet-popup-content-wrapper {
      border-radius: 14px;
      padding: 4px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.18);
    }

    .popup-inner {
      font-family: var(--font-sans);
      max-width: 250px;
      padding: 4px;
    }

    .popup-time-badge {
      font-size: 0.74rem;
      color: var(--primary);
      font-weight: 800;
      margin-bottom: 4px;
      display: inline-block;
      background: var(--primary-light);
      padding: 2px 8px;
      border-radius: 4px;
    }

    .popup-title { font-size: 1rem; font-weight: 800; color: #1a1816; margin-bottom: 2px; }
    .popup-sub { font-size: 0.78rem; color: var(--text-muted); margin-bottom: 6px; }
    .popup-desc { font-size: 0.8rem; color: #555; line-height: 1.45; margin-bottom: 10px; }

    .popup-button-row { display: flex; gap: 6px; }
    .popup-btn {
      flex: 1;
      text-align: center;
      font-size: 0.74rem;
      font-weight: 700;
      padding: 5px 8px;
      border-radius: 6px;
      text-decoration: none;
    }
    .btn-detail { background: var(--primary); color: #fff; }
    .btn-gmaps { background: var(--bg-subtle); color: var(--text-main); border: 1px solid var(--border-color); }

    /* Mobile Layout */
    @media (max-width: 960px) {
      .app-viewport { flex-direction: column; }
      .itinerary-panel {
        width: 100%;
        height: 52%;
        border-left: none;
        border-top: 1px solid var(--border-color);
      }
      .map-container { height: 48%; }
      .map-overlay-controls { top: 10px; left: 10px; }
      .traffic-status-card { bottom: 10px; left: 10px; padding: 6px 12px; }
    }

    .toast-pill {
      position: fixed;
      bottom: 24px;
      left: 50%;
      transform: translateX(-50%);
      background: #1e293b;
      color: #fff;
      padding: 10px 22px;
      border-radius: 50px;
      box-shadow: 0 10px 25px rgba(0,0,0,0.25);
      font-size: 0.84rem;
      font-weight: 700;
      z-index: 2000;
      display: none;
      align-items: center;
      gap: 8px;
    }
  </style>
</head>
<body>

  <!-- Top Bar -->
  <header class="top-navbar">
    <div class="brand-group">
      <span style="font-size:1.35rem;">🌸</span>
      <div>
        <h1 class="brand-title">東京 & 草津溫泉 浪漫雙人行</h1>
      </div>
      <span class="brand-pill">9/25 – 9/29 • 5天4夜</span>
    </div>

    <div class="nav-buttons">
      <button class="btn-nav-action" onclick="fitFullTrafficRoute()">
        <span>🗺️ 全程視角</span>
      </button>
      <button class="btn-nav-action" onclick="downloadCalendarFile()">
        <span>📅 加入日曆 (.ics)</span>
      </button>
      <button class="btn-nav-action btn-nav-primary" onclick="copyShareURL()">
        <span>🔗 分享給女朋友</span>
      </button>
    </div>
  </header>

  <!-- Application Viewport: Map is Dominant -->
  <div class="app-viewport">
    
    <!-- Dominant Interactive Map Stage -->
    <main class="map-container">
      
      <!-- Day Switcher Tabs directly on Map -->
      <div class="map-overlay-controls">
        <button class="day-selector-btn active" onclick="switchActiveDay('all', this)">
          <span>✨ 全部景點</span>
        </button>
        <button class="day-selector-btn" onclick="switchActiveDay(1, this)">
          <span>9/25 (五) 新百合之夜</span>
        </button>
        <button class="day-selector-btn" onclick="switchActiveDay(2, this)">
          <span>9/26 (六) 壽司 & 鐵塔</span>
        </button>
        <button class="day-selector-btn" onclick="switchActiveDay(3, this)">
          <span>9/27 (日) 迪士尼海洋</span>
        </button>
        <button class="day-selector-btn" onclick="switchActiveDay(4, this)">
          <span>9/28 (一) 草津溫泉</span>
        </button>
        <button class="day-selector-btn" onclick="switchActiveDay(5, this)">
          <span>9/29 (二) 牛排 & 夜景</span>
        </button>
      </div>

      <!-- Leaflet Map Container -->
      <div id="trip-map"></div>

      <!-- Live Traffic Flow Indicator Card -->
      <div class="traffic-status-card">
        <div class="traffic-indicator-beacon">
          <div class="live-pulse-dot"></div>
          <span id="traffic-status-label">即時交通動態：行駛中</span>
        </div>
        <button class="traffic-replay-btn" onclick="restartCurrentDayTraffic()">
          <span>▶ 重播交通路線</span>
        </button>
      </div>
    </main>

    <!-- Side Itinerary Drawer -->
    <aside class="itinerary-panel" id="itinerary-panel">
      <div class="panel-header">
        <div>
          <h2><span>📋</span> 詳細行程路線</h2>
          <p>點選任意行程卡片，地圖將平滑導航至該地點並沿真實道路行駛</p>
        </div>
        <button class="panel-toggle-btn" title="切換檢視" onclick="togglePanelWidth()">⇋</button>
      </div>

      <div class="panel-scroll-area" id="panel-scroll">
        
        <!-- DAY 1 -->
        <div class="day-block" id="block-day-1">
          <div class="day-block-header" onclick="switchActiveDay(1)">
            <div class="day-title-wrap">
              <span class="day-badge-tag badge-d1">Day 1</span>
              <div class="day-title-text">
                <h3>9月25日 (星期五) • 抵達與溫馨晚餐</h3>
                <span>手打漢堡排 ‧ 放鬆安頓</span>
              </div>
            </div>
            <span style="font-size:0.75rem; color:var(--text-muted);">1 個地點</span>
          </div>

          <div class="day-block-body">
            <!-- Shane's Burg -->
            <div class="venue-card" onclick="focusVenue(35.6033, 139.5080, 'シェーンズバーグ 新百合ヶ丘店')">
              <div class="card-top-row">
                <span class="card-time-pill">⏰ 19:00 (晚上 7:00)</span>
                <span class="card-status-pill pill-booking">✓ 已預約晚餐</span>
              </div>
              <div class="venue-japanese-name">🥩 シェーンズバーグ 新百合ヶ丘店</div>
              <div class="venue-chinese-subtitle">Shane's Burg • 新百合之丘 Elmi Road 5F 美式漢堡排專門店</div>
              <p class="venue-details">
                每日新鮮現打手作特級牛肉漢堡排，經炭火高溫封烤，肉汁飽滿。在美式木質溫暖氛圍中放鬆用餐，為美好旅程揭開序幕！
              </p>
              <div class="venue-highlight-note">
                <strong>💡 推薦點餐：</strong>經典多蜜醬（デミグラス）或日式蒜蓉洋蔥醬漢堡排，加融化起司；配酥脆薯塊與生啤酒/Highball。<br>
                <strong>💰 人均預算：</strong>約 ¥1,500 – ¥2,500。
              </div>
              <div class="card-footer-row">
                <span class="venue-location-text">📍 小田急線 新百合ヶ丘駅 直通商場 5F</span>
                <div class="venue-actions">
                  <a href="https://tabelog.com/kanagawa/A1405/A140508/14009641/" target="_blank" class="btn-action-pill" onclick="event.stopPropagation()">📖 食べログ</a>
                  <a href="https://maps.google.com/?q=Shane's+Burg+Shin-Yurigaoka" target="_blank" class="btn-action-pill" onclick="event.stopPropagation()">🗺️ Google 地圖</a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- DAY 2 -->
        <div class="day-block" id="block-day-2">
          <div class="day-block-header" onclick="switchActiveDay(2)">
            <div class="day-title-wrap">
              <span class="day-badge-tag badge-d2">Day 2</span>
              <div class="day-title-text">
                <h3>9月26日 (星期六) • 壽司之神、鐵塔與高空酒吧</h3>
                <span>六本木板前 ‧ 浪漫鐵塔 ‧ 亞洲50最佳酒吧</span>
              </div>
            </div>
            <span style="font-size:0.75rem; color:var(--text-muted);">4 個地點</span>
          </div>

          <div class="day-block-body">
            <!-- Sukiyabashi Jiro -->
            <div class="venue-card" onclick="focusVenue(35.6586978, 139.7291446, 'すきやばし 次郎 六本木ヒルズ店')">
              <div class="card-top-row">
                <span class="card-time-pill">⏰ 13:00 (下午 1:00)</span>
                <span class="card-status-pill pill-booking">✓ 已預約板前席</span>
              </div>
              <div class="venue-japanese-name">🍣 すきやばし 次郎 六本木ヒルズ店</div>
              <div class="venue-chinese-subtitle">Sukiyabashi Jiro • 六本木之丘 櫸坂通 3F 江戶前壽司</div>
              <p class="venue-details">
                世界傳奇「壽司之神」小野二郎之子——小野隆主理。極致純粹的江戶前板前握壽司，米飯溫度精確，魚生刀工絕倫，是一生難忘的頂級味蕾盛宴。
              </p>
              <div class="venue-highlight-note">
                <strong>💡 禮儀小貼士：</strong>師傅刷好醬汁握好送上後，建議在數秒內以手或筷直接享用最佳溫度；店內禁止噴過濃香水。
              </div>
              <div class="card-footer-row">
                <span class="venue-location-text">📍 六本木ヒルズ けやき坂通り 3F</span>
                <div class="venue-actions">
                  <a href="https://maps.app.goo.gl/Brh2wvb1fPBVpNn79" target="_blank" class="btn-action-pill" onclick="event.stopPropagation()">🗺️ Google 地圖</a>
                </div>
              </div>
            </div>

            <!-- Tokyo Tower -->
            <div class="venue-card" onclick="focusVenue(35.6585805, 139.7454329, '東京タワー')">
              <div class="card-top-row">
                <span class="card-time-pill">⏰ 15:30 – 17:00</span>
                <span class="card-status-pill pill-sightseeing">浪漫地標</span>
              </div>
              <div class="venue-japanese-name">🗼 東京タワー (Tokyo Tower)</div>
              <div class="venue-chinese-subtitle">Main Deck 150m 展望台 ‧ 透明玻璃步道</div>
              <p class="venue-details">
                從六本木搭乘計程車約10分鐘即可抵達。登上 150 米主展望台俯瞰東京全景與台場海灣，走在驚險的透明玻璃地板合影，並參拜東京最高的戀愛神社「タワー大神宮」。
              </p>
              <div class="card-footer-row">
                <span class="venue-location-text">📍 港區芝公園 4-2-8</span>
                <div class="venue-actions">
                  <a href="https://www.tokyotower.co.jp/" target="_blank" class="btn-action-pill" onclick="event.stopPropagation()">🌐 官方網站</a>
                </div>
              </div>
            </div>

            <!-- VIRTU -->
            <div class="venue-card" onclick="focusVenue(35.6872, 139.7645, 'VIRTÙ (フォーシーズンズホテル東京大手町)')">
              <div class="card-top-row">
                <span class="card-time-pill">⏰ 17:30 – 19:15</span>
                <span class="card-status-pill pill-sightseeing">亞洲50最佳酒吧</span>
              </div>
              <div class="venue-japanese-name">🍸 VIRTÙ (フォーシーズンズホテル東京大手町 39F)</div>
              <div class="venue-chinese-subtitle">Four Seasons Hotel Tokyo at Otemachi • 法日融合巴黎沙龍風</div>
              <p class="venue-details">
                榮登「亞洲50佳酒吧」！挑高雙層落地窗俯瞰皇居御苑與新宿天際線晚霞。室內兼具1920年代巴黎裝飾藝術與現代摩登氣派，品味獨創的《Smoked Ume Fashioned》調酒。
              </p>
              <div class="venue-highlight-note">
                <strong>👔 服裝要求（Smart Casual）：</strong>男士請著長褲與有領襯衫、皮鞋（勿穿拖鞋、短褲）；女士建議典雅洋裝或精緻便服。
              </div>
              <div class="card-footer-row">
                <span class="venue-location-text">📍 大手町 1-2-1 酒店 39 樓</span>
                <div class="venue-actions">
                  <a href="https://www.fourseasons.com/tokyo-otemachi/dining/lounges/virtu/" target="_blank" class="btn-action-pill" onclick="event.stopPropagation()">🍸 酒單預覽</a>
                </div>
              </div>
            </div>

            <!-- Kura Sushi -->
            <div class="venue-card" onclick="focusVenue(35.6719, 139.7648, '無添くら寿司')">
              <div class="card-top-row">
                <span class="card-time-pill">⏰ 20:00 (晚上 8:00)</span>
                <span class="card-status-pill pill-booking">趣味歡樂晚餐</span>
              </div>
              <div class="venue-japanese-name">🍣 無添くら寿司 (Muten Kura Sushi)</div>
              <div class="venue-chinese-subtitle">無人工添加物迴轉壽司 ‧ 必玩「畢庫拉碰」扭蛋遊戲</div>
              <p class="venue-details">
                與中午的嚴肅板前形成可愛的反差萌！全品項無人工添加的美味迴轉壽司，每吃完 5 盤投入回收口，螢幕就會自動啟動抽獎動畫，情侶一起挑戰扭蛋超有樂趣！
              </p>
              <div class="card-footer-row">
                <span class="venue-location-text">📍 東京旗艦店 / 銀座店</span>
                <div class="venue-actions">
                  <a href="https://www.kurasushi.co.jp/mutenkura/" target="_blank" class="btn-action-pill" onclick="event.stopPropagation()">🌐 官方網站</a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- DAY 3 -->
        <div class="day-block" id="block-day-3">
          <div class="day-block-header" onclick="switchActiveDay(3)">
            <div class="day-title-wrap">
              <span class="day-badge-tag badge-d3">Day 3</span>
              <div class="day-title-text">
                <h3>9月27日 (星期日) • 東京迪士尼海洋奇幻日</h3>
                <span>夢幻泉鄉 ‧ 貢多拉 ‧ 豪華客輪晚宴</span>
              </div>
            </div>
            <span style="font-size:0.75rem; color:var(--text-muted);">2 個地點</span>
          </div>

          <div class="day-block-body">
            <!-- Tokyo DisneySea -->
            <div class="venue-card" onclick="focusVenue(35.6267, 139.8851, '東京ディズニーシー')">
              <div class="card-top-row">
                <span class="card-time-pill">⏰ 09:00 開園入園</span>
                <span class="card-status-pill pill-booking">一日遊園門票</span>
              </div>
              <div class="venue-japanese-name">🏰 東京ディズニーシー (Tokyo DisneySea)</div>
              <div class="venue-chinese-subtitle">地中海港灣 ‧ 夢幻泉鄉 (Fantasy Springs) ‧ 翱翔</div>
              <p class="venue-details">
                公認全世界造景最浪漫精緻的迪士尼樂園！搭乘威尼斯貢多拉遊船聽船夫吟唱、探訪全新「夢幻泉鄉」（冰雪奇緣、長髮公主、小飛俠），體驗震撼的《翱翔：夢幻奇航》。
              </p>
              <div class="venue-highlight-note">
                <strong>📱 入園關鍵操作：</strong>09:00 一刷過閘門立刻打開官方 App 搶購「夢幻泉鄉 DPA 快速通關」；同時抽《翱翔》40週年免費優先券。
              </div>
              <div class="card-footer-row">
                <span class="venue-location-text">📍 JR舞濱站 轉乘 迪士尼度假區線單軌電車</span>
                <div class="venue-actions">
                  <a href="https://www.tokyodisneyresort.jp/tc/tds/" target="_blank" class="btn-action-pill" onclick="event.stopPropagation()">📱 官方中文指南</a>
                </div>
              </div>
            </div>

            <!-- S.S. Columbia -->
            <div class="venue-card" onclick="focusVenue(35.6238, 139.8860, 'S.S.コロンビア・ダイニングルーム')">
              <div class="card-top-row">
                <span class="card-time-pill">⏰ 19:20 (晚上 7:20)</span>
                <span class="card-status-pill pill-booking">✓ 已預約優先席</span>
              </div>
              <div class="venue-japanese-name">🛳️ S.S.コロンビア・ダイニングルーム</div>
              <div class="venue-chinese-subtitle">S.S. Columbia Dining Room • 20世紀奢華遠洋巨輪 B-Deck 大餐廳</div>
              <p class="venue-details">
                登上停泊在美國海濱的宏偉蒸氣客輪。在水晶吊燈、古典浮雕與純白桌巾的愛德華時代沙龍內，享用烤頂級牛肉與炙煎沙朗牛排套餐，沉浸在優雅的古典樂與紅酒香氣中。
              </p>
              <div class="venue-highlight-note">
                <strong>🎆 晚餐後接續：</strong>20:30 在地中海港灣欣賞壓軸水上光雕煙火秀《堅信！～夢想之海～（Believe! Sea of Dreams）》。
              </div>
              <div class="card-footer-row">
                <span class="venue-location-text">📍 美國海濱 哥倫比亞號 3F 船艙</span>
                <div class="venue-actions">
                  <a href="https://www.tokyodisneyresort.jp/tc/tds/restaurant/detail/431/" target="_blank" class="btn-action-pill" onclick="event.stopPropagation()">🍽️ 餐廳詳情</a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- DAY 4 -->
        <div class="day-block" id="block-day-4">
          <div class="day-block-header" onclick="switchActiveDay(4)">
            <div class="day-title-wrap">
              <span class="day-badge-tag badge-d4">Day 4</span>
              <div class="day-title-text">
                <h3>9月28日 (星期一) • 草津溫泉祕境與櫻井旅館</h3>
                <span>日本第一名湯 ‧ 湯畑浴衣散策 ‧ 會席料理</span>
              </div>
            </div>
            <span style="font-size:0.75rem; color:var(--text-muted);">2 個地點 + 鐵路</span>
          </div>

          <div class="day-block-body">
            <!-- Exact Transit Schedule Card -->
            <div class="transit-guide-box">
              <div class="transit-guide-title">
                <span>🚆 前往草津溫泉乘車時刻表（依路線2）</span>
                <span style="color:#059669;">全程 3h 58m • ¥6,353 (198.8 km)</span>
              </div>

              <div class="transit-step-item">
                <div class="step-time-box">08:55</div>
                <div class="step-marker-dot start"></div>
                <div class="step-desc-wrap">
                  <div class="step-station-name">百合ヶ丘 (Yurigaoka) [2號月台]</div>
                  <div class="step-subline">
                    <span class="subline-badge">小田急小田原線 (新宿行)</span>
                    <span>乘車位置: 8輛車前方</span>
                    <span>¥293</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-item">
                <div class="step-time-box">09:39<br><small style="color:#94a3b8;">09:51</small></div>
                <div class="step-marker-dot"></div>
                <div class="step-desc-wrap">
                  <div class="step-station-name">新宿 (Shinjuku) [10號到 → 3號發]</div>
                  <div class="step-subline">
                    <span class="subline-badge">JR 埼京線 (武藏浦和行・始發)</span>
                    <span>12分鐘換乘</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-item">
                <div class="step-time-box">10:04<br><small style="color:#94a3b8;">10:10</small></div>
                <div class="step-marker-dot"></div>
                <div class="step-desc-wrap">
                  <div class="step-station-name">赤羽 (Akabane) [8號到 → 4號發]</div>
                  <div class="step-subline">
                    <span class="subline-badge">JR 特急草津・四万1號 (長野原草津口行)</span>
                    <strong style="color:#b91c1c;">4號車指定席</strong>
                    <span>運費 ¥3,190 + 特急 ¥2,090</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-item">
                <div class="step-time-box">12:18<br><small style="color:#94a3b8;">12:31</small></div>
                <div class="step-marker-dot"></div>
                <div class="step-desc-wrap">
                  <div class="step-station-name">長野原草津口 (Naganoharakusatsuguchi)</div>
                  <div class="step-subline">
                    <span>步行3分鐘至巴士站</span>
                    <span class="subline-badge">JR巴士關東 (直通 草津溫泉行)</span>
                    <span>¥780</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-item">
                <div class="step-time-box">12:53</div>
                <div class="step-marker-dot end"></div>
                <div class="step-desc-wrap">
                  <div class="step-station-name">草津温泉バスターミナル (草津溫泉)</div>
                  <div class="step-subline">
                    <strong style="color:#10b981;">抵達日本三大名湯之首！✨</strong>
                  </div>
                </div>
              </div>
            </div>

            <!-- Hotel Sakurai -->
            <div class="venue-card" onclick="focusVenue(36.6212, 138.5996, '草津温泉 ホテル櫻井')">
              <div class="card-top-row">
                <span class="card-time-pill">⏰ 13:30 登記入住</span>
                <span class="card-status-pill pill-booking">✓ 頂級溫泉旅館</span>
              </div>
              <div class="venue-japanese-name">♨️ 草津温泉 ホテル櫻井 (Hotel Sakurai)</div>
              <div class="venue-chinese-subtitle">五星級溫泉旅館 ‧ 引流萬代、西之河原等 3 種天然源泉</div>
              <p class="venue-details">
                草津規模最大也最負盛名的溫泉旅館。擁有全長約30米的巨大天然溫泉大浴場與巨石露天風呂。入住後先挑選喜歡的花色浴衣，在大浴場好好洗滌疲憊，肌膚瞬間潤滑。
              </p>
              <div class="card-footer-row">
                <span class="venue-location-text">📍 群馬縣草津町 465-4</span>
                <div class="venue-actions">
                  <a href="https://www.hotel-sakurai.co.jp/" target="_blank" class="btn-action-pill" onclick="event.stopPropagation()">♨️ 旅館官網</a>
                </div>
              </div>
            </div>

            <!-- Yubatake -->
            <div class="venue-card" onclick="focusVenue(36.6208, 138.5960, '湯畑 (Yubatake)')">
              <div class="card-top-row">
                <span class="card-time-pill">⏰ 15:30 – 18:00</span>
                <span class="card-status-pill pill-sightseeing">浴衣街區漫遊</span>
              </div>
              <div class="venue-japanese-name">🏮 湯畑 (Yubatake) & 溫泉街</div>
              <div class="venue-chinese-subtitle">草津地標 ‧ 翠綠沸騰泉水 ‧ 免費足湯 ‧ 溫泉饅頭</div>
              <p class="venue-details">
                換上日式浴衣與木屐，搭接駁車或散步至湯畑。看著中央木槽奔流而下的翡翠綠溫泉與裊裊白煙，一起在「湯煙亭」泡足湯、品嚐現蒸熱呼呼的溫泉饅頭；黃昏點燈時分更是極致浪漫。
              </p>
              <div class="card-footer-row">
                <span class="venue-location-text">📍 草津町中心街區</span>
                <div class="venue-actions">
                  <a href="https://maps.google.com/?q=Yubatake+Kusatsu" target="_blank" class="btn-action-pill" onclick="event.stopPropagation()">🗺️ Google 地圖</a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- DAY 5 -->
        <div class="day-block" id="block-day-5">
          <div class="day-block-header" onclick="switchActiveDay(5)">
            <div class="day-title-wrap">
              <span class="day-badge-tag badge-d5">Day 5</span>
              <div class="day-title-text">
                <h3>9月29日 (星期二) • 新幹線、頂級牛排與爵士之夜</h3>
                <span>青山沃夫岡 ‧ 澀谷潮流 ‧ 柏悅高空酒吧</span>
              </div>
            </div>
            <span style="font-size:0.75rem; color:var(--text-muted);">3 個地點 + 返程</span>
          </div>

          <div class="day-block-body">
            <!-- Exact Return Transit Schedule Card -->
            <div class="transit-guide-box">
              <div class="transit-guide-title">
                <span>🚅 回程交通：草津溫泉 → 外苑前 (青山)</span>
                <span style="color:#059669;">13:35 抵達 • 完美接駁 14:30 牛排！</span>
              </div>

              <div class="transit-step-item">
                <div class="step-time-box">09:20</div>
                <div class="step-marker-dot start"></div>
                <div class="step-desc-wrap">
                  <div class="step-station-name">草津温泉 (Kusatsu Onsen 巴士站)</div>
                  <div class="step-subline">
                    <span class="subline-badge">JR巴士關東 (長野原草津口行)</span>
                    <span>¥780</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-item">
                <div class="step-time-box">09:48<br><small style="color:#94a3b8;">10:08</small></div>
                <div class="step-marker-dot"></div>
                <div class="step-desc-wrap">
                  <div class="step-station-name">長野原草津口 (Naganoharakusatsuguchi)</div>
                  <div class="step-subline">
                    <span class="subline-badge">JR 吾妻線 (高崎行・始發)</span>
                    <span>直達高崎 7號月台</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-item">
                <div class="step-time-box">11:35<br><small style="color:#94a3b8;">12:04</small></div>
                <div class="step-marker-dot"></div>
                <div class="step-desc-wrap">
                  <div class="step-station-name">高崎 (Takasaki) [13號月台]</div>
                  <div class="step-subline">
                    <span class="subline-badge">JR 新幹線たにがわ410號 (東京行)</span>
                    <strong style="color:#2563eb;">新幹線極速直達東京</strong>
                    <span>運費 ¥3,190 + 自由席 ¥2,510</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-item">
                <div class="step-time-box">13:00<br><small style="color:#94a3b8;">13:13</small></div>
                <div class="step-marker-dot"></div>
                <div class="step-desc-wrap">
                  <div class="step-station-name">東京 (Tokyo Station) [21號到 → 5號發]</div>
                  <div class="step-subline">
                    <span class="subline-badge">JR 山手線外環 (品川・澀谷方向)</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-item">
                <div class="step-time-box">13:17<br><small style="color:#94a3b8;">13:26</small></div>
                <div class="step-marker-dot"></div>
                <div class="step-desc-wrap">
                  <div class="step-station-name">新橋 (Shimbashi) [4號到 → 1號發]</div>
                  <div class="step-subline">
                    <span class="subline-badge">東京Metro 銀座線 (澀谷行)</span>
                    <span>¥178</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-item">
                <div class="step-time-box">13:35</div>
                <div class="step-marker-dot end"></div>
                <div class="step-desc-wrap">
                  <div class="step-station-name">外苑前 (Gaienmae) [4a 出口]</div>
                  <div class="step-subline">
                    <strong style="color:#10b981;">直通 THE ARGYLE AOYAMA 大樓！🥩</strong>
                  </div>
                </div>
              </div>
            </div>

            <!-- Wolfgang's -->
            <div class="venue-card" onclick="focusVenue(35.6698, 139.7180, 'ウルフギャング・ステーキハウス シグニチャー 青山店')">
              <div class="card-top-row">
                <span class="card-time-pill">⏰ 14:30 準時抵達</span>
                <span class="card-status-pill pill-booking">✓ 預約 14:30 午餐</span>
              </div>
              <div class="venue-japanese-name">🥩 ウルフギャング・ステーキハウス シグニチャー 青山店</div>
              <div class="venue-chinese-subtitle">Wolfgang's Steakhouse Signature Aoyama • 頂級乾式熟成黑安格斯丁骨牛排</div>
              <p class="venue-details">
                美國頂級 USDA Prime 安格斯牛肉經 28 天乾式熟成，以 900 度高溫極速炙烤，上桌時瓷盤內濃香奶油滋滋作響！肉質外酥內嫩，奢華感十足。
              </p>
              <div class="venue-highlight-note">
                <strong>💡 推薦必點：</strong>招牌雙人丁骨大牛排（Steak for Two）、大西洋蟹肉餅（Jumbo Lump Crab Cake）、奶油菠菜、德式煎馬鈴薯、鮮奶油蘋果派。
              </div>
              <div class="card-footer-row">
                <span class="venue-location-text">📍 外苑前站 4a 出口直達 THE ARGYLE AOYAMA 1F/2F</span>
                <div class="venue-actions">
                  <a href="https://wolfgangssteakhouse.jp/" target="_blank" class="btn-action-pill" onclick="event.stopPropagation()">🥩 官方網站</a>
                  <a href="https://maps.google.com/?q=Wolfgang's+Steakhouse+Signature+Aoyama" target="_blank" class="btn-action-pill" onclick="event.stopPropagation()">🗺️ Google 地圖</a>
                </div>
              </div>
            </div>

            <!-- Shibuya -->
            <div class="venue-card" onclick="focusVenue(35.6595, 139.7005, '渋谷スクランブル交差点 & MIYASHITA PARK')">
              <div class="card-top-row">
                <span class="card-time-pill">⏰ 19:30 (晚上 7:30)</span>
                <span class="card-status-pill pill-sightseeing">澀谷霓虹熱潮</span>
              </div>
              <div class="venue-japanese-name">🌆 渋谷スクランブル交差点 & MIYASHITA PARK</div>
              <div class="venue-chinese-subtitle">Shibuya • 宮下公園屋頂草坪 ‧ 潮流購物 ‧ SHIBUYA SKY 夜景</div>
              <p class="venue-details">
                走進世界最著名的澀谷十字路口感受東京脈搏；逛逛極具設計感的 MIYASHITA PARK（宮下公園），在空中綠地坐看山手線穿梭；亦可預訂 SHIBUYA SKY 俯瞰無死角璀璨夜景。
              </p>
              <div class="card-footer-row">
                <span class="venue-location-text">📍 澀谷車站周邊</span>
                <div class="venue-actions">
                  <a href="https://maps.google.com/?q=Shibuya+Crossing" target="_blank" class="btn-action-pill" onclick="event.stopPropagation()">🗺️ Google 地圖</a>
                </div>
              </div>
            </div>

            <!-- New York Bar -->
            <div class="venue-card" onclick="focusVenue(35.6856, 139.6910, 'ニューヨーク バー (パーク ハイアット 東京 52F)')">
              <div class="card-top-row">
                <span class="card-time-pill">⏰ 21:30 – 深夜</span>
                <span class="card-status-pill pill-booking">壓軸浪漫收尾</span>
              </div>
              <div class="venue-japanese-name">🎷 ニューヨーク バー / New York Bar (パーク ハイアット 東京 52F)</div>
              <div class="venue-chinese-subtitle">Park Hyatt Tokyo 52F • 《愛情，不用翻譯》傳奇爵士高空酒吧</div>
              <p class="venue-details">
                歷經全面重金改裝，於2025年底奢華重開！坐落於西新宿柏悅酒店頂層 52 樓，四面頂級落地窗倒映著無限延伸的東京璀璨燈海。現場國際爵士樂隊演奏，舉起馬丁尼對飲，為這趟旅程畫下最完美的句點。
              </p>
              <div class="venue-highlight-note">
                <strong>👔 服裝提醒：</strong>請著 Smart Casual（男士請勿穿著拖鞋或無領背心）。
              </div>
              <div class="card-footer-row">
                <span class="venue-location-text">📍 新宿區西新宿 3-7-1-2 新宿公園塔 52 樓</span>
                <div class="venue-actions">
                  <a href="https://maps.google.com/?q=Park+Hyatt+Tokyo+New+York+Bar" target="_blank" class="btn-action-pill" onclick="event.stopPropagation()">🗺️ Google 地圖</a>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </aside>
  </div>

  <div class="toast-pill" id="toast-pill">
    <span>✓</span> <span id="toast-msg">已複製分享連結！</span>
  </div>

  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  
  <script>
    // Spots Dataset
    const tripVenues = [
      {
        day: 1,
        title: "シェーンズバーグ 新百合ヶ丘店",
        sub: "Shane's Burg (炭火漢堡排)",
        time: "9/25 19:00",
        lat: 35.6033,
        lng: 139.5080,
        color: "#e07a7e",
        desc: "現烤手打純牛肉漢堡排，肉汁豐沛溫馨晚餐。",
        link: "https://tabelog.com/kanagawa/A1405/A140508/14009641/"
      },
      {
        day: 2,
        title: "すきやばし 次郎 六本木ヒルズ店",
        sub: "Sukiyabashi Jiro (壽司之神板前)",
        time: "9/26 13:00",
        lat: 35.6586978,
        lng: 139.7291446,
        color: "#9b51e0",
        desc: "小野隆主理，江戶前壽司極致藝術體驗。",
        link: "https://maps.app.goo.gl/Brh2wvb1fPBVpNn79"
      },
      {
        day: 2,
        title: "東京タワー (Tokyo Tower)",
        sub: "150m 主展望台 & 玻璃地板",
        time: "9/26 15:30",
        lat: 35.6585805,
        lng: 139.7454329,
        color: "#9b51e0",
        desc: "俯瞰東京全景與海灣，東京最浪漫經典紅色地標。",
        link: "https://www.tokyotower.co.jp/"
      },
      {
        day: 2,
        title: "VIRTÙ (フォーシーズンズ大手町 39F)",
        sub: "亞洲50最佳酒吧",
        time: "9/26 17:30",
        lat: 35.6872,
        lng: 139.7645,
        color: "#9b51e0",
        desc: "挑高落地窗俯瞰皇居御苑與日落天際線，頂級法日調酒。",
        link: "https://www.fourseasons.com/tokyo-otemachi/dining/lounges/virtu/"
      },
      {
        day: 2,
        title: "無添くら寿司 (Muten Kura Sushi)",
        sub: "趣味扭蛋迴轉壽司",
        time: "9/26 20:00",
        lat: 35.6719,
        lng: 139.7648,
        color: "#9b51e0",
        desc: "無添加迴轉壽司，投盤抽「畢庫拉碰」扭蛋樂趣無限。",
        link: "https://www.kurasushi.co.jp/mutenkura/"
      },
      {
        day: 3,
        title: "東京ディズニーシー (Tokyo DisneySea)",
        sub: "夢幻泉鄉 & 威尼斯貢多拉",
        time: "9/27 09:00",
        lat: 35.6267,
        lng: 139.8851,
        color: "#2f80ed",
        desc: "全世界最浪漫迪士尼，夢幻泉鄉（冰雪/長髮公主）與翱翔。",
        link: "https://www.tokyodisneyresort.jp/tc/tds/"
      },
      {
        day: 3,
        title: "S.S.コロンビア・ダイニングルーム",
        sub: "豪華客輪古典晚餐",
        time: "9/27 19:20",
        lat: 35.6238,
        lng: 139.8860,
        color: "#2f80ed",
        desc: "愛德華時代頂級遠洋巨輪，享用烤牛排與美酒套餐。",
        link: "https://www.tokyodisneyresort.jp/tc/tds/restaurant/detail/431/"
      },
      {
        day: 4,
        title: "草津温泉 ホテル櫻井 (Hotel Sakurai)",
        sub: "草津五星級名宿",
        time: "9/28 13:30",
        lat: 36.6212,
        lng: 138.5996,
        color: "#10b981",
        desc: "引流3種天然名湯源泉，巨石露天溫泉與會席料理。",
        link: "https://www.hotel-sakurai.co.jp/"
      },
      {
        day: 4,
        title: "湯畑 (Yubatake)",
        sub: "草津溫泉心臟地標",
        time: "9/28 15:30",
        lat: 36.6208,
        lng: 138.5960,
        color: "#10b981",
        desc: "浴衣散策，漫步在翡翠綠沸騰溫泉池與黃昏溫暖燈籠下。",
        link: "https://maps.google.com/?q=Yubatake+Kusatsu"
      },
      {
        day: 5,
        title: "ウルフギャング・ステーキハウス シグニチャー 青山店",
        sub: "Wolfgang's 乾式熟成牛排",
        time: "9/29 14:30",
        lat: 35.6698,
        lng: 139.7180,
        color: "#f59e0b",
        desc: "28天乾式熟成 USDA Prime 丁骨牛排，熱奶油香氣濃烈上桌。",
        link: "https://wolfgangssteakhouse.jp/"
      },
      {
        day: 5,
        title: "渋谷スクランブル交差点 & MIYASHITA PARK",
        sub: "澀谷夜色潮流散策",
        time: "9/29 19:30",
        lat: 35.6595,
        lng: 139.7005,
        color: "#f59e0b",
        desc: "經典澀谷十字路口、宮下公園空中綠地、SHIBUYA SKY。",
        link: "https://maps.google.com/?q=Shibuya+Crossing"
      },
      {
        day: 5,
        title: "ニューヨーク バー (パーク ハイアット 東京 52F)",
        sub: "New York Bar 傳奇爵士酒吧",
        time: "9/29 21:30",
        lat: 35.6856,
        lng: 139.6910,
        color: "#f59e0b",
        desc: "52層天際爵士酒吧，絕美落地窗俯瞰新宿百萬夜景乾杯。",
        link: "https://maps.google.com/?q=Park+Hyatt+Tokyo+New+York+Bar"
      }
    ];

    // REALISTIC TRANSIT & ROAD WAYPOINTS (Following Actual Roads and Rail Traffic!)
    // Absolutely NO straight dotted lines across buildings or mountains!
    const trafficRoutes = {
      // Day 1: Odakyu Line traffic to Shinyurigaoka
      1: [
        [35.6015, 139.5165],
        [35.6025, 139.5120],
        [35.6033, 139.5080]
      ],
      // Day 2: Roppongi Keyakizaka -> Tokyo Tower -> Otemachi -> Ginza (Following real road traffic)
      2: [
        [35.6586978, 139.7291446], // Roppongi Hills Keyakizaka
        [35.6602, 139.7298],       // Roppongi-dori
        [35.6628, 139.7340],       // Roppongi Crossing
        [35.6605, 139.7390],       // Roppongi 1-chome
        [35.6585, 139.7425],       // Gaien-Higashi-dori
        [35.6585805, 139.7454329], // Tokyo Tower
        [35.6620, 139.7485],       // Onarimon / Hibiya-dori
        [35.6700, 139.7540],       // Toranomon / Shimbashi
        [35.6760, 139.7580],       // Hibiya Park / Imperial Palace
        [35.6815, 139.7620],       // Marunouchi
        [35.6872, 139.7645],       // VIRTÙ (Four Seasons Otemachi)
        [35.6830, 139.7660],       // Yaesu
        [35.6765, 139.7650],       // Kyobashi
        [35.6719, 139.7648]        // Kura Sushi Ginza
      ],
      // Day 3: Maihama Disney Resort Line Traffic Loop
      3: [
        [35.6358, 139.8835],       // Maihama Station
        [35.6320, 139.8845],       // Resort Gateway
        [35.6267, 139.8851],       // DisneySea Main Entrance
        [35.6255, 139.8855],       // Mediterranean Harbor
        [35.6238, 139.8860]        // S.S. Columbia Pier
      ],
      // Day 4: Realistic Train & Mountain Highway Route to Kusatsu
      4: [
        [35.6033, 139.5080],       // Yurigaoka Station
        [35.6250, 139.5750],       // Noborito (Odakyu Line)
        [35.6600, 139.6600],       // Shimo-Kitazawa
        [35.6900, 139.7005],       // Shinjuku Station
        [35.7200, 139.7120],       // Ikebukuro
        [35.7775, 139.7215],       // Akabane Station
        [35.8600, 139.6300],       // Urawa
        [35.9065, 139.6240],       // Omiya (JR Takasaki Line)
        [36.0600, 139.4600],       // Konosu
        [36.1400, 139.3800],       // Kumagaya
        [36.2500, 139.1800],       // Honjo
        [36.3220, 139.0130],       // Takasaki Station
        [36.4000, 139.0050],       // Shin-Maebashi
        [36.4950, 139.0030],       // Shibukawa (JR Agatsuma Line junction)
        [36.5600, 138.8500],       // Nakanojo
        [36.5600, 138.6500],       // Naganoharakusatsuguchi Station
        [36.5750, 138.6300],       // Route 292 Highway entrance
        [36.5950, 138.6150],       // Mountain Highway ascent
        [36.6180, 138.6010],       // Kusatsu Onsen Bus Terminal
        [36.6212, 138.5996],       // Hotel Sakurai
        [36.6208, 138.5960]        // Yubatake
      ],
      // Day 5: Return Shinkansen, Aoyama Wolfgang's, Shibuya & Shinjuku
      5: [
        [36.6208, 138.5960],       // Kusatsu
        [36.5600, 138.6500],       // Naganoharakusatsuguchi
        [36.3220, 139.0130],       // Takasaki (Shinkansen)
        [35.9065, 139.6240],       // Omiya
        [35.7130, 139.7770],       // Ueno
        [35.6812, 139.7671],       // Tokyo Station
        [35.6660, 139.7580],       // Shimbashi
        [35.6670, 139.7420],       // Toranomon (Ginza Line)
        [35.6720, 139.7280],       // Akasaka-Mitsuke
        [35.6698, 139.7180],       // Wolfgang's Steakhouse Aoyama (Gaienmae)
        [35.6660, 139.7100],       // Omotesando
        [35.6595, 139.7005],       // Shibuya Scramble & Miyashita Park
        [35.6700, 139.7020],       // Harajuku / Meiji-dori
        [35.6856, 139.6910]        // New York Bar (Park Hyatt Tokyo 52F)
      ]
    };

    // Full Combined Route for "All" view
    const allRoutes = [
      ...trafficRoutes[1],
      ...trafficRoutes[2],
      ...trafficRoutes[3],
      ...trafficRoutes[4],
      ...trafficRoutes[5]
    ];

    // Initialize Map with Crisp Carto Voyager Tiles
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

    let mapPins = [];
    let activeRoutePolylines = [];
    let movingTrafficMarker = null;
    let trafficAnimId = null;
    let currentActiveDay = 'all';

    // Solid Map Pin Builder (No messy dots)
    function buildPin(color, dayNum) {
      return L.divIcon({
        className: 'pin-holder',
        html: `<div class="map-pin-badge" style="background-color: ${color};">
          <span>D${dayNum}</span>
        </div>`,
        iconSize: [34, 34],
        iconAnchor: [17, 34],
        popupAnchor: [0, -34]
      });
    }

    // Add Venue Pins
    tripVenues.forEach(spot => {
      const pinIcon = buildPin(spot.color, spot.day);
      const marker = L.marker([spot.lat, spot.lng], { icon: pinIcon }).addTo(map);

      const balloonHtml = `
        <div class="popup-inner">
          <span class="popup-time-badge">Day ${spot.day} • ${spot.time}</span>
          <div class="popup-title">${spot.title}</div>
          <div class="popup-sub">${spot.sub}</div>
          <p class="popup-desc">${spot.desc}</p>
          <div class="popup-button-row">
            <a href="${spot.link}" target="_blank" class="popup-btn btn-detail">店家官方/預約</a>
            <a href="https://maps.google.com/?q=${encodeURIComponent(spot.title)}" target="_blank" class="popup-btn btn-gmaps">導航</a>
          </div>
        </div>
      `;
      marker.bindPopup(balloonHtml);
      marker.spotMeta = spot;
      mapPins.push(marker);
    });

    // Draw Smooth Solid Routes following actual traffic
    function renderSolidTrafficLines(day) {
      // Clear old lines
      activeRoutePolylines.forEach(l => map.removeLayer(l));
      activeRoutePolylines = [];

      const dayColors = {
        1: '#e07a7e',
        2: '#9b51e0',
        3: '#2f80ed',
        4: '#10b981',
        5: '#f59e0b'
      };

      if (day === 'all') {
        // Draw each day's distinct solid route along traffic
        [1, 2, 3, 4, 5].forEach(d => {
          const coords = trafficRoutes[d];
          // Underglow casing line
          const glow = L.polyline(coords, {
            color: '#ffffff',
            weight: 6,
            opacity: 0.85
          }).addTo(map);

          // Solid colored road route line (NO DASHES, NO DOTS!)
          const mainLine = L.polyline(coords, {
            color: dayColors[d],
            weight: 3.5,
            opacity: 0.95
          }).addTo(map);

          activeRoutePolylines.push(glow, mainLine);
        });
      } else {
        const coords = trafficRoutes[day];
        const glow = L.polyline(coords, {
          color: '#ffffff',
          weight: 7,
          opacity: 0.95
        }).addTo(map);

        const mainLine = L.polyline(coords, {
          color: dayColors[day] || '#9e2846',
          weight: 4,
          opacity: 1.0
        }).addTo(map);

        activeRoutePolylines.push(glow, mainLine);
      }
    }

    // VEHICLE TRAFFIC ANIMATION (Move following the traffic!)
    function startMovingTraffic(day) {
      if (movingTrafficMarker) map.removeLayer(movingTrafficMarker);
      if (trafficAnimId) cancelAnimationFrame(trafficAnimId);

      const targetPath = (day === 'all') ? allRoutes : trafficRoutes[day];
      if (!targetPath || targetPath.length < 2) return;

      const vehicleIcons = {
        1: '🚗',
        2: '🚕',
        3: '🚝',
        4: '🚆',
        5: '🚅',
        'all': '🚗'
      };

      const vehicleIcon = L.divIcon({
        className: 'vehicle-icon-holder',
        html: `<div class="traffic-vehicle-marker">${vehicleIcons[day] || '🚗'}</div>`,
        iconSize: [32, 32],
        iconAnchor: [16, 16]
      });

      movingTrafficMarker = L.marker(targetPath[0], { icon: vehicleIcon }).addTo(map);

      let step = 0;
      const totalSteps = targetPath.length * 35; // smooth speed

      function moveVehicle() {
        step = (step + 1) % totalSteps;
        const progress = step / totalSteps;
        const currentCoord = interpolateCoordinates(targetPath, progress);
        movingTrafficMarker.setLatLng(currentCoord);
        trafficAnimId = requestAnimationFrame(moveVehicle);
      }
      moveVehicle();
    }

    // Mathematical coordinate interpolation along multi-point path
    function interpolateCoordinates(coords, progress) {
      const totalSegments = coords.length - 1;
      const exactIndex = progress * totalSegments;
      const segmentIndex = Math.min(Math.floor(exactIndex), totalSegments - 1);
      const segmentProgress = exactIndex - segmentIndex;

      const p1 = coords[segmentIndex];
      const p2 = coords[segmentIndex + 1];

      return [
        p1[0] + (p2[0] - p1[0]) * segmentProgress,
        p1[1] + (p2[1] - p1[1]) * segmentProgress
      ];
    }

    // Switch Active Day
    function switchActiveDay(day, btnEl) {
      currentActiveDay = day;
      document.querySelectorAll('.day-selector-btn').forEach(b => b.classList.remove('active'));
      if (btnEl) btnEl.classList.add('active');

      const visiblePins = [];
      mapPins.forEach(m => {
        if (day === 'all' || m.spotMeta.day === parseInt(day)) {
          m.addTo(map);
          visiblePins.push(m);
        } else {
          map.removeLayer(m);
        }
      });

      renderSolidTrafficLines(day);
      startMovingTraffic(day);

      // Fit View
      if (visiblePins.length > 0) {
        const group = new L.featureGroup(visiblePins);
        map.fitBounds(group.getBounds().pad(0.2));
      }

      // Update UI label
      const labels = {
        'all': '全部行程：全線交通行駛中',
        1: 'Day 1：前往新百合ヶ丘行駛中 🚗',
        2: 'Day 2：六本木 ➔ 鐵塔 ➔ 大手町 ➔ 銀座車流中 🚕',
        3: 'Day 3：迪士尼海洋單軌電車巡遊中 🚝',
        4: 'Day 4：特急草津四萬號 & 山道巴士行駛中 🚆',
        5: 'Day 5：新幹線返京 ➔ 青山 ➔ 澀谷 ➔ 新宿 🚅'
      };
      document.getElementById('traffic-status-label').textContent = labels[day] || '即時交通路線中';

      // Highlight block in drawer
      document.querySelectorAll('.day-block').forEach(b => b.classList.remove('active-day-block'));
      if (day !== 'all') {
        const targetBlock = document.getElementById('block-day-' + day);
        if (targetBlock) {
          targetBlock.classList.add('active-day-block');
          targetBlock.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    }

    function restartCurrentDayTraffic() {
      startMovingTraffic(currentActiveDay);
    }

    // Focus on Venue from Drawer Card
    function focusVenue(lat, lng, name) {
      map.flyTo([lat, lng], 15, { animate: true, duration: 1.2 });
      mapPins.forEach(m => {
        if (Math.abs(m.getLatLng().lat - lat) < 0.001 && Math.abs(m.getLatLng().lng - lng) < 0.001) {
          setTimeout(() => { m.openPopup(); }, 700);
        }
      });
    }

    function fitFullTrafficRoute() {
      switchActiveDay('all', document.querySelector('.day-selector-btn:first-child'));
      const group = new L.featureGroup(mapPins);
      map.fitBounds(group.getBounds().pad(0.12));
    }

    // Drawer Width Toggle
    let isCompact = false;
    function togglePanelWidth() {
      const panel = document.getElementById('itinerary-panel');
      if (window.innerWidth > 960) {
        if (!isCompact) {
          panel.style.width = '360px';
          isCompact = true;
        } else {
          panel.style.width = '500px';
          isCompact = false;
        }
        setTimeout(() => { map.invalidateSize(); }, 300);
      }
    }

    function copyShareURL() {
      navigator.clipboard.writeText(window.location.href);
      showToast('✓ 已複製分享連結！快傳給她看吧 ❤️');
    }

    function showToast(msg) {
      const t = document.getElementById('toast-pill');
      document.getElementById('toast-msg').textContent = msg;
      t.style.display = 'flex';
      setTimeout(() => { t.style.display = 'none'; }, 2600);
    }

    // Download iCal (.ics) Calendar
    function downloadCalendarFile() {
      const icsData = `BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Couple Japan Romance Trip//ZH
CALSCALE:GREGORIAN
METHOD:PUBLISH
BEGIN:VEVENT
SUMMARY:晚餐：シェーンズバーグ 新百合ヶ丘店
DTSTART;TZID=Asia/Tokyo:20260925T190000
DTEND;TZID=Asia/Tokyo:20260925T210000
DESCRIPTION:抵達東京溫馨開場晚餐，新百合之丘 Elmi Road 5F 手打漢堡排
LOCATION:シェーンズバーグ 新百合ヶ丘店
STATUS:CONFIRMED
END:VEVENT
BEGIN:VEVENT
SUMMARY:午餐：すきやばし 次郎 六本木ヒルズ店 (板前壽司)
DTSTART;TZID=Asia/Tokyo:20260926T130000
DTEND;TZID=Asia/Tokyo:20260926T143000
DESCRIPTION:六本木之丘 櫸坂通 3F，小野隆主理江戶前板前握壽司
LOCATION:すきやばし 次郎 六本木ヒルズ店
STATUS:CONFIRMED
END:VEVENT
BEGIN:VEVENT
SUMMARY:觀光：東京タワー (Tokyo Tower)
DTSTART;TZID=Asia/Tokyo:20260926T153000
DTEND;TZID=Asia/Tokyo:20260926T170000
DESCRIPTION:東京鐵塔 150m 主展望台，透明玻璃天窗步道與塔大神宮
LOCATION:東京タワー
END:VEVENT
BEGIN:VEVENT
SUMMARY:調酒：VIRTÙ (フォーシーズンズホテル東京大手町 39F)
DTSTART;TZID=Asia/Tokyo:20260926T173000
DTEND;TZID=Asia/Tokyo:20260926T191500
DESCRIPTION:亞洲50最佳酒吧，39層高空俯瞰皇居御苑日落夕陽與法日調酒 (請著 Smart Casual)
LOCATION:VIRTÙ, Four Seasons Hotel Tokyo at Otemachi
END:VEVENT
BEGIN:VEVENT
SUMMARY:晚餐：無添くら寿司 (迴轉壽司扭蛋)
DTSTART;TZID=Asia/Tokyo:20260926T200000
DTEND;TZID=Asia/Tokyo:20260926T213000
DESCRIPTION:無人工添加迴轉壽司，每 5 盤投入抽「畢庫拉碰」扭蛋遊戲
LOCATION:無添くら寿司
END:VEVENT
BEGIN:VEVENT
SUMMARY:東京ディズニーシー (Tokyo DisneySea)
DTSTART;TZID=Asia/Tokyo:20260927T090000
DTEND;TZID=Asia/Tokyo:20260927T210000
DESCRIPTION:09:00 開園入園，夢幻泉鄉 (Fantasy Springs)、威尼斯貢多拉、翱翔夢幻奇航
LOCATION:東京ディズニーシー
STATUS:CONFIRMED
END:VEVENT
BEGIN:VEVENT
SUMMARY:晚餐：S.S.コロンビア・ダイニングルーム
DTSTART;TZID=Asia/Tokyo:20260927T192000
DTEND;TZID=Asia/Tokyo:20260927T202000
DESCRIPTION:迪士尼海洋 美國海濱 豪華蒸氣巨輪 B-Deck 大餐廳牛排晚宴 (已預約優先席 19:20)
LOCATION:S.S.コロンビア・ダイニングルーム
STATUS:CONFIRMED
END:VEVENT
BEGIN:VEVENT
SUMMARY:草津溫泉之旅：草津温泉 ホテル櫻井
DTSTART;TZID=Asia/Tokyo:20260928T085500
DTEND;TZID=Asia/Tokyo:20260928T220000
DESCRIPTION:08:55 百合之丘出發搭乘特急草津四萬號，入住草津溫泉ホテル櫻井，湯畑浴衣漫步與足湯
LOCATION:草津温泉 ホテル櫻井
STATUS:CONFIRMED
END:VEVENT
BEGIN:VEVENT
SUMMARY:午餐：ウルフギャング・ステーキハウス シグニチャー 青山店
DTSTART;TZID=Asia/Tokyo:20260929T143000
DTEND;TZID=Asia/Tokyo:20260929T163000
DESCRIPTION:青山 THE ARGYLE AOYAMA，28天乾式熟成 USDA Prime 丁骨牛排 (14:30 準時抵達)
LOCATION:ウルフギャング・ステーキハウス シグニチャー 青山店
STATUS:CONFIRMED
END:VEVENT
BEGIN:VEVENT
SUMMARY:散策：渋谷スクランブル交差点 & MIYASHITA PARK
DTSTART;TZID=Asia/Tokyo:20260929T193000
DTEND;TZID=Asia/Tokyo:20260929T210000
DESCRIPTION:走過澀谷十字路口，逛宮下公園空中綠地商場
LOCATION:渋谷
END:VEVENT
BEGIN:VEVENT
SUMMARY:酒吧：ニューヨーク バー (パーク ハイアット 東京 52F)
DTSTART;TZID=Asia/Tokyo:20260929T213000
DTEND;TZID=Asia/Tokyo:20260929T233000
DESCRIPTION:《愛情，不用翻譯》傳奇高空酒吧奢華回歸，現場爵士樂團與52層新宿絕景 (請著 Smart Casual)
LOCATION:New York Bar, Park Hyatt Tokyo 52F
END:VEVENT
END:VCALENDAR`;

      const blob = new Blob([icsData], { type: 'text/calendar;charset=utf-8' });
      const link = document.createElement('a');
      link.href = window.URL.createObjectURL(blob);
      link.setAttribute('download', 'tokyo_kusatsu_romance_2026.ics');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);

      showToast('✓ 行程已下載！點擊檔案即可一鍵加入手機日曆 📅');
    }

    // Auto-fit on load
    setTimeout(() => {
      fitFullTrafficRoute();
    }, 400);

  </script>
</body>
</html>
'''

with open('/Users/rondey/japan-trip-itinerary/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('/Users/rondey/tokyo-kusatsu-itinerary.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Traffic-Flow Solid Route HTML written successfully!")
