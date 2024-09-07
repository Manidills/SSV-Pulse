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

@st.cache_resource
def generate_summary(df):
    csv_data_str = df.to_string(index=False)
    prompt = f"Here SSV network staking protocol data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences and suggest us a good time for the investments in points"
    st.write(chat_bot(prompt))

@st.cache_resource
def generate_summary_p(df):
    csv_data_str = df.to_string(index=False)
    prompt = f"Here SSV network staking protocol  data\n{csv_data_str}\ngive some short summary insights about the data in points"
    st.write(chat_bot(prompt))



def fees():
    st.markdown("##")

    df = pd.read_csv("sql/SSV_fee_withdraw.csv")
    st.subheader("SSV fee withdraw")
    st.data_editor(df,width=1400)


    a,b = st.columns([2,2])
    df['data_date'] = pd.to_datetime(df.data_date, errors='coerce')
    with a:
        st.altair_chart(
    alt.Chart(df).mark_bar().encode(
        x=alt.X('data_date:T', title='Hour'),
        y=alt.Y('total_fee_withdrawn:Q', title='total_fee_withdrawn'),
       
    ).properties(
        width=800,
        height=300,
        title='SSV Accumulated Deposit'
    ), use_container_width=True
    )
        
    with b:

        st.altair_chart(
    alt.Chart(df).mark_bar(color='aquamarine').encode(
        x=alt.X('data_date:T', title='Hour'),
        y=alt.Y('accumulated_operator_fee_withdrawn:Q', title='accumulated_operator_fee_withdrawn'),
    ).properties(
        width=800,
        height=300,
        title='SSV  deposited'
    ), use_container_width=True
    )
        
    generate_summary_p(df)
        



    st.markdown("##")

    df = pd.read_csv("sql/SSV_net_deposit.csv")
    st.subheader("SSV net deposit")
    st.data_editor(df,width=1400)


    a,b = st.columns([2,2])
    df['date_time'] = pd.to_datetime(df.date_time, errors='coerce')
    with a:
        st.altair_chart(
    alt.Chart(df).mark_bar(color='wheat').encode(
        x=alt.X('date_time:T', title='Hour'),
        y=alt.Y('accumulated_deposited:Q', title='accumulated_deposited'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_USD:Q', title='Cumulative USD Amount')],
    ).properties(
        width=800,
        height=300,
        title='SSV Accumulated Deposit'
    ), use_container_width=True
    )
        st.markdown("##")

        st.altair_chart(
    alt.Chart(df).mark_bar(color='red').encode(
        x=alt.X('date_time:T', title='Hour'),
        y=alt.Y('accumulated_withdrawn:Q', title='accumulated_withdrawn'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Amount BNB:Q', title='Amount BNB')],
    ).properties(
        width=800,
        height=300,
        title='SSV Accumulated Withdrawn'
    ), use_container_width=True
    )
        
    with b:

        st.altair_chart(
    alt.Chart(df).mark_bar(color='lemonchiffon').encode(
        x=alt.X('date_time:T', title='Hour'),
        y=alt.Y('deposited:Q', title='deposited'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Amount BNB:Q', title='Amount BNB')],
    ).properties(
        width=800,
        height=300,
        title='SSV  deposited'
    ), use_container_width=True
    )
        
        st.markdown("##")

        st.altair_chart(
    alt.Chart(df).mark_bar(color='firebrick').encode(
        x=alt.X('date_time:T', title='Hour'),
        y=alt.Y('withdrawn:Q', title='withdrawn'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Amount BNB:Q', title='Amount BNB')],
    ).properties(
        width=800,
        height=300,
        title='SSV  Withdrawn'
    ), use_container_width=True
    )
        
    generate_summary(df)