# Project Planning

## Backlog
- [x] [T11] **High**: Sanitize all generated column names so they are database-safe (convert spaces/special characters to underscores, enforce valid prefixes).
- [x] [T1] Select an open-source license (MIT or Apache-2.0), add `LICENSE`, and update `README.md` references.
- [x] [T2] Decide `.xls` support scope; either add required dependency (`xlrd`) or drop the format from docs and validation.
- [x] [T3] Align documentation with code: update `architecture.md` and `README.md` to reflect actual modules and file locations.
- [x] [T4] Introduce a `tests/` package with pytest covering `FileReader`, `TypeInferrer`, and `DialectMapper` happy-path cases.
- [x] [T5] Add edge-case tests for mixed-type columns, encoding detection, and unsupported dialects to prevent regressions.
- [x] [T6] Provide packaging metadata (`pyproject.toml`) with console entry point `csv2ddl` and update install docs.
- [x] [T7] Configure CI (e.g., GitHub Actions) to run linting and pytest on pushes and pull requests.
- [x] [T8] Publish example-driven docs showing Snowflake vs SQLite outputs for the same dataset and note limitations.
- [x] [T9] Add contribution templates (ISSUE_TEMPLATE, PULL_REQUEST_TEMPLATE) to guide new contributors.
- [x] [T10] Create a roadmap for additional dialects and invite community feedback via Issues/Discussions.

## Sprint Roadmap

### Sprint 1 – Open Source Launchpad
- **Goal:** Make the repository legally distributable and trustworthy for newcomers.
- **Scope:** Complete [T1], [T2], and [T3].
- **Deliverable:** Licensed repo with accurate docs and confirmed Excel support stance; run `python csv2ddl.py sample_data.csv` to validate baseline functionality.

### Sprint 2 – Testable Foundations
- **Goal:** Ship a verifiable codebase with basic automated confidence.
- **Scope:** Complete [T4] and [T5].
- **Deliverable:** Passing `pytest` suite covering main inference paths; document test commands in `README.md`.

### Sprint 3 – Distribution Ready
- **Goal:** Package and automate delivery for wider usage.
- **Scope:** Complete [T6], [T7], and [T8].
- **Deliverable:** Installable package with CI badge and refreshed usage docs; verify by installing locally via `pip install .` and rerunning CLI.

### Sprint 4 – Community Enablement
- **Goal:** Prepare for external contributions and future roadmap work.
- **Scope:** Complete [T9] and [T10].
- **Deliverable:** Contributor workflow templates plus published roadmap capturing dialect priorities and community channels.

> When ready, say "execute sprint 1" to focus the team on the first slice of work.
