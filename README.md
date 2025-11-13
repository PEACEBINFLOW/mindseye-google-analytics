# MindsEye Google Analytics

Analytics layer for the MindsEye Google ecosystem: exports, charts, and dashboards over the **Prompt Evolution Tree (PET)** ledger.

This repo sits on top of:

- `mindseye-google-ledger` (Google Sheets: `nodes` + `runs`)
- All other MindsEye repos that log runs into the ledger (`orchestrator`, `workspace-automation`, etc.)

It does three main things:

1. **Exports**: sample CSV exports for `nodes` and `runs`.
2. **Local analytics**: Python scripts to compute stats + generate charts.
3. **Dashboards**: Looker Studio setup and KPI definitions.

---

## 📁 Structure

```text
mindseye-google-analytics/
├─ README.md
├─ LICENSE
├─ exports/
│  ├─ nodes_sample_export.csv       # Sample export from ledger
│  └─ runs_sample_export.csv
├─ dashboards/
│  ├─ looker_studio_config.md      # How to connect Sheets to Looker
│  └─ kpi_definitions.md           # Definitions for all metrics
├─ scripts/
│  ├─ compute_stats.py             # Basic stats over nodes/runs exports
│  └─ generate_charts.py           # Local chart creation (PNG charts)
└─ docs/
   └─ ANALYTICS_MODEL.md           # How PET + runs are analyzed
