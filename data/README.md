# Dataset Documentation – Facebook Ads Sample

This folder contains the **sample dataset** used by the agentic system to analyze
campaign performance, detect ROAS/CTR declines, and generate insights.

The file in this directory:

```
sample.csv
```

---

## 📌 File Description: `sample.csv`

This is a **synthetic but realistic Facebook Ads dataset** containing daily performance metrics for multiple campaigns.

Each row represents **one day of performance** for a specific adset inside a campaign.

---

## 📊 Column Definitions

| Column Name        | Description |
|-------------------|-------------|
| `campaign_name`   | Name of the campaign being analyzed. |
| `adset_name`      | The specific adset inside the campaign. |
| `date`            | Daily date (YYYY-MM-DD). |
| `spend`           | Amount spent on ads for that day. |
| `impressions`     | Number of times the ads were shown. |
| `clicks`          | Number of clicks received. |
| `ctr`             | Click-through rate. If missing, computed as clicks/impressions. |
| `purchases`       | Number of conversions/purchases. |
| `revenue`         | Total revenue generated. |
| `roas`            | Return on ad spend. If missing, computed as revenue/spend. |
| `creative_type`   | Type of creative used (Image / Video / UGC / Carousel). |
| `creative_message`| The headline or message inside the ad. |
| `audience_type`   | Target audience segment (Broad / Retargeting / Lookalike). |

---

## 🧪 How This Dataset Is Used

### The agent system uses this file to:
- Compute CTR, ROAS, and performance metrics  
- Build daily time-series  
- Identify ROAS or CTR drops  
- Generate insights and hypotheses  
- Produce creative recommendations  

---

## 🔄 Replacing the Dataset

If you want to analyze another dataset:

1. Replace `sample.csv` inside this folder  
2. The new CSV **must contain the same columns** as listed above  
3. Run the pipeline again:

```bash
python -m src.orchestrator.run
```

---

## 📝 Notes for Reproducibility

- The dataset should have **at least 14+ days** per campaign for reliable pre/post analysis.  
- Missing CTR or ROAS values are automatically computed.  
- The system supports any number of campaigns.

---