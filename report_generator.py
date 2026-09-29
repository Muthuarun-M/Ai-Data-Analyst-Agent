import pandas as pd
import plotly.express as px
import plotly.io as pio
import html


def generate_visual_report(df, analysis):
    """
    Generate a complete HTML visual report containing:
    - Dataset overview
    - Data quality
    - Automatic insights
    - Statistical summary
    - Distribution chart
    - Category chart
    - Scatter plot
    - Correlation heatmap
    - Time-series chart
    """

    # =====================================================
    # BASIC INFORMATION
    # =====================================================

    rows = analysis["rows"]
    columns = analysis["columns"]

    missing_values = int(
        df.isnull().sum().sum()
    )

    duplicates = int(
        df.duplicated().sum()
    )

    numeric_columns = analysis[
        "numeric_columns"
    ]

    categorical_columns = analysis[
        "categorical_columns"
    ]

    datetime_columns = analysis[
        "datetime_columns"
    ]

    insights = analysis[
        "insights"
    ]


    # =====================================================
    # CHART HTML STORAGE
    # =====================================================

    charts = []


    # =====================================================
    # 1. DISTRIBUTION CHART
    # =====================================================

    if numeric_columns:

        selected_column = numeric_columns[0]

        fig = px.histogram(
            df,
            x=selected_column,
            title=f"Distribution of {selected_column}",
            marginal="box"
        )

        fig.update_layout(
            height=500,
            template="plotly_white"
        )

        chart_html = pio.to_html(
            fig,
            full_html=False,
            include_plotlyjs="cdn"
        )

        charts.append(
            f"""
            <section class="chart-section">
                <h2>📈 Distribution Analysis</h2>
                <p>
                    Distribution of
                    <strong>{html.escape(selected_column)}</strong>
                </p>
                {chart_html}
            </section>
            """
        )


    # =====================================================
    # 2. CATEGORY BAR CHART
    # =====================================================

    if categorical_columns and numeric_columns:

        category_column = categorical_columns[0]
        value_column = numeric_columns[0]

        grouped_data = (
            df.groupby(category_column)[value_column]
            .mean()
            .reset_index()
        )

        fig = px.bar(
            grouped_data,
            x=category_column,
            y=value_column,
            title=(
                f"Average {value_column} "
                f"by {category_column}"
            )
        )

        fig.update_layout(
            height=500,
            template="plotly_white"
        )

        chart_html = pio.to_html(
            fig,
            full_html=False,
            include_plotlyjs=False
        )

        charts.append(
            f"""
            <section class="chart-section">
                <h2>🏷️ Category Analysis</h2>
                {chart_html}
            </section>
            """
        )


    # =====================================================
    # 3. SCATTER PLOT
    # =====================================================

    if len(numeric_columns) >= 2:

        x_column = numeric_columns[0]
        y_column = numeric_columns[1]

        fig = px.scatter(
            df,
            x=x_column,
            y=y_column,
            title=f"{x_column} vs {y_column}"
        )

        fig.update_layout(
            height=500,
            template="plotly_white"
        )

        chart_html = pio.to_html(
            fig,
            full_html=False,
            include_plotlyjs=False
        )

        charts.append(
            f"""
            <section class="chart-section">
                <h2>🔗 Relationship Analysis</h2>
                {chart_html}
            </section>
            """
        )


    # =====================================================
    # 4. CORRELATION HEATMAP
    # =====================================================

    if len(numeric_columns) >= 2:

        correlation = (
            df[numeric_columns]
            .corr()
        )

        fig = px.imshow(
            correlation,
            text_auto=True,
            title="Feature Correlation"
        )

        fig.update_layout(
            height=550,
            template="plotly_white"
        )

        chart_html = pio.to_html(
            fig,
            full_html=False,
            include_plotlyjs=False
        )

        charts.append(
            f"""
            <section class="chart-section">
                <h2>🔥 Correlation Analysis</h2>
                {chart_html}
            </section>
            """
        )


    # =====================================================
    # 5. TIME SERIES
    # =====================================================

    if datetime_columns and numeric_columns:

        date_column = datetime_columns[0]
        metric_column = numeric_columns[0]

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

        fig = px.line(
            time_df,
            x=date_column,
            y=metric_column,
            title=f"{metric_column} Over Time"
        )

        fig.update_layout(
            height=500,
            template="plotly_white"
        )

        chart_html = pio.to_html(
            fig,
            full_html=False,
            include_plotlyjs=False
        )

        charts.append(
            f"""
            <section class="chart-section">
                <h2>⏱️ Time-Series Analysis</h2>
                {chart_html}
            </section>
            """
        )


    # =====================================================
    # INSIGHTS HTML
    # =====================================================

    insights_html = ""

    for insight in insights:

        insights_html += f"""
        <div class="insight">
            💡 {html.escape(str(insight))}
        </div>
        """


    # =====================================================
    # COLUMN INFORMATION
    # =====================================================

    numeric_html = "".join(
        f"<li>{html.escape(str(column))}</li>"
        for column in numeric_columns
    )

    categorical_html = "".join(
        f"<li>{html.escape(str(column))}</li>"
        for column in categorical_columns
    )


    # =====================================================
    # STATISTICAL SUMMARY
    # =====================================================

    statistics_html = analysis[
        "statistics"
    ].to_html(
        classes="statistics-table",
        border=0
    )


    # =====================================================
    # FINAL HTML REPORT
    # =====================================================

    report = f"""
<!DOCTYPE html>

<html>

<head>

<meta charset="UTF-8">

<meta name="viewport"
      content="width=device-width, initial-scale=1.0">

<title>AI Data Analyst Report</title>

<style>

body {{
    font-family:
        Arial,
        Helvetica,
        sans-serif;

    background:
        #f4f7fb;

    color:
        #1f2937;

    margin:
        0;

    padding:
        0;
}}

.container {{
    max-width:
        1200px;

    margin:
        auto;

    padding:
        40px 25px;
}}

.header {{
    background:
        linear-gradient(
            135deg,
            #2563eb,
            #1d4ed8
        );

    color:
        white;

    padding:
        40px;

    border-radius:
        18px;

    margin-bottom:
        25px;
}}

.header h1 {{
    margin:
        0;

    font-size:
        36px;
}}

.header p {{
    margin-top:
        10px;

    opacity:
        0.9;

    font-size:
        16px;
}}

.section {{
    background:
        white;

    padding:
        25px;

    border-radius:
        15px;

    margin-bottom:
        25px;

    box-shadow:
        0 2px 10px
        rgba(0,0,0,0.05);
}}

h2 {{
    color:
        #111827;

    margin-top:
        0;
}}

.kpi-grid {{
    display:
        grid;

    grid-template-columns:
        repeat(4, 1fr);

    gap:
        15px;
}}

.kpi {{
    background:
        #f8fafc;

    border:
        1px solid #e5e7eb;

    padding:
        20px;

    border-radius:
        12px;

    text-align:
        center;
}}

.kpi-title {{
    color:
        #6b7280;

    font-size:
        14px;
}}

.kpi-value {{
    color:
        #111827;

    font-size:
        30px;

    font-weight:
        700;

    margin-top:
        8px;
}}

.insight {{
    background:
        #eff6ff;

    border-left:
        4px solid #2563eb;

    padding:
        14px 18px;

    border-radius:
        8px;

    margin-bottom:
        10px;
}}

.columns-grid {{
    display:
        grid;

    grid-template-columns:
        1fr 1fr;

    gap:
        25px;
}}

.column-box {{
    background:
        #f8fafc;

    padding:
        20px;

    border-radius:
        10px;

    border:
        1px solid #e5e7eb;
}}

.statistics-table {{
    width:
        100%;

    border-collapse:
        collapse;

    font-size:
        14px;
}}

.statistics-table th,
.statistics-table td {{
    border:
        1px solid #e5e7eb;

    padding:
        10px;

    text-align:
        right;
}}

.statistics-table th {{
    background:
        #f1f5f9;

    color:
        #111827;
}}

.chart-section {{
    background:
        white;

    padding:
        25px;

    border-radius:
        15px;

    margin-bottom:
        25px;

    box-shadow:
        0 2px 10px
        rgba(0,0,0,0.05);
}}

.footer {{
    text-align:
        center;

    color:
        #6b7280;

    margin-top:
        30px;

    font-size:
        13px;
}}

@media (max-width: 800px) {{

    .kpi-grid {{
        grid-template-columns:
            repeat(2, 1fr);
    }}

    .columns-grid {{
        grid-template-columns:
            1fr;
    }}

    .header h1 {{
        font-size:
            28px;
    }}

}}

</style>

</head>


<body>

<div class="container">


<!-- HEADER -->

<div class="header">

    <h1>📊 AI Data Analyst Report</h1>

    <p>
        Automated dataset analysis,
        insights and visualizations
    </p>

</div>


<!-- DATASET OVERVIEW -->

<div class="section">

    <h2>📌 Dataset Overview</h2>

    <div class="kpi-grid">

        <div class="kpi">

            <div class="kpi-title">
                Rows
            </div>

            <div class="kpi-value">
                {rows:,}
            </div>

        </div>


        <div class="kpi">

            <div class="kpi-title">
                Columns
            </div>

            <div class="kpi-value">
                {columns}
            </div>

        </div>


        <div class="kpi">

            <div class="kpi-title">
                Missing Values
            </div>

            <div class="kpi-value">
                {missing_values}
            </div>

        </div>


        <div class="kpi">

            <div class="kpi-title">
                Duplicate Rows
            </div>

            <div class="kpi-value">
                {duplicates}
            </div>

        </div>

    </div>

</div>


<!-- INSIGHTS -->

<div class="section">

    <h2>🧠 Automatic Insights</h2>

    {insights_html}

</div>


<!-- COLUMN INFORMATION -->

<div class="section">

    <h2>🔎 Column Information</h2>

    <div class="columns-grid">

        <div class="column-box">

            <h3>🔢 Numerical Columns</h3>

            <ul>
                {numeric_html}
            </ul>

        </div>


        <div class="column-box">

            <h3>🏷️ Categorical Columns</h3>

            <ul>
                {categorical_html}
            </ul>

        </div>

    </div>

</div>


<!-- STATISTICS -->

<div class="section">

    <h2>📋 Statistical Summary</h2>

    {statistics_html}

</div>


<!-- CHARTS -->

{''.join(charts)}


<!-- FOOTER -->

<div class="footer">

    Generated by
    <strong>AI Data Analyst Agent</strong>

</div>


</div>

</body>

</html>
"""

    return report