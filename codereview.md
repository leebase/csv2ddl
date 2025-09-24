# Code Review – Security & Development Best Practices

This assessment highlights risks and improvement opportunities discovered while reviewing the current codebase. Address the findings in priority order and keep this checklist for future audits.

## Security Findings

1. **Missing Bounds on Type Inference Sampling**  
   - *Files*: `type_inference.py`  
   - *Risk*: Sampling logic trusts the requested row count blindly. Large files or crafted inputs could trigger excessive memory usage.  
   - *Recommendation*: Clamp `sample_size` to a sensible maximum and stream data in chunks where practical. Document the limit.

2. **Unvalidated CLI Output Paths**  
   - *Files*: `csv2ddl.py`  
   - *Risk*: Passing `--output` with a path traversal sequence (e.g., `../../somefile`) writes outside the project directory.  
   - *Recommendation*: Resolve paths with `Path(...).resolve()` and warn when writing outside CWD unless explicitly allowed.

3. **Limited Reserved Keyword List**  
   - *Files*: `ddl_generator.py`  
   - *Risk*: The hard-coded keyword set does not account for dialect-specific lists or future SQL standards.  
   - *Recommendation*: Move reserved words into per-dialect registries or load from canonical lists; add tests covering known problem identifiers per dialect.

4. **No Guardrails for Excel Sheets or Column Counts**  
   - *Files*: `file_reader.py`  
   - *Risk*: Malicious spreadsheets with thousands of columns may degrade performance or trigger DDL explosion.  
   - *Recommendation*: Add a configurable maximum column count and emit warnings when exceeded.

5. **Packaging Meta Includes Test Dependencies by Default**  
   - *Files*: `requirements.txt`, `pyproject.toml`  
   - *Risk*: Shipping `pytest` and `ruff` as mandatory dependencies increases the attack surface for end users.  
   - *Recommendation*: Move dev/test tooling into extras (`pip install .[dev]`) and keep runtime requirements lean.

## Development Best Practices

1. **Lack of Linting in CI**  
   - *Files*: `.github/workflows/ci.yml`  
   - *Issue*: CI runs tests but not `ruff`. Manual enforcement is easy to forget.  
   - *Action*: Add a `ruff check .` step before `pytest`.

2. **CLI Command Uses `print` for Errors**  
   - *Files*: `csv2ddl.py`  
   - *Issue*: Mixing stdout/stderr makes scripting harder; return codes and logging should be clearer.  
   - *Action*: Adopt `logging` with level-aware messages and ensure non-zero `sys.exit` paths always go through `stderr`.

3. **Static Reserved Word Suffixing**  
   - *Files*: `ddl_generator.py`  
   - *Issue*: Suffix decisions (`_dt`, `_col`) are hard-coded and might surprise maintainers adding new dialects.  
   - *Action*: Provide a configuration layer or strategy interface so dialects can choose alternative suffixes or quoting rules.

4. **Docs Reference Placeholder URLs**  
   - *Files*: `README.md`, `GITHUB.md`  
   - *Issue*: `OWNER/REPO` placeholders may linger post-publish, leading to broken badges or instructions.  
   - *Action*: Track a post-publish task to replace placeholders and run `README` link checks periodically.

5. **Sampling and Type Detection Lack Logging Hooks**  
   - *Files*: `type_inference.py`, `csv2ddl.py`  
   - *Issue*: Debugging inference mismatches requires adding print statements manually.  
   - *Action*: Use `logging` and expose a verbosity flag (`--verbose`) to aid troubleshooting without code changes.

## Suggested Follow-Up Process

1. Create GitHub issues for each open recommendation using the provided templates.
2. Prioritize fixes by severity and effort; align with your next sprint plan.
3. Add regression tests or integration tests when addressing security-sensitive items.
4. Update documentation (README, HOWTO) after implementing policy or process changes.
5. Re-run this audit periodically or after major architectural changes.

Use this document as a living checklist—update it as issues are resolved or new risks emerge.
