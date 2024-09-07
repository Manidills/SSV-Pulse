import streamlit as st
import altair as alt
import pandas as pd

# Set the page title and layout
def home():

    # Main Content: Introduction
    st.title("Welcome to SSV Pulse")
    # Styled Introduction Section
    st.markdown("""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
        <h3 style="color: #333333;"> <b>Welcome to <span style="color:#4CAF50;">SSV Pulse</span>!</b></h3>
        <p style="font-size:18px; line-height:1.6; color:#444;">
        <b>SSV Pulse</b> is an advanced AI-based analytics platform designed to provide deep insights into the <b>SSV network</b>.
        Powered by cutting-edge <b>LLM models</b>, SSV Pulse not only analyzes key data but also suggests investment strategies,
        predicts trends, and educates new users. Our platform is specifically tailored to assist stakeholders in understanding 
        the intricacies of the SSV network, from validators and operators to overall network performance.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##")

    # Section: ETH Stake Analytics
    st.header("1. ETH Stake Analytics")
    st.markdown("""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
        <p style="font-size:18px; line-height:1.6; color:#444;">
        Track the amount of ETH staked within the SSV network. Understand staking trends and their implications on the network's security and rewards. 
        SSV Pulse provides predictive insights, enabling users to gauge future staking activity, identify key staking participants, 
        and explore potential growth opportunities.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##")

    # Section: Fees Analytics
    st.header("2. Fees Analytics")
    st.markdown("""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
        <p style="font-size:18px; line-height:1.6; color:#444;">
        Analyze the fees generated within the SSV network. This section provides detailed insights into the distribution of fees across validators, operators, and the network. 
        SSV Pulse uses AI to predict future fee structures, offering suggestions to optimize fee revenue or minimize operational costs. 
        The analytics are essential for validators and operators to assess the profitability of their positions.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##")

    # Section: Growth Analytics
    st.header("3. Growth Analytics")
    st.markdown("""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
        <p style="font-size:18px; line-height:1.6; color:#444;">
         Monitor the growth of the SSV network over time. Our platform visualizes network expansion in terms of new validators, operators, 
         and key milestones such as network upgrades. We use LLM models to forecast growth trajectories, giving users an early edge in 
         understanding the long-term health and scalability of the network.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##")

    # Section: Holders Analytics
    st.header("4. Holders Analytics")
    st.markdown("""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
        <p style="font-size:18px; line-height:1.6; color:#444;">
        Explore the distribution and concentration of SSV tokens among holders. SSV Pulse tracks wallet activities, identifying major holders 
        and analyzing their behaviors. Our AI models predict holder movements and offer suggestions for strategic investment based on trends 
        in accumulation or distribution patterns.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##")

    # Section: Network Graph, Insights & Connections
    st.header("5. Network Graph, Insights & Connections")
    st.markdown("""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
        <p style="font-size:18px; line-height:1.6; color:#444;">
        Visualize the complex relationships between validators, operators, accounts, and clusters within the SSV network. This interactive network graph 
        helps users understand the interdependencies and connections that drive the network’s operations. SSV Pulse provides detailed insights into these 
        connections, offering a unique perspective into the behaviors and decisions of key participants. AI-driven suggestions and predictions help users 
        navigate this intricate ecosystem, making it easier to find opportunities for collaboration, investment, and optimization.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("##")


    # Section: Educate & Design Support
    st.header("A Place for Learning and Design Innovation")
    st.markdown("""
    <div style="background-color: #f9f9f9; padding: 20px; border-radius: 10px; border: 1px solid #ddd;">
        <p style="font-size:18px; line-height:1.6; color:#444;">
        At SSV Pulse, we strive to educate new users about the SSV ecosystem. Through comprehensive analytics and insights, 
        we guide users toward better decision-making. Our AI-driven suggestions enable investors and operators to optimize their strategies 
        and improve their overall participation in the network. The platform also helps drive innovation by supporting the design and deployment 
        of better solutions within the SSV ecosystem.
        </p>
    </div>
    """, unsafe_allow_html=True)
    

    # Footer
    st.markdown("---")
    st.write("**SSV Pulse** - Empowering Users with Data-Driven Insights | Powered by AI | [Contact Us](mailto:contact@ssvpulse.com)")
