import streamlit as st
import pandas as pd
import plotly.express as px

from report_generator import generate_visual_report
from analyzer import analyze_dataset
from agent import run_agent


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Data Analyst",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* =========================
       MAIN APP
       ========================= */

    .stApp {
        background-color: #f8fafc;
        color: #111827;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #f8fafc;
    }

    [data-testid="stHeader"] {
        background-color: #ffffff;
    }


    /* =========================
       MAIN CONTENT
       ========================= */

    .main-title {
        font-size: 42px;
        font-weight: 800;
        color: #111827 !important;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 17px;
        color: #4b5563 !important;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 25px;
        font-weight: 700;
        color: #111827 !important;
        margin-top: 30px;
        margin-bottom: 18px;
    }


    /* =========================
       METRIC CARDS
       ========================= */

    div[data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #e5e7eb;
        padding: 20px;
        border-radius: 14px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    div[data-testid="stMetricLabel"] {
        color: #6b7280 !important;
        font-size: 14px;
        font-weight: 600;
    }

    div[data-testid="stMetricValue"] {
        color: #111827 !important;
        font-size: 30px;
        font-weight: 800;
    }


    /* =========================
       SIDEBAR
       ========================= */

    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e7eb;
    }

    section[data-testid="stSidebar"] * {
        color: #374151;
    }

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #111827 !important;
    }


    /* =========================
       DATAFRAME
       ========================= */

    [data-testid="stDataFrame"] {
        border: 1px solid #e5e7eb;
        border-radius: 10px;
    }


    /* =========================
       EXPANDER
       ========================= */

    [data-testid="stExpander"] {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-radius: 12px;
    }


    /* =========================
       INSIGHT BOX
       ========================= */

    .insight-box {
        background-color: #ffffff;
        border: 1px solid #e5e7eb;
        border-left: 4px solid #2563eb;
        padding: 14px 18px;
        margin-bottom: 10px;
        border-radius: 9px;
        color: #374151 !important;
        box-shadow: 0 2px 6px rgba(0,0,0,0.03);
    }


    /* =========================
       AI BOX
       ========================= */

    .ai-box {
        background: linear-gradient(
            135deg,
            #eff6ff,
            #f8fafc
        );
        border: 1px solid #bfdbfe;
        padding: 24px;
        border-radius: 15px;
        color: #1f2937 !important;
        margin-top: 10px;
    }

    .ai-box b {
        color: #111827 !important;
    }


    /* =========================
       TABS
       ========================= */

    button[data-baseweb="tab"] {
        color: #4b5563 !important;
        font-weight: 600;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #2563eb !important;
    }


    /* =========================
       INPUTS
       ========================= */

    input {
        color: #111827 !important;
        background-color: #ffffff !important;
    }

    textarea {
        color: #111827 !important;
        background-color: #ffffff !important;
    }


    /* =========================
       FILE UPLOADER
       ========================= */

    [data-testid="stFileUploader"] {
        background-color: #ffffff;
        border-radius: 12px;
    }


    /* =========================
       BUTTONS
       ========================= */

    button[kind="primary"] {
        border-radius: 8px;
        font-weight: 600;
    }


    /* =========================
       GENERAL TEXT
       ========================= */

    p, label, span {
        color: #374151;
    }

    h1, h2, h3, h4, h5, h6 {
        color: #111827 !important;
    }
    .ai-box {
    background: linear-gradient(
        135deg,
        #eff6ff,
        #f8fafc
    );
    border: 1px solid #bfdbfe;
    padding: 24px;
    border-radius: 15px;
    color: #1f2937 !important;
    margin-top: 10px;
}

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<div class="main-title">📊 AI Data Analyst</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Upload your dataset, explore insights, visualize patterns, and ask AI questions.'
    '</div>',
    unsafe_allow_html=True
)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.header("📁 Dataset")

    uploaded_file = st.file_uploader(
        "Upload CSV or Excel",
        type=["csv", "xlsx"]
    )

    st.markdown("---")

    st.markdown("### 🚀 Features")

    st.write("✓ Automatic Data Analysis")
    st.write("✓ Interactive Visualizations")
    st.write("✓ Missing Value Detection")
    st.write("✓ Duplicate Detection")
    st.write("✓ Outlier Detection")
    st.write("✓ Correlation Analysis")
    st.write("✓ Time-Series Analysis")
    st.write("✓ AI Data Analyst")


# =========================================================
# NO FILE UPLOADED
# =========================================================

if not uploaded_file:

    st.info(
        "👈 Upload a CSV or Excel dataset from the sidebar to get started."
    )

    st.markdown(
        """
        ### 🔍 What can this AI Data Analyst do?

        **📊 Explore**
        - Dataset dimensions
        - Column types
        - Statistical summary

        **🧠 Analyze**
        - Missing values
        - Duplicate rows
        - Outliers
        - Correlations

        **📈 Visualize**
        - Histograms
        - Bar charts
        - Scatter plots
        - Time-series charts

        **🤖 Ask AI**
        - Ask natural-language questions about your dataset.
        """
    )

    st.stop()


# =========================================================
# LOAD DATASET
# =========================================================

try:

    with st.spinner("Loading dataset..."):

        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)

        else:
            df = pd.read_excel(uploaded_file)

except Exception as e:

    st.error(f"❌ Unable to load dataset: {e}")

    st.stop()


st.success(
    f"✅ {uploaded_file.name} loaded successfully"
)


# =========================================================
# ANALYZE DATASET
# =========================================================

analysis = analyze_dataset(df)

numeric_columns = analysis["numeric_columns"]
categorical_columns = analysis["categorical_columns"]
datetime_columns = analysis["datetime_columns"]


# =========================================================
# KPI CARDS
# =========================================================

st.markdown(
    '<div class="section-title">📌 Dataset Overview</div>',
    unsafe_allow_html=True
)

total_missing = int(df.isnull().sum().sum())
duplicates = int(df.duplicated().sum())

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "Rows",
        f"{len(df):,}"
    )

with col2:

    st.metric(
        "Columns",
        len(df.columns)
    )

with col3:

    st.metric(
        "Missing Values",
        total_missing
    )

with col4:

    st.metric(
        "Duplicate Rows",
        duplicates
    )


# =========================================================
# DATA PREVIEW
# =========================================================

st.markdown(
    '<div class="section-title">📋 Dataset Preview</div>',
    unsafe_allow_html=True
)

with st.expander("View Dataset", expanded=True):

    st.dataframe(
        df.head(20),
        use_container_width=True,
        height=350
    )


# =========================================================
# DATA STRUCTURE
# =========================================================

st.markdown(
    '<div class="section-title">🔎 Data Structure</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 🔢 Numerical Columns")

    if numeric_columns:

        for column in numeric_columns:
            st.write(f"• `{column}`")

    else:

        st.info("No numerical columns detected.")


with col2:

    st.markdown("### 🏷️ Categorical Columns")

    if categorical_columns:

        for column in categorical_columns:
            st.write(f"• `{column}`")

    else:

        st.info("No categorical columns detected.")


# =========================================================
# DATETIME DETECTION
# =========================================================

if datetime_columns:

    st.success(
        "🕒 Datetime detected: "
        + ", ".join(datetime_columns)
    )


# =========================================================
# AI INSIGHTS
# =========================================================

st.markdown(
    '<div class="section-title">🧠 Automatic Insights</div>',
    unsafe_allow_html=True
)

for insight in analysis["insights"]:

    st.markdown(
        f"""
        <div class="insight-box">
        💡 {insight}
        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# ANALYTICS TABS
# =========================================================

st.markdown(
    '<div class="section-title">📊 Data Analytics</div>',
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "📈 Statistics",
        "📊 Distribution",
        "🔗 Relationships",
        "🔥 Correlation",
        "⏱️ Time Series"
    ]
)


# =========================================================
# TAB 1 — STATISTICS
# =========================================================

with tab1:

    st.subheader("📈 Statistical Summary")

    st.dataframe(
        analysis["statistics"],
        use_container_width=True
    )


# =========================================================
# TAB 2 — DISTRIBUTION
# =========================================================

with tab2:

    if numeric_columns:

        selected_numeric = st.selectbox(
            "Select numerical column",
            numeric_columns,
            key="distribution_column"
        )

        fig_hist = px.histogram(
            df,
            x=selected_numeric,
            title=f"Distribution of {selected_numeric}",
            marginal="box"
        )

        fig_hist.update_layout(
            height=500
        )

        st.plotly_chart(
            fig_hist,
            use_container_width=True
        )

    else:

        st.info("No numerical columns available.")


# =========================================================
# TAB 3 — RELATIONSHIPS
# =========================================================

with tab3:

    if len(numeric_columns) >= 2:

        st.subheader("🔗 Numerical Relationships")

        col1, col2 = st.columns(2)

        with col1:

            x_column = st.selectbox(
                "X-axis",
                numeric_columns,
                key="x_axis"
            )

        with col2:

            y_column = st.selectbox(
                "Y-axis",
                numeric_columns,
                key="y_axis"
            )

        fig_scatter = px.scatter(
            df,
            x=x_column,
            y=y_column,
            title=f"{x_column} vs {y_column}"
        )

        st.plotly_chart(
            fig_scatter,
            use_container_width=True
        )

    else:

        st.info(
            "At least two numerical columns are required."
        )


# =========================================================
# CATEGORICAL ANALYSIS
# =========================================================

if categorical_columns and numeric_columns:

    st.subheader("🏷️ Category Analysis")

    col1, col2 = st.columns(2)

    with col1:

        category_column = st.selectbox(
            "Category",
            categorical_columns,
            key="category_column"
        )

    with col2:

        value_column = st.selectbox(
            "Numerical Value",
            numeric_columns,
            key="category_value"
        )

    grouped_data = (
        df.groupby(category_column)[value_column]
        .mean()
        .reset_index()
    )

    fig_bar = px.bar(
        grouped_data,
        x=category_column,
        y=value_column,
        title=f"Average {value_column} by {category_column}"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )


# =========================================================
# TAB 4 — CORRELATION
# =========================================================

with tab4:

    if len(numeric_columns) >= 2:

        correlation = df[numeric_columns].corr()

        fig_corr = px.imshow(
            correlation,
            text_auto=True,
            title="Feature Correlation"
        )

        fig_corr.update_layout(
            height=550
        )

        st.plotly_chart(
            fig_corr,
            use_container_width=True
        )

    else:

        st.info(
            "At least two numerical columns are required."
        )


# =========================================================
# TAB 5 — TIME SERIES
# =========================================================

with tab5:

    if datetime_columns and numeric_columns:

        date_column = st.selectbox(
            "Date / Time Column",
            datetime_columns,
            key="date_column"
        )

        metric_column = st.selectbox(
            "Metric",
            numeric_columns,
            key="time_metric"
        )

        time_df = df.copy()

        time_df[date_column] = pd.to_datetime(
            time_df[date_column],
            errors="coerce"
        )

        time_df = time_df.dropna(
            subset=[date_column]
        )

        time_df = time_df.sort_values(
            date_column
        )

        fig_time = px.line(
            time_df,
            x=date_column,
            y=metric_column,
            title=f"{metric_column} Over Time"
        )

        st.plotly_chart(
            fig_time,
            use_container_width=True
        )

    else:

        st.info(
            "Datetime and numerical columns are required."
        )
# =========================================================
# AI CHAT HISTORY
# =========================================================

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# =========================================================
# VISUAL REPORT DOWNLOAD
# =========================================================

st.markdown(
    '<div class="section-title">📥 Report</div>',
    unsafe_allow_html=True
)

visual_report = generate_visual_report(
    df,
    analysis
)

st.download_button(
    label="📊 Download Visual Report",
    data=visual_report,
    file_name="ai_data_analyst_report.html",
    mime="text/html",
    use_container_width=True
)

# =========================================================
# AI DATA ANALYST
# =========================================================

st.markdown(
    '<div class="section-title">🤖 AI Data Analyst</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="ai-box">
        <b>💡 Ask questions about your dataset</b><br>
        Get data-driven answers using natural language.
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------------

if st.session_state.chat_history:

    st.markdown("### 💬 Conversation")

    for chat in st.session_state.chat_history:

        st.markdown(
            f"""
            <div style="
                background:#eff6ff;
                padding:14px 18px;
                border-radius:12px;
                margin-bottom:8px;
                border:1px solid #dbeafe;
            ">
                <b>👤 You</b><br>
                {chat["question"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div style="
                background:#ffffff;
                padding:14px 18px;
                border-radius:12px;
                margin-bottom:15px;
                border:1px solid #e5e7eb;
            ">
                <b>🤖 AI Data Analyst</b><br>
                {chat["answer"]}
            </div>
            """,
            unsafe_allow_html=True
        )


# ---------------------------------------------------------
# QUESTION INPUT
# ---------------------------------------------------------

question = st.text_input(
    "Ask your question",
    placeholder="Example: What is the average carbon_emissions?",
    key="ai_question"
)


# ---------------------------------------------------------
# BUTTONS
# ---------------------------------------------------------

col1, col2 = st.columns([4, 1])

with col1:

    ask_button = st.button(
        "🤖 Analyze with AI",
        type="primary",
        use_container_width=True
    )

with col2:

    clear_button = st.button(
        "🗑️ Clear",
        use_container_width=True
    )


# ---------------------------------------------------------
# CLEAR CHAT
# ---------------------------------------------------------

if clear_button:

    st.session_state.chat_history = []

    st.rerun()


# ---------------------------------------------------------
# ASK AI
# ---------------------------------------------------------

if ask_button:

    if not question.strip():

        st.warning(
            "Please enter a question first."
        )

    else:

        with st.spinner(
            "🤖 AI Data Analyst is analyzing..."
        ):

            answer = run_agent(
                df,
                question
            )

        st.session_state.chat_history.append(
            {
                "question": question,
                "answer": answer
            }
        )

        st.rerun()