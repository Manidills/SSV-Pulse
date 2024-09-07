import streamlit as st

from dashboard import dashboard_stake
from fees import fees
from graph import graph

# Set page configuration
st.set_page_config(page_title="Shanthi Transport & Logistics", page_icon="🚛", layout="wide")

# Increase font size for better readability
st.markdown("""
<style>
body {
    font-size: 60px;
}
</style>
""", unsafe_allow_html=True)

# Create columns for the logo and navigation
col1, col2 = st.columns([1, 3])

with col1:
    st.image("https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDFjb2UzaWFwMnZqZWE1b2N3Yjc5OTltYzdxM2h5YXY2MWd6MXBxbyZlcD12MV9pbnRlcm5naWZfYnlfaWQmY3Q9cw/UAragLbg9oKRfZLThq/giphy.webp", width=250)

with col2:
    new_title = '<p style="font-family:cursive; color:green; font-size: 70px;">SSV-PULSE</p>'
    st.markdown(new_title, unsafe_allow_html=True)
    section = st.radio("Navigate to", ["Home", "ETH_STAKE", "Fees", "Graph", "Contact Us"], horizontal=True)



if section == "ETH_STAKE":
    dashboard_stake()
elif section == "Fees":
    fees()
elif section == "Graph":
    graph()