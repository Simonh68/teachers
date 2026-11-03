# Shared GitHub work routing — 2026-11-03

This file is the cross-project routing reference for ChatGPT work. It is a convention, NOT an access-control mechanism.

| User-declared conversation scope | Repository | Working branch | Owned paths |
|---|---|---|---|
| Grade 7 / כיתה ז | Simonh68/teachers | classroom/grade7 | grade7/** |
| Grade 8 / כיתה ח | Simonh68/teachers | classroom/grade8 | grade8/** |
| Grade 9 / כיתה ט | Simonh68/teachers | classroom/grade9 | grade9/** |
| Grade 10 / כיתה י | Simonh68/teachers | classroom/grade10 | grade10/** |
| Grade 11 / כיתה יא | Simonh68/teachers | classroom/grade11 | grade11/** |
| Grade 12 / כיתה יב | Simonh68/teachers | classroom/grade12 | grade12/** |
| English for Noar site | Simonh68/english-for-noar-home | work/english-for-noar | site application excluding reports |
| Usage reports / דוחות שימוש | Simonh68/english-for-noar-home | work/usage-reports | reports and usage analytics |
| Exams tracking / מבחנים ומעקב | Simonh68/teachers | work/exams-tracking | tooling only; no student personal data |

Rules:
1. The first explicit user scope in a conversation selects its repository and branch. Never infer a different branch from the current Git checkout.
2. Read this mapping and verify the actual target branch before each write. Never commit or push to main from a classroom task.
3. Do not change another scope's files. Shared files (root index.html, shared/, global Actions, common app configuration) require a separate coordinated integration change.
4. Build jobs must not push to main; use scope-specific branches or artifacts. Existing workflows may still violate this rule until migrated.
5. Publication is a separate artifact assembly and deployment step; do not merge work branches into main.
6. Report repository, branch, commit SHA and deployment status distinctly. A branch commit is NOT proof of live publication.
7. Do not put scanned exams, student names, grades or other sensitive records into a public repository.
8. This document does not enforce permissions; GitHub rulesets, required checks, and restricted credentials are needed for technical guarantees.


## Mandatory publishing architecture — independent branch artifacts (2026-11-03)

Chosen architecture: **option 3, assemble and publish validated outputs from independent branches without merging work branches into main**.

- Each of the nine scopes commits and builds only on its assigned work branch. A classroom build MUST NOT push to main.
- A central publisher retrieves pinned, verified revisions/artifacts from approved scope branches and assembles the public site(s) in an isolated workspace. It must not merge branch histories into main.
- Keep the existing Teachers site and English for Noar site at their current addresses; they are separate existing deployments, not one merged repository.
- Publish a single atomic artifact per existing site. Serialize deployment for each site, not builds across scopes. A failed scope build must not block other scopes' development.
- Scope outputs must have explicit ownership; shared homepage/navigation and QR components must be assembled by the publisher, not edited concurrently by class jobs.
- Preserve the last known good deployment on failed build/validation. Pin artifact versions, validate cross-links, and avoid duplicating analytics or Firebase writes in QA.
- A work-branch commit is NOT a live publication. Report branch, commit, artifact/build status, and actual deployed revision.
- Existing legacy workflows that push to main remain unsafe until migrated. Do NOT claim this architecture is operational until the deployment workflow is installed, tested, and the Pages/source settings verified.
- No student personal data in public repositories or public build artifacts.

This section supersedes any earlier instruction that requires merging each classroom change into main to publish.
