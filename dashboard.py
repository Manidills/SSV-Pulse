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



def dashboard_stake():
    a,b,c= st.columns([2,2,2])
    with a:
        st.metric("Validators_num", "43,422")
    with b:
        st.metric("ETH_stake", "1,389,504")
    with c:
        st.metric("User_addresses", "380")
    st.markdown("##")



    a,b = st.columns([2,2])
    df = pd.read_csv('sql/eth_stake_validators.csv')
    df['day'] = pd.to_datetime(df.day, errors='coerce')
    # Define the date of interest
    nov_2023 = pd.Timestamp('2023-11-01')

    # Filter the rows where 'day' is greater than November 2023
    df = df[df['day'] > nov_2023]
    with a:
        st.altair_chart(
    alt.Chart(df).mark_bar().encode(
        x=alt.X('day:T', title='Hour'),
        y=alt.Y('total_num:Q', title='total_num'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_USD:Q', title='Cumulative USD Amount')],
    ).properties(
        width=800,
        height=300,
        title='ETH STAKE VALIDATORS TOTAL NUMBERS'
    ), use_container_width=True
    )
        st.markdown("##")

        st.altair_chart(
    alt.Chart(df).mark_bar(color='yellow').encode(
        x=alt.X('day:T', title='Hour'),
        y=alt.Y('net_add_num:Q', title='net_add_num'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Amount BNB:Q', title='Amount BNB')],
    ).properties(
        width=800,
        height=300,
        title='ETH STAKE VALIDATORS NET ADD NUMBERS'
    ), use_container_width=True
    )
        
        st.markdown("##")

        st.altair_chart(
    alt.Chart(df).mark_bar(color='brown').encode(
        x=alt.X('day:T', title='Hour'),
        y=alt.Y('add_num:Q', title='add_num'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Amount_USD:Q', title='Amount_USD')],
    ).properties(
        width=800,
        height=300,
        title='ETH STAKE VALIDATORS NET ADD NUMBERS'
    ), use_container_width=True
    )

    with b:
        st.altair_chart(
    alt.Chart(df).mark_bar(color='red').encode(
        x=alt.X('day:T', title='Hour'),
        y=alt.Y('tvl:Q', title='tvl'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_USD:Q', title='Cumulative USD Amount')],
    ).properties(
        width=800,
        height=300,
        title='ETH STAKE TVL'
    ), use_container_width=True
    )
          
        st.markdown("##")
        st.altair_chart(
    alt.Chart(df).mark_bar(color='blue').encode(
        x=alt.X('day:T', title='Hour'),
        y=alt.Y('ssv_price:Q', title='ssv_price'),
    ).properties(
        width=800,
        height=300,
        title='SSV PRICE'
    ), use_container_width=True
    )
        
        st.markdown("##")
        st.altair_chart(
    alt.Chart(df).mark_bar(color='orange').encode(
        x=alt.X('day:T', title='Hour'),
        y=alt.Y('remove_num:Q', title='remove_num'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_USD:Q', title='Cumulative_USD')],
    ).properties(
        width=800,
        height=300,
        title='ETH STAKE VALIDATORS REMOVE NUMBERS'
    ), use_container_width=True
    )
        
    generate_summary(df)

    df = pd.read_csv('sql/ssv_in_Efficient_Frontier.csv')
    

    df['time_scale'] = pd.to_datetime(df['time_scale'])

    # Melt the DataFrame to long format
    df_melted = pd.melt(df, id_vars=['time_scale'], value_vars=['inflow', 'outflow', 's_total', 'u_total', 'total_inflow', 'day_net_inflow'])

    # Altair plot
    st.markdown("##")
    st.altair_chart(
        alt.Chart(df_melted).mark_circle().encode(
            x=alt.X('time_scale:T', title='Time Scale'),
            y=alt.Y('value:Q', title='Value'),
            color='variable:N',  # Color by variable (column names)
            tooltip=[alt.Tooltip('time_scale:T', title='Time Scale'),
                    alt.Tooltip('variable:N', title='Variable'),
                    alt.Tooltip('value:Q', title='Value')],
        ).properties(
            width=800,
            height=300,
            title='Efficient Frontier'
        ), use_container_width=True
    )

    generate_summary_p(df)

    st.markdown("##")
    a,b = st.columns([2,2])
    df = pd.read_csv('sql/erc20_MVRV.csv')
    df_1 = pd.read_csv("sql/ssv_on_cex.csv")
    df['time'] = pd.to_datetime(df.time, errors='coerce')
    df_1['day'] = pd.to_datetime(df_1.day, errors='coerce')
    with a:
        st.altair_chart(
    alt.Chart(df).mark_bar().encode(
        x=alt.X('time:T', title='Hour'),
        y=alt.Y('price:Q', title='price'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_USD:Q', title='Cumulative USD Amount')],
    ).properties(
        width=800,
        height=300,
        title='ERC20 price'
    ), use_container_width=True
    )
        st.markdown("##")

        st.altair_chart(
    alt.Chart(df).mark_bar(color='blueviolet').encode(
        x=alt.X('time:T', title='Hour'),
        y=alt.Y('realized_price:Q', title='realized_price'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Amount BNB:Q', title='Amount BNB')],
    ).properties(
        width=800,
        height=300,
        title='ERC20 realized_price'
    ), use_container_width=True
    )
        
        st.markdown("##")

        st.altair_chart(
    alt.Chart(df).mark_bar(color='darkslategray').encode(
        x=alt.X('time:T', title='Hour'),
        y=alt.Y('mvrv:Q', title='mvrv'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Amount_USD:Q', title='Amount_USD')],
    ).properties(
        width=800,
        height=300,
        title='ERC20 mvrv'
    ), use_container_width=True
    )

    with b:
        st.altair_chart(
    alt.Chart(df_1).mark_bar(color='lightcoral').encode(
        x=alt.X('day:T', title='Hour'),
        y=alt.Y('net_balance:Q', title='net_balance'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_USD:Q', title='Cumulative USD Amount')],
    ).properties(
        width=800,
        height=300,
        title='SSV Centralized Exchanges'
    ), use_container_width=True
    )
          
        st.markdown("##")
        st.altair_chart(
    alt.Chart(df_1).mark_bar(color='salmon').encode(
        x=alt.X('day:T', title='Hour'),
        y=alt.Y('total_balance:Q', title='total_balance'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_BNB:Q', title='Cumulative_BNB')],
    ).properties(
        width=800,
        height=300,
        title='SSV Centralized Exchanges Toatal Prices'
    ), use_container_width=True
    )
        
        st.markdown("##")
        st.altair_chart(
    alt.Chart(df).mark_bar(color='indigo').encode(
        x=alt.X('time:T', title='Hour'),
        y=alt.Y('baseline:Q', title='baseline'),
        tooltip=[alt.Tooltip('hour:T', title='Hour'), alt.Tooltip('Cumulative_USD:Q', title='Cumulative_USD')],
    ).properties(
        width=800,
        height=300,
        title='ERC20 baseline'
    ), use_container_width=True
    )
        
    generate_summary(df_1)



