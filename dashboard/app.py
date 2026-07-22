from pathlib import Path

import pandas as pd
import streamlit as st


# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------

st.set_page_config(
    page_title="Cloud Governance Operations Center",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ---------------------------------------------------------
# ENTERPRISE UI STYLING
# ---------------------------------------------------------

st.markdown(
    """
    <style>
        .stApp {
            background:
                radial-gradient(circle at top right, rgba(33, 150, 243, 0.08), transparent 28%),
                radial-gradient(circle at top left, rgba(0, 188, 212, 0.05), transparent 22%);
        }

        [data-testid="stSidebar"] {
            border-right: 1px solid rgba(128, 128, 128, 0.18);
        }

        [data-testid="stSidebar"] .block-container {
            padding-top: 1.4rem;
        }

        .dashboard-hero {
            padding: 1.35rem 1.5rem 1.2rem;
            border: 1px solid rgba(128, 128, 128, 0.22);
            border-radius: 18px;
            background: linear-gradient(
                135deg,
                rgba(17, 24, 39, 0.96),
                rgba(15, 70, 95, 0.90)
            );
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.16);
            margin-bottom: 1rem;
        }

        .dashboard-eyebrow {
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.13em;
            text-transform: uppercase;
            color: #7dd3fc;
            margin-bottom: 0.4rem;
        }

        .dashboard-title {
            font-size: clamp(1.8rem, 3vw, 2.8rem);
            font-weight: 800;
            line-height: 1.05;
            color: #f8fafc;
            margin: 0;
        }

        .dashboard-subtitle {
            max-width: 860px;
            margin-top: 0.65rem;
            color: #cbd5e1;
            font-size: 1rem;
            line-height: 1.55;
        }

        .hero-meta {
            display: flex;
            flex-wrap: wrap;
            gap: 0.55rem;
            margin-top: 1rem;
        }

        .hero-pill {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            padding: 0.4rem 0.7rem;
            border: 1px solid rgba(255, 255, 255, 0.16);
            border-radius: 999px;
            background: rgba(255, 255, 255, 0.07);
            color: #e2e8f0;
            font-size: 0.83rem;
        }

        .section-heading {
            margin-top: 1.1rem;
            margin-bottom: 0.15rem;
            font-size: 1.15rem;
            font-weight: 750;
        }

        .section-caption {
            color: #94a3b8;
            margin-bottom: 0.75rem;
            font-size: 0.92rem;
        }

        .kpi-card {
            min-height: 148px;
            padding: 1rem 1rem 0.9rem;
            border: 1px solid rgba(128, 128, 128, 0.20);
            border-radius: 16px;
            background: rgba(255, 255, 255, 0.035);
            box-shadow: 0 8px 18px rgba(0, 0, 0, 0.08);
        }

        .kpi-topline {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.5rem;
        }

        .kpi-icon {
            font-size: 1.15rem;
        }

        .kpi-label {
            color: #94a3b8;
            font-size: 0.82rem;
            font-weight: 650;
            letter-spacing: 0.02em;
        }

        .kpi-value {
            margin-top: 0.45rem;
            font-size: 2rem;
            font-weight: 800;
            line-height: 1;
        }

        .kpi-note {
            margin-top: 0.55rem;
            color: #94a3b8;
            font-size: 0.76rem;
            line-height: 1.35;
        }

        .tone-blue { color: #38bdf8; }
        .tone-red { color: #fb7185; }
        .tone-amber { color: #fbbf24; }
        .tone-green { color: #4ade80; }
        .tone-violet { color: #a78bfa; }
        .tone-slate { color: #e2e8f0; }

        .attention-banner {
            padding: 0.9rem 1rem;
            border-left: 4px solid #fb7185;
            border-radius: 10px;
            background: rgba(244, 63, 94, 0.08);
            margin-bottom: 0.8rem;
        }

        .attention-title {
            color: #fecdd3;
            font-weight: 750;
            margin-bottom: 0.15rem;
        }

        .attention-copy {
            color: #cbd5e1;
            font-size: 0.88rem;
            margin: 0;
        }

        .sidebar-brand {
            padding: 0.85rem 0.9rem;
            border: 1px solid rgba(128, 128, 128, 0.20);
            border-radius: 14px;
            background: rgba(255, 255, 255, 0.035);
            margin-bottom: 1rem;
        }

        .sidebar-brand-title {
            font-weight: 800;
            font-size: 1rem;
        }

        .sidebar-brand-copy {
            color: #94a3b8;
            font-size: 0.78rem;
            line-height: 1.35;
            margin-top: 0.2rem;
        }

        .filter-summary {
            padding: 0.75rem 0.85rem;
            border-radius: 12px;
            background: rgba(56, 189, 248, 0.08);
            border: 1px solid rgba(56, 189, 248, 0.18);
            margin-top: 0.8rem;
        }

        .filter-summary strong {
            color: #7dd3fc;
        }

        .footer {
            margin-top: 2rem;
            padding: 1.2rem 0 0.7rem;
            border-top: 1px solid rgba(128, 128, 128, 0.18);
            color: #94a3b8;
            font-size: 0.78rem;
            text-align: center;
        }

        div[data-testid="stDataFrame"] {
            border: 1px solid rgba(128, 128, 128, 0.16);
            border-radius: 14px;
            overflow: hidden;
        }

        div[data-testid="stVegaLiteChart"] {
            border: 1px solid rgba(128, 128, 128, 0.14);
            border-radius: 14px;
            padding: 0.4rem;
            background: rgba(255, 255, 255, 0.018);
        }

        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 2rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# FILE PATHS
# ---------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "cloud_governance_pipeline_clean.csv"
)


# ---------------------------------------------------------
# DATA LOADING
# ---------------------------------------------------------

@st.cache_data
def load_data(file_path: Path) -> pd.DataFrame:
    """Load and prepare the processed governance dataset."""
    if not file_path.exists():
        raise FileNotFoundError(
            f"Processed data file was not found: {file_path}"
        )

    dataframe = pd.read_csv(file_path)

    if "Submission Date" in dataframe.columns:
        dataframe["Submission Date"] = pd.to_datetime(
            dataframe["Submission Date"],
            errors="coerce",
        )

    if "Days in Stage" in dataframe.columns:
        dataframe["Days in Stage"] = pd.to_numeric(
            dataframe["Days in Stage"],
            errors="coerce",
        ).fillna(0)

    return dataframe


try:
    df = load_data(DATA_FILE)
except FileNotFoundError as error:
    st.error(str(error))
    st.info(
        "Run the Python pipeline first to generate the processed dataset."
    )
    st.stop()
except Exception as error:
    st.error(f"Unable to load the dashboard data: {error}")
    st.stop()


# ---------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------

def available_values(
    dataframe: pd.DataFrame,
    column_name: str,
) -> list[str]:
    """Return sorted, non-empty filter values for a column."""
    if column_name not in dataframe.columns:
        return []

    values = (
        dataframe[column_name]
        .dropna()
        .astype(str)
        .str.strip()
    )

    values = values[values != ""]

    return sorted(values.unique().tolist())


def filter_dataframe(
    dataframe: pd.DataFrame,
    providers: list[str],
    owners: list[str],
    stages: list[str],
    health_statuses: list[str],
    risk_levels: list[str],
    evidence_statuses: list[str],
    region_statuses: list[str],
) -> pd.DataFrame:
    """Apply all sidebar filters to the governance dataset."""
    filtered = dataframe.copy()

    filter_map = {
        "Cloud Provider": providers,
        "Owner": owners,
        "Current Stage": stages,
        "Health Status": health_statuses,
        "Risk Level": risk_levels,
        "Evidence Status": evidence_statuses,
        "Region Compliance": region_statuses,
    }

    for column_name, selected_values in filter_map.items():
        if selected_values and column_name in filtered.columns:
            filtered = filtered[
                filtered[column_name]
                .astype(str)
                .isin(selected_values)
            ]

    return filtered


def count_matches(
    dataframe: pd.DataFrame,
    column_name: str,
    expected_value: str,
) -> int:
    """Count rows matching a case-insensitive value."""
    if column_name not in dataframe.columns:
        return 0

    return int(
        dataframe[column_name]
        .astype(str)
        .str.strip()
        .str.casefold()
        .eq(expected_value.casefold())
        .sum()
    )


def format_date_range(dataframe: pd.DataFrame) -> str:
    """Create a readable reporting-period label."""
    if (
        "Submission Date" not in dataframe.columns
        or dataframe["Submission Date"].dropna().empty
    ):
        return "Reporting period unavailable"

    earliest = dataframe["Submission Date"].min()
    latest = dataframe["Submission Date"].max()

    return f"{earliest:%b %d, %Y} – {latest:%b %d, %Y}"


def calculate_average_aging(dataframe: pd.DataFrame) -> float:
    """Return the average number of days in the current stage."""
    if "Days in Stage" not in dataframe.columns or dataframe.empty:
        return 0.0

    return float(dataframe["Days in Stage"].mean())


def calculate_compliance_rate(dataframe: pd.DataFrame) -> float:
    """Return the percentage of region-compliant records."""
    if "Region Compliance" not in dataframe.columns or dataframe.empty:
        return 0.0

    compliant = count_matches(
        dataframe,
        "Region Compliance",
        "Compliant",
    )

    return (compliant / len(dataframe)) * 100


def render_kpi_card(
    icon: str,
    label: str,
    value: str,
    note: str,
    tone: str,
) -> None:
    """Render a custom executive KPI card."""
    st.markdown(
        f"""
        <div class="kpi-card">
            <div class="kpi-topline">
                <div class="kpi-label">{label}</div>
                <div class="kpi-icon">{icon}</div>
            </div>
            <div class="kpi-value {tone}">{value}</div>
            <div class="kpi-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def active_filter_count(*filter_groups: list[str]) -> int:
    """Return the number of filters with at least one selection."""
    return sum(bool(group) for group in filter_groups)


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-title">☁️ Governance Control Center</div>
            <div class="sidebar-brand-copy">
                Interactive operational reporting for cloud governance,
                risk, evidence, and compliance oversight.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("⚙️ Dashboard Filters")
    st.caption(
        "Isolate specific ownership, risk, provider, and workflow conditions."
    )

    provider_options = available_values(df, "Cloud Provider")
    owner_options = available_values(df, "Owner")
    stage_options = available_values(df, "Current Stage")
    health_options = available_values(df, "Health Status")
    risk_options = available_values(df, "Risk Level")
    evidence_options = available_values(df, "Evidence Status")
    region_options = available_values(df, "Region Compliance")

    selected_providers = st.multiselect(
        "Cloud Provider",
        options=provider_options,
        placeholder="All providers",
    )

    selected_owners = st.multiselect(
        "Owner",
        options=owner_options,
        placeholder="All owners",
    )

    selected_stages = st.multiselect(
        "Current Stage",
        options=stage_options,
        placeholder="All stages",
    )

    selected_health = st.multiselect(
        "Health Status",
        options=health_options,
        placeholder="All health statuses",
    )

    selected_risk = st.multiselect(
        "Risk Level",
        options=risk_options,
        placeholder="All risk levels",
    )

    selected_evidence = st.multiselect(
        "Evidence Status",
        options=evidence_options,
        placeholder="All evidence statuses",
    )

    selected_region = st.multiselect(
        "Region Compliance",
        options=region_options,
        placeholder="All region statuses",
    )


filtered_df = filter_dataframe(
    dataframe=df,
    providers=selected_providers,
    owners=selected_owners,
    stages=selected_stages,
    health_statuses=selected_health,
    risk_levels=selected_risk,
    evidence_statuses=selected_evidence,
    region_statuses=selected_region,
)


with st.sidebar:
    selected_filter_total = active_filter_count(
        selected_providers,
        selected_owners,
        selected_stages,
        selected_health,
        selected_risk,
        selected_evidence,
        selected_region,
    )

    st.markdown(
        f"""
        <div class="filter-summary">
            <strong>{len(filtered_df):,}</strong> of
            <strong>{len(df):,}</strong> requests shown<br>
            <span style="font-size:0.76rem;color:#94a3b8;">
                {selected_filter_total} active filter group(s)
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Clear selections manually to return to the full dataset.")


# ---------------------------------------------------------
# DASHBOARD HEADER
# ---------------------------------------------------------

st.markdown(
    f"""
    <div class="dashboard-hero">
        <div class="dashboard-eyebrow">
            Enterprise Governance &amp; Compliance Operations
        </div>
        <h1 class="dashboard-title">
            Cloud Governance Operations Center
        </h1>
        <div class="dashboard-subtitle">
            Executive visibility into pipeline health, operational aging,
            compliance exceptions, evidence readiness, and cloud risk.
        </div>
        <div class="hero-meta">
            <span class="hero-pill">📅 {format_date_range(filtered_df)}</span>
            <span class="hero-pill">
                📋 {len(filtered_df):,} of {len(df):,} use cases
            </span>
            <span class="hero-pill">🔄 Processed dataset</span>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# EXECUTIVE KPI CARDS
# ---------------------------------------------------------

total_requests = len(filtered_df)
critical_risks = count_matches(
    filtered_df,
    "Risk Level",
    "Critical",
)
red_health = count_matches(
    filtered_df,
    "Health Status",
    "Red",
)
missing_evidence = count_matches(
    filtered_df,
    "Evidence Status",
    "Missing",
)
region_exceptions = count_matches(
    filtered_df,
    "Region Compliance",
    "Non-Compliant",
)
average_aging = calculate_average_aging(filtered_df)
compliance_rate = calculate_compliance_rate(filtered_df)

st.markdown(
    '<div class="section-heading">Executive Snapshot</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-caption">'
    'Current operational posture based on the selected governance population.'
    '</div>',
    unsafe_allow_html=True,
)

kpi_1, kpi_2, kpi_3 = st.columns(3)
kpi_4, kpi_5, kpi_6 = st.columns(3)

with kpi_1:
    render_kpi_card(
        "📋",
        "Open Requests",
        f"{total_requests:,}",
        "Governance use cases matching the current filters.",
        "tone-blue",
    )

with kpi_2:
    render_kpi_card(
        "🚨",
        "Critical Risks",
        f"{critical_risks:,}",
        "Items requiring immediate risk review or escalation.",
        "tone-red",
    )

with kpi_3:
    render_kpi_card(
        "🔴",
        "Red Health",
        f"{red_health:,}",
        "Requests currently outside acceptable operating health.",
        "tone-red",
    )

with kpi_4:
    render_kpi_card(
        "📎",
        "Missing Evidence",
        f"{missing_evidence:,}",
        "Requests with incomplete governance documentation.",
        "tone-amber",
    )

with kpi_5:
    render_kpi_card(
        "🗺️",
        "Region Exceptions",
        f"{region_exceptions:,}",
        "Use cases operating outside approved cloud regions.",
        "tone-violet",
    )

with kpi_6:
    render_kpi_card(
        "✅",
        "Region Compliance",
        f"{compliance_rate:.0f}%",
        f"Average aging is {average_aging:.1f} days in the current stage.",
        "tone-green",
    )


# ---------------------------------------------------------
# EMPTY-RESULT HANDLING
# ---------------------------------------------------------

if filtered_df.empty:
    st.warning(
        "No governance records match the current filter selection."
    )
    st.stop()


# ---------------------------------------------------------
# OPERATIONS ANALYTICS
# ---------------------------------------------------------

st.markdown(
    '<div class="section-heading">Operational Analytics</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-caption">'
    'Pipeline distribution, health posture, provider risk, and aging trends.'
    '</div>',
    unsafe_allow_html=True,
)

chart_col_1, chart_col_2 = st.columns(2)

with chart_col_1:
    st.subheader("Pipeline by Stage")

    if "Current Stage" in filtered_df.columns:
        stage_counts = (
            filtered_df["Current Stage"]
            .value_counts()
            .rename_axis("Current Stage")
            .reset_index(name="Use Cases")
        )

        st.bar_chart(
            stage_counts,
            x="Current Stage",
            y="Use Cases",
            width="stretch",
        )
    else:
        st.info("Current Stage data is unavailable.")

with chart_col_2:
    st.subheader("Health Distribution")

    if "Health Status" in filtered_df.columns:
        health_counts = (
            filtered_df["Health Status"]
            .value_counts()
            .rename_axis("Health Status")
            .reset_index(name="Use Cases")
        )

        st.bar_chart(
            health_counts,
            x="Health Status",
            y="Use Cases",
            width="stretch",
        )
    else:
        st.info("Health Status data is unavailable.")


chart_col_3, chart_col_4 = st.columns(2)

with chart_col_3:
    st.subheader("Risk by Cloud Provider")

    required_columns = {"Cloud Provider", "Risk Level"}

    if required_columns.issubset(filtered_df.columns):
        provider_risk = (
            filtered_df.groupby(
                ["Cloud Provider", "Risk Level"]
            )
            .size()
            .unstack(fill_value=0)
        )

        st.bar_chart(
            provider_risk,
            width="stretch",
        )
    else:
        st.info("Provider risk data is unavailable.")

with chart_col_4:
    st.subheader("Average Days by Stage")

    required_columns = {"Current Stage", "Days in Stage"}

    if required_columns.issubset(filtered_df.columns):
        average_days = (
            filtered_df.groupby("Current Stage")["Days in Stage"]
            .mean()
            .round(1)
            .sort_values(ascending=False)
        )

        st.bar_chart(
            average_days,
            width="stretch",
        )
    else:
        st.info("Aging data is unavailable.")


# ---------------------------------------------------------
# LEADERSHIP EXCEPTION QUEUE
# ---------------------------------------------------------

st.markdown(
    '<div class="section-heading">Leadership Exception Queue</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="attention-banner">
        <div class="attention-title">🚨 Priority Governance Attention</div>
        <p class="attention-copy">
            This queue surfaces records with red health, critical risk,
            missing evidence, or non-compliant cloud-region usage.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

exception_conditions = pd.Series(
    False,
    index=filtered_df.index,
)

if "Health Status" in filtered_df.columns:
    exception_conditions |= (
        filtered_df["Health Status"]
        .astype(str)
        .str.casefold()
        .eq("red")
    )

if "Risk Level" in filtered_df.columns:
    exception_conditions |= (
        filtered_df["Risk Level"]
        .astype(str)
        .str.casefold()
        .eq("critical")
    )

if "Region Compliance" in filtered_df.columns:
    exception_conditions |= (
        filtered_df["Region Compliance"]
        .astype(str)
        .str.casefold()
        .eq("non-compliant")
    )

if "Evidence Status" in filtered_df.columns:
    exception_conditions |= (
        filtered_df["Evidence Status"]
        .astype(str)
        .str.casefold()
        .eq("missing")
    )

exception_queue = filtered_df[exception_conditions].copy()

risk_priority = {
    "Critical": 1,
    "High": 2,
    "Medium": 3,
    "Low": 4,
}

if "Risk Level" in exception_queue.columns:
    exception_queue["_Risk Sort"] = (
        exception_queue["Risk Level"]
        .map(risk_priority)
        .fillna(99)
    )

sort_columns = [
    column
    for column in ["_Risk Sort", "Days in Stage"]
    if column in exception_queue.columns
]

if sort_columns:
    ascending = [True if column == "_Risk Sort" else False for column in sort_columns]
    exception_queue = exception_queue.sort_values(
        by=sort_columns,
        ascending=ascending,
    )

preferred_exception_columns = [
    "Use Case ID",
    "Owner",
    "Cloud Provider",
    "Current Stage",
    "Days in Stage",
    "Health Status",
    "Evidence Status",
    "Region Compliance",
    "Risk Level",
    "Escalation Required",
]

visible_exception_columns = [
    column
    for column in preferred_exception_columns
    if column in exception_queue.columns
]

if exception_queue.empty:
    st.success(
        "No exception items require leadership attention "
        "under the current filters."
    )
else:
    st.dataframe(
        exception_queue[visible_exception_columns],
        width="stretch",
        hide_index=True,
        column_config={
            "Days in Stage": st.column_config.NumberColumn(
                "Days in Stage",
                format="%d days",
            ),
        },
    )


# ---------------------------------------------------------
# FULL GOVERNANCE PIPELINE
# ---------------------------------------------------------

st.markdown(
    '<div class="section-heading">Governance Pipeline Detail</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="section-caption">'
    'Complete operational view of requests matching the selected filters.'
    '</div>',
    unsafe_allow_html=True,
)

pipeline_df = filtered_df.copy()

if {"Risk Level", "Days in Stage"}.issubset(pipeline_df.columns):
    pipeline_df["_Risk Sort"] = (
        pipeline_df["Risk Level"]
        .map(risk_priority)
        .fillna(99)
    )
    pipeline_df = (
        pipeline_df
        .sort_values(
            by=["_Risk Sort", "Days in Stage"],
            ascending=[True, False],
        )
        .drop(columns=["_Risk Sort"])
    )

st.dataframe(
    pipeline_df,
    width="stretch",
    hide_index=True,
    column_config={
        "Submission Date": st.column_config.DateColumn(
            "Submission Date",
            format="MMM DD, YYYY",
        ),
        "Days in Stage": st.column_config.NumberColumn(
            "Days in Stage",
            format="%d days",
        ),
    },
)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown(
    """
    <div class="footer">
        Cloud Governance Operations Dashboard · Version 1.0<br>
        Python · Pandas · Streamlit · Built by Kareem Watts
    </div>
    """,
    unsafe_allow_html=True,
)
