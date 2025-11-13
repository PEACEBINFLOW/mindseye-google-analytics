# MindsEye Analytics Model

This doc explains how the **Prompt Evolution Tree (PET)** + **runs** ledger  
is turned into metrics and visualizations in `mindseye-google-analytics`.

---

## 1. Source of truth

All analytics are derived from the **MindsEye ledger**:

- `nodes` tab — defines each prompt node in the PET.
- `runs` tab — every execution of a node.

Schema mirrors `mindseye-google-ledger/schema/ledger_columns.md`:

### nodes

- `node_id`
- `parent_node_id`
- `title`
- `prompt_type`
- `doc_url`
- `status`
- `tags`
- `created_at`
- `updated_at`

### runs

- `run_id`
- `node_id`
- `model`
- `run_context`
- `input_ref`
- `output_ref`
- `score`
- `notes`
- `run_time`

The analytics repo **never writes** back to the ledger; it only reads exports.

---

## 2. Logical model

We treat:

- `Node` as the **unit of design** (a prompt / meta-prompt).
- `Run` as the **unit of execution**.

Relationships:

- Each `Run` **belongs to** exactly one `Node` via `run.node_id`.
- Nodes can be organized into a tree via `parent_node_id`:
  - e.g. `PET-00001` → base Gmail summary prompt
  - `PET-00002` → variation with action items (child of 00001)

This gives us three layers:

1. **Design layer**: `nodes` (prompt types, status, tags, doc_url).
2. **Execution layer**: `runs` (time, model, surface, quality).
3. **Analytics layer**: metrics derived from counts + aggregations.

---

## 3. Core questions

The model is built to answer questions like:

- How many prompts exist, and what types are they?
- How often are they actually being used (runs per node)?
- Which surfaces are most active (`run_context`)?
- Which models are performing best (avg score)?
- Which prompt types are reliable (success_rate by `prompt_type`)?
- How is activity evolving over time (runs per day, new nodes per day)?

---

## 4. Derived fields

Several analytics require **derived fields** that aren’t stored in the ledger directly.

Examples:

### 4.1 success_flag

Binary indicator based on `score`:

```text
success_flag = 1 if score >= 0.8 else 0
