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

def load_exclude_set(exclude_path="exclude.txt"):
    """
    Load a set of Chinese characters to exclude from a file.
    The file can contain a string of characters or one character per line.
    """
    try:
        with open(exclude_path, encoding="utf-8") as f:
            content = f.read().strip()
            # Treat each character in the content as an excluded character.
            exclude_chars = set(content)
        return exclude_chars
    except Exception as e:
        st.error(f"Error loading exclude file: {e}")
        return set()

# Load dictionary of valid Chinese words and set of characters to exclude.
valid_words = load_chinese_dictionary()
exclude_chars = load_exclude_set()

def extract_valid_bigrams(text, valid_words, exclude_chars):
    """
    Remove non-Chinese characters, exclude any characters found in exclude_chars,
    and return a list of consecutive Chinese character pairs (bigrams)
    that are valid words according to the provided dictionary.
    """
    # Extract only Chinese characters
    pattern = re.compile(r'[\u4e00-\u9fff]+')
    cleaned = ''.join(pattern.findall(text))
    # Remove excluded characters from the cleaned text
    filtered = ''.join([char for char in cleaned if char not in exclude_chars])
    # Create bigrams using a sliding window over the filtered text
    bigrams = [filtered[i:i+2] for i in range(len(filtered) - 1)]
    # Keep only those bigrams that are present in the valid dictionary
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
        bigrams = extract_valid_bigrams(text_input, valid_words, exclude_chars)
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
