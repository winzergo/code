import streamlit as st
import pandas as pd
import re
from collections import Counter

def load_chinese_dictionary(dict_path="chinese_dictionary.txt"):
    """
    Load a set of valid Chinese words from a file.
    The file should have one word per line.
    """
    try:
        with open(dict_path, encoding="utf-8") as f:
            # Create a set of words, stripping any extra whitespace
            words = {line.strip() for line in f if line.strip()}
        return words
    except Exception as e:
        st.error(f"Error loading dictionary file: {e}")
        return set()

# Load dictionary of valid Chinese words.
valid_words = load_chinese_dictionary()

def extract_valid_bigrams(text, valid_words):
    """
    Remove non-Chinese characters and return a list of consecutive Chinese character pairs
    that are valid words according to the provided dictionary.
    """
    # Keep only Chinese characters by matching one or more occurrences
    pattern = re.compile(r'[\u4e00-\u9fff]+')
    cleaned = ''.join(pattern.findall(text))
    # Create bigrams using a sliding window
    bigrams = [cleaned[i:i+2] for i in range(len(cleaned) - 1)]
    # Filter out bigrams that are not valid Chinese words
    valid_bigrams = [bg for bg in bigrams if bg in valid_words]
    return valid_bigrams

# Streamlit UI
st.title("Chinese Bigram Frequency Analyzer")
st.write("Enter your Chinese text below and click **Analyze** to see the frequency of each valid two-character pair.")

# Text input for Chinese text
text_input = st.text_area("Enter Chinese text:", height=200)

# Analyze button
if st.button("Analyze"):
    if text_input:
        bigrams = extract_valid_bigrams(text_input, valid_words)
        if bigrams:
            # Count frequency using Counter
            frequency = Counter(bigrams)
            # Convert the frequency dictionary to a pandas DataFrame and sort by frequency descending
            df = pd.DataFrame(frequency.items(), columns=["Bigram", "Frequency"]).sort_values(by="Frequency", ascending=False)
            st.write("### Bigram Frequency Results")
            st.dataframe(df)
        else:
            st.write("No valid bigrams found in the text.")
    else:
        st.error("Please enter some Chinese text before clicking Analyze.")
