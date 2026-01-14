#!/usr/bin/env python3
"""
Process downloaded ToxValDB Excel files into parquet format.
Combines all source Excel files into a single parquet.
"""
import json
from pathlib import Path

import pandas as pd

def get_version_info():
    """Read version info."""
    version_file = Path("download/version.json")
    if version_file.exists():
        with open(version_file) as f:
            return json.load(f)
    return {"toxvaldb_version": "unknown"}

def process_excel_files(excel_dir, output_path):
    """Combine Excel files into single parquet."""
    print(f"Processing Excel files from: {excel_dir}")

    excel_files = sorted(Path(excel_dir).glob("*.xlsx"))
    if not excel_files:
        print("  ERROR: No Excel files found!")
        return False

    print(f"  Found {len(excel_files)} Excel files")

    all_dfs = []
    total_records = 0

    for i, excel_file in enumerate(excel_files, 1):
        try:
            # Extract source name from filename
            # e.g., toxval_all_res_toxval_v97_0_IRIS.xlsx -> IRIS
            source_name = excel_file.stem.split("_")[-1]

            df = pd.read_excel(excel_file)
            record_count = len(df)
            total_records += record_count

            # Add source column if not present
            if '_source' not in df.columns and 'source' not in df.columns:
                df['_source_file'] = source_name

            all_dfs.append(df)
            print(f"    [{i}/{len(excel_files)}] {source_name}: {record_count:,} records")

        except Exception as e:
            print(f"    [{i}/{len(excel_files)}] Warning: Could not read {excel_file.name}: {e}")

    if not all_dfs:
        print("  ERROR: No data loaded from Excel files!")
        return False

    # Combine all dataframes
    print(f"\n  Combining {len(all_dfs)} sources...")
    combined = pd.concat(all_dfs, ignore_index=True)

    # Convert object columns to string for parquet compatibility
    for col in combined.select_dtypes(include=['object']).columns:
        combined[col] = combined[col].astype(str)

    combined.to_parquet(output_path, index=False)
    print(f"\n  SUCCESS: Combined {total_records:,} records from {len(all_dfs)} sources")
    print(f"  Saved to {output_path}")
    return True

def main():
    download_dir = Path("download")
    brick_dir = Path("brick")
    brick_dir.mkdir(exist_ok=True)

    output_path = brick_dir / "toxvaldb.parquet"

    # Get version info
    version_info = get_version_info()
    version = version_info.get("toxvaldb_version", "unknown")
    print(f"Processing ToxValDB {version}")
    print("=" * 50)

    # Process Excel files
    excel_dir = download_dir / "excel"
    if excel_dir.exists():
        success = process_excel_files(excel_dir, output_path)
    else:
        print(f"ERROR: Excel directory not found: {excel_dir}")
        success = False

    if success:
        # Save version metadata alongside parquet
        version_meta = brick_dir / "version.json"
        with open(version_meta, 'w') as f:
            json.dump(version_info, f, indent=2)

        # Print summary
        print("\n" + "=" * 50)
        print("Processing complete!")
        print(f"  Output: {output_path}")
        print(f"  Version: {version}")

        # Verify output
        df = pd.read_parquet(output_path)
        print(f"  Records: {len(df):,}")
        print(f"  Columns: {len(df.columns)}")
    else:
        print("\nERROR: Processing failed!")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
