import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()


# =================================================
# ANSWER USER QUESTION
# =================================================

def answer_question(df, question):

    question = question.lower().strip()

    # Number of rows
    if "how many rows" in question or "number of rows" in question:
        return f"The dataset contains {len(df)} rows."

    # Number of columns
    if "how many columns" in question or "number of columns" in question:
        return f"The dataset contains {len(df.columns)} columns."

    # Missing values
    if "missing" in question:

        total_missing = int(
            df.isnull().sum().sum()
        )

        if total_missing == 0:
            return "The dataset has no missing values."

        return (
            f"The dataset contains "
            f"{total_missing} missing values."
        )

    # Duplicate rows
    if "duplicate" in question:

        duplicates = int(
            df.duplicated().sum()
        )

        return (
            f"The dataset contains "
            f"{duplicates} duplicate rows."
        )

    # Average / Mean
    if "average" in question or "mean" in question:

        for column in df.select_dtypes(
            include="number"
        ).columns:

            if column.lower() in question:

                value = df[column].mean()

                return (
                    f"The average {column} is "
                    f"{value:.2f}."
                )

    # Maximum
    if (
        "highest" in question
        or "maximum" in question
        or "max" in question
    ):

        for column in df.select_dtypes(
            include="number"
        ).columns:

            if column.lower() in question:

                value = df[column].max()

                return (
                    f"The highest {column} is "
                    f"{value:.2f}."
                )

    # Minimum
    if (
        "lowest" in question
        or "minimum" in question
        or "min" in question
    ):

        for column in df.select_dtypes(
            include="number"
        ).columns:

            if column.lower() in question:

                value = df[column].min()

                return (
                    f"The lowest {column} is "
                    f"{value:.2f}."
                )

    return (
        "I couldn't answer that question yet. "
        "Try asking about rows, columns, "
        "missing values, averages, highest "
        "or lowest values."
    )

def ai_answer_question(df, question):

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        return "OPENAI_API_KEY is not configured."

    client = OpenAI(api_key=api_key)

    # Create a compact dataset summary
    numeric_summary = df.describe().to_string()

    column_info = "\n".join(
        [
            f"{column}: {dtype}"
            for column, dtype in df.dtypes.items()
        ]
    )

    missing_values = df.isnull().sum().to_string()

    prompt = f"""
You are an AI Data Analyst.

Analyze the dataset information below and answer
the user's question accurately.

Dataset columns:
{column_info}

Statistical summary:
{numeric_summary}

Missing values:
{missing_values}

User question:
{question}

Rules:
- Answer only using the provided dataset information.
- Do not invent values.
- If the available information is insufficient, say so.
- Explain the answer clearly and briefly.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt
    )

    return response.output_text


# =================================================
# ANALYZE DATASET
# =================================================

def analyze_dataset(df):

    analysis = {}

    # -----------------------------
    # Basic Information
    # -----------------------------

    analysis["rows"] = df.shape[0]
    analysis["columns"] = df.shape[1]

    # -----------------------------
    # Missing Values
    # -----------------------------

    analysis["missing_values"] = (
        df.isnull()
        .sum()
        .sort_values(ascending=False)
    )

    # -----------------------------
    # Duplicate Rows
    # -----------------------------

    analysis["duplicates"] = df.duplicated().sum()

    # -----------------------------
    # Datetime Detection
    # -----------------------------

    datetime_columns = []

    for column in df.columns:

        converted = pd.to_datetime(
            df[column],
            errors="coerce"
        )

        valid_ratio = converted.notna().mean()

        if valid_ratio >= 0.8:
            datetime_columns.append(column)

    analysis["datetime_columns"] = datetime_columns

    # -----------------------------
    # Numerical Columns
    # -----------------------------

    analysis["numeric_columns"] = (
        df.select_dtypes(
            include="number"
        )
        .columns
        .tolist()
    )

    # -----------------------------
    # Categorical Columns
    # -----------------------------

    analysis["categorical_columns"] = (
        df.select_dtypes(
            include="object"
        )
        .columns
        .tolist()
    )

    analysis["categorical_columns"] = [
        column
        for column in analysis["categorical_columns"]
        if column not in datetime_columns
    ]

    # -----------------------------
    # Statistical Summary
    # -----------------------------

    analysis["statistics"] = df.describe()

    # -----------------------------
    # Automatic Insights
    # -----------------------------

    insights = []

    insights.append(
        f"The dataset contains {analysis['rows']} rows "
        f"and {analysis['columns']} columns."
    )

    total_missing = int(
        analysis["missing_values"].sum()
    )

    if total_missing == 0:

        insights.append(
            "No missing values were detected."
        )

    else:

        insights.append(
            f"The dataset contains "
            f"{total_missing} missing values."
        )

    if analysis["duplicates"] == 0:

        insights.append(
            "No duplicate rows were detected."
        )

    else:

        insights.append(
            f"{analysis['duplicates']} duplicate rows "
            f"were detected."
        )

    # -----------------------------
    # Numerical Insights
    # -----------------------------

    for column in analysis["numeric_columns"]:

        mean_value = df[column].mean()
        max_value = df[column].max()
        min_value = df[column].min()

        insights.append(
            f"{column}: average = {mean_value:.2f}, "
            f"minimum = {min_value:.2f}, "
            f"maximum = {max_value:.2f}."
        )

        insights.append(
            f"Highest {column}: {max_value:.2f}."
        )

        insights.append(
            f"Lowest {column}: {min_value:.2f}."
        )

    # -----------------------------
    # Correlation
    # -----------------------------

    if len(analysis["numeric_columns"]) >= 2:

        correlation = df[
            analysis["numeric_columns"]
        ].corr()

        for i in range(len(correlation.columns)):

            for j in range(i + 1, len(correlation.columns)):

                col1 = correlation.columns[i]
                col2 = correlation.columns[j]

                corr_value = correlation.iloc[i, j]

                if abs(corr_value) >= 0.7:

                    insights.append(
                        f"Strong relationship detected between "
                        f"{col1} and {col2} "
                        f"(correlation: {corr_value:.2f})."
                    )

    # -----------------------------
    # Outlier Detection
    # -----------------------------

    for column in analysis["numeric_columns"]:

        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)

        IQR = Q3 - Q1

        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR

        outliers = df[
            (df[column] < lower_bound)
            | (df[column] > upper_bound)
        ]

        if len(outliers) > 0:

            insights.append(
                f"{column} contains "
                f"{len(outliers)} potential outlier(s)."
            )

    # -----------------------------
    # Datetime Insight
    # -----------------------------

    if analysis["datetime_columns"]:

        insights.append(
            "Datetime column(s) detected: "
            + ", ".join(
                analysis["datetime_columns"]
            )
        )

    analysis["insights"] = insights

    return analysis