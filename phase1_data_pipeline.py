"""
=============================================================
  Social Media Campaign Intelligence Dashboard
  PHASE 1 — Data Generation, Cleaning & SQL Database Setup
=============================================================
Author  : Your Name
Project : Social Media Campaign Analytics
Tools   : Python, SQLite (easily swap to PostgreSQL)
=============================================================
"""

import sqlite3
import random
import os
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
random.seed(42)

# ─────────────────────────────────────────────
# CONFIG
# ─────────────────────────────────────────────
DB_PATH   = "data/social_media_campaigns.db"
CSV_DIR   = "data"
START_DATE = datetime(2024, 1, 1)
END_DATE   = datetime(2024, 12, 31)

PLATFORMS      = ["Instagram", "Twitter", "YouTube", "TikTok", "LinkedIn"]
CONTENT_TYPES  = ["Reel", "Story", "Post", "Video", "Carousel", "Tweet", "Article"]
CAMPAIGN_GOALS = ["Brand Awareness", "Lead Generation", "Sales Conversion", "Engagement", "Retargeting"]
INDUSTRIES     = ["Fashion", "Tech", "Food & Beverage", "Fitness", "Finance", "Travel"]
AD_FORMATS     = ["Image", "Video", "Carousel", "Story Ad", "Sponsored Post"]

# Platform-specific realistic engagement rate ranges
PLATFORM_ENGAGEMENT = {
    "Instagram": (0.03, 0.12),
    "Twitter":   (0.005, 0.04),
    "YouTube":   (0.02, 0.08),
    "TikTok":    (0.05, 0.18),
    "LinkedIn":  (0.02, 0.06),
}

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
def random_date(start: datetime, end: datetime) -> datetime:
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def calc_engagement_rate(likes, comments, shares, reach):
    return round((likes + comments + shares) / reach, 4) if reach > 0 else 0

def calc_ctr(clicks, impressions):
    return round(clicks / impressions, 4) if impressions > 0 else 0

def calc_roas(revenue, spend):
    return round(revenue / spend, 2) if spend > 0 else 0


# ─────────────────────────────────────────────
# TABLE 1: campaigns
# ─────────────────────────────────────────────
def generate_campaigns(n=30):
    print(f"  Generating {n} campaigns...")
    rows = []
    for i in range(1, n + 1):
        start = random_date(START_DATE, END_DATE - timedelta(days=30))
        end   = start + timedelta(days=random.randint(7, 60))
        budget = round(random.uniform(5000, 100000), 2)
        spend  = round(budget * random.uniform(0.6, 1.0), 2)
        rows.append({
            "campaign_id"   : i,
            "campaign_name" : f"Campaign_{fake.bs().title().replace(' ', '_')}_{i}",
            "brand"         : fake.company(),
            "industry"      : random.choice(INDUSTRIES),
            "goal"          : random.choice(CAMPAIGN_GOALS),
            "platform"      : random.choice(PLATFORMS),
            "start_date"    : start.strftime("%Y-%m-%d"),
            "end_date"      : end.strftime("%Y-%m-%d"),
            "budget_usd"    : budget,
            "spend_usd"     : spend,
            "target_audience": random.choice(["18-24", "25-34", "35-44", "45-54", "55+"]),
            "region"        : fake.country(),
            "status"        : random.choice(["Completed", "Active", "Paused"]),
        })
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────
# TABLE 2: posts
# ─────────────────────────────────────────────
def generate_posts(campaigns_df, posts_per_campaign=20):
    print(f"  Generating posts (~{len(campaigns_df) * posts_per_campaign} rows)...")
    rows = []
    post_id = 1
    for _, camp in campaigns_df.iterrows():
        platform  = camp["platform"]
        camp_start = datetime.strptime(camp["start_date"], "%Y-%m-%d")
        camp_end   = datetime.strptime(camp["end_date"],   "%Y-%m-%d")
        if camp_end <= camp_start:
            camp_end = camp_start + timedelta(days=7)

        for _ in range(random.randint(15, posts_per_campaign)):
            post_date  = random_date(camp_start, camp_end)
            reach      = random.randint(1000, 500000)
            impressions= int(reach * random.uniform(1.1, 3.5))
            eng_low, eng_high = PLATFORM_ENGAGEMENT.get(platform, (0.02, 0.10))
            eng_rate   = random.uniform(eng_low, eng_high)
            likes      = int(reach * eng_rate * random.uniform(0.5, 0.8))
            comments   = int(reach * eng_rate * random.uniform(0.05, 0.15))
            shares     = int(reach * eng_rate * random.uniform(0.02, 0.10))
            clicks     = int(impressions * random.uniform(0.01, 0.08))
            saves      = int(likes * random.uniform(0.05, 0.25))

            rows.append({
                "post_id"        : post_id,
                "campaign_id"    : camp["campaign_id"],
                "platform"       : platform,
                "content_type"   : random.choice(CONTENT_TYPES),
                "post_date"      : post_date.strftime("%Y-%m-%d"),
                "post_hour"      : random.randint(0, 23),
                "day_of_week"    : post_date.strftime("%A"),
                "caption_length" : random.randint(20, 500),
                "hashtag_count"  : random.randint(0, 30),
                "has_emoji"      : random.choice([True, False]),
                "reach"          : reach,
                "impressions"    : impressions,
                "likes"          : likes,
                "comments"       : comments,
                "shares"         : shares,
                "saves"          : saves,
                "clicks"         : clicks,
                "engagement_rate": calc_engagement_rate(likes, comments, shares, reach),
                "ctr"            : calc_ctr(clicks, impressions),
                "sentiment_score": round(random.uniform(-1, 1), 3),   # will be recalculated in Phase 3
                "sentiment_label": random.choice(["Positive", "Neutral", "Negative"]),
            })
            post_id += 1
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────
# TABLE 3: ad_performance
# ─────────────────────────────────────────────
def generate_ad_performance(campaigns_df):
    print(f"  Generating ad performance records...")
    rows = []
    ad_id = 1
    for _, camp in campaigns_df.iterrows():
        for _ in range(random.randint(3, 8)):
            spend     = round(camp["spend_usd"] / random.randint(3, 8), 2)
            clicks    = random.randint(100, 10000)
            conversions = int(clicks * random.uniform(0.01, 0.08))
            revenue   = round(conversions * random.uniform(20, 500), 2)
            rows.append({
                "ad_id"         : ad_id,
                "campaign_id"   : camp["campaign_id"],
                "ad_format"     : random.choice(AD_FORMATS),
                "ad_spend_usd"  : spend,
                "impressions"   : random.randint(5000, 200000),
                "clicks"        : clicks,
                "conversions"   : conversions,
                "revenue_usd"   : revenue,
                "ctr"           : calc_ctr(clicks, random.randint(5000, 200000)),
                "cpc"           : round(spend / clicks, 4) if clicks > 0 else 0,
                "cpa"           : round(spend / conversions, 2) if conversions > 0 else 0,
                "roas"          : calc_roas(revenue, spend),
                "date"          : random_date(
                                    datetime.strptime(camp["start_date"], "%Y-%m-%d"),
                                    datetime.strptime(camp["end_date"],   "%Y-%m-%d")
                                  ).strftime("%Y-%m-%d"),
            })
            ad_id += 1
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────
# TABLE 4: audience_demographics
# ─────────────────────────────────────────────
def generate_demographics(campaigns_df):
    print(f"  Generating audience demographics...")
    rows = []
    age_groups = ["13-17", "18-24", "25-34", "35-44", "45-54", "55+"]
    genders    = ["Male", "Female", "Non-binary"]
    devices    = ["Mobile", "Desktop", "Tablet"]
    demo_id    = 1
    for _, camp in campaigns_df.iterrows():
        for age in random.sample(age_groups, k=random.randint(3, 6)):
            for gender in genders:
                rows.append({
                    "demo_id"     : demo_id,
                    "campaign_id" : camp["campaign_id"],
                    "age_group"   : age,
                    "gender"      : gender,
                    "device"      : random.choice(devices),
                    "country"     : fake.country(),
                    "reach"       : random.randint(500, 50000),
                    "clicks"      : random.randint(50, 5000),
                    "conversions" : random.randint(1, 200),
                    "spend_usd"   : round(random.uniform(100, 5000), 2),
                })
                demo_id += 1
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────
# LOAD INTO SQLITE
# ─────────────────────────────────────────────
def load_to_sqlite(dfs: dict, db_path: str):
    print(f"\n  Loading into SQLite → {db_path}")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    for table_name, df in dfs.items():
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print(f"    ✓ {table_name:25s} → {len(df):,} rows loaded")
    conn.close()
    print("  SQLite database ready!\n")


# ─────────────────────────────────────────────
# SAVE CSVs
# ─────────────────────────────────────────────
def save_csvs(dfs: dict, output_dir: str):
    print(f"  Saving CSVs → {output_dir}/")
    os.makedirs(output_dir, exist_ok=True)
    for name, df in dfs.items():
        path = os.path.join(output_dir, f"{name}.csv")
        df.to_csv(path, index=False)
        print(f"    ✓ {name}.csv saved")


# ─────────────────────────────────────────────
# SQL ANALYSIS QUERIES
# ─────────────────────────────────────────────
ANALYSIS_QUERIES = {
    "top_platforms_by_engagement": """
        SELECT
            p.platform,
            COUNT(p.post_id)                        AS total_posts,
            ROUND(AVG(p.engagement_rate) * 100, 2)  AS avg_engagement_pct,
            ROUND(AVG(p.ctr) * 100, 2)              AS avg_ctr_pct,
            SUM(p.reach)                            AS total_reach,
            SUM(p.likes + p.comments + p.shares)    AS total_interactions
        FROM posts p
        GROUP BY p.platform
        ORDER BY avg_engagement_pct DESC
    """,

    "best_content_types": """
        SELECT
            p.content_type,
            COUNT(*)                                AS total_posts,
            ROUND(AVG(p.engagement_rate) * 100, 2) AS avg_engagement_pct,
            ROUND(AVG(p.ctr) * 100, 4)             AS avg_ctr_pct,
            SUM(p.reach)                           AS total_reach
        FROM posts p
        GROUP BY p.content_type
        ORDER BY avg_engagement_pct DESC
    """,

    "best_posting_hour": """
        SELECT
            p.post_hour,
            COUNT(*)                                AS total_posts,
            ROUND(AVG(p.engagement_rate) * 100, 2) AS avg_engagement_pct,
            SUM(p.reach)                           AS total_reach
        FROM posts p
        GROUP BY p.post_hour
        ORDER BY avg_engagement_pct DESC
        LIMIT 10
    """,

    "campaign_roi_summary": """
        SELECT
            c.campaign_name,
            c.platform,
            c.goal,
            c.industry,
            c.spend_usd,
            SUM(a.revenue_usd)                         AS total_revenue,
            ROUND(SUM(a.revenue_usd) / c.spend_usd, 2) AS roas,
            SUM(a.conversions)                         AS total_conversions,
            ROUND(c.spend_usd / NULLIF(SUM(a.conversions), 0), 2) AS cpa
        FROM campaigns c
        LEFT JOIN ad_performance a ON c.campaign_id = a.campaign_id
        GROUP BY c.campaign_id
        ORDER BY roas DESC
        LIMIT 10
    """,

    "day_of_week_performance": """
        SELECT
            p.day_of_week,
            COUNT(*)                                AS total_posts,
            ROUND(AVG(p.engagement_rate) * 100, 2) AS avg_engagement_pct,
            ROUND(AVG(p.ctr) * 100, 4)             AS avg_ctr_pct
        FROM posts p
        GROUP BY p.day_of_week
        ORDER BY avg_engagement_pct DESC
    """,

    "sentiment_by_platform": """
        SELECT
            platform,
            sentiment_label,
            COUNT(*)                              AS post_count,
            ROUND(AVG(engagement_rate) * 100, 2) AS avg_engagement_pct
        FROM posts
        GROUP BY platform, sentiment_label
        ORDER BY platform, post_count DESC
    """,
}


def run_analysis_queries(db_path: str):
    print("  Running SQL analysis queries...\n")
    conn = sqlite3.connect(db_path)
    results = {}
    for query_name, sql in ANALYSIS_QUERIES.items():
        df = pd.read_sql_query(sql, conn)
        results[query_name] = df
        print(f"  ── {query_name.replace('_', ' ').upper()} ──")
        print(df.to_string(index=False))
        print()
    conn.close()
    return results


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  PHASE 1 — Data Generation & SQL Pipeline")
    print("=" * 60)

    # 1. Generate data
    print("\n[1/4] Generating datasets...")
    campaigns    = generate_campaigns(n=30)
    posts        = generate_posts(campaigns, posts_per_campaign=20)
    ad_perf      = generate_ad_performance(campaigns)
    demographics = generate_demographics(campaigns)

    dfs = {
        "campaigns"            : campaigns,
        "posts"                : posts,
        "ad_performance"       : ad_perf,
        "audience_demographics": demographics,
    }

    # Summary
    print("\n  Dataset Summary:")
    for name, df in dfs.items():
        print(f"    {name:25s} → {len(df):,} rows × {len(df.columns)} columns")

    # 2. Save CSVs
    print("\n[2/4] Saving raw CSVs...")
    save_csvs(dfs, CSV_DIR)

    # 3. Load into SQLite
    print("\n[3/4] Loading into SQLite database...")
    load_to_sqlite(dfs, DB_PATH)

    # 4. Run SQL analysis
    print("[4/4] Running exploratory SQL queries...")
    run_analysis_queries(DB_PATH)

    print("=" * 60)
    print("  ✅ Phase 1 Complete!")
    print(f"  Database : {DB_PATH}")
    print(f"  CSVs     : {CSV_DIR}/")
    print("=" * 60)


if __name__ == "__main__":
    main()
