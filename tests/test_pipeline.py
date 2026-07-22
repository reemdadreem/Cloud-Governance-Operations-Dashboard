from pathlib import Path

import pandas as pd

from src.pipeline import build_pipeline


def test_pipeline_creates_expected_columns(tmp_path: Path) -> None:
    input_path = Path("data/raw/cloud_governance_pipeline_raw.csv")
    processed_path, _ = build_pipeline(input_path, tmp_path)

    df = pd.read_csv(processed_path)

    expected = {
        "Days in Stage",
        "Health Status",
        "Evidence Status",
        "Region Compliance",
        "Escalation Required",
    }
    assert expected.issubset(df.columns)
    assert set(df["Health Status"]).issubset({"Red", "Yellow", "Green"})
