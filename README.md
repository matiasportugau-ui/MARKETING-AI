# Gravity Workspace

> **Status**: ACTIVE
> **Agent**: Gravity (Prompt Pack v1.0)
> **Ops Manual**: `gravity_operations_manual.md`

This directory is the "Command Center" for the Gravity AI Agent. It is designed for structured interaction between the User (You) and the Agent (Gravity).

## 📂 Structure

- `inputs/`: **DROP ZONE**. Save your CSV exports here.
  - Naming: `google_ads_last30.csv`, `meta_ads_report.csv` (Agent auto-detects).
- `outputs/`: **RESULTS**. Gravity writes here.
  - `context.json`: The "Brain State" after digesting your CSVs.
  - `gravity_report_DATE.md`: The analysis report.
- `tools/`: **AUTOMATION**.
  - `python3 tools/gravity_ingest.py`: Reads `inputs/*`, updates `outputs/context.json`.
  - `python3 tools/gravity_assessor.py`: Checks risks.
- `memory/`: **LOGS**.
  - `decision_journal.json`: The permanent record of "EJECUTAR" commands.

## 🚀 How to use this workspace (Workflow)

1.  **Ingest Data** (Daily/Weekly)
    - Export CSVs from Ads Manager.
    - Save to `inputs/`.
    - Run: `python3 tools/gravity_ingest.py`
2.  **Ask Questions**

    - Use your Agent interface (referencing this workspace).
    - "Gravity, read the new context. How is our CPA trending?"

3.  **Execute**
    - If Gravity proposes a plan, it may write a JSON draft.
    - Run `python3 tools/gravity_assessor.py` (Optional) to validate.
    - Say "EJECUTAR" to proceed.

## 🛠 Setup

```bash
pip install -r requirements.txt
```
