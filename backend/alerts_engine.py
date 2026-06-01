from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from models import Project, Milestone, Alert


def refresh_alerts(db: Session) -> int:
    """Delete all existing alerts and regenerate based on current data."""
    # 1. Delete all old alerts
    db.query(Alert).delete()
    db.flush()

    now = datetime.utcnow()
    new_alerts = []

    # ── Rule 1: delay ──────────────────────────────────────
    # Milestone past due_date and not completed
    milestones = db.query(Milestone).all()
    for ms in milestones:
        if ms.status and ms.status.lower() == "completed" or not ms.due_date:
            continue
        try:
            due = datetime.strptime(ms.due_date, "%Y-%m-%d")
        except ValueError:
            continue
        if due >= now:
            continue
        days_over = (now - due).days
        if days_over >= 14:
            level = "red"
        elif days_over >= 7:
            level = "orange"
        else:
            level = "yellow"
        project = db.query(Project).filter(Project.id == ms.project_id).first()
        project_name = project.name if project else "Unknown"
        new_alerts.append(Alert(
            project_id=ms.project_id,
            type="delay",
            level=level,
            message=f"Milestone '{ms.name}' of project {project_name} is {days_over} days overdue",
            is_read=0,
            created_at=now.strftime("%Y-%m-%d %H:%M:%S"),
        ))

    # ── Rule 2: stuck ──────────────────────────────────────
    # Project not updated for >7 days
    projects = db.query(Project).all()
    for p in projects:
        if p.status and p.status.lower() in ("completed", "on hold") or not p.updated_at:
            continue
        try:
            updated = datetime.strptime(p.updated_at, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            try:
                updated = datetime.strptime(p.updated_at, "%Y-%m-%d")
            except ValueError:
                continue
        days_idle = (now - updated).days
        if days_idle >= 14:
            level = "red"
        elif days_idle >= 7:
            level = "yellow"
        else:
            continue
        new_alerts.append(Alert(
            project_id=p.id,
            type="stuck",
            level=level,
            message=f"Project {p.name} has no updates for {days_idle} days",
            is_read=0,
            created_at=now.strftime("%Y-%m-%d %H:%M:%S"),
        ))

    # ── Rule 3: due_soon ───────────────────────────────────
    # Milestone due within 3 days and not completed
    for ms in milestones:
        if ms.status and ms.status.lower() == "completed" or not ms.due_date:
            continue
        try:
            due = datetime.strptime(ms.due_date, "%Y-%m-%d")
        except ValueError:
            continue
        days_left = (due - now).days
        if days_left < 0:
            continue  # already handled by delay rule
        if days_left <= 1:
            level = "orange"
        elif days_left <= 3:
            level = "yellow"
        else:
            continue
        project = db.query(Project).filter(Project.id == ms.project_id).first()
        project_name = project.name if project else "Unknown"
        new_alerts.append(Alert(
            project_id=ms.project_id,
            type="due_soon",
            level=level,
            message=f"Milestone '{ms.name}' of project {project_name} is due in {days_left} day(s)",
            is_read=0,
            created_at=now.strftime("%Y-%m-%d %H:%M:%S"),
        ))

    # ── Rule 4: resource_conflict ──────────────────────────
    # Same owner has >=2 In Progress projects
    from collections import Counter
    owner_counts = Counter()
    owner_projects = {}
    for p in projects:
        if p.status and p.status.lower() == "in progress" and p.owner:
            owner_counts[p.owner] += 1
            owner_projects.setdefault(p.owner, []).append(p.name)
    for owner, count in owner_counts.items():
        if count >= 3:
            level = "orange"
        elif count >= 2:
            level = "yellow"
        else:
            continue
        # Create one alert per project for that owner
        for p in projects:
            if p.owner == owner and p.status and p.status.lower() == "in progress":
                new_alerts.append(Alert(
                    project_id=p.id,
                    type="resource_conflict",
                    level=level,
                    message=f"{owner} has {count} In-Progress projects: {', '.join(owner_projects[owner])}",
                    is_read=0,
                    created_at=now.strftime("%Y-%m-%d %H:%M:%S"),
                ))

    # Bulk insert
    for alert in new_alerts:
        db.add(alert)

    db.commit()
    return len(new_alerts)
