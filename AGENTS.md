# AutoPM development coordination

Codex is the lead maintainer and coordinator. It defines scope, assigns work, reviews evidence, integrates changes and maintains GitHub Issues. DuMate, Qoder and other assistants execute explicitly assigned work.

Start with [the collaboration guide](collaboration/使用分工指南.md) and [current decisions](collaboration/README.md). Read the assigned Issue before changing files. Historical planning is context, not permission to implement superseded designs.

- One task ID, one responsible executor, one isolated branch or work directory.
- Do not modify another worker's files or overwrite uncommitted work.
- Remote assistants use repository-relative paths, Issue comments and PRs; Windows drive paths are source references only.
- Deliver actual changes, checks, version and remaining gaps. Codex verifies before accepting or closing work.
- Preserve the existing Task completion behavior and the pause on project progress redesign.
- GitHub development Issues, Airtable project Tasks and business Issues/Issue Actions have distinct purposes.
- No credentials in files or Issues. Do not modify production, send external messages, change access, merge or deploy beyond the assigned scope.
- Use the in-app browser when the user says browser, unless they explicitly specify another browser.

The application code predates this coordination setup. This change adds management documentation, not a new production release.
