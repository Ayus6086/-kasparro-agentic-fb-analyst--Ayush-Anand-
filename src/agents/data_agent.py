# src/agents/data_agent.py

from pathlib import Path
from typing import Dict, List, Optional

import pandas as pd


class DataAgent:
    """
    Responsible for:
    - Loading the CSV
    - Validating schema
    - Adding derived metrics (CTR, ROAS)
    - Summarizing data
    - Building per-campaign time series
    """

    def __init__(
        self,
        sample_frac: float = 0.2,
        required_columns: Optional[List[str]] = None,
        random_state: int = 42,
    ):
        self.sample_frac = sample_frac
        self.random_state = random_state
        self.required_columns = required_columns or [
            "campaign_name",
            "adset_name",
            "date",
            "spend",
            "impressions",
            "clicks",
            "purchases",
            "revenue",
            "ctr",
            "roas",
            "creative_type",
            "creative_message",
            "audience_type",
        ]

    # ---------- Schema validation ----------

    def validate_schema(self, df: pd.DataFrame) -> None:
        """Ensure all required columns are present. Raise ValueError if not."""
        missing = [c for c in self.required_columns if c not in df.columns]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")

    # ---------- Load with sampling ----------

    def load(self, path: Path) -> pd.DataFrame:
        """Load CSV into DataFrame and validate schema."""
        df = pd.read_csv(path)
        # optional sampling for speed
        if 0 < self.sample_frac < 1.0:
            df = df.sample(frac=self.sample_frac, random_state=self.random_state)

        # make sure basic types are correct
        if "date" in df.columns:
            df["date"] = pd.to_datetime(df["date"], errors="coerce")

        self.validate_schema(df)
        return df

    # ---------- Metrics & anomaly checks ----------

    def add_metrics(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Add/repair 'ctr' and 'roas', handle missing values,
        and detect simple anomalies (negative values).
        """

        # convert numeric columns safely
        for col in ["spend", "impressions", "clicks", "purchases", "revenue"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")

        # handle missing values (do not crash)
        df["spend"] = df["spend"].fillna(0.0)
        df["impressions"] = df["impressions"].fillna(0.0)
        df["clicks"] = df["clicks"].fillna(0.0)
        df["purchases"] = df["purchases"].fillna(0.0)
        df["revenue"] = df["revenue"].fillna(0.0)

        # recompute ctr if needed
        if "ctr" not in df.columns:
            df["ctr"] = 0.0
        df["ctr"] = df.apply(
            lambda row: (row["clicks"] / row["impressions"] * 100.0)
            if row["impressions"] > 0
            else 0.0,
            axis=1,
        )

        # recompute roas if needed
        if "roas" not in df.columns:
            df["roas"] = 0.0
        df["roas"] = df.apply(
            lambda row: (row["revenue"] / row["spend"])
            if row["spend"] > 0
            else 0.0,
            axis=1,
        )

        # simple anomaly flags (extreme values)
        df["anomaly_negative_spend"] = df["spend"] < 0
        df["anomaly_negative_impressions"] = df["impressions"] < 0

        return df

    # ---------- Summary ----------

    def summarize(self, df: pd.DataFrame) -> Dict:
        """Return global summary for planner/insight agents."""
        if df.empty:
            return {
                "date_range": [None, None],
                "total_spend": 0.0,
                "avg_ctr": 0.0,
                "avg_roas": 0.0,
                "campaigns_count": 0,
                "top_by_roas": {},
            }

        date_min = df["date"].min()
        date_max = df["date"].max()

        summary = {
            "date_range": [
                date_min.strftime("%Y-%m-%d") if pd.notnull(date_min) else None,
                date_max.strftime("%Y-%m-%d") if pd.notnull(date_max) else None,
            ],
            "total_spend": float(df["spend"].sum()),
            "avg_ctr": float(df["ctr"].mean()),
            "avg_roas": float(df["roas"].mean()),
            "campaigns_count": int(df["campaign_name"].nunique()),
        }

        # top campaigns by average roas
        roas_by_campaign = df.groupby("campaign_name")["roas"].mean().sort_values(
            ascending=False
        )
        # convert to plain dict
        summary["top_by_roas"] = roas_by_campaign.head(50).to_dict()
        return summary

    # ---------- Time series ----------

    def aggregate_timeseries(self, df: pd.DataFrame) -> Dict[str, List[Dict]]:
        """
        Build a per-campaign time series (sorted by date).
        Returns:
        {
          "Campaign A": [{"date": ..., "ctr": ..., "roas": ..., ...}, ...],
          ...
        }
        """
        if df.empty:
            return {}

        grouped = (
            df.groupby(["campaign_name", "date"])
            .agg(
                {
                    "spend": "sum",
                    "impressions": "sum",
                    "clicks": "sum",
                    "purchases": "sum",
                    "revenue": "sum",
                    "ctr": "mean",
                    "roas": "mean",
                }
            )
            .reset_index()
            .sort_values(["campaign_name", "date"])
        )

        result: Dict[str, List[Dict]] = {}
        for _, row in grouped.iterrows():
            camp = row["campaign_name"]
            payload = {
                "date": row["date"],
                "spend": float(row["spend"]),
                "impressions": float(row["impressions"]),
                "clicks": float(row["clicks"]),
                "purchases": float(row["purchases"]),
                "revenue": float(row["revenue"]),
                "ctr": float(row["ctr"]),
                "roas": float(row["roas"]),
            }
            result.setdefault(camp, []).append(payload)

        return result
