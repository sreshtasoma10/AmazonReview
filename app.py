import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import time
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Correct ChromeDriver path (use raw string or double backslashes)
chrome_driver_path = r"C:\Users\somas\Downloads\chromedriver-win64 (2)\chromedriver-win64\chromedriver.exe"

def scrape_amazon_reviews(url, driver_path):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    time.sleep(3)

    reviews = []
    while True:
        review_elements = driver.find_elements(By.CSS_SELECTOR, ".review-text-content span")
        for element in review_elements:
            reviews.append(element.text.strip())

        try:
            next_button = driver.find_element(By.CSS_SELECTOR, "li.a-last a")
            if "a-disabled" in next_button.get_attribute("class"):
                break
            next_button.click()
            time.sleep(3)
        except Exception:
            break

    driver.quit()
    return reviews

def analyze_sentiment(reviews):
    analyzer = SentimentIntensityAnalyzer()
    sentiments = []
    for review in reviews:
        score = analyzer.polarity_scores(review)
        compound = score['compound']
        if compound >= 0.05:
            sentiment = "Positive"
        elif compound <= -0.05:
            sentiment = "Negative"
        else:
            sentiment = "Neutral"
        sentiments.append((review, sentiment))
    return sentiments

# Streamlit UI
st.title("Amazon Product Review Sentiment Analysis")

url = st.text_input("Enter Amazon Product Review URL")
if st.button("Analyze"):
    if url:
        with st.spinner("Scraping and analyzing reviews..."):
            try:
                reviews = scrape_amazon_reviews(url, chrome_driver_path)
                if reviews:
                    results = analyze_sentiment(reviews)
                    df = pd.DataFrame(results, columns=["Review", "Sentiment"])

                    # Display DataFrame
                    st.subheader("Sentiment Table")
                    st.dataframe(df)

                    # Display Sentiment Distribution Graph
                    st.subheader("Sentiment Distribution")
                    sentiment_counts = df['Sentiment'].value_counts().reset_index()
                    sentiment_counts.columns = ['Sentiment', 'Count']
                    sns.set(style="whitegrid")
                    fig, ax = plt.subplots()
                    sns.barplot(x="Sentiment", y="Count", data=sentiment_counts, ax=ax, palette="pastel")
                    st.pyplot(fig)
                else:
                    st.warning("No reviews found on the given page.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid URL.")
