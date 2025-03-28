import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def count_live_words(url):
    # Use a browser-like user-agent to avoid simple blocking
    headers = {"User-Agent": "Mozilla/5.0 (compatible; YourAppName/1.0)"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        # Parse HTML content
        soup = BeautifulSoup(response.text, "html.parser")
        # Remove script and style elements
        for element in soup(["script", "style"]):
            element.extract()
        # Get clean text and replace newlines and extra spaces
        text = soup.get_text(separator=" ")
        text = " ".join(text.split())
        # Use regex to count occurrences of the word "live" (case-insensitive)
        count = len(re.findall(r'\blive\b', text, flags=re.IGNORECASE))
        return count, text
    else:
        return None, None

def main():
    st.title("CNN.com 'live' Word Counter")
    st.write("This tool crawls CNN.com and calculates how many times the word **live** appears on the homepage.")

    url = "https://www.cnn.com"
    st.write("Fetching content from:", url)
    count, text = count_live_words(url)

    if count is not None:
        st.success(f"The word 'live' appears **{count}** times on cnn.com.")
        
        # Create a DataFrame with the result for display using pandas
        df = pd.DataFrame({"Word": ["live"], "Count": [count]})
        st.dataframe(df)
        
        # Optionally, let the user view a snippet of the crawled text
        if st.checkbox("Show a snippet of the crawled text"):
            st.text_area("Crawled Text (first 1000 characters)", text[:1000], height=250)
    else:
        st.error("Failed to fetch content from cnn.com. Please check your internet connection or the URL.")

if __name__ == "__main__":
    main()
