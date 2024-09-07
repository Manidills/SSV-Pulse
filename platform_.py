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
    prompt = f"Here SSV network staking protocol  data\n{csv_data_str}\ngive some short summary insights about the data in 6 sentences and in points"
    st.write(chat_bot(prompt))


def platform_():
    st.markdown("##")

    df = pd.read_csv("sql/staking_amount.csv")

    st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('week:T', title='Time'),
            y=alt.Y('active_validators:Q', stack=None, title='active_validators'),
            color=alt.Color('platform_type:N', legend=alt.Legend(title='platform_type'))
        ).properties(
            width=800,
            height=400,
            title='Active Validators'
        ),
        use_container_width=True
    )
    a,b= st.columns([2,2])

    with a:
       st.altair_chart(
        alt.Chart(df).mark_bar().encode(
            x=alt.X('week:T', title='Time'),
            y=alt.Y('amount:Q', stack=None, title='amount'),
            color=alt.Color('platform_type:N', legend=alt.Legend(title='platform_type'))
        ).properties(
            width=800,
            height=400,
            title='Amount'
        ),
        use_container_width=True
    )
       
       st.markdown("##")

       st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('week:T', title='Time'),
            y=alt.Y('net_value_usd:Q', stack=None, title='amount'),
            color=alt.Color('platform_type:N', legend=alt.Legend(title='platform_type'))
        ).properties(
            width=800,
            height=400,
            title='Net_Value_Usd'
        ),
        use_container_width=True
    )
       
       st.markdown("##")

       st.altair_chart(
        alt.Chart(df).mark_bar().encode(
            x=alt.X('week:T', title='Time'),
            y=alt.Y('amount_exited:Q', stack=None, title='amount_exited'),
            color=alt.Color('platform_type:N', legend=alt.Legend(title='platform_type'))
        ).properties(
            width=800,
            height=400,
            title='Amount_Exited'
        ),
        use_container_width=True
    )
       
    with b:

        st.altair_chart(
        alt.Chart(df).mark_bar().encode(
            x=alt.X('week:T', title='Time'),
            y=alt.Y('amount:Q', stack=None, title='amount'),
            color=alt.Color('staking_type:N', legend=alt.Legend(title='staking_type'))
        ).properties(
            width=800,
            height=400,
            title='Amount'
        ),
        use_container_width=True
    )
       
        st.markdown("##")

        st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('week:T', title='Time'),
            y=alt.Y('net_value_usd:Q', stack=None, title='amount'),
            color=alt.Color('staking_type:N', legend=alt.Legend(title='staking_type'))
        ).properties(
            width=800,
            height=400,
            title='Net_Value_Usd'
        ),
        use_container_width=True
    )
       
        st.markdown("##")

        st.altair_chart(
        alt.Chart(df).mark_bar().encode(
            x=alt.X('week:T', title='Time'),
            y=alt.Y('amount_exited:Q', stack=None, title='amount_exited'),
            color=alt.Color('staking_type:N', legend=alt.Legend(title='staking_type'))
        ).properties(
            width=800,
            height=400,
            title='Amount_Exited'
        ),
        use_container_width=True
    )
        

    st.markdown("##")

    df = pd.read_csv("sql/staking_amount.csv")

    st.altair_chart(
        alt.Chart(df).mark_line().encode(
            x=alt.X('week:T', title='Time'),
            y=alt.Y('active_validators:Q', stack=None, title='active_validators'),
            color=alt.Color('staking_type:N', legend=alt.Legend(title='staking_type'))
        ).properties(
            width=800,
            height=400,
            title='Active Validators'
        ),
        use_container_width=True
    )

    st.markdown("##")
    st.dataframe(pd.read_csv("sql/staking_amount.csv"),width=1400)


    generate_summary_p(df)

    generate_summary(df)