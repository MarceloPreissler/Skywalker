"""Run a query in Snowflake, export the results to CSV, and load them into SQL Server.

Edit the connection details for Snowflake and SQL Server before running.
"""

import os
import pandas as pd
import snowflake.connector
import pyodbc

# Snowflake connection information - replace with your credentials
SNOWFLAKE_ACCOUNT = 'YOUR_ACCOUNT'
SNOWFLAKE_USER = 'YOUR_USER'
SNOWFLAKE_PASSWORD = 'YOUR_PASSWORD'
SNOWFLAKE_WAREHOUSE = 'YOUR_WAREHOUSE'
SNOWFLAKE_DATABASE = 'RETAIL_PRD'
SNOWFLAKE_SCHEMA = 'USERDB_RESMKT'

# SQL Server connection string - replace with your server information
SQL_SERVER_CONNECTION_STRING = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=YOUR_SQL_SERVER;'
    'DATABASE=Skywalker;'
    'Trusted_Connection=yes;'
)

# Path to save the CSV file
CSV_PATH = (
    r"C:\Users\mp311723\OneDrive - Vistra Corp\SQL SSMS\DGL_Repository"
)

SNOWFLAKE_QUERY = (
    "SELECT *\n"
    "FROM RETAIL_PRD.USERDB_RESMKT.CALL_CENTER_REPORT_AUTO\n"
    "WHERE CALL_DT > '2024-01-01'"
)


def fetch_from_snowflake() -> pd.DataFrame:
    """Retrieve data from Snowflake and return it as a DataFrame."""
    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )
    try:
        df = pd.read_sql(SNOWFLAKE_QUERY, conn)
    finally:
        conn.close()
    return df


def save_to_csv(df: pd.DataFrame) -> str:
    """Save the DataFrame to a CSV file and return the path."""
    os.makedirs(CSV_PATH, exist_ok=True)
    csv_file = os.path.join(
        CSV_PATH,
        f"snowflake_export_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
    )
    df.to_csv(csv_file, index=False)
    return csv_file


def map_dtype_to_sql(dtype) -> str:
    """Map pandas dtype to a SQL Server column type."""
    if pd.api.types.is_integer_dtype(dtype):
        return 'INT'
    if pd.api.types.is_float_dtype(dtype):
        return 'FLOAT'
    if pd.api.types.is_datetime64_any_dtype(dtype):
        return 'DATETIME'
    return 'NVARCHAR(MAX)'


def create_sql_table(cursor, df: pd.DataFrame):
    """Create Skywalker.dbo.MP_SnowflakeData with columns from the DataFrame."""
    cursor.execute(
        """
        IF OBJECT_ID('Skywalker.dbo.MP_SnowflakeData', 'U') IS NOT NULL
            DROP TABLE Skywalker.dbo.MP_SnowflakeData;
        """
    )

    columns = [
        f"[{col}] {map_dtype_to_sql(dtype)}"
        for col, dtype in zip(df.columns, df.dtypes)
    ]
    create_stmt = (
        "CREATE TABLE Skywalker.dbo.MP_SnowflakeData (" +
        ", ".join(columns) +
        ")"
    )
    cursor.execute(create_stmt)


def insert_into_sql_server(df: pd.DataFrame):
    """Insert DataFrame rows into the SQL Server table."""
    with pyodbc.connect(SQL_SERVER_CONNECTION_STRING) as conn:
        cursor = conn.cursor()
        create_sql_table(cursor, df)
        conn.commit()

        insert_stmt = (
            "INSERT INTO Skywalker.dbo.MP_SnowflakeData (" +
            ", ".join(f"[{c}]" for c in df.columns) +
            ") VALUES (" + ", ".join('?' for _ in df.columns) + ")"
        )
        cursor.fast_executemany = True
        cursor.executemany(insert_stmt, df.itertuples(index=False, name=None))
        conn.commit()


def main() -> None:
    df = fetch_from_snowflake()
    csv_file = save_to_csv(df)
    print(f"Saved Snowflake results to {csv_file}")

    insert_into_sql_server(df)
    print("Data loaded into SQL Server table Skywalker.dbo.MP_SnowflakeData")


if __name__ == '__main__':
    main()
