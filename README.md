# Snowflake Query Runner

This repository provides example Python scripts for transferring data
between Snowflake and SQL Server.

* `run_snowflake_query.py` demonstrates how to execute a Snowflake query
  from SQL Server using `OPENQUERY`.
* `snowflake_to_sqlserver.py` connects directly to Snowflake, exports the
  results to CSV, and loads them into a SQL Server table.

## Requirements
Install the dependencies with pip:
```bash
pip install pandas pyodbc snowflake-connector-python
```

## `run_snowflake_query.py`
Edit `SQL_SERVER_CONNECTION_STRING` and run:
```bash
python run_snowflake_query.py
```
The script creates a temporary table in SQL Server with data pulled from
Snowflake and prints a preview.

## `snowflake_to_sqlserver.py`
1. Update the Snowflake credentials (`SNOWFLAKE_ACCOUNT`, `SNOWFLAKE_USER`,
   etc.) and the SQL Server connection string.
2. Run:
```bash
python snowflake_to_sqlserver.py
```
This will:
- Query Snowflake for call center data after 2024-01-01.
- Save the results to a CSV file in
  `C:\Users\mp311723\OneDrive - Vistra Corp\SQL SSMS\DGL_Repository`.
- Create the table `Skywalker.dbo.MP_SnowflakeData` and insert the data
  so you can query it from SQL Server.
