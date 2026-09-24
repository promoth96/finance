-- ==============================================================================
-- PRODUCTION MULTI-TOUCH ATTRIBUTION (MTA) & PERFORMANCE SQL ENGINE
-- Dialect: Google BigQuery / Snowflake / Databricks ANSI SQL
-- Description:
--   1. Computes First-Touch, Last-Touch, and Linear Attribution using Window Functions.
--   2. Joins touchpoint paths with conversion and spend data.
--   3. Calculates blended and channel-specific ROAS, CAC, and attribution variance.
-- ==============================================================================

WITH TouchpointsNumbered AS (
    SELECT
        user_id,
        touchpoint_order,
        channel,
        campaign_id,
        timestamp,
        -- Window count of total touchpoints in the user journey
        COUNT(1) OVER (PARTITION BY user_id) AS total_touchpoints,
        -- Sequence identifiers
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp ASC) AS asc_rank,
        ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY timestamp DESC) AS desc_rank
    FROM
        `marketing_analytics.user_touchpoints`
),

AttributedWeights AS (
    SELECT
        t.user_id,
        t.touchpoint_order,
        t.channel,
        t.campaign_id,
        t.timestamp,
        t.total_touchpoints,
        c.conversion_id,
        c.revenue,
        
        -- 1. First-Touch Attribution Weight (100% to first touchpoint)
        CASE WHEN t.asc_rank = 1 THEN 1.0 ELSE 0.0 END AS weight_first_touch,
        
        -- 2. Last-Touch Attribution Weight (100% to final touchpoint)
        CASE WHEN t.desc_rank = 1 THEN 1.0 ELSE 0.0 END AS weight_last_touch,
        
        -- 3. Linear Attribution Weight (Equal split: 1 / N)
        (1.0 / t.total_touchpoints) AS weight_linear,
        
        -- 4. Position-Based (U-Shaped 40/20/40) Weight
        CASE
            WHEN t.total_touchpoints = 1 THEN 1.0
            WHEN t.total_touchpoints = 2 THEN 0.50
            WHEN t.asc_rank = 1 THEN 0.40
            WHEN t.desc_rank = 1 THEN 0.40
            ELSE 0.20 / (t.total_touchpoints - 2)
        END AS weight_position_based
    FROM
        TouchpointsNumbered t
    INNER JOIN
        `marketing_analytics.conversions` c
        ON t.user_id = c.user_id
        AND c.timestamp >= t.timestamp -- Ensure touchpoint preceded conversion
),

ChannelAttributionSummary AS (
    SELECT
        channel,
        -- Conversions by Model
        SUM(weight_first_touch) AS conversions_first_touch,
        SUM(weight_last_touch) AS conversions_last_touch,
        SUM(weight_linear) AS conversions_linear,
        SUM(weight_position_based) AS conversions_position,
        
        -- Attributed Revenue by Model
        SUM(revenue * weight_first_touch) AS revenue_first_touch,
        SUM(revenue * weight_last_touch) AS revenue_last_touch,
        SUM(revenue * weight_linear) AS revenue_linear,
        SUM(revenue * weight_position_based) AS revenue_position
    FROM
        AttributedWeights
    GROUP BY
        channel
),

ChannelSpendSummary AS (
    SELECT
        channel,
        SUM(impressions) AS total_impressions,
        SUM(clicks) AS total_clicks,
        SUM(spend) AS total_spend
    FROM
        `marketing_analytics.campaign_performance`
    GROUP BY
        channel
)

SELECT
    s.channel,
    s.total_impressions,
    s.total_clicks,
    s.total_spend,
    
    -- Last-Touch Baseline Metrics
    a.conversions_last_touch,
    ROUND(a.revenue_last_touch, 2) AS revenue_last_touch,
    ROUND(SAFE_DIVIDE(a.revenue_last_touch, s.total_spend), 2) AS roas_last_touch,
    ROUND(SAFE_DIVIDE(s.total_spend, a.conversions_last_touch), 2) AS cac_last_touch,
    
    -- First-Touch Metrics
    a.conversions_first_touch,
    ROUND(a.revenue_first_touch, 2) AS revenue_first_touch,
    ROUND(SAFE_DIVIDE(a.revenue_first_touch, s.total_spend), 2) AS roas_first_touch,
    
    -- Linear Metrics
    ROUND(a.conversions_linear, 2) AS conversions_linear,
    ROUND(a.revenue_linear, 2) AS revenue_linear,
    ROUND(SAFE_DIVIDE(a.revenue_linear, s.total_spend), 2) AS roas_linear,
    
    -- Variance Analysis: Linear vs Last-Touch (% change in attributed revenue)
    ROUND(SAFE_DIVIDE(a.revenue_linear - a.revenue_last_touch, a.revenue_last_touch) * 100, 1) AS linear_vs_last_rev_pct_change
FROM
    ChannelSpendSummary s
LEFT JOIN
    ChannelAttributionSummary a
    ON s.channel = a.channel
ORDER BY
    s.total_spend DESC;
