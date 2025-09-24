#!/usr/bin/env python3
"""
CSV/Excel to SQL DDL Converter

Converts CSV and Excel files to SQL DDL statements for various databases.
"""

import argparse
import sys
import os
from pathlib import Path

from file_reader import FileReader
from type_inference import TypeInferrer
from dialect_mapper import DialectMapper
from ddl_generator import DDLGenerator


def main():
    parser = argparse.ArgumentParser(
        description="Convert CSV/Excel files to SQL DDL",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python csv2ddl.py data.csv
  python csv2ddl.py --dialect sqlite data.xlsx --sheet-name Sheet1
  python csv2ddl.py --output schema.sql --table-name my_table data.csv
        """
    )

    parser.add_argument(
        'file_path',
        help='Path to CSV or Excel file'
    )

    parser.add_argument(
        '--dialect',
        choices=DialectMapper.get_supported_dialects(),
        default='snowflake',
        help='SQL dialect (default: snowflake)'
    )

    parser.add_argument(
        '--sample-size',
        type=int,
        default=1000,
        help='Number of rows to sample for type inference (default: 1000)'
    )

    parser.add_argument(
        '--output',
        help='Output file path (prints to stdout if not specified)'
    )

    parser.add_argument(
        '--allow-outside-output',
        action='store_true',
        help='Permit writing output files outside the current working directory'
    )

    parser.add_argument(
        '--table-name',
        help='Custom table name (uses filename if not specified)'
    )

    parser.add_argument(
        '--delimiter',
        default=',',
        help='CSV delimiter (default: ,)'
    )

    parser.add_argument(
        '--encoding',
        help='File encoding (auto-detected if not specified)'
    )

    parser.add_argument(
        '--sheet-name',
        help='Excel sheet name (uses first sheet if not specified)'
    )

    parser.add_argument(
        '--max-columns',
        type=int,
        help='Maximum allowed columns before aborting (default: 512)'
    )

    args = parser.parse_args()

    try:
        # Validate file exists
        if not os.path.exists(args.file_path):
            print(f"Error: File '{args.file_path}' not found", file=sys.stderr)
            sys.exit(1)

        # Determine table name
        if args.table_name:
            table_name = args.table_name
        else:
            # Use filename without extension
            table_name = Path(args.file_path).stem

        # Read file
        print(f"Reading file: {args.file_path}", file=sys.stderr)
        df = FileReader.read_file(
            file_path=args.file_path,
            delimiter=args.delimiter,
            encoding=args.encoding,
            sheet_name=args.sheet_name,
            sample_size=args.sample_size,
            max_columns=args.max_columns
        )

        if df.empty:
            print("Error: File is empty or no data found", file=sys.stderr)
            sys.exit(1)

        print(f"Loaded {len(df)} rows, {len(df.columns)} columns", file=sys.stderr)

        # Infer types
        print("Inferring data types...", file=sys.stderr)
        inferrer = TypeInferrer()
        type_info = inferrer.infer_types(df)

        # Map to dialect
        print(f"Mapping to {args.dialect} dialect...", file=sys.stderr)
        mapper = DialectMapper(args.dialect)
        column_types = mapper.map_column_types(type_info)

        # Generate DDL
        print("Generating DDL...", file=sys.stderr)
        generator = DDLGenerator(args.dialect)
        ddl = generator.generate_ddl(table_name, column_types)

        # Output
        if args.output:
            output_path = Path(args.output).expanduser()
            resolved_output = output_path.resolve()
            cwd = Path.cwd().resolve()

            if not args.allow_outside_output and not str(resolved_output).startswith(str(cwd)):
                print(
                    f"Error: Refusing to write outside the working directory ({resolved_output})."
                    " Use --allow-outside-output to override.",
                    file=sys.stderr
                )
                sys.exit(1)

            resolved_output.parent.mkdir(parents=True, exist_ok=True)
            with open(resolved_output, 'w', encoding='utf-8') as f:
                f.write(ddl)
            print(f"DDL written to: {resolved_output}", file=sys.stderr)
        else:
            print(ddl)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
