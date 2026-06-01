"""
PDF Upload & Intelligent Parser for AutoPM
Extracts project data from uploaded PDF/DOCX files and auto-imports into the system.

Supports:
- Project briefs, schedules, meeting notes, NPI documents
- Extracts: project name, owner, dates, milestones, risks, department, brand
- Pattern matching for common SharkNinja PM document formats
"""

import re
import os
import json
from datetime import datetime, timedelta
from typing import List, Dict, Optional

UPLOAD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads", "documents")
os.makedirs(UPLOAD_DIR, exist_ok=True)


def extract_text_from_pdf(file_path: str) -> str:
    """Extract text from PDF file using pdfplumber (better for tables)."""
    text = ""
    try:
        import pdfplumber
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text() or ""
                text += page_text + "\n"
                # Also extract tables
                tables = page.extract_tables()
                for table in tables:
                    for row in table:
                        text += " | ".join([str(cell or "") for cell in row]) + "\n"
    except Exception as e:
        # Fallback to PyPDF2
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(file_path)
            for page in reader.pages:
                text += page.extract_text() or "" + "\n"
        except:
            pass
    return text


def extract_text_from_docx(file_path: str) -> str:
    """Extract text from DOCX file."""
    try:
        from docx import Document
        doc = Document(file_path)
        text = ""
        for para in doc.paragraphs:
            text += para.text + "\n"
        for table in doc.tables:
            for row in table.rows:
                text += " | ".join([cell.text for cell in row.cells]) + "\n"
        return text
    except ImportError:
        return ""


def extract_text(file_path: str) -> str:
    """Auto-detect file type and extract text."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == '.pdf':
        return extract_text_from_pdf(file_path)
    elif ext in ('.docx', '.doc'):
        return extract_text_from_docx(file_path)
    elif ext in ('.txt', '.md', '.csv'):
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    return ""


# ── Pattern Matchers ──────────────────────────────────

PROJECT_CODE_RE = re.compile(
    r'\b([A-Z]{2,4}[-–]\d{2,4})\b'  # e.g. XT-500, RV-900, AF-400
)

DATE_RE = re.compile(
    r'\b(\d{4}[-/]\d{1,2}[-/]\d{1,2}|\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|'
    r'(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*[\s.,]+\d{1,2}[\s,]+\d{2,4})\b',
    re.IGNORECASE
)

OWNER_RE = re.compile(
    r'(?:owner|assignee|responsible|lead|PM|manager)[:\s]+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)',
    re.IGNORECASE
)

DEPT_RE = re.compile(
    r'\b(PMO|PD|EE|ID|CMF|DQTP|SC|Quality|Compliance|MFG|Marketing|NPI|Engineering)\b',
    re.IGNORECASE
)

BRAND_RE = re.compile(
    r'\b(Shark|Ninja)\b',
    re.IGNORECASE
)

PHASE_RE = re.compile(
    r'\b(Kick\s*Off|Concept|Design|EB0|EB1|DQTP|Compliance|MP\s*Prep|MP|M8|Mass\s*Production)\b',
    re.IGNORECASE
)

PRIORITY_RE = re.compile(
    r'\b(P0|P1|P2|P3|Critical|High|Medium|Low)\b',
    re.IGNORECASE
)

MILESTONE_RE = re.compile(
    r'(?:G\d|Gate\s*\d|milestone|checkpoint|phase)[:\s]+([^\n]{5,80})',
    re.IGNORECASE
)

RISK_RE = re.compile(
    r'(?:risk|blocker|issue|delay|concern|bottleneck)[:\s–-]+([^\n]{5,120})',
    re.IGNORECASE
)

CATEGORY_RE = re.compile(
    r'\b(Extension|Legacy|NPD|Dual\s*Source|Capacity\s*Tools|Upsell|New\s*CMF|Transfer)\b',
    re.IGNORECASE
)


def parse_project_data(text: str, filename: str = "") -> Dict:
    """
    Parse extracted text and return structured project data.
    Returns a dict with:
      - projects: list of project dicts to import
      - raw_text: the full extracted text (for reference)
      - summary: what was found
    """
    projects = []
    summary = {
        "filename": filename,
        "text_length": len(text),
        "project_codes_found": [],
        "dates_found": [],
        "owners_found": [],
        "departments_found": [],
        "brands_found": [],
        "risks_found": [],
        "milestones_found": [],
    }

    # Extract all entities
    project_codes = list(set(PROJECT_CODE_RE.findall(text)))
    dates = DATE_RE.findall(text)
    owners = list(set(OWNER_RE.findall(text)))
    departments = list(set(DEPT_RE.findall(text)))
    brands = list(set(BRAND_RE.findall(text)))
    phases = list(set(PHASE_RE.findall(text)))
    priorities = list(set(PRIORITY_RE.findall(text)))
    milestones = MILESTONE_RE.findall(text)
    risks = RISK_RE.findall(text)
    categories = list(set(CATEGORY_RE.findall(text)))

    summary["project_codes_found"] = project_codes[:20]
    summary["dates_found"] = dates[:10]
    summary["owners_found"] = owners[:10]
    summary["departments_found"] = departments[:10]
    summary["brands_found"] = brands[:5]
    summary["risks_found"] = risks[:10]
    summary["milestones_found"] = milestones[:10]

    # If we found project codes, create a project for each
    if project_codes:
        for code in project_codes:
            # Try to infer metadata from context around the code
            project = {
                "name": code,
                "source_system": f"PDF Upload ({filename})",
                "source_file": filename,
            }

            # Try to find owner near this project code
            code_pos = text.find(code)
            context_window = text[max(0, code_pos-200):min(len(text), code_pos+200)]
            
            context_owner = OWNER_RE.search(context_window)
            if context_owner:
                project["owner"] = context_owner.group(1)

            context_dept = DEPT_RE.search(context_window)
            if context_dept:
                project["department"] = context_dept.group(1)

            context_brand = BRAND_RE.search(context_window)
            if context_brand:
                project["brand"] = context_brand.group(1)

            context_phase = PHASE_RE.search(context_window)
            if context_phase:
                project["phase"] = context_phase.group(1)

            context_priority = PRIORITY_RE.search(context_window)
            if context_priority:
                p = context_priority.group(1)
                if p in ('P0', 'Critical'):
                    project["priority"] = "P0"
                    project["risk_flag"] = "Critical"
                elif p in ('P1', 'High'):
                    project["priority"] = "P1"
                    project["risk_flag"] = "High"
                elif p in ('P2', 'Medium'):
                    project["priority"] = "P2"
                else:
                    project["priority"] = "P3"

            context_cat = CATEGORY_RE.search(context_window)
            if context_cat:
                project["category"] = context_cat.group(1)

            # Try to find dates
            context_dates = DATE_RE.findall(context_window)
            if len(context_dates) >= 2:
                project["start_date"] = _normalize_date(context_dates[0])
                project["end_date"] = _normalize_date(context_dates[-1])
            elif len(context_dates) == 1:
                project["end_date"] = _normalize_date(context_dates[0])

            # Default brand from overall document if not found in context
            if "brand" not in project and brands:
                project["brand"] = brands[0]
            if "department" not in project and departments:
                # Pick most common dept
                project["department"] = departments[0]

            projects.append(project)
    else:
        # No project codes found - try to create a generic project from the document
        # Use filename as project name hint
        base_name = os.path.splitext(filename)[0] if filename else "Uploaded"
        project = {
            "name": f"DOC-{base_name[:8].upper()}",
            "source_system": f"PDF Upload ({filename})",
            "source_file": filename,
            "notes": f"Auto-imported from {filename}",
        }
        
        if owners:
            project["owner"] = owners[0]
        if departments:
            project["department"] = departments[0]
        if brands:
            project["brand"] = brands[0]
        if phases:
            project["phase"] = phases[0]
        if priorities:
            project["priority"] = priorities[0]
        if dates:
            project["end_date"] = _normalize_date(dates[0])

        projects.append(project)

    # Extract milestones for each project
    if milestones:
        for proj in projects:
            proj["_milestones"] = [m.strip() for m in milestones[:10]]

    # Extract risks
    if risks:
        for proj in projects:
            proj["_risks"] = [r.strip() for r in risks[:5]]

    return {
        "projects": projects,
        "raw_text": text[:5000],  # First 5000 chars for preview
        "summary": summary,
    }


def _normalize_date(date_str: str) -> str:
    """Try to normalize various date formats to YYYY-MM-DD."""
    date_str = date_str.strip()
    
    # Already ISO format
    if re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return date_str
    
    # MM/DD/YYYY or MM-DD-YYYY
    m = re.match(r'^(\d{1,2})[-/](\d{1,2})[-/](\d{2,4})$', date_str)
    if m:
        mon, day, year = m.groups()
        year = year if len(year) == 4 else '20' + year
        return f"{year}-{int(mon):02d}-{int(day):02d}"
    
    # Try month name format
    try:
        from datetime import datetime
        dt = datetime.strptime(date_str.replace(',', '').replace('.', ''), '%b %d %Y')
        return dt.strftime('%Y-%m-%d')
    except:
        pass
    
    return date_str


def get_upload_history() -> List[Dict]:
    """Get list of previously uploaded files and their import status."""
    history_file = os.path.join(UPLOAD_DIR, "upload_history.json")
    if not os.path.exists(history_file):
        return []
    try:
        with open(history_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return []


def save_upload_history(entry: Dict):
    """Append to upload history."""
    history = get_upload_history()
    history.append(entry)
    # Keep last 50
    history = history[-50:]
    history_file = os.path.join(UPLOAD_DIR, "upload_history.json")
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)
