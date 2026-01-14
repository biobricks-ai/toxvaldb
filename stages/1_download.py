#!/usr/bin/env python3
"""
Download ToxValDB from EPA Clowder repository.
Fetches the latest version's SQL database dump.
"""
import json
import os
import re
import requests
from pathlib import Path

# Clowder API endpoints
CLOWDER_DATASET_ID = "61147fefe4b0856fdc65639b"
CLOWDER_FILES_API = f"https://clowder.edap-cluster.com/api/datasets/{CLOWDER_DATASET_ID}/files"

def get_version_info():
    """Read version info from the invalidation step."""
    version_file = Path("download/version.json")
    if version_file.exists():
        with open(version_file) as f:
            return json.load(f)
    return {"toxvaldb_version": "unknown"}

def find_toxval_files(files_list, version_pattern):
    """Find the main ToxValDB SQL files for the given version."""
    # Version format: v9.7.0 -> 97_0 for file matching
    version_num = version_pattern.replace("v", "").replace(".", "")  # "970"
    version_underscore = version_num[:-1] + "_" + version_num[-1]  # "97_0"

    sql_pattern = re.compile(rf"res_toxval_v{version_underscore}\.sql\.gz", re.IGNORECASE)
    source_pattern = re.compile(rf"res_toxval_source_v{version_underscore}\.sql\.gz", re.IGNORECASE)

    main_file = None
    source_file = None

    for f in files_list:
        filename = f.get("filename", "")
        if sql_pattern.match(filename):
            main_file = f
        elif source_pattern.match(filename):
            source_file = f

    return main_file, source_file

def find_excel_files(files_list, version_pattern):
    """Find individual source Excel files for the version."""
    # Version format: v9.7.0 -> 97_0 for file matching
    version_num = version_pattern.replace("v", "").replace(".", "")  # "970"
    version_underscore = version_num[:-1] + "_" + version_num[-1]  # "97_0"
    pattern = re.compile(rf"toxval_all_res_toxval_v{version_underscore}_.*\.xlsx", re.IGNORECASE)

    return [f for f in files_list if pattern.match(f.get("filename", ""))]

def download_file(file_info, output_dir):
    """Download a file from Clowder."""
    file_id = file_info["id"]
    filename = file_info["filename"]
    output_path = output_dir / filename

    url = f"https://clowder.edap-cluster.com/api/files/{file_id}"

    print(f"Downloading {filename} ({int(file_info.get('size', 0)) / 1024 / 1024:.1f} MB)...")

    response = requests.get(url, stream=True)
    response.raise_for_status()

    with open(output_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"  Saved to {output_path}")
    return output_path

def main():
    download_dir = Path("download")
    download_dir.mkdir(exist_ok=True)

    # Get version info
    version_info = get_version_info()
    version = version_info.get("toxvaldb_version", "v9.7.0")
    print(f"Downloading ToxValDB {version}")

    # Get file list from Clowder
    print("Fetching file list from Clowder...")
    response = requests.get(CLOWDER_FILES_API)
    response.raise_for_status()
    files = response.json()
    print(f"Found {len(files)} files in dataset")

    # Download Excel files (more reliable than SQL dump for processing)
    print("\nDownloading individual Excel files...")
    excel_files = find_excel_files(files, version)

    # Filter to only data files (not QC files)
    excel_files = [f for f in excel_files if not f.get("filename", "").startswith("qc_")]

    print(f"Found {len(excel_files)} Excel data files")

    if not excel_files:
        # Try alternative version patterns for debugging
        print("Warning: No Excel files found. Checking alternative patterns...")
        for f in files:
            if "v97_0" in f.get("filename", "") and "toxval_all" in f.get("filename", ""):
                print(f"  Found: {f['filename']}")

    excel_dir = download_dir / "excel"
    excel_dir.mkdir(exist_ok=True)

    for i, excel_file in enumerate(excel_files):
        print(f"[{i+1}/{len(excel_files)}] ", end="")
        download_file(excel_file, excel_dir)

    # Also download metadata files
    metadata_patterns = [
        "Data file column dictionary",
        "source_info",
        "source_count",
        "Release Notes"
    ]

    for f in files:
        filename = f.get("filename", "")
        for pattern in metadata_patterns:
            if pattern.lower() in filename.lower() and version.replace("v", "").replace(".", "_") in filename:
                try:
                    download_file(f, download_dir)
                except Exception as e:
                    print(f"  Warning: Could not download {filename}: {e}")
                break

    # Save manifest
    manifest = {
        "version": version,
        "files_downloaded": [f.name for f in download_dir.glob("*") if f.is_file()],
        "excel_files": [f.name for f in (download_dir / "excel").glob("*.xlsx")] if (download_dir / "excel").exists() else []
    }

    with open(download_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)

    print(f"\nDownload complete. Manifest saved to download/manifest.json")

if __name__ == "__main__":
    main()
