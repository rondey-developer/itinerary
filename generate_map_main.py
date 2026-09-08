import json
import os

html_content = '''<!DOCTYPE html>
<html lang="zh-HK">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>東京 & 草津溫泉 浪漫雙人之旅 | 互動地圖行程</title>
  
  <!-- Google Fonts -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Noto+Sans+TC:wght@300;400;500;700;900&family=Noto+Serif+TC:wght@600;700&family=Playfair+Display:ital,wght@0,600;0,700;1,600&display=swap" rel="stylesheet">
  
  <!-- Leaflet CSS -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
  
  <style>
    :root {
      --primary: #a12b48;
      --primary-dark: #7b1d34;
      --primary-light: #fdf2f4;
      --accent-gold: #c79549;
      --accent-gold-light: #fef8ed;
      --accent-blue: #2563eb;
      --accent-emerald: #059669;
      --bg-body: #f8f6f2;
      --bg-card: #ffffff;
      --bg-subtle: #f4f0e8;
      --text-main: #1c1917;
      --text-muted: #6b665f;
      --border-color: #e8e2d8;
      --shadow-sm: 0 2px 8px rgba(28, 25, 23, 0.05);
      --shadow-md: 0 10px 30px rgba(28, 25, 23, 0.08);
      --shadow-lg: 0 18px 45px rgba(28, 25, 23, 0.14);
      --font-serif: 'Noto Serif TC', 'Playfair Display', Georgia, serif;
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

    /* Top Navigation Bar */
    .top-navbar {
      height: 64px;
      background: rgba(255, 255, 255, 0.95);
      backdrop-filter: blur(14px);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 20px;
      z-index: 1000;
      flex-shrink: 0;
      box-shadow: 0 2px 10px rgba(0,0,0,0.03);
    }

    .brand-area {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .brand-title {
      font-family: var(--font-serif);
      font-size: 1.18rem;
      font-weight: 700;
      color: var(--primary);
      letter-spacing: -0.01em;
    }

    .brand-tag {
      font-size: 0.76rem;
      background: var(--accent-gold-light);
      color: #925f16;
      border: 1px solid #f9e2b8;
      padding: 2px 10px;
      border-radius: 20px;
      font-weight: 600;
    }

    .top-actions {
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .btn-nav {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 7px 14px;
      border-radius: 50px;
      font-size: 0.82rem;
      font-weight: 700;
      cursor: pointer;
      text-decoration: none;
      transition: all 0.2s ease;
      border: 1px solid var(--border-color);
      background: #fff;
      color: var(--text-main);
    }

    .btn-nav:hover {
      background: var(--bg-subtle);
      border-color: #d1c7b8;
    }

    .btn-nav-primary {
      background: linear-gradient(135deg, #a12b48 0%, #7b1d34 100%);
      color: #fff;
      border: none;
      box-shadow: 0 3px 10px rgba(161, 43, 72, 0.35);
    }

    .btn-nav-primary:hover {
      transform: translateY(-1px);
      box-shadow: 0 5px 14px rgba(161, 43, 72, 0.45);
    }

    /* Main Split Application Layout: MAP IS MAIN */
    .app-main {
      flex: 1;
      display: flex;
      position: relative;
      overflow: hidden;
    }

    /* Map Stage (Takes center stage / dominant left-center) */
    .map-stage {
      flex: 1;
      height: 100%;
      position: relative;
      z-index: 1;
      background: #e5e9ec;
    }

    #trip-map {
      width: 100%;
      height: 100%;
      z-index: 1;
    }

    /* Floating Map Controls & Day Selector */
    .floating-day-selector {
      position: absolute;
      top: 18px;
      left: 20px;
      z-index: 500;
      display: flex;
      gap: 8px;
      background: rgba(255, 255, 255, 0.94);
      backdrop-filter: blur(16px);
      padding: 6px 8px;
      border-radius: 50px;
      box-shadow: var(--shadow-md);
      border: 1px solid rgba(255, 255, 255, 0.9);
      overflow-x: auto;
      max-width: calc(100% - 40px);
      scrollbar-width: none;
    }
    .floating-day-selector::-webkit-scrollbar { display: none; }

    .day-pill-btn {
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

    .day-pill-btn.active {
      background: var(--primary);
      color: #fff;
      box-shadow: 0 4px 12px rgba(161, 43, 72, 0.35);
    }

    .day-pill-btn:hover:not(.active) {
      background: var(--bg-subtle);
      color: var(--text-main);
    }

    /* Floating Legend / View Switcher */
    .floating-map-legend {
      position: absolute;
      bottom: 24px;
      left: 20px;
      z-index: 500;
      background: rgba(255, 255, 255, 0.92);
      backdrop-filter: blur(12px);
      padding: 10px 16px;
      border-radius: var(--radius-sm);
      box-shadow: var(--shadow-md);
      border: 1px solid var(--border-color);
      font-size: 0.78rem;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .legend-item {
      display: flex;
      align-items: center;
      gap: 5px;
      font-weight: 600;
    }

    .legend-dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }

    /* Side Itinerary Drawer (Collapsible & Scrollable) */
    .itinerary-drawer {
      width: 520px;
      height: 100%;
      background: #ffffff;
      border-left: 1px solid var(--border-color);
      z-index: 600;
      display: flex;
      flex-direction: column;
      box-shadow: -4px 0 25px rgba(0,0,0,0.06);
      transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1);
      flex-shrink: 0;
    }

    .drawer-header {
      padding: 18px 22px;
      border-bottom: 1px solid var(--border-color);
      background: #faf7f2;
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
    }

    .drawer-header h2 {
      font-family: var(--font-serif);
      font-size: 1.25rem;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .drawer-header .drawer-sub {
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-top: 2px;
    }

    .drawer-toggle-btn {
      width: 34px;
      height: 34px;
      border-radius: 50%;
      border: 1px solid var(--border-color);
      background: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
      color: var(--text-muted);
      transition: all 0.2s ease;
    }
    .drawer-toggle-btn:hover {
      background: var(--bg-subtle);
      color: var(--text-main);
    }

    .drawer-scroll-body {
      flex: 1;
      overflow-y: auto;
      padding: 20px;
      display: flex;
      flex-direction: column;
      gap: 20px;
      scroll-behavior: smooth;
    }

    /* Day Accordion Block in Drawer */
    .day-card-group {
      border: 1px solid var(--border-color);
      border-radius: var(--radius-md);
      background: #fff;
      overflow: hidden;
      box-shadow: var(--shadow-sm);
      transition: all 0.25s ease;
    }

    .day-card-group.active-day-group {
      border-color: var(--primary);
      box-shadow: 0 6px 20px rgba(161, 43, 72, 0.12);
    }

    .day-group-header {
      padding: 14px 18px;
      background: #fbf9f6;
      border-bottom: 1px solid var(--border-color);
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
    }

    .day-group-title {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .day-tag-badge {
      font-size: 0.72rem;
      font-weight: 800;
      padding: 4px 10px;
      border-radius: 8px;
      color: #fff;
    }

    .badge-d1 { background: #e07a7e; }
    .badge-d2 { background: #9b51e0; }
    .badge-d3 { background: #2f80ed; }
    .badge-d4 { background: #10b981; }
    .badge-d5 { background: #f59e0b; }

    .day-group-text h3 {
      font-size: 0.96rem;
      font-weight: 800;
      color: var(--text-main);
    }

    .day-group-text span {
      font-size: 0.78rem;
      color: var(--text-muted);
    }

    .day-group-content {
      padding: 16px;
      display: flex;
      flex-direction: column;
      gap: 14px;
    }

    /* Schedule Entry Card */
    .schedule-card {
      border: 1px solid #f0eae1;
      background: #fff;
      border-radius: var(--radius-sm);
      padding: 14px 16px;
      position: relative;
      transition: all 0.2s ease;
      cursor: pointer;
    }

    .schedule-card:hover {
      border-color: var(--accent-gold);
      transform: translateY(-2px);
      box-shadow: var(--shadow-sm);
    }

    .card-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 6px;
    }

    .card-time {
      font-size: 0.8rem;
      font-weight: 800;
      color: var(--primary);
      background: var(--primary-light);
      padding: 2px 8px;
      border-radius: 6px;
      display: inline-flex;
      align-items: center;
      gap: 4px;
    }

    .status-badge {
      font-size: 0.72rem;
      font-weight: 700;
      padding: 2px 8px;
      border-radius: 6px;
    }

    .status-reserved {
      background: #e6f7ef;
      color: #0b784a;
      border: 1px solid #b3e6cc;
    }

    .status-highlight {
      background: #fdf5e6;
      color: #a86500;
      border: 1px solid #f9e2b3;
    }

    .card-shop-name {
      font-size: 1.05rem;
      font-weight: 800;
      color: #1a1816;
      margin-bottom: 2px;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .card-chinese-sub {
      font-size: 0.82rem;
      color: var(--text-muted);
      margin-bottom: 8px;
      font-weight: 500;
    }

    .card-description {
      font-size: 0.84rem;
      color: #4b4845;
      line-height: 1.5;
      margin-bottom: 10px;
    }

    .card-tips-box {
      background: var(--bg-subtle);
      border-left: 3px solid var(--accent-gold);
      border-radius: 4px;
      padding: 8px 12px;
      font-size: 0.78rem;
      color: #5d5955;
      margin-bottom: 10px;
    }

    .card-tips-box strong { color: #222; }

    .card-bottom-bar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-top: 1px solid #f6f2ec;
      padding-top: 10px;
      font-size: 0.78rem;
    }

    .card-loc-text {
      color: var(--text-muted);
      display: flex;
      align-items: center;
      gap: 4px;
    }

    .card-links {
      display: flex;
      gap: 6px;
    }

    .btn-card-link {
      color: var(--primary);
      text-decoration: none;
      font-weight: 700;
      font-size: 0.75rem;
      display: inline-flex;
      align-items: center;
      gap: 4px;
      padding: 3px 8px;
      border-radius: 4px;
      background: var(--bg-subtle);
      border: 1px solid var(--border-color);
      transition: all 0.15s ease;
    }
    .btn-card-link:hover {
      background: var(--primary-light);
      border-color: var(--primary);
    }

    /* Transit Timetable Visualizer in Drawer */
    .transit-block {
      background: #f8fafc;
      border: 1px solid #e2e8f0;
      border-radius: 10px;
      padding: 14px;
      margin: 10px 0;
    }

    .transit-block-head {
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

    .transit-step-row {
      display: flex;
      gap: 12px;
      position: relative;
      padding-bottom: 14px;
    }

    .transit-step-row:last-child { padding-bottom: 0; }

    .transit-step-row::after {
      content: "";
      position: absolute;
      left: 17px;
      top: 22px;
      bottom: -4px;
      width: 2px;
      background: #cbd5e1;
    }
    .transit-step-row:last-child::after { display: none; }

    .step-time {
      font-family: monospace;
      font-size: 0.82rem;
      font-weight: 800;
      color: #0f172a;
      width: 44px;
      text-align: right;
    }

    .step-dot {
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
    .step-dot.start { background: #10b981; box-shadow: 0 0 0 2px #10b981; }
    .step-dot.end { background: #ef4444; box-shadow: 0 0 0 2px #ef4444; }

    .step-info { flex: 1; }
    .step-stn { font-weight: 800; font-size: 0.88rem; color: #1e293b; }
    .step-meta {
      font-size: 0.76rem;
      color: #64748b;
      margin-top: 2px;
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
      align-items: center;
    }

    .train-badge {
      background: #e2e8f0;
      padding: 1px 6px;
      border-radius: 4px;
      font-size: 0.72rem;
      color: #334155;
      font-weight: 700;
    }

    /* Custom Leaflet Pins */
    .custom-map-pin {
      width: 34px;
      height: 34px;
      border-radius: 50% 50% 50% 0;
      transform: rotate(-45deg);
      border: 2px solid #ffffff;
      box-shadow: 0 4px 12px rgba(0,0,0,0.3);
      display: flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }

    .custom-map-pin span {
      transform: rotate(45deg);
      color: #ffffff;
      font-size: 11px;
      font-weight: 900;
      font-family: var(--font-sans);
    }

    /* Leaflet Popup Styling */
    .leaflet-popup-content-wrapper {
      border-radius: 16px;
      padding: 4px;
      box-shadow: 0 12px 30px rgba(0,0,0,0.2);
    }

    .map-balloon {
      font-family: var(--font-sans);
      max-width: 260px;
      padding: 4px;
    }

    .balloon-time {
      font-size: 0.75rem;
      color: var(--primary);
      font-weight: 800;
      margin-bottom: 4px;
      display: inline-block;
      background: var(--primary-light);
      padding: 2px 8px;
      border-radius: 4px;
    }

    .balloon-title {
      font-size: 1.02rem;
      font-weight: 800;
      color: #1a1816;
      margin-bottom: 2px;
    }

    .balloon-subtitle {
      font-size: 0.78rem;
      color: var(--text-muted);
      margin-bottom: 8px;
    }

    .balloon-desc {
      font-size: 0.8rem;
      color: #555;
      line-height: 1.45;
      margin-bottom: 10px;
    }

    .balloon-actions {
      display: flex;
      gap: 6px;
    }

    .balloon-btn {
      flex: 1;
      text-align: center;
      font-size: 0.75rem;
      font-weight: 700;
      padding: 5px 8px;
      border-radius: 6px;
      text-decoration: none;
    }

    .btn-focus {
      background: var(--primary);
      color: #fff;
    }

    .btn-maps {
      background: var(--bg-subtle);
      color: var(--text-main);
      border: 1px solid var(--border-color);
    }

    /* Responsive Mobile Handling */
    @media (max-width: 960px) {
      .app-main {
        flex-direction: column;
      }
      .itinerary-drawer {
        width: 100%;
        height: 52%;
        border-left: none;
        border-top: 1px solid var(--border-color);
      }
      .map-stage {
        height: 48%;
      }
      .floating-day-selector {
        top: 10px;
        left: 10px;
      }
      .floating-map-legend {
        display: none;
      }
    }

    /* Toast Notification */
    .toast-box {
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
    <div class="brand-area">
      <span style="font-size:1.4rem;">🌸</span>
      <div>
        <h1 class="brand-title">東京 & 草津溫泉 浪漫雙人行</h1>
      </div>
      <span class="brand-tag">9/25 – 9/29 • 5天4夜</span>
    </div>

    <div class="top-actions">
      <button class="btn-nav" onclick="fitFullRoute()">
        <span>🗺️ 全程視角</span>
      </button>
      <button class="btn-nav" onclick="downloadCalendarFile()">
        <span>📅 加入日曆 (.ics)</span>
      </button>
      <button class="btn-nav btn-nav-primary" onclick="copyShareURL()">
        <span id="share-btn-text">🔗 分享給女朋友</span>
      </button>
    </div>
  </header>

  <!-- Main Application Body: MAP IS THE MAIN STAGE -->
  <div class="app-main">
    
    <!-- Primary Interactive Map Canvas -->
    <main class="map-stage">
      
      <!-- Floating Day Filters directly on Map -->
      <div class="floating-day-selector">
        <button class="day-pill-btn active" onclick="selectDayFilter('all', this)">
          <span>✨ 全部景點</span>
        </button>
        <button class="day-pill-btn" onclick="selectDayFilter(1, this)">
          <span>9/25 (五) 新百合之夜</span>
        </button>
        <button class="day-pill-btn" onclick="selectDayFilter(2, this)">
          <span>9/26 (六) 壽司 & 鐵塔</span>
        </button>
        <button class="day-pill-btn" onclick="selectDayFilter(3, this)">
          <span>9/27 (日) 迪士尼海洋</span>
        </button>
        <button class="day-pill-btn" onclick="selectDayFilter(4, this)">
          <span>9/28 (一) 草津溫泉</span>
        </button>
        <button class="day-pill-btn" onclick="selectDayFilter(5, this)">
          <span>9/29 (二) 牛排 & 夜景</span>
        </button>
      </div>

      <!-- Interactive Leaflet Map Container -->
      <div id="trip-map"></div>

      <!-- Floating Map Legend -->
      <div class="floating-map-legend">
        <span style="font-weight:700; color:var(--text-main);">路線標記：</span>
        <div class="legend-item"><div class="legend-dot" style="background:#e07a7e;"></div><span>Day 1</span></div>
        <div class="legend-item"><div class="legend-dot" style="background:#9b51e0;"></div><span>Day 2</span></div>
        <div class="legend-item"><div class="legend-dot" style="background:#2f80ed;"></div><span>Day 3</span></div>
        <div class="legend-item"><div class="legend-dot" style="background:#10b981;"></div><span>Day 4</span></div>
        <div class="legend-item"><div class="legend-dot" style="background:#f59e0b;"></div><span>Day 5</span></div>
      </div>
    </main>

    <!-- Detailed Itinerary Sidebar Drawer -->
    <aside class="itinerary-drawer" id="itinerary-drawer">
      <div class="drawer-header">
        <div>
          <h2><span>📋</span> 詳細行程清單</h2>
          <div class="drawer-sub">點選任意行程，地圖將自動飛行導航至該地點</div>
        </div>
        <button class="drawer-toggle-btn" title="切換檢視" onclick="toggleDrawerWidth()">⇋</button>
      </div>

      <div class="drawer-scroll-body" id="drawer-scroll">
        
        <!-- DAY 1 -->
        <div class="day-card-group" id="group-day-1">
          <div class="day-group-header" onclick="selectDayFilter(1)">
            <div class="day-group-title">
              <span class="day-tag-badge badge-d1">Day 1</span>
              <div class="day-group-text">
                <h3>9月25日 (星期五) • 抵達與溫馨晚餐</h3>
                <span>手打漢堡排 ‧ 放鬆安頓</span>
              </div>
            </div>
            <span>📍 1 個地點</span>
          </div>

          <div class="day-group-content">
            <!-- Shane's Burg -->
            <div class="schedule-card" onclick="flyToSpot(35.6033, 139.5080, 'シェーンズバーグ 新百合ヶ丘店')">
              <div class="card-top">
                <span class="card-time">⏰ 19:00 (晚上 7:00)</span>
                <span class="status-badge status-reserved">✓ 已預約晚餐</span>
              </div>
              <div class="card-shop-name">🥩 シェーンズバーグ 新百合ヶ丘店</div>
              <div class="card-chinese-sub">Shane's Burg • 新百合之丘 Elmi Road 5F 美式漢堡排專門店</div>
              <p class="card-description">
                每日嚴選新鮮牛肉在店內手工製作的頂級漢堡排，經炭火現烤香氣濃郁，切開肉汁飽滿。在溫馨輕鬆的木質美式氛圍中，揭開浪漫假期的序幕！
              </p>
              <div class="card-tips-box">
                <strong>💡 推薦點餐：</strong>招牌多蜜醬漢堡排（デミグラス）或日式蒜蓉洋蔥醬，可加融化起司；配酥脆薯塊與生啤酒/Highball。<br>
                <strong>💰 人均預算：</strong>約 ¥1,500 – ¥2,500。
              </div>
              <div class="card-bottom-bar">
                <span class="card-loc-text">📍 小田急線 新百合ヶ丘駅 直通商場 5F</span>
                <div class="card-links">
                  <a href="https://tabelog.com/kanagawa/A1405/A140508/14009641/" target="_blank" class="btn-card-link" onclick="event.stopPropagation()">📖 食べログ</a>
                  <a href="https://maps.google.com/?q=Shane's+Burg+Shin-Yurigaoka" target="_blank" class="btn-card-link" onclick="event.stopPropagation()">🗺️ Google 地圖</a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- DAY 2 -->
        <div class="day-card-group" id="group-day-2">
          <div class="day-group-header" onclick="selectDayFilter(2)">
            <div class="day-group-title">
              <span class="day-tag-badge badge-d2">Day 2</span>
              <div class="day-group-text">
                <h3>9月26日 (星期六) • 壽司之神、鐵塔與高空酒吧</h3>
                <span>米其林板前 ‧ 浪漫地標 ‧ 亞洲50強酒吧</span>
              </div>
            </div>
            <span>📍 4 個地點</span>
          </div>

          <div class="day-group-content">
            <!-- Sukiyabashi Jiro -->
            <div class="schedule-card" onclick="flyToSpot(35.6586978, 139.7291446, 'すきやばし 次郎 六本木ヒルズ店')">
              <div class="card-top">
                <span class="card-time">⏰ 13:00 (下午 1:00)</span>
                <span class="status-badge status-reserved">✓ 已預約板前席</span>
              </div>
              <div class="card-shop-name">🍣 すきやばし 次郎 六本木ヒルズ店</div>
              <div class="card-chinese-sub">Sukiyabashi Jiro • 六本木之丘 櫸坂通 3F 江戶前壽司</div>
              <p class="card-description">
                世界傳奇「壽司之神」小野二郎之子——小野隆主理。極致純粹的江戶前板前握壽司，米飯溫度精準，魚生刀工絕倫，是一生難忘的頂級味蕾盛宴。
              </p>
              <div class="card-tips-box">
                <strong>💡 禮儀小貼士：</strong>師傅刷好醬汁握好送上後，建議在數秒內以手或筷直接入口享用最佳溫度；店內禁止噴過濃香水。
              </div>
              <div class="card-bottom-bar">
                <span class="card-loc-text">📍 六本木ヒルズ けやき坂通り 3F</span>
                <div class="card-links">
                  <a href="https://maps.app.goo.gl/Brh2wvb1fPBVpNn79" target="_blank" class="btn-card-link" onclick="event.stopPropagation()">🗺️ Google 地圖</a>
                </div>
              </div>
            </div>

            <!-- Tokyo Tower -->
            <div class="schedule-card" onclick="flyToSpot(35.6585805, 139.7454329, '東京タワー')">
              <div class="card-top">
                <span class="card-time">⏰ 15:30 – 17:00</span>
                <span class="status-badge status-highlight">東京浪漫象徵</span>
              </div>
              <div class="card-shop-name">🗼 東京タワー (Tokyo Tower)</div>
              <div class="card-chinese-sub">Main Deck 150m 展望台 ‧ 透明玻璃步道</div>
              <p class="card-description">
                從六本木搭乘計程車約10分鐘即可抵達。登上 150 米主展望台俯瞰東京全景與台場海灣，走在驚險的透明玻璃地板合影，並參拜東京最高的戀愛神社「タワー大神宮」。
              </p>
              <div class="card-bottom-bar">
                <span class="card-loc-text">📍 港區芝公園 4-2-8</span>
                <div class="card-links">
                  <a href="https://www.tokyotower.co.jp/" target="_blank" class="btn-card-link" onclick="event.stopPropagation()">🌐 官方網站</a>
                </div>
              </div>
            </div>

            <!-- VIRTU -->
            <div class="schedule-card" onclick="flyToSpot(35.6872, 139.7645, 'VIRTÙ (フォーシーズンズホテル東京大手町)')">
              <div class="card-top">
                <span class="card-time">⏰ 17:30 – 19:15</span>
                <span class="status-badge status-highlight">亞洲50最佳酒吧</span>
              </div>
              <div class="card-shop-name">🍸 VIRTÙ (フォーシーズンズホテル東京大手町 39F)</div>
              <div class="card-chinese-sub">Four Seasons Hotel Tokyo at Otemachi • 法日融合巴黎沙龍風</div>
              <p class="card-description">
                名列「亞洲50佳酒吧」榜單！挑高雙層落地窗俯瞰皇居御苑與新宿天際線晚霞。室內兼具1920年代巴黎裝飾藝術與現代摩登氣派，品味獨創的《Smoked Ume Fashioned》調酒。
              </p>
              <div class="card-tips-box">
                <strong>👔 服裝要求（Smart Casual）：</strong>男士請著長褲與有領襯衫、休閒皮鞋（勿穿拖鞋、短褲）；女士建議典雅洋裝或精緻便服。
              </div>
              <div class="card-bottom-bar">
                <span class="card-loc-text">📍 大手町 1-2-1 酒店 39 樓</span>
                <div class="card-links">
                  <a href="https://www.fourseasons.com/tokyo-otemachi/dining/lounges/virtu/" target="_blank" class="btn-card-link" onclick="event.stopPropagation()">🍸 酒單預覽</a>
                </div>
              </div>
            </div>

            <!-- Kura Sushi -->
            <div class="schedule-card" onclick="flyToSpot(35.6719, 139.7648, '無添くら寿司')">
              <div class="card-top">
                <span class="card-time">⏰ 20:00 (晚上 8:00)</span>
                <span class="status-badge status-reserved">趣味歡樂晚餐</span>
              </div>
              <div class="card-shop-name">🍣 無添くら寿司 (Muten Kura Sushi)</div>
              <div class="card-chinese-sub">無人工添加物迴轉壽司 ‧ 必玩「畢庫拉碰」扭蛋遊戲</div>
              <p class="card-description">
                與中午的極上板前形成可愛的反差萌！全品項無人工添加的美味迴轉壽司，每吃完 5 盤投入回收口，螢幕就會自動啟動抽獎動畫，情侶一起挑戰扭蛋超有樂趣！
              </p>
              <div class="card-bottom-bar">
                <span class="card-loc-text">📍 東京旗艦店 / 銀座店</span>
                <div class="card-links">
                  <a href="https://www.kurasushi.co.jp/mutenkura/" target="_blank" class="btn-card-link" onclick="event.stopPropagation()">🌐 官方網站</a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- DAY 3 -->
        <div class="day-card-group" id="group-day-3">
          <div class="day-group-header" onclick="selectDayFilter(3)">
            <div class="day-group-title">
              <span class="day-tag-badge badge-d3">Day 3</span>
              <div class="day-group-text">
                <h3>9月27日 (星期日) • 東京迪士尼海洋奇幻日</h3>
                <span>夢幻泉鄉 ‧ 貢多拉 ‧ 豪華郵輪晚宴</span>
              </div>
            </div>
            <span>📍 2 個主要點</span>
          </div>

          <div class="day-group-content">
            <!-- Tokyo DisneySea -->
            <div class="schedule-card" onclick="flyToSpot(35.6267, 139.8851, '東京ディズニーシー')">
              <div class="card-top">
                <span class="card-time">⏰ 09:00 開園入園</span>
                <span class="status-badge status-reserved">一日遊園門票</span>
              </div>
              <div class="card-shop-name">🏰 東京ディズニーシー (Tokyo DisneySea)</div>
              <div class="card-chinese-sub">地中海港灣 ‧ 夢幻泉鄉 (Fantasy Springs) ‧ 翱翔</div>
              <p class="card-description">
                公認全世界造景最浪漫精緻的迪士尼樂園！搭乘威尼斯貢多拉遊船聽船夫吟唱、探訪全新「夢幻泉鄉」（冰雪奇緣、長髮公主、小飛俠），體驗震撼的《翱翔：夢幻奇航》。
              </p>
              <div class="card-tips-box">
                <strong>📱 入園關鍵操作：</strong>09:00 一刷過閘門立刻打開官方 App 搶購「夢幻泉鄉 DPA 快速通關」或預約排隊券；同時抽《翱翔》40週年免費優先券。
              </div>
              <div class="card-bottom-bar">
                <span class="card-loc-text">📍 JR舞濱站 轉乘 迪士尼度假區線單軌電車</span>
                <div class="card-links">
                  <a href="https://www.tokyodisneyresort.jp/tc/tds/" target="_blank" class="btn-card-link" onclick="event.stopPropagation()">📱 官方中文指南</a>
                </div>
              </div>
            </div>

            <!-- S.S. Columbia -->
            <div class="schedule-card" onclick="flyToSpot(35.6238, 139.8860, 'S.S.コロンビア・ダイニングルーム')">
              <div class="card-top">
                <span class="card-time">⏰ 19:20 (晚上 7:20)</span>
                <span class="status-badge status-reserved">✓ 已預約優先席</span>
              </div>
              <div class="card-shop-name">🛳️ S.S.コロンビア・ダイニングルーム</div>
              <div class="card-chinese-sub">S.S. Columbia Dining Room • 20世紀奢華遠洋巨輪 B-Deck 大餐廳</div>
              <p class="card-description">
                登上停泊在美國海濱的宏偉蒸氣客輪。在水晶吊燈、古典浮雕與純白桌巾的愛德華時代沙龍內，享用烤頂級牛肉與炙煎沙朗牛排套餐，沉浸在優雅的古典樂與紅酒香氣中。
              </p>
              <div class="card-tips-box">
                <strong>🎆 晚餐後接續：</strong>20:30 在地中海港灣欣賞壓軸水上光雕煙火秀《堅信！～夢想之海～（Believe! Sea of Dreams）》。
              </div>
              <div class="card-bottom-bar">
                <span class="card-loc-text">📍 美國海濱 哥倫比亞號 3F 船艙</span>
                <div class="card-links">
                  <a href="https://www.tokyodisneyresort.jp/tc/tds/restaurant/detail/431/" target="_blank" class="btn-card-link" onclick="event.stopPropagation()">🍽️ 餐廳詳情</a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- DAY 4 -->
        <div class="day-card-group" id="group-day-4">
          <div class="day-group-header" onclick="selectDayFilter(4)">
            <div class="day-group-title">
              <span class="day-tag-badge badge-d4">Day 4</span>
              <div class="day-group-text">
                <h3>9月28日 (星期一) • 草津溫泉祕境與櫻井旅館</h3>
                <span>日本第一名湯 ‧ 湯畑浴衣散策 ‧ 會席料理</span>
              </div>
            </div>
            <span>📍 2 個景點 + 乘車</span>
          </div>

          <div class="day-group-content">
            <!-- Exact Transit Schedule Card -->
            <div class="transit-block">
              <div class="transit-block-head">
                <span>🚆 前往草津溫泉乘車時刻表（依路線2）</span>
                <span style="color:#059669;">全程 3h 58m • ¥6,353 (198.8 km)</span>
              </div>

              <div class="transit-step-row">
                <div class="step-time">08:55</div>
                <div class="step-dot start"></div>
                <div class="step-info">
                  <div class="step-stn">百合ヶ丘 (Yurigaoka) [2號月台]</div>
                  <div class="step-meta">
                    <span class="train-badge">小田急小田原線 (新宿行)</span>
                    <span>乘車位置: 8輛車前方</span>
                    <span>¥293</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-row">
                <div class="step-time">09:39<br><small style="color:#94a3b8;">09:51</small></div>
                <div class="step-dot"></div>
                <div class="step-info">
                  <div class="step-stn">新宿 (Shinjuku) [10號到 → 3號發]</div>
                  <div class="step-meta">
                    <span class="train-badge">JR 埼京線 (武藏浦和行・始發)</span>
                    <span>12分鐘換乘</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-row">
                <div class="step-time">10:04<br><small style="color:#94a3b8;">10:10</small></div>
                <div class="step-dot"></div>
                <div class="step-info">
                  <div class="step-stn">赤羽 (Akabane) [8號到 → 4號發]</div>
                  <div class="step-meta">
                    <span class="train-badge">JR 特急草津・四万1號 (長野原草津口行)</span>
                    <strong style="color:#b91c1c;">4號車指定席</strong>
                    <span>運費 ¥3,190 + 特急 ¥2,090</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-row">
                <div class="step-time">12:18<br><small style="color:#94a3b8;">12:31</small></div>
                <div class="step-dot"></div>
                <div class="step-info">
                  <div class="step-stn">長野原草津口 (Naganoharakusatsuguchi)</div>
                  <div class="step-meta">
                    <span>步行3分鐘至巴士站</span>
                    <span class="train-badge">JR巴士關東 (直通 草津溫泉行)</span>
                    <span>¥780</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-row">
                <div class="step-time">12:53</div>
                <div class="step-dot end"></div>
                <div class="step-info">
                  <div class="step-stn">草津温泉バスターミナル (草津溫泉)</div>
                  <div class="step-meta">
                    <strong style="color:#10b981;">抵達日本三大名湯之首！✨</strong>
                  </div>
                </div>
              </div>
            </div>

            <!-- Hotel Sakurai -->
            <div class="schedule-card" onclick="flyToSpot(36.6212, 138.5996, '草津温泉 ホテル櫻井')">
              <div class="card-top">
                <span class="card-time">⏰ 13:30 登記入住</span>
                <span class="status-badge status-reserved">✓ 頂級溫泉旅館</span>
              </div>
              <div class="card-shop-name">♨️ 草津温泉 ホテル櫻井 (Hotel Sakurai)</div>
              <div class="card-chinese-sub">五星級溫泉旅館 ‧ 引流萬代、西之河原等 3 種天然源泉</div>
              <p class="card-description">
                草津規模最大也最負盛名的溫泉旅館。擁有全長約30米的巨大天然溫泉大浴場與巨石露天風呂。入住後先挑選喜歡的花色浴衣，在大浴場好好洗滌疲憊，肌膚瞬間潤滑。
              </p>
              <div class="card-bottom-bar">
                <span class="card-loc-text">📍 群馬縣草津町 465-4 (巴士總站有免費接駁)</span>
                <div class="card-links">
                  <a href="https://www.hotel-sakurai.co.jp/" target="_blank" class="btn-card-link" onclick="event.stopPropagation()">♨️ 旅館官網</a>
                </div>
              </div>
            </div>

            <!-- Yubatake -->
            <div class="schedule-card" onclick="flyToSpot(36.6208, 138.5960, '湯畑 (Yubatake)')">
              <div class="card-top">
                <span class="card-time">⏰ 15:30 – 18:00</span>
                <span class="status-badge status-highlight">浴衣街區漫遊</span>
              </div>
              <div class="card-shop-name">🏮 湯畑 (Yubatake) & 溫泉街</div>
              <div class="card-chinese-sub">草津地標 ‧ 翠綠沸騰泉水 ‧ 免費足湯 ‧ 溫泉饅頭</div>
              <p class="card-description">
                換上日式浴衣與木屐，搭接駁車或散步至湯畑。看著中央木槽奔流而下的翡翠綠溫泉與裊裊白煙，一起在「湯煙亭」泡足湯、品嚐現蒸熱呼呼的溫泉饅頭；黃昏點燈時分更是極致浪漫。
              </p>
              <div class="card-bottom-bar">
                <span class="card-loc-text">📍 草津町中心街區</span>
                <div class="card-links">
                  <a href="https://maps.google.com/?q=Yubatake+Kusatsu" target="_blank" class="btn-card-link" onclick="event.stopPropagation()">🗺️ Google 地圖</a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- DAY 5 -->
        <div class="day-card-group" id="group-day-5">
          <div class="day-group-header" onclick="selectDayFilter(5)">
            <div class="day-group-title">
              <span class="day-tag-badge badge-d5">Day 5</span>
              <div class="day-group-text">
                <h3>9月29日 (星期二) • 新幹線、頂級牛排與爵士之夜</h3>
                <span>青山沃夫岡 ‧ 澀谷潮流 ‧ 柏悅高空酒吧</span>
              </div>
            </div>
            <span>📍 3 個景點 + 返程</span>
          </div>

          <div class="day-group-content">
            <!-- Exact Return Transit Schedule Card -->
            <div class="transit-block">
              <div class="transit-block-head">
                <span>🚅 回程交通：草津溫泉 → 外苑前 (青山)</span>
                <span style="color:#059669;">13:35 抵達 • 完美接駁 14:30 牛排！</span>
              </div>

              <div class="transit-step-row">
                <div class="step-time">09:20</div>
                <div class="step-dot start"></div>
                <div class="step-info">
                  <div class="step-stn">草津温泉 (Kusatsu Onsen 巴士站)</div>
                  <div class="step-meta">
                    <span class="train-badge">JR巴士關東 (長野原草津口行)</span>
                    <span>¥780</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-row">
                <div class="step-time">09:48<br><small style="color:#94a3b8;">10:08</small></div>
                <div class="step-dot"></div>
                <div class="step-info">
                  <div class="step-stn">長野原草津口 (Naganoharakusatsuguchi)</div>
                  <div class="step-meta">
                    <span class="train-badge">JR 吾妻線 (高崎行・始發)</span>
                    <span>直達高崎 7號月台</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-row">
                <div class="step-time">11:35<br><small style="color:#94a3b8;">12:04</small></div>
                <div class="step-dot"></div>
                <div class="step-info">
                  <div class="step-stn">高崎 (Takasaki) [13號月台]</div>
                  <div class="step-meta">
                    <span class="train-badge">JR 新幹線たにがわ410號 (東京行)</span>
                    <strong style="color:#2563eb;">新幹線極速直達東京</strong>
                    <span>運費 ¥3,190 + 自由席 ¥2,510</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-row">
                <div class="step-time">13:00<br><small style="color:#94a3b8;">13:13</small></div>
                <div class="step-dot"></div>
                <div class="step-info">
                  <div class="step-stn">東京 (Tokyo Station) [21號到 → 5號發]</div>
                  <div class="step-meta">
                    <span class="train-badge">JR 山手線外環 (品川・澀谷方向)</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-row">
                <div class="step-time">13:17<br><small style="color:#94a3b8;">13:26</small></div>
                <div class="step-dot"></div>
                <div class="step-info">
                  <div class="step-stn">新橋 (Shimbashi) [4號到 → 1號發]</div>
                  <div class="step-meta">
                    <span class="train-badge">東京Metro 銀座線 (澀谷行)</span>
                    <span>¥178</span>
                  </div>
                </div>
              </div>

              <div class="transit-step-row">
                <div class="step-time">13:35</div>
                <div class="step-dot end"></div>
                <div class="step-info">
                  <div class="step-stn">外苑前 (Gaienmae) [4a 出口]</div>
                  <div class="step-meta">
                    <strong style="color:#10b981;">直通 THE ARGYLE AOYAMA 大樓！🥩</strong>
                  </div>
                </div>
              </div>
            </div>

            <!-- Wolfgang's -->
            <div class="schedule-card" onclick="flyToSpot(35.6698, 139.7180, 'ウルフギャング・ステーキハウス シグニチャー 青山店')">
              <div class="card-top">
                <span class="card-time">⏰ 14:30 準時抵達</span>
                <span class="status-badge status-reserved">✓ 預約 14:30 午餐</span>
              </div>
              <div class="card-shop-name">🥩 ウルフギャング・ステーキハウス シグニチャー 青山店</div>
              <div class="card-chinese-sub">Wolfgang's Steakhouse Signature Aoyama • 頂級乾式熟成黑安格斯丁骨牛排</div>
              <p class="card-description">
                美國頂級 USDA Prime 安格斯牛肉經 28 天乾式熟成，以 900 度高溫極速炙烤，上桌時瓷盤內濃香奶油滋滋作響！肉質外酥內嫩，奢華感十足。
              </p>
              <div class="card-tips-box">
                <strong>💡 推薦必點：</strong>招牌雙人丁骨大牛排（Steak for Two）、大西洋蟹肉餅（Jumbo Lump Crab Cake）、奶油菠菜、德式煎馬鈴薯、甜點蘋果派配鮮奶油。
              </div>
              <div class="card-bottom-bar">
                <span class="card-loc-text">📍 外苑前站 4a 出口直達 THE ARGYLE AOYAMA 1F/2F</span>
                <div class="card-links">
                  <a href="https://wolfgangssteakhouse.jp/" target="_blank" class="btn-card-link" onclick="event.stopPropagation()">🥩 官方網站</a>
                  <a href="https://maps.google.com/?q=Wolfgang's+Steakhouse+Signature+Aoyama" target="_blank" class="btn-card-link" onclick="event.stopPropagation()">🗺️ Google 地圖</a>
                </div>
              </div>
            </div>

            <!-- Shibuya -->
            <div class="schedule-card" onclick="flyToSpot(35.6595, 139.7005, '渋谷スクランブル交差点 & MIYASHITA PARK')">
              <div class="card-top">
                <span class="card-time">⏰ 19:30 (晚上 7:30)</span>
                <span class="status-badge status-highlight">澀谷霓虹熱潮</span>
              </div>
              <div class="card-shop-name">🌆 渋谷スクランブル交差点 & MIYASHITA PARK</div>
              <div class="card-chinese-sub">Shibuya • 宮下公園屋頂草坪 ‧ 潮流購物 ‧ SHIBUYA SKY 夜景</div>
              <p class="card-description">
                走進世界最著名的澀谷十字路口感受東京脈搏；逛逛極具設計感的 MIYASHITA PARK（宮下公園），在空中綠地坐看山手線穿梭；亦可預訂 SHIBUYA SKY 俯瞰無死角璀璨夜景。
              </p>
              <div class="card-bottom-bar">
                <span class="card-loc-text">📍 澀谷車站周邊</span>
                <div class="card-links">
                  <a href="https://maps.google.com/?q=Shibuya+Crossing" target="_blank" class="btn-card-link" onclick="event.stopPropagation()">🗺️ Google 地圖</a>
                </div>
              </div>
            </div>

            <!-- New York Bar -->
            <div class="schedule-card" onclick="flyToSpot(35.6856, 139.6910, 'ニューヨーク バー (パーク ハイアット 東京 52F)')">
              <div class="card-top">
                <span class="card-time">⏰ 21:30 – 深夜</span>
                <span class="status-badge status-reserved">壓軸浪漫收尾</span>
              </div>
              <div class="card-shop-name">🎷 ニューヨーク バー / New York Bar (パーク ハイアット 東京 52F)</div>
              <div class="card-chinese-sub">Park Hyatt Tokyo 52F • 《愛情，不用翻譯》傳奇爵士高空酒吧</div>
              <p class="card-description">
                歷經全面重金改裝，於2025年底奢華重開！坐落於西新宿柏悅酒店頂層 52 樓，四面頂級落地窗倒映著無限延伸的東京璀璨燈海。現場國際爵士樂隊演奏，舉起馬丁尼對飲，為這趟旅程畫下最完美的句點。
              </p>
              <div class="card-tips-box">
                <strong>👔 服裝提醒：</strong>請著 Smart Casual（男士請勿穿著拖鞋或無領背心）。
              </div>
              <div class="card-bottom-bar">
                <span class="card-loc-text">📍 新宿區西新宿 3-7-1-2 新宿公園塔 52 樓</span>
                <div class="card-links">
                  <a href="https://maps.google.com/?q=Park+Hyatt+Tokyo+New+York+Bar" target="_blank" class="btn-card-link" onclick="event.stopPropagation()">🗺️ Google 地圖</a>
                </div>
              </div>
            </div>
          </div>
        </div>

      </div>
    </aside>
  </div>

  <div class="toast-box" id="toast-notify">
    <span>✓</span> <span id="toast-text">已複製分享連結！</span>
  </div>

  <!-- Leaflet JS -->
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
  
  <script>
    // Spots Dataset
    const tripSpots = [
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

    // Initialize Map
    let map = L.map('trip-map', {
      center: [35.68, 139.75],
      zoom: 11,
      zoomControl: true
    });

    // Carto Voyager Light Tiles
    L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://carto.com/">CARTO</a> & OSM',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(map);

    let mapMarkers = [];

    // Custom Map Marker Pin Builder
    function createPinElement(color, dayNum) {
      return L.divIcon({
        className: 'custom-pin-icon-wrap',
        html: `<div class="custom-map-pin" style="background-color: ${color};">
          <span>D${dayNum}</span>
        </div>`,
        iconSize: [34, 34],
        iconAnchor: [17, 34],
        popupAnchor: [0, -34]
      });
    }

    // Populate Markers
    tripSpots.forEach(spot => {
      const pinIcon = createPinElement(spot.color, spot.day);
      const marker = L.marker([spot.lat, spot.lng], { icon: pinIcon }).addTo(map);

      const popupContent = `
        <div class="map-balloon">
          <span class="balloon-time">Day ${spot.day} • ${spot.time}</span>
          <div class="balloon-title">${spot.title}</div>
          <div class="balloon-subtitle">${spot.sub}</div>
          <p class="balloon-desc">${spot.desc}</p>
          <div class="balloon-actions">
            <a href="${spot.link}" target="_blank" class="balloon-btn btn-focus">開啟詳情</a>
            <a href="https://maps.google.com/?q=${encodeURIComponent(spot.title)}" target="_blank" class="balloon-btn btn-maps">Google 地圖</a>
          </div>
        </div>
      `;
      marker.bindPopup(popupContent);
      marker.spotData = spot;
      mapMarkers.push(marker);
    });

    // Connecting Route Polyline between stops
    const mainPolyline = L.polyline([
      [35.6033, 139.5080], // 新百合
      [35.6587, 139.7291], // 六本木次郎
      [35.6586, 139.7454], // 東京鐵塔
      [35.6872, 139.7645], // 大手町VIRTU
      [35.6267, 139.8851], // 迪士尼海洋
      [36.3220, 139.0130], // 高崎
      [36.5600, 138.6500], // 長野原草津口
      [36.6212, 138.5996], // 草津溫泉櫻井
      [35.6698, 139.7180], // 青山沃夫岡
      [35.6595, 139.7005], // 澀谷
      [35.6856, 139.6910]  // 新宿紐約酒吧
    ], {
      color: '#a12b48',
      weight: 3.5,
      opacity: 0.6,
      dashArray: '6, 8'
    }).addTo(map);

    // Fly to Spot
    function flyToSpot(lat, lng, name) {
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

    // Filter Map by Day
    function selectDayFilter(day, pillEl) {
      document.querySelectorAll('.day-pill-btn').forEach(b => b.classList.remove('active'));
      if (pillEl) pillEl.classList.add('active');

      const targetMarkers = [];
      mapMarkers.forEach(m => {
        if (day === 'all' || m.spotData.day === parseInt(day)) {
          m.addTo(map);
          targetMarkers.push(m);
        } else {
          map.removeLayer(m);
        }
      });

      if (targetMarkers.length > 0) {
        const group = new L.featureGroup(targetMarkers);
        map.fitBounds(group.getBounds().pad(0.18));
      }

      // Highlight in Drawer
      document.querySelectorAll('.day-card-group').forEach(grp => grp.classList.remove('active-day-group'));
      if (day !== 'all') {
        const targetGroup = document.getElementById('group-day-' + day);
        if (targetGroup) {
          targetGroup.classList.add('active-day-group');
          targetGroup.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }
    }

    // Fit Full Route
    function fitFullRoute() {
      selectDayFilter('all', document.querySelector('.day-pill-btn:first-child'));
      const group = new L.featureGroup(mapMarkers);
      map.fitBounds(group.getBounds().pad(0.12));
    }

    // Toggle Drawer Width for wider map
    let isDrawerNarrow = false;
    function toggleDrawerWidth() {
      const drawer = document.getElementById('itinerary-drawer');
      if (window.innerWidth > 960) {
        if (!isDrawerNarrow) {
          drawer.style.width = '380px';
          isDrawerNarrow = true;
        } else {
          drawer.style.width = '520px';
          isDrawerNarrow = false;
        }
        setTimeout(() => { map.invalidateSize(); }, 300);
      }
    }

    // Copy Share Link
    function copyShareURL() {
      navigator.clipboard.writeText(window.location.href);
      showToast('✓ 已複製分享連結！快傳給她看吧 ❤️');
    }

    function showToast(text) {
      const t = document.getElementById('toast-notify');
      document.getElementById('toast-text').textContent = text;
      t.style.display = 'flex';
      setTimeout(() => { t.style.display = 'none'; }, 2800);
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

    // Auto fit full view on load
    setTimeout(() => { fitFullRoute(); }, 400);

  </script>
</body>
</html>
'''

with open('/Users/rondey/japan-trip-itinerary/index.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

with open('/Users/rondey/tokyo-kusatsu-itinerary.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("Map-Main Traditional Chinese HTML generated successfully!")
