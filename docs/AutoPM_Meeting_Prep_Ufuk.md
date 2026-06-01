# AutoPM Meeting Prep: Matthieu + Ufuk

> Prepared for the meeting with Matthieu & Ufuk on AutoPM project

---

## Part 1: Project Introduction

### What is AutoPM?

AutoPM is an **AI-powered NPI Project Management Platform** built for SharkNinja's product development process. SharkNinja currently has **no centralized project management tool** — everything runs on Excel, email chains, and manual tracking. AutoPM fills that gap.

### The Problem

- **1500+ active projects** tracked in spreadsheets — no single source of truth
- **Cross-functional visibility is zero**: PD doesn't know what SC is doing, PMO can't see bottlenecks in real time
- **Risk detection is reactive**: Issues surface only when someone escalates, not when the data shows warning signs
- **12 departments** (PMO, PD, NPI, ID, EE, CMF, DQTP, SC, Quality, Compliance, MFG, Marketing) each operate in silos
- **NPI gates (G1-G6)** are tracked manually with no system enforcement

### Our Solution

A four-layer architecture designed around **who needs what information**:

| Layer | Who | What they see |
|-------|-----|---------------|
| **L1 Company** | CEO / C-Suite | Portfolio health, pipeline, trend analytics, AI insights |
| **L2 Department** | Dept Heads | Dept performance, project list, team allocation, AI suggestions |
| **L3 Personal** | Individual | My tasks, my projects, my deadlines |
| **L4 Project** | Project Team | Project overview, task board, workflow gates, documents, team |

Plus a **Document** layer (LD) with brand → category → project → folder drill-down.

### Current Status

- **Working prototype** deployed at `autopm-dashboard.onrender.com`
- **Pilot project**: XT-500 (real SharkNinja project, data masked for demo)
- **12-department coverage** with realistic team assignments
- **Gate Flowchart (G1-G6)** with branching paths and task-level tracking
- **AI features** (prototype): risk flagging, bottleneck detection, smart suggestions
- **All frontend**, no IT integration yet — designed to work standalone

### What Makes This Different

- **Portfolio-level bottleneck diagnosis** — not just task tracking, but *why* things are stuck
- **Cross-department attribution** — see that 30% of delays come from DQTP, not just that a task is late
- **Role-based views by design** — CEO sees different data than a PM, naturally
- **Built on real NPI workflow** — not a generic PM tool, purpose-built for hardware product development

---

## Part 2: Demo Walkthrough Script

### Opening (30 sec)

> "Let me walk you through AutoPM. This is a prototype we've built to solve SharkNinja's project visibility problem. I'll go through each layer — from CEO view down to individual task level."

### L1 — Company Level (2 min)

**Switch to: Company 👔 → Dashboard tab**

- Show the **portfolio health dashboard**: total projects, on-track/at-risk/delayed counts
- Point out the **heat map** — instantly see which departments have issues
- Click **Pipeline tab**: project pipeline by phase (G1→G6)
- Click **Analytics tab**: trend charts, department comparison
- Click **AI Insights tab**: automated risk flags and bottleneck alerts

> "At CEO level, you see everything in 10 seconds. No digging through spreadsheets."

### L2 — Department Level (2 min)

**Switch to: Department 🏢 → Overview tab**

- Show **department selector pills** (PMO, PD, NPI, ID, EE, CMF, DQTP, SC, Quality, Compliance, MFG, Marketing)
- Click different departments — show how the view changes
- Point out **department-specific project list** and team allocation
- Click **AI Suggestions tab**: "The system tells this department what to focus on"

> "Each department head sees only what's relevant to them. They can switch between departments if they manage multiple."

### L3 — Personal Level (1 min)

**Switch to: Personal 👤 → My Work tab**

- Show **personal task list** with status and deadlines
- Click into a project → jumps to L4

> "At the individual level, it's simple — what do I need to do, and when is it due."

### L4 — Project Level (3 min)

**Switch to: Project 📋 → Overview tab**

- Show **project selector** dropdown — switch between projects
- Point out the **12-department wheel** at the bottom — center shows overall progress, each node is a department with in-progress task count
- Click a department node → see their task details

**Switch to: Tasks tab**

- Show **editable task board** — click status to cycle (Not Started → In Progress → Complete → Delayed)
- Show **date picker** for due dates
- Show **save with toast confirmation**

**Switch to: Workflow tab**

- Show the **Gate Flowchart (G1-G6)** — full interactive flowchart with:
  - Diamond decision gates
  - MP (Mass Production) milestone
  - 21 task bars with assignees
  - Branch switching between Main Line / Component / DQTP / Tooling / Structure / EE / SW+CMF+Pkg

> "This is the actual NPI workflow — G1 through G6 to MP. Each task is assigned, trackable, and the flowchart shows the critical path."

**Switch to: Document tab**

- Show **project-specific documents** — 14 folders organized by NPI category
- Mention: "The standalone Document tab goes deeper — brand → category → project → folder"

**Switch to: Team tab**

- Show **12 team member cards** — avatar, role, department, task count, status

### LD — Document Layer (1 min)

**Switch to: Document 📁 tab**

- Show the **drill-down**: Shark → Category → Project → Folders
- Show Ninja → Category → Project → Folders
- "All project documentation organized by brand and product line"

### Closing (30 sec)

> "This is a working prototype. All data is currently manual input — the next step is connecting it to real data sources and adding AI-powered automation. That's where I'd love your input, Ufuk."

---

## Part 3: Meeting Questions for Ufuk

### 🔧 Technical & Architecture

1. **Data Pipeline**: Our biggest gap is getting real project data into the system. Currently everything is manual input. What's the most practical way to build a data pipeline from SharkNinja's existing systems (Excel, email, SharePoint)? How would you approach this?

2. **AI Integration Strategy**: We have AI features at prototype level (risk flagging, bottleneck detection). If you were to architect the AI layer properly, what would the tech stack look like? What models/approaches would you recommend for:
   - Automated risk detection from project timeline data
   - Predictive delay forecasting
   - Cross-department bottleneck attribution

3. **Scalability**: This prototype serves one project (XT-500) with 12 departments. In reality, SharkNinja has 1500+ projects. What architecture changes would you recommend to scale from prototype to production?

### 🤝 Collaboration & Resources

4. **Your Availability**: Matthieu mentioned your team is stretched right now. Realistically, how many hours per week could you contribute? And what would be the most impactful way to use that time — advising on architecture, or actually writing code?

5. **Your AI Project**: Matthieu mentioned your team is also working on an AI project internally. Are there overlaps or synergies with what we're building? Could we share components or learnings?

6. **Tech Stack Preference**: Our current stack is simple — Python/FastAPI backend, vanilla JS frontend, PostgreSQL, deployed on Render. Would you recommend sticking with this or migrating to something else for production?

### 📋 Practical Next Steps

7. **MVP Scope**: If we had 4-6 weeks with your support, what would you prioritize? Our current thinking: (1) data pipeline, (2) AI risk detection, (3) real project onboarding. Would you change that order?

8. **Integration Points**: What existing tools or data sources should we plan to integrate with? (SAP, SharePoint, Teams, Jira, etc.) Any experience with enterprise integrations at SharkNinja?

9. **Demo to Production**: What's your assessment of the gap between this prototype and something that could be used by real teams daily? What are the top 3 things that need to change?

### 🎯 Strategic

10. **AI Differentiation**: There are plenty of PM tools (Jira, Asana, Monday). Our bet is that AI-powered bottleneck diagnosis at the portfolio level is the differentiator. Do you agree? Or would you focus the AI differently?

11. **SharkNinja Internal AI Landscape**: Who else is working on AI within the company? Are there existing AI platforms or initiatives we should be aware of (Corey Hudson's AI Hub, etc.)?

---

## Quick Reference

| Item | Detail |
|------|--------|
| Demo URL | https://autopm-dashboard.onrender.com |
| Pilot Project | XT-500 (masked data) |
| Key Stakeholders | Mark Barrocas (CEO), Ross (CDO), Jen (boss), Matthieu |
| Current Stack | Python/FastAPI + Vanilla JS + PostgreSQL + Render |
| Status | Working prototype, no IT integration yet |
| Ufuk's Background | AI developer, did 45hr AI Mirror project (concept UI + embedded + CV) |
| Matthieu's View | Interested but team busy; can only offer advice for now |

---

*Document prepared for AutoPM meeting with Matthieu & Ufuk*
