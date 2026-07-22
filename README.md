# Cloud Governance Operations Dashboard

An enterprise-style portfolio project that uses **Python**, **data-quality rules**, and an executive dashboard to transform a messy cloud-governance pipeline into actionable leadership reporting.

> **Portfolio goal:** Demonstrate how a Business Analyst or Governance professional can use automation to reduce manual reporting, identify cloud risk, and improve operational visibility.

## Overview

Cloud-governance teams often manage intake requests across spreadsheets, ticketing tools, email, and meetings. Leadership needs to know:

- Which cloud use cases are blocked?
- Which requests are aging?
- What evidence is missing?
- Are teams deploying into approved cloud regions?
- Which items need escalation?
- Where is the greatest operational risk?

This project creates a repeatable pipeline that answers those questions.

## Architecture

```text
Raw CSV / Excel Export
        |
        v
Python Data Pipeline
  - clean fields
  - validate records
  - calculate aging
  - test region compliance
  - assign RAG health
        |
        v
Processed Dataset + KPI JSON
        |
        +---------------------+
        |                     |
        v                     v
Streamlit Dashboard      Power BI Model
(portfolio demo)         (planned)
```

## Project Structure

```text
cloud-governance-operations-dashboard/
├── dashboard/
│   └── app.py
├── data/
│   ├── raw/
│   │   └── cloud_governance_pipeline_raw.csv
│   └── processed/
├── docs/
│   └── screenshots/
├── src/
│   └── pipeline.py
├── tests/
│   └── test_pipeline.py
├── .gitignore
├── LICENSE
├── README.md
└── requirements.txt
```

## Business Problem

Manual governance reporting creates several common problems:

1. Analysts spend time repeatedly cleaning spreadsheets.
2. Aging calculations may differ between reports.
3. Missing evidence is difficult to track consistently.
4. Region-policy violations can be overlooked.
5. Leadership receives status updates instead of an exception-focused view.
6. The team lacks a single, reproducible source of truth.

The solution is a lightweight automation pipeline that standardizes data and surfaces only the items requiring attention.

## Python Automation

The script in `src/pipeline.py`:

1. Imports the raw governance pipeline.
2. Cleans whitespace, capitalization, dates, and identifiers.
3. Removes duplicate or invalid records.
4. Calculates the number of days each item has been open.
5. Flags missing documentation.
6. checks whether the actual cloud region is approved.
7. Assigns **Red**, **Yellow**, or **Green** health.
8. Creates a leadership exception queue.
9. Exports a clean CSV and KPI summary.

### RAG Logic

| Status | Example rule |
|---|---|
| Red | Unapproved region, critical risk, or more than 90 days old |
| Yellow | Missing evidence, high risk, or more than 45 days old |
| Green | Approved or progressing within expected thresholds |

These rules are simplified for demonstration and can be replaced with organization-specific policy.

## Running the Project

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

```bash
# macOS/Linux
source .venv/bin/activate

# Windows PowerShell
.venv\Scripts\Activate.ps1
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the data pipeline

```bash
python src/pipeline.py
```

This creates:

```text
data/processed/cloud_governance_pipeline_clean.csv
data/processed/kpi_summary.json
```

### 4. Launch the dashboard

```bash
streamlit run dashboard/app.py
```

## Power BI Dashboard

The planned Power BI report will use the processed CSV and include:

- Executive KPI cards
- Pipeline volume by stage
- RAG health distribution
- Aging buckets
- Region-compliance exceptions
- Missing-evidence analysis
- Risk by cloud provider
- Owner workload
- Leadership escalation queue

### Recommended Pages

**Page 1 — Executive Overview**

- Total use cases
- Red and yellow items
- Average aging
- Missing evidence
- Region exceptions
- Pipeline by stage

**Page 2 — Risk and Compliance**

- Risk level by provider
- Approved versus unapproved regions
- Critical and high-risk items
- Evidence gaps

**Page 3 — Operational Detail**

- Searchable use-case table
- Owner and stage filters
- Aging buckets
- Escalation status

## Screenshots

Add screenshots here as the project develops:

```text
docs/screenshots/
├── executive-overview.png
├── risk-compliance.png
└── exception-queue.png
```

Then display them in this README:

```markdown
![Executive Overview](docs/screenshots/executive-overview.png)
```

## Future Improvements

- Read directly from Excel, SharePoint, Jira, or ServiceNow.
- Send weekly exception summaries by email or Microsoft Teams.
- Add SLA rules by governance stage.
- Add automated data-quality tests.
- Add an AI-generated executive summary.
- Connect to Azure Resource Graph, AWS Config, or GCP Asset Inventory.
- Validate live cloud resources against approved-region policy.
- Provision the dashboard environment with Terraform.
- Add CI/CD with GitHub Actions.
- Containerize the application with Docker.

## Lessons Learned

This section should be updated as the project develops. Strong lessons may include:

- Governance rules must be translated into explicit, testable logic.
- Data cleaning is often the largest part of reporting automation.
- Leadership dashboards should prioritize exceptions, not raw activity.
- Technical solutions are more valuable when tied to a measurable business problem.
- Documentation makes an automation maintainable and transferable.

## Skills Demonstrated

- Python
- pandas
- Data cleaning and validation
- Business analysis
- Cloud governance
- Risk and compliance reporting
- Executive dashboard design
- Git and GitHub
- Streamlit
- Power BI planning
- Automation and process improvement

## Responsible Use

This repository uses entirely synthetic data. It does not contain confidential employer information, internal policies, real employee names, or proprietary workflows.

## License

MIT
