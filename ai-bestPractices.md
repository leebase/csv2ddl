# AI Collaboration Playbook for `csv2ddl`

This guide captures how the project lead currently runs AI-assisted development on the `csv2ddl` repository, along with opportunities to refine the workflow and an overall assessment of leadership practices.

## How the Tooling Is Used Today
- **AI as coding pair**: The AI agent receives structured tasks (e.g., “execute Sprint 2”, “implement column sanitization”), responds with plans, and performs edits through shell commands and patch applications. The user maintains final control—running `git status`, committing, and pushing once satisfied.
- **Sprint-driven cadence**: Work is broken into named sprints with explicit backlog items (`TODO.md`). The AI executes a sprint, updates documentation, and marks tasks complete, providing traceability for each iteration.
- **Repository hygiene**: The lead keeps supporting docs in sync (`README`, `architecture.md`, `GITHUB.md`, `OpenSourceCommunityHowTo.md`, `ai-bestPractices.md`) so changes are discoverable. Documentation is treated as a first-class deliverable.
- **Validation loop**: After AI edits, the lead runs `pytest`, `ruff`, or manual command checks locally—especially when the AI cannot install dependencies or push to remotes. This human-in-the-loop validation ensures production-quality changes.
- **Git workflow**: Commits originate from the lead’s laptop or designated “canonical” machine. The AI avoids final commits/pushes but keeps `codereview.md` updated, leaving an audit trail of remaining risks.

## Areas for Improvement
1. **Remote git coordination**
   - *Observation*: Nextcloud syncing without `.git/` caused divergent histories across machines. GitHub integration was added later, but remote pushes should happen immediately after each significant sprint.
   - *Recommendation*: Standardize on `git push origin main` from the canonical machine after reviewing AI changes. Consider a protected-branch workflow for future collaborators.

2. **Automated verification inside CI**
   - *Observation*: Tests and lint run locally, but CI still needs real pushes to execute. During AI-driven development, we rely on local validation only.
   - *Recommendation*: After each sprint, push to GitHub so the Actions workflow confirms cross-platform reproducibility. Failures in CI provide early warning before release.

3. **Decision log for AI instructions**
   - *Observation*: Sprint tasks are documented, yet the reasoning behind certain choices (e.g., dropping `.xls` support, setting sampling caps) lives in conversation history only.
   - *Recommendation*: Start an `DECISIONS.md` or expand `architecture.md` with dated entries capturing “what/why” for cross-team clarity.

4. **Access management & secrets**
   - *Observation*: AI currently manipulates code within a sandbox that can’t reach Git or the internet without manual help.
   - *Recommendation*: When the project scales, configure a dedicated service account for the AI with limited credentials (PAT or SSH deploy key) so it can verify remote pushes/tests in a controlled environment.

5. **Automated release pipeline**
   - *Observation*: Packaging work now exists, but releases remain manual.
   - *Recommendation*: Introduce a tagged-release workflow (GitHub Actions job that builds wheels/sdist, maybe uploads to TestPyPI) to align with packaging best practices when the code stabilizes.

## Evaluation of the Project Lead
- **Strengths**
  - *Structured orchestration*: The lead provides clear sprint boundaries and explicit acceptance criteria, enabling the AI to deliver coherent increments.
  - *Documentation-first mindset*: Every significant change comes with README/GITHUB/TODO updates, keeping contributors aligned.
  - *Safety awareness*: Security findings (sampling caps, output validation, reserved-word policies) were prioritized quickly and tracked through `codereview.md`.

- **Growth Opportunities**
  - *Automation after validation*: Integrate the canonical machine and GitHub pushes into the standard flow, so verified work is always mirrored in the remote repository.
  - *Delegation efficiency*: As the project grows, consider delegating some validation steps (e.g., automated tests, release tooling) to CI rather than performing all checks manually.

- **Overall Assessment**
  - The project lead demonstrates disciplined coordination of AI assistance, pairing human judgment with automated execution. Planning, documentation, and security considerations are handled thoughtfully. The remaining gaps (remote coordination, automated releases) are operational rather than strategic. With light process adjustments, this approach scales well for open-source collaboration.

Use this playbook when onboarding new contributors or expanding AI involvement—the goal is to preserve the deliberate, traceable workflow while continuing to automate repetitive pieces.
