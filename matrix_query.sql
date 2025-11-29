/*
Query to produce gain counts by ScottChannel with monthly columns for
2024 (Jan–Dec) and 2025 (Jan–Jun). The data comes from the
Mass_Plan_Proj_Actual table.  Each column represents the total GAINs for
the respective month.
*/

WITH SourceData AS (
    SELECT
        LEFT(a.YEARMONTH,4)  AS YearLook,
        RIGHT(a.YEARMONTH,2) AS MonthLook,
        CASE WHEN a.CHANNEL IN ('WEB PHONE REACTIVE', 'REACTIVE', 'CALL CENTER') THEN 'CALL CENTER'
        CASE WHEN a.CHANNEL IN ('WEB PHONE REACTIVE', 'REACTIVE', 'CALL CENTER') THEN 'Reactive'
             WHEN a.CHANNEL IN ('WEB SEARCH', 'WEB_SEARCH')             THEN 'Web Search'
             WHEN a.CHANNEL IN ('ONLINE PARTNER')                      THEN 'SOE'
             WHEN a.CHANNEL IN ('RAQ','REQUEST A QUOTE','TEE.COM')     THEN 'RAQ'
             WHEN a.CHANNEL IN ('OUTBOUND','AGILE','OBTM')             THEN 'Agile'
             WHEN a.CHANNEL IN ('DIRECT MAIL','DM')                    THEN 'DM'
             WHEN a.CHANNEL IN ('BAAT')                                THEN 'BAAT'
             WHEN a.CHANNEL IN ('PARTNERSHIPS/EVENTS')                 THEN 'Partnerships/Events'
             WHEN a.CHANNEL IN ('BD_MASS - POLR')                      THEN 'POLR'
             WHEN (a.CHANNEL IN ('UNK','BD_LBM','LBM','DOOR TO DOOR','SPECIALTY_MKT','') OR a.CHANNEL IS NULL)
                  THEN 'Other'
             ELSE 'Unknown'
        END AS MatrixChannel,
        CASE WHEN a.CUSTOMER_FLAG IN ('B_MASS_TERM') THEN 'TERM' ELSE 'MTM' END AS TermMTM,
        SUM(a.GAIN) AS Gains
    FROM Skywalker.dbo.Mass_Plan_Proj_Actual a
    WHERE a.CATEGORY IN ('MASS_PORTFOLIO_ACTUAL')
      AND (a.BRAND_NAME IN ('TXU') OR a.BRAND_NAME IS NULL)
      AND LEFT(a.YEARMONTH,4) IN ('2024','2025')
      AND a.CUSTOMER_FLAG IN ('B_MASS_MTM', 'B_MASS_TERM')
      AND a.CHANNEL NOT IN ('BD_MASS')
    GROUP BY
        a.YEARMONTH,
        CASE WHEN a.CHANNEL IN ('WEB PHONE REACTIVE', 'REACTIVE', 'CALL CENTER') THEN 'CALL CENTER'
        CASE WHEN a.CHANNEL IN ('WEB PHONE REACTIVE', 'REACTIVE', 'CALL CENTER') THEN 'Reactive'
             WHEN a.CHANNEL IN ('WEB SEARCH', 'WEB_SEARCH')             THEN 'Web Search'
             WHEN a.CHANNEL IN ('ONLINE PARTNER')                      THEN 'SOE'
             WHEN a.CHANNEL IN ('RAQ','REQUEST A QUOTE','TEE.COM')     THEN 'RAQ'
             WHEN a.CHANNEL IN ('OUTBOUND','AGILE','OBTM')             THEN 'Agile'
             WHEN a.CHANNEL IN ('DIRECT MAIL','DM')                    THEN 'DM'
             WHEN a.CHANNEL IN ('BAAT')                                THEN 'BAAT'
             WHEN a.CHANNEL IN ('PARTNERSHIPS/EVENTS')                 THEN 'Partnerships/Events'
             WHEN a.CHANNEL IN ('BD_MASS - POLR')                      THEN 'POLR'
             WHEN (a.CHANNEL IN ('UNK','BD_LBM','LBM','DOOR TO DOOR','SPECIALTY_MKT','') OR a.CHANNEL IS NULL)
                  THEN 'Other'
             ELSE 'Unknown'
        END,
        CASE WHEN a.CUSTOMER_FLAG IN ('B_MASS_TERM') THEN 'TERM' ELSE 'MTM' END
)
,
ScottChannels AS (
    SELECT
        YearLook,
        MonthLook,
        CASE WHEN MatrixChannel IN ('CALL CENTER','Partnerships/Events','Other','Unknown')
        CASE WHEN MatrixChannel IN ('Reactive','Partnerships/Events','Other','Unknown')
                  THEN 'Reactive'
             ELSE MatrixChannel
        END AS ScottChannel,
        TermMTM,
        SUM(Gains) AS GainCount
    FROM SourceData
    GROUP BY
        YearLook,
        MonthLook,
        CASE WHEN MatrixChannel IN ('CALL CENTER','Partnerships/Events','Other','Unknown')
        CASE WHEN MatrixChannel IN ('Reactive','Partnerships/Events','Other','Unknown')
                  THEN 'Reactive'
             ELSE MatrixChannel
        END,
        TermMTM
)

SELECT ScottChannel,
       [202401],[202402],[202403],[202404],[202405],[202406],
       [202407],[202408],[202409],[202410],[202411],[202412],
       [202501],[202502],[202503],[202504],[202505],[202506]
FROM ScottChannels
PIVOT (
    SUM(GainCount)
    FOR (YearLook + MonthLook) IN (
        [202401],[202402],[202403],[202404],[202405],[202406],
        [202407],[202408],[202409],[202410],[202411],[202412],
        [202501],[202502],[202503],[202504],[202505],[202506]
    )
) AS p
SELECT
    ScottChannel,
    [202401],[202402],[202403],[202404],[202405],[202406],
    [202407],[202408],[202409],[202410],[202411],[202412],
    [202501],[202502],[202503],[202504],
    CASE WHEN ScottChannel = 'SOE' THEN ISNULL([202505],0) + 285
         WHEN ScottChannel = 'Reactive' THEN ISNULL([202505],0) - 285
         ELSE [202505] END AS [202505],
    [202506]
FROM (
    SELECT ScottChannel,
           [202401],[202402],[202403],[202404],[202405],[202406],
           [202407],[202408],[202409],[202410],[202411],[202412],
           [202501],[202502],[202503],[202504],[202505],[202506]
    FROM ScottChannels
    PIVOT (
        SUM(GainCount)
        FOR (YearLook + MonthLook) IN (
            [202401],[202402],[202403],[202404],[202405],[202406],
            [202407],[202408],[202409],[202410],[202411],[202412],
            [202501],[202502],[202503],[202504],[202505],[202506]
        )
    ) AS p
) adj
ORDER BY ScottChannel;
