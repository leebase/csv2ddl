# CSV to Snowflake DDL Converter - Design Document

## Overview
This project aims to create a Python-based tool that analyzes CSV files and generates optimal Snowflake DDL (Data Definition Language) statements for creating tables. The tool infers data types from untyped CSV data, determining appropriate column types and sizes based on the actual data content.

## Requirements

### Functional Requirements
1. **File Input Processing**
   - Accept CSV or Excel file paths as input
   - Auto-detect file type based on extension (.csv, .xlsx)
   - Support standard CSV format with configurable delimiters
   - Support Excel files (.xlsx) with multiple sheets
   - Handle various encodings (UTF-8, ISO-8859-1, etc.)
   - Process headers as column names

2. **Data Type Inference**
   - **Date Recognition**: Identify date/datetime columns using common formats (YYYY-MM-DD, MM/DD/YYYY, etc.)
   - **Numeric Types**: Distinguish between integers and floats, determine precision and scale
   - **String Types**: Calculate optimal VARCHAR length based on maximum string length in data
   - **Null Handling**: Account for NULL values in type inference

3. **Extensible DDL Generation**
   - Generate CREATE TABLE statements for multiple SQL dialects
   - Initial support for Snowflake and SQLite
   - Map inferred types to appropriate dialect-specific data types:
     - Dates → DATE/TIMESTAMP (Snowflake), DATE/TEXT (SQLite)
     - Integers → NUMBER(precision, 0) (Snowflake), INTEGER (SQLite)
     - Floats → NUMBER(precision, scale) (Snowflake), REAL (SQLite)
     - Strings → VARCHAR(length) (Snowflake), TEXT (SQLite)
   - Include column names, types, and basic constraints
   - Pluggable dialect system for easy addition of new SQL databases

4. **Performance Considerations**
   - Sample data efficiently (e.g., first N rows or random sampling) with sane upper bounds
   - Handle large CSV files without loading entire file into memory
   - Provide configurable sampling parameters

### Non-Functional Requirements
1. **External Execution**: Run as standalone Python script without Snowflake connection
2. **Future Snowflake SP Compatibility**: Design to be easily adaptable for Snowflake Python stored procedures
3. **Error Handling**: Graceful handling of malformed CSV, encoding issues, and type inference failures
4. **Logging**: Provide informative output about type inference decisions

### Constraints
- Python-based implementation
- No external database connections required for core functionality
- Focus on common data types (dates, numbers, strings)
- Optimize for typical business data scenarios

## User Stories

### Primary User Story
As a data engineer, I want to quickly generate Snowflake DDL from CSV files so that I can create tables that match the data structure without manual type guessing.

### Secondary User Stories
- As a developer, I want the tool to handle various CSV formats and encodings so that I can process diverse data sources.
- As a Snowflake user, I want DDL that uses appropriate data types and sizes so that storage is optimized and queries perform well.
- As a system integrator, I want the tool to be easily callable from other systems so that it can be integrated into ETL pipelines.

## Features

### Core Features
   - Command-line interface for CSV or Excel (.xlsx) processing
   - Automatic type inference with configurable sampling (capped to prevent runaway memory use)
   - DDL output to console or file for supported dialects
   - Support for custom delimiters and encodings
   - Column count guardrails to protect downstream tooling

### Advanced Features (Future)
- Integration with Snowflake Python stored procedures
- Batch processing of multiple CSV files
- Custom type mapping rules
- Data profiling reports alongside DDL generation

## Assumptions
- CSV files have headers in the first row
- Data is relatively clean (not heavily corrupted)
- Common date formats are used
- Numeric data fits within Snowflake NUMBER type constraints
- String data is reasonable length (not exceeding VARCHAR limits)
