import streamlit as st
from ebooklib import epub
from bs4 import BeautifulSoup
import pandas as pd
import re

st.set_page_config(page_title="Laws of Human Nature", layout="centered")

st.title("📘 Laws of Human Nature")
st.write("Consume Robert Greene’s wisdom in byte-sized pieces.")

# File upload
uploaded_file = st.file_uploader("Upload the EPUB file", type="epub")

@st.cache_data
def extract_laws(epub_file):
    book = epub.read_epub(epub_file)
    chapters = []
    for item in book.get_items():
        if item.get_type() == epub.ITEM_DOCUMENT:
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text = soup.get_text(separator=' ', strip=True)
            chapters.append(text)
    full_text = ' '.join(chapters)
    law_blocks = re.findall(r'(LAW\s+#?\d+[:\-–]\s+.*?)(?=LAW\s+#?\d+[:\-–]|$)', full_text, re.DOTALL | re.IGNORECASE)
    
    law_data = []
    for idx, block in enumerate(law_blocks, start=1):
        title_match = re.match(r'LAW\s+#?\d+[:\-–]\s+(.*)', block.strip(), re.IGNORECASE)
        law_name = title_match.group(1).strip() if title_match else f"Law #{idx}"
        law_data.append({
            "Law Number": f"Law #{idx}",
            "Law Text": law_name
        })
    return pd.DataFrame(law_data)

# If file is uploaded
if uploaded_file:
    laws_df = extract_laws(uploaded_file)

    if 'law_index' not in st.session_state:
        st.session_state.law_index = 0

    law = laws_df.iloc[st.session_state.law_index]

    st.markdown(f"### {law['Law Number']}")
    st.markdown(f"**{law['Law Text']}**")

    # Navigation
    col1, col2 = st.columns(2)
    with col1:
        if st.button("⬅️ Previous", disabled=st.session_state.law_index == 0):
            st.session_state.law_index -= 1
    with col2:
        if st.button("Next ➡️", disabled=st.session_state.law_index >= len(laws_df) - 1):
            st.session_state.law_index += 1
else:
    st.info("Please upload the EPUB file to begin.")
