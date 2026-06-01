"""Seed the database with ~2200 projects, blockers, capacity data for AutoPM v17.0."""
import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timedelta
from database import engine, SessionLocal, Base
from models import Project, Milestone, Risk, User, Alert, Feedback, UserProject
from auth import hash_password
from alerts_engine import refresh_alerts

random.seed(42)

# ════════════════════════════════════════════════════════════
# 12 Departments with capacity data
# ════════════════════════════════════════════════════════════
DEPARTMENTS = [
    {'id': 'PMO', 'headcount': 8, 'allocated': 7, 'icon': '📋', 'fullName': 'CN NPI / US PMO'},
    {'id': 'PD', 'headcount': 6, 'allocated': 4, 'icon': '📐', 'fullName': 'US Product Design'},
    {'id': 'NPI', 'headcount': 5, 'allocated': 4, 'icon': '🔄', 'fullName': 'NPI Engineering'},
    {'id': 'ID', 'headcount': 4, 'allocated': 2, 'icon': '🎨', 'fullName': 'US Industrial Design'},
    {'id': 'EE', 'headcount': 7, 'allocated': 6, 'icon': '⚡', 'fullName': 'US/CN Electrical Engineering'},
    {'id': 'CMF', 'headcount': 5, 'allocated': 3, 'icon': '🖌️', 'fullName': 'CN Artwork & CMF'},
    {'id': 'DQTP', 'headcount': 6, 'allocated': 5, 'icon': '🔬', 'fullName': 'CN DQTP Lab'},
    {'id': 'SC', 'headcount': 8, 'allocated': 7, 'icon': '📦', 'fullName': 'CN Supply Chain'},
    {'id': 'Quality', 'headcount': 4, 'allocated': 2, 'icon': '✅', 'fullName': 'CN/US Quality Assurance'},
    {'id': 'Compliance', 'headcount': 3, 'allocated': 2, 'icon': '📋', 'fullName': 'CN Compliance'},
    {'id': 'MFG', 'headcount': 6, 'allocated': 4, 'icon': '🏭', 'fullName': 'Factory Manufacturing'},
    {'id': 'Marketing', 'headcount': 4, 'allocated': 1, 'icon': '📢', 'fullName': 'US Creative / UK Marketing'},
]

# Department distribution weights (proportional to size)
DEPT_WEIGHTS = {
    'PMO': 0.12, 'PD': 0.08, 'NPI': 0.07, 'ID': 0.05,
    'EE': 0.11, 'CMF': 0.07, 'DQTP': 0.08, 'SC': 0.13,
    'Quality': 0.06, 'Compliance': 0.05, 'MFG': 0.10, 'Marketing': 0.08
}

# Higher at-risk rates for certain departments
DEPT_AT_RISK_RATE = {
    'PMO': 0.28, 'PD': 0.18, 'NPI': 0.20, 'ID': 0.10,
    'EE': 0.22, 'CMF': 0.18, 'DQTP': 0.20, 'SC': 0.30,
    'Quality': 0.15, 'Compliance': 0.25, 'MFG': 0.22, 'Marketing': 0.08
}

CATEGORIES = [
    'NPD CAT A', 'NPD CAT B', 'NPD/Dual source', 'Extension', 'Legacy/Dual Source',
    'Legacy/Transfer', 'Capacity Tools', 'New CMF', 'Upsell'
]

FACTORIES = [
    'Factory Alpha', 'Factory Beta', 'Factory Gamma', 'Factory Delta',
    'Factory Epsilon', 'Factory Zeta', 'Factory Eta', 'Factory Theta',
    'Factory Iota', 'Factory Kappa', 'Factory Lambda', 'Factory Mu',
    'Factory Nu', 'Factory Xi', 'Factory Omicron', 'Factory Pi',
    'Factory Rho', 'Factory Sigma', 'Factory Tau', 'Factory Upsilon'
]

OWNERS = [
    'L****', 'N*****', 'S****', 'B***', 'H****', 'K***', 'N**',
    'M*******', 'T******', 'S******', 'Z***', 'A*****', 'F****',
    'L***', 'B**', 'P***', 'M****', 'L*', 'S**', 'K****', 'B****'
]

PHASES = ['Kick Off', 'Concept', 'Design', 'EB0', 'EB1', 'DQTP', 'Compliance', 'M8', 'MP Prep', 'MP']
PHASE_PROGRESS = {
    'Kick Off': 5, 'Concept': 12, 'Design': 25, 'EB0': 35, 'EB1': 48,
    'DQTP': 58, 'Compliance': 65, 'M8': 75, 'MP Prep': 85, 'MP': 95
}

BRANDS = ['Shark', 'Ninja']
CATEGORY_BRAND = {
    'NPD CAT A': 'Ninja', 'NPD CAT B': 'Ninja', 'NPD/Dual source': 'Ninja',
    'Extension': 'Ninja', 'Upsell': 'Ninja',
    'Legacy/Dual Source': 'Shark', 'Legacy/Transfer': 'Shark',
    'Capacity Tools': 'Shark', 'New CMF': 'Shark'
}

PROJECT_PREFIXES = [
    'XT', 'FS', 'PB', 'AF', 'MZ', 'DD', 'CM', 'WF', 'CL', 'AS',
    'FO', 'FT', 'FN', 'CE', 'NC', 'ES', 'CN', 'DZ', 'GR', 'SP',
    'NK', 'WK', 'CO', 'DB', 'TB', 'BN', 'BE', 'BC', 'N7', 'JC',
    'BP', 'QB', 'NJ', 'BR', 'SL', 'SF', 'OL', 'AD', 'BW', 'PG',
    'MC', 'C9', 'CW', 'DW', 'KS', 'CI', 'CF', 'OF', 'KN', 'DC'
]


def generate_projects():
    """Generate ~2200 projects with realistic distribution."""
    target_total = 2200
    projects = []

    # Per-department allocation
    for dept in DEPARTMENTS:
        dept_id = dept['id']
        count = int(target_total * DEPT_WEIGHTS[dept_id])
        at_risk_rate = DEPT_AT_RISK_RATE[dept_id]
        delayed_rate = at_risk_rate * 0.35  # ~35% of at-risk are delayed

        for i in range(count):
            # Determine risk status
            r = random.random()
            if r < delayed_rate:
                risk_flag = 'Critical'
                status = 'Delayed'
                blocked_at = random.choice(['Delayed', 'At Risk', 'Delayed'])
                blocked_department = random.choice([d['id'] for d in DEPARTMENTS if d['id'] != dept_id])
                blocked_days = random.randint(3, 30)
                priority = random.choices(['P0', 'P1', 'P2'], weights=[0.2, 0.5, 0.3])[0]
                risk_note = _generate_risk_note(blocked_department, blocked_days)
            elif r < at_risk_rate:
                risk_flag = 'High'
                status = 'In Progress'
                blocked_at = random.choice(['At Risk', None])
                blocked_department = random.choice([d['id'] for d in DEPARTMENTS if d['id'] != dept_id]) if blocked_at else None
                blocked_days = random.randint(1, 7) if blocked_at else 0
                priority = random.choices(['P1', 'P2', 'P3'], weights=[0.2, 0.4, 0.4])[0]
                risk_note = _generate_risk_note(blocked_department, blocked_days) if blocked_at else None
            else:
                risk_flag = 'None'
                status = 'In Progress'
                blocked_at = None
                blocked_department = None
                blocked_days = 0
                priority = random.choices(['P1', 'P2', 'P3'], weights=[0.05, 0.25, 0.70])[0]
                risk_note = None

            # Project details
            prefix = random.choice(PROJECT_PREFIXES)
            cat = random.choice(CATEGORIES)
            phase = random.choice(PHASES)
            progress = PHASE_PROGRESS.get(phase, 10)
            # Add some variance to progress
            progress = min(95, max(5, progress + random.randint(-8, 8)))

            start_date = (datetime.utcnow() - timedelta(days=random.randint(30, 365))).strftime('%Y-%m-%d')
            end_date = (datetime.utcnow() + timedelta(days=random.randint(10, 365))).strftime('%Y-%m-%d')

            projects.append({
                'name': f'{prefix}-{random.randint(100, 999)}',
                'category': cat,
                'status': status,
                'phase': phase,
                'owner': random.choice(OWNERS),
                'brand': CATEGORY_BRAND.get(cat, random.choice(BRANDS)),
                'factory': random.choice(FACTORIES),
                'start_date': start_date,
                'end_date': end_date,
                'progress': float(progress),
                'risk_flag': risk_flag,
                'risk_note': risk_note,
                'source_system': 'Manual',
                'department': dept_id,
                'blocked_at': blocked_at,
                'blocked_days': blocked_days,
                'blocked_department': blocked_department,
                'priority': priority,
                'notes': None,
            })

    return projects


def _generate_risk_note(dept, days):
    """Generate realistic risk note."""
    notes = {
        'PMO': [
            'MP AW uploading delayed due to prioritization of other SKUs',
            'PMO confirmed the earliest MP date is postponed',
            'Project prioritization conflict — waiting for PMO clearance',
        ],
        'SC': [
            'Sample PO not released per plan',
            'Material ETD shifted — supplier capacity constrained',
            'No firm PO — waiting on Supply Chain confirmation',
        ],
        'Compliance': [
            'Compliance report delayed — test lab backlog',
            'NTT test failed, certificate will delay',
            'Compliance AW cannot be ensured by target date',
        ],
        'CMF': [
            'CMF color still needs improvement — approval pending',
            'Design/CMF review backlog — limited team capacity',
            'Color code confirmation required from CMF team',
        ],
        'EE': [
            'PCB layout approval pending from EE team',
            'FW alpha release sign-off delayed',
            'Electrical spec revision under review',
        ],
        'DQTP': [
            'DQTP report not provided per plan',
            'Test plan approval delayed',
            'Reliability testing stuck — resource constraint',
        ],
        'Quality': [
            'Quality gate review postponed',
            'SIRIM certificate delay due to test failure',
            'KPI food test stuck at custom',
        ],
        'MFG': [
            'Production capacity share — assembly line conflict',
            '2nd tooling transfer delayed',
            'Pilot run schedule under review',
        ],
        'PD': [
            'PD confirmed to release AW later than planned',
            'Product design revision pending approval',
            'Spec change requires PD sign-off',
        ],
        'NPI': [
            'NPI process gate stuck — resource constraint',
            'Build postpone due to material delay',
            'NPI team capacity limited for parallel review',
        ],
        'ID': [
            'UI mylar update needed',
            'Packaging design review pending',
            'Industrial design change request under review',
        ],
        'Marketing': [
            'Budget approval pending from PMO',
            'Marketing materials not ready',
            'Launch date coordination pending',
        ],
    }
    dept_notes = notes.get(dept, ['Delayed — reason under investigation'])
    return random.choice(dept_notes) + (f' ({days} days)' if days else '')


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

        # ── Admin users ────
        admin = db.query(User).filter(User.username == "demo_admin").first()
        if not admin:
            admin = User(
                username="demo_admin", email="admin@autopm.local",
                password_hash=hash_password("autopm2026"), role="admin", created_at=now_str,
            )
            db.add(admin)
            db.flush()

        sunny = db.query(User).filter(User.username == "sunny").first()
        if not sunny:
            sunny = User(
                username="sunny", email="sunny@autopm.local",
                password_hash=hash_password("autopm2026"), role="admin", created_at=now_str,
            )
            db.add(sunny)
            db.flush()

        # ── Create team member users ────
        team_members = []
        for owner_name in OWNERS:
            existing = db.query(User).filter(User.username == owner_name).first()
            if not existing:
                u = User(
                    username=owner_name, email=f"{owner_name.lower().replace('*','')}@autopm.local",
                    password_hash=hash_password("autopm2026"), role="member", created_at=now_str,
                )
                db.add(u)
                team_members.append(u)
        db.flush()

        # ════════════════════════════════════════════════════════════
        # Generate ~2200 projects
        # ════════════════════════════════════════════════════════════
        projects_data = generate_projects()
        created = 0
        for pd in projects_data:
            p = Project(
                name=pd['name'], category=pd['category'], status=pd['status'],
                phase=pd['phase'], owner=pd['owner'], brand=pd['brand'],
                factory=pd['factory'], start_date=pd['start_date'],
                end_date=pd['end_date'], progress=pd['progress'],
                risk_flag=pd['risk_flag'], risk_note=pd['risk_note'],
                source_system=pd['source_system'], department=pd['department'],
                blocked_at=pd['blocked_at'], blocked_days=pd['blocked_days'],
                blocked_department=pd['blocked_department'], priority=pd['priority'],
                notes=pd['notes'], created_at=now_str, updated_at=now_str,
            )
            db.add(p)
            created += 1
        db.commit()
        print(f"Created {created} projects.")

        # ── Find XT-500-like project for demo (first P0 project) ────
        xt500_proj = db.query(Project).filter(Project.priority == 'P0').first()
        if not xt500_proj:
            xt500_proj = db.query(Project).first()

        # ── Seed blockers for XT-500 project ────
        if xt500_proj:
            blockers = [
                {'description': 'PCB layout approval — waiting on EE', 'severity': 'Critical',
                 'owner': 'EE', 'status': 'Open', 'days': 5},
                {'description': 'Material sample — waiting on SC', 'severity': 'High',
                 'owner': 'SC', 'status': 'Open', 'days': 3},
                {'description': 'Color code confirmation — waiting on CMF', 'severity': 'Medium',
                 'owner': 'CMF', 'status': 'Open', 'days': 1},
            ]
            for bl in blockers:
                risk = Risk(
                    project_id=xt500_proj.id,
                    description=bl['description'],
                    severity=bl['severity'],
                    mitigation=f'Escalate to {bl["owner"]} team lead',
                    owner=bl['owner'],
                    status=bl['status'],
                    days=bl['days'],
                    created_at=now_str,
                    updated_at=now_str,
                )
                db.add(risk)

            # Update XT-500 blocked info
            xt500_proj.blocked_at = 'At Risk'
            xt500_proj.blocked_days = 5
            xt500_proj.blocked_department = 'EE'
            xt500_proj.risk_flag = 'Critical'
            xt500_proj.name = 'XT-500'
            xt500_proj.phase = 'EB0'
            xt500_proj.progress = 35.0
            xt500_proj.department = 'PMO'
            xt500_proj.owner = 'L****'
            xt500_proj.factory = 'Factory Alpha'
            xt500_proj.category = 'Extension'
            xt500_proj.priority = 'P0'
        db.commit()

        # ── Add blocker to an FS project (Budget approval) ────
        fs_proj = db.query(Project).filter(Project.name.like('FS%'), Project.risk_flag == 'High').first()
        if fs_proj:
            risk = Risk(
                project_id=fs_proj.id,
                description='Budget approval — waiting on PMO',
                severity='High',
                mitigation='Escalate to PMO director for budget sign-off',
                owner='PMO',
                status='Open',
                days=2,
                created_at=now_str,
                updated_at=now_str,
            )
            db.add(risk)
            fs_proj.blocked_at = 'At Risk'
            fs_proj.blocked_days = 2
            fs_proj.blocked_department = 'PMO'
            fs_proj.risk_flag = 'High'
        db.commit()

        # ── Mark 3-5 projects as "Needs Decision" ────
        decision_projects = db.query(Project).filter(Project.risk_flag == 'Critical').limit(5).all()
        for i, dp in enumerate(decision_projects):
            reasons = [
                'Budget overrun risk — need VP approval to continue',
                'Scope change request — requires product line decision',
                'Supplier sole-source failure — alternate sourcing decision needed',
                'Timeline conflict with NPD CAT A — prioritize or delay?',
                'Regulatory change impact — compliance strategy decision needed',
            ]
            dp.notes = f'DECISION REQUIRED: {reasons[i % len(reasons)]}'
        db.commit()

        # ── Seed demo milestones for XT-500 ────
        today = now.strftime("%Y-%m-%d")
        yesterday = (now - timedelta(days=1)).strftime("%Y-%m-%d")
        tomorrow = (now + timedelta(days=1)).strftime("%Y-%m-%d")
        next_week = (now + timedelta(days=5)).strftime("%Y-%m-%d")
        next_2week = (now + timedelta(days=12)).strftime("%Y-%m-%d")
        next_3week = (now + timedelta(days=20)).strftime("%Y-%m-%d")

        if xt500_proj:
            demo_milestones = [
                {"name": "Kick Off Complete", "phase": "Kick Off", "due_date": yesterday, "status": "Completed", "owner": "PMO"},
                {"name": "Concept Approval", "phase": "Concept", "due_date": yesterday, "status": "Completed", "owner": "PMO"},
                {"name": "Design Freeze", "phase": "Design", "due_date": yesterday, "status": "Completed", "owner": "PD"},
                {"name": "Confirm 2nd Color Chip Sample", "phase": "EB0", "due_date": yesterday, "status": "Not Started", "owner": "CMF"},
                {"name": "EB0 Material Preparation Review", "phase": "EB0", "due_date": yesterday, "status": "Not Started", "owner": "PMO"},
                {"name": "DQTP Test Plan Approval", "phase": "EB0", "due_date": today, "status": "In Progress", "owner": "PMO"},
                {"name": "Supplier Qualification Audit", "phase": "EB0", "due_date": tomorrow, "status": "In Progress", "owner": "SC"},
                {"name": "Color Sample Approval", "phase": "EB0", "due_date": next_week, "status": "In Progress", "owner": "CMF"},
                {"name": "FW Alpha Release Sign-off", "phase": "EB0", "due_date": next_week, "status": "In Progress", "owner": "EE"},
                {"name": "Pilot Run Schedule Review", "phase": "EB1", "due_date": next_2week, "status": "Not Started", "owner": "PMO"},
                {"name": "Compliance Report Update", "phase": "Compliance", "due_date": next_2week, "status": "Not Started", "owner": "Compliance"},
                {"name": "MP Preparation Kickoff", "phase": "MP", "due_date": next_3week, "status": "Not Started", "owner": "PMO"},
            ]
            for md in demo_milestones:
                ms = Milestone(
                    project_id=xt500_proj.id,
                    name=md["name"], phase=md["phase"], due_date=md["due_date"],
                    status=md["status"], owner=md["owner"],
                    is_manual=0, created_at=now_str, updated_at=now_str,
                )
                db.add(ms)

        # Also add milestones for a few other projects
        other_projs = db.query(Project).filter(Project.id != (xt500_proj.id if xt500_proj else -1)).limit(10).all()
        for proj in other_projs:
            phase = proj.phase or 'EB0'
            ms = Milestone(
                project_id=proj.id,
                name=f'{phase} Gate Review',
                phase=phase,
                due_date=(now + timedelta(days=random.randint(-7, 30))).strftime('%Y-%m-%d'),
                status=random.choice(['Not Started', 'In Progress', 'Completed']),
                owner=proj.department or 'PMO',
                is_manual=0, created_at=now_str, updated_at=now_str,
            )
            db.add(ms)
        db.commit()
        print(f"Seeded milestones for XT-500 and {len(other_projs)} other projects.")

        # ── Assign projects to users via UserProject ────
        all_projs = db.query(Project).all()
        for proj in all_projs:
            if proj.owner and random.random() < 0.3:
                up = UserProject(username=proj.owner, project_id=proj.id, created_at=now_str)
                db.add(up)
        db.commit()

        # ── Verification ────
        total = db.query(Project).count()
        on_track = db.query(Project).filter(Project.risk_flag == "None").count()
        at_risk = db.query(Project).filter(Project.risk_flag == "High").count()
        delayed = db.query(Project).filter(Project.risk_flag == "Critical").count()
        needs_decision = db.query(Project).filter(Project.notes.like('DECISION REQUIRED%')).count()
        print(f"Seed complete: {total} projects ({on_track} On Track, {at_risk} At Risk, {delayed} Delayed, {needs_decision} Need Decision)")

        # ── Generate alerts ────
        count = refresh_alerts(db)
        print(f"Generated {count} alerts.")

    except Exception as e:
        db.rollback()
        print(f"Seed failed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
