"""Escaped standalone review artifact without credentials."""

import html
import json
from pathlib import Path

from . import (
    __version__ as AUTOPM_VERSION,
)  # 每次升级递增版本号（唯一真源：autopm/__init__.py）


def enrich_display(plan, snapshot):
    """Show linked people/factory names while retaining IDs in write payloads."""
    lookup = {}
    all_fields = {}
    for table in snapshot.get("schema", {}).get("tables", []):
        primary = table.get("primaryFieldId")
        all_fields.update({field["id"]: field for field in table.get("fields", [])})
        for record in snapshot.get("records", {}).get(table["id"], []):
            lookup[record["id"]] = record.get("fields", {}).get(primary) or record["id"]
    for change in plan.get("changes", []):
        guard = next((g.get('unit_identity') for g in plan.get('project_guards', [])
                      if g['record_id'] == change.get('project_record_id')), None)
        if guard:
            unit = guard['number']+' / '+guard['sku']+' / '+', '.join(str(lookup.get(r,r)) for r in guard['factory_ids'])
            change['unit_label'] = unit
            title_field = change.get('identity',{}).get('title_field')
            title = change.get('fields',{}).get(title_field) or change.get('source_title') or change.get('identity',{}).get('title')
            change['record_title'] = unit + (' · '+str(title) if title else '')
        for origin, target in (
            ("before", "display_before"),
            ("fields", "display_after"),
        ):
            display = {}
            for fid, value in change.get(origin, {}).items():
                if all_fields.get(fid, {}).get(
                    "type"
                ) == "multipleRecordLinks" and isinstance(value, list):
                    display[fid] = [lookup.get(v, v) for v in value]
                else:
                    display[fid] = value
            change[target] = display
    return plan


def _fmt_cell(text):
    if text is None:
        return '<span class="null">(空)</span>'
    text = str(text)
    if len(text) > 300:
        return '<details><summary>展开完整内容（'+str(len(text))+' 字）</summary>'+html.escape(text).replace('\n','<br>')+'</details>'
    return html.escape(text).replace("\n", "<br>")


def _stats(plan):
    changes = plan.get("changes", [])
    stats = {"projects": 0, "tasks": 0, "issues": 0}
    for c in changes:
        k = c.get("kind")
        if k in stats:
            stats[k] += 1
    return stats, len(changes)


def _field_diff(name, old_val, new_val):
    """Render a single field difference row (empty string if no change)."""
    if old_val == new_val:
        return ""

    old_str = _fmt_cell(old_val)
    new_str = _fmt_cell(new_val)

    change_type = ""
    if old_val is None or old_val == "":
        change_type = "new-value"
    elif new_val is None or new_val == "":
        change_type = "removed"

    return (
        f'<div class="field-diff {change_type}">\n'
        f'  <div class="field-name">{name}</div>\n'
        f'  <div class="diff-content">\n'
        f'    <div class="diff-side before">{old_str}</div>\n'
        f'    <div class="diff-arrow">→</div>\n'
        f'    <div class="diff-side after">{new_str}</div>\n'
        f"  </div>\n"
        f"</div>"
    )


def _task_item(change):
    """Render a task item within a project card."""
    op_type = "新增" if not change.get("record_id") else "更新"
    op_class = "new" if not change.get("record_id") else "update"

    field_names = change.get("field_names", {})
    before = change.get("display_before", {})
    after = change.get("display_after", {})

    # Try to extract task name from a field that looks like a name/title
    task_name = html.escape(str(change['record_title'])) if change.get('record_title') else None
    for fid in change.get("fields", {}).keys():
        fname = field_names.get(fid, "")
        lowered = fname.lower()
        if any(k in lowered for k in ("name", "名称", "title", "标题")):
            task_name = html.escape(str(after.get(fid, before.get(fid, ""))))
            break
    if not task_name:
        task_name = "未命名任务"

    # Field diffs
    field_diffs = []
    for fid in change.get("fields", {}).keys():
        fname = html.escape(str(field_names.get(fid, fid)))
        old_val = before.get(fid)
        new_val = after.get(fid)
        diff_html = _field_diff(fname, old_val, new_val)
        if diff_html:
            field_diffs.append(diff_html)

    fields_html = (
        "\n".join(field_diffs)
        if field_diffs
        else '<div class="no-field-changes">字段值无变化</div>'
    )

    return (
        f'<div class="task-item {op_class}">\n'
        f'  <div class="task-header">\n'
        f'    <span class="task-badge {op_class}">{op_type}</span>\n'
        f'    <span class="task-name">{task_name}</span>\n'
        f"  </div>\n"
        f'  <div class="task-fields">\n'
        f"    {fields_html}\n"
        f"  </div>\n"
        f"</div>"
    )


def _project_card(project_id, items, record_id):
    """Render a single project card."""
    project_changes = [c for c in items if c.get("kind") == "projects"]
    task_changes = [c for c in items if c.get("kind") == "tasks"]
    issue_changes = [c for c in items if c.get("kind") == "issues"]

    new_tasks = len([c for c in task_changes if not c.get("record_id")])
    updated_tasks = len([c for c in task_changes if c.get("record_id")])

    has_changes = bool(project_changes or task_changes or issue_changes)

    # Project field diffs
    project_fields_html = []
    for c in project_changes:
        field_names = c.get("field_names", {})
        before = c.get("display_before", {})
        after = c.get("display_after", {})
        for fid in c.get("fields", {}).keys():
            fname = html.escape(str(field_names.get(fid, fid)))
            old_val = before.get(fid)
            new_val = after.get(fid)
            diff_html = _field_diff(fname, old_val, new_val)
            if diff_html:
                project_fields_html.append(diff_html)

    # Build card body
    body_parts = []
    if project_fields_html:
        body_parts.append(
            f'<div class="section-title">项目字段更新</div>\n'
            + "\n".join(project_fields_html)
        )
    else:
        body_parts.append('<div class="no-changes-hint">项目字段无变更</div>')

    if task_changes:
        task_items_html = "\n".join(_task_item(c) for c in task_changes)
        body_parts.append(
            f'<div class="section-title">'
            f'任务变更 <span class="section-count">({len(task_changes)} 条)</span>'
            f"</div>\n"
            f'<div class="task-list">\n'
            f"{task_items_html}\n"
            f"</div>"
        )

    if issue_changes:
        body_parts.append(
            f'<div class="section-title">'
            f'问题变更 <span class="section-count">({len(issue_changes)} 条)</span>'
            f"</div>" + '<div class="task-list">' + ''.join(_task_item(c) for c in issue_changes) + '</div>'
        )

    project_body = "\n".join(body_parts)

    # Badges
    badges = []
    if project_changes:
        badges.append(
            f'<span class="badge update">{len(project_changes)} 项目更新</span>'
        )
    if new_tasks:
        badges.append(f'<span class="badge new">{new_tasks} 新增任务</span>')
    if updated_tasks:
        badges.append(f'<span class="badge update">{updated_tasks} 更新任务</span>')

    badges_html = (
        " ".join(badges) if badges else '<span class="badge none">无变更</span>'
    )

    card_class = "has-changes" if has_changes else "no-changes"
    expanded = "true" if has_changes else "false"
    icon = "▼" if has_changes else "▶"
    display = "block" if has_changes else "none"

    return (
        f'<div class="project-card {card_class}" data-project="{project_id}" '
        f'id="proj-{record_id}">\n'
        f'  <div class="project-header" onclick="toggleProject(this)" '
        f'data-expanded="{expanded}">\n'
        f'    <span class="toggle-icon">{icon}</span>\n'
        f'    <span class="project-id">{project_id}</span>\n'
        f'    <span class="project-badges">{badges_html}</span>\n'
        f"  </div>\n"
        f'  <div class="project-body" style="display:{display}">\n'
        f"    {project_body}\n"
        f"  </div>\n"
        f"</div>"
    )


def save_preview(report, plan, directory):
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "parsed_report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    if plan is not None:
        (directory / "preview.json").write_text(
            json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    payload = plan if plan is not None else report

    if plan is None:
        # No plan yet: simplified JSON view
        content = html.escape(json.dumps(payload, ensure_ascii=False, indent=2))
        page = (
            f'<!doctype html><html lang="zh-CN"><meta charset="utf-8">\n'
            f"<title>AutoPM 导入预览</title><style>\n"
            f'body{{font:15px/1.65 "Microsoft YaHei",sans-serif;background:#f5f7fa;'
            f"color:#182b43;max-width:1180px;margin:40px auto;padding:0 24px}}\n"
            f"h1{{font-size:28px}}pre{{background:white;padding:24px;border:1px solid #dbe3ed;"
            f"white-space:pre-wrap;overflow-wrap:anywhere}}\n"
            f"</style><h1>AutoPM 本次导入预览</h1>\n"
            f"<p>源文件：{html.escape(str(report.get('source', '')))}。"
            f"此页面用于查看，本身不会写入 Airtable。</p><pre>{content}</pre></html>"
        )
        target = directory / "preview.html"
        target.write_text(page, encoding="utf-8")
        return target

    stats, total = _stats(plan)
    changes = plan.get("changes", [])

    # Group by project
    by_project = {}
    for c in changes:
        prid = c.get("project_record_id", "unknown")
        if prid not in by_project:
            by_project[prid] = {
                "project_id": c.get('unit_label') or c.get("project_id", ""),
                "items": [],
            }
        by_project[prid]["items"].append(c)

    # Generate project cards
    project_cards = []
    project_ids = []
    for prid, proj in by_project.items():
        project_id = html.escape(proj["project_id"])
        record_id = html.escape(str(prid), quote=True)
        project_ids.append((record_id,project_id))
        project_cards.append(_project_card(project_id, proj["items"],record_id))

    cards_html = "\n".join(project_cards)

    # Project quick-index
    index_html = "".join(
        f'<a href="#proj-{rid}" class="index-item" data-target="{rid}" '
        f'onclick="scrollToProject(event, this.dataset.target)">{pid}</a>'
        for rid,pid in sorted(project_ids)
    )

    source = html.escape(str(report.get("source", "")))
    report_date = html.escape(str(plan.get("report_date", "")))

    page = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AutoPM 导入预览 v{AUTOPM_VERSION} — {source}</title>
<style>
/* ===== Base ===== */
body{{
  font:14px/1.6 "Microsoft YaHei","PingFang SC",sans-serif;
  background:#f1f5f9;
  color:#0f172a;
  margin:0;
  padding:0;
}}
.container{{
  max-width:1200px;
  margin:0 auto;
  padding:16px 20px 40px;
}}

/* ===== Top Bar (sticky) ===== */
.top-bar{{
  position:sticky;
  top:0;
  z-index:200;
  background:rgba(255,255,255,0.95);
  backdrop-filter:blur(8px);
  border-bottom:1px solid #e2e8f0;
  padding:12px 20px;
  margin:-16px -20px 16px;
}}
.top-bar-inner{{
  max-width:1200px;
  margin:0 auto;
}}
.top-bar h1{{
  font-size:18px;
  margin:0 0 8px;
  font-weight:600;
}}
.top-bar .subtitle{{
  font-size:12px;
  color:#64748b;
  margin-bottom:12px;
}}

/* ===== Stats ===== */
.stats-bar{{
  display:flex;
  gap:12px;
  margin-bottom:12px;
  flex-wrap:wrap;
}}
.stat{{
  background:white;
  border:1px solid #e2e8f0;
  border-radius:8px;
  padding:10px 16px;
  min-width:100px;
  text-align:center;
}}
.stat .num{{
  font-size:24px;
  font-weight:700;
  color:#2563eb;
}}
.stat .label{{
  font-size:11px;
  color:#64748b;
  margin-top:2px;
}}

/* ===== Filter Bar ===== */
.filter-bar{{
  display:flex;
  gap:10px;
  align-items:center;
  flex-wrap:wrap;
  margin-bottom:4px;
}}
.filter-bar input, .filter-bar select{{
  padding:6px 10px;
  border:1px solid #cbd5e1;
  border-radius:6px;
  font-size:13px;
  background:white;
}}
.filter-bar input{{
  min-width:220px;
}}
.filter-bar button{{
  padding:6px 14px;
  border:0;
  border-radius:6px;
  background:#2563eb;
  color:white;
  font-size:13px;
  cursor:pointer;
}}
.filter-bar button:hover{{
  background:#1d4ed8;
}}
.filter-bar button.secondary{{
  background:#f8fafc;
  color:#475569;
  border:1px solid #e2e8f0;
}}
.filter-bar button.secondary:hover{{
  background:#f1f5f9;
}}
.filter-bar button.active{{
  background:#059669;
}}

/* ===== Project Index ===== */
.project-index{{
  display:flex;
  flex-wrap:wrap;
  gap:6px;
  margin:12px 0;
  padding:8px;
  background:white;
  border-radius:8px;
  border:1px solid #e2e8f0;
  max-height:120px;
  overflow-y:auto;
}}
.index-item{{
  padding:3px 8px;
  border-radius:4px;
  font-size:11px;
  color:#475569;
  background:#f8fafc;
  border:1px solid #e2e8f0;
  text-decoration:none;
  cursor:pointer;
}}
.index-item:hover{{
  background:#eff6ff;
  border-color:#3b82f6;
  color:#1d4ed8;
}}

/* ===== Project Card ===== */
.project-card{{
  background:white;
  border-radius:10px;
  border:1px solid #e2e8f0;
  margin-bottom:12px;
  overflow:hidden;
  box-shadow:0 1px 3px rgba(0,0,0,0.04);
  transition:box-shadow 0.2s;
}}
.project-card:hover{{
  box-shadow:0 4px 12px rgba(0,0,0,0.08);
}}
.project-card.no-changes{{
  opacity:0.7;
}}
.project-card.no-changes .project-header{{
  background:#f8fafc;
}}
.project-card.hidden{{
  display:none !important;
}}

.project-header{{
  padding:12px 16px;
  background:#f8fafc;
  cursor:pointer;
  display:flex;
  align-items:center;
  gap:10px;
  border-bottom:1px solid #e2e8f0;
  user-select:none;
}}
.project-header:hover{{
  background:#f1f5f9;
}}
.toggle-icon{{
  font-size:12px;
  color:#94a3b8;
  width:16px;
  text-align:center;
  transition:transform 0.2s;
}}
.project-id{{
  font-weight:700;
  font-size:14px;
  color:#1e293b;
  font-family:monospace;
}}
.project-badges{{
  margin-left:auto;
  display:flex;
  gap:6px;
}}
.badge{{
  padding:2px 8px;
  border-radius:10px;
  font-size:11px;
  font-weight:500;
}}
.badge.new{{
  background:#dcfce7;
  color:#166534;
}}
.badge.update{{
  background:#dbeafe;
  color:#1e40af;
}}
.badge.none{{
  background:#f1f5f9;
  color:#94a3b8;
}}

.project-body{{
  padding:0 16px 16px;
}}

/* ===== Section Title ===== */
.section-title{{
  font-weight:700;
  color:#475569;
  margin:16px 0 10px;
  font-size:12px;
  text-transform:uppercase;
  letter-spacing:0.8px;
  border-bottom:1px solid #e2e8f0;
  padding-bottom:4px;
}}
.section-count{{
  font-weight:400;
  color:#94a3b8;
  text-transform:none;
  letter-spacing:0;
  font-size:12px;
}}

/* ===== Field Diff ===== */
.field-diff{{
  display:flex;
  gap:12px;
  padding:10px 0;
  border-bottom:1px solid #f1f5f9;
  align-items:flex-start;
}}
.field-diff:last-child{{
  border-bottom:none;
}}
.field-name{{
  width:160px;
  flex-shrink:0;
  font-weight:600;
  color:#334155;
  font-size:12px;
  padding-top:2px;
}}
.diff-content{{
  display:flex;
  gap:10px;
  flex:1;
  align-items:flex-start;
}}
.diff-side{{
  flex:1;
  padding:8px 12px;
  border-radius:6px;
  font-size:13px;
  line-height:1.5;
  min-width:0;
  word-break:break-word;
}}
.diff-side.before{{
  background:#f8fafc;
  color:#64748b;
  border:1px solid #e2e8f0;
}}
.diff-side.after{{
  background:#f0fdf4;
  color:#0f172a;
  border-left:3px solid #22c55e;
  border:1px solid #bbf7d0;
  border-left:3px solid #22c55e;
}}
.diff-arrow{{
  color:#94a3b8;
  padding-top:8px;
  font-size:14px;
  flex-shrink:0;
}}

/* New value */
.field-diff.new-value .diff-side.after{{
  background:#dcfce7;
  border-left-color:#16a34a;
}}
.field-diff.new-value .diff-side.before{{
  opacity:0.4;
}}

/* Removed value */
.field-diff.removed .diff-side.after{{
  background:#fef2f2;
  border-left-color:#dc2626;
  border:1px solid #fecaca;
  border-left:3px solid #dc2626;
}}
.field-diff.removed .diff-side.before{{
  opacity:1;
  color:#0f172a;
}}

/* Null marker */
.null{{
  color:#94a3b8;
  font-style:italic;
}}

/* ===== Task Item ===== */
.task-list{{
  display:flex;
  flex-direction:column;
  gap:8px;
}}
.task-item{{
  padding:12px;
  border-radius:8px;
  background:#fafafa;
  border:1px solid #e2e8f0;
}}
.task-item.new{{
  background:#f0fdf4;
  border-left:4px solid #22c55e;
  border:1px solid #bbf7d0;
  border-left:4px solid #22c55e;
}}
.task-item.update{{
  background:#eff6ff;
  border-left:4px solid #3b82f6;
  border:1px solid #bfdbfe;
  border-left:4px solid #3b82f6;
}}
.task-header{{
  display:flex;
  align-items:center;
  gap:8px;
  margin-bottom:8px;
}}
.task-badge{{
  padding:2px 8px;
  border-radius:4px;
  font-size:11px;
  font-weight:600;
}}
.task-badge.new{{
  background:#16a34a;
  color:white;
}}
.task-badge.update{{
  background:#2563eb;
  color:white;
}}
.task-name{{
  font-weight:700;
  font-size:14px;
  color:#0f172a;
}}

/* ===== No changes hint ===== */
.no-changes-hint{{
  color:#94a3b8;
  font-style:italic;
  padding:16px;
  text-align:center;
  font-size:13px;
}}
.no-field-changes{{
  color:#94a3b8;
  font-size:12px;
  padding:4px 0;
}}

/* ===== Footer ===== */
.footer{{
  text-align:center;
  padding:20px;
  color:#94a3b8;
  font-size:11px;
  border-top:1px solid #e2e8f0;
  margin-top:20px;
}}

/* ===== Responsive ===== */
@media (max-width:768px){{
  .field-name{{ width:100px; }}
  .diff-content{{ flex-direction:column; }}
  .diff-arrow{{ display:none; }}
  .project-badges{{ flex-wrap:wrap; margin-left:0; margin-top:4px; }}
  .project-header{{ flex-wrap:wrap; }}
}}
</style>
</head>
<body>

<div class="container">

  <div class="top-bar">
    <div class="top-bar-inner">
      <h1>AutoPM 导入预览</h1>
      <div class="subtitle">
        源文件：{source} &nbsp;|&nbsp; 报告日期：{report_date} &nbsp;|&nbsp; 版本 v{AUTOPM_VERSION}
      </div>

      <div class="stats-bar">
        <div class="stat"><div class="num">{stats["projects"]}</div><div class="label">项目更新</div></div>
        <div class="stat"><div class="num">{stats["tasks"]}</div><div class="label">任务变更</div></div>
        <div class="stat"><div class="num">{stats["issues"]}</div><div class="label">问题变更</div></div>
        <div class="stat"><div class="num">{total}</div><div class="label">总记录数</div></div>
      </div>

      <div class="filter-bar">
        <input type="text" id="searchInput" placeholder="搜索项目ID或内容…" oninput="filterAll()">
        <select id="typeFilter" onchange="filterAll()">
          <option value="">全部类型</option>
          <option value="projects">仅项目更新</option>
          <option value="tasks">仅任务变更</option>
        </select>
        <select id="opFilter" onchange="filterAll()">
          <option value="">全部操作</option>
          <option value="new">仅新增</option>
          <option value="update">仅更新</option>
        </select>
        <button id="btnOnlyChanges" class="secondary" onclick="toggleOnlyChanges()">只看有变更</button>
        <button class="secondary" onclick="expandAll(true)">全部展开</button>
        <button class="secondary" onclick="expandAll(false)">全部折叠</button>
      </div>
    </div>
  </div>

  <div class="project-index" id="projectIndex">
    {index_html}
  </div>

  <div id="projectCards">
    {cards_html}
  </div>

  <div class="footer">
    AutoPM v{AUTOPM_VERSION} &nbsp;·&nbsp; 此预览页仅用于查看，不会写入 Airtable
  </div>

</div>

<script>
function toggleProject(header) {{
  const card = header.closest('.project-card');
  const body = card.querySelector('.project-body');
  const icon = header.querySelector('.toggle-icon');
  const expanded = header.dataset.expanded === 'true';
  
  if (expanded) {{
    body.style.display = 'none';
    icon.textContent = '▶';
    header.dataset.expanded = 'false';
  }} else {{
    body.style.display = 'block';
    icon.textContent = '▼';
    header.dataset.expanded = 'true';
  }}
}}

function expandAll(expand) {{
  document.querySelectorAll('.project-card').forEach(card => {{
    const header = card.querySelector('.project-header');
    const body = card.querySelector('.project-body');
    const icon = header.querySelector('.toggle-icon');
    if (expand) {{
      body.style.display = 'block';
      icon.textContent = '▼';
      header.dataset.expanded = 'true';
    }} else {{
      body.style.display = 'none';
      icon.textContent = '▶';
      header.dataset.expanded = 'false';
    }}
  }});
}}

let onlyChanges = false;
function toggleOnlyChanges() {{
  onlyChanges = !onlyChanges;
  const btn = document.getElementById('btnOnlyChanges');
  if (onlyChanges) {{
    btn.classList.add('active');
    btn.textContent = '显示全部';
  }} else {{
    btn.classList.remove('active');
    btn.textContent = '只看有变更';
  }}
  filterAll();
}}

function filterAll() {{
  const search = document.getElementById('searchInput').value.toLowerCase();
  const typeFilter = document.getElementById('typeFilter').value;
  const opFilter = document.getElementById('opFilter').value;
  
  document.querySelectorAll('.project-card').forEach(card => {{
    const projectId = card.dataset.project.toLowerCase();
    const headerText = card.querySelector('.project-header').innerText.toLowerCase();
    const bodyText = card.querySelector('.project-body').innerText.toLowerCase();
    const hasChanges = card.classList.contains('has-changes');
    
    let show = true;
    
    // Search filter
    if (search && !projectId.includes(search) && !bodyText.includes(search)) {{
      show = false;
    }}
    
    // Only changes filter
    if (onlyChanges && !hasChanges) {{
      show = false;
    }}
    
    // Type filter (check if card contains the type)
    if (typeFilter) {{
      const hasType = bodyText.includes(typeFilter === 'projects' ? '项目字段' : '任务');
      if (!hasType) show = false;
    }}
    
    // Op filter - hide individual task items instead of whole card
    // For simplicity, we show/hide the whole card if it contains matching ops
    if (opFilter) {{
      const badges = card.querySelector('.project-badges').innerText;
      if (opFilter === 'new' && !badges.includes('新增')) show = false;
      if (opFilter === 'update' && !badges.includes('更新')) show = false;
    }}
    
    card.style.display = show ? '' : 'none';
  }});
}}

function scrollToProject(event, pid) {{
  event.preventDefault();
  const el = document.getElementById('proj-' + pid);
  if (el) {{
    el.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    // Auto-expand
    const header = el.querySelector('.project-header');
    if (header.dataset.expanded === 'false') {{
      toggleProject(header);
    }}
  }}
}}

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {{
  if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {{
    e.preventDefault();
    document.getElementById('searchInput').focus();
  }}
}});
</script>

</body>
</html>"""

    target = directory / "preview.html"
    target.write_text(page, encoding="utf-8")
    return target
