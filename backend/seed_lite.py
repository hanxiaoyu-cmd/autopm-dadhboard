"""Seed the database with 5 demo projects — lean version for daily use."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from database import engine, SessionLocal, Base
from models import Project, Milestone, Risk, User, Alert, Feedback, UserProject
from auth import hash_password
from alerts_engine import refresh_alerts

def now_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def seed():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear all data
    for tbl in [Alert, Risk, Milestone, UserProject, Feedback, User, Project]:
        db.query(tbl).delete()
    db.commit()

    # ── Admin User ──
    admin = User(username="sunny", password_hash=hash_password("autopm2026"), role="admin", created_at=now_str())
    db.add(admin)

    # ── 5 Projects ──
    projects = [
        Project(
            name="XT-500", category="NPD CAT A", status="In Progress", phase="EB1",
            owner="Li Ming", brand="Ninja", factory="Factory Alpha",
            start_date="2026-01-15", end_date="2026-09-30",
            progress=48, risk_flag="High", risk_note="PCB layout delay — waiting on EE approval",
            source_system="Manual", department="EE", priority="P1",
            blocked_at="2026-05-10", blocked_days=12, blocked_department="EE",
            notes="Q3 launch target, key account customer",
            created_at=now_str(), updated_at=now_str()
        ),
        Project(
            name="RV-900", category="Extension", status="In Progress", phase="DQTP",
            owner="Zhang Wei", brand="Shark", factory="Factory Beta",
            start_date="2025-11-01", end_date="2026-07-15",
            progress=65, risk_flag="Medium", risk_note="Supplier component shortage for motor assembly",
            source_system="Manual", department="SC", priority="P2",
            blocked_at=None, blocked_days=0, blocked_department=None,
            notes="Extension of RV-800 platform, same tooling",
            created_at=now_str(), updated_at=now_str()
        ),
        Project(
            name="AF-400", category="NPD CAT B", status="On Hold", phase="Concept",
            owner="Wang Fang", brand="Ninja", factory="Factory Gamma",
            start_date="2026-03-01", end_date="2027-01-31",
            progress=12, risk_flag="Critical", risk_note="Budget cut review — project may be cancelled",
            source_system="Manual", department="PMO", priority="P0",
            blocked_at="2026-04-20", blocked_days=32, blocked_department="PMO",
            notes="Pending executive decision on market sizing",
            created_at=now_str(), updated_at=now_str()
        ),
        Project(
            name="CM-200", category="New CMF", status="In Progress", phase="Compliance",
            owner="Chen Jie", brand="Shark", factory="Factory Delta",
            start_date="2025-09-15", end_date="2026-06-30",
            progress=78, risk_flag="Low", risk_note="UL certification expected by end of May",
            source_system="Manual", department="DQTP", priority="P3",
            blocked_at=None, blocked_days=0, blocked_department=None,
            notes="Color refresh for holiday season",
            created_at=now_str(), updated_at=now_str()
        ),
        Project(
            name="BK-350", category="Legacy/Dual Source", status="Completed", phase="MP",
            owner="Liu Yang", brand="Ninja", factory="Factory Alpha",
            start_date="2025-06-01", end_date="2026-04-15",
            progress=100, risk_flag="None", risk_note=None,
            source_system="Manual", department="MFG", priority="P2",
            blocked_at=None, blocked_days=0, blocked_department=None,
            notes="Dual source qualified, mass production stable",
            created_at=now_str(), updated_at=now_str()
        ),
    ]

    for p in projects:
        db.add(p)
    db.flush()

    # ── Milestones for each project ──
    milestone_defs = {
        "XT-500": [
            ("Kick Off Complete", "Kick Off", "2026-01-15", "2026-01-15", "Completed", "Li Ming"),
            ("Concept Approval", "Concept", "2026-02-28", "2026-03-05", "Completed", "Wang Fang"),
            ("Design Freeze", "Design", "2026-04-15", "2026-04-18", "Completed", "Zhang Wei"),
            ("EB0 Review", "EB0", "2026-05-01", "2026-05-03", "Completed", "Li Ming"),
            ("EB1 Review", "EB1", "2026-06-15", None, "In Progress", "Li Ming"),
            ("DQTP Start", "DQTP", "2026-07-01", None, "Not Started", "Chen Jie"),
            ("MP", "MP", "2026-09-15", None, "Not Started", "Liu Yang"),
        ],
        "RV-900": [
            ("Kick Off", "Kick Off", "2025-11-01", "2025-11-01", "Completed", "Zhang Wei"),
            ("EB0 Review", "EB0", "2026-01-15", "2026-01-14", "Completed", "Zhang Wei"),
            ("EB1 Review", "EB1", "2026-03-01", "2026-03-03", "Completed", "Zhang Wei"),
            ("DQTP Testing", "DQTP", "2026-04-15", None, "In Progress", "Chen Jie"),
            ("Compliance Cert", "Compliance", "2026-06-01", None, "Not Started", "Liu Yang"),
            ("MP", "MP", "2026-07-01", None, "Not Started", "Zhang Wei"),
        ],
        "AF-400": [
            ("Kick Off", "Kick Off", "2026-03-01", "2026-03-01", "Completed", "Wang Fang"),
            ("Concept Review", "Concept", "2026-04-30", None, "On Hold", "Wang Fang"),
            ("Design Start", "Design", "2026-06-01", None, "Not Started", "TBD"),
        ],
        "CM-200": [
            ("Kick Off", "Kick Off", "2025-09-15", "2025-09-15", "Completed", "Chen Jie"),
            ("EB1 Approval", "EB1", "2025-12-20", "2025-12-18", "Completed", "Chen Jie"),
            ("DQTP Complete", "DQTP", "2026-03-15", "2026-03-20", "Completed", "Chen Jie"),
            ("UL Certification", "Compliance", "2026-05-31", None, "In Progress", "Liu Yang"),
            ("MP", "MP", "2026-06-15", None, "Not Started", "Chen Jie"),
        ],
        "BK-350": [
            ("Kick Off", "Kick Off", "2025-06-01", "2025-06-01", "Completed", "Liu Yang"),
            ("EB1 Approval", "EB1", "2025-09-01", "2025-08-28", "Completed", "Liu Yang"),
            ("DQTP", "DQTP", "2025-12-01", "2025-11-25", "Completed", "Chen Jie"),
            ("MP Achieved", "MP", "2026-03-01", "2026-02-28", "Completed", "Liu Yang"),
        ],
    }

    for proj in projects:
        if proj.name in milestone_defs:
            for ms in milestone_defs[proj.name]:
                db.add(Milestone(
                    project_id=proj.id, name=ms[0], phase=ms[1],
                    due_date=ms[2], actual_date=ms[3], status=ms[4], owner=ms[5],
                    created_at=now_str(), updated_at=now_str()
                ))

    # ── Risks ──
    risk_defs = {
        "XT-500": [("PCB layout delay — waiting on EE team approval", "High", "Escalate to EE director", "Li Ming")],
        "RV-900": [("Motor assembly supplier shortage", "Medium", "Identify backup supplier", "Zhang Wei")],
        "AF-400": [("Project may be cancelled due to budget review", "Critical", "Prepare ROI analysis for exec team", "Wang Fang")],
        "CM-200": [("UL cert timeline tight", "Low", "Pre-submission review scheduled", "Chen Jie")],
    }
    for proj in projects:
        if proj.name in risk_defs:
            for r in risk_defs[proj.name]:
                db.add(Risk(
                    project_id=proj.id, description=r[0], severity=r[1],
                    mitigation=r[2], owner=r[3], status="Open",
                    created_at=now_str(), updated_at=now_str()
                ))

    db.commit()

    # Refresh alerts
    refresh_alerts(db)

    print(f"Seeded {len(projects)} projects with milestones and risks.")
    db.close()


if __name__ == "__main__":
    seed()
