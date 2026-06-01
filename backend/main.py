from datetime import datetime, timedelta
from typing import Optional, List
import os

from fastapi import FastAPI, Depends, HTTPException, Query, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, StreamingResponse
from sqlalchemy.orm import Session
from collections import Counter

from database import engine, get_db, Base
from models import Project, Milestone, Risk, Alert, User, Feedback, UserProject
from schemas import (
    LoginRequest, TokenResponse, UserOut,
    ProjectCreate, ProjectUpdate, ProjectOut, ProjectDetail,
    MilestoneCreate, MilestoneUpdate, MilestoneOut,
    RiskCreate, RiskUpdate, RiskOut,
    AlertOut,
    FeedbackCreate, FeedbackOut,
    DashboardStats, TimelineItem,
    UserProjectCreate, UserProjectOut,
    ManualTaskCreate, ManualTaskUpdate,
)
from auth import (
    hash_password, verify_password, create_access_token,
    get_current_user, require_admin,
)
from alerts_engine import refresh_alerts
from feedback_persist import append_feedback

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AutoPM API", version="1.0.0")

# Run seed on startup via FastAPI lifespan event
@app.on_event("startup")
def startup_seed():
    from seed import seed
    seed()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ═══════════════════════════════════════════════════════
# Helper
# ═══════════════════════════════════════════════════════

def now_str() -> str:
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def trigger_refresh(db: Session):
    """Refresh alerts after any data change."""
    refresh_alerts(db)


# ═══════════════════════════════════════════════════════
# Health Check
# ═══════════════════════════════════════════════════════

@app.get("/api/health")
def health_check():
    return {"status": "ok", "timestamp": now_str()}


# ═══════════════════════════════════════════════════════
# Auth
# ═══════════════════════════════════════════════════════

@app.post("/api/auth/login", response_model=TokenResponse)
def login(req: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == req.username).first()
    if not user or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token({"sub": user.username, "role": user.role})
    return TokenResponse(access_token=token)


@app.get("/api/auth/me", response_model=UserOut)
def me(current_user: User = Depends(get_current_user)):
    return current_user


# ═══════════════════════════════════════════════════════
# Projects CRUD
# ═══════════════════════════════════════════════════════


@app.get("/api/projects/summary")
def get_projects_summary(db: Session = Depends(get_db)):
    """Lightweight summary for dashboard - uses SQL aggregation."""
    from collections import Counter, defaultdict
    import random
    from sqlalchemy import func, text as sql_text
    
    total = db.query(func.count(Project.id)).scalar() or 0
    by_status = dict(db.query(Project.status, func.count(Project.id)).group_by(Project.status).all())
    by_risk = dict(db.query(Project.risk_flag, func.count(Project.id)).group_by(Project.risk_flag).all())
    by_dept_rows = db.query(Project.department, func.count(Project.id)).group_by(Project.department).all()
    by_dept = {(s or 'Other'): c for s, c in by_dept_rows}
    by_cat_rows = db.query(Project.category, func.count(Project.id)).group_by(Project.category).all()
    by_category = {(s or 'Other'): c for s, c in by_cat_rows}
    by_brand_rows = db.query(Project.brand, func.count(Project.id)).group_by(Project.brand).all()
    by_brand = {(s or 'Other'): c for s, c in by_brand_rows}
    blocked_count = db.query(func.count(Project.id)).filter(Project.blocked_department != None, Project.blocked_department != '').scalar() or 0
    needs_decision_count = db.query(func.count(Project.id)).filter(Project.notes.like('%DECISION REQUIRED%')).scalar() or 0
    on_track = by_risk.get('None', 0) + by_risk.get('Low', 0)
    at_risk_count = by_risk.get('High', 0)
    delayed_count = by_risk.get('Critical', 0)
    # Dept risk summary via SQL
    dept_risk_rows = db.query(Project.department, Project.risk_flag, func.count(Project.id)).filter(Project.department != None).group_by(Project.department, Project.risk_flag).all()
    dept_risk_summary = defaultdict(lambda: {'total': 0, 'risk': 0})
    for dept, risk, cnt in dept_risk_rows:
        dept = dept or 'Other'
        dept_risk_summary[dept]['total'] += cnt
        if risk in ('High', 'Critical'):
            dept_risk_summary[dept]['risk'] += cnt
    # Top risk projects (only 10)
    risk_order_sql = "CASE risk_flag WHEN 'Critical' THEN 0 WHEN 'High' THEN 1 WHEN 'Medium' THEN 2 WHEN 'Low' THEN 3 ELSE 4 END"
    top_risk = db.query(Project).order_by(sql_text(risk_order_sql), Project.progress.asc()).limit(10).all()
    # Decision projects (only 5)
    needs_decision = db.query(Project).filter(Project.notes.like('%DECISION REQUIRED%')).limit(5).all()
    # 7-day trend (simulated based on current at_risk count)
    at_risk_total = at_risk_count + delayed_count
    trend = [at_risk_total - 4 + i + random.randint(-1, 1) for i in range(7)]
    trend[-1] = at_risk_total
    
    # By stage (lifecycle phase)
    by_stage_rows = db.query(Project.phase, func.count(Project.id)).group_by(Project.phase).all()
    by_stage = {(s or 'Other'): c for s, c in by_stage_rows}
    # By priority
    by_priority_rows = db.query(Project.priority, func.count(Project.id)).group_by(Project.priority).all()
    by_priority = {(s or 'P3'): c for s, c in by_priority_rows}
    
    return {
        "total": total,
        "by_status": by_status,
        "by_risk": by_risk,
        "by_department": by_dept,
        "by_category": by_category,
        "by_brand": by_brand,
        "by_stage": by_stage,
        "by_priority": by_priority,
        "blocked_count": blocked_count,
        "needs_decision_count": needs_decision_count,
        "on_track": on_track,
        "at_risk": at_risk_count,
        "delayed": delayed_count,
        "trend_7day": trend,
        "top_risk_projects": [{
            "id": p.id, "name": p.name, "category": p.category,
            "risk_flag": p.risk_flag, "progress": p.progress,
            "owner": p.owner, "department": p.department,
            "blocked_at": p.blocked_at, "blocked_days": p.blocked_days,
            "blocked_department": p.blocked_department, "notes": p.notes
        } for p in top_risk],
        "decision_projects": [{
            "id": p.id, "name": p.name, "category": p.category,
            "department": p.department, "notes": p.notes,
            "blocked_at": p.blocked_at, "blocked_department": p.blocked_department
        } for p in needs_decision],
        "dept_risk_summary": dict(dept_risk_summary)
    }


@app.get("/api/projects", response_model=List[ProjectOut])
def list_projects(
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    owner: Optional[str] = Query(None),
    department: Optional[str] = Query(None),
    limit: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Public: no auth required for reading projects
    q = db.query(Project)
    if status:
        q = q.filter(Project.status == status)
    if category:
        q = q.filter(Project.category == category)
    if owner:
        q = q.filter(Project.owner == owner)
    if department:
        q = q.filter(Project.department == department)
    # Default limit for performance: 100 if not specified
    if limit is None:
        limit = 100
    return q.order_by(Project.id).limit(limit).all()


@app.get("/api/projects/{project_id}", response_model=ProjectDetail)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Public: no auth required for reading project detail
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    milestones = db.query(Milestone).filter(Milestone.project_id == project_id).all()
    risks = db.query(Risk).filter(Risk.project_id == project_id).all()
    alerts = db.query(Alert).filter(Alert.project_id == project_id).all()
    return ProjectDetail(
        **{c.name: getattr(project, c.name) for c in project.__table__.columns},
        milestones=milestones,
        risks=risks,
        alerts=alerts,
    )


@app.post("/api/projects", response_model=ProjectOut, status_code=201)
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    now = now_str()
    project = Project(**data.model_dump(), created_at=now, updated_at=now)
    db.add(project)
    db.commit()
    db.refresh(project)
    trigger_refresh(db)
    return project


@app.put("/api/projects/{project_id}", response_model=ProjectOut)
def update_project(
    project_id: int,
    data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(project, k, v)
    project.updated_at = now_str()
    db.commit()
    db.refresh(project)
    trigger_refresh(db)
    return project


@app.delete("/api/projects/{project_id}", status_code=204)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    # Cascade delete related records
    db.query(Milestone).filter(Milestone.project_id == project_id).delete()
    db.query(Risk).filter(Risk.project_id == project_id).delete()
    db.query(Alert).filter(Alert.project_id == project_id).delete()
    db.delete(project)
    db.commit()
    trigger_refresh(db)


# ═══════════════════════════════════════════════════════
# Milestones CRUD
# ═══════════════════════════════════════════════════════

@app.get("/api/milestones", response_model=List[MilestoneOut])
def list_milestones(
    project_id: Optional[int] = Query(None),
    status: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Public: no auth required for reading milestones
    q = db.query(Milestone)
    if project_id:
        q = q.filter(Milestone.project_id == project_id)
    if status:
        q = q.filter(Milestone.status == status)
    return q.order_by(Milestone.id).all()


@app.post("/api/milestones", response_model=MilestoneOut, status_code=201)
def create_milestone(
    data: MilestoneCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    now = now_str()
    milestone = Milestone(**data.model_dump(), created_at=now, updated_at=now)
    db.add(milestone)
    db.commit()
    db.refresh(milestone)
    # Also update project's updated_at
    project = db.query(Project).filter(Project.id == data.project_id).first()
    if project:
        project.updated_at = now
        db.commit()
    trigger_refresh(db)
    return milestone


@app.put("/api/milestones/{milestone_id}", response_model=MilestoneOut)
def update_milestone(
    milestone_id: int,
    data: MilestoneUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(milestone, k, v)
    milestone.updated_at = now_str()
    # Also update project's updated_at
    project = db.query(Project).filter(Project.id == milestone.project_id).first()
    if project:
        project.updated_at = now_str()
    db.commit()
    db.refresh(milestone)
    trigger_refresh(db)
    return milestone


@app.delete("/api/milestones/{milestone_id}", status_code=204)
def delete_milestone(
    milestone_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    project_id = milestone.project_id
    db.delete(milestone)
    db.commit()
    # Update project's updated_at
    project = db.query(Project).filter(Project.id == project_id).first()
    if project:
        project.updated_at = now_str()
        db.commit()
    trigger_refresh(db)


# ═══════════════════════════════════════════════════════
# Risks
# ═══════════════════════════════════════════════════════

@app.get("/api/risks", response_model=List[RiskOut])
def list_risks(
    project_id: Optional[int] = Query(None),
    severity: Optional[str] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Public: no auth required for reading risks
    q = db.query(Risk)
    if project_id:
        q = q.filter(Risk.project_id == project_id)
    if severity:
        q = q.filter(Risk.severity == severity)
    return q.order_by(Risk.id).all()


@app.post("/api/risks", response_model=RiskOut, status_code=201)
def create_risk(
    data: RiskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    now = now_str()
    risk = Risk(**data.model_dump(), created_at=now, updated_at=now)
    db.add(risk)
    db.commit()
    db.refresh(risk)
    # Update project's risk_flag based on highest severity
    project = db.query(Project).filter(Project.id == data.project_id).first()
    if project:
        project.updated_at = now
        _update_project_risk_flag(db, project)
    trigger_refresh(db)
    return risk


@app.put("/api/risks/{risk_id}", response_model=RiskOut)
def update_risk(
    risk_id: int,
    data: RiskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    risk = db.query(Risk).filter(Risk.id == risk_id).first()
    if not risk:
        raise HTTPException(status_code=404, detail="Risk not found")
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(risk, k, v)
    risk.updated_at = now_str()
    project = db.query(Project).filter(Project.id == risk.project_id).first()
    if project:
        project.updated_at = now_str()
        _update_project_risk_flag(db, project)
    db.commit()
    db.refresh(risk)
    trigger_refresh(db)
    return risk


def _update_project_risk_flag(db: Session, project: Project):
    """Set project risk_flag to highest open risk severity."""
    severity_order = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1, "None": 0}
    risks = db.query(Risk).filter(
        Risk.project_id == project.id, Risk.status != "Closed"
    ).all()
    highest = "None"
    for r in risks:
        if severity_order.get(r.severity, 0) > severity_order.get(highest, 0):
            highest = r.severity
    project.risk_flag = highest


# ═══════════════════════════════════════════════════════


@app.post("/api/admin/dedup-milestones")
def dedup_milestones(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Remove duplicate milestones (same project_id + name). Keep the one with lowest ID."""
    from collections import defaultdict
    all_ms = db.query(Milestone).all()
    groups = defaultdict(list)
    for m in all_ms:
        key = (m.project_id, m.name)
        groups[key].append(m)
    deleted = 0
    for key, items in groups.items():
        if len(items) > 1:
            items.sort(key=lambda x: x.id)
            for item in items[1:]:
                db.delete(item)
                deleted += 1
    db.commit()
    return {"deleted_duplicates": deleted, "remaining": db.query(Milestone).count()}


@app.post("/api/admin/add-demo-data")
def add_demo_data(count: int = 2200, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Add demo/fake project data for L1/L2 views without touching real projects."""
    import random
    random.seed(42)
    
    existing_count = db.query(Project).count()
    if existing_count >= 100:
        return {"status": "skipped", "message": f"Already have {existing_count} projects"}
    
    now = datetime.utcnow()
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    
    CATEGORIES = ['NPD CAT A', 'NPD CAT B', 'NPD/Dual source', 'Extension', 'Legacy/Dual Source', 'Legacy/Transfer', 'Capacity Tools', 'New CMF', 'Upsell']
    FACTORIES = [f'Factory {chr(65+i)}' for i in range(20)]
    OWNERS = ['L****', 'N*****', 'S****', 'B***', 'H****', 'K***', 'N**', 'M*******', 'T******', 'S******', 'Z***', 'A*****']
    PHASES = ['Kick Off', 'Concept', 'Design', 'EB0', 'EB1', 'DQTP', 'Compliance', 'M8', 'MP Prep', 'MP']
    BRANDS = ['Shark', 'Ninja']
    DEPARTMENTS = ['PMO', 'PD', 'NPI', 'EE', 'CMF', 'DQTP', 'SC', 'Quality', 'Compliance', 'MFG', 'Marketing', 'ID']
    
    prefix_parts = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    num_parts = '0123456789'
    
    created = 0
    for i in range(count):
        cat = random.choice(CATEGORIES)
        brand = 'Ninja' if cat in ['NPD CAT A', 'NPD CAT B', 'NPD/Dual source', 'Extension', 'Upsell'] else 'Shark'
        prefix = random.choice(prefix_parts) + random.choice(prefix_parts)
        num = str(random.randint(100, 999))
        name = f"{prefix}-{num}"
        
        phase = random.choice(PHASES)
        progress_map = {'Kick Off': 5, 'Concept': 15, 'Design': 25, 'EB0': 40, 'EB1': 55, 'DQTP': 65, 'Compliance': 72, 'M8': 80, 'MP Prep': 88, 'MP': 95}
        base_progress = progress_map.get(phase, 50)
        progress = min(100, max(0, base_progress + random.randint(-10, 10)))
        
        risk = random.choices(['None', 'High', 'Critical'], weights=[0.6, 0.25, 0.15])[0]
        status = 'Completed' if progress >= 100 else 'In Progress'
        
        p = Project(
            name=name, category=cat, brand=brand,
            factory=random.choice(FACTORIES), phase=phase,
            status=status, progress=float(progress),
            department=random.choice(DEPARTMENTS),
            owner=random.choice(OWNERS),
            risk_flag=risk,
            start_date=(now - timedelta(days=random.randint(10, 200))).strftime('%Y-%m-%d'),
            created_at=now_str, updated_at=now_str,
        )
        db.add(p)
        created += 1
        
        if created % 500 == 0:
            db.flush()
    
    db.commit()
    return {"created": created, "total_projects": db.query(Project).count()}
# Alerts
# ═══════════════════════════════════════════════════════

@app.get("/api/alerts", response_model=List[AlertOut])
def list_alerts(
    level: Optional[str] = Query(None),
    type: Optional[str] = Query(None),
    is_read: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Public: no auth required for reading alerts
    q = db.query(Alert)
    if level:
        q = q.filter(Alert.level == level)
    if type:
        q = q.filter(Alert.type == type)
    if is_read is not None:
        q = q.filter(Alert.is_read == is_read)
    return q.order_by(Alert.id.desc()).all()


@app.put("/api/alerts/{alert_id}/read", response_model=AlertOut)
def mark_alert_read(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    alert.is_read = 1
    db.commit()
    db.refresh(alert)
    return alert


@app.post("/api/alerts/refresh")
def refresh_all_alerts(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    count = refresh_alerts(db)
    return {"generated_alerts": count}


# ═══════════════════════════════════════════════════════
# Dashboard
# ═══════════════════════════════════════════════════════

@app.get("/api/dashboard/stats", response_model=DashboardStats)
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Public: no auth required for reading dashboard stats
    projects = db.query(Project).all()
    total = len(projects)
    by_status = dict(Counter(p.status for p in projects))

    # Overdue milestones
    now = datetime.utcnow()
    overdue_count = 0
    due_soon_count = 0
    milestones = db.query(Milestone).all()
    for ms in milestones:
        if (ms.status and ms.status.lower() == "completed") or not ms.due_date:
            continue
        try:
            due = datetime.strptime(ms.due_date, "%Y-%m-%d")
        except ValueError:
            continue
        days_diff = (due - now).days
        if days_diff < 0:
            overdue_count += 1
        elif days_diff <= 3:
            due_soon_count += 1

    alert_count = db.query(Alert).filter(Alert.is_read == 0).count()

    return DashboardStats(
        total=total,
        by_status=by_status,
        overdue_count=overdue_count,
        alert_count=alert_count,
        due_soon_count=due_soon_count,
    )


@app.get("/api/dashboard/timeline", response_model=List[TimelineItem])
def dashboard_timeline(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Public: no auth required for reading timeline
    projects = db.query(Project).order_by(Project.end_date).all()
    result = []
    for p in projects:
        ms = db.query(Milestone).filter(Milestone.project_id == p.id).order_by(Milestone.due_date).all()
        result.append(TimelineItem(project=p, milestones=ms))
    return result


# ═══════════════════════════════════════════════════════
# Public APIs (no auth required - for personal view)
# ═══════════════════════════════════════════════════════

@app.get("/api/public/team-members")
def get_team_members(db: Session = Depends(get_db)):
    """Return deduplicated list of all team members from project owners and milestone owners."""
    owners = set()
    # From project owners
    for p in db.query(Project).all():
        if p.owner:
            for o in p.owner.split(","):
                o = o.strip()
                if o:
                    owners.add(o)
    # From milestone owners
    for m in db.query(Milestone).all():
        if m.owner:
            for o in m.owner.split(","):
                o = o.strip()
                if o:
                    owners.add(o)
    # From risk owners
    for r in db.query(Risk).all():
        if r.owner:
            for o in r.owner.split(","):
                o = o.strip()
                if o:
                    owners.add(o)
    return sorted(list(owners))


# ═══════════════════════════════════════════════════════
# Visitor Count API
# ═══════════════════════════════════════════════════════

@app.post("/api/public/visit")
def record_visit(db: Session = Depends(get_db)):
    """Increment visitor count. Creates the record if it doesn't exist."""
    from sqlalchemy import text as sql_text
    # Ensure the visit_count table exists
    db.execute(sql_text("""
        CREATE TABLE IF NOT EXISTS visit_count (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            count INTEGER NOT NULL DEFAULT 0
        )
    """))
    db.commit()
    # Try to update existing row
    result = db.execute(sql_text("UPDATE visit_count SET count = count + 1 WHERE id = 1"))
    if result.rowcount == 0:
        # No row yet, insert one with count = 1
        db.execute(sql_text("INSERT INTO visit_count (id, count) VALUES (1, 1)"))
    db.commit()
    # Return the new count
    row = db.execute(sql_text("SELECT count FROM visit_count WHERE id = 1")).fetchone()
    return {"count": row[0] if row else 1}


@app.get("/api/public/visit-count")
def get_visit_count(db: Session = Depends(get_db)):
    """Return current visitor count."""
    from sqlalchemy import text as sql_text
    try:
        row = db.execute(sql_text("SELECT count FROM visit_count WHERE id = 1")).fetchone()
        return {"count": row[0] if row else 0}
    except Exception:
        return {"count": 0}


@app.get("/api/public/my-dashboard/{owner_name:path}")
def get_my_dashboard(owner_name: str, db: Session = Depends(get_db)):
    """Return personalized dashboard data for a specific team member."""
    now = datetime.utcnow()

    # Find projects owned by this person
    all_projects = db.query(Project).all()
    my_projects = []
    for p in all_projects:
        if p.owner and owner_name.lower() in p.owner.lower():
            my_projects.append(p)

    # Risk summary
    total_projects = len(my_projects)
    risk_projects = len([p for p in my_projects if p.risk_flag in ("High", "Critical")])
    medium_risk_projects = len([p for p in my_projects if p.risk_flag == "Medium"])
    normal_projects = total_projects - risk_projects - medium_risk_projects

    # My tasks (milestones where owner matches)
    all_milestones = db.query(Milestone).all()
    my_tasks = []
    for m in all_milestones:
        if m.owner and owner_name.lower() in m.owner.lower() and m.status != "Completed":
            # Determine urgency
            overdue = False
            due_soon = False
            days_until_due = None
            if m.due_date:
                try:
                    due = datetime.strptime(m.due_date, "%Y-%m-%d")
                    days_until_due = (due - now).days
                    if days_until_due < 0 and m.status != "Completed":
                        overdue = True
                    elif days_until_due <= 3:
                        due_soon = True
                except ValueError:
                    pass

            # Get project info
            project = next((p for p in all_projects if p.id == m.project_id), None)

            my_tasks.append({
                "id": m.id,
                "name": m.name,
                "project_id": m.project_id,
                "project_name": project.name if project else "Unknown",
                "phase": m.phase,
                "due_date": m.due_date,
                "status": m.status,
                "owner": m.owner,
                "overdue": overdue,
                "due_soon": due_soon,
                "days_until_due": days_until_due,
                "project_risk_flag": project.risk_flag if project else "None",
            })

    # Sort: overdue first, then due_soon, then by days_until_due
    urgency_order = {"Overdue": 0, "Due Soon": 1, "In Progress": 2, "Not Started": 3}
    def task_sort_key(t):
        if t["overdue"]:
            primary = 0
        elif t["due_soon"]:
            primary = 1
        elif t["status"] == "In Progress":
            primary = 2
        else:
            primary = 3
        secondary = t["days_until_due"] if t["days_until_due"] is not None else 9999
        return (primary, secondary)

    my_tasks.sort(key=task_sort_key)

    # My risks
    all_risks = db.query(Risk).all()
    my_risks = []
    for r in all_risks:
        if r.owner and owner_name.lower() in r.owner.lower() and r.status != "Closed":
            project = next((p for p in all_projects if p.id == r.project_id), None)
            my_risks.append({
                "id": r.id,
                "description": r.description,
                "severity": r.severity,
                "project_id": r.project_id,
                "project_name": project.name if project else "Unknown",
                "status": r.status,
            })

    # Overdue count
    overdue_count = len([t for t in my_tasks if t["overdue"]])
    due_soon_count = len([t for t in my_tasks if t["due_soon"]])

    return {
        "owner": owner_name,
        "projects": {
            "total": total_projects,
            "at_risk": risk_projects,
            "medium_risk": medium_risk_projects,
            "normal": normal_projects,
        },
        "tasks": {
            "total": len(my_tasks),
            "overdue": overdue_count,
            "due_soon": due_soon_count,
            "items": my_tasks,
        },
        "risks": {
            "total": len(my_risks),
            "items": my_risks,
        },
    }



# ═══════════════════════════════════════════════════════
# CSV Import / Export
# ═══════════════════════════════════════════════════════

import csv
import io

VALID_STATUSES = {"On Track", "At Risk", "Delayed", "Delay", "In Progress", "Completed"}
VALID_TYPES = {"NPD", "NPD CAT A", "NPD CAT B", "NPD/Dual source", "Extension", "Cost Out", "Color Refresh", "New CMF", "Legacy/Dual Source", "Legacy/Transfer", "Capacity Tools", "Upsell"}
VALID_PHASES = {"Concept", "Design", "DQTP", "Compliance", "Production", "Launch",
                "Kick Off", "EB0", "EB1", "MP Prep", "MP"}
VALID_PRIORITIES = {"P1", "P2", "P3"}


@app.get("/api/projects/template")
def download_csv_template():
    """Download the CSV import template."""
    template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "template_projects.csv")
    if os.path.exists(template_path):
        return FileResponse(template_path, filename="template_projects.csv", media_type="text/csv")
    # Fallback: generate template on-the-fly
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["project_name", "project_type", "current_phase", "status", "pm_name",
                      "brand", "factory", "department", "blocked_at", "blocked_days", "blocked_department",
                      "start_date", "target_launch_date", "priority", "notes"])
    writer.writerow(["Project-Alpha", "NPD", "Design", "On Track", "Alice Wang", "Ninja", "Factory-A", "R&D",
                      "", "0", "", "2026-01-15", "2026-09-30", "P1",
                      "New product development for US market"])
    writer.writerow(["Project-Beta", "Extension", "DQTP", "At Risk", "Bob Chen", "Ninja", "Factory-B", "Engineering",
                      "Compliance", "14", "Quality", "2026-02-01", "2026-07-15", "P2",
                      "Waiting for compliance approval"])
    output.seek(0)
    return StreamingResponse(io.BytesIO(output.getvalue().encode("utf-8")),
                             media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=template_projects.csv"})


@app.post("/api/projects/import")
async def import_projects_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Import projects from a CSV file. Upsert by project_name."""
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")

    content = await file.read()
    try:
        text = content.decode("utf-8-sig")  # Handle BOM
    except UnicodeDecodeError:
        try:
            text = content.decode("gbk")  # Try Chinese encoding
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="Cannot decode file. Use UTF-8 or GBK encoding.")

    reader = csv.DictReader(io.StringIO(text))
    rows = list(reader)

    if not rows:
        raise HTTPException(status_code=400, detail="CSV file is empty or has no data rows")

    created_count = 0
    updated_count = 0
    failed_count = 0
    errors = []

    for row_idx, row in enumerate(rows, start=2):  # Row 2 = first data row (1 is header)
        try:
            # Required field check
            project_name = (row.get("project_name") or "").strip()
            if not project_name:
                errors.append({"row": row_idx, "error": "project_name is required"})
                failed_count += 1
                continue

            # Map CSV fields to model fields
            csv_status = (row.get("status") or "").strip()
            # Normalize status
            status_map = {
                "On Track": "In Progress",
                "At Risk": "In Progress",
                "Delayed": "In Progress",
                "Delay": "In Progress",
                "In Progress": "In Progress",
                "Completed": "Completed",
            }
            mapped_status = status_map.get(csv_status, "In Progress")

            # Determine risk_flag from status
            risk_map = {"On Track": "None", "At Risk": "High", "Delayed": "Critical", "Delay": "Critical", "In Progress": "None", "Completed": "None"}
            risk_flag = risk_map.get(csv_status, "None")

            csv_type = (row.get("project_type") or "").strip()
            phase = (row.get("current_phase") or "").strip()
            owner = (row.get("pm_name") or row.get("npi_lead") or "").strip()
            brand = (row.get("brand") or "").strip()
            factory = (row.get("factory") or "").strip()
            department = (row.get("department") or "").strip()
            blocked_at = (row.get("blocked_at") or "").strip()
            blocked_days_str = (row.get("blocked_days") or "0").strip()
            blocked_department = (row.get("blocked_department") or "").strip()
            start_date = (row.get("start_date") or "").strip()
            end_date = (row.get("target_launch_date") or "").strip()
            priority = (row.get("priority") or "").strip()
            notes = (row.get("notes") or row.get("delay_reason") or "").strip()

            # Validate date formats
            for field_name, date_val in [("start_date", start_date), ("target_launch_date", end_date)]:
                if date_val:
                    try:
                        datetime.strptime(date_val, "%Y-%m-%d")
                    except ValueError:
                        errors.append({"row": row_idx, "error": f"Invalid date format for {field_name}: '{date_val}'. Use YYYY-MM-DD"})
                        failed_count += 1
                        break
            else:
                # Parse blocked_days
                try:
                    blocked_days = int(blocked_days_str) if blocked_days_str else 0
                except ValueError:
                    errors.append({"row": row_idx, "error": f"Invalid blocked_days: '{blocked_days_str}'. Must be integer"})
                    failed_count += 1
                    continue

                # Build risk_note from blocked info or delay_reason
                delay_reason = (row.get("delay_reason") or "").strip()
                risk_note = ""
                if delay_reason:
                    risk_note = delay_reason
                elif blocked_at and blocked_days > 0:
                    risk_note = f"Blocked at {blocked_at} for {blocked_days} days, waiting on {blocked_department or 'unknown'}"
                    if risk_flag == "None":
                        risk_flag = "High"

                # Calculate progress from phase
                phase_progress = {
                    "Concept": 10, "Design": 25, "DQTP": 40, "Compliance": 55,
                    "Production": 75, "Launch": 90, "Kick Off": 5, "EB0": 20,
                    "EB1": 35, "MP Prep": 70, "MP": 85,
                }
                progress = float(phase_progress.get(phase, 0))

                # Upsert: find existing project by name
                existing = db.query(Project).filter(Project.name == project_name).first()
                now = now_str()

                if existing:
                    existing.category = csv_type or existing.category
                    existing.status = mapped_status
                    existing.phase = phase or existing.phase
                    existing.owner = owner or existing.owner
                    existing.brand = brand or existing.brand
                    existing.factory = factory or existing.factory
                    existing.start_date = start_date or existing.start_date
                    existing.end_date = end_date or existing.end_date
                    existing.progress = progress if progress > 0 else existing.progress
                    existing.risk_flag = risk_flag
                    existing.risk_note = risk_note or existing.risk_note
                    existing.source_system = "CSV Import"
                    existing.department = department or existing.department
                    existing.blocked_at = blocked_at or existing.blocked_at
                    existing.blocked_days = blocked_days
                    existing.blocked_department = blocked_department or existing.blocked_department
                    existing.priority = priority or existing.priority
                    existing.notes = notes or existing.notes
                    existing.updated_at = now
                    updated_count += 1
                else:
                    project = Project(
                        name=project_name,
                        category=csv_type or None,
                        status=mapped_status,
                        phase=phase or None,
                        owner=owner or None,
                        brand=brand or None,
                        factory=factory or None,
                        start_date=start_date or None,
                        end_date=end_date or None,
                        progress=progress,
                        risk_flag=risk_flag,
                        risk_note=risk_note or None,
                        source_system="CSV Import",
                        department=department or None,
                        blocked_at=blocked_at or None,
                        blocked_days=blocked_days,
                        blocked_department=blocked_department or None,
                        priority=priority or None,
                        notes=notes or None,
                        created_at=now,
                        updated_at=now,
                    )
                    db.add(project)
                    created_count += 1

                db.commit()

        except Exception as e:
            errors.append({"row": row_idx, "error": str(e)})
            failed_count += 1
            db.rollback()

    trigger_refresh(db)

    return {
        "created": created_count,
        "updated": updated_count,
        "failed": failed_count,
        "errors": errors,
    }


@app.get("/api/projects/export")
def export_projects_csv(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Export all projects as CSV."""
    projects = db.query(Project).order_by(Project.id).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["project_name", "project_type", "current_phase", "status", "pm_name",
                      "brand", "factory", "department", "blocked_at", "blocked_days", "blocked_department",
                      "start_date", "target_launch_date", "priority", "notes"])

    # Reverse status mapping
    status_reverse_map = {
        "In Progress": "On Track",
        "Completed": "On Track",
    }

    for p in projects:
        # Try to recover original CSV status from risk_flag
        csv_status = "On Track"
        if p.status == "Completed":
            csv_status = "On Track"
        elif p.risk_flag in ("High", "Critical"):
            csv_status = "Delayed" if (p.blocked_days or 0) > 14 else "At Risk"
        elif p.risk_flag == "Medium":
            csv_status = "At Risk"

        writer.writerow([
            p.name or "",
            p.category or "",
            p.phase or "",
            csv_status,
            p.owner or "",
            p.brand or "",
            p.factory or "",
            p.department or "",
            p.blocked_at or "",
            p.blocked_days or 0,
            p.blocked_department or "",
            p.start_date or "",
            p.end_date or "",
            p.priority or "",
            p.notes or "",
        ])

    output.seek(0)
    return StreamingResponse(
        io.BytesIO(output.getvalue().encode("utf-8")),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=autopm_projects_export.csv"},
    )



# ═══════════════════════════════════════════════════════
# Feedback
# ═══════════════════════════════════════════════════════

@app.post("/api/feedback", response_model=FeedbackOut, status_code=201)
def create_feedback(req: FeedbackCreate):
    """Create feedback - stored in JSON file for persistence across deploys."""
    from feedback_persist import append_feedback, load_feedback_from_json
    import time
    created = now_str()
    entry = {
        "name": req.name or "Anonymous",
        "role": req.role,
        "category": req.category,
        "content": req.content,
        "created_at": created,
    }
    append_feedback(entry)
    # Return in FeedbackOut format (need an id)
    entries = load_feedback_from_json()
    return FeedbackOut(id=len(entries), name=entry["name"], role=entry["role"],
                       category=entry["category"], content=entry["content"],
                       created_at=created)


@app.get("/api/feedback", response_model=List[FeedbackOut])
def list_feedback():
    """List all feedback - read from JSON file for persistence across deploys."""
    from feedback_persist import load_feedback_from_json
    entries = load_feedback_from_json()
    # Return in reverse order (newest first)
    result = []
    for i, e in enumerate(reversed(entries)):
        result.append(FeedbackOut(
            id=len(entries) - i,
            name=e.get("name", "Anonymous"),
            role=e.get("role", ""),
            category=e.get("category", "suggestion"),
            content=e.get("content", ""),
            created_at=e.get("created_at", ""),
        ))
    return result

# ═══════════════════════════════════════════════════════
# User Projects (Star / Follow)
# ═══════════════════════════════════════════════════════

@app.get("/api/user-projects/{username}", response_model=List[UserProjectOut])
def get_user_projects(username: str, db: Session = Depends(get_db)):
    """Get list of projects starred/followed by a user."""
    return db.query(UserProject).filter(UserProject.username == username).all()


@app.post("/api/user-projects", response_model=UserProjectOut, status_code=201)
def add_user_project(data: UserProjectCreate, db: Session = Depends(get_db)):
    """Star/follow a project for a user."""
    existing = db.query(UserProject).filter(
        UserProject.username == data.username,
        UserProject.project_id == data.project_id,
    ).first()
    if existing:
        return existing
    up = UserProject(
        username=data.username,
        project_id=data.project_id,
        created_at=now_str(),
    )
    db.add(up)
    db.commit()
    db.refresh(up)
    return up


@app.delete("/api/user-projects/{username}/{project_id}", status_code=204)
def remove_user_project(username: str, project_id: int, db: Session = Depends(get_db)):
    """Unstar/unfollow a project for a user."""
    up = db.query(UserProject).filter(
        UserProject.username == username,
        UserProject.project_id == project_id,
    ).first()
    if not up:
        raise HTTPException(status_code=404, detail="User project not found")
    db.delete(up)
    db.commit()


# ═══════════════════════════════════════════════════════
# Manual Tasks (Today's Tasks - user-created)
# ═══════════════════════════════════════════════════════

@app.post("/api/tasks/manual", response_model=MilestoneOut, status_code=201)
def create_manual_task(data: ManualTaskCreate, db: Session = Depends(get_db)):
    """Create a manual task (stored as Milestone with is_manual=1)."""
    now = now_str()
    milestone = Milestone(
        project_id=data.project_id or 0,
        name=data.name,
        phase="Manual Task",
        due_date=data.due_date,
        status="Not Started",
        owner=data.owner,
        is_manual=1,
        manual_priority=data.manual_priority or "P3",
        manual_notes=data.manual_notes,
        created_at=now,
        updated_at=now,
    )
    db.add(milestone)
    db.commit()
    db.refresh(milestone)
    return milestone


@app.get("/api/tasks/manual", response_model=List[MilestoneOut])
def list_manual_tasks(
    owner: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    """List all manual tasks."""
    q = db.query(Milestone).filter(Milestone.is_manual == 1)
    if owner:
        q = q.filter(Milestone.owner == owner)
    return q.order_by(Milestone.id.desc()).all()


@app.put("/api/tasks/manual/{task_id}", response_model=MilestoneOut)
def update_manual_task(
    task_id: int,
    data: ManualTaskUpdate,
    db: Session = Depends(get_db),
):
    """Update a manual task."""
    milestone = db.query(Milestone).filter(
        Milestone.id == task_id,
        Milestone.is_manual == 1,
    ).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Manual task not found")
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(milestone, k, v)
    milestone.updated_at = now_str()
    db.commit()
    db.refresh(milestone)
    return milestone


@app.delete("/api/tasks/manual/{task_id}", status_code=204)
def delete_manual_task(
    task_id: int,
    db: Session = Depends(get_db),
):
    """Delete a manual task."""
    milestone = db.query(Milestone).filter(
        Milestone.id == task_id,
        Milestone.is_manual == 1,
    ).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Manual task not found")
    db.delete(milestone)
    db.commit()


# ═══════════════════════════════════════════════════════
# Project Tasks (CRUD for project-level tasks/milestones)
# ═══════════════════════════════════════════════════════

@app.post("/api/projects/{project_id}/tasks", response_model=MilestoneOut, status_code=201)
def create_project_task(
    project_id: int,
    data: ManualTaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create a new task for a project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    now = now_str()
    milestone = Milestone(
        project_id=project_id,
        name=data.name,
        phase=data.phase if hasattr(data, 'phase') and data.phase else "Manual Task",
        due_date=data.due_date,
        status="Not Started",
        owner=data.owner,
        is_manual=1,
        manual_priority=data.manual_priority or "P2",
        manual_notes=data.manual_notes,
        created_at=now,
        updated_at=now,
    )
    db.add(milestone)
    db.commit()
    db.refresh(milestone)
    return milestone


@app.put("/api/projects/{project_id}/tasks/{task_id}", response_model=MilestoneOut)
def update_project_task(
    project_id: int,
    task_id: int,
    data: ManualTaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Update a project task (status, due date, assignee, priority)."""
    milestone = db.query(Milestone).filter(
        Milestone.id == task_id,
        Milestone.project_id == project_id,
    ).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Task not found")
    update_data = data.model_dump(exclude_unset=True)
    for k, v in update_data.items():
        setattr(milestone, k, v)
    milestone.updated_at = now_str()
    db.commit()
    db.refresh(milestone)
    return milestone


@app.delete("/api/projects/{project_id}/tasks/{task_id}", status_code=204)
def delete_project_task(
    project_id: int,
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Delete a project task."""
    milestone = db.query(Milestone).filter(
        Milestone.id == task_id,
        Milestone.project_id == project_id,
    ).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(milestone)
    db.commit()


# ═══════════════════════════════════════════════════════
# Project Blockers
# ═══════════════════════════════════════════════════════

@app.get("/api/projects/{project_id}/blockers")
def get_project_blockers(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get blockers (open risks) for a project."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    risks = db.query(Risk).filter(
        Risk.project_id == project_id,
        Risk.status != "Closed",
    ).all()
    blockers = []
    for r in risks:
        blockers.append({
            "id": r.id,
            "description": r.description,
            "severity": r.severity,
            "owner": r.owner,
            "status": r.status,
            "mitigation": r.mitigation,
            "days": r.days or 0,
        })
    return blockers


@app.put("/api/projects/{project_id}/blockers/{blocker_id}/resolve")
def resolve_blocker(
    project_id: int,
    blocker_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Resolve a blocker by closing the associated risk."""
    risk = db.query(Risk).filter(
        Risk.id == blocker_id,
        Risk.project_id == project_id,
    ).first()
    if not risk:
        raise HTTPException(status_code=404, detail="Blocker not found")
    risk.status = "Closed"
    risk.updated_at = now_str()
    # Update project blocked info
    remaining = db.query(Risk).filter(
        Risk.project_id == project_id,
        Risk.status != "Closed",
    ).count()
    project = db.query(Project).filter(Project.id == project_id).first()
    if project and remaining == 0:
        project.blocked_at = None
        project.blocked_days = 0
        project.blocked_department = None
        if project.risk_flag == "Critical":
            project.risk_flag = "High"
        elif project.risk_flag == "High":
            project.risk_flag = "None"
    db.commit()
    return {"status": "resolved", "blocker_id": blocker_id, "remaining": remaining}


# ═══════════════════════════════════════════════════════
# Department Capacity
# ═══════════════════════════════════════════════════════

@app.get("/api/departments/capacity")
def get_department_capacity(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get department capacity data - optimized with SQL aggregation."""
    from sqlalchemy import func
    departments = [
        {"id": "PMO", "headcount": 8, "allocated": 7, "icon": "📋", "fullName": "CN NPI / US PMO"},
        {"id": "PD", "headcount": 6, "allocated": 4, "icon": "📐", "fullName": "US Product Design"},
        {"id": "NPI", "headcount": 5, "allocated": 4, "icon": "🔄", "fullName": "NPI Engineering"},
        {"id": "ID", "headcount": 4, "allocated": 2, "icon": "🎨", "fullName": "US Industrial Design"},
        {"id": "EE", "headcount": 7, "allocated": 6, "icon": "⚡", "fullName": "US/CN Electrical Engineering"},
        {"id": "CMF", "headcount": 5, "allocated": 3, "icon": "🖌️", "fullName": "CN Artwork & CMF"},
        {"id": "DQTP", "headcount": 6, "allocated": 5, "icon": "🔬", "fullName": "CN DQTP Lab"},
        {"id": "SC", "headcount": 8, "allocated": 7, "icon": "📦", "fullName": "CN Supply Chain"},
        {"id": "Quality", "headcount": 4, "allocated": 2, "icon": "✅", "fullName": "CN/US Quality Assurance"},
        {"id": "Compliance", "headcount": 3, "allocated": 2, "icon": "📋", "fullName": "CN Compliance"},
        {"id": "MFG", "headcount": 6, "allocated": 4, "icon": "🏭", "fullName": "Factory Manufacturing"},
        {"id": "Marketing", "headcount": 4, "allocated": 1, "icon": "📢", "fullName": "US Creative / UK Marketing"},
    ]
    # Use SQL aggregation instead of loading all projects
    dept_counts = dict(db.query(Project.department, func.count(Project.id)).group_by(Project.department).all())
    dept_risk_counts = dict(db.query(Project.department, func.count(Project.id)).filter(Project.risk_flag.in_(['High', 'Critical'])).group_by(Project.department).all())
    dept_delayed_counts = dict(db.query(Project.department, func.count(Project.id)).filter(Project.risk_flag == 'Critical').group_by(Project.department).all())
    
    for dept in departments:
        dept["total_projects"] = dept_counts.get(dept["id"], 0)
        dept["at_risk_projects"] = dept_risk_counts.get(dept["id"], 0)
        dept["delayed_projects"] = dept_delayed_counts.get(dept["id"], 0)
        pct = (dept["allocated"] / dept["headcount"] * 100) if dept["headcount"] > 0 else 0
        dept["percentage"] = round(pct, 1)
        dept["status"] = "overloaded" if pct >= 85 else ("high" if pct >= 70 else "normal")
    return departments


# ═══════════════════════════════════════════════════════
# Data Persistence: Backup & Restore
# ═══════════════════════════════════════════════════════

@app.post("/api/admin/reseed")
def reseed_database(db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Force re-seed the database. Admin only."""
    from seed import seed
    seed(force=True)
    return {"status": "ok", "message": "Database re-seeded"}


# ═══════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════
# AI Chat History - Co-creation Persistence
# ═══════════════════════════════════════════════════════
import json as _json

AI_CHAT_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai_chat_history.json")

@app.post("/api/ai-chat/message")
def save_ai_chat_message(req: dict):
    """Save a single AI chat message. Body: {user, level, type, content, session_id}"""
    messages = []
    if os.path.exists(AI_CHAT_FILE):
        try:
            with open(AI_CHAT_FILE, "r", encoding="utf-8") as f:
                messages = _json.load(f)
        except:
            messages = []
    
    entry = {
        "id": len(messages) + 1,
        "user": req.get("user", "Anonymous"),
        "level": req.get("level", "L1"),
        "type": req.get("type", "user"),  # 'user' or 'ai'
        "content": req.get("content", ""),
        "session_id": req.get("session_id", "default"),
        "created_at": now_str()
    }
    messages.append(entry)
    
    with open(AI_CHAT_FILE, "w", encoding="utf-8") as f:
        _json.dump(messages, f, ensure_ascii=False, indent=2)
    
    return {"status": "ok", "id": entry["id"]}

@app.get("/api/ai-chat/history")
def get_ai_chat_history(session_id: str = "default", limit: int = 50):
    """Get AI chat history for a session."""
    messages = []
    if os.path.exists(AI_CHAT_FILE):
        try:
            with open(AI_CHAT_FILE, "r", encoding="utf-8") as f:
                messages = _json.load(f)
        except:
            messages = []
    
    if session_id != "all":
        messages = [m for m in messages if m.get("session_id") == session_id]
    
    # Return last N messages
    return messages[-limit:]

@app.get("/api/ai-chat/sessions")
def get_ai_chat_sessions():
    """List all chat sessions with last message preview."""
    messages = []
    if os.path.exists(AI_CHAT_FILE):
        try:
            with open(AI_CHAT_FILE, "r", encoding="utf-8") as f:
                messages = _json.load(f)
        except:
            messages = []
    
    # Group by session_id
    sessions = {}
    for m in messages:
        sid = m.get("session_id", "default")
        if sid not in sessions:
            sessions[sid] = {"session_id": sid, "count": 0, "last_message": "", "last_time": "", "user": ""}
        sessions[sid]["count"] += 1
        sessions[sid]["last_message"] = m.get("content", "")[:80]
        sessions[sid]["last_time"] = m.get("created_at", "")
        sessions[sid]["user"] = m.get("user", "")
    
    return sorted(sessions.values(), key=lambda x: x.get("last_time", ""), reverse=True)

@app.post("/api/ai-chat/feedback")
def ai_chat_to_feedback(req: dict):
    """Convert an AI chat conversation to a feedback entry for co-creation."""
    from feedback_persist import append_feedback
    
    session_id = req.get("session_id", "default")
    messages = []
    if os.path.exists(AI_CHAT_FILE):
        try:
            with open(AI_CHAT_FILE, "r", encoding="utf-8") as f:
                messages = _json.load(f)
        except:
            messages = []
    
    session_msgs = [m for m in messages if m.get("session_id") == session_id]
    if not session_msgs:
        raise HTTPException(status_code=404, detail="No messages found for this session")
    
    # Build feedback content from conversation
    conv_text = " | ".join([f"{m.get('type','user')}: {m.get('content','')[:60]}" for m in session_msgs[-6:]])
    
    entry = {
        "name": req.get("user", "Anonymous"),
        "role": req.get("role", ""),
        "category": req.get("category", "suggestion"),
        "content": f"[AI Chat] {conv_text}",
        "created_at": now_str()
    }
    append_feedback(entry)
    
    return {"status": "ok", "message": "Feedback created from AI chat"}





# ═══════════════════════════════════════════════════════
# Quick Field Update (inline editing)
# ═══════════════════════════════════════════════════════
@app.patch("/api/projects/{project_id}/field")
def update_project_field(project_id: int, data: dict, db: Session = Depends(get_db)):
    """Update a single field on a project — for inline editing."""
    proj = db.query(Project).filter(Project.id == project_id).first()
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    
    field = data.get("field")
    value = data.get("value")
    
    # Whitelist of editable fields
    EDITABLE_FIELDS = {
        "name", "category", "status", "phase", "owner", "brand", "factory",
        "start_date", "end_date", "progress", "risk_flag", "risk_note",
        "source_system", "department", "blocked_at", "blocked_days",
        "blocked_department", "priority", "notes"
    }
    
    if field not in EDITABLE_FIELDS:
        raise HTTPException(status_code=400, detail=f"Field '{field}' is not editable")
    
    # Type conversion
    if field == "progress":
        value = float(value) if value is not None else 0.0
    elif field == "blocked_days":
        value = int(value) if value is not None else 0
    
    # If setting blocked_at to today, also set blocked_department if provided
    if field == "blocked_at" and value:
        proj.blocked_at = value
        if "blocked_department" in data:
            proj.blocked_department = data["blocked_department"]
        proj.updated_at = now_str()
        db.commit()
        db.refresh(proj)
        return proj
    
    # If clearing blocked status
    if field == "blocked_at" and not value:
        proj.blocked_at = None
        proj.blocked_days = 0
        proj.blocked_department = None
        proj.updated_at = now_str()
        db.commit()
        db.refresh(proj)
        return proj
    
    setattr(proj, field, value)
    proj.updated_at = now_str()
    db.commit()
    db.refresh(proj)
    return proj


@app.patch("/api/milestones/{milestone_id}/field")


@app.post("/api/admin/batch-milestones")
def batch_create_milestones(data: dict, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    """Batch create milestones. Body: {"milestones": [{project_id, name, phase, due_date, status, owner}, ...]}"""
    milestones_data = data.get("milestones", [])
    created = 0
    now = now_str()
    for m in milestones_data:
        ms = Milestone(
            project_id=m["project_id"],
            name=m["name"],
            phase=m.get("phase", "Unphased"),
            due_date=m.get("due_date", ""),
            status=m.get("status", "Not Started"),
            owner=m.get("owner", ""),
            is_manual=0,
            created_at=now,
            updated_at=now,
        )
        db.add(ms)
        created += 1
    db.commit()
    return {"created": created}
def update_milestone_field(milestone_id: int, data: dict, db: Session = Depends(get_db)):
    """Update a single field on a milestone — for inline editing."""
    ms = db.query(Milestone).filter(Milestone.id == milestone_id).first()
    if not ms:
        raise HTTPException(status_code=404, detail="Milestone not found")
    
    field = data.get("field")
    value = data.get("value")
    
    EDITABLE_FIELDS = {"name", "phase", "due_date", "actual_date", "status", "owner"}
    if field not in EDITABLE_FIELDS:
        raise HTTPException(status_code=400, detail=f"Field '{field}' is not editable")
    
    setattr(ms, field, value)
    ms.updated_at = now_str()
    db.commit()
    db.refresh(ms)
    return ms


# ═══════════════════════════════════════════════════════
# PDF Upload & Smart Import
# ═══════════════════════════════════════════════════════
import re as _re
from pdf_parser import (
    extract_text, parse_project_data, 
    get_upload_history, save_upload_history,
    UPLOAD_DIR
)

@app.post("/api/upload/document")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF/DOCX file and auto-parse project data."""
    import shutil as _shutil
    
    # Validate file type
    allowed_ext = {'.pdf', '.docx', '.doc', '.txt', '.md', '.csv'}
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext not in allowed_ext:
        raise HTTPException(status_code=400, detail=f"Unsupported file type: {ext}. Allowed: {', '.join(allowed_ext)}")
    
    # Save file
    safe_name = _re.sub(r'[^a-zA-Z0-9._-]', '_', file.filename or "upload")
    file_path = os.path.join(UPLOAD_DIR, safe_name)
    
    # Avoid overwrite
    if os.path.exists(file_path):
        base, ext2 = os.path.splitext(safe_name)
        file_path = os.path.join(UPLOAD_DIR, f"{base}_{int(datetime.now().timestamp())}{ext2}")
    
    with open(file_path, "wb") as buffer:
        _shutil.copyfileobj(file.file, buffer)
    
    # Parse the document
    text = extract_text(file_path)
    result = parse_project_data(text, file.filename or "unknown")
    
    # Save upload history
    save_upload_history({
        "filename": file.filename,
        "saved_path": file_path,
        "uploaded_at": now_str(),
        "projects_found": len(result["projects"]),
        "risks_found": len(result["summary"].get("risks_found", [])),
        "imported": False
    })
    
    return {
        "status": "ok",
        "filename": file.filename,
        "text_length": len(text),
        "projects_found": len(result["projects"]),
        "summary": result["summary"],
        "projects": result["projects"],
        "preview": result["raw_text"][:2000]
    }


@app.post("/api/upload/import")
def import_parsed_projects(data: dict, db: Session = Depends(get_db)):
    """Import the parsed projects from an uploaded document into the database."""
    from models import Project, Milestone, Risk
    projects = data.get("projects", [])
    if not projects:
        raise HTTPException(status_code=400, detail="No projects to import")
    
    imported = []
    for proj_data in projects:
        # Remove internal keys (don't mutate original)
        clean_proj = dict(proj_data)
        milestones_data = clean_proj.pop("_milestones", [])
        risks_data = clean_proj.pop("_risks", [])
        source_file = clean_proj.pop("source_file", "")
        
        # Check if project already exists
        existing = db.query(Project).filter(Project.name == clean_proj.get("name")).first()
        if existing:
            # Update existing project
            for key, value in clean_proj.items():
                if value and key in Project.__table__.columns.keys():
                    setattr(existing, key, value)
            existing.updated_at = now_str()
            project_id = existing.id
        else:
            # Create new project
            clean_proj.setdefault("status", "In Progress")
            proj_data.setdefault("risk_flag", "None")
            proj_data.setdefault("source_system", f"PDF Upload ({source_file})")
            clean_proj["created_at"] = now_str()
            clean_proj["updated_at"] = now_str()
            # Only keep valid columns
            valid_keys = Project.__table__.columns.keys()
            clean_data = {k: v for k, v in clean_proj.items() if k in valid_keys}
            new_proj = Project(**clean_data)
            db.add(new_proj)
            db.flush()
            project_id = new_proj.id
        
        # Add milestones
        for ms_name in milestones_data:
            ms = Milestone(
                project_id=project_id,
                name=ms_name[:200],
                status="Not Started",
                created_at=now_str(),
                updated_at=now_str()
            )
            db.add(ms)
        
        # Add risks
        for risk_desc in risks_data:
            risk = Risk(
                project_id=project_id,
                description=risk_desc[:500],
                severity="Medium",
                status="Open",
                created_at=now_str(),
                updated_at=now_str()
            )
            db.add(risk)
        
        imported.append({"name": clean_proj.get("name"), "id": project_id})
    
    db.commit()
    
    return {
        "status": "ok",
        "imported_count": len(imported),
        "projects": imported
    }


@app.get("/api/upload/history")
def list_uploads():
    """List upload history."""
    return get_upload_history()

# ═══════════════════════════════════════════════════════
# Serve Frontend (must be last - catch-all)
# ═══════════════════════════════════════════════════════

# Mount frontend static files at root
import os
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")