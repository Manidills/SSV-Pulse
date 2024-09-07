from io import StringIO
import requests
import streamlit as st
import pandas as pd
import datetime
import altair as alt
import time
import os
import g4f

def get_response(prompt):
    url = f"https://api.kastg.xyz/api/ai/chatgptV4?prompt={prompt}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            json_response = response.json()
            if json_response.get("status") == "true" and json_response.get("result"):
                return json_response["result"][0]["response"]
            else:
                return "Error in API response"
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"
    

def chat_bot(prompt):
    response = g4f.ChatCompletion.create(
        # model="gpt-3.5-turbo",
        model=g4f.models.default,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )

    return response
# Define the API endpoint and your API key
API_URL = "https://api.dune.com/api/v1/query/{query_id}/results/csv"
API_KEY = "NJoI9Yz7jPHhaaOmtalgfARPLI9p0x8H"

def fetch_data(api_url, api_key):
    # Prepare headers with API key
    headers = {
        "X-Dune-Api-Key": api_key
    }

    # Make GET request to the API URL with headers
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        # Read CSV data into pandas DataFrame
        df = pd.read_csv(StringIO(response.text))
        return df
    else:
        st.error(f"Failed to load data: {response.status_code} - {response.reason}")
        return None
    
def data(query_id):
    query_id = query_id  # Replace with actual query ID
    api_url = API_URL.format(query_id=query_id)

    df = fetch_data(api_url, API_KEY)

    if df is not None:
        return df
    
@st.cache_resource
def generate_summary(df):
    csv_data_str = df.to_string(index=False)
    prompt = f"Here SSV network staking protocol data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences and suggest us a good time for the investments in points"
    st.write(chat_bot(prompt))

@st.cache_resource
def generate_summary_p(df):
    csv_data_str = df.to_string(index=False)
    prompt = f"Here SSV network staking protocol  data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences and in points"
    st.write(chat_bot(prompt))




def holders():
    st.markdown("##")
    st.subheader("Token Holders")


    df = data("2967498")
    st.data_editor(df, width=1400)
    df['Date'] = pd.to_datetime(df.Date, errors='coerce')
    # Plot the chart
    st.altair_chart(
        alt.Chart(df).mark_area(color='orange').encode(
            x=alt.X('Date:T', title='Hour'),
            y=alt.Y('SSV Token Holders:Q', title='SSV Token Holders')
        ).properties(
            width=800,
            height=300
        ), use_container_width=True
    )

    st.markdown("##")

    st.altair_chart(
        alt.Chart(df).mark_bar(color='pink').encode(
            x=alt.X('Date:T', title='Hour'),
            y=alt.Y('Change in 1 Day:Q', title='Change in 1 Day')
        ).properties(
            width=800,
            height=300
        ), use_container_width=True
    )

    generate_summary_p(df)

    st.markdown("##")

    df = data("2967307")
    st.subheader("Top 100 Holders")

    st.data_editor(df, width=1400)
    generate_summary_p(df)
