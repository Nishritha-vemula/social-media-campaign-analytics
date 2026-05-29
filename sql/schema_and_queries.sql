-- ============================================================
--  Social Media Campaign Intelligence Dashboard
--  SQL Schema & Analysis Queries Reference
-- ============================================================

-- ─────────────────────────────────────────────
-- SCHEMA DEFINITION
-- ─────────────────────────────────────────────

CREATE TABLE IF NOT EXISTS campaigns (
    campaign_id      INTEGER PRIMARY KEY,
    campaign_name    TEXT    NOT NULL,
    brand            TEXT,
    industry         TEXT,
    goal             TEXT,     -- Brand Awareness | Lead Generation | Sales Conversion | Engagement | Retargeting
    platform         TEXT,     -- Instagram | Twitter | YouTube | TikTok | LinkedIn
    start_date       DATE,
    end_date         DATE,
    budget_usd       REAL,
    spend_usd        REAL,
    target_audience  TEXT,     -- Age bracket e.g. 18-24
    region           TEXT,
    status           TEXT      -- Active | Completed | Paused
);

CREATE TABLE IF NOT EXISTS posts (
    post_id          INTEGER PRIMARY KEY,
    campaign_id      INTEGER REFERENCES campaigns(campaign_id),
    platform         TEXT,
    content_type     TEXT,     -- Reel | Story | Post | Video | Carousel | Tweet | Article
    post_date        DATE,
    post_hour        INTEGER,  -- 0-23
    day_of_week      TEXT,
    caption_length   INTEGER,
    hashtag_count    INTEGER,
    has_emoji        BOOLEAN,
    reach            INTEGER,
    impressions      INTEGER,
    likes            INTEGER,
    comments         INTEGER,
    shares           INTEGER,
    saves            INTEGER,
    clicks           INTEGER,
    engagement_rate  REAL,     -- (likes+comments+shares) / reach
    ctr              REAL,     -- clicks / impressions
    sentiment_score  REAL,     -- -1.0 to 1.0 (recalculated in Phase 3)
    sentiment_label  TEXT      -- Positive | Neutral | Negative
);

CREATE TABLE IF NOT EXISTS ad_performance (
    ad_id            INTEGER PRIMARY KEY,
    campaign_id      INTEGER REFERENCES campaigns(campaign_id),
    ad_format        TEXT,
    ad_spend_usd     REAL,
    impressions      INTEGER,
    clicks           INTEGER,
    conversions      INTEGER,
    revenue_usd      REAL,
    ctr              REAL,     -- clicks / impressions
    cpc              REAL,     -- spend / clicks
    cpa              REAL,     -- spend / conversions
    roas             REAL,     -- revenue / spend
    date             DATE
);

CREATE TABLE IF NOT EXISTS audience_demographics (
    demo_id          INTEGER PRIMARY KEY,
    campaign_id      INTEGER REFERENCES campaigns(campaign_id),
    age_group        TEXT,
    gender           TEXT,
    device           TEXT,     -- Mobile | Desktop | Tablet
    country          TEXT,
    reach            INTEGER,
    clicks           INTEGER,
    conversions      INTEGER,
    spend_usd        REAL
);


-- ─────────────────────────────────────────────
-- ANALYSIS QUERY 1: Platform Performance
-- ─────────────────────────────────────────────
SELECT
    p.platform,
    COUNT(p.post_id)                        AS total_posts,
    ROUND(AVG(p.engagement_rate) * 100, 2)  AS avg_engagement_pct,
    ROUND(AVG(p.ctr) * 100, 2)              AS avg_ctr_pct,
    SUM(p.reach)                            AS total_reach,
    SUM(p.likes + p.comments + p.shares)    AS total_interactions
FROM posts p
GROUP BY p.platform
ORDER BY avg_engagement_pct DESC;


-- ─────────────────────────────────────────────
-- ANALYSIS QUERY 2: Best Content Types
-- ─────────────────────────────────────────────
SELECT
    content_type,
    COUNT(*)                                AS total_posts,
    ROUND(AVG(engagement_rate) * 100, 2)   AS avg_engagement_pct,
    ROUND(AVG(ctr) * 100, 4)               AS avg_ctr_pct,
    SUM(reach)                             AS total_reach
FROM posts
GROUP BY content_type
ORDER BY avg_engagement_pct DESC;


-- ─────────────────────────────────────────────
-- ANALYSIS QUERY 3: Best Posting Hours
-- ─────────────────────────────────────────────
SELECT
    post_hour,
    COUNT(*)                                AS total_posts,
    ROUND(AVG(engagement_rate) * 100, 2)   AS avg_engagement_pct,
    SUM(reach)                             AS total_reach
FROM posts
GROUP BY post_hour
ORDER BY avg_engagement_pct DESC
LIMIT 10;


-- ─────────────────────────────────────────────
-- ANALYSIS QUERY 4: Campaign ROI / ROAS
-- ─────────────────────────────────────────────
SELECT
    c.campaign_name,
    c.platform,
    c.goal,
    c.industry,
    c.spend_usd,
    SUM(a.revenue_usd)                              AS total_revenue,
    ROUND(SUM(a.revenue_usd) / c.spend_usd, 2)     AS roas,
    SUM(a.conversions)                              AS total_conversions,
    ROUND(c.spend_usd / NULLIF(SUM(a.conversions),0), 2) AS cpa
FROM campaigns c
LEFT JOIN ad_performance a ON c.campaign_id = a.campaign_id
GROUP BY c.campaign_id
ORDER BY roas DESC
LIMIT 10;


-- ─────────────────────────────────────────────
-- ANALYSIS QUERY 5: Day of Week Performance
-- ─────────────────────────────────────────────
SELECT
    day_of_week,
    COUNT(*)                                AS total_posts,
    ROUND(AVG(engagement_rate) * 100, 2)   AS avg_engagement_pct,
    ROUND(AVG(ctr) * 100, 4)               AS avg_ctr_pct
FROM posts
GROUP BY day_of_week
ORDER BY avg_engagement_pct DESC;


-- ─────────────────────────────────────────────
-- ANALYSIS QUERY 6: Sentiment vs Engagement by Platform
-- ─────────────────────────────────────────────
SELECT
    platform,
    sentiment_label,
    COUNT(*)                               AS post_count,
    ROUND(AVG(engagement_rate) * 100, 2)  AS avg_engagement_pct
FROM posts
GROUP BY platform, sentiment_label
ORDER BY platform, post_count DESC;


-- ─────────────────────────────────────────────
-- ANALYSIS QUERY 7: Audience Demographics – Top Converting Segments
-- ─────────────────────────────────────────────
SELECT
    age_group,
    gender,
    device,
    SUM(reach)                                     AS total_reach,
    SUM(conversions)                               AS total_conversions,
    ROUND(SUM(conversions) * 1.0 / SUM(reach), 4) AS conversion_rate,
    SUM(spend_usd)                                 AS total_spend,
    ROUND(SUM(spend_usd) / NULLIF(SUM(conversions),0), 2) AS cpa
FROM audience_demographics
GROUP BY age_group, gender, device
ORDER BY conversion_rate DESC
LIMIT 15;
