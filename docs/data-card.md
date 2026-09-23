# Data Card

This project uses synthetic retail data generated for this course.

The data is designed for practicing SQL joins, grouping, filtering, aggregation, and visualization with related tables.

## Retail Data

The dataset contains four related CSV files:

- **region.csv** - one row per business region
- **store.csv** - one row per store
- **employee.csv** - one row per employee
- **sale.csv** - one row per sale

## Relationships

The tables are connected using shared keys:

- A region can have many stores.
- A store belongs to one region.
- A store can have many employees.
- An employee belongs to one store.
- A store can have many sales.
- A sale belongs to one store.

The `region_id` field connects the region and store tables.

The `store_id` field connects the store table with the employee and sale tables.

## Analysis

The retail data is used to explore store sales performance, including:

- total sales by store
- total sales by region
- total sales by store type
- the relationship between store size and total sales
- sales per employee
- the relationship between employee count and total sales
