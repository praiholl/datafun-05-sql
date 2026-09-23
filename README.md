# datafun-05-sql

[![Workflow Guide](https://img.shields.io/badge/Pro--Guide-pro--analytics--02-green)](https://denisecase.github.io/pro-analytics-02/workflow-b-apply-example-project/)
[![Python 3.14](https://img.shields.io/badge/python-3.14%2B-blue?logo=python)](./pyproject.toml)
[![uv managed](https://img.shields.io/badge/uv-managed-DE5FE9)](https://docs.astral.sh/uv/)
[![ty type checked](https://img.shields.io/badge/ty-type_checked-2F80ED)](https://docs.astral.sh/ty/)
[![marimo](https://img.shields.io/badge/marimo-reactive_notebook-FF6B6B)](https://docs.marimo.io/)
[![SQLite](https://img.shields.io/badge/SQLite-database-003B57?logo=sqlite&logoColor=white)](https://www.sqlite.org/)
[![Zensical docs](https://img.shields.io/badge/Zensical-docs-purple)](https://zensical.org/)
[![MIT](https://img.shields.io/badge/license-see%20LICENSE-yellow.svg)](./LICENSE)

> A Python and SQL project exploring factors related to store sales performance.

This project uses related retail data to explore store sales using SQL, SQLite, pandas, and Python visualizations.

The analysis compares sales across stores and examines whether store size and employee count are related to total sales. It also compares sales per employee to account for differences in staffing between stores.

The retail data is stored in four related tables:

- regions
- stores
- employees
- sales

These tables are connected using shared keys such as `region_id` and `store_id`.

## Motivation

Business data is often stored across multiple related tables rather than in a single file. SQL makes it possible to connect these tables and analyze information from different parts of a business.

For this project, I wanted to explore store sales performance and determine whether factors such as store size and number of employees appear to be related to total sales. I also wanted to compare sales per employee to see how store performance changes when staffing levels are considered.

## This Project

This project uses relational retail data and SQL to analyze store sales performance.

The analysis uses four related tables containing information about regions, stores, employees, and sales. SQL queries combine and summarize these tables to explore several aspects of the data.

The project examines:

- total sales by store
- total sales by region
- total sales by store type
- the relationship between store size and total sales
- sales per employee
- the relationship between employee count and total sales

The analysis uses SQLite for the relational database, SQL for querying the data, pandas for working with query results, and Python for calculating correlations and creating visualizations.

## Produced Artifacts

This project produces several outputs from the retail sales analysis:

- a SQLite database containing the related retail tables
- SQL query results in `project.log`
- correlation calculations comparing store characteristics with total sales
- scatter plots showing the relationships between store size, employee count, and total sales


## Initial Results

### Store Size vs. Total Sales

![Store Size vs. Total Sales](docs/images/store-size-vs-sales.png)

The correlation between store size and total sales was 0.185, indicating a weak positive relationship. Larger stores did not necessarily have higher total sales.

### Employee Count vs. Total Sales

![Employee Count vs. Total Sales](docs/images/employee-count-vs-sales.png)

The correlation between employee count and total sales was 0.335, also indicating a weak positive relationship. This relationship was stronger than the relationship between store size and total sales, but it was still weak.

Sales per employee also varied across stores, showing that stores with the highest total sales were not always the stores with the highest sales per employee.

## Important Folders and Files

- **data/retail/** - CSV input files and the generated SQLite database
- **docs/images/** - generated charts from the analysis
- **src/datafun/app.py** - main Python and SQL analysis
- **project.log** - logged query results, correlations, and project output
- **zensical.toml** - documentation site configuration
- **pyproject.toml** - project metadata and dependencies


## Command Reference

The commands below are used in the workflow guide above.
They are provided here for convenience.

Follow the guide for the **full instructions**.

<details>
<summary>Show command reference</summary>

### In a machine terminal (open in your `Repos` folder)

Open a machine terminal in your `Repos` folder,
change directory (cd) into the new folder,
and run `code .` to open only this example project in VS Code:

```shell
git clone https://github.com/praiholl/datafun-05-sql

cd datafun-05-sql
code .
```

### In a VS Code terminal

These are listed for convenience.
For best results, follow the detailed instructions in
[pro-analytics-02 guide](https://denisecase.github.io/pro-analytics-02/).

Use VS Code menu option `Terminal` / `New Terminal` to open a **VS Code terminal**
in the root project folder.
Copy each command, paste into your terminal, and hit ENTER,
to run each command one at a time.

```shell
uv self update
uv python pin 3.14
uv python install
uv lock --upgrade
uv sync

uv run pre-commit install
uv run pre-commit autoupdate

git add -A
uv run pre-commit run --all-files
# repeat if changes were made by pre-commit tasks
git add -A
uv run pre-commit run --all-files

# run the Python module
uv run python -m datafun.app

# run marimo nb as a reactive app
# press Ctrl + C in the terminal to exit
uv run marimo run src/datafun/notebook.py

# Or: run marimo nb as a notebook
uv run marimo edit src/datafun/notebook.py

# do chores
uv run ruff format .
uv run ruff check . --fix
uv run ty check
uv run python -m pytest
uv run python -m zensical build

# save progress as you work
git add -A
git commit -m "your message here"
# repeat if changes were made (try the UP ARROW)
git add -A
git commit -m "your message here"

git push -u origin main
```

</details>

## Helpful Tips

- Use the **UP ARROW** and **DOWN ARROW** in the terminal
  to scroll through past commands.
- Use `CTRL+f` to find (and replace) text within a file.

## Much Can Be Ignored

- You do not need to add to or modify `tests/`.
  Tests are recommended and provided for example only.
- Many files are silent helpers.
  [Explore](https://denisecase.github.io/professional-python-project-explainer/)
  as you like, but most files are never touched.
- You do NOT need to understand everything;
  let understanding build over time.

## As Needed

If VS Code does not automatically use the new `.venv` environment:

1. Open the Command Palette (`Ctrl+Shift+P`).
2. Run **Python: Select Interpreter**.
3. Select the interpreter from this project's `.venv` folder.

If VS Code still does not recognize the environment or newly installed tools:

1. Open the Command Palette (`Ctrl+Shift+P`).
2. Run **Developer: Reload Window**.

## Troubleshooting >>>

If you see something like this in your terminal: `>>>` or `...`
You accidentally started Python interactive mode.
It happens.
Press `Ctrl c` (both keys together) or `Ctrl+Z` then `Enter` on Windows.

## Documentation

- [Documentation](https://praiholl.github.io/datafun-05-sql/)

## Annotations

- [.annotations/annotations.md](./.annotations/annotations.md)

## Citation

- [CITATION.cff](./CITATION.cff)

## License

This project is licensed under the [MIT License](./LICENSE).
