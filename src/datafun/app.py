"""src/datafun/app.py - Project script.

Author: Holly Praiswater
Date: 2026-09

HOW TO RUN THIS FILE:

From the VS Code menu (with only this project open in VS Code),
click "Terminal" / New Terminal to
open an integrated Terminal in the root project folder.
Paste the following command and press ENTER or RETURN
to run this file as a script:

uv run python -m datafun.app

DOMAIN:

A small business with regions, stores, employees and sales.

The data is stored in four related CSV files:

- one row per region
- one row per store
- one row per employee
- one row per sale

One region can have many stores.
One store can have many employees.
One store can have many sales.

EXPLORE:

Sometimes the information needed for an analysis
is stored in more than one related table.

SQL is especially useful when tables share keys
and we want to analyze information across them.

A simple Python and SQL process is:

1. LOAD the related tables.
2. INSPECT the grain and keys.
3. CREATE a SQLite database.
4. LOAD the tables into SQLite.
5. QUERY across related tables with SQL.
6. VISUALIZE the query result with Python.
7. SUMMARIZE what you found.
8. DISPLAY the visualization.

DESIGN:

Use this file to declare the data-specific choices
and the reasoning behind them,
then orchestrate the work.

SQLite comes from the Python Standard Library.
Pandas loads tabular data into SQLite
and returns SQL query results as DataFrames.
Reusable visualization functions come from eda-vizkit.

The SQL stays here because the query is an
analytical decision specific to this project.
"""

# === DECLARE IMPORTS (BRING IN FREE CODE) ===

import logging
from pathlib import Path
import sqlite3
from typing import Final

from datafun_toolkit.logger import get_logger, log_header, log_path
from eda_vizkit import save_chart
import matplotlib.pyplot as plt
import pandas as pd

# === CONFIGURE LOGGER ONCE FOR THE APPLICATION ===

LOG: logging.Logger = get_logger("P05", level="DEBUG")

# === DECLARE GLOBAL CONSTANTS ===

# Some global variables are CONSTANT.
# They do NOT change while the program runs.
# By convention, constants use UPPERCASE_WITH_UNDERSCORES.
# Final indicates that the value should not be reassigned.

# === LOCATE THE DATA FILES ===

DATA_DIR: Final[Path] = Path("data") / "retail"

REGION_FILE: Final[Path] = DATA_DIR / "region.csv"
STORE_FILE: Final[Path] = DATA_DIR / "store.csv"
EMPLOYEE_FILE: Final[Path] = DATA_DIR / "employee.csv"
SALE_FILE: Final[Path] = DATA_DIR / "sale.csv"

# === LOCATE THE SQLITE DATABASE ===

DATABASE_FILE: Final[Path] = DATA_DIR / "business.sqlite"

# === LOCATE THE CHART OUTPUT ===

CHART_DIR: Final[Path] = Path("docs") / "images"
STORE_SIZE_CHART_PATH: Final[Path] = CHART_DIR / "store-size-vs-sales.png"
EMPLOYEE_SALES_CHART_PATH: Final[Path] = CHART_DIR / "employee-count-vs-sales.png"

# === DETERMINE WHAT ONE ROW REPRESENTS ===

REGION_GRAIN: Final[str] = "one business region"
STORE_GRAIN: Final[str] = "one store"
EMPLOYEE_GRAIN: Final[str] = "one employee"
SALE_GRAIN: Final[str] = "one sale"

# === DESCRIBE THE TABLE RELATIONSHIPS ===

RELATIONSHIP_DECISION: Final[str] = r"""
The data is stored in four related tables.

One region can have many stores.
The stores table uses region_id to identify each store's region.

One store can have many employees.
The employees table uses store_id to identify each employee's store.

One store can have many sales.
The sales table uses store_id to identify each sale's store.

The shared keys connect information stored in different tables.
"""

# === DEFINE THE ANALYTICAL QUESTION ===

CUSTOM_QUERY_DECISION: Final[str] = r"""
I want to explore factors that may be related to store sales performance.

I will compare total sales across stores and examine whether store size or employee count has a relationship with total sales. I will also compare sales per employee to account for differences in staffing between stores.

The analysis uses related information from the stores, employees, and sales tables. The shared store_id connects the tables.
"""

# === WRITE THE SQL QUERY ===


SALES_BY_STORE_QUERY: Final[str] = """
SELECT
    r.region_name,
    s.store_name,
    SUM(sa.sale_amount) AS total_sales
FROM stores AS s
JOIN sales AS sa
    ON s.store_id = sa.store_id
JOIN regions AS r
    ON s.region_id = r.region_id
GROUP BY
    r.region_name,
    s.store_name
ORDER BY
    total_sales DESC;
"""

SALES_BY_REGION_QUERY: Final[str] = """
SELECT
    r.region_name,
    SUM(sa.sale_amount) AS total_sales
FROM regions AS r
JOIN stores AS s
    ON r.region_id = s.region_id
JOIN sales AS sa
    ON s.store_id = sa.store_id
GROUP BY
    r.region_name
ORDER BY
    total_sales DESC;
"""

SALES_BY_STORE_TYPE_QUERY: Final[str] = """
SELECT
    s.store_type,
    SUM(sa.sale_amount) AS total_sales
FROM stores AS s
JOIN sales AS sa
    ON s.store_id = sa.store_id
GROUP BY
    s.store_type
ORDER BY
    total_sales DESC;
"""

SALES_BY_SQUARE_FEET_QUERY: Final[str] = """
SELECT
    s.store_name,
    s.square_feet,
    SUM(sa.sale_amount) AS total_sales
FROM stores AS s
JOIN sales AS sa
    ON s.store_id = sa.store_id
GROUP BY
    s.store_name,
    s.square_feet
ORDER BY
    s.square_feet ASC;
"""

SALES_PER_EMPLOYEE_QUERY: Final[str] = """
WITH employee_counts AS(
    SELECT
        store_id,
        COUNT(employee_id) AS employee_count
    FROM employees
    GROUP BY
        store_id
    ),
    store_sales AS (
        SELECT
            store_id,
            SUM(sale_amount) AS total_sales
        FROM sales
        GROUP BY
            store_id
    )
    SELECT
        s.store_name,
        ec.employee_count,
        ss.total_sales,
        ROUND(ss.total_sales / ec.employee_count, 2) AS sales_per_employee
    FROM stores AS s
    JOIN employee_counts AS ec
        ON s.store_id = ec.store_id
    JOIN store_sales AS ss
        ON s.store_id = ss.store_id
    ORDER BY
        sales_per_employee DESC;
    """

# === CHOOSE A VISUALIZATION ===

CUSTOM_CHART_DECISION: Final[str] = r"""
I chose scatter plots to compare store size and employee count with total sales.

Scatterplots are useful for comparing two numerical variables and make it easier to see whether there appears to be a relationship between them.

I will compare store size with total sales and employee count with total sales. I will also calculate the correlation coefficient for each relationship.
"""


# === DEFINE THE MAIN FUNCTION ===


def main() -> None:
    """Entry point when running this file as a Python script.

    This is where the instructions begin.

    Arguments: None.
    Returns: None.
    """
    log_header(LOG, "P05 - PYTHON AND SQL")

    LOG.info("===================================")
    LOG.info("START main()")
    LOG.info("===================================")

    LOG.info("-------------------------------")
    LOG.info("01. LOAD the related tables.")
    LOG.info("-------------------------------")

    log_path(LOG, "regions file", path=REGION_FILE)
    log_path(LOG, "stores file", path=STORE_FILE)
    log_path(LOG, "employees file", path=EMPLOYEE_FILE)
    log_path(LOG, "sales file", path=SALE_FILE)

    regions_df: pd.DataFrame = pd.read_csv(REGION_FILE)
    stores_df: pd.DataFrame = pd.read_csv(STORE_FILE)
    employees_df: pd.DataFrame = pd.read_csv(EMPLOYEE_FILE)
    sales_df: pd.DataFrame = pd.read_csv(SALE_FILE)

    LOG.info("Related tables loaded successfully.")

    LOG.info("-------------------------------")
    LOG.info("02. INSPECT the grain and keys.")
    LOG.info("-------------------------------")

    LOG.info(f"Regions grain: {REGION_GRAIN}")
    LOG.info(f"Stores grain: {STORE_GRAIN}")
    LOG.info(f"Employees grain: {EMPLOYEE_GRAIN}")
    LOG.info(f"Sales grain: {SALE_GRAIN}")

    LOG.info(f"Regions columns: {regions_df.columns.tolist()}")
    LOG.info(f"Stores columns: {stores_df.columns.tolist()}")
    LOG.info(f"Employees columns: {employees_df.columns.tolist()}")
    LOG.info(f"Sales columns: {sales_df.columns.tolist()}")

    LOG.info(RELATIONSHIP_DECISION)

    LOG.info("-------------------------------")
    LOG.info("03. CREATE a SQLite database.")
    LOG.info("-------------------------------")

    log_path(LOG, "SQLite database", path=DATABASE_FILE)

    connection: sqlite3.Connection = sqlite3.connect(DATABASE_FILE)

    LOG.info("SQLite database connection created.")

    LOG.info("-------------------------------")
    LOG.info("04. LOAD the tables into SQLite.")
    LOG.info("-------------------------------")

    regions_df.to_sql(
        "regions",
        connection,
        if_exists="replace",
        index=False,
    )

    stores_df.to_sql(
        "stores",
        connection,
        if_exists="replace",
        index=False,
    )

    employees_df.to_sql(
        "employees",
        connection,
        if_exists="replace",
        index=False,
    )

    sales_df.to_sql(
        name="sales",
        con=connection,
        if_exists="replace",
        index=False,
    )

    LOG.info("Related tables loaded into SQLite.")

    LOG.info("-------------------------------")
    LOG.info("05. QUERY across related tables with SQL.")
    LOG.info("-------------------------------")

    LOG.info(CUSTOM_QUERY_DECISION)

    sales_by_store_df: pd.DataFrame = pd.read_sql_query(
        SALES_BY_STORE_QUERY,
        connection,
    )

    sales_by_region_df: pd.DataFrame = pd.read_sql_query(
        SALES_BY_REGION_QUERY,
        connection,
    )

    sales_by_store_type_df: pd.DataFrame = pd.read_sql_query(
        sql=SALES_BY_STORE_TYPE_QUERY,
        con=connection,
    )

    sales_by_square_feet_df: pd.DataFrame = pd.read_sql_query(
        sql=SALES_BY_SQUARE_FEET_QUERY,
        con=connection,
    )

    sales_per_employee_df: pd.DataFrame = pd.read_sql_query(
        sql=SALES_PER_EMPLOYEE_QUERY,
        con=connection,
    )

    LOG.info(f"\nSales by store: \n{sales_by_store_df.to_string(index=False)}")
    LOG.info(f"\nSales by region:\n{sales_by_region_df.to_string(index=False)}")
    LOG.info(f"\nSales by store type:\n{sales_by_store_type_df.to_string(index=False)}")
    LOG.info(
        f"\nSales by square feet:\n{sales_by_square_feet_df.to_string(index=False)}"
    )

    correlation = sales_by_square_feet_df["square_feet"].corr(
        sales_by_square_feet_df["total_sales"]
    )

    LOG.info(f"Correlation between store size and total sales: {correlation:.3f}")

    LOG.info(f"\nSales per employee:\n{sales_per_employee_df.to_string(index=False)}")

    employee_sales_correlation = sales_per_employee_df["employee_count"].corr(
        sales_per_employee_df["total_sales"]
    )

    LOG.info(
        f"Correlation between employee count and total sales: "
        f"{employee_sales_correlation:.3f}"
    )

    LOG.info("-------------------------------")
    LOG.info("06. VISUALIZE the query result with Python.")
    LOG.info("-------------------------------")

    LOG.info(CUSTOM_CHART_DECISION)

    CHART_DIR.mkdir(parents=True, exist_ok=True)

    sales_size_ax = sales_by_square_feet_df.plot.scatter(
        x="square_feet",
        y="total_sales",
    )

    sales_size_ax.set_title("Store Size vs. Total Sales")
    sales_size_ax.set_xlabel("Store Size (Square Feet)")
    sales_size_ax.set_ylabel("Total Sales ($)")

    save_chart(
        sales_size_ax,
        STORE_SIZE_CHART_PATH,
    )

    LOG.info(f"Chart saved sucessfully at {STORE_SIZE_CHART_PATH}.")

    employee_sales_ax = sales_per_employee_df.plot.scatter(
        x="employee_count",
        y="total_sales",
    )

    employee_sales_ax.set_title("Employee Count vs. Total Sales")
    employee_sales_ax.set_xlabel("Number of Employees")
    employee_sales_ax.set_ylabel("Total Sales ($)")

    save_chart(
        employee_sales_ax,
        EMPLOYEE_SALES_CHART_PATH,
    )

    LOG.info(f"Chart saved successfully at {EMPLOYEE_SALES_CHART_PATH}.")

    LOG.info("-------------------------------")
    LOG.info("07. SUMMARIZE what you found.")
    LOG.info("-------------------------------")

    # Run this app first.
    # Review the SQL result and visualization.
    # Then record your CUSTOM observations
    # in a simple multi-line raw string.

    LOG.info(r"""CUSTOM OBSERVATIONS:
    Total sales varied across the stores in the dataset.

    The correlation between store size and total sales was 0.185, which indicates a weak positive relationship. Larger stores did not necessarily have higher total sales.

    The correlation between employee count and total sales was 0.335. This was also a weak positive relationship, although it was stronger than the relationship between store size and total sales.

    Sales per employee also varied across stores. The stores with the highest total sales were not always the stores with the highest sales per employee.
    """)

    LOG.info("-------------------------------")
    LOG.info("08. DISPLAY the visualization.")
    LOG.info("-------------------------------")

    LOG.info("In a script, call plt.show() at the end to display all charts.")
    LOG.info("Close all chart windows (with the close button) to continue.")

    plt.show()

    connection.close()

    LOG.info("===================================")
    LOG.info("END main() - Executed successfully!")
    LOG.info("===================================")


# === CONDITIONAL EXECUTION GUARD ===

# WHY: This is standard Python "boilerplate" - we copy and paste it
# into every Python script. It is a "conditional execution" guard,
# meaning: if this file is being run as a script, then execute the code
# in the main() function.

if __name__ == "__main__":
    main()
