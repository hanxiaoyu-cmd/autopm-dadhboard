from sqlalchemy import Column, Integer, Text, Float
from database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    category = Column(Text)
    status = Column(Text, default="In Progress")
    phase = Column(Text)
    owner = Column(Text)
    brand = Column(Text)
    factory = Column(Text)
    start_date = Column(Text)
    end_date = Column(Text)
    progress = Column(Float, default=0.0)
    risk_flag = Column(Text, default="None")
    risk_note = Column(Text)
    source_system = Column(Text, default="Manual")
    department = Column(Text)
    blocked_at = Column(Text)
    blocked_days = Column(Integer, default=0)
    blocked_department = Column(Text)
    priority = Column(Text)
    notes = Column(Text)
    created_at = Column(Text)
    updated_at = Column(Text)


class Milestone(Base):
    __tablename__ = "milestones"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False)
    name = Column(Text, nullable=False)
    phase = Column(Text)
    due_date = Column(Text)
    actual_date = Column(Text)
    status = Column(Text, default="Not Started")
    owner = Column(Text)
    is_manual = Column(Integer, default=0)
    manual_priority = Column(Text)
    manual_notes = Column(Text)
    created_at = Column(Text)
    updated_at = Column(Text)


class Risk(Base):
    __tablename__ = "risks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer, nullable=False)
    description = Column(Text, nullable=False)
    severity = Column(Text, default="Low")
    mitigation = Column(Text)
    owner = Column(Text)
    status = Column(Text, default="Open")
    days = Column(Integer, default=0)
    created_at = Column(Text)
    updated_at = Column(Text)


class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(Integer)
    type = Column(Text)
    level = Column(Text)
    message = Column(Text)
    is_read = Column(Integer, default=0)
    created_at = Column(Text)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, unique=True, nullable=False)
    email = Column(Text)
    password_hash = Column(Text, nullable=False)
    role = Column(Text, default="member")
    created_at = Column(Text)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text)
    role = Column(Text)
    category = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(Text)


class UserProject(Base):
    __tablename__ = "user_projects"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False)
    project_id = Column(Integer, nullable=False)
    created_at = Column(Text)
