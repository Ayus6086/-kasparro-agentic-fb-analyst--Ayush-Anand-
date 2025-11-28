import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1] 
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd 

from src.agents.data_agent import DataAgent


def test_missing_required_columns_raises_value_error(tmp_path):
    df = pd.DataFrame(
        {
            "adset_name": ["Adset 1"],
            "date": ["2025-01-01"],
            "spend": [100],
            "impressions": [1000],
            "clicks": [50],
            "purchases": [5],
            "revenue": [500],
            "ctr": [5.0],
            "roas": [5.0],
            "creative_type": ["Image"],
            "creative_message": ["Test"],
            "audience_type": ["Broad"],
        }
    )
    csv_path = tmp_path / "bad_missing_column.csv"
    df.to_csv(csv_path, index=False)

    agent = DataAgent(sample_frac=1.0)  

    try:
        agent.load(csv_path)
        assert False, "Expected ValueError for missing required columns"
    except ValueError as e:
        assert "Missing required columns" in str(e)


def test_add_metrics_handles_missing_values(tmp_path):
    df = pd.DataFrame(
        {
            "campaign_name": ["Test Campaign"],
            "adset_name": ["Adset 1"],
            "date": ["2025-01-01"],
            "spend": [None],
            "impressions": [None],
            "clicks": [10],
            "purchases": [1],
            "revenue": [100],
            "ctr": [None],
            "roas": [None],
            "creative_type": ["Image"],
            "creative_message": ["Test"],
            "audience_type": ["Broad"],
        }
    )
    csv_path = tmp_path / "missing_values.csv"
    df.to_csv(csv_path, index=False)

    agent = DataAgent(sample_frac=1.0)
    df_loaded = agent.load(csv_path)
    df_metrics = agent.add_metrics(df_loaded)

    assert "ctr" in df_metrics.columns
    assert "roas" in df_metrics.columns
    assert df_metrics["ctr"].dtype.kind in "fi"  
    assert df_metrics["roas"].dtype.kind in "fi"


def test_add_metrics_flags_negative_spend(tmp_path):
    df = pd.DataFrame(
        {
            "campaign_name": ["Test Campaign"],
            "adset_name": ["Adset 1"],
            "date": ["2025-01-01"],
            "spend": [-100],
            "impressions": [1000],
            "clicks": [50],
            "purchases": [5],
            "revenue": [500],
            "ctr": [5.0],
            "roas": [5.0],
            "creative_type": ["Image"],
            "creative_message": ["Test"],
            "audience_type": ["Broad"],
        }
    )
    csv_path = tmp_path / "negative_spend.csv"
    df.to_csv(csv_path, index=False)

    agent = DataAgent(sample_frac=1.0)
    df_loaded = agent.load(csv_path)
    df_metrics = agent.add_metrics(df_loaded)

    assert "anomaly_negative_spend" in df_metrics.columns
    assert bool(df_metrics["anomaly_negative_spend"].iloc[0]) is True
