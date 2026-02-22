#!/usr/bin/env python3
"""Patch interactive_profile.html: sidebar table + visible repo nodes + bidirectional linking."""
import sys

with open('templates/interactive_profile.html', 'r', encoding='utf-8') as f:
    content = f.read()

def replace_exact(old, new, label):
    """Try exact match first, then try with normalized trailing whitespace."""
    global content
    if old in content:
        content = content.replace(old, new, 1)
        print(f"  {label} OK (exact)")
        return True
    # Try normalizing: strip trailing spaces on each line
    import re
    old_norm = re.sub(r' +\n', '\n', old)
    content_norm = re.sub(r' +\n', '\n', content)
    if old_norm in content_norm:
        # Find position in normalized, then replace in original via line matching
        # Simpler: just normalize the content and replace
        content = content_norm.replace(old_norm, new, 1)
        print(f"  {label} OK (normalized)")
        return True
    print(f"  {label} FAILED")
    return False


changes = 0

# ═══════════════════════════════════════════════════════════
#  1. CSS: Replace .node-item styles with .node-table styles
# ═══════════════════════════════════════════════════════════
print("[1] CSS: node-table styles...")

old_css = """  /* Node list */
  .node-list {
    flex: 1;
    overflow-y: auto;
    padding: 8px 0;
  }

  .node-list::-webkit-scrollbar { width: 4px; }
  .node-list::-webkit-scrollbar-track { background: transparent; }
  .node-list::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 2px; }

  .node-item {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 8px 16px;
    cursor: pointer;
    transition: all 0.15s;
    border-left: 2px solid transparent;
  }

  .node-item:hover {
    background: rgba(255,255,255,0.03);
  }

  .node-item.selected {
    background: rgba(139,105,20,0.1);
    border-left-color: var(--gold);
  }

  .node-item.hidden { display: none; }

  .node-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }

  .node-item .node-id {
    font-size: 9px;
    opacity: 0.35;
    width: 28px;
    flex-shrink: 0;
  }

  .node-item .node-label {
    font-size: 10px;
    opacity: 0.7;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    flex: 1;
  }

  .node-item .node-conf {
    font-size: 8px;
    opacity: 0.3;
    flex-shrink: 0;
  }

  /* Level headers in list */
  .level-header {
    padding: 10px 16px 4px;
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    opacity: 0.25;
  }"""

new_css = """  /* Node list */
  .node-list {
    flex: 1;
    overflow-y: auto;
    padding: 0;
  }

  .node-list::-webkit-scrollbar { width: 4px; }
  .node-list::-webkit-scrollbar-track { background: transparent; }
  .node-list::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 2px; }

  /* Interactive Table */
  .node-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 10px;
  }

  .node-table thead {
    position: sticky;
    top: 0;
    background: var(--bg2);
    z-index: 2;
  }

  .node-table th {
    padding: 6px 8px;
    text-align: left;
    font-size: 8px;
    letter-spacing: 2px;
    text-transform: uppercase;
    opacity: 0.3;
    font-weight: 400;
    border-bottom: 1px solid rgba(255,255,255,0.06);
  }

  .node-table .level-row td {
    padding: 12px 8px 4px;
    font-size: 9px;
    letter-spacing: 2px;
    text-transform: uppercase;
    opacity: 0.25;
    border: none;
  }

  .node-table .node-row {
    cursor: pointer;
    transition: all 0.15s;
    border-left: 2px solid transparent;
  }

  .node-table .node-row:hover {
    background: rgba(255,255,255,0.04);
  }

  .node-table .node-row.selected {
    background: rgba(139,105,20,0.12);
    border-left-color: var(--gold);
  }

  .node-table .node-row.highlight {
    background: rgba(139,105,20,0.08);
    border-left-color: var(--gold-light);
  }

  .node-table .node-row.hidden { display: none; }

  .node-table td {
    padding: 6px 8px;
    vertical-align: middle;
    border-bottom: 1px solid rgba(255,255,255,0.02);
  }

  .node-table .col-dot { width: 16px; }
  .node-table .col-id { width: 32px; opacity: 0.35; font-size: 9px; }
  .node-table .col-label {
    opacity: 0.7;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    max-width: 140px;
  }
  .node-table .col-conf {
    width: 40px;
    text-align: right;
    opacity: 0.3;
    font-size: 8px;
  }
  .node-table .col-status {
    width: 24px;
    text-align: center;
    font-size: 10px;
  }

  .node-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }"""

if replace_exact(old_css, new_css, "node-table CSS"):
    changes += 1
else:
    sys.exit(1)

# ═══════════════════════════════════════════════════════════
#  2. CSS: Add highlight/pulse + connector styles after .node-ring
# ═══════════════════════════════════════════════════════════
print("[2] CSS: highlight/pulse + connector...")

old_ring = """  .node-ring {
    opacity: 0;
    transition: all 0.25s ease;
  }"""

new_ring = """  .node-ring {
    opacity: 0;
    transition: all 0.25s ease;
  }

  @keyframes nodePulse {
    0%, 100% { opacity: 0.5; }
    50% { opacity: 1; }
  }
  .tree-svg .node-g.highlight .node-ring {
    opacity: 1;
    stroke-width: 3;
    animation: nodePulse 0.8s ease-in-out infinite;
  }
  .tree-svg .node-g.highlight .node-bg { filter: url(#glow); }

  .connector-svg {
    position: absolute;
    top: 0; left: 0;
    width: 100%; height: 100%;
    pointer-events: none;
    z-index: 5;
  }
  .connector-line {
    stroke: var(--gold);
    stroke-width: 1;
    stroke-dasharray: 4,4;
    opacity: 0;
    transition: opacity 0.3s ease;
  }
  .connector-line.active { opacity: 0.4; }"""

if replace_exact(old_ring, new_ring, "highlight/connector CSS"):
    changes += 1
else:
    sys.exit(1)

# ═══════════════════════════════════════════════════════════
#  3. HTML: Add connector SVG
# ═══════════════════════════════════════════════════════════
print("[3] HTML: connector SVG...")

old_canvas = '  <!-- MAIN CANVAS -->\n  <div class="canvas" id="canvas">'
new_canvas = '  <!-- Connector overlay -->\n  <svg class="connector-svg" id="connectorSvg" xmlns="http://www.w3.org/2000/svg"></svg>\n\n  <!-- MAIN CANVAS -->\n  <div class="canvas" id="canvas">'

if replace_exact(old_canvas, new_canvas, "connector SVG"):
    changes += 1
else:
    sys.exit(1)

# ═══════════════════════════════════════════════════════════
#  4. JS: Replace buildNodeList() — use marker-based approach
# ═══════════════════════════════════════════════════════════
print("[4] JS: buildNodeList → table...")

# Find the function boundaries
start = content.find('function buildNodeList(nodes) {')
end = content.find('\nfunction filterNodes()')
if start == -1 or end == -1:
    print("  FAILED: buildNodeList boundaries not found")
    sys.exit(1)

new_buildNodeList = """function buildNodeList(nodes) {
  const list = document.getElementById("nodeList");
  const grouped = {};

  nodes.forEach(n => {
    const key = nodeLevelKey(n);
    if (!grouped[key]) grouped[key] = [];
    grouped[key].push(n);
  });

  let html = `<table class="node-table">
    <thead><tr>
      <th></th><th>ID</th><th>Label</th><th>Conf</th><th>St</th>
    </tr></thead><tbody>`;

  const levelOrder = ["C", "F", "b", "B", "T", "R-1", "R-2", "R-3", "R-4", "R-5"];

  for (const lk of levelOrder) {
    const lev = LEVELS[lk];
    const group = grouped[lk];
    if (!group || !lev) continue;

    html += `<tr class="level-row"><td colspan="5">${lev.label}</td></tr>`;
    for (const n of group) {
      html += `
      <tr class="node-row" data-id="${n.id}" data-status="${n.status}" data-level="${lk}">
        <td class="col-dot"><div class="node-dot" style="background:${statusColor(n.status)}"></div></td>
        <td class="col-id">${n.id}</td>
        <td class="col-label" title="${n.label}">${n.label}</td>
        <td class="col-conf">${n.confidence || 0}%</td>
        <td class="col-status">${statusIcon(n.status)}</td>
      </tr>`;
    }
  }
  html += `</tbody></table>`;
  list.innerHTML = html;

  list.querySelectorAll(".node-row").forEach(row => {
    row.addEventListener("click", () => selectNode(row.dataset.id));
    row.addEventListener("mouseenter", () => highlightTreeNode(row.dataset.id, true));
    row.addEventListener("mouseleave", () => highlightTreeNode(row.dataset.id, false));
  });
}

"""

content = content[:start] + new_buildNodeList + content[end+1:]
changes += 1
print("  buildNodeList → table OK")

# ═══════════════════════════════════════════════════════════
#  5. JS: Replace filterNodes() — .node-item → .node-row
# ═══════════════════════════════════════════════════════════
print("[5] JS: filterNodes...")

old_filter = '.querySelectorAll(".node-item").forEach(item =>'
new_filter = '.querySelectorAll(".node-row").forEach(row =>'

# Replace first occurrence (in filterNodes)
if old_filter in content:
    # Replace all .node-item refs in filterNodes block
    content = content.replace(
        'document.querySelectorAll(".node-item").forEach(item => {\n    if (statusFilter === "all" || item.dataset.status === statusFilter) {\n      item.classList.remove("hidden");\n    } else {\n      item.classList.add("hidden");\n    }\n  });',
        'document.querySelectorAll(".node-row").forEach(row => {\n    if (statusFilter === "all" || row.dataset.status === statusFilter) {\n      row.classList.remove("hidden");\n    } else {\n      row.classList.add("hidden");\n    }\n  });',
        1
    )
    changes += 1
    print("  filterNodes OK")
else:
    print("  WARN: .node-item in filterNodes not found")

# ═══════════════════════════════════════════════════════════
#  6. JS: Replace repo node rendering
# ═══════════════════════════════════════════════════════════
print("[6] JS: visible repo nodes...")

# Find by marker
marker_start = '  // ────── REPO NODES'
marker_end_str = '    </g>`;\n  });\n'
idx_start = content.find(marker_start)
if idx_start == -1:
    print("  FAILED: REPO NODES marker not found")
    sys.exit(1)

# Find the end of the nodes.forEach block
idx_end = content.find(marker_end_str, idx_start)
if idx_end == -1:
    # Try alternative ending
    marker_end_str = '    </g>`;\n  });'
    idx_end = content.find(marker_end_str, idx_start)
    if idx_end == -1:
        print("  FAILED: end of repo nodes not found")
        sys.exit(1)
idx_end += len(marker_end_str)

new_repo = """  // ────── REPO NODES (visibles, mappes sur squelette) ──────
  const idealByLevel = {};
  idealTree.forEach(n => {
    if (!idealByLevel[n.lk]) idealByLevel[n.lk] = [];
    idealByLevel[n.lk].push(n);
  });

  const posMap = {};
  for (const [lk, lev] of Object.entries(LEVELS)) {
    const repoGroup = grouped[lk] || [];
    const idealGroup = idealByLevel[lk] || [];
    repoGroup.forEach((n, i) => {
      if (i < idealGroup.length) {
        const ideal = idealGroup[i];
        posMap[n.id] = { x: ideal.x, y: ideal.y };
      } else {
        const side = i % 2 === 0 ? 1 : -1;
        const bounds = lev.zone === "aerial" ? canopyWidthAt(lev.y) : rootWidthAt(lev.y);
        const half = side > 0 ? Math.max(bounds.right - CENTER_X, 30) : Math.max(CENTER_X - bounds.left, 30);
        const x = lk === "T" ? CENTER_X : CENTER_X + side * half * (0.2 + (i * 0.12));
        posMap[n.id] = { x: Math.round(x), y: lev.y };
      }
    });
  }

  nodes.forEach(n => {
    const pos = posMap[n.id] || { x: CENTER_X, y: 500 };
    const lk = nodeLevelKey(n);
    const sc = statusColor(n.status);
    const r = NODE_R[lk] || 8;
    svgHTML += `
    <g class="node-g" data-id="${n.id}" data-status="${n.status}" data-level="${lk}">
      <circle class="node-ring" cx="${pos.x}" cy="${pos.y}" r="${r + 8}"
        fill="none" stroke="${sc}" stroke-width="2"/>
      <circle class="node-bg" cx="${pos.x}" cy="${pos.y}" r="${r * 0.6}"
        fill="rgba(0,0,0,0.4)" stroke="${sc}" stroke-width="1.5"/>
      <circle class="node-core" cx="${pos.x}" cy="${pos.y}" r="${Math.max(2, r * 0.2)}"
        fill="${sc}"/>
    </g>`;
  });
"""

content = content[:idx_start] + new_repo + content[idx_end:]
changes += 1
print("  visible repo nodes OK")

# ═══════════════════════════════════════════════════════════
#  7. JS: SVG events + selectNode + highlightTreeNode + connector
# ═══════════════════════════════════════════════════════════
print("[7] JS: SVG events + selectNode + connector...")

# Find the SVG click events block
idx_svg_events = content.find('  // Node click events\n  svg.querySelectorAll(".node-g")')
if idx_svg_events == -1:
    # Try alternate marker
    idx_svg_events = content.find('  // Node click events')
    if idx_svg_events == -1:
        # Try the event block pattern
        idx_svg_events = content.find('svg.querySelectorAll(".node-g").forEach(g => {\n    g.addEventListener("click"')
        if idx_svg_events != -1:
            # Go back to find the comment
            idx_svg_events = content.rfind('\n', 0, idx_svg_events) + 1

if idx_svg_events == -1:
    print("  FAILED: SVG events marker not found")
    sys.exit(1)

# Find end of buildSVG function (the closing })
idx_buildsvg_end = content.find('\n}\n', idx_svg_events)
if idx_buildsvg_end == -1:
    print("  FAILED: end of buildSVG not found")
    sys.exit(1)
idx_buildsvg_end += 3  # include \n}\n

# Find selectNode function
idx_select_start = content.find('// ── NODE SELECTION ──\nfunction selectNode(id)')
if idx_select_start == -1:
    idx_select_start = content.find('function selectNode(id)')
    if idx_select_start != -1:
        # Include the comment before it if any
        line_start = content.rfind('\n', 0, idx_select_start)
        if line_start != -1 and '// ' in content[line_start:idx_select_start]:
            idx_select_start = line_start + 1

if idx_select_start == -1:
    print("  FAILED: selectNode not found")
    sys.exit(1)

# Find end of selectNode (ends with showDetail(node);\n})
idx_select_end = content.find('showDetail(node);\n}', idx_select_start)
if idx_select_end == -1:
    print("  FAILED: end of selectNode not found")
    sys.exit(1)
idx_select_end = content.find('\n', idx_select_end + len('showDetail(node);\n}')) + 1

new_svg_events_and_select = """  // Node click + hover events (bidirectional)
  svg.querySelectorAll(".node-g").forEach(g => {
    g.addEventListener("click", (e) => {
      e.stopPropagation();
      selectNode(g.dataset.id);
    });
    g.addEventListener("mouseenter", () => {
      const row = document.querySelector(`.node-row[data-id="${g.dataset.id}"]`);
      if (row) {
        row.classList.add("highlight");
        row.scrollIntoView({ behavior: "smooth", block: "nearest" });
      }
    });
    g.addEventListener("mouseleave", () => {
      const row = document.querySelector(`.node-row[data-id="${g.dataset.id}"]`);
      if (row) row.classList.remove("highlight");
    });
  });
}

// ── HIGHLIGHT TREE NODE (from sidebar hover) ──
function highlightTreeNode(id, on) {
  const g = document.querySelector(`.node-g[data-id="${id}"]`);
  if (!g) return;
  if (on) g.classList.add("highlight");
  else g.classList.remove("highlight");
}

// ── CONNECTOR LINE (sidebar row → tree node) ──
function updateConnector(id) {
  const svg = document.getElementById("connectorSvg");
  const app = document.querySelector(".app");
  if (!svg || !app) return;
  svg.setAttribute("width", app.clientWidth);
  svg.setAttribute("height", app.clientHeight);
  svg.innerHTML = "";
  if (!id) return;

  const row = document.querySelector(`.node-row[data-id="${id}"]`);
  const nodeG = document.querySelector(`.node-g[data-id="${id}"]`);
  if (!row || !nodeG) return;
  const circle = nodeG.querySelector("circle.node-bg");
  if (!circle) return;

  const rowRect = row.getBoundingClientRect();
  const appRect = app.getBoundingClientRect();
  const rowY = rowRect.top + rowRect.height / 2 - appRect.top;
  const rowX = rowRect.right - appRect.left;

  const cx = parseFloat(circle.getAttribute("cx"));
  const cy = parseFloat(circle.getAttribute("cy"));
  const sidebarW = 300;
  const nodeScreenX = sidebarW + panX + cx * zoom;
  const nodeScreenY = panY + cy * zoom;

  const midX = rowX + (nodeScreenX - rowX) * 0.4;
  svg.innerHTML = `
    <path class="connector-line active"
          d="M${rowX},${rowY} C${midX},${rowY} ${midX},${nodeScreenY} ${nodeScreenX},${nodeScreenY}"
          fill="none"/>
  `;
}

// ── NODE SELECTION ──
function selectNode(id) {
  selectedNodeId = id;
  const node = TREE_DATA.nodes.find(n => n.id === id);
  if (!node) return;

  // Highlight in table
  document.querySelectorAll(".node-row").forEach(i => i.classList.remove("selected"));
  const listItem = document.querySelector(`.node-row[data-id="${id}"]`);
  if (listItem) {
    listItem.classList.add("selected");
    listItem.scrollIntoView({ behavior: "smooth", block: "nearest" });
  }

  // Highlight in SVG
  document.querySelectorAll(".node-g").forEach(g => g.classList.remove("selected"));
  const svgNode = document.querySelector(`.node-g[data-id="${id}"]`);
  if (svgNode) svgNode.classList.add("selected");

  // Pan to node
  if (svgNode) {
    const circle = svgNode.querySelector("circle.node-bg");
    if (circle) {
      panToPoint(parseFloat(circle.getAttribute("cx")), parseFloat(circle.getAttribute("cy")));
    }
  }

  // Draw connector
  updateConnector(id);

  // Open detail
  showDetail(node);
}
"""

content = content[:idx_svg_events] + new_svg_events_and_select + content[idx_select_end:]
changes += 1
print("  SVG events + selectNode + connector OK")

# ═══════════════════════════════════════════════════════════
#  8. JS: Fix closeDetail() — .node-item → .node-row + connector
# ═══════════════════════════════════════════════════════════
print("[8] JS: closeDetail...")

old_close = '  document.querySelectorAll(".node-item").forEach(i => i.classList.remove("selected"));\n  document.querySelectorAll(".node-g").forEach(g => g.classList.remove("selected"));\n}'
new_close = '  document.querySelectorAll(".node-row").forEach(i => i.classList.remove("selected"));\n  document.querySelectorAll(".node-g").forEach(g => g.classList.remove("selected"));\n  updateConnector(null);\n}'

if old_close in content:
    content = content.replace(old_close, new_close, 1)
    changes += 1
    print("  closeDetail OK")
else:
    print("  WARN: closeDetail already patched or not found")

# ═══════════════════════════════════════════════════════════
#  9. JS: applyTransform() + connector update
# ═══════════════════════════════════════════════════════════
print("[9] JS: applyTransform...")

old_zoom = '  document.getElementById("zoomLevel").textContent = `${Math.round(zoom * 100)}%`;\n}'
new_zoom = '  document.getElementById("zoomLevel").textContent = `${Math.round(zoom * 100)}%`;\n  if (selectedNodeId) updateConnector(selectedNodeId);\n}'

if old_zoom in content:
    content = content.replace(old_zoom, new_zoom, 1)
    changes += 1
    print("  applyTransform OK")
else:
    print("  WARN: applyTransform not found")

# ═══════════════════════════════════════════════════════════
#  WRITE OUTPUT
# ═══════════════════════════════════════════════════════════

with open('templates/interactive_profile.html', 'w', encoding='utf-8') as f:
    f.write(content)

print(f"\nDONE — {changes} patches applied successfully")
