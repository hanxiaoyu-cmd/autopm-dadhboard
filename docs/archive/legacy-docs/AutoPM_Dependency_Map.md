# AutoPM Platform Build — Dependency Map & Resource Allocation

> **Version**: v1.0 | **Baseline**: Project Kickoff | **Scope**: Dependency graph + role allocation
> **Rule**: Global toolchain only — no region-locked services

---

## Module Dependency Overview

```
                        ┌─────────────────────────┐
                        │  Module 1: Infrastructure │
                        │  5-7 days · 1 DevOps     │
                        └──────────┬──────────────┘
                                   │
                 ┌─────────────────┼──────────────────┐
                 │                 │                   │
                 ▼                 ▼                   ▼
  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────┐
  │ Module 2:        │  │ Module 6:        │  │ Module 4:            │
  │ Data Pipeline    │  │ Security &       │  │ Frontend Refactoring │
  │ 7-14 days        │  │ Compliance       │  │ 7-10 days            │
  │ 1-2 Backend+M+S  │  │ 2-4 weeks (wait) │  │ 1 Frontend Dev       │
  │ ⚠️ HIGHEST RISK  │  │ IT Security Team  │  │ (mock API from Day1) │
  └────────┬─────────┘  └──────────────────┘  └──────────┬───────────┘
           │                                              │
           │  data ready                                  │  API ready
           ▼                                              │
  ┌──────────────────┐                                    │
  │ Module 3:        │                                    │
  │ AI Engine        │◄───────────────────────────────────┘
  │ 7-10 days        │   (4.2 waits for Module 2 API)
  │ 1 AI Dev + Sunny │
  └────────┬─────────┘
           │  alerts generated
           ▼
  ┌──────────────────┐
  │ Module 5:        │
  │ Notification &   │
  │ Push System      │
  │ 5-7 days         │
  │ 1 Backend Dev    │
  └──────────────────┘
```

---

## Detailed Dependency Chain

### Module 1: Infrastructure & Deployment (5-7 days)

| # | Task | Days | Role | Depends On | Deliverable |
|---|------|------|------|-----------|-------------|
| 1.1 | Server selection & provisioning | 2 | 1 DevOps Engineer | — | Server instance live, SSH accessible |
| 1.2 | Runtime environment setup (OS, Python, Nginx, PostgreSQL, Redis) | 2 | 1 DevOps Engineer | 1.1 | Environment checklist verified |
| 1.3 | Domain & intranet access configuration | 1 | 1 DevOps + IT Network | 1.2 | Domain resolves, curl returns 200 |
| 1.4 | CI/CD deployment pipeline | 1 | 1 DevOps Engineer | 1.2 | `git push` → auto-deploy in 5 min |
| 1.5 | Server health monitoring (Prometheus + Grafana) | 1 | 1 DevOps Engineer | 1.2 | Grafana dashboard + alerts active |

**Dependency chain**:
```
[1.1 Server Provisioning] → (2d) → [DevOps] → [None] → Server instance ready
    │
    ▼
[1.2 Runtime Setup] → (2d) → [DevOps] → [1.1] → Environment verified
    │
    ├──▶ [1.3 Domain Config] → (1d) → [DevOps + IT Network] → [1.2] → Domain accessible
    ├──▶ [1.4 CI/CD Pipeline] → (1d) → [DevOps] → [1.2] → Auto-deploy working
    └──▶ [1.5 Monitoring] → (1d) → [DevOps] → [1.2] → Alerts firing
```

**Team**: 1 DevOps Engineer (full ownership)

---

### Module 2: Data Pipeline (7-14 days) — ⚠️ HIGHEST RISK

| # | Task | Days | Role | Depends On | Deliverable |
|---|------|------|------|-----------|-------------|
| 2.1 | E3 API/CSV/DB investigation | 2-3 | 1 Backend Dev + Marcus (IT) | Module 1 complete | Data source scenario confirmed |
| 2.2 | E3 data connector build (3 scenarios) | 3-5 | 1-2 Backend Devs | 2.1 | Connector tested with sample data |
| 2.3 | PLM data connector | 2-3 | 1 Backend Dev + IT | 2.1 | PLM data flowing into staging |
| 2.4 | Email parsing (CC emails → project status) | 2 | 1 Backend Dev | Module 1 (server for mail daemon) | Email parser returns structured data |
| 2.5 | Data cleaning & standardization | 2-3 | 1 Backend Dev + Sunny (PM) | 2.2, 2.3 | Clean dataset, mapping rules doc |
| 2.6 | Data sync mechanism (frequency, incremental/full) | 1-2 | 1 Backend Dev | 2.5 | Sync job running on schedule |
| 2.7 | Database selection & schema design | 1 | 1 Backend Dev | 2.1 (schema depends on data shape) | Schema v1 documented |
| 2.8 | Initial data import script | 1-2 | 1 Backend Dev | 2.5, 2.7 | Production DB populated |
| 2.9 | Data quality audit (≥70% fill rate) | 1 | Sunny (PM) | 2.8 | Quality report with gap analysis |
| 2.10 | Fallback: CSV manual import workflow | 1 | Sunny (PM) | If 2.2 fails | CSV upload UI + validation |

**Dependency chain**:
```
[2.1 E3 Investigation] → (2-3d) → [1 Backend + Marcus(IT)] → [Module 1] → Scenario confirmed
    │
    ├──▶ [2.2 E3 Connector] → (3-5d) → [1-2 Backend Devs] → [2.1] → Connector working
    ├──▶ [2.3 PLM Connector] → (2-3d) → [1 Backend + IT] → [2.1] → PLM data flowing
    ├──▶ [2.7 DB Schema Design] → (1d) → [1 Backend Dev] → [2.1] → Schema v1 locked
    │
    │        ┌── [2.2 done] ──┐
    │        └── [2.3 done] ──┼──▶ [2.5 Data Cleaning] → (2-3d) → [1 Backend + Sunny] → [2.2+2.3] → Clean dataset
    │                                                    │
    │                                        ┌───────────┤
    │                                        │           │
    │                                        ▼           ▼
    │                          [2.6 Sync Mechanism]  [2.8 Initial Import]
    │                           (1-2d, Backend)      (1-2d, Backend)
    │                           depends: 2.5         depends: 2.5+2.7
    │                                                    │
    │                                                    ▼
    │                                          [2.9 Quality Audit] → (1d) → [Sunny(PM)] → [2.8] → ≥70% fill rate
    │
    [2.4 Email Parsing] → (2d) → [1 Backend Dev] → [Module 1] → Email→data working
    [2.10 CSV Fallback] → (1d) → [Sunny(PM)] → [If 2.2 fails] → Manual import path
```

**Team**: 1-2 Backend Developers + Marcus (IT contact) + Sunny (PM)

---

### Module 3: AI Engine (7-10 days)

| # | Task | Days | Role | Depends On | Deliverable |
|---|------|------|------|-----------|-------------|
| 3.1 | Migrate 3-layer analysis logic (JS → Python) | 2-3 | 1 Backend/AI Dev | Module 2 data ready | Python analysis module running |
| 3.2 | LLM integration (OpenAI / Copilot API) | 2 | 1 Backend/AI Dev | 3.1 | LLM returning structured analysis |
| 3.3 | Scheduled task framework (daily analysis + alerts) | 1-2 | 1 Backend Dev | 3.2 | Cron job triggers analysis daily |
| 3.4 | Alert rules engine (Delay / Stuck / Conflict) | 1-2 | 1 Backend/AI Dev | 3.2 | 3 alert types firing correctly |
| 3.5 | Signal-to-noise optimization (actionable ≥60%) | 1-2 | 1 AI Dev + Sunny | 3.4 | Noise filtered, actionable rate ≥60% |
| 3.6 | Historical data backtesting | 1 | 1 AI Dev | 3.4 | Backtest report with accuracy metrics |
| 3.7 | Alert priority classification | 1 | 1 AI Dev | 3.4 | P1/P2/P3 labels applied |
| 3.8 | Prompt engineering & tuning | 1-2 | 1 AI Dev + Sunny | 3.2 | Prompt template v1 frozen |

**Dependency chain**:
```
[3.1 Logic Migration] → (2-3d) → [1 AI Dev] → [Module 2 data] → Python analysis working
    │
    ▼
[3.2 LLM Integration] → (2d) → [1 AI Dev] → [3.1] → OpenAI/Copilot API connected
    │
    ├──▶ [3.3 Scheduled Tasks] → (1-2d) → [1 Backend] → [3.2] → Daily cron running
    ├──▶ [3.4 Alert Rules Engine] → (1-2d) → [1 AI Dev] → [3.2] → 3 alert types firing
    │        │
    │        ├──▶ [3.5 Signal-to-Noise] → (1-2d) → [AI Dev + Sunny] → [3.4] → ≥60% actionable
    │        ├──▶ [3.6 Backtesting] → (1d) → [1 AI Dev] → [3.4] → Accuracy report
    │        └──▶ [3.7 Priority Classification] → (1d) → [1 AI Dev] → [3.4] → P1/P2/P3 tagged
    │
    └──▶ [3.8 Prompt Tuning] → (1-2d) → [AI Dev + Sunny] → [3.2] → Prompt v1 frozen
```

**Team**: 1 Backend/AI Developer + Sunny (PM, part-time)

---

### Module 4: Frontend Refactoring (7-10 days)

| # | Task | Days | Role | Depends On | Deliverable |
|---|------|------|------|-----------|-------------|
| 4.1 | Restructure single HTML → deployable web app | 2-3 | 1 Frontend Dev | Module 1 (deploy target) | App scaffolded, builds, deploys |
| 4.2 | Replace hardcoded data → API calls | 2 | 1 Frontend Dev | Module 2 API ready | Live data rendering |
| 4.3 | User Authentication (SSO/LDAP) | 1-2 | 1 Frontend Dev + IT | 4.1 | SSO login flow working |
| 4.4 | Real-time data refresh | 1 | 1 Frontend Dev | 4.2 | Auto-refresh without reload |
| 4.5 | Responsive design optimization | 1-2 | 1 Frontend Dev | 4.1 (can start with mock) | Mobile/tablet layouts |
| 4.6 | Analysis page refactoring | 1-2 | 1 Frontend Dev | 4.2, Module 3 | Analysis UI with live AI results |
| 4.7 | Error handling & loading states | 1 | 1 Frontend Dev | 4.2 | Graceful error UX |
| 4.8 | Browser compatibility testing | 1 | 1 Frontend Dev | 4.1-4.7 | Cross-browser pass report |

**Dependency chain**:
```
[4.1 App Restructure] → (2-3d) → [1 Frontend] → [Module 1] → App builds & deploys
    │
    ├──▶ [4.3 SSO/LDAP Auth] → (1-2d) → [Frontend + IT] → [4.1] → Login flow working
    ├──▶ [4.5 Responsive Design] → (1-2d) → [1 Frontend] → [4.1] → Mobile layouts ✅
    │
    ▼ (waits for Module 2 API)
[4.2 API Integration] → (2d) → [1 Frontend] → [Module 2 API] → Live data rendering
    │
    ├──▶ [4.4 Real-time Refresh] → (1d) → [1 Frontend] → [4.2] → Auto-refresh ✅
    ├──▶ [4.6 Analysis Page] → (1-2d) → [1 Frontend] → [4.2 + Module 3] → AI results in UI
    └──▶ [4.7 Error Handling] → (1d) → [1 Frontend] → [4.2] → Graceful error UX
    │
    ▼
[4.8 Browser Testing] → (1d) → [1 Frontend] → [4.1-4.7] → Cross-browser pass

⚡ PARALLEL TRACK: 4.1 → 4.5 can start with mock API before Module 2 completes
```

**Team**: 1 Frontend Developer (full ownership)

---

### Module 5: Notification & Push System (5-7 days)

| # | Task | Days | Role | Depends On | Deliverable |
|---|------|------|------|-----------|-------------|
| 5.1 | AI alert email auto-send (Exchange/Office 365 SMTP) | 1-2 | 1 Backend Dev | Module 3 (alerts exist) | Alert emails firing |
| 5.2 | Email receiving & parsing (CC → system data) | 1-2 | 1 Backend Dev | Module 1 | Inbound email → parsed data |
| 5.3 | Microsoft Teams integration (webhook/bot) | 1-2 | 1 Backend Dev + IT | Module 3 | Alerts posting to Teams channels |
| 5.4 | Microsoft Copilot integration | 1-2 | 1 Backend/AI Dev | 3.2 | Copilot surface shows alerts |
| 5.5 | Notification dedup & noise reduction | 1 | 1 Backend Dev | 5.1 | No duplicate alerts |
| 5.6 | Priority-based notification routing | 1 | 1 Backend Dev | 5.1, 3.7 | P1→immediate, P2→digest, P3→weekly |

**Dependency chain**:
```
[Module 3: AI alerts ready] ──┐
                               │
    ┌──────────────────────────┤
    │                          │
    ▼                          ▼
[5.1 Email Auto-send]    [5.3 Teams Integration] → (1-2d) → [Backend + IT] → [Module 3] → Teams bot posting
 (1-2d, Backend)          [5.4 Copilot Integration] → (1-2d) → [Backend/AI Dev] → [3.2] → Copilot surface
    │
    ├──▶ [5.5 Dedup & Noise Reduction] → (1d) → [1 Backend] → [5.1] → No duplicates
    └──▶ [5.6 Priority Routing] → (1d) → [1 Backend] → [5.1 + 3.7] → Route by priority

[5.2 Email Receiving] → (1-2d) → [1 Backend Dev] → [Module 1] → Inbound parser live
```

**Team**: 1 Backend Developer (+ IT for Teams/Copilot setup)

---

### Module 6: Security & Compliance (2-4 weeks, mostly waiting)

| # | Task | Days | Role | Depends On | Delivers |
|---|------|------|------|-----------|----------|
| 6.1 | User authentication & role-based access | 2-3 | 1 DevOps + IT Security | Module 1 | SSO/RBAC configured |
| 6.2 | HTTPS & data encryption in transit | 1 | IT Security | Module 1 | TLS certs installed |
| 6.3 | IT security audit submission | ⏳ 1-2 weeks wait | IT Security Team | Module 1 | Audit request submitted |
| 6.4 | Data access control (project-level permissions) | 2-3 | 1 Backend Dev + IT | 6.1 | Per-project access enforced |
| 6.5 | Audit logging | 1-2 | 1 Backend Dev | 6.1 | All actions logged |
| 6.6 | GDPR / data privacy compliance check | ⏳ 1-2 weeks wait | Legal + IT Security | 6.4 | Compliance clearance |
| 6.7 | Penetration testing (if required) | ⏳ | IT Security | 6.3 | Pen-test report |

**Dependency chain**:
```
[Module 1: Server ready] ──┐
                            │
    ┌───────────────────────┤
    │                       │
    ▼                       ▼
[6.1 Auth & RBAC]    [6.2 HTTPS & Encryption] → (1d) → [IT Security] → [Module 1] → TLS active
 (2-3d, DevOps+IT)
    │
    ├──▶ [6.3 Audit Submission] → (⏳ 1-2w) → [IT Security Team] → [Module 1] → Submitted
    │        │
    │        └──▶ [6.7 Pen-test] → (⏳) → [IT Security] → [6.3] → Pen-test report
    │
    ├──▶ [6.4 Project-Level Access Control] → (2-3d) → [Backend + IT] → [6.1] → Per-project perms
    │        │
    │        └──▶ [6.6 GDPR Check] → (⏳ 1-2w) → [Legal + IT Security] → [6.4] → Compliance clearance
    │
    └──▶ [6.5 Audit Logging] → (1-2d) → [1 Backend Dev] → [6.1] → All actions logged

📌 Week 1: Submit audit request IMMEDIATELY — do not wait for other modules.
```

**Team**: IT Security Team + 1 Backend Dev (part-time)

---

## Critical Path Analysis

### Path Definitions

```
CRITICAL PATH (most likely):

Day 0        Day 7           Day 21              Day 31           Day 38        Day 45
  │           │                │                   │                │              │
  ▼           ▼                ▼                   ▼                ▼              ▼
  ├─ Module 1 ─┤── Module 2 ──────┤── Module 3 ──────┤── Module 5 ───┤
  │ (5-7d)    │  (7-14d, risk)    │  (7-10d)         │  (5-7d)       │
  │ 1 DevOps  │  1-2 Backend+M+S  │  1 AI Dev+Sunny  │  1 Backend    │
  │           │                   │                   │               │
  │           │    Module 4 ──────────────┤           │               │
  │           │  (starts Day 7, mock API) │  (4.2 waits│               │
  │           │   1 Frontend              │   for M2)  │               │
  │           │                           │            │               │
  │  Module 6 starts Day 0 (submit audit request immediately)          │
  │  Security Team parallel throughout                                  │
```

### Three Scenarios

| Scenario | Total Duration | Path | Key Assumptions |
|----------|---------------|------|-----------------|
| **Optimistic** | **5-6 weeks** | M1(5d) → M2(7d) → M3(7d) → M5(5d) | E3 has API, no data quality issues, Copilot API smooth |
| **Most Likely** | **7-8 weeks** | M1(7d) → M2(14d) → M3(10d) → M5(7d) | E3 needs CSV fallback, data cleaning takes extra iteration |
| **Pessimistic** | **10-12 weeks** | M1(7d) → M2(14d+) → M3(10d+) → M5(7d+) + security blockers | E3 has no API, manual data entry, security audit rejection, GDPR issues |

### Critical Path with Role Tags

```
FASTEST (Optimistic — 5-6 weeks):

[1 DevOps]          [1-2 Backend]        [1 AI Dev]           [1 Backend]
     │                    │                    │                    │
M1(5d) ───────▶ M2(7d) ───────▶ M3(7d) ───────▶ M5(5d)
                   +Marcus(IT)      +Sunny(PM)          +IT(Teams)
                   +Sunny(PM)


MOST LIKELY (7-8 weeks):

[1 DevOps]    [1-2 Backend]        [1 AI Dev]           [1 Backend]
     │              │                    │                    │
M1(7d) ──────▶ M2(14d) ──────▶ M3(10d) ──────▶ M5(7d)
                +Marcus(IT)        +Sunny(PM)          +IT(Teams)
                +Sunny(PM)

 ═══════════ PARALLEL ═══════════
 [1 Frontend]   [IT Security Team]
      │                │
  M4(7-10d)      M6(2-4 weeks, mostly wait)
  starts Day 7   starts Day 0


SLOWEST (Pessimistic — 10-12 weeks):

[1 DevOps]   [1-2 Backend]         [1 AI Dev]           [1 Backend]
     │             │                     │                    │
M1(7d) ────▶ M2(14d+) ────────▶ M3(10d+) ────────▶ M5(7d+)
               +Marcus(IT)          +Sunny(PM)          +IT(Teams)
               +Sunny(PM)
               ⚠️ E3 no API         ⚠️ LLM tuning         ⚠️ Copilot
               ⚠️ Manual CSV         ⚠️ Signal-to-noise       delays
               ⚠️ Data quality <70%

 BLOCKER: M6 security audit rejection → rework → 2-4 weeks extra delay
```

---

## Resource Timeline (Who Does What, When)

```
Week    1     2     3     4     5     6     7     8
        ├─────┼─────┼─────┼─────┼─────┼─────┼─────┤

DevOps  ████──·     ·     ·     ·     ·     ·     ·     M1 only
              ↑ M1 done

Backend ·  ███████████████████·─────·─────·     ·     M2 → M5
        ·  M2 (data)          ↑M2 done
        ·                      ·  M5 (notify)

AI Dev  ·     ·     ·     ███████████·─────·     ·     M3
        ·     ·     ·     M3 (engine)  ↑M3 done

Frontend·  ░░░░░░░░░░░░░░░░·─────·     ·     ·     M4
        ·  M4 (mock API)  ↑ real API
        ·                   ↑ M4 done

Sunny   ·  ██·  ████·  ███·  ██·   █·    ·     ·     PM (part-time)
(PM)    ·  M2  M2    M3   M3   M5
        ·  data  audit  S/N  tune  verify

IT Sec  ██·─────────────────────────████████████·     M6 (submit early, wait)
        ·  submit audit request      audit result
        ·                            + remediation

Marcus  ·  ██·     ·     ·     ·     ·     ·     ·     IT contact (M2 only)
(IT)    ·  M2 E3
        ·  investigation
```

**Legend**: █ active work · ░ mock/parallel work · ↑ milestone

---

## Module Summary Table

| Module | Days | Roles Needed | Headcount | Risk | Key Dependency |
|--------|------|-------------|-----------|------|----------------|
| 1. Infrastructure & Deployment | 5-7 | DevOps Engineer | 1 | Low | None (starting point) |
| 2. Data Pipeline | 7-14 | Backend Devs + Marcus(IT) + Sunny(PM) | 2-3 | **Very High** | Module 1 complete; E3 API availability unknown |
| 3. AI Engine | 7-10 | Backend/AI Dev + Sunny(PM) | 1-2 | Medium | Module 2 data ready |
| 4. Frontend Refactoring | 7-10 | Frontend Dev + IT (SSO) | 1-2 | Low | Module 1 (deploy) + Module 2 (API); mock API allows parallel start |
| 5. Notification & Push System | 5-7 | Backend Dev + IT (Teams/Copilot) | 1-2 | Medium | Module 3 (alerts must exist before pushing) |
| 6. Security & Compliance | 2-4 weeks | IT Security Team + Backend Dev + Legal | 2-3 | High | Module 1 (server for audit); submit Week 1, don't wait |

---

## Global Toolchain Reference

| Function | Tool | Note |
|----------|------|------|
| Communication | Microsoft Teams | Replaces Feishu/DingTalk |
| Email | Exchange / Office 365 | Replaces China-only mail services |
| AI Platform | OpenAI API / Microsoft Copilot | Replaces Qwen (Alibaba) |
| Version Control | GitHub / GitLab | Company standard |
| CI/CD | GitHub Actions / GitLab CI | Company standard |
| Monitoring | Prometheus + Grafana | Industry standard |
| Database | PostgreSQL 15+ | Primary data store |
| Cache | Redis 7+ | Session & queue |
| Web Server | Nginx | Reverse proxy |
| Container | Docker + Docker Compose | Deployment |

---

## Key Risk Callouts

1. **E3 API Availability** (Module 2) — If no API exists, fall back to CSV manual import. This adds 3-5 days and reduces data freshness.
2. **Data Quality < 70%** (Module 2.9) — If fill rate is too low, AI analysis accuracy drops. Sunny must validate early.
3. **Security Audit Timeline** (Module 6) — Submit audit request in Week 1. A rejection can add 2-4 weeks.
4. **Signal-to-Noise Ratio** (Module 3.5) — If actionable rate < 60%, users will ignore alerts. Requires iterative prompt tuning.
5. **LLM API Rate Limits** (Module 3.2) — OpenAI/Copilot rate limits may throttle batch analysis. Plan for queuing.
