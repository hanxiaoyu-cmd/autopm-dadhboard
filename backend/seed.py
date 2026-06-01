"""Seed the database with 4 real NPI projects for AutoPM v17.5.6."""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from database import engine, SessionLocal, Base
from models import Project, Milestone, Risk, User, Alert, Feedback, UserProject
from auth import hash_password
from alerts_engine import refresh_alerts

DEPARTMENTS = [
    {'id': 'PMO', 'headcount': 8, 'allocated': 7, 'fullName': 'CN NPI / US PMO'},
    {'id': 'PD', 'headcount': 6, 'allocated': 4, 'fullName': 'US Product Design'},
    {'id': 'NPI', 'headcount': 5, 'allocated': 4, 'fullName': 'NPI Engineering'},
    {'id': 'ID', 'headcount': 4, 'allocated': 2, 'fullName': 'US Industrial Design'},
    {'id': 'EE', 'headcount': 7, 'allocated': 6, 'fullName': 'US/CN Electrical Engineering'},
    {'id': 'CMF', 'headcount': 5, 'allocated': 3, 'fullName': 'CN Artwork & CMF'},
    {'id': 'DQTP', 'headcount': 6, 'allocated': 5, 'fullName': 'CN DQTP Lab'},
    {'id': 'SC', 'headcount': 8, 'allocated': 7, 'fullName': 'CN Supply Chain'},
    {'id': 'Quality', 'headcount': 4, 'allocated': 2, 'fullName': 'CN/US Quality Assurance'},
    {'id': 'Compliance', 'headcount': 3, 'allocated': 2, 'fullName': 'CN Compliance'},
    {'id': 'MFG', 'headcount': 6, 'allocated': 4, 'fullName': 'Factory Manufacturing'},
    {'id': 'Marketing', 'headcount': 4, 'allocated': 1, 'fullName': 'US Creative / UK Marketing'},
]


def seed(force=False):
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if not force and db.query(User).filter(User.username == "sunny").first():
            print("Database already seeded. Skipping.")
            return

        if force:
            print("Force re-seed: clearing existing data...")
            db.query(Alert).delete()
            db.query(Risk).delete()
            db.query(Milestone).delete()
            db.query(UserProject).delete()
            db.query(Project).delete()
            db.query(User).delete()
            db.commit()
            print("Cleared all tables.")

        now = datetime.utcnow()
        now_str = now.strftime("%Y-%m-%d %H:%M:%S")

        # -- Admin users --
        sunny = db.query(User).filter(User.username == "sunny").first()
        if not sunny:
            sunny = User(
                username="sunny", email="sunny@autopm.local",
                password_hash=hash_password("autopm2026"), role="admin", created_at=now_str,
            )
            db.add(sunny)
            db.flush()
        print(f"User sunny id={sunny.id}")

        # -- 4 Real Projects --
        projects_data = [
            {
                "name": "Project-S", "category": "NPD CAT A", "status": "In Progress",
                "phase": "EB0", "owner": "CN NPI", "brand": "Shark",
                "factory": "Factory Alpha", "start_date": "2026-03-03",
                "end_date": "2026-06-26", "progress": 52.0,
                "risk_flag": "None", "source_system": "Manual",
                "department": "PMO", "priority": "P1",
            },
            {
                "name": "Project-B", "category": "NPD CAT A", "status": "In Progress",
                "phase": "EB1", "owner": "CN NPI", "brand": "Shark",
                "factory": "Factory Alpha", "start_date": "2025-12-15",
                "end_date": "2026-06-26", "progress": 61.0,
                "risk_flag": "None", "source_system": "Manual",
                "department": "PMO", "priority": "P1",
            },
            {
                "name": "Project-A8", "category": "NPD CAT A", "status": "In Progress",
                "phase": "EB1", "owner": "CN NPI", "brand": "Shark",
                "factory": "Factory Alpha", "start_date": "2026-03-23",
                "end_date": "2026-06-17", "progress": 5.0,
                "risk_flag": "None", "source_system": "Manual",
                "department": "PMO", "priority": "P2",
            },
            {
                "name": "Project-A1", "category": "NPD CAT A", "status": "In Progress",
                "phase": "EB1", "owner": "CN NPI", "brand": "Ninja",
                "factory": "Factory Beta", "start_date": "2026-03-18",
                "end_date": "2026-09-19", "progress": 9.0,
                "risk_flag": "None", "source_system": "Manual",
                "department": "PMO", "priority": "P2",
            },
        ]

        created_projects = []
        for pd in projects_data:
            p = Project(
                name=pd['name'], category=pd['category'], status=pd['status'],
                phase=pd['phase'], owner=pd['owner'], brand=pd['brand'],
                factory=pd['factory'], start_date=pd['start_date'],
                end_date=pd['end_date'], progress=pd['progress'],
                risk_flag=pd['risk_flag'], source_system=pd['source_system'],
                department=pd['department'], priority=pd['priority'],
                blocked_at='None', blocked_days=0, notes='',
                created_at=now_str, updated_at=now_str,
            )
            db.add(p)
            db.flush()
            created_projects.append(p)
            print(f"  Created: {pd['name']} id={p.id}")

        db.commit()

        # -- Milestones for each project --
        milestones_data = {
            "Project-S": [
                ("Kick Off", "Kick Off", "2026-03-03", "Done", "CN NPI,US PMO"),
                ("Received PIS for EB1", "Kick Off", "2026-03-03", "Done", "US PD"),
                ("Received UI Spec for EB1", "Kick Off", "2026-03-06", "Done", "US PD,US ID"),
                ("Received ID Spec EB1", "Kick Off", "2026-03-06", "Done", "US ID,US PD"),
                ("Prepare product change PPT and ECN", "EB0", "2026-03-05", "Done", "Factory"),
                ("Finalize PSD and UI flow", "EB0", "2026-03-05", "Done", "CN NPI"),
                ("Finalize sample plan for EB1", "EB0", "2026-03-19", "Done", "CN NPI,US PMO"),
                ("Provide redline EBOM", "EB0", "2026-03-19", "Done", "Factory,CN NPI"),
                ("Finalize CBOM for EB1", "EB0", "2026-03-30", "Done", "CN SC"),
                ("Approve ECN to DD", "EB0", "2026-04-10", "Done", "CN NPI"),
                ("PMO approve sample plan", "EB0", "2026-04-03", "Not Started", "US PMO"),
                ("Prepare UI mylar sample", "EB0", "2026-04-18", "Done", "Factory"),
                ("Send samples to EE team", "EB0", "2026-03-18", "Done", "CN EE,US EE"),
                ("Finalize UI flow", "EB0", "2026-03-26", "Done", "CN EE"),
                ("Software design", "EB0", "2026-04-08", "Done", "CN EE,US EE"),
                ("Reflash software", "EB0", "2026-04-10", "Done", "Factory"),
                ("Delivery PCBA to factory", "EB0", "2026-03-29", "Done", "Factory"),
                ("Performance test", "EB0", "2026-04-14", "Done", "Factory"),
                ("NTK test", "EB0", "2026-05-08", "Not Started", "CN Testing"),
                ("Send color chip to factory", "EB0", "2026-03-12", "Done", "US ID,Factory"),
                ("Develop color 1st time", "EB0", "2026-03-21", "Done", "Factory"),
                ("Develop 2nd color chips", "EB0", "2026-03-31", "Done", "Factory"),
                ("CN-CMF review 2nd color", "EB0", "2026-04-02", "Done", "CN Artwork"),
                ("Approve color chips", "EB0", "2026-04-02", "Done", "US ID"),
                ("Upload artwork for EB1", "EB0", "2026-03-25", "Done", "CN Artwork"),
                ("Prepare EB1 materials", "EB0", "2026-04-15", "Done", "Factory"),
                ("EB1 assembly", "EB0", "2026-04-18", "Done", "Factory"),
                ("Verify temperature and KPI", "EB0", "2026-04-24", "Done", "Factory"),
                ("Ship samples to US/UK", "EB0", "2026-05-03", "Done", "CN NPI"),
                ("Provide feedback of EB1", "EB0", "2026-05-08", "Done", "US PD,US Quality"),
                ("Life test", "EB0", "2026-05-28", "Not Started", "CN DQTP"),
                ("Release DQTP report", "EB0", "2026-05-29", "Not Started", "CN Testing"),
                ("Run KPI checkout", "EB0", "2026-05-22", "Not Started", "CN Testing"),
                ("Arrange B/W testing", "EB0", "2026-05-22", "Not Started", "CN EE"),
                ("Arrange UI flow check", "EB0", "2026-05-18", "Not Started", "CN EE"),
                ("Conduct Compliance test", "EB0", "2026-06-05", "Not Started", "CN Compliance"),
                ("Update compliance report", "EB0", "2026-06-08", "Not Started", "CN Compliance"),
                ("Release LOA/PO for LLT material", "MP Prep", "2026-04-28", "Done", "CN SC"),
                ("Update ID & UI spec for MP", "MP Prep", "2026-05-26", "Not Started", "US ID"),
                ("Upload artwork for MP", "MP Prep", "2026-05-29", "Not Started", "CN Artwork"),
                ("Update EBOM for MP", "MP Prep", "2026-06-03", "Not Started", "Factory"),
                ("Update CBOM for MP", "MP Prep", "2026-06-10", "Not Started", "CN SC"),
                ("Release ECN to factory", "MP Prep", "2026-06-17", "Not Started", "CN NPI"),
                ("Initiate MP Work Flow in PLM", "MP Prep", "2026-06-24", "Not Started", "CN NPI"),
                ("Prepare MP materials", "MP Prep", "2026-06-24", "Not Started", "Factory"),
                ("Sign golden samples for MP", "MP Prep", "2026-06-25", "Not Started", "CN NPI"),
            ],
            "Project-B": [
                ("Kick Off", "Kick Off", "2025-12-15", "Done", "CN NPI,US PMO"),
                ("Finalize PIS for EB0", "Kick Off", "2025-12-16", "Done", "US PD"),
                ("Finalize UI Spec for EB0", "Kick Off", "2025-12-16", "Done", "US PD,US ID"),
                ("Finalize ID Spec EB0", "Kick Off", "2025-12-16", "Done", "US ID,US PD"),
                ("Prepare product change PPT and ECN", "Prototype", "2025-12-17", "Done", "Factory"),
                ("DQTP & compliance Comment", "Prototype", "2025-12-19", "Done", "CN Compliance"),
                ("MIFA supplier selection", "Prototype", "2025-12-22", "Done", "CN SC"),
                ("PCBA hardware development", "Prototype", "2026-02-16", "Done", "CN EE"),
                ("Software development", "Prototype", "2026-02-19", "Done", "CN EE,US EE"),
                ("Approve ECN to DD", "Prototype", "2025-12-29", "Done", "CN NPI"),
                ("PMO approve sample plan", "Prototype", "2026-01-02", "Done", "US PMO"),
                ("Color development", "Prototype", "2026-01-17", "Done", "US ID,Factory"),
                ("P1 assembly", "Prototype", "2026-02-03", "Done", "Factory"),
                ("Verify temperature and KPI for P1", "Prototype", "2026-02-05", "Done", "Factory"),
                ("Ship P1 samples to US/UK", "Prototype", "2026-02-12", "Done", "CN NPI"),
                ("Provide feedback of P1 samples", "Prototype", "2026-02-19", "Done", "US PD,US Quality"),
                ("Finalize PSD and UI flow for EB0", "EB0", "2026-02-24", "Done", "CN NPI"),
                ("Update redline EBOM for EB0", "EB0", "2026-02-24", "Done", "Factory"),
                ("Finalize CBOM for EB0", "EB0", "2026-03-04", "Done", "CN SC"),
                ("Approve ECN to DD for EB0", "EB0", "2026-03-09", "Done", "CN NPI"),
                ("Finalize sample plan for EB1", "EB1", "2026-03-11", "Done", "CN NPI,US PMO"),
                ("Update redline EBOM for EB1", "EB1", "2026-03-12", "Done", "Factory"),
                ("Finalize CBOM for EB1", "EB1", "2026-03-20", "Done", "CN SC"),
                ("PCBA development for EB1", "EB1", "2026-04-14", "In Progress", "CN EE,US EE"),
                ("Prepare common parts for EB1", "EB1", "2026-04-14", "In Progress", "Factory"),
                ("EB1 assembly", "EB1", "2026-04-16", "Not Started", "Factory"),
                ("Verify temperature and KPI for EB1", "EB1", "2026-04-18", "Not Started", "Factory"),
                ("Ship EB1 samples to US/UK", "EB1", "2026-04-25", "Not Started", "CN NPI"),
                ("Life test", "EB1", "2026-05-19", "Not Started", "CN DQTP"),
                ("Release DQTP report", "EB1", "2026-05-20", "Not Started", "CN Testing"),
                ("Conduct Compliance test", "EB1", "2026-05-19", "Not Started", "CN Compliance"),
                ("Release LOA/PO for LLT material", "MP Prep", "2026-04-17", "Done", "CN SC"),
                ("Update ID & UI spec for MP", "MP Prep", "2026-05-22", "Not Started", "US ID"),
                ("Upload artwork for MP", "MP Prep", "2026-05-27", "Not Started", "CN Artwork"),
                ("Update EBOM for MP", "MP Prep", "2026-05-30", "Not Started", "Factory"),
                ("Update CBOM for MP", "MP Prep", "2026-06-05", "Not Started", "CN SC"),
                ("Release ECN to factory", "MP Prep", "2026-06-09", "Not Started", "CN NPI"),
                ("Initiate MP Work Flow in PLM", "MP Prep", "2026-06-16", "Not Started", "CN NPI"),
                ("Prepare MP materials", "MP Prep", "2026-06-16", "Not Started", "Factory"),
                ("Sign golden samples for MP", "MP Prep", "2026-06-17", "Not Started", "CN NPI"),
                ("Start MP", "MP", "2026-06-26", "Not Started", "CN NPI"),
            ],
            "Project-A8": [
                ("Kick Off", "Kick Off", "2026-03-23", "Done", "CN NPI,US PMO"),
                ("Finalize PIS for EB0", "Kick Off", "2026-03-27", "Done", "US PD"),
                ("Finalize ID Spec EB0", "Kick Off", "2026-03-27", "Done", "US ID,US PD"),
                ("Finalize UI Spec for EB0", "Kick Off", "2026-03-27", "Not Started", "US PD,US ID"),
                ("Prepare product change PPT and ECN", "EB1", "2026-03-30", "Done", "Factory"),
                ("Create ECN", "EB1", "2026-03-31", "Done", "CN NPI"),
                ("Prepare ECN DD documents", "EB1", "2026-04-07", "Not Started", "CN Compliance,CN NPI"),
                ("Finalize CBOM for EB0", "EB1", "2026-04-14", "Not Started", "CN SC"),
                ("Finalize sample plan for EB0", "EB1", "2026-04-10", "Not Started", "CN NPI,US PMO"),
                ("Sign off ECN to DD approved", "EB1", "2026-04-10", "Not Started", "CN NPI"),
                ("PMO approve sample plan", "EB1", "2026-04-16", "Not Started", "US PMO"),
                ("Prepare common parts for EB1", "EB1", "2026-05-02", "Not Started", "Factory"),
                ("Finish pulp tray CAD", "EB1", "2026-04-03", "Not Started", "CN Packaging"),
                ("Make pulp tray prototype", "EB1", "2026-04-09", "Not Started", "Factory"),
                ("Approve tool cost and release EPS tooling", "EB1", "2026-04-10", "Not Started", "CN Tooling,US PMO"),
                ("Fabricate pulp tray tooling", "EB1", "2026-04-30", "Not Started", "Factory"),
                ("EB1 assembly", "EB1", "2026-05-05", "Not Started", "Factory"),
                ("Verify temperature and KPI for EB1", "EB1", "2026-05-07", "Not Started", "Factory"),
                ("Ship EB1 samples to US/UK", "EB1", "2026-05-16", "Not Started", "CN NPI"),
                ("Life test", "EB1", "2026-06-05", "Not Started", "CN DQTP"),
                ("Release DQTP report", "EB1", "2026-06-08", "Not Started", "CN Testing"),
                ("Conduct Compliance test", "EB1", "2026-06-05", "Not Started", "CN Compliance"),
                ("Release LOA/PO for LLT material", "MP Prep", "2026-05-06", "Not Started", "CN SC"),
                ("Update ID & UI spec for MP", "MP Prep", "2026-06-02", "Not Started", "US ID"),
                ("Upload artwork for MP", "MP Prep", "2026-06-05", "Not Started", "CN Artwork"),
                ("Update EBOM for MP", "MP Prep", "2026-06-03", "Not Started", "Factory"),
                ("Update CBOM for MP", "MP Prep", "2026-06-09", "Not Started", "CN SC"),
                ("Release ECN to factory", "MP Prep", "2026-06-10", "Not Started", "CN NPI"),
                ("Initiate MP Work Flow in PLM", "MP Prep", "2026-06-17", "Not Started", "CN NPI"),
                ("Prepare MP materials", "MP Prep", "2026-06-17", "Not Started", "Factory"),
                ("Sign golden samples for MP", "MP Prep", "2026-06-17", "Not Started", "CN NPI"),
            ],
            "Project-A1": [
                ("Kick Off", "Kick Off", "2026-03-18", "Done", "US PMO"),
                ("Provide PIS", "Kick Off", "2026-03-19", "Done", "US PD"),
                ("Finalize ID Spec for EB1", "Kick Off", "2026-03-20", "Done", "US ID,US PD"),
                ("Finalize UI Spec for EB1", "Kick Off", "2026-03-20", "Done", "US Creative"),
                ("Prepare product change PPT and ECN", "EB1", "2026-03-24", "Done", "Factory"),
                ("Prepare heating element samples 220V/2000W", "EB1", "2026-04-01", "Done", "Factory"),
                ("Prepare motor samples 220V/60HZ", "EB1", "2026-04-01", "Done", "Factory"),
                ("EE Change PPT", "EB1", "2026-03-30", "Done", "CN EE"),
                ("P1 prototype Build", "EB1", "2026-04-06", "Done", "Factory"),
                ("Finalize sample plan for EB1", "EB1", "2026-04-07", "Done", "US PMO"),
                ("Update redline EBOM for EB1", "EB1", "2026-04-02", "Done", "Factory"),
                ("Finalize CBOM for EB1", "EB1", "2026-04-08", "Done", "CN SC"),
                ("Release Artwork for EB1", "EB1", "2026-04-28", "Not Started", "US Creative"),
                ("PMO approve sample plan", "EB1", "2026-04-13", "Not Started", "US PMO"),
                ("Approve ECN to DD", "EB1", "2026-04-21", "Not Started", "CN NPI"),
                ("Prepare materials for EB1", "EB1", "2026-04-22", "Not Started", "Factory"),
                ("Software development", "EB1", "2026-05-10", "Not Started", "CN EE"),
                ("Verify EMC test", "EB1", "2026-04-21", "Not Started", "Factory"),
                ("Update software for Korean", "EB1", "2026-04-28", "Not Started", "CN EE"),
                ("Prepare PCBA for EB1", "EB1", "2026-05-10", "Not Started", "Factory"),
                ("EB1 assembly", "EB1", "2026-05-12", "Not Started", "Factory"),
                ("Verify temperature and KPI for EB1", "EB1", "2026-05-14", "Not Started", "Factory"),
                ("Conduct PSI + Calibration", "EB1", "2026-05-16", "Not Started", "Factory"),
                ("Life test", "EB1", "2026-06-16", "Not Started", "CN DQTP"),
                ("Release DQTP report", "EB1", "2026-06-17", "Not Started", "CN Testing"),
                ("NTK test", "EB1", "2026-06-16", "Not Started", "CN Testing"),
                ("Conduct Compliance test", "EB1", "2026-06-16", "Not Started", "CN Compliance"),
                ("Release LOA/PO for LLT material", "MP Prep", "2026-05-17", "Not Started", "CN SC"),
                ("Update ID & UI spec for MP", "MP Prep", "2026-06-29", "Not Started", "US ID"),
                ("Upload artwork for MP", "MP Prep", "2026-07-03", "Not Started", "CN Artwork"),
                ("Update EBOM for MP", "MP Prep", "2026-07-03", "Not Started", "Factory"),
                ("Update CBOM for MP", "MP Prep", "2026-07-09", "Not Started", "CN SC"),
                ("Release ECN to factory", "MP Prep", "2026-07-10", "Not Started", "CN NPI"),
                ("Initiate MP Work Flow in PLM", "MP Prep", "2026-07-17", "Not Started", "CN NPI"),
                ("Prepare MP materials", "MP Prep", "2026-07-17", "Not Started", "Factory"),
                ("Sign golden samples for MP", "MP Prep", "2026-09-18", "Not Started", "CN NPI"),
                ("Start MP", "MP", "2026-09-19", "Not Started", "CN NPI"),
            ],
        }

        total_ms = 0
        for proj in created_projects:
            ms_list = milestones_data.get(proj.name, [])
            for name, phase, due, status, owner in ms_list:
                m = Milestone(
                    project_id=proj.id, name=name, phase=phase,
                    due_date=due, actual_date=due if status == "Done" else None,
                    status=status, owner=owner,
                    is_manual=0, created_at=now_str, updated_at=now_str,
                )
                db.add(m)
                total_ms += 1
            print(f"  {proj.name}: {len(ms_list)} milestones")

        db.commit()
        print(f"Total milestones: {total_ms}")

        # -- Subscribe sunny to all 4 projects --
        for proj in created_projects:
            up = UserProject(user_id=sunny.id, project_id=proj.id, created_at=now_str)
            db.add(up)
        db.commit()
        print(f"Subscribed sunny to {len(created_projects)} projects")

        # -- Verification --
        total = db.query(Project).count()
        print(f"Seed complete: {total} projects")

        # -- Generate alerts --
        count = refresh_alerts(db)
        print(f"Generated {count} alerts.")

    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed(force=True)
