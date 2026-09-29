# GitAnalyzer — GitHub Developer Analytics Platform

GitAnalyzer is a Python-based GitHub developer analytics platform that extracts repository activity from the GitHub REST API, transforms and stores the data in a relational SQLite database, calculates development and collaboration metrics, and presents the results through an interactive Streamlit dashboard.

The platform analyzes commits, contributors, pull requests, and issues to provide a data-driven view of repository activity and a configurable Repository Health Score.

---

## Features

- Search and discover public GitHub repositories
- Fetch commits, pull requests, and issues using the GitHub REST API
- Transform and validate GitHub API data
- Store processed data in a relational SQLite database
- Calculate repository development and collaboration metrics
- Calculate a configurable Repository Health Score
- Interactive Streamlit dashboard
- Weekly commit activity visualization
- Pull request closing-time distribution
- Issue resolution-time distribution
- Open and recently closed PR/issue statistics
- Configurable Health Score metric weights
- Repository-level data refresh while preserving data for other analyzed repositories

---

## Architecture

```text
                    GitHub REST API
                           │
                           ▼
                  ┌─────────────────┐
                  │    Ingestion    │
                  │    src/ingest   │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │ Transformation  │
                  │  src/transform  │
                  └────────┬────────┘
                           │
                           ▼
                  ┌─────────────────┐
                  │     Loading     │
                  │     src/load    │
                  └────────┬────────┘
                           │
                           ▼
                    ┌────────────┐
                    │   SQLite   │
                    │  Database  │
                    └─────┬──────┘
                          │
              ┌───────────┴───────────┐
              ▼                       ▼
       ┌──────────────┐        ┌──────────────┐
       │   Metrics    │        │ Health Score │
       │  src/metrics │        │  src/health  │
       └──────┬───────┘        └──────┬───────┘
              │                       │
              └───────────┬───────────┘
                          ▼
                  ┌─────────────────┐
                  │    Streamlit    │
                  │    Dashboard    │
                  │     app.py      │
                  └─────────────────┘
```

---

## Data Pipeline

GitAnalyzer follows an ETL-style workflow.

### 1. Extract

The application communicates with the GitHub REST API to retrieve:

- Repository metadata
- Commits
- Pull requests
- Issues

The ingestion layer also supports GitHub repository discovery and repository analysis.

### 2. Transform

Raw API responses are transformed into structured records suitable for analytical storage.

Transformation includes:

- Selecting relevant fields
- Normalizing API records
- Handling missing values
- Converting timestamps
- Preparing records for relational storage

### 3. Load

Processed records are loaded into SQLite tables:

- `commits`
- `pull_requests`
- `issues`

Repository-level refreshes replace previously stored records for the selected repository while preserving data belonging to other repositories.

### 4. Analyze

Python and SQL-based analytics functions calculate repository activity and collaboration metrics.

### 5. Visualize

The Streamlit application presents the resulting metrics through interactive KPIs and Plotly visualizations.

---

## Database Schema

The current database contains three primary analytical tables.

### Commits

Stores:

- Commit SHA
- Repository
- Author
- Commit date
- Commit message

### Pull Requests

Stores:

- Pull request ID
- Repository
- Pull request number
- Title
- State
- Creation timestamp
- Closing timestamp
- Author

### Issues

Stores:

- Issue ID
- Repository
- Issue number
- Title
- State
- Creation timestamp
- Closing timestamp
- Author
- Comment count

---

## Analytics

### Commit Frequency

Measures repository development activity by calculating commits per week.

The dashboard also displays commits during the most recent 30-day period.

### Active Contributors

Measures the number of unique contributors who have committed during the recent 90-day analysis window.

### Pull Request Closing Time

Measures the elapsed time between pull request creation and closure.

The metric is calculated for pull requests closed during the recent 90-day period.

> **Note:** The current implementation measures PR closing time rather than merge time because the current database schema stores `closed_at`.

### Issue Resolution Time

Measures the elapsed time between issue creation and closure for issues closed during the recent 90-day period.

### Open Pull Requests

Counts pull requests currently marked as open in the analyzed dataset.

### Open Issues

Counts issues currently marked as open in the analyzed dataset.

### Recently Closed Pull Requests

Counts pull requests closed during the recent 90-day analysis period.

### Recently Closed Issues

Counts issues closed during the recent 90-day analysis period.

---

## Repository Health Score

GitAnalyzer calculates a normalized **Repository Health Score from 0–100**.

The score combines four components:

| Component | Reference / Target | Direction |
|---|---:|---|
| Commit Frequency | 20 commits/week | Higher is better |
| Active Contributors | 15 contributors | Higher is better |
| PR Closing Speed | 72 hours | Lower is better |
| Issue Resolution Speed | 168 hours | Lower is better |

### Default Weighting

Each component has a default weight of 25%.

```text
Health Score =
    25% × Commit Frequency Score
  + 25% × Contributor Score
  + 25% × PR Closing Speed Score
  + 25% × Issue Resolution Score
```

The dashboard allows these weights to be adjusted interactively.

If a metric does not have available data, GitAnalyzer excludes that metric and normalizes the remaining available weights.

The Health Score is intended as a composite analytical indicator and should be interpreted together with the underlying repository metrics.

---

## Analysis Windows

The current implementation uses different windows for different metrics:

| Metric | Analysis Window |
|---|---|
| Commits | Recent 30-day activity |
| Active Contributors | Last 90 days |
| Pull Requests | Recent analysis dataset |
| Issues | Recent analysis dataset |
| PR Closing Time | PRs closed in the last 90 days |
| Issue Resolution Time | Issues closed in the last 90 days |

A PR or issue that was created much earlier but closed during the recent 90-day period can therefore have a large resolution time because the calculation measures the full creation-to-closure duration.

---

## Dashboard

### Repository Discovery

Search GitHub repositories by name or topic and explore popular repositories.

### Repository Overview

Displays:

- Repository Health Score
- Commits in the last 30 days
- Active contributors
- Average PR closing time

### Visual Analytics

Interactive Plotly charts display:

- Weekly commit frequency
- Pull request closing-time distribution
- Issue resolution-time distribution
- Individual Health Score component scores

### PR and Issue Statistics

Displays:

- Open PRs
- Recently closed PRs
- Open issues
- Recently closed issues
- Average PR closing time
- Average issue resolution time

---

## Project Structure

```text
github_analyzer/
│
├── app.py
├── schema.sql
├── .gitignore
├── requirements.txt
│
├── data/
│   ├── raw/
│   └── gitpulse.db
│
└── src/
    ├── config.py
    ├── ingest.py
    ├── transform.py
    ├── load.py
    ├── metrics.py
    └── health.py
```

> The local SQLite database and raw data are excluded from version control through `.gitignore`.

---

## Technologies

| Technology | Purpose |
|---|---|
| Python | ETL, data processing, and analytics |
| SQL / SQLite | Relational data storage and querying |
| GitHub REST API | Repository data source |
| Pandas | Data transformation and analysis |
| NumPy | Numerical processing |
| Requests | API communication |
| python-dotenv | Environment configuration |
| Streamlit | Interactive dashboard |
| Plotly | Interactive data visualization |
| Git / GitHub | Version control |

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/akhilamulukutla/github_analyzer.git
cd github_analyzer
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

Activate it on macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure GitHub authentication

Create a `.env` file in the project root:

```env
GITHUB_TOKEN=your_github_token_here
```

The `.env` file is excluded from Git through `.gitignore`.

### 5. Run the application

```bash
streamlit run app.py
```

The application will open in your browser.

---

## GitHub API Authentication

GitAnalyzer uses a GitHub personal access token for authenticated API requests.

The token should be stored locally in `.env` and should never be committed to the repository.

Example:

```env
GITHUB_TOKEN=your_github_token_here
```

**Never place an actual GitHub token in source code or documentation.**

---

## Current Scope

The current version focuses on repository analytics and an interactive dashboard.

The pipeline analyzes a recent subset of repository activity rather than maintaining a complete historical copy of every GitHub event.

Future improvements include:

- True incremental loading using database watermarks
- PR merge-time analytics using `merged_at`
- Contributor retention analysis across time periods
- ETL execution logging
- Additional repository quality metrics
- Automated scheduled ingestion
- Expanded analytical storage

---

## Project Goal

GitAnalyzer was built to demonstrate practical data engineering and analytics concepts through a real-world public API.

```text
API Integration
      ↓
Data Ingestion
      ↓
Data Transformation
      ↓
Relational Storage
      ↓
Analytical Metrics
      ↓
Data Visualization
```

The project combines data engineering, SQL, Python analytics, API integration, and dashboard development into a single end-to-end application.