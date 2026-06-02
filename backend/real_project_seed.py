from datetime import datetime, timedelta

from models import Project, Milestone, UserProject


REAL_PROJECT_PLANS = [
    {
        "legacy_names": ["Project-B"],
        "name": "BW1001EUUK",
        "category": "NPD CAT A",
        "status": "In Progress",
        "phase": "EB0",
        "owner": "CN NPI",
        "brand": "SharkNinja",
        "factory": "Factory Alpha",
        "start_date": "2026-01-05",
        "end_date": "2026-07-05",
        "progress": 61.0,
        "risk_flag": "High",
        "department": "PMO",
        "priority": "P1",
        "notes": "Imported from Project plan/BW1001EUUK.mpp and BW1001EUUK-0518.pdf for real My Project task maintenance.",
        "tasks": [
            ("Kick Off", "Kick Off", "2026-01-05", "Done", "CN NPI,US PMO"),
            ("Kick off ECN and approve ECN to DD", "Kick Off", "2026-01-08", "Done", "CN NPI"),
            ("Finalize PIS for EB0", "EB0", "2026-01-12", "Done", "US PD"),
            ("Finalize ID Spec EB0", "EB0", "2026-01-13", "Done", "US ID,US PD"),
            ("Finalize UI Spec for EB0", "EB0", "2026-01-14", "Done", "US PD,US ID"),
            ("Finalize sample plan for EB0", "EB0", "2026-01-19", "Done", "CN NPI,US PMO"),
            ("Finalize EBOM and factory internal BOM for EB0", "EB0", "2026-01-21", "Done", "Factory"),
            ("Finalize CBOM for EB0", "EB0", "2026-01-24", "Done", "CN SC"),
            ("Prepare PCBA for EB0", "EB0-PCBA", "2026-02-05", "Done", "Factory,CN EE"),
            ("PCBA hardware development", "EB0-PCBA", "2026-02-14", "Done", "CN EE"),
            ("Software development", "EB0-PCBA", "2026-02-19", "Done", "CN EE,US EE"),
            ("Delivery PCBA to factory", "EB0-PCBA", "2026-02-26", "Done", "Factory"),
            ("EB0 assembly", "EB0", "2026-03-04", "Done", "Factory"),
            ("Verify temperature and KPI data for EB0 samples", "EB0", "2026-03-07", "Done", "Factory"),
            ("Ship samples to US and UK team", "Sample", "2026-03-12", "Done", "CN NPI"),
            ("Provide feedback of EB0 samples", "EB0", "2026-03-19", "Done", "US PD,US Quality"),
            ("Run EB0 DQTP", "EB0-DQTP", "2026-04-03", "In Progress", "CN DQTP"),
            ("Release DQTP report", "EB0-DQTP", "2026-04-08", "Not Started", "CN Testing"),
            ("Run compliance testing", "EB1-Compliance", "2026-04-15", "In Progress", "CN Compliance"),
            ("Sample check and send to compliance", "EB1-Compliance", "2026-04-17", "Not Started", "CN Compliance"),
            ("Release tooling PO to factory", "EB0-Tooling", "2026-04-22", "Not Started", "CN Tooling,Factory"),
            ("Mold trial and inject parts for EB0", "EB0", "2026-04-28", "Not Started", "Factory"),
            ("Upload artwork for EB0", "EB0", "2026-05-06", "Not Started", "CN Artwork"),
            ("Prepare EB0 materials", "EB0", "2026-05-08", "Not Started", "Factory"),
            ("Prepare PKG for MP", "MP-PKG", "2026-05-18", "Not Started", "CN Packaging"),
            ("Conduct Packaging Test", "MP-PKG", "2026-05-22", "Not Started", "CN Packaging"),
            ("Release LOA or PO for LLT material", "MP Prep", "2026-05-26", "Not Started", "CN SC"),
            ("Update ID & UI spec for MP", "MP Prep", "2026-06-03", "Not Started", "US ID"),
            ("Upload artwork for MP", "MP Prep", "2026-06-07", "Not Started", "CN Artwork"),
            ("Update EBOM for MP", "MP Prep", "2026-06-10", "Not Started", "Factory"),
            ("Update CBOM for MP", "MP Prep", "2026-06-14", "Not Started", "CN SC"),
            ("Release ECN to factory", "MP Prep", "2026-06-18", "Not Started", "CN NPI"),
            ("Initiate MP Work Flow in PLM", "MP Prep", "2026-06-24", "Not Started", "CN NPI"),
            ("Prepare MP materials", "MP Prep", "2026-06-28", "Not Started", "Factory"),
            ("Sign golden samples for MP", "MP Prep", "2026-07-03", "Not Started", "CN NPI"),
            ("Start MP", "MP", "2026-07-05", "Not Started", "CN NPI"),
        ],
    },
    {
        "legacy_names": ["AS080UK/EU", "Project-A8"],
        "name": "AS080UK&EU",
        "category": "NPD CAT A",
        "status": "In Progress",
        "phase": "EB1",
        "owner": "CN NPI",
        "brand": "SharkNinja",
        "factory": "Factory Alpha",
        "start_date": "2026-03-23",
        "end_date": "2026-07-05",
        "progress": 18.0,
        "risk_flag": "Critical",
        "department": "PMO",
        "priority": "P1",
        "notes": "Imported from Project plan/AS080UK&EU project plan (MP on July 5).mpp and AS080UK&EU project plan_0330.pdf for real My Project task maintenance.",
        "tasks": [
            ("Kick Off", "Kick Off", "2026-03-23", "Done", "CN NPI,US PMO"),
            ("Finalize PIS for EB0", "EB0", "2026-03-27", "Done", "US PD"),
            ("Finalize ID Spec EB0", "EB0", "2026-03-27", "Done", "US ID,US PD"),
            ("Finalize UI Spec for EB0", "EB0", "2026-03-27", "Not Started", "US PD,US ID"),
            ("Prepare product change PPT and ECN documents", "EB1", "2026-03-30", "Done", "Factory"),
            ("Create ECN", "EB1", "2026-03-31", "Done", "CN NPI"),
            ("Prepare ECN DD documents", "EB1-Compliance", "2026-04-07", "Not Started", "CN Compliance,CN NPI"),
            ("Finalize CBOM for EB0, provide unit cost to PMO", "EB0", "2026-04-14", "Not Started", "CN SC"),
            ("Finalize sample plan for EB0", "EB0", "2026-04-10", "Not Started", "CN NPI,US PMO"),
            ("Sign off ECN to DD approved", "EB1", "2026-04-10", "Not Started", "CN NPI"),
            ("PMO approve sample plan and release P.O to factory", "EB1", "2026-04-16", "Not Started", "US PMO"),
            ("Color chip develop", "EB0-Color", "2026-04-17", "Not Started", "CN Artwork,US ID"),
            ("Prepare improved color chips", "EB0-Color", "2026-04-24", "Not Started", "CN Artwork"),
            ("Approve improved color chips", "EB0-Color", "2026-05-06", "Not Started", "US ID"),
            ("Approve tool cost and release pulp tray EPS tooling", "EB0-Tooling", "2026-04-21", "Not Started", "CN Tooling,US PMO"),
            ("Release Tooling PO", "EB0-Tooling", "2026-04-30", "Not Started", "CN Tooling"),
            ("Prepare common parts for EB1", "EB1", "2026-05-02", "Not Started", "Factory"),
            ("Release and freeze UI flow and control flow for EB1", "EB1", "2026-05-04", "Not Started", "CN EE,US EE"),
            ("Delivery EB1 PCBA to factory", "EB1", "2026-05-06", "Not Started", "Factory"),
            ("Prepare EB1 raw materials", "EB1", "2026-05-08", "Not Started", "Factory"),
            ("Inject and Stamp EB1 materials", "EB1", "2026-05-10", "Not Started", "Factory"),
            ("Upload artwork for EB1", "EB1", "2026-05-11", "Not Started", "CN Artwork"),
            ("EB1 assembly", "EB1", "2026-05-12", "Not Started", "Factory"),
            ("Conduct PSI + Calibration", "EB1", "2026-05-14", "Not Started", "Factory"),
            ("Ship samples to US and UK team", "Sample", "2026-05-16", "Not Started", "CN NPI"),
            ("Provide feedback of EB1 samples", "EB1", "2026-05-22", "Not Started", "US PD,US Quality"),
            ("Run EB1 DQTP", "EB1-DQTP", "2026-05-26", "Not Started", "CN DQTP"),
            ("Run life test", "EB1-DQTP", "2026-06-08", "Not Started", "CN DQTP"),
            ("Release DQTP report", "EB1-DQTP", "2026-06-11", "Not Started", "CN Testing"),
            ("Deliver EB1 samples to HK UL lab", "EB1-Compliance", "2026-05-26", "Not Started", "CN Compliance"),
            ("Compliance test with EB1 samples", "EB1-Compliance", "2026-06-17", "Not Started", "CN Compliance"),
            ("Release LOA or PO for LLT material", "MP Prep", "2026-05-26", "Not Started", "CN SC"),
            ("Update ID & UI spec for MP", "MP Prep", "2026-06-02", "Not Started", "US ID"),
            ("Upload artwork for MP", "MP Prep", "2026-06-05", "Not Started", "CN Artwork"),
            ("Update EBOM for MP", "MP Prep", "2026-06-10", "Not Started", "Factory"),
            ("Update CBOM for MP", "MP Prep", "2026-06-12", "Not Started", "CN SC"),
            ("Release ECN to factory", "MP Prep", "2026-06-17", "Not Started", "CN NPI"),
            ("Initiate MP Work Flow in PLM", "MP Prep", "2026-06-24", "Not Started", "CN NPI"),
            ("Prepare MP materials", "MP Prep", "2026-06-27", "Not Started", "Factory"),
            ("Sign golden samples for MP", "MP Prep", "2026-07-03", "Not Started", "CN NPI"),
            ("Start MP", "MP", "2026-07-05", "Not Started", "CN NPI"),
        ],
    },
]


def _now_str():
    return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def _find_project(db, plan):
    names = [plan["name"]] + plan.get("legacy_names", [])
    for name in names:
        project = db.query(Project).filter(Project.name == name).first()
        if project:
            return project
    return None


def _infer_manual_note(task_name, due_date, status):
    try:
        due = datetime.strptime(due_date, "%Y-%m-%d")
        today = datetime.utcnow()
        if status != "Done" and due < today:
            return f"Imported project-plan task. Overdue by {(today - due).days} days; owner should update action note."
        if status != "Done" and due <= today + timedelta(days=14):
            return "Imported project-plan task. Due soon; confirm owner action and dependency impact."
    except Exception:
        pass
    return "Imported from real project plan for My Project maintenance."


def ensure_real_project_plans(db, username="sunny"):
    now = _now_str()
    ensured = []

    for plan in REAL_PROJECT_PLANS:
        project = _find_project(db, plan)
        if project:
            project.name = plan["name"]
        else:
            project = Project(name=plan["name"], created_at=now)
            db.add(project)
            db.flush()

        for field in (
            "category", "status", "phase", "owner", "brand", "factory",
            "start_date", "end_date", "progress", "risk_flag", "department",
            "priority", "notes",
        ):
            setattr(project, field, plan.get(field))
        project.source_system = "Project Plan Import"
        project.updated_at = now

        existing_tasks = {
            (m.phase or "", m.name): m
            for m in db.query(Milestone).filter(Milestone.project_id == project.id).all()
        }
        for name, phase, due_date, status, owner in plan["tasks"]:
            key = (phase or "", name)
            milestone = existing_tasks.get(key)
            if not milestone:
                milestone = Milestone(
                    project_id=project.id,
                    name=name,
                    phase=phase,
                    due_date=due_date,
                    status=status,
                    owner=owner,
                    is_manual=0,
                    manual_priority="P1" if plan["priority"] == "P1" else "P2",
                    manual_notes=_infer_manual_note(name, due_date, status),
                    created_at=now,
                    updated_at=now,
                )
                if status == "Done":
                    milestone.actual_date = due_date
                db.add(milestone)

        subscription = db.query(UserProject).filter(
            UserProject.username == username,
            UserProject.project_id == project.id,
        ).first()
        if not subscription:
            db.add(UserProject(username=username, project_id=project.id, created_at=now))

        for legacy_name in plan.get("legacy_names", []):
            duplicate = db.query(Project).filter(Project.name == legacy_name).first()
            if duplicate and duplicate.id != project.id:
                for milestone in db.query(Milestone).filter(Milestone.project_id == duplicate.id).all():
                    key = (milestone.phase or "", milestone.name)
                    if key in existing_tasks:
                        db.delete(milestone)
                    else:
                        milestone.project_id = project.id
                        existing_tasks[key] = milestone
                db.query(UserProject).filter(UserProject.project_id == duplicate.id).delete()
                db.delete(duplicate)

        ensured.append(project.name)

    db.commit()
    return ensured
