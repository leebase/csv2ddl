# Dialect Roadmap

This document outlines planned database dialect support beyond the current Snowflake and SQLite targets. Contributions are welcome—open an issue or PR if you want to champion a dialect.

## Near-Term Targets

1. **PostgreSQL**
   - Rich type system (NUMERIC, TEXT, timestamptz) aligns well with current inference.
   - Primary work: map `TypeInferrer` outputs to PostgreSQL types and extend tests.

2. **MySQL / MariaDB**
   - Widely used; relies on VARCHAR, DECIMAL, DATE equivalents.
   - Address identifier quoting and reserved words (`backticks`).

## Future Considerations

- **BigQuery**
  - Requires explicit schema definitions but supports flexible data types.
  - Evaluate how sampling impacts column mode (NULLABLE vs REQUIRED).

- **Redshift**
  - Similar to PostgreSQL but with distribution and sort keys—consider optional metadata fields.

- **Snowflake Stored Procedure Integration**
  - Expose APIs tailored for Snowflake’s Python runtime.

## How to Contribute

1. Comment on an existing issue or open a new thread for the dialect you want to add.
2. Share sample CSV/Excel data that represents real-world edge cases for the dialect.
3. Outline the mapping rules and get feedback before implementation.
4. Implement, add tests, update docs, and submit a PR using the provided template.

## Community Feedback

We maintain discussion threads for roadmap feedback. Bring use cases, performance considerations, and tooling ideas to the GitHub Discussions board or issues.
