# Open Source Community How-To

New to open source? This guide explains how to operate csv2ddl as a welcoming, sustainable project.

## 1. Define a Clear Value Proposition
- **What it does:** csv2ddl converts tabular data into CREATE TABLE statements with type inference.
- **Who it serves:** data engineers, analysts, and partners onboarding datasets into warehouses.
- Reiterate this everywhere (README, roadmap) so potential contributors grasp the mission quickly.

## 2. Maintain Transparent Documentation
- Keep `README.md`, `ROADMAP.md`, and `TODO.md` current.
- Document workflow decisions (coding standards, release cadence) to reduce guesswork.
- Link to architecture/design docs for newcomers seeking depth.

## 3. Set Contribution Expectations
- Use `.github/ISSUE_TEMPLATE` to guide bug reports and feature requests.
- Provide a pull request template so changes include context, tests, and expected output.
- Publish a `CONTRIBUTING.md` later that references coding style, branching strategy, and review SLAs.

## 4. Engage Respectfully and Promptly
- Respond to issues/PRs within a couple of days—even a quick “Thanks, I’ll review soon” helps community health.
- When providing feedback, be specific and courteous. Offer examples or snippets rather than vague critiques.
- Assume positive intent; most contributors just want to help.

## 5. Curate the Backlog
- Use `TODO.md` to track sprint plans, but summarize top priorities in GitHub issues too.
- Tag “good first issue” or “help wanted” once tasks are well-scoped for outside contributors.
- Close issues with a short explanation when work is done or plans change.

## 6. Automate Quality Checks
- Keep CI (GitHub Actions) green; broken builds discourage contributors.
- Run tests locally before pushing. If CI fails, fix or comment on the root cause.
- Consider adding linting (ruff/flake8) or formatting (black) once the project grows.

## 7. Celebrate and Document Releases
- Tag releases (`git tag v0.x.y`) once meaningful milestones land.
- Draft release notes highlighting new features, fixes, and contributors to recognize their work.
- Share updates via README badges or Discussions to keep momentum.

## 8. Be Security-Conscious
- Avoid committing secrets or proprietary datasets. Sanitize sample data.
- Review dependencies periodically for vulnerabilities.
- Document how users should report security issues privately if needed.

## 9. Grow Responsibly
- Invite collaboration but retain review authority. Don’t feel pressured to accept every change.
- If the project gains traction, recruit co-maintainers to share triage, code reviews, and releases.
- Periodically revisit the roadmap to reflect community feedback and your capacity.

## 10. Keep Learning
- Observe how mature projects manage workflows (e.g., pandas, FastAPI).
- Participate in open-source communities to gain perspective on governance and community-building.
- Iterate on processes—openness and adaptability are core to successful open source.

Open source is as much about people as code. Stay communicative, organized, and enthusiastic; contributors will follow your lead.
