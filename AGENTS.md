# Repository Guidelines

## Project Structure & Module Organization
The CLI entry point `csv2ddl.py` orchestrates the conversion flow across helper modules dedicated to reading files, inferring types, translating dialects, and emitting DDL. Source modules live at the repository root; keep new modules co-located and importable without packages to preserve the current lightweight layout. Sample Excel inputs reside in `data/`, while existing `.sql` fixtures and documentation (`architecture.md`, `design.md`, `README.md`) stay in the root for quick cross-checking when extending features.

## Build, Test, and Development Commands
Work in Python 3.10+ with an isolated environment:
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
Run the converter with `python csv2ddl.py data/sample_data.csv --dialect snowflake` for stdout output, or add `--output schema.sql` to persist results. Use `--dialect sqlite` when validating type mappings across dialects. Execute `pytest` (after adding a `tests/` folder) to run automated checks before pushing changes.

## Coding Style & Naming Conventions
Follow PEP 8 with 4-space indentation, explicit imports, and descriptive function names (`verb_noun` for helpers, `PascalCase` for classes). Prefer type hints and docstrings mirroring existing modules to keep interfaces self-documenting. Use f-strings for formatted messages, and keep functions focused—extract helpers when logic exceeds roughly 40 lines.

## Testing Guidelines
Target `pytest` for unit coverage; mirror module names (`tests/test_type_inference.py`) and group scenarios with `TestClass` containers. Include representative CSV/Excel fixtures under `data/` or a new `tests/fixtures/` directory to exercise edge cases such as mixed numeric columns or non-UTF encodings. Aim to cover new inference branches and dialect mappings, and document gaps in the PR if coverage cannot reach critical paths.

## Commit & Pull Request Guidelines
Initialize a git repository if one is not yet present so history remains reviewable. Write imperative, concise commit subjects (e.g., `Add SQLite mapping for decimal types`) and include relevant context bodies when behavior changes. PRs should explain the workflow impact, reference any tickets, list testing commands executed, and attach sample DDL output when the change alters generated SQL.

## Data & Configuration Notes
Avoid committing proprietary spreadsheets—use sanitized examples similar to `sample_data.csv`. When introducing new dialects or configuration toggles, update `README.md` and provide a minimal usage example so agents can reproduce the scenario.
