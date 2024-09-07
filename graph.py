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


def create_single_validator_graph():
    # User input for the validator ID
    validator_id = st.text_input("Enter Validator ID",
                                 value="0x800038b93ae208b820e348348e86ec02be3788dbd328101ac6bbe419a015173711d79b70b13eafe4e9dc92ce0ac51aae")
    submit_button = st.button('Fetch Validator Details')

    if submit_button:
        # Constructing the query using the provided validator ID
        query = f"""
        {{
          validator(id: "{validator_id}", subgraphError: allow) {{
            active
            id
            lastUpdateBlockNumber
            lastUpdateBlockTimestamp
            lastUpdateTransactionHash
            shares
          }}
        }}
        """

        # GraphQL API URL
        url = "https://gateway.thegraph.com/api/535e83a86f270e66f83c6227ae349334/subgraphs/id/7V45fKPugp9psQjgrGsfif98gWzCyC6ChN7CW98VyQnr"
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']['validator']

            if data:
                st.write("## Validator Details")
                st.json(data)  # Display raw data in JSON format

                # Optionally, we can convert the validator data into a DataFrame for further analysis
                df = pd.DataFrame([data])
                generate_summary(df)  # Generate a summary based on the validator data

                # Extracting data for nodes and edges (if a network graph is needed)
                nodes = []
                edges = []

                # Add a node for the validator
                nodes.append({
                    'id': f"Validator: {data['id']}",
                    'label': f"Validator: {data['id']}",
                    'title': f"Active: {data['active']}, Shares: {data['shares']}, Last Update Block: {data['lastUpdateBlockNumber']}"
                })

                # Creating the network graph
                graph = Network(height="800px", width="100%", notebook=True)

                # Add the validator node to the graph
                for node in nodes:
                    graph.add_node(node['id'], label=node['label'], title=node['title'])

                # Since we don't have any additional relationships for this query (e.g., operators or clusters),
                # the graph will display only the validator node.

                # Using a temporary file to display the graph
                with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
                    graph.show(tmpfile.name)
                    tmpfile.seek(0)
                    html_content = tmpfile.read().decode("utf-8")

                st.components.v1.html(html_content, height=800)

            else:
                st.warning("No data found for this validator ID.")
        else:
            raise Exception(f"Query failed with status code {response.status_code}. Query: {query}")


def create_operators_network_graph():
    # User input for the query parameters
    first = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=10)
    skip = st.number_input("Skip records", min_value=0, max_value=50, value=10)
    orderBy_options = st.selectbox("Order By", ["active", "fee", "totalWithdraw", "lastUpdateBlockNumber"])
    orderD = st.selectbox("Order Direction", ['desc', 'asc'])
    submit_button = st.button('Submit')

    if submit_button:
        # Constructing the query with user input
        query = f"""
        {{
          operators(
            first: {first}
            orderBy: {orderBy_options}
            orderDirection: {orderD}
            skip: {skip}
            subgraphError: allow
          ) {{
            active
            fee
            id
            isPrivate
            lastUpdateBlockNumber
            lastUpdateBlockTimestamp
            lastUpdateTransactionHash
            operatorId
            previousFee
            publicKey
            totalWithdrawn
            validatorCount
          }}
        }}
        """

        # GraphQL API URL
        url = "https://gateway.thegraph.com/api/535e83a86f270e66f83c6227ae349334/subgraphs/id/7V45fKPugp9psQjgrGsfif98gWzCyC6ChN7CW98VyQnr"
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']
            st.dataframe(data['operators'])

            st.markdown("##")
            generate_summary(pd.DataFrame(data['operators']))
            st.markdown("##")
        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

        # Extracting data for nodes and edges (if we want to build a network graph for operators)
        nodes = []
        edges = []

        for operator in data['operators']:
            operator_id = operator['id']
            nodes.append({'id': f"Operator: {operator_id}", 'label': f"Operator: {operator_id}", 'title': ''})

        # Creating the network graph
        graph = Network(height="800px", width="100%", notebook=True)

        for node in nodes:
            graph.add_node(node['id'], label=node['label'], title=node['title'])

        # Using a temporary file to display the graph
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmpfile:
            graph.show(tmpfile.name)
            tmpfile.seek(0)
            html_content = tmpfile.read().decode("utf-8")

        return html_content


def create_single_operator_graph():
    # User input for the operator ID
    operator_id = st.text_input("Enter Operator ID", value="1007")
    submit_button = st.button('Fetch Operator Details')

    if submit_button:
        # Constructing the query using the provided operator ID
        query = f"""
        {{
          operator(id: "{operator_id}", subgraphError: allow) {{
            active
            fee
            id
            isPrivate
            lastUpdateBlockNumber
            lastUpdateBlockTimestamp
            lastUpdateTransactionHash
            operatorId
            previousFee
            publicKey
            totalWithdrawn
            validatorCount
            whitelistedContract
          }}
        }}
        """

        # GraphQL API URL
        url = "https://gateway.thegraph.com/api/535e83a86f270e66f83c6227ae349334/subgraphs/id/7V45fKPugp9psQjgrGsfif98gWzCyC6ChN7CW98VyQnr"
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']['operator']

            if data:
                st.write("## Operator Details")
                st.json(data)  # Display raw data in JSON format

                # Optionally, we can convert the operator data into a DataFrame for further analysis
                df = pd.DataFrame([data])
                generate_summary(df)  # Generate a summary based on the operator data

                # Extracting data for nodes and edges (if a network graph is needed)
                nodes = []
                edges = []

                nodes.append({'id': f"Operator: {data['id']}", 'label': f"Operator: {data['id']}", 'title': ''})
                nodes.append({'id': f"Public Key: {data['publicKey']}", 'label': f"Public Key: {data['publicKey']}",
                              'title': ''})

                # Adding edges
                edges.append({'source': f"Operator: {data['id']}", 'target': f"Public Key: {data['publicKey']}"})

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

                st.components.v1.html(html_content, height=800)

            else:
                st.warning("No data found for this operator ID.")
        else:
            raise Exception(f"Query failed with status code {response.status_code}. Query: {query}")


def create_clusters_network_graph():
    # User input for the query parameters
    first = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=5)
    skip = st.number_input("Skip records", min_value=0, max_value=50, value=10)
    orderBy_options = st.selectbox("Order By", ["active", "balance", "index", "lastUpdateBlockNumber"])
    orderD = st.selectbox("Order Direction", ['desc', 'asc'])
    submit_button = st.button('Submit')

    if submit_button:
        # Constructing the query with user input
        query = f"""
        {{
          clusters(
            first: {first}
            orderBy: {orderBy_options}
            orderDirection: {orderD}
            skip: {skip}
            subgraphError: allow
          ) {{
            id
            owner {{
              id
              nonce
              validatorCount
            }}
            operatorIds
            validatorCount
            active
            balance
            index
            lastUpdateBlockNumber
            lastUpdateBlockTimestamp
            lastUpdateTransactionHash
            networkFeeIndex
          }}
        }}
        """

        # GraphQL API URL
        url = "https://gateway.thegraph.com/api/535e83a86f270e66f83c6227ae349334/subgraphs/id/7V45fKPugp9psQjgrGsfif98gWzCyC6ChN7CW98VyQnr"
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']
            st.dataframe(data['clusters'])

            # Generate a summary from the fetched data
            st.markdown("## Summary")
            generate_summary(pd.DataFrame(data['clusters']))
            st.markdown("##")

        else:
            raise Exception(f"Query failed to run by returning code of {response.status_code}. {query}")

        # Extracting data for nodes and edges for the network graph
        nodes = []
        edges = []

        for cluster in data['clusters']:
            cluster_id = cluster['id']
            owner_id = cluster['owner']['id']
            nodes.append({'id': f"Cluster: {cluster_id}", 'label': f"Cluster: {cluster_id}", 'title': ''})
            nodes.append({'id': f"Owner: {owner_id}", 'label': f"Owner: {owner_id}",
                          'title': f"Owner Nonce: {cluster['owner']['nonce']}, Validator Count: {cluster['owner']['validatorCount']}"})

            # Adding operator nodes
            for operator_id in cluster['operatorIds']:
                nodes.append({'id': f"Operator: {operator_id}", 'label': f"Operator: {operator_id}", 'title': ''})
                edges.append({'source': f"Cluster: {cluster_id}", 'target': f"Operator: {operator_id}"})

            # Adding edges between cluster and owner
            edges.append({'source': f"Cluster: {cluster_id}", 'target': f"Owner: {owner_id}"})

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


def create_single_cluster_graph():
    # User input for the cluster ID
    cluster_id = st.text_input("Enter Cluster ID", value="0x078dc682083132b4e86731062fcf95a729bac067-17-188-200-208")
    submit_button = st.button('Fetch Cluster Details')

    if submit_button:
        # Constructing the query using the provided cluster ID
        query = f"""
        {{
          cluster(id: "{cluster_id}", subgraphError: allow) {{
            active
            balance
            id
            index
            lastUpdateBlockNumber
            lastUpdateBlockTimestamp
            lastUpdateTransactionHash
            networkFeeIndex
            operatorIds
            validatorCount
          }}
        }}
        """

        # GraphQL API URL
        url = "https://gateway.thegraph.com/api/535e83a86f270e66f83c6227ae349334/subgraphs/id/7V45fKPugp9psQjgrGsfif98gWzCyC6ChN7CW98VyQnr"
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']['cluster']

            if data:
                st.write("## Cluster Details")
                st.json(data)  # Display raw data in JSON format

                # Optionally, we can convert the cluster data into a DataFrame for further analysis
                df = pd.DataFrame([data])
                generate_summary(df)  # Generate a summary based on the cluster data

                # Extracting data for nodes and edges (if a network graph is needed)
                nodes = []
                edges = []

                nodes.append({'id': f"Cluster: {data['id']}", 'label': f"Cluster: {data['id']}",
                              'title': f"Balance: {data['balance']}, Index: {data['index']}"})

                # Adding operator nodes
                for operator_id in data['operatorIds']:
                    nodes.append({'id': f"Operator: {operator_id}", 'label': f"Operator: {operator_id}", 'title': ''})
                    edges.append({'source': f"Cluster: {data['id']}", 'target': f"Operator: {operator_id}"})

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

                st.components.v1.html(html_content, height=800)

            else:
                st.warning("No data found for this cluster ID.")
        else:
            raise Exception(f"Query failed with status code {response.status_code}. Query: {query}")


def create_validator_addeds_graph():
    # User input for query parameters
    first = st.number_input("Number of records to fetch", min_value=1, max_value=50, value=13)
    skip = st.number_input("Skip records", min_value=0, max_value=50, value=10)
    orderBy_options = st.selectbox("Order By", ["cluster_active", "cluster_balance", "cluster_index", "publicKey"])
    orderD = st.selectbox("Order Direction", ['desc', 'asc'])
    submit_button = st.button('Submit')

    if submit_button:
        # Constructing the query with user input
        query = f"""
        {{
          validatorAddeds(
            first: {first}
            orderBy: {orderBy_options}
            orderDirection: {orderD}
            skip: {skip}
            subgraphError: allow
          ) {{
            blockNumber
            cluster_active
            transactionHash
            shares
            publicKey
            operatorIds
            owner
            id
            cluster_validatorCount
            cluster_networkFeeIndex
            cluster_index
            cluster_balance
            blockTimestamp
          }}
        }}
        """

        # GraphQL API URL
        url = "https://gateway.thegraph.com/api/535e83a86f270e66f83c6227ae349334/subgraphs/id/7V45fKPugp9psQjgrGsfif98gWzCyC6ChN7CW98VyQnr"
        response = requests.post(url, json={'query': query})

        if response.status_code == 200:
            data = response.json()['data']['validatorAddeds']
            st.dataframe(pd.DataFrame(data))  # Display data as a dataframe

            # Generate a summary from the fetched data
            st.markdown("## Summary")
            generate_summary(pd.DataFrame(data))
            st.markdown("##")

            # Extracting data for nodes and edges for the network graph
            nodes = []
            edges = []

            for validator_added in data:
                validator_id = validator_added['id']
                public_key = validator_added['publicKey']
                nodes.append({'id': f"Validator: {validator_id}", 'label': f"Validator: {validator_id}", 'title': ''})
                nodes.append({'id': f"Public Key: {public_key}", 'label': f"Public Key: {public_key}", 'title': ''})
                edges.append({'source': f"Validator: {validator_id}", 'target': f"Public Key: {public_key}"})

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

            st.components.v1.html(html_content, height=800)

        else:
            raise Exception(f"Query failed with status code {response.status_code}. Query: {query}")


def graph():
    st.markdown("### Select an Option")
    option = st.radio(
        "Select Choice",
        ("Validators", "Validator", "Operators", "Operator", "Clusters", "Cluster", "ValidatorAddeds"),
        index=0,
        horizontal=True
    )

    if option == 'Validators':
        html_content = create_validators_network_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'Validator':
        html_content = create_single_validator_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'Operators':
        html_content = create_operators_network_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'Operator':
        html_content = create_single_operator_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'Clusters':
        html_content = create_clusters_network_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'Cluster':
        html_content = create_single_cluster_graph()
        st.components.v1.html(html_content, height=800)
    elif option == 'ValidatorAddeds':
        html_content = create_validator_addeds_graph()
        st.components.v1.html(html_content, height=800)
