from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


# ── Auth ──────────────────────────────────────────────
class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None
    role: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


# ── Project ──────────────────────────────────────────
class ProjectCreate(BaseModel):
    name: str
    category: Optional[str] = None
    status: Optional[str] = "In Progress"
    phase: Optional[str] = None
    owner: Optional[str] = None
    brand: Optional[str] = None
    factory: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    progress: Optional[float] = 0.0
    risk_flag: Optional[str] = "None"
    risk_note: Optional[str] = None
    source_system: Optional[str] = "Manual"
    department: Optional[str] = None
    blocked_at: Optional[str] = None
    blocked_days: Optional[int] = 0
    blocked_department: Optional[str] = None
    priority: Optional[str] = None
    notes: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    status: Optional[str] = None
    phase: Optional[str] = None
    owner: Optional[str] = None
    brand: Optional[str] = None
    factory: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    progress: Optional[float] = None
    risk_flag: Optional[str] = None
    risk_note: Optional[str] = None
    source_system: Optional[str] = None
    department: Optional[str] = None
    blocked_at: Optional[str] = None
    blocked_days: Optional[int] = None
    blocked_department: Optional[str] = None
    priority: Optional[str] = None
    notes: Optional[str] = None


class ProjectOut(BaseModel):
    id: int
    name: str
    category: Optional[str] = None
    status: Optional[str] = None
    phase: Optional[str] = None
    owner: Optional[str] = None
    brand: Optional[str] = None
    factory: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    progress: Optional[float] = None
    risk_flag: Optional[str] = None
    risk_note: Optional[str] = None
    source_system: Optional[str] = None
    department: Optional[str] = None
    blocked_at: Optional[str] = None
    blocked_days: Optional[int] = None
    blocked_department: Optional[str] = None
    priority: Optional[str] = None
    notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


class ProjectDetail(ProjectOut):
    milestones: List["MilestoneOut"] = []
    risks: List["RiskOut"] = []
    alerts: List["AlertOut"] = []


# ── Milestone ────────────────────────────────────────
class MilestoneCreate(BaseModel):
    project_id: int
    name: str
    phase: Optional[str] = None
    due_date: Optional[str] = None
    actual_date: Optional[str] = None
    status: Optional[str] = "Not Started"
    owner: Optional[str] = None


class MilestoneUpdate(BaseModel):
    name: Optional[str] = None
    phase: Optional[str] = None
    due_date: Optional[str] = None
    actual_date: Optional[str] = None
    status: Optional[str] = None
    owner: Optional[str] = None
    manual_notes: Optional[str] = None


class MilestoneOut(BaseModel):
    id: int
    project_id: int
    name: str
    phase: Optional[str] = None
    due_date: Optional[str] = None
    actual_date: Optional[str] = None
    status: Optional[str] = None
    owner: Optional[str] = None
    is_manual: Optional[int] = 0
    manual_priority: Optional[str] = None
    manual_notes: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


# ── Risk ─────────────────────────────────────────────
class RiskCreate(BaseModel):
    project_id: int
    description: str
    severity: Optional[str] = "Low"
    mitigation: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = "Open"


class RiskUpdate(BaseModel):
    description: Optional[str] = None
    severity: Optional[str] = None
    mitigation: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None


class RiskOut(BaseModel):
    id: int
    project_id: int
    description: str
    severity: Optional[str] = None
    mitigation: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    days: Optional[int] = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    class Config:
        from_attributes = True


# ── Alert ────────────────────────────────────────────
class AlertOut(BaseModel):
    id: int
    project_id: Optional[int] = None
    type: Optional[str] = None
    level: Optional[str] = None
    message: Optional[str] = None
    is_read: Optional[int] = 0
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


# ── Dashboard ────────────────────────────────────────
class DashboardStats(BaseModel):
    total: int
    by_status: dict
    overdue_count: int
    alert_count: int
    due_soon_count: int


class TimelineItem(BaseModel):
    project: ProjectOut
    milestones: List[MilestoneOut]


# ── User Project (star/follow) ────────────────────────
class UserProjectCreate(BaseModel):
    username: str
    project_id: int


class UserProjectOut(BaseModel):
    id: int
    username: str
    project_id: int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True


# ── Manual Task ──────────────────────────────────────
class ManualTaskCreate(BaseModel):
    name: str
    project_id: Optional[int] = None
    phase: Optional[str] = None
    due_date: Optional[str] = None
    manual_priority: Optional[str] = "P3"
    manual_notes: Optional[str] = None
    owner: Optional[str] = None


class ManualTaskUpdate(BaseModel):
    name: Optional[str] = None
    project_id: Optional[int] = None
    phase: Optional[str] = None
    due_date: Optional[str] = None
    status: Optional[str] = None
    manual_priority: Optional[str] = None
    manual_notes: Optional[str] = None
    owner: Optional[str] = None
    status: Optional[str] = None
    owner: Optional[str] = None


# ── Feedback ─────────────────────────────────────────
class FeedbackCreate(BaseModel):
    name: Optional[str] = None
    role: Optional[str] = None
    category: str
    content: str

class FeedbackOut(BaseModel):
    id: int
    name: Optional[str] = None
    role: Optional[str] = None
    category: str
    content: str
    created_at: Optional[str] = None

    class Config:
        from_attributes = True

# Resolve forward references
ProjectDetail.model_rebuild()
