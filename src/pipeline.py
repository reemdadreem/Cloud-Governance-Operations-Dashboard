"""Cloud Governance Operations Dashboard data pipeline.

This script:
1. Imports the raw governance pipeline file.
2. Cleans and standardizes the data.
3. Calculates aging.
4. Flags missing evidence and unapproved regions.
5. Assigns RAG health status.
6. Exports a leadership-ready dataset and KPI summary.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd


REQUIRED_COLUMNS = {
    "Use Case ID",
    "Owner",
    "Cloud Provider",
    "Current Stage",
    "Submission Date",
    "Missing Evidence",
    "Approved Region",
    "Actual Region",
    "Risk Level",
}


def normalize_text(series: pd.Series) -> pd.Series:
    """Trim whitespace and collapse repeated spaces."""
    return (
        series.fillna("")
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )


def title_case_owner(series: pd.Series) -> pd.Series:
    """Standardize owner names without changing initials."""
    return normalize_text(series).str.title()


def normalize_provider(series: pd.Series) -> pd.Series:
    """Normalize cloud-provider names."""
    mapping = {"azure": "Azure", "aws": "AWS", "gcp": "GCP"}
    cleaned = normalize_text(series).str.lower()
    return cleaned.map(mapping).fillna(cleaned.str.upper())


def calculate_health(row: pd.Series) -> str:
    """Assign Green, Yellow, or Red using simple governance rules."""
    if row["Current Stage"] == "Approved":
        return "Green"

    if (
        row["Region Compliance"] == "Non-Compliant"
        or row["Risk Level"] == "Critical"
        or row["Days in Stage"] > 90
    ):
        return "Red"

    if (
        row["Evidence Status"] == "Missing"
        or row["Risk Level"] == "High"
        or row["Days in Stage"] > 45
    ):
        return "Yellow"

    return "Green"


def build_pipeline(input_path: Path, output_dir: Path) -> tuple[Path, Path]:
    """Run the full transformation and export process."""
    output_dir.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(input_path)
    missing_columns = REQUIRED_COLUMNS.difference(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    # Clean core fields.
    df["Use Case ID"] = normalize_text(df["Use Case ID"]).str.upper()
    df["Owner"] = title_case_owner(df["Owner"])
    df["Cloud Provider"] = normalize_provider(df["Cloud Provider"])
    df["Current Stage"] = normalize_text(df["Current Stage"]).str.title()
    df["Actual Region"] = normalize_text(df["Actual Region"])
    df["Approved Region"] = normalize_text(df["Approved Region"])
    df["Risk Level"] = normalize_text(df["Risk Level"]).str.title()
    df["Missing Evidence"] = normalize_text(df["Missing Evidence"])

    # Remove duplicates and invalid IDs.
    df = df.drop_duplicates(subset=["Use Case ID"], keep="last")
    df = df[df["Use Case ID"].str.match(r"^CG-\d{4}$", na=False)].copy()

    # Date and aging logic.
    df["Submission Date"] = pd.to_datetime(df["Submission Date"], errors="coerce")
    df = df.dropna(subset=["Submission Date"]).copy()
    today = pd.Timestamp.today().normalize()
    df["Days in Stage"] = (today - df["Submission Date"]).dt.days.clip(lower=0)

    # Evidence and region validations.
    df["Evidence Status"] = df["Missing Evidence"].apply(
        lambda value: "Complete" if value == "" else "Missing"
    )
    df["Region Compliance"] = df.apply(
        lambda row: (
            "Compliant"
            if row["Actual Region"] in row["Approved Region"].split("|")
            else "Non-Compliant"
        ),
        axis=1,
    )

    # Health and escalation logic.
    df["Health Status"] = df.apply(calculate_health, axis=1)
    df["Escalation Required"] = df["Health Status"].eq("Red").map(
        {True: "Yes", False: "No"}
    )

    # Sort most urgent work first.
    health_rank = {"Red": 1, "Yellow": 2, "Green": 3}
    df["_health_rank"] = df["Health Status"].map(health_rank)
    df = df.sort_values(
        ["_health_rank", "Days in Stage", "Risk Level"],
        ascending=[True, False, True],
    ).drop(columns=["_health_rank"])

    processed_path = output_dir / "cloud_governance_pipeline_clean.csv"
    df.to_csv(processed_path, index=False)

    kpis = {
        "total_use_cases": int(len(df)),
        "red_use_cases": int((df["Health Status"] == "Red").sum()),
        "yellow_use_cases": int((df["Health Status"] == "Yellow").sum()),
        "green_use_cases": int((df["Health Status"] == "Green").sum()),
        "missing_evidence": int((df["Evidence Status"] == "Missing").sum()),
        "non_compliant_regions": int(
            (df["Region Compliance"] == "Non-Compliant").sum()
        ),
        "average_days_in_stage": round(float(df["Days in Stage"].mean()), 1),
        "oldest_open_item_days": int(
            df.loc[df["Current Stage"] != "Approved", "Days in Stage"].max()
        ),
    }

    kpi_path = output_dir / "kpi_summary.json"
    kpi_path.write_text(json.dumps(kpis, indent=2), encoding="utf-8")
    return processed_path, kpi_path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Clean cloud governance pipeline data.")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/raw/cloud_governance_pipeline_raw.csv"),
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/processed"),
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    clean_file, kpi_file = build_pipeline(args.input, args.output_dir)
    print(f"Created: {clean_file}")
    print(f"Created: {kpi_file}")
