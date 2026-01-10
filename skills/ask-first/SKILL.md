---
name: ask-first
description: >
  REQUIRED first step for: data analysis, queries, metrics, dashboards, reports, features, tools.
  Triggers on: "analyze", "query", "build", "create", "how many", "show me", "investigate", "understand", "decay", "cohort", "trend", "compare".
  Conducts requirements interview and writes project_spec.md before any implementation.
  After interview complete, routes to data-analysis, mysql, redshift, or other skills.
---

# Ask First

Conduct an in-depth interview with the user to gather comprehensive requirements before any implementation work. Start by asking clarifying questions. Probe deeply into:

- Technical implementation details (e.g., architecture choices, scalability considerations, integration points).
- UI & UX elements (e.g., user flows, accessibility features, edge case handling in interfaces).
- Concerns and risks (e.g., potential failure modes, security vulnerabilities, compliance issues).
- Tradeoffs (e.g., performance vs. cost, simplicity vs. flexibility, short-term vs. long-term implications).
- Any other relevant areas like timelines, stakeholders, metrics for success, or constraints.


Ask insightful questions that uncover nuances and hidden requirements. Instead of "What do you want?", ask "What specific performance benchmarks must the system meet under peak load, and how should it degrade gracefully if those are exceeded?"

Use the AskUserQuestionTool to follow up on responses, ask for elaborations, and explore related topics. Continue until you have a complete understanding or the user confirms requirements gathering is done.

Once the interview is complete, write a detailed specification to `project_spec.md` with sections: Overview, Requirements, Technical Details, UI/UX, Risks & Tradeoffs, and Next Steps.

If the task evolves or new aspects emerge later, restart the interviewing process.
