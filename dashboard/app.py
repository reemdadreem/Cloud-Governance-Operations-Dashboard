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
    """
    Load and prepare the processed governance dataset.

    Streamlit caches the result so the CSV is not reloaded
    every time the user interacts with a filter.
    """
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
        if (
            selected_values
            and column_name in filtered.columns
        ):
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

    return (
        f"Submission period: "
        f"{earliest:%b %d, %Y} – {latest:%b %d, %Y}"
    )


# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------

with st.sidebar:
    st.title("Dashboard Filters")

    st.caption(
        "Use the filters below to isolate risk, ownership, "
        "provider, and workflow conditions."
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

    st.divider()

    st.caption(
        "Clear selections manually to return to the full dataset."
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


# ---------------------------------------------------------
# DASHBOARD HEADER
# ---------------------------------------------------------

st.title("☁️ Cloud Governance Operations Center")

st.markdown(
    """
    Executive visibility into governance pipeline health,
    compliance exceptions, operational aging, and risk.
    """
)

header_col_1, header_col_2 = st.columns([3, 1])

with header_col_1:
    st.caption(format_date_range(filtered_df))

with header_col_2:
    st.caption(
        f"Showing **{len(filtered_df):,}** of **{len(df):,}** use cases"
    )

st.divider()


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

kpi_1, kpi_2, kpi_3, kpi_4, kpi_5 = st.columns(5)

with kpi_1:
    st.metric(
        label="Total Requests",
        value=f"{total_requests:,}",
        help="Total governance use cases matching the current filters.",
    )

with kpi_2:
    st.metric(
        label="Critical Risks",
        value=f"{critical_risks:,}",
        help="Use cases currently classified as Critical risk.",
    )

with kpi_3:
    st.metric(
        label="Red Health",
        value=f"{red_health:,}",
        help="Use cases requiring immediate governance attention.",
    )

with kpi_4:
    st.metric(
        label="Missing Evidence",
        value=f"{missing_evidence:,}",
        help="Use cases with incomplete governance evidence.",
    )

with kpi_5:
    st.metric(
        label="Region Exceptions",
        value=f"{region_exceptions:,}",
        help="Use cases operating outside approved cloud regions.",
    )

st.divider()


# ---------------------------------------------------------
# EMPTY-RESULT HANDLING
# ---------------------------------------------------------

if filtered_df.empty:
    st.warning(
        "No governance records match the current filter selection."
    )
    st.stop()


# ---------------------------------------------------------
# CHART ROW 1
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# CHART ROW 2
# ---------------------------------------------------------

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

st.divider()


# ---------------------------------------------------------
# LEADERSHIP EXCEPTION QUEUE
# ---------------------------------------------------------

st.subheader("Leadership Exception Queue")

st.caption(
    "Priority governance items requiring escalation, remediation, "
    "or documented risk acceptance."
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

if "Days in Stage" in exception_queue.columns:
    exception_queue = exception_queue.sort_values(
        by=["Risk Level", "Days in Stage"],
        ascending=[True, False],
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
    )

st.divider()


# ---------------------------------------------------------
# FULL GOVERNANCE PIPELINE
# ---------------------------------------------------------

st.subheader("Full Governance Pipeline")

st.caption(
    "Detailed operational view of all governance requests "
    "matching the current filter selection."
)

st.dataframe(
    filtered_df,
    width="stretch",
    hide_index=True,
)
