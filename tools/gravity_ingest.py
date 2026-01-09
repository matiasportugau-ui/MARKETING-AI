import pandas as pd
import json
import os
import glob
from datetime import datetime

# CONFIG
INPUT_DIR = "../inputs"
OUTPUT_DIR = "../outputs"
OUTPUT_FILE = "context_snapshot.json"


def detect_platform(df):
    cols = set(df.columns)
    if "Ad name" in cols or "Ad set name" in cols or "Frequency" in cols:
        return "Meta Ads"
    if "Campaign" in cols or "Ad group" in cols or "Search keyword" in cols:
        return "Google Ads"
    return "Unknown"


def clean_currency(value):
    if isinstance(value, str):
        return float(value.replace("$", "").replace(",", ""))
    return value


def ingest_data():
    snapshot = {
        "generated_at": datetime.now().isoformat(),
        "platforms": {},
        "alerts": [],
    }

    csv_files = glob.glob(os.path.join(INPUT_DIR, "*.csv"))

    if not csv_files:
        print("No CSV files found in inputs/")
        return

    for file_path in csv_files:
        try:
            filename = os.path.basename(file_path)
            # Read CSV (try common encodings)
            try:
                df = pd.read_csv(file_path, encoding="utf-8")
            except:
                df = pd.read_csv(file_path, encoding="latin1")

            platform = detect_platform(df)

            # Basic scrubbing
            # Assuming standard export columns - modify based on actual client exports
            # This is a robust framework, likely needs specific column mapping adjustment

            summary = {
                "source_file": filename,
                "rows_processed": len(df),
                "total_spend": 0,
                "total_conversions": 0,
            }

            # Attempt to sum spend/conversions if columns exist
            for col in df.columns:
                lower_col = col.lower()
                if (
                    "spend" in lower_col
                    or "cost" in lower_col
                    or "amount spent" in lower_col
                ):
                    try:
                        summary["total_spend"] += df[col].apply(clean_currency).sum()
                    except:
                        pass

                if (
                    "conversion" in lower_col
                    and "rate" not in lower_col
                    and "cost" not in lower_col
                ):
                    try:
                        summary["total_conversions"] += pd.to_numeric(
                            df[col], errors="coerce"
                        ).sum()
                    except:
                        pass

            snapshot["platforms"][platform] = summary
            print(f"Processed {filename} detected as {platform}")

        except Exception as e:
            snapshot["alerts"].append(f"Failed to process {filename}: {str(e)}")

    return snapshot


def fetch_from_api_mock(snapshot):
    # This function would be replaced by real calls similar to test_connections.py
    # For V1, we will trust the test_connections.py to validate, and this logic needs to be fully implemented
    # once the user confirms credentials are working.
    print(
        "API Fetching enabled... (Mocking for now until credentials verified in test_connections.py)"
    )
    snapshot["alerts"].append(
        "API Fetching Attempted - See test_connections.py for real status."
    )
    return snapshot


def ingest_data():
    from dotenv import load_dotenv

    load_dotenv()

    snapshot = {
        "generated_at": datetime.now().isoformat(),
        "platforms": {},
        "alerts": [],
    }

    if os.getenv("USE_API") == "true":
        snapshot = fetch_from_api_mock(snapshot)

    # ALWAYS check generic CSVs as fallback or supplement
    csv_files = glob.glob(os.path.join(INPUT_DIR, "*.csv"))

    if not csv_files and os.getenv("USE_API") != "true":
        print("No CSV files found in inputs/ and USE_API!=true")
        return

    for file_path in csv_files:
        try:
            filename = os.path.basename(file_path)
            # Read CSV (try common encodings)
            try:
                df = pd.read_csv(file_path, encoding="utf-8")
            except:
                df = pd.read_csv(file_path, encoding="latin1")

            platform = detect_platform(df)

            # Basic scrubbing
            summary = {
                "source_file": filename,
                "rows_processed": len(df),
                "total_spend": 0,
                "total_conversions": 0,
            }

            # Attempt to sum spend/conversions if columns exist
            for col in df.columns:
                lower_col = col.lower()
                if (
                    "spend" in lower_col
                    or "cost" in lower_col
                    or "amount spent" in lower_col
                ):
                    try:
                        summary["total_spend"] += df[col].apply(clean_currency).sum()
                    except:
                        pass

                if (
                    "conversion" in lower_col
                    and "rate" not in lower_col
                    and "cost" not in lower_col
                ):
                    try:
                        summary["total_conversions"] += pd.to_numeric(
                            df[col], errors="coerce"
                        ).sum()
                    except:
                        pass

            snapshot["platforms"][platform] = summary
            print(f"Processed {filename} detected as {platform}")

        except Exception as e:
            snapshot["alerts"].append(f"Failed to process {filename}: {str(e)}")
