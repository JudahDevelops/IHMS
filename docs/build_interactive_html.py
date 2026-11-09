#!/usr/bin/env python3
import os

with open('docs/assets/ihms_erd.svg', 'r') as f:
    erd_svg = f.read()

with open('docs/assets/ihms_engine_workflow.svg', 'r') as f:
    workflow_svg = f.read()

def clean_svg(s, svg_id):
    start = s.find('<svg')
    s = s[start:]
    end_tag = s.find('>')
    svg_tag = s[:end_tag+1]
    clean_tag = svg_tag.replace('<svg', f'<svg id="{svg_id}" class="diagram-svg"')
    return clean_tag + s[end_tag+1:]

erd_clean = clean_svg(erd_svg, 'svg-erd')
workflow_clean = clean_svg(workflow_svg, 'svg-workflow')

template = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>IHMS Database Relational Architecture & ERD Viewer</title>
  <style>
    :root {
      --bg: #090d16;
      --panel-bg: #111827;
      --card-bg: #1f2937;
      --card-border: #374151;
      --text: #f9fafb;
      --text-muted: #9ca3af;
      --primary: #38bdf8;
      --primary-dark: #0284c7;
      --accent: #2563eb;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      display: flex;
      height: 100vh;
      overflow: hidden;
    }

    /* Sidebar */
    #sidebar {
      width: 320px;
      min-width: 320px;
      background: var(--panel-bg);
      border-right: 1px solid var(--card-border);
      display: flex;
      flex-direction: column;
      z-index: 10;
      box-shadow: 4px 0 20px rgba(0,0,0,0.4);
    }
    .header-box {
      padding: 18px;
      border-bottom: 1px solid var(--card-border);
    }
    .badge-sub {
      display: inline-block;
      font-size: 10px;
      font-weight: 700;
      color: var(--primary);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      margin-bottom: 4px;
    }
    h1 {
      font-size: 16px;
      font-weight: 700;
      color: #fff;
      line-height: 1.3;
    }
    .subtitle {
      font-size: 12px;
      color: var(--text-muted);
      margin-top: 4px;
    }

    .search-box {
      padding: 12px 18px;
      border-bottom: 1px solid var(--card-border);
    }
    .search-box input {
      width: 100%;
      padding: 9px 12px;
      border-radius: 6px;
      border: 1px solid var(--card-border);
      background: #090d16;
      color: #fff;
      font-size: 13px;
      outline: none;
      transition: border-color 0.2s;
    }
    .search-box input:focus {
      border-color: var(--primary);
    }

    .table-list {
      flex: 1;
      overflow-y: auto;
      padding: 10px 14px;
    }
    .table-item {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 9px 12px;
      border-radius: 6px;
      cursor: pointer;
      margin-bottom: 4px;
      transition: all 0.15s;
      font-size: 13px;
      border: 1px solid transparent;
    }
    .table-item:hover {
      background: rgba(56, 189, 248, 0.1);
      border-color: rgba(56, 189, 248, 0.2);
      color: var(--primary);
    }
    .table-item.active {
      background: rgba(56, 189, 248, 0.2);
      border-color: var(--primary);
      color: #fff;
      font-weight: 600;
    }
    .col-count {
      font-size: 11px;
      color: var(--text-muted);
      background: rgba(255,255,255,0.06);
      padding: 2px 7px;
      border-radius: 10px;
    }

    .sidebar-footer {
      padding: 14px 18px;
      border-top: 1px solid var(--card-border);
      font-size: 11px;
      color: var(--text-muted);
      line-height: 1.5;
    }

    /* Main Viewport */
    #viewport {
      flex: 1;
      position: relative;
      overflow: hidden;
      background: #0a0e17;
      background-image: 
        radial-gradient(#1f2937 1px, transparent 1px),
        radial-gradient(#1f2937 1px, #0a0e17 1px);
      background-size: 32px 32px;
      background-position: 0 0, 16px 16px;
      cursor: grab;
      user-select: none;
    }
    #viewport:active {
      cursor: grabbing;
    }

    /* Floating Toolbar */
    .toolbar {
      position: absolute;
      top: 16px;
      right: 16px;
      background: rgba(17, 24, 39, 0.95);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      display: flex;
      padding: 5px;
      gap: 6px;
      z-index: 20;
      box-shadow: 0 8px 24px rgba(0,0,0,0.5);
      backdrop-filter: blur(8px);
    }
    .tool-btn {
      background: rgba(255,255,255,0.05);
      border: 1px solid rgba(255,255,255,0.1);
      color: #fff;
      padding: 7px 12px;
      font-size: 12px;
      font-weight: 600;
      border-radius: 6px;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      text-decoration: none;
      transition: all 0.15s;
    }
    .tool-btn:hover {
      background: rgba(255,255,255,0.15);
      border-color: rgba(255,255,255,0.25);
    }
    .tool-btn.primary {
      background: var(--primary-dark);
      border-color: var(--primary);
    }
    .tool-btn.primary:hover {
      background: var(--primary);
      color: #000;
    }

    /* Canvas Stage */
    #canvas-stage {
      position: absolute;
      top: 0;
      left: 0;
      transform-origin: 0 0;
      will-change: transform;
      padding: 30px;
    }

    .svg-wrapper {
      background: #ffffff;
      border-radius: 12px;
      padding: 20px;
      box-shadow: 0 20px 50px rgba(0,0,0,0.8);
      border: 1px solid #cbd5e1;
      display: inline-block;
    }

    .diagram-svg {
      display: block;
      max-width: none;
      height: auto;
    }

    /* Highlighted table in SVG */
    .highlight-table path {
      stroke: #0284c7 !important;
      stroke-width: 3px !important;
      filter: drop-shadow(0 0 10px rgba(2, 132, 199, 0.9));
    }

    /* Legend Overlay */
    .legend {
      position: absolute;
      bottom: 16px;
      left: 16px;
      background: rgba(17, 24, 39, 0.95);
      border: 1px solid var(--card-border);
      border-radius: 8px;
      padding: 10px 16px;
      display: flex;
      gap: 16px;
      font-size: 12px;
      backdrop-filter: blur(8px);
      z-index: 10;
      box-shadow: 0 4px 16px rgba(0,0,0,0.4);
    }
    .legend-item {
      display: flex;
      align-items: center;
      gap: 6px;
    }
    .dot {
      width: 10px;
      height: 10px;
      border-radius: 50%;
    }
  </style>
</head>
<body>

  <!-- Sidebar Directory -->
  <aside id="sidebar">
    <div class="header-box">
      <span class="badge-sub">Nile University • Group 39</span>
      <h1>IHMS Schema Inspector</h1>
      <p class="subtitle">Normalized Relational Architecture (16 Tables)</p>
    </div>

    <div class="search-box">
      <input type="text" id="searchInput" placeholder="Search tables...">
    </div>

    <div class="table-list" id="tableList"></div>

    <div class="sidebar-footer">
      <strong>Lecturer Presentation Tip:</strong><br>
      • Click any table to focus and highlight.<br>
      • Drag to Pan • Mouse wheel to Zoom.<br>
      • Use 'Switch: Workflow Engine' to show Escalation.<br>
      • Works in any browser offline.
    </div>
  </aside>

  <!-- Viewport -->
  <main id="viewport">
    <div class="toolbar">
      <button class="tool-btn" id="btnZoomIn">➕ Zoom In</button>
      <button class="tool-btn" id="btnZoomOut">➖ Zoom Out</button>
      <button class="tool-btn" id="btnReset">🔄 Reset</button>
      <button class="tool-btn primary" id="btnToggleView">👁️ Switch: Workflow Engine</button>
      <a class="tool-btn" href="assets/ihms_erd.png" target="_blank" download="ihms_erd.png">📥 PNG</a>
    </div>

    <div id="canvas-stage">
      <div class="svg-wrapper" id="erdWrapper">
        __ERD_SVG__
      </div>
      <div class="svg-wrapper" id="workflowWrapper" style="display: none;">
        __WORKFLOW_SVG__
      </div>
    </div>

    <div class="legend" id="erdLegend">
      <div class="legend-item"><span class="dot" style="background: #1E3A8A;"></span> Users & Profiles</div>
      <div class="legend-item"><span class="dot" style="background: #047857;"></span> Hostels & Beds</div>
      <div class="legend-item"><span class="dot" style="background: #7C3AED;"></span> Allocations</div>
      <div class="legend-item"><span class="dot" style="background: #B91C1C;"></span> Complaints & Triage</div>
      <div class="legend-item"><span class="dot" style="background: #0F766E;"></span> Maintenance Units</div>
      <div class="legend-item"><span class="dot" style="background: #475569;"></span> Audit & SMTP Logs</div>
    </div>
  </main>

  <script>
    const tables = [
      { name: "users", cols: 10 },
      { name: "roles", cols: 4 },
      { name: "user_role", cols: 3 },
      { name: "student_profiles", cols: 13 },
      { name: "staff_profiles", cols: 9 },
      { name: "maintenance_units", cols: 7 },
      { name: "hostels", cols: 9 },
      { name: "rooms", cols: 8 },
      { name: "bed_spaces", cols: 6 },
      { name: "academic_sessions", cols: 7 },
      { name: "allocations", cols: 13 },
      { name: "complaints", cols: 22 },
      { name: "complaint_history", cols: 10 },
      { name: "notification_logs", cols: 11 },
      { name: "triage_keywords", cols: 7 },
      { name: "audit_logs", cols: 9 }
    ];

    const tableListEl = document.getElementById("tableList");
    const searchInput = document.getElementById("searchInput");

    function renderList(filter = "") {
      tableListEl.innerHTML = "";
      tables.filter(t => t.name.toLowerCase().includes(filter.toLowerCase())).forEach(t => {
        const item = document.createElement("div");
        item.className = "table-item";
        item.dataset.table = t.name;
        item.innerHTML = `
          <span>${t.name}</span>
          <span class="col-count">${t.cols} cols</span>
        `;
        item.onclick = () => focusTable(t.name);
        tableListEl.appendChild(item);
      });
    }
    renderList();

    searchInput.addEventListener("input", (e) => renderList(e.target.value));

    // Pan & Zoom Logic
    const stage = document.getElementById("canvas-stage");
    const viewport = document.getElementById("viewport");
    let scale = 0.55;
    let posX = 40;
    let posY = 20;
    let isDragging = false;
    let startX, startY;

    function applyTransform() {
      stage.style.transform = `translate(${posX}px, ${posY}px) scale(${scale})`;
    }
    applyTransform();

    viewport.addEventListener("mousedown", (e) => {
      if (e.target.closest(".toolbar") || e.target.closest(".legend")) return;
      isDragging = true;
      startX = e.clientX - posX;
      startY = e.clientY - posY;
    });

    window.addEventListener("mousemove", (e) => {
      if (!isDragging) return;
      posX = e.clientX - startX;
      posY = e.clientY - startY;
      applyTransform();
    });

    window.addEventListener("mouseup", () => { isDragging = false; });

    viewport.addEventListener("wheel", (e) => {
      e.preventDefault();
      const zoomFactor = e.deltaY < 0 ? 1.15 : 0.85;
      const newScale = Math.min(Math.max(0.15, scale * zoomFactor), 3.0);
      
      const rect = viewport.getBoundingClientRect();
      const mouseX = e.clientX - rect.left;
      const mouseY = e.clientY - rect.top;

      posX = mouseX - (mouseX - posX) * (newScale / scale);
      posY = mouseY - (mouseY - posY) * (newScale / scale);
      scale = newScale;
      applyTransform();
    });

    document.getElementById("btnZoomIn").onclick = () => {
      scale = Math.min(3.0, scale * 1.25);
      applyTransform();
    };
    document.getElementById("btnZoomOut").onclick = () => {
      scale = Math.max(0.15, scale * 0.8);
      applyTransform();
    };
    document.getElementById("btnReset").onclick = () => {
      scale = 0.55;
      posX = 40;
      posY = 20;
      applyTransform();
      clearHighlight();
    };

    // Switch between ERD and Workflow
    let activeView = "erd";
    const erdWrapper = document.getElementById("erdWrapper");
    const workflowWrapper = document.getElementById("workflowWrapper");
    const toggleBtn = document.getElementById("btnToggleView");
    const legendEl = document.getElementById("erdLegend");

    toggleBtn.onclick = () => {
      if (activeView === "erd") {
        erdWrapper.style.display = "none";
        workflowWrapper.style.display = "inline-block";
        activeView = "workflow";
        toggleBtn.innerHTML = "👁️ Switch: Relational ERD";
        legendEl.style.display = "none";
        scale = 0.85;
        posX = 80;
        posY = 40;
      }} else {
        erdWrapper.style.display = "inline-block";
        workflowWrapper.style.display = "none";
        activeView = "erd";
        toggleBtn.innerHTML = "👁️ Switch: Workflow Engine";
        legendEl.style.display = "flex";
        scale = 0.55;
        posX = 40;
        posY = 20;
      }
      applyTransform();
    };

    // Focus and highlight table node
    function clearHighlight() {
      document.querySelectorAll(".highlight-table").forEach(el => el.classList.remove("highlight-table"));
      document.querySelectorAll(".table-item").forEach(el => el.classList.remove("active"));
    }

    function focusTable(tableName) {
      clearHighlight();
      
      const itemEl = document.querySelector(`.table-item[data-table="${tableName}"]`);
      if (itemEl) itemEl.classList.add("active");

      if (activeView !== "erd") {
        toggleBtn.click();
      }

      // Find SVG node by title text
      const titles = document.querySelectorAll("#svg-erd g.node title");
      for (const t of titles) {
        if (t.textContent.trim() === tableName) {
          const nodeG = t.parentElement;
          nodeG.classList.add("highlight-table");
          
          // Center on node
          const bbox = nodeG.getBBox();
          const vpRect = viewport.getBoundingClientRect();
          scale = 1.0;
          posX = (vpRect.width / 2) - (bbox.x + bbox.width / 2) - 40;
          posY = (vpRect.height / 2) - (bbox.y + bbox.height / 2) - 40;
          applyTransform();
          break;
        }
      }
    }
  </script>
</body>
</html>
"""

final_html = template.replace('__ERD_SVG__', erd_clean).replace('__WORKFLOW_SVG__', workflow_clean)

with open('docs/erd_interactive.html', 'w') as f:
    f.write(final_html)

print("✅ docs/erd_interactive.html generated cleanly with inlined vector graphics!")
