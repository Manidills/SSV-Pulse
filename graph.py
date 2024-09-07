from io import StringIO
import streamlit as st
import pandas as pd
import requests
import json
from pyvis.network import Network
import tempfile
import g4f
from streamlit.components.v1 import html



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
    prompt = f"Here ssv network staking related data\n{csv_data_str}\ngive some short summary insights about the data in  points"
    st.write(chat_bot(prompt))





def create_validators_network_graph():
    # User input for the query parameters
    first = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=5)
    orderBy_options = st.selectbox("Order By", ["active", "balance", "index", "lastUpdateBlockNumber"])
    orderD = st.selectbox("Order Direction", ['desc', 'asc'])
    submit_button = st.button('Submit')

    if submit_button:
        # Constructing the query with user input
        query = f"""
        {{
          validators(first: {first}, orderBy: {orderBy_options}, orderDirection: {orderD}) {{
            id
            owner {{
              id
            }}
            operators {{
              id
            }}
            cluster {{
              id
              active
              balance
              index
              lastUpdateBlockNumber
              lastUpdateBlockTimestamp
              lastUpdateTransactionHash
              networkFeeIndex
              operatorIds
              validatorCount
            }}
            lastUpdateBlockNumber
            lastUpdateBlockTimestamp
            lastUpdateTransactionHash
          }}
        }}
        """
        
        # Updated URL for the GraphQL endpoint (replace with the correct one)
        url = "https://gateway.thegraph.com/api/535e83a86f270e66f83c6227ae349334/subgraphs/id/7V45fKPugp9psQjgrGsfif98gWzCyC6ChN7CW98VyQnr"
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']
            st.dataframe(data['validators'])

            st.markdown("##")
            generate_summary(pd.DataFrame(data['validators']))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")
        
        # Extracting data for nodes and edges
        nodes = []
        edges = []

        for validator in data['validators']:
            validator_id = validator['id']
            owner_id = validator['owner']['id']
            operators = validator['operators']
            cluster = validator['cluster']
            
            # Adding validator node
            nodes.append({'id': f"Validator: {validator_id}", 'label': f"Validator: {validator_id}", 'title': ''})
            nodes.append({'id': f"Owner: {owner_id}", 'label': f"Owner: {owner_id}", 'title': ''})
            
            # Adding operator nodes
            for operator in operators:
                operator_id = operator['id']
                nodes.append({'id': f"Operator: {operator_id}", 'label': f"Operator: {operator_id}", 'title': ''})
                edges.append({'source': f"Validator: {validator_id}", 'target': f"Operator: {operator_id}"})
            
            # Adding cluster node and properties
            cluster_id = cluster['id']
            cluster_title = f"Active: {cluster['active']}, Balance: {cluster['balance']}, Index: {cluster['index']}, Validators: {cluster['validatorCount']}"
            nodes.append({'id': f"Cluster: {cluster_id}", 'label': f"Cluster: {cluster_id}", 'title': cluster_title})

            # Adding edges
            edges.append({'source': f"Validator: {validator_id}", 'target': f"Owner: {owner_id}"})
            edges.append({'source': f"Validator: {validator_id}", 'target': f"Cluster: {cluster_id}"})

        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)

        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])

        for edge in edges:
            graph.add_edge(edge['source'], edge['target'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content

def graph():
    st.title('OpBNB Bridge Users')
    st.markdown("### Select an Option")
    option = st.radio(
        "Select Choice",
        ("Validators","Validator"),
        index=0,
        horizontal=True
    )

    if option == 'Validators':
        html_content = create_validators_network_graph()
        st.components.v1.html(html_content, height=800)

