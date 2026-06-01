# AutoPM — Review of Rodyr Proposal & Draft Reply

> Prepared for: Sun Sun  
> Date: 2026-05-25  
> Context: Ufuk Karaca (Rodyr) sent a feature catalogue + open questions following the discovery call. This document reviews the proposal against AutoPM's actual state and drafts a reply.

---

## Part 1: What Ufuk Got Right

These points are accurate and worth acknowledging:

1. **The 7 quotes** (S01) faithfully capture the core problems. No corrections needed on the framing.

2. **The 3-layer spine** (Collection → Trend Analysis → Optimization) is a sound mental model. AutoPM's current build already covers parts of Layer 1 (Collection) and is beginning Layer 2 (Trend Analysis). Layer 3 is correctly flagged as less mature.

3. **"Not managing tasks, but understanding workflows"** — this is the right positioning. AutoPM was never meant to be another Jira.

4. **The "sit on top of existing systems, not duplicate"** principle (Matthieu's point) is correct as a design constraint. However, see the critical correction below about what "existing systems" actually means at SharkNinja.

5. **The open questions are thoughtful** and most need real answers before any scoping makes sense.

---

## Part 2: What Ufuk Got Wrong or Missed

### ❌ Critical Correction #1: SharkNinja Has NO PM Tool

The proposal repeatedly assumes integration with existing project management systems (PLM, E3, etc.). The reality:

> **SharkNinja has zero project management tool. No Jira, no Feishu PM, no Asana, no nothing.**

AutoPM is not "sitting on top of" an existing PM system — AutoPM IS the system. PLM is just a file folder with no structured data. The "Integration" layer (Cards 11-14) should be reframed: there is nothing to integrate with for project tracking. The only data sources are email threads, Excel files, and human memory.

This changes the entire scope of the engagement. The "Knowledge Graph Substrate" (Card 01) is not integrating with existing databases — it IS the database.

### ❌ Critical Correction #2: AutoPM Is Not a Prototype — It's a Working System

The proposal treats AutoPM as a prototype that needs to be rebuilt from scratch. The actual state:

| Capability | Status |
|---|---|
| 4-layer architecture (Company → Department → Personal → Project) | ✅ Built, deployed, working |
| 2,200+ projects with structured data | ✅ Live on Neon PostgreSQL |
| Task CRUD with phase-grouped board | ✅ Working (v17.5+) |
| Blocker detection & visualization | ✅ Working |
| Gate flowchart (6-gate NPI workflow) | ✅ Working |
| AI contextual hints at every level | ✅ Working |
| Operational Frontier radar (4-dimension scoring) | ✅ Working |
| User authentication & data persistence | ✅ Working |
| Document management (14 NPI folders) | ✅ Working |
| PDF upload → auto task decomposition | ✅ Working |
| Personal daily brief / today's tasks | ✅ Working |

This is v17.6, not a mockup. The foundation Ufuk proposes to build (Cards 01-05) largely already exists.

### ❌ Critical Correction #3: The "Notion/Linear Already Does This" Framing Is Wrong

In the meeting, Ufuk said most AutoPM features can be done by Notion/Linear. This misses the point:

- Notion/Linear are **generic** PM tools. They don't understand SharkNinja's 6-gate NPI process.
- AutoPM is **purpose-built** for this exact workflow: KO → Concept → Design → EB0 → DQTP → Compliance → MP, with 12 departments and Shark/Ninja dual-brand structure.
- No generic tool produces the insight: "30% of DQTP delays originate at G3" — that requires a data model designed around gates, not tasks.

The differentiation is not "better task management" — it's **workflow intelligence for a specific process**.

### ⚠️ Important Correction #4: Pilot Is Already Running

The proposal scopes "Pilot Infrastructure & Rollout" (Card 15) as a consulting track. But:

- 5 real projects are already live in the system (XT-500, RV-900, AF-400, CM-200, BK-350)
- SL500EUUK was just imported with 39 tasks auto-decomposed from an MS Project PDF
- The "pilot" is happening now, solo, without an IT counterpart or a named team

The question isn't "how to set up a pilot" — it's "how to scale what's already working."

### ⚠️ Important Correction #5: Solo Builder Reality

The proposal assumes there will be:
- An IT counterpart (Prerequisite #1)
- A named pilot team and PM contact (Prerequisite #2)
- Someone owning the "No Excel" mandate (Prerequisite #6)

The reality: **one person (Sun Sun) is building, maintaining, and piloting AutoPM alone.** No IT resources. No dedicated pilot team. No mandate enforcement owner. Any proposal must account for this constraint — or the proposal is for a different company.

---

## Part 3: Answers to Open Questions

### Q1: "The deck cites 1,500+ projects; the prototype shows 23. Which number is the operational scope?"

**Answer:** The current system has **2,200+ projects** loaded (from real Ninja project data). The "23" figure is outdated — that was the state of an earlier demo. The pilot scope for Color Refresh is ~20 projects, but the historical data available for pattern mining is the full 2,200+.

### Q2: "Which category does Color Refresh map to in the prototype's classification?"

**Answer:** Color Refresh maps to **"Extension"** in our classification. These are existing products getting new color variants, which follow a compressed 4-gate process (KO → EB0 → DQTP → MP) rather than the full 6-gate NPD flow.

### Q3: "Are the recommendations in the prototype's Recommended Actions panel LLM-generated or heuristic?"

**Answer:** Currently **heuristic** — rule-based patterns tied to project status and gate positions. Example: if a project is At Risk at G3, the action recommends checking DQTP timeline. This is deliberately not LLM-generated yet because the cost/benefit of LLM for this specific surface hasn't been validated.

### Q4: "Is the workflow editor at /workflow.html a PM-facing configuration surface or a read-only viewer?"

**Answer:** **Both.** It currently renders the gate flowchart for the selected project (read-only visualization of KO → Concept → ... → MP with task bars per gate). The configuration layer is the JSON model behind it, which Sunny maintains. Making it PM-editable is on the roadmap but not yet built.

### Q5: "Are the four target dimensions on slide 10 operational acceptance criteria or directional priorities?"

**Answer:** **Directional priorities.** They describe where AutoPM should drive improvement, not pass/fail tests. The three measurable targets are:
- Information latency: 2 hours → 2 minutes
- Delay detection: 3 days late → same day
- Weekly meeting: 30 min → 5 min

### Q6: "What is the LLM provider posture?"

**Answer:** Under discussion. China data residency requires either Aliyun Qwen or Azure OpenAI on a China region. The current prototype uses Coze (ByteDance) for AI features. Final decision depends on the IT architecture conversation.

### Q7: "Where does the platform run?"

**Answer:** Currently on **Render** (US) with **Neon PostgreSQL** (Singapore) for data. For production with China data residency, we would need Aliyun or Tencent Cloud. This is a key decision point for the IT architecture conversation.

### Q8: "What is the email substrate?"

**Answer:** Mix of **Exchange/O365** (US/UK teams) and **Lark/Feishu** (China teams). Not a single system. Any email connector would need to handle both.

### Q9: "What is the identity/SSO posture?"

**Answer:** Currently basic username/password auth. No SSO. SharkNinja uses Azure AD for corporate systems and Lark for China. SSO integration is needed but not yet implemented — gated on the IT architecture conversation.

### Q10: "Which historical projects are available for ingestion, and in what format?"

**Answer:** 2,200+ projects are already in the system in structured format (PostgreSQL: projects, milestones, tasks, blockers, risks). Gate-level event data exists for the 5 real projects. For the broader 2,200, the data is at project-level (status, phase, department, priority) but not at task-level granularity. Deeper historical data would need to be extracted from email, Excel gate sheets, and PLM folders.

### Q11: "How are PM decisions recorded today?"

**Answer:** **They're not systematically recorded.** Decisions live across email threads, WeChat/Lark messages, meeting notes, and sometimes in the ECN document itself. There is no canonical surface for decisions. This is one of the core problems AutoPM aims to solve — making decisions visible and traceable.

### Q12: "For the 1,500+ historical projects, what is accessible programmatically?"

**Answer:** The 2,200+ projects currently in AutoPM were imported via structured CSV → database. For deeper data (gate timing, decision records, blocker history), the sources would be:
- **Programmatically accessible**: Nothing currently. No API access to email, PLM, or gate sheets.
- **Semi-structured**: Excel gate sheets (per project, maintained by PMs, inconsistent format).
- **Effectively lost**: Decisions made in WeChat/Lark chats with no written record.

---

## Part 4: Recommended Reply Strategy

### Tone
- Appreciative but grounded. Ufuk did good work; acknowledge it.
- Direct about corrections. Don't let wrong assumptions propagate.
- Realistic about constraints. One person, no IT resources, no mandate enforcement.
- Clear about what AutoPM already is vs. what it needs.

### Key Messages
1. **AutoPM is further along than the proposal assumes** — it's a working system, not a prototype.
2. **The "no existing PM tool" reality changes everything** — there's nothing to integrate with; AutoPM IS the system.
3. **The foundation already exists** — Cards 01-05 are largely already built. Let's focus on Cards 06-10 (the intelligence layer) where the real gap is.
4. **Pilot is already running** — we need scaling help, not pilot setup.
5. **We can answer most open questions now** — and the remaining ones need the IT architecture call, which we should schedule.

### What to Push Back On
- The "Knowledge Graph Substrate" as a separate build — the data model already exists.
- The implication that AutoPM needs to be rebuilt — it needs to be extended, not replaced.
- The "Notion/Linear does this" framing — they don't, for this specific workflow.
- Pricing opacity — every card saying "scoped together in our next call" means we can't evaluate ROI.

### What to Accept
- The 3-layer spine (Collection → Trend → Optimization) is right.
- The feature catalogue structure is useful for prioritization.
- The open questions are legitimate and need answers.
- The IT architecture call is the critical next step.

---

## Part 5: Draft Email Reply

> **Subject:** Re: AutoPM AI – SharkNinja second brain

Hi Ufuk,

Thanks for putting this together — the structure is clear and the feature catalogue is a useful framework for prioritization. I've walked through the full document and have comments in three categories: confirmations, corrections, and answers to the open questions.

**What you got right:**
- The 7 problem statements are accurate — no corrections on framing.
- The 3-layer spine (Collection → Trend Analysis → Optimization) maps well to where AutoPM is and where it needs to go.
- The "sit on top of existing systems" principle is correct as a design constraint.

**Key corrections:**

1. **SharkNinja has no PM tool.** The proposal assumes integration with existing project management systems, but there are none. No Jira, no Feishu PM, no Asana. AutoPM is not sitting on top of another system — it IS the system. PLM is just file folders with no structured data. This changes the scope of the "Integration" layer entirely.

2. **AutoPM is further along than the proposal assumes.** It's at v17.6 with a working 4-layer architecture, 2,200+ projects on PostgreSQL, task CRUD, blocker detection, gate flowcharts, AI contextual hints, and PDF-to-tasks auto-decomposition. Cards 01-05 (the foundation) largely already exist. The real gap is in Cards 06-10 — the intelligence and insight layer.

3. **The pilot is already running.** Five real projects are live (XT-500, RV-900, AF-400, CM-200, BK-350), and I just imported SL500EUUK with 39 auto-decomposed tasks from an MS Project PDF. We need scaling help, not pilot setup.

4. **The "Notion/Linear does this" framing misses the differentiation.** Those are generic PM tools. AutoPM is purpose-built for our 6-gate NPI process with Shark/Ninja dual-brand structure. No generic tool produces gate-level bottleneck insights.

**Answers to open questions:**

- Q1: The system has 2,200+ projects loaded. The "23" figure is outdated. Pilot scope is ~20 Color Refresh projects; historical data is the full 2,200+.
- Q2: Color Refresh maps to "Extension" in our classification.
- Q3: Currently heuristic (rule-based), not LLM-generated.
- Q4: The workflow editor is both — read-only visualization now, PM-editable on the roadmap.
- Q5: Directional priorities, not acceptance criteria. Three measurable targets: info latency 2h→2min, delay detection 3d→same day, weekly meeting 30min→5min.
- Q6-Q9: These all depend on the IT architecture conversation. Current state: Render+Neon, basic auth, no SSO, mixed Exchange/Lark email.
- Q10: 2,200+ projects in structured format at project level; task-level data exists for 5 real projects. Deeper history needs extraction from email/Excel/PLM.
- Q11: PM decisions are not systematically recorded today — they live across email, WeChat/Lark, and meetings. This is one of the core problems.
- Q12: Nothing is programmatically accessible today. Excel gate sheets are semi-structured. Chat-based decisions are effectively lost.

**On next steps:** I agree the IT architecture conversation is the critical one. I'll flag that we need to get Matthieu to introduce the IT lead so we can resolve Q6-Q9 and move from discovery to scoping. In the meantime, I'd suggest we focus the next conversation on Cards 06-10 (the intelligence layer) since that's where the real value-add and the real gap is.

Happy to walk through the live system anytime — it's more persuasive than the proposal deck.

Best,  
Sun Sun
