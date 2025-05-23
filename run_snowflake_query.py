"""Run a SQL Server query that pulls data from Snowflake via OPENQUERY.

This script connects to SQL Server and executes a T-SQL statement that 
creates a temporary table (#TDSP) containing data from Snowflake. After
executing the query, it selects the data from the temporary table and
prints the first few rows.

Edit `SQL_SERVER_CONNECTION_STRING` with your connection information
before running the script.
"""

import pyodbc
import pandas as pd

SQL_SERVER_CONNECTION_STRING = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=YOUR_SERVER;'
    'DATABASE=YOUR_DATABASE;'
    'Trusted_Connection=yes;'
)

SNOWFLAKE_QUERY = """
IF OBJECT_ID('tempdb.dbo.#TDSP', 'U') IS NOT NULL
    DROP TABLE #TDSP;

SELECT *
INTO #TDSP
FROM OPENQUERY ([Snowflake],
'
SELECT a.business_partner_id
      ,a.ESI_ID
      ,a.gain_dt
      ,a.loss_dt
      ,a.acquisition_method
      ,a.counttype
      ,a.customer_active_count
      ,a.fica_risk_class
      ,a.product_gp
      ,a.product_desc
      ,a.contract_acct
      ,a.rate_type
      ,a.annual_kwh_qty
      ,a.channel
      ,a.usage_bucket
      ,a.move_in_dt
      ,a.move_out_dt
      ,a.enrlmnt_channel
      ,a.tenure
      ,a.YYYYMMDD AS AlternateDateKey
FROM RETAIL_PRD.USERDB_RESMKT_BUSINTL.CXTHLC_ENDINGS_EOM_CONSOLIDATED a
WHERE a.BRAND_NAME IN (''TXU'')
  AND a.SEGMENT IN (''B_MASS'')');
"""

def main() -> None:
    """Execute the Snowflake query and display a preview of the results."""
    with pyodbc.connect(SQL_SERVER_CONNECTION_STRING) as conn:
        cursor = conn.cursor()
        cursor.execute(SNOWFLAKE_QUERY)
        conn.commit()

        df = pd.read_sql('SELECT * FROM #TDSP', conn)

    print(df.head())


if __name__ == '__main__':
    main()
