import json
import os
import pandas as pd

from dotenv import load_dotenv
from openai import OpenAI


# =========================================================
# ENVIRONMENT
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH, override=True)


# =========================================================
# TOOL 1 — DATASET SUMMARY
# =========================================================

def dataset_summary(df):

    return {
        "rows": int(len(df)),
        "columns": int(len(df.columns)),
        "column_names": df.columns.tolist(),
        "missing_values": int(df.isnull().sum().sum()),
        "duplicate_rows": int(df.duplicated().sum()),
        "numeric_columns": df.select_dtypes(
            include="number"
        ).columns.tolist(),
        "categorical_columns": df.select_dtypes(
            include="object"
        ).columns.tolist()
    }


# =========================================================
# TOOL 2 — COLUMN STATISTICS
# =========================================================

def column_statistics(df, column):

    if column not in df.columns:

        return {
            "error": f"Column '{column}' not found."
        }

    if not pd.api.types.is_numeric_dtype(df[column]):

        return {
            "error": f"Column '{column}' is not numerical."
        }

    return {
        "column": column,
        "mean": float(df[column].mean()),
        "median": float(df[column].median()),
        "minimum": float(df[column].min()),
        "maximum": float(df[column].max()),
        "standard_deviation": float(df[column].std())
    }


# =========================================================
# TOOL 3 — CORRELATION ANALYSIS
# =========================================================

def correlation_analysis(df):

    numeric_df = df.select_dtypes(
        include="number"
    )

    if numeric_df.shape[1] < 2:

        return {
            "error": "At least two numerical columns are required."
        }

    correlation = numeric_df.corr()

    result = {}

    for column in correlation.columns:

        result[column] = {
            other: round(
                float(correlation.loc[column, other]),
                3
            )

            for other in correlation.columns

            if other != column
        }

    return result


# =========================================================
# TOOL 4 — CALCULATE AVERAGE
# =========================================================

def calculate_average(df, column):

    if column not in df.columns:

        return {
            "error": f"Column '{column}' not found."
        }

    if not pd.api.types.is_numeric_dtype(df[column]):

        return {
            "error": f"Column '{column}' is not numerical."
        }

    return {
        "column": column,
        "average": float(df[column].mean())
    }


# =========================================================
# TOOL 5 — MISSING VALUES
# =========================================================

def missing_value_analysis(df):

    missing_by_column = {
        column: int(value)
        for column, value
        in df.isnull().sum().items()
    }

    return {
        "total_missing": int(
            df.isnull().sum().sum()
        ),
        "missing_by_column": missing_by_column
    }


# =========================================================
# TOOL 6 — DUPLICATES
# =========================================================

def duplicate_analysis(df):

    return {
        "duplicate_rows": int(
            df.duplicated().sum()
        )
    }


# =========================================================
# TOOL 7 — OUTLIER ANALYSIS
# =========================================================

def outlier_analysis(df, column):

    if column not in df.columns:

        return {
            "error": f"Column '{column}' not found."
        }

    if not pd.api.types.is_numeric_dtype(df[column]):

        return {
            "error": f"Column '{column}' is not numerical."
        }

    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)

    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    outliers = df[
        (df[column] < lower_bound) |
        (df[column] > upper_bound)
    ]

    return {
        "column": column,
        "outlier_count": int(len(outliers)),
        "lower_bound": float(lower_bound),
        "upper_bound": float(upper_bound),
        "outlier_values": outliers[column].tolist()
    }


# =========================================================
# AI DATA ANALYST AGENT
# =========================================================

def run_agent(df, question):

    # -----------------------------------------------------
    # LOAD ENVIRONMENT
    # -----------------------------------------------------

    load_dotenv(
        ENV_PATH,
        override=True
    )

    api_key = os.environ.get(
        "GROQ_API_KEY"
    )

    if not api_key:

        return (
            "GROQ_API_KEY is not configured. "
            "Please check your .env file."
        )


    # -----------------------------------------------------
    # GROQ CLIENT
    # -----------------------------------------------------

    client = OpenAI(
        api_key=api_key,
        base_url="https://api.groq.com/openai/v1"
    )


    # =====================================================
    # TOOLS
    # =====================================================

    tools = [

        # -------------------------------------------------
        # DATASET SUMMARY
        # -------------------------------------------------

        {
            "type": "function",

            "function": {

                "name": "dataset_summary",

                "description": (
                    "Get the dataset size, column names, "
                    "missing values, duplicate rows, "
                    "numerical columns and categorical columns."
                ),

                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },


        # -------------------------------------------------
        # CALCULATE AVERAGE
        # -------------------------------------------------

        {
            "type": "function",

            "function": {

                "name": "calculate_average",

                "description": (
                    "Calculate the average of a "
                    "numerical column."
                ),

                "parameters": {

                    "type": "object",

                    "properties": {

                        "column": {
                            "type": "string",
                            "description":
                                "Name of the numerical column"
                        }
                    },

                    "required": [
                        "column"
                    ]
                }
            }
        },


        # -------------------------------------------------
        # COLUMN STATISTICS
        # -------------------------------------------------

        {
            "type": "function",

            "function": {

                "name": "column_statistics",

                "description": (
                    "Calculate mean, median, minimum, "
                    "maximum and standard deviation "
                    "of a numerical column."
                ),

                "parameters": {

                    "type": "object",

                    "properties": {

                        "column": {
                            "type": "string",
                            "description":
                                "Name of the numerical column"
                        }
                    },

                    "required": [
                        "column"
                    ]
                }
            }
        },


        # -------------------------------------------------
        # CORRELATION
        # -------------------------------------------------

        {
            "type": "function",

            "function": {

                "name": "correlation_analysis",

                "description": (
                    "Calculate correlations between "
                    "all numerical columns."
                ),

                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },


        # -------------------------------------------------
        # MISSING VALUES
        # -------------------------------------------------

        {
            "type": "function",

            "function": {

                "name": "missing_value_analysis",

                "description": (
                    "Find missing values in each column "
                    "and return the total number."
                ),

                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },


        # -------------------------------------------------
        # DUPLICATES
        # -------------------------------------------------

        {
            "type": "function",

            "function": {

                "name": "duplicate_analysis",

                "description": (
                    "Find the number of duplicate rows "
                    "in the dataset."
                ),

                "parameters": {
                    "type": "object",
                    "properties": {},
                    "required": []
                }
            }
        },


        # -------------------------------------------------
        # OUTLIERS
        # -------------------------------------------------

        {
            "type": "function",

            "function": {

                "name": "outlier_analysis",

                "description": (
                    "Detect potential outliers in a "
                    "numerical column using the IQR method."
                ),

                "parameters": {

                    "type": "object",

                    "properties": {

                        "column": {
                            "type": "string",
                            "description":
                                "Name of the numerical column"
                        }
                    },

                    "required": [
                        "column"
                    ]
                }
            }
        }
    ]


    # =====================================================
    # SYSTEM PROMPT
    # =====================================================

    messages = [

        {
            "role": "system",

            "content": """
You are an AI Data Analyst Agent.

Your job is to analyze the user's uploaded dataset.

IMPORTANT RULES:

1. Use the available tools whenever actual
   dataset calculations are required.

2. Never invent numerical results.

3. Use the exact values returned by the tools.

4. After receiving a tool result, answer the
   user's question directly.

5. Do not call another tool after you already
   have enough information to answer.

6. For dataset description questions, use
   dataset_summary and then provide a clear
   natural-language description.

7. Keep answers clear and concise.

8. Mention important numbers when relevant.

9. If a tool returns an error, explain the
   error clearly to the user.
"""
        },

        {
            "role": "user",
            "content": question
        }
    ]


    # =====================================================
    # AI REQUEST
    # =====================================================

    try:

        # -------------------------------------------------
        # FIRST AI CALL
        # -------------------------------------------------

        response = client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=messages,

            tools=tools,

            tool_choice="auto"
        )


        message = response.choices[0].message


        # -------------------------------------------------
        # NO TOOL REQUIRED
        # -------------------------------------------------

        if not message.tool_calls:

            return message.content


        # -------------------------------------------------
        # ADD ASSISTANT TOOL CALL MESSAGE
        # -------------------------------------------------

        assistant_tool_calls = []

        for tool_call in message.tool_calls:

            assistant_tool_calls.append(
                {
                    "id": tool_call.id,

                    "type": "function",

                    "function": {
                        "name":
                            tool_call.function.name,

                        "arguments":
                            tool_call.function.arguments
                    }
                }
            )


        messages.append(
            {
                "role": "assistant",

                "content":
                    message.content,

                "tool_calls":
                    assistant_tool_calls
            }
        )


        # =================================================
        # EXECUTE TOOLS
        # =================================================

        for tool_call in message.tool_calls:

            tool_name = (
                tool_call.function.name
            )

            try:

                arguments = json.loads(
                    tool_call.function.arguments
                )

            except json.JSONDecodeError:

                arguments = {}


            # ---------------------------------------------
            # DATASET SUMMARY
            # ---------------------------------------------

            if tool_name == "dataset_summary":

                result = dataset_summary(df)


            # ---------------------------------------------
            # CALCULATE AVERAGE
            # ---------------------------------------------

            elif tool_name == "calculate_average":

                column = arguments.get(
                    "column"
                )

                result = calculate_average(
                    df,
                    column
                )


            # ---------------------------------------------
            # COLUMN STATISTICS
            # ---------------------------------------------

            elif tool_name == "column_statistics":

                column = arguments.get(
                    "column"
                )

                result = column_statistics(
                    df,
                    column
                )


            # ---------------------------------------------
            # CORRELATION
            # ---------------------------------------------

            elif tool_name == "correlation_analysis":

                result = correlation_analysis(
                    df
                )


            # ---------------------------------------------
            # MISSING VALUES
            # ---------------------------------------------

            elif tool_name == "missing_value_analysis":

                result = missing_value_analysis(
                    df
                )


            # ---------------------------------------------
            # DUPLICATES
            # ---------------------------------------------

            elif tool_name == "duplicate_analysis":

                result = duplicate_analysis(
                    df
                )


            # ---------------------------------------------
            # OUTLIERS
            # ---------------------------------------------

            elif tool_name == "outlier_analysis":

                column = arguments.get(
                    "column"
                )

                result = outlier_analysis(
                    df,
                    column
                )


            # ---------------------------------------------
            # UNKNOWN TOOL
            # ---------------------------------------------

            else:

                result = {
                    "error":
                        f"Unknown tool: {tool_name}"
                }


            # ---------------------------------------------
            # ADD TOOL RESULT
            # ---------------------------------------------

            messages.append(
                {
                    "role": "tool",

                    "tool_call_id":
                        tool_call.id,

                    "name":
                        tool_name,

                    "content":
                        json.dumps(
                            result,
                            default=str
                        )
                }
            )


        # =================================================
        # FINAL AI RESPONSE
        # =================================================

        final_response = client.chat.completions.create(

            model="openai/gpt-oss-120b",

            messages=messages,

            tool_choice="none"
        )


        final_message = (
            final_response
            .choices[0]
            .message
            .content
        )


        if not final_message:

            return (
                "The analysis was completed, "
                "but the AI did not return a response."
            )


        return final_message


    # =====================================================
    # ERROR HANDLING
    # =====================================================

    except Exception as e:

        return (
            f"Groq API Error: {str(e)}"
        )