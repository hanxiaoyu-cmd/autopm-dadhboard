# AutoPM Vendor Assessment Summary

**To:** Jen | **Date:** 29 May 2026 | **By:** Sunny

---

## AutoPM Vision

Simplify processes, flatten the organisation, accelerate decisions, improve efficiency, full participation. From 50-user pilot to 2,000 users company-wide — transforming how SN runs NPI.

---

## Six-Dimension Assessment

| Dimension | Ody | Agileex | Critical Gap |
|-----------|-----|---------|--------------|
| D1 PM Domain & Product | ★★☆☆☆ | ★☆☆☆☆ | Neither understands PM — SN must own process design. Ody has room to build; Agileex cannot build what's needed |
| D2 Data Integration | ★★★★☆ | ★★☆☆☆ | Auto-ingestion vs manual entry — Ody breaks the wall, Agileex just moves the form online |
| D3 AI & Insight | ★★★★★ | ★☆☆☆☆ | Generational gap — Ody's 6 agents are the product core; Agileex just wraps an LLM |
| D4 Team & Delivery | ★★☆☆☆ | ★★★★☆ | Capable vendor can't deliver; deliverable vendor can't build what we need |
| D5 Security & Sovereignty | ★★★★☆ | ★★★☆☆ | Ody: data in our hands. Agileex: data in Microsoft's hands |
| D6 Scalability & Lock-in | ★★★☆☆ | ★★☆☆☆ | Ody may not survive but we keep the data. Agileex may hit a ceiling but we can't leave |
| **Overall** | **★★★☆☆** | **★★☆☆☆** | |

---

## Key Judgements

**1. Neither vendor understands project management.** Sunny's AutoPM prototype is the only thing in this programme with PM thinking. SN must own process design; the vendor is the builder, not the architect.

**2. Agileex's limits are clear.** It's a form-filling + BI tool within the Microsoft ecosystem — no PM capability, no AI understanding, no auto-ingestion. It can deliver a 4-week MVP, but the ceiling is definitive: it will not scale to what AutoPM requires, and migrating away is extremely costly.

**3. Ody's direction matches AutoPM closely, but most capabilities are unvalidated.** Auto-ingestion, contradiction detection, AI agents, custom model training — if real, this is exactly what we need. But if the claims don't hold up, we waste valuable pilot time.

**4. The core tension: short-term survival vs long-term success.** Agileex gets us a faster, safer pilot — but can't reach 2,000 users. Ody points in the right direction but carries significant risk. Choosing the wrong pilot path is far more costly than spending a few extra weeks validating Ody.

---

## Recommendation

| Step | Action | Output |
|------|--------|--------|
| This week | Prepare Ody capability validation checklist | Deep-dive question list for 2nd meeting |
| Within 2 weeks | Second Ody meeting — no presentations, demand specifics and real cases | Validation conclusions |
| Post-validation | Pass → Discovery Phase (LOI); Fail → evaluate alternatives | Decision |
| In parallel | Define PM process based on Sunny's prototype (required regardless of vendor) | PM process specification |
| Agileex | Not recommended as AutoPM primary vendor | Retain as Power BI fallback option |

---

## Alternatives (if Ody fails validation)

- **Build in-house:** Based on Sunny's prototype, form internal team + outsourced dev
- **Mature PM SaaS + integration:** Monday.com / Asana + integration partner for data pipes
- **Data platform first:** MuleSoft / Boomi to break data silos, then build application layer

---

*Sources: Ody meeting (28 May), IT Onboarding doc, Agileex meeting (29 May), Ufuk email*  
*⚠️ Most of Ody's capabilities are vendor-claimed and unvalidated in SN's environment*
