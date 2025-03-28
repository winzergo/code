import streamlit as st
import pandas as pd
import re
from collections import Counter

def extract_bigrams(text):
    """
    Remove non-Chinese characters and return a list of consecutive Chinese character pairs.
    """
    # Only keep Chinese characters
    pattern = re.compile(r'[\u4e00-\u9fff]')
    cleaned = ''.join(pattern.findall(text))
    # Create bigrams using a sliding window
    bigrams = [cleaned[i:i+2] for i in range(len(cleaned) - 1)]
    return bigrams

# Streamlit UI
st.title("Chinese Bigram Frequency Analyzer")
st.write("Enter your Chinese text below and click **Analyze** to see the frequency of each two-character pair.")

# Text input for Chinese text
text_input = st.text_area("Enter Chinese text:", height=200)

# Analyze button
if st.button("Analyze"):
    if text_input:
        bigrams = extract_bigrams(text_input)
        # Count frequency using Counter
        frequency = Counter(bigrams)
        # Convert the dictionary to a pandas DataFrame and sort by frequency descending
        df = pd.DataFrame(frequency.items(), columns=["Bigram", "Frequency"]).sort_values(by="Frequency", ascending=False)
        st.write("### Bigram Frequency Results")
        st.dataframe(df)
    else:
        st.error("Please enter some Chinese text before clicking Analyze.")
