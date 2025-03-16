import streamlit as st
import feedparser
import pandas as pd

# Set page config
st.set_page_config(page_title="News Scraper", page_icon="📰", layout="wide")

# Custom CSS for styling
st.markdown("""
    <style>
        /* Increase title size */
        .main-title {
            text-align: center;
            font-size: 4.5rem;
            color: #ff4b4b;
            font-weight: bold;
        }
        .sidebar .sidebar-content {
            background-color: #f7f7f7;
            padding: 10px;
        }
        .footer {
            position: fixed;
            bottom: 0;
            left: 0;
            width: 100%;
            background-color: #f7f7f7;
            text-align: center;
            padding: 10px;
            font-size: 14px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Dictionary of news sources with their RSS feed URLs
news_sources = {
    "BBC News": "http://feeds.bbci.co.uk/news/rss.xml",
    "AajTak": "https://aajtak.intoday.in/rssfeeds/?id=home",
    "Times of India": "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
    "NDTV": "https://feeds.feedburner.com/ndtvnews-top-stories",
    "CNN": "http://rss.cnn.com/rss/edition.rss",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "New York Times": "https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml"
}

def scrape_news(feed_url):
    """Fetch news articles from an RSS feed and return as a DataFrame."""
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries:
        articles.append({
            "Title": entry.title,
            "Link": entry.link,
            "Published Date": entry.published if "published" in entry else "N/A",
            "Summary": entry.summary if "summary" in entry else "No Summary Available",
            "Source": feed_url
        })

    return pd.DataFrame(articles)

# Title with increased size
st.markdown('<p class="main-title">📰 Live News Scraper</p>', unsafe_allow_html=True)
st.write("Select a news website from the sidebar to fetch news.")

# Sidebar
st.sidebar.header("🗞️ Select News Source")
selected_source = st.sidebar.selectbox("Choose a news website:", ["Select a source"] + list(news_sources.keys()))

# Sidebar filters
st.sidebar.header("📌 Select News Details")
all_columns = ["Title", "Summary", "Published Date", "Link", "Source"]
selected_columns = st.sidebar.multiselect(
    "Choose what to display:",
    options=["All"] + all_columns,  
    default=all_columns
)

# If "All" is selected, show all columns
if "All" in selected_columns:
    selected_columns = all_columns

# Only fetch news if a source is selected
if selected_source != "Select a source":
    rss_url = news_sources[selected_source]
    news_df = scrape_news(rss_url)

    if not news_df.empty:
        st.success(f"✅ Fetched latest news from **{selected_source}**!")
        
        # Display only selected columns
        st.dataframe(news_df[selected_columns])

        # Save news to CSV file
        csv_file = f"{selected_source.replace(' ', '_').lower()}_news.csv"
        news_df.to_csv(csv_file, index=False, encoding="utf-8")

        # Provide a download link for CSV file
        with open(csv_file, "rb") as f:
            st.download_button(
                label="📥 Download CSV",
                data=f,
                file_name=csv_file,
                mime="text/csv"
            )
    else:
        st.error("❌ No news articles found. Please try again later.")
else:
    st.warning("⚠ Please select a news source from the sidebar.")

# Footer with LinkedIn at the bottom
st.markdown("""
    <div class="footer">
        👨‍💻 <a href="https://www.linkedin.com/in/mohuzaif/" target="_blank">Connect with me on LinkedIn: Mohd Huzaif 🚀</a>
    </div>
""", unsafe_allow_html=True)
