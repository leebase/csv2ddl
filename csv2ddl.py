#!/usr/bin/env python3
"""
CSV/Excel to SQL DDL Converter

Converts CSV and Excel files to SQL DDL statements for various databases.
"""

import argparse
import logging
import sys
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

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable debug logging output for troubleshooting'
    )

    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(levelname)s: %(message)s',
        force=True
    )
    logger = logging.getLogger(__name__)

    try:
        target_path = Path(args.file_path).expanduser()

        # Validate file exists
        if not target_path.exists():
            logger.error("File '%s' not found", target_path)
            sys.exit(1)

        # Determine table name
        if args.table_name:
            table_name = args.table_name
        else:
            # Use filename without extension
            table_name = target_path.stem

        # Read file
        logger.info("Reading file: %s", target_path)
        df = FileReader.read_file(
            file_path=str(target_path),
            delimiter=args.delimiter,
            encoding=args.encoding,
            sheet_name=args.sheet_name,
            sample_size=args.sample_size,
            max_columns=args.max_columns
        )

        if df.empty:
            logger.error("File is empty or no data found")
            sys.exit(1)

        logger.info("Loaded %s rows, %s columns", len(df), len(df.columns))

        # Infer types
        logger.debug("Inferring data types")
        inferrer = TypeInferrer()
        type_info = inferrer.infer_types(df)

        # Map to dialect
        logger.debug("Mapping to %s dialect", args.dialect)
        mapper = DialectMapper(args.dialect)
        column_types = mapper.map_column_types(type_info)

        # Generate DDL
        logger.debug("Generating DDL")
        generator = DDLGenerator(args.dialect)
        ddl = generator.generate_ddl(table_name, column_types)

        # Output
        if args.output:
            output_path = Path(args.output).expanduser()
            resolved_output = output_path.resolve()
            cwd = Path.cwd().resolve()

            if not args.allow_outside_output and not str(resolved_output).startswith(str(cwd)):
                logger.error(
                    "Refusing to write outside the working directory (%s). "
                    "Use --allow-outside-output to override.",
                    resolved_output
                )
                sys.exit(1)

            resolved_output.parent.mkdir(parents=True, exist_ok=True)
            with open(resolved_output, 'w', encoding='utf-8') as f:
                f.write(ddl)
            logger.info("DDL written to: %s", resolved_output)
        else:
            logger.debug("Writing DDL to stdout")
            print(ddl)

    except Exception as e:
        if logger.isEnabledFor(logging.DEBUG):
            logger.exception("Unhandled error")
        else:
            logger.error("Error: %s", e)
        sys.exit(1)


if __name__ == '__main__':
    main()
