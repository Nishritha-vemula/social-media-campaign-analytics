# 📊 Social Media Campaign Intelligence Dashboard

> An end-to-end data analysis project analyzing 30 campaigns, 527 posts, and 155 ad records across 5 social media platforms — built to demonstrate real-world data analyst skills.

---

## 🎯 Project Objective

To build a complete marketing analytics system that answers real business questions:

- Which platforms and content types drive the most engagement?
- What is the best time and day to post?
- Which campaigns are actually profitable?
- Does caption sentiment and tone affect performance?

---

## 📁 Project Structure

```
social_media_analytics/
├── data/
│   ├── campaigns.csv
│   ├── posts.csv
│   ├── ad_performance.csv
│   ├── audience_demographics.csv
│   └── powerbi_data.xlsx             ← used in Phase 4
├── sql/
│   └── schema_and_queries.sql        ← full schema + 7 analysis queries
├── notebooks/
│   ├── social_media_compaign_analysis.ipynb   ← exploratory data analysis & VADER + TextBlob sentiment analysis
│ 
├── dashboard/
│   └── social_media_dashboard.pbix   ← Power BI 5-page dashboard
├── report/
│   └── executive_summary.docx        ← business recommendations report
├── phase1_data_pipeline.py           ← data generation + MySQL pipeline
└── README.md
```

---

## 🔧 Tech Stack

| Tool | Purpose |
|---|---|
| Python — Pandas, Matplotlib, Seaborn | Data generation, EDA, visualization |
| MySQL + SQLAlchemy | Database design, schema, querying |
| VADER + TextBlob | NLP sentiment analysis on post captions |
| Power BI + DAX | Interactive 5-page business dashboard |

---

## 📋 Project Phases

### Phase 1 — Data Pipeline
- Generated realistic social media campaign data using Python Faker
- Designed a 4-table MySQL database using a star schema
- Built SQL pipeline loading all tables via SQLAlchemy
- Wrote 7 analysis queries covering engagement, ROAS, and demographics

### Phase 2 — Exploratory Data Analysis
- 6 analysis sections covering platforms, content types, timing, and correlations
- Key finding: TikTok leads engagement (9.1%) but Twitter has the most raw reach
- Heatmap revealing best hour-day combinations for posting
- Identified the reach vs engagement paradox — high reach does not guarantee high engagement

### Phase 3 — Sentiment Analysis
- Generated 527 post captions using synthetic data techniques
- Applied VADER (built specifically for social media text) and TextBlob for cross-validation
- Measured subjectivity scores to understand factual vs opinionated content
- Key finding: positive and emotionally opinionated posts consistently outperform neutral ones

### Phase 4 — Power BI Dashboard
- Built a 5-page interactive dashboard (Home navigation + 4 report pages)
- DAX measures for ROAS, CPA, Conversion Rate, Avg Engagement Rate, Sentiment Rate
- Star schema data model connecting all 4 tables via campaign_id
- Page navigation buttons for professional UX

### Phase 5 — Executive Summary
- Business recommendations written for a non-technical audience
- Top 5 actionable insights with estimated impact metrics
- Full technical documentation

---

## 📊 Key Findings

| Finding | Insight |
|---|---|
| Best Platform | TikTok — 9.1% avg engagement rate |
| Best Content Format | Video + Carousel outperform all other formats |
| Best Posting Time | Friday at 6 AM or 9 PM |
| Best Platform for ROI | YouTube — highest median ROAS |
| Sentiment Impact | Positive posts drive higher engagement than neutral |
| Top Converting Audience | 25–34 age group drives most conversions |
| Device Split | Mobile dominates — design all creatives mobile-first |

---

## 💡 Top 3 Recommendations

1. **Shift budget to Video content** — highest engagement per rupee spent across all platforms
2. **Post on Friday at 6 AM or 9 PM** — heatmap analysis confirms these as peak engagement windows
3. **Write with emotion and personality** — opinionated captions consistently outperform factual ones

---

## 🚀 How to Run

```bash
# 1. Clone the repo
git clone https://github.com/Nishritha-vemula/social-media-campaign-analytics.git
cd social-media-campaign-analytics

# 2. Create and activate virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Install dependencies
pip install pandas faker sqlalchemy pymysql mysql-connector-python
pip install matplotlib seaborn jupyter vaderSentiment textblob nltk openpyxl

# 4. Run Phase 1 — generates data + loads into MySQL
python phase1_data_pipeline.py

# 5. Open Phase 2 EDA notebook
jupyter notebook notebooks/social_media_compaign_analysis.ipynb

# 6. Open Phase 3 Sentiment notebook
jupyter notebook notebooks/social_media_compaign_analysis.ipynb

# 7. Open Power BI dashboard
# Open dashboard/social_media_analytics_dashboard.pbix in Power BI Desktop
```

---

## 📸 Dashboard Screenshots

> <img width="1309" height="734" alt="image" src="https://github.com/user-attachments/assets/ac68f04e-c90c-496e-8a70-aa3451c652e7" />

<img width="1323" height="742" alt="image" src="https://github.com/user-attachments/assets/07bca3d9-99bd-462d-acca-53dd71c2b78e" />

<img width="1309" height="737" alt="image" src="https://github.com/user-attachments/assets/56c2495a-cbe7-4f19-8e60-534c965a3aca" />

<img width="1311" height="724" alt="image" src="https://github.com/user-attachments/assets/f090b36e-8ac6-4de0-b96d-8ff78bcb3a14" />

<img width="1310" height="730" alt="image" src="https://github.com/user-attachments/assets/b3a62cbc-b36c-4f17-a693-07487ba4ad60" />



| Page | Description |
|---|---|
| Home | Navigation page with links to all 4 reports |
| Campaign Overview | KPIs, platform breakdown, goal distribution |
| Content & Timing | Engagement heatmap, content type analysis |
| Audience & Demographics | Age, gender, device conversion analysis |
| Ad Performance & ROI | ROAS, CPA, spend vs revenue scatter |

---

## 📬 Contact

**[Your Name]**
📧 nishrithavemula19@gmail.com
💼 [LinkedIn] https://www.linkedin.com/in/nishritha-vemula-2159232a6/
🐙 [GitHub]https://github.com/Nishritha-vemula/

---

*Built as a portfolio project demonstrating end-to-end data analyst skills:
Python · SQL · NLP · Business Intelligence · Data Storytelling*
