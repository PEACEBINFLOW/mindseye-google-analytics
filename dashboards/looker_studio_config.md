# Looker Studio Configuration for MindsEye Analytics

This guide walks you through connecting the **MindsEye ledger** (Google Sheets) to **Looker Studio** and building a dashboard for:

- Prompt evolution (nodes)
- Run activity (runs)
- Success metrics by model / surface / prompt_type

---

## 1. Prepare the data in Google Sheets

You should already have:

- A Sheet with:
  - `nodes` tab
  - `runs` tab

from `mindseye-google-ledger`.

**Recommended:**

- Make sure the first row in each sheet is a **header row** exactly matching:

`nodes`:

```text
node_id,parent_node_id,title,prompt_type,doc_url,status,tags,created_at,updated_at
