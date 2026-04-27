import streamlit as st

import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px


# DB Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Ksurendar@123",
    database="phonepe"
)

st.title("PHONEPE PROJECT1")

def run_query(query):
    cursor = conn.cursor()
    cursor.execute(query)

    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()

    df = pd.DataFrame(data, columns=columns)
    return df

r = st.sidebar.radio("Navigation",["home","bussiness case study"])
if r =="home":
 st.title("📊 PHONEPE DATA ANALYSIS")
 

 st.title("📊 State-wise Transaction Map")

 def run_query(query):
    cursor = conn.cursor()
    cursor.execute(query)
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()
    return pd.DataFrame(data, columns=columns)

 query = """
 SELECT state, SUM(Transaction_amount) AS total_amount
 FROM agg_transaction
 GROUP BY state
 """
 df = run_query(query)

# ---------------- CLEAN STATE NAMES ----------------
 df["state"] = df["state"].str.replace("-", " ").str.title()

# Fix mismatches with GeoJSON
 df["state"] = df["state"].replace({
    "Andaman & Nicobar Islands": "Andaman and Nicobar",
    "Dadra & Nagar Haveli & Daman & Diu": "Dadra and Nagar Haveli and Daman and Diu"
 })

# ---------------- CHOROPLETH MAP ----------------
 fig = px.choropleth(
    df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey="properties.ST_NM",
    locations="state",
    color="total_amount",   # 🔥 your transaction column
    color_continuous_scale="Reds",
    title="State-wise Transaction Amount"
 )

 fig.update_geos(fitbounds="locations", visible=False)


# ---------------- SHOW IN STREAMLIT ----------------
 st.plotly_chart(fig, use_container_width=True)


elif r=="bussiness case study":
    st.title("📊 PHONEPE DATA ANALYSIS")
    st.subheader("bussiness case study")
    option = st.selectbox(
        "Choose Analysis",
        [
            "1. Decoding Transaction Dynamics on PhonePe",
            "2. Device Dominance and User Engagement Analysis",
            "3. Insurance Penetration and Growth Potential Analysis",
            "4. Transaction Analysis Across States and Districts",
            "5. User Registration Analysis"
        ]
    )



    if option == "1. Decoding Transaction Dynamics on PhonePe":

        st.header("📌 Transaction Dynamics Analysis")

        sub_option = st.selectbox(
            "Select Sub Analysis",
            [
                "State Performance",
                "Quarterly Trend",
                "Transaction Type",
                "Top 5 States",
                "Growth Analysis"
            ]
        )

        if sub_option == "State Performance":
                    query = """ 
                    SELECT state,SUM(Transaction_count) AS total_count
                    FROM agg_transaction 
                    GROUP BY state 
                    ORDER BY total_count DESC;
                    """ 
                    df = run_query(query) 
                    st.dataframe(df) 
                    top_df = df.head(10)
                    

        # ---------------- BAR CHART ----------------
                    bar_fig = px.bar(
                    top_df,
                    x="state",
                    y="total_count",
                    color="state",
                    title="Top 10 States - Transaction Count"
                    )

                    st.plotly_chart(bar_fig, use_container_width=True)

        # ---------------- DONUT CHART ----------------
                    donut_fig = px.pie(
                    top_df,
                    names="state",
                    values="total_count",
                    hole=0.5,   # makes it donut
                    title="Transaction Share by State"
                    )
                    st.plotly_chart(donut_fig, use_container_width=True)
        #-------------line chart--------------
                    fig_line = px.line(
                    df,
                    x="state",
                    y="total_count",
                    markers=True,
                    title="State-wise Transaction Count (Line Chart)"
                    )

                    fig_line.update_layout(xaxis_tickangle=-45)

                    st.plotly_chart(fig_line, use_container_width=True)

                    fig_tree = px.treemap(
                        top_df,
                        path=["state"],
                        values="total_count",
                        title="Transaction Distribution - Treemap"
                    )
                    st.plotly_chart(fig_tree, use_container_width=True)
    #--------------------------------------------------------------------------------
        if sub_option == "Quarterly Trend":
                query = """
                SELECT year, quater, SUM(transaction_count) AS total_count
                FROM agg_transaction
                GROUP BY year, quater
                ORDER BY year, quater;
                """
                df = run_query(query)
                st.dataframe(df)
            
            
            # Create proper x-axis
                df["Year-Quater"] = df["year"].astype(str) + "-Q" + df["quater"].astype(str)
                df = df.sort_values(["year", "quater"])

            

            #---time label-----
                df["time"] = df["year"].astype(str) + "-Q" + df["quater"].astype(str)

                fig_bar = px.bar(
                    df,
                    x="time",
                    y="total_count",
                    title="Quarterly Transaction Count",
                    color="total_count"
                )

                st.plotly_chart(fig_bar, use_container_width=True)
                #----donut chart----
                quater_df = df.groupby("quater")["total_count"].sum().reset_index()

                fig_donut = px.pie(
                    quater_df,
                    names="quater",
                    values="total_count",
                    hole=0.5,
                    title="Quarter Contribution to Total Transactions"
                )

                st.plotly_chart(fig_donut, use_container_width=True)

                #---line chart---
                fig_line = px.line(
                df,
                x="time",
                y="total_count",
                markers=True,
                title="Quarterly Transaction Trend"
                )

                st.plotly_chart(fig_line, use_container_width=True)

                fig_stacked = px.bar(
                    df,
                    x="year",
                    y="total_count",
                    color="quater",
                    title="Quarter Contribution per Year"
                )

                st.plotly_chart(fig_stacked, use_container_width=True)
            #----------------------------------------------------------------------

        if sub_option == "Transaction Type":
                query = """
                SELECT transaction_type, SUM(transaction_count) AS total_count
                FROM agg_transaction
                GROUP BY transaction_type;
                """
                df = run_query(query)
                st.dataframe(df)
                st.bar_chart(df.set_index('transaction_type'))
                
                fig_donut = px.pie(
                    df,
                    names='transaction_type',
                    values='total_count',
                    hole=0.5  # makes it donut
                )

                st.plotly_chart(fig_donut, use_container_width=True)

                fig_hbar = px.bar(
                    df,
                    x='total_count',
                    y='transaction_type',
                    orientation='h',
                    title="Transaction Type Distribution"
                )

                st.plotly_chart(fig_hbar, use_container_width=True)

                fig_tree = px.treemap(
                    df,
                    path=['transaction_type'],
                    values='total_count',
                    title="Transaction Share by Type"
                )

                st.plotly_chart(fig_tree, use_container_width=True)
            #---------------------
        if sub_option == "Top 5 States":
                query = """
                SELECT state, SUM(transaction_count) AS total_count
                FROM agg_transaction
                GROUP BY state
                ORDER BY total_count DESC
                LIMIT 5;
                """
                df = run_query(query)

                st.subheader("Top 5 States")
                st.dataframe(df)
                df = df.sort_values(by="total_count", ascending=False)

                fig_bar = px.bar(
                    df,
                    x='state',
                    y='total_count',
                    text='total_count',
                    title="Top 5 States by Transaction Count"
                )

                fig_bar.update_traces(textposition='outside')

                st.plotly_chart(fig_bar, use_container_width=True)

                fig_donut = px.pie(
                    df,
                    names='state',
                    values='total_count',
                    hole=0.5,
                    title="Transaction Share by State"
                )

                st.plotly_chart(fig_donut, use_container_width=True)


                fig_hbar = px.bar(
                    df,
                    x='total_count',
                    y='state',
                    orientation='h',
                    text='total_count',
                    title="Top 5 States (Horizontal View)"
                )

                fig_hbar.update_traces(textposition='outside')

                st.plotly_chart(fig_hbar, use_container_width=True)

                fig_funnel = px.funnel(
                    df,
                    x='total_count',
                    y='state',
                    title="Top 5 States Funnel View"
                )

                st.plotly_chart(fig_funnel, use_container_width=True)
                #-------------------------------------------------------------------

        if sub_option == "Growth Analysis":

            query = """SELECT 
                Transaction_type,
                Year,
                Quater,
                total_count,
                
                LAG(total_count) OVER (
                    PARTITION BY Transaction_type 
                    ORDER BY Year, Quater
                ) AS prev_count,

                ROUND(
                    (total_count - LAG(total_count) OVER (
                        PARTITION BY Transaction_type 
                        ORDER BY Year, Quater
                    )) 
                    / LAG(total_count) OVER (
                        PARTITION BY Transaction_type 
                        ORDER BY Year, Quater
                    ) * 100, 2
                ) AS growth_rate

            FROM (
                SELECT 
                    Transaction_type,
                    Year,
                    Quater,
                    SUM(Transaction_count) AS total_count
                FROM agg_transaction
                GROUP BY Transaction_type, Year, Quater
            ) t;    """
            df = run_query(query)

            st.subheader("📈 Transaction Type Growth Rate")
            st.dataframe(df)

            # Create time column
            df["time"] = df["Year"].astype(str) + "-Q" + df["Quater"].astype(str)

            # ---- Line Chart ----
            fig_line = px.line(
                df,
                x="time",
                y="growth_rate",
                color="Transaction_type",
                markers=True,
                title="QoQ Growth Rate by Transaction Type"
            )

            st.plotly_chart(fig_line, use_container_width=True)

            # ---- Bar Chart ----
            fig_bar = px.bar(
                df,
                x="time",
                y="growth_rate",
                color="Transaction_type",
                title="Growth Rate Comparison"
            )

            st.plotly_chart(fig_bar, use_container_width=True)

            pivot_df = df.pivot_table(
                index="Transaction_type",
                columns="time",
                values="growth_rate"
            )

            fig_heatmap = px.imshow(
                pivot_df,
                text_auto=True,
                aspect="auto",
                title="Growth Rate Heatmap (Transaction Type vs Time)"
            )

            st.plotly_chart(fig_heatmap, use_container_width=True)

        #-----------------------------------------------------------------------------------------------------

    if option == "2. Device Dominance and User Engagement Analysis":

            st.header("📱 Device Dominance & User Engagement Analysis")

            query = """
                    SELECT State, Year, SUM(user_count) AS total_users
                    FROM agg_user
                    GROUP BY State, Year;
                    """

            df = run_query(query)

                    # ---------------- DATA CLEANING ----------------
            df["State"] = df["State"].str.replace("-", " ").str.title()

                    # Fix common mismatches
            df["State"] = df["State"].replace({
                        "Andaman & Nicobar": "Andaman and Nicobar Islands",
                        "Dadra & Nagar Haveli": "Dadra and Nagar Haveli and Daman and Diu"
                })

                    # ---------------- CHOROPLETH MAP ----------------
                    

            fig = px.choropleth(
                        df,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey="properties.ST_NM",
                        locations="State",
                        color="total_users",
                        animation_frame="Year",
                        color_continuous_scale="Blues",
                        title="User Growth Map (Year-wise)"
                    )

            fig.update_geos(fitbounds="locations", visible=False)

            st.plotly_chart(fig, use_container_width=True)

            sub_option = st.selectbox(
                "Select Sub Analysis",
                [
                    "Top Device Brands",
                    "Brand Share Percentage",
                    "Underutilized Devices",
                    "State-wise Distribution",
                    "Quarterly Trend"
                ]
            )

        # ---------------- 1. TOP DEVICE BRANDS ----------------
            if sub_option == "Top Device Brands":
                query = """
                SELECT user_brand, SUM(user_count) AS total_users
                FROM agg_user
                GROUP BY user_brand
                ORDER BY total_users DESC;
                """
                df = run_query(query)

            st.subheader("📊 Top Device Brands by Users")
            st.dataframe(df)

            col1, col2 = st.columns(2)

            with col1:
                fig = px.bar(df, x="user_brand", y="total_users", title="Users by Brand")
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                fig = px.pie(df, names="user_brand", values="total_users", title="User Share")
                st.plotly_chart(fig, use_container_width=True)

                fig = px.bar(
                    df,
                    x="total_users",
                    y="user_brand",
                    orientation="h",
                    title="Users by Brand (Horizontal)"
                )
                st.plotly_chart(fig, use_container_width=True)

        # ---------------- 2. BRAND SHARE PERCENTAGE ----------------
            if sub_option == "Brand Share Percentage":
                query = """
                SELECT user_brand, AVG(user_percentage) AS avg_percentage
                FROM agg_user
                GROUP BY user_brand
                ORDER BY avg_percentage DESC;
                """
                df = run_query(query)

                st.subheader("📈 Brand Share Percentage")
                st.dataframe(df)

                fig = px.bar(df, x="user_brand", y="avg_percentage", title="Avg Brand Share %")
                st.plotly_chart(fig, use_container_width=True)

                fig = px.pie(
                    df,
                    names="user_brand",
                    values="avg_percentage",
                    hole=0.5,
                    title="Brand Share Distribution (%)"
                )
                st.plotly_chart(fig, use_container_width=True)

                fig = px.bar(
                    df,
                    x="avg_percentage",
                    y="user_brand",
                    orientation="h",
                    title="Brand Share Ranking"
                )
                st.plotly_chart(fig, use_container_width=True)

                fig = px.treemap(
                    df,
                    path=["user_brand"],
                    values="avg_percentage",
                    title="Brand Share Hierarchy"
                )
                st.plotly_chart(fig, use_container_width=True)

                # ---------------- 3. UNDERUTILIZED DEVICES ----------------
            elif sub_option == "Underutilized Devices":
                query = """
                SELECT 
                    user_brand,
                    SUM(user_count) AS total_users,
                    AVG(user_percentage) AS avg_percentage
                FROM agg_user
                GROUP BY user_brand
                HAVING total_users > 1000000
                ORDER BY avg_percentage ASC;
                """
                df = run_query(query)

                st.subheader("⚠️ Underutilized Devices (Low % Share)")
                st.dataframe(df)

                fig = px.bar(df, x="user_brand", y="avg_percentage", title="Low Performing Brands")
                st.plotly_chart(fig, use_container_width=True)


                fig = px.bar(
                    df,
                    x="avg_percentage",
                    y="user_brand",
                    orientation="h",
                    title="Underutilized Devices (Low Engagement Ranking)"
                )
                st.plotly_chart(fig, use_container_width=True)

                fig = px.treemap(
                    df,
                    path=["user_brand"],
                    values="total_users",
                    color="avg_percentage",
                    title="Underutilized Device Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)

                fig = px.box(
                    df,
                    x="user_brand",
                    y="avg_percentage",
                    title="Engagement Distribution Across Devices"
                )
                st.plotly_chart(fig, use_container_width=True)

                # ---------------- 4. STATE-WISE DISTRIBUTION ----------------
            elif sub_option == "State-wise Distribution":
                query = """
                SELECT State, user_brand, SUM(user_count) AS total_users
                FROM agg_user
                GROUP BY State, user_brand;
                """
                df = run_query(query)

                st.subheader("🗺️ State-wise Device Distribution")
                st.dataframe(df)

                fig = px.treemap(df, path=["State", "user_brand"], values="total_users",
                                title="Device Usage by State")
                st.plotly_chart(fig, use_container_width=True)
                
                fig = px.bar(
                    df,
                    x="State",
                    y="total_users",
                    color="user_brand",
                    title="State-wise Device Usage (Stacked)"
                )
                st.plotly_chart(fig, use_container_width=True)

                fig = px.bar(
                    df,
                    x="State",
                    y="total_users",
                    color="user_brand",
                    barmode="group",
                    title="Device Usage by State (Grouped)"
                )
                st.plotly_chart(fig, use_container_width=True)

                fig = px.sunburst(
                    df,
                    path=["State", "user_brand"],
                    values="total_users",
                    title="State → Device Brand Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
                # ---------------- 5. QUARTERLY TREND ----------------
            elif sub_option == "Quarterly Trend":
                query = """
                SELECT Year, Quater, user_brand, SUM(user_count) AS total_users
                FROM agg_user
                GROUP BY Year, Quater, user_brand
                ORDER BY Year, Quater;
                """
                df = run_query(query)

                df["time"] = df["Year"].astype(str) + " Q" + df["Quater"].astype(str)

                st.subheader("📈 Quarterly User Trend by Device")
                st.dataframe(df)

                fig = px.line(df, x="time", y="total_users", color="user_brand",
                            title="User Growth Trend")
                st.plotly_chart(fig, use_container_width=True)

                fig = px.area(
                    df,
                    x="time",
                    y="total_users",
                    color="user_brand",
                    title="Quarterly Trend (Area View)"
                )
                st.plotly_chart(fig, use_container_width=True)

                fig = px.bar(
                    df,
                    x="user_brand",
                    y="total_users",
                    color="user_brand",
                    animation_frame="time",
                    title="Quarterly Growth Animation"
                )
                st.plotly_chart(fig, use_container_width=True)

                fig = px.bar(
                    df,
                    x="time",
                    y="total_users",
                    color="user_brand",
                    title="Total Growth Trend (Stacked)"
                )
                st.plotly_chart(fig, use_container_width=True)
    #----------------------------------------------------------------------------------------------

    if option == "3. Insurance Penetration and Growth Potential Analysis":
        st.header("🛡️ Insurance Penetration & Growth Analysis")

        
    # ---------------- QUERY ----------------
        query = """
        SELECT State, SUM(Insurance_amount) AS total_amount
        FROM agg_insurance
        GROUP BY State;
        """
        df = run_query(query)

                    # ---------------- DATA CLEANING ----------------
        df["State"] = df["State"].str.replace("-", " ").str.title()

                    # Fix common mismatches
        df["State"] = df["State"].replace({
        "Andaman & Nicobar": "Andaman and Nicobar Islands",
        "Dadra & Nagar Haveli": "Dadra and Nagar Haveli and Daman and Diu"
        })

                    # ---------------- CHOROPLETH MAP ----------------
        fig = px.choropleth(
                        df,
                        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey="properties.ST_NM",
                        locations="State",
                        color="total_amount",
                        color_continuous_scale="Greens",
                        title="India Map - Insurance Revenue"
                    )

        fig.update_geos(fitbounds="locations", visible=False)

        st.plotly_chart(fig, use_container_width=True)

        sub_option = st.selectbox(
                "Select Sub Analysis",
                [
                    "State-wise Penetration",
                    "Growth Trend",
                    "Insurance Type Distribution",
                    "High Value States",
                    "Untapped States"
                ]
            )
        
        if sub_option == "State-wise Penetration":
            query = """
            SELECT State, SUM(Insurance_count) AS total_policies
            FROM agg_insurance
            GROUP BY State
            ORDER BY total_policies DESC;
            """
            df = run_query(query)

            st.subheader("📊 State-wise Insurance Penetration")
            st.dataframe(df)

            fig = px.bar(df, x="State", y="total_policies",
                        title="Insurance Adoption by State")
            st.plotly_chart(fig, use_container_width=True)

            fig = px.bar(
                df,
                x="total_policies",
                y="State",
                orientation="h",
                title="Insurance Penetration (Horizontal View)"
            )
            st.plotly_chart(fig, use_container_width=True)

            fig = px.pie(
                df,
                names="State",
                values="total_policies",
                hole=0.5,
                title="State-wise Insurance Share"
            )
            st.plotly_chart(fig, use_container_width=True)

            fig = px.treemap(
                df,
                path=["State"],
                values="total_policies",
                title="Insurance Penetration by State"
            )
            st.plotly_chart(fig, use_container_width=True)

            # ---------------- 2. GROWTH TREND ----------------
        elif sub_option == "Growth Trend":
            query = """
            SELECT Year, Quarter, SUM(Insurance_count) AS total_policies
            FROM agg_insurance
            GROUP BY Year, Quarter
            ORDER BY Year, Quarter;
            """
            df = run_query(query)

            df["time"] = df["Year"].astype(str) + " Q" + df["Quarter"].astype(str)

            st.subheader("📈 Insurance Growth Trend")
            st.dataframe(df)
            fig = px.bar(
                    df,
                    x="time",
                    y="total_policies",
                    animation_frame="Year",
                    title="Insurance Growth Animation"
                )
            st.plotly_chart(fig, use_container_width=True)

            fig = px.line(df, x="time", y="total_policies",
                        title="Insurance Growth Over Time")
            st.plotly_chart(fig, use_container_width=True)

            fig = px.area(
                df,
                x="time",
                y="total_policies",
                title="Insurance Growth Trend (Area View)"
            )
            st.plotly_chart(fig, use_container_width=True)

            fig = px.bar(
                df,
                x="time",
                y="total_policies",
                title="Quarter-wise Insurance Growth"
            )
            st.plotly_chart(fig, use_container_width=True)

            # ---------------- 3. INSURANCE TYPE DISTRIBUTION ----------------
        elif sub_option == "Insurance Type Distribution":
            query = """
            SELECT Insurance_type, SUM(Insurance_count) AS total_policies
            FROM agg_insurance
            GROUP BY Insurance_type
            ORDER BY total_policies DESC;
            """
            df = run_query(query)

            st.subheader("📊 Insurance Type Distribution")
            st.dataframe(df)

            fig = px.pie(df, names="Insurance_type", values="total_policies",
                        hole=0.5,
                        title="Insurance Type Share")
            st.plotly_chart(fig, use_container_width=True)


            fig = px.bar(
                df,
                x="Insurance_type",
                y="total_policies",
                color="Insurance_type",
                title="Insurance Type Comparison"
            )
            st.plotly_chart(fig, use_container_width=True)

            fig = px.bar(
                df,
                x="total_policies",
                y="Insurance_type",
                orientation="h",
                title="Insurance Type Ranking"
            )
            st.plotly_chart(fig, use_container_width=True)

            # ---------------- 4. HIGH VALUE STATES ----------------
        elif sub_option == "High Value States":
            query = """
            SELECT State, SUM(Insurance_amount) AS total_amount
            FROM agg_insurance
            GROUP BY State
            ORDER BY total_amount DESC;
            """
            df = run_query(query)

            st.subheader("💰 High Value States")
            st.dataframe(df)

            fig = px.treemap(df, path=["State"], values="total_amount",
                            title="Insurance Revenue by State")
            st.plotly_chart(fig, use_container_width=True)

            fig = px.bar(
                df,
                x="State",
                y="total_amount",
                color="State",
                title="Insurance Revenue by State"
            )
            st.plotly_chart(fig, use_container_width=True)
        
            fig = px.bar(
                df,
                x="total_amount",
                y="State",
                orientation="h",
                title="High Value States (Ranking)"
            )
            st.plotly_chart(fig, use_container_width=True)
        
            fig = px.pie(
                df,
                names="State",
                values="total_amount",
                hole=0.5,
                title="State-wise Revenue Share"
            )
            st.plotly_chart(fig, use_container_width=True)
    # ---------------- 5. UNTAPPED STATES ----------------
        elif sub_option == "Untapped States":
            query = """
            SELECT State, SUM(Insurance_count) AS total_policies
            FROM agg_insurance
            GROUP BY State
            ORDER BY total_policies ASC
            LIMIT 10;
            """
            df = run_query(query)

            st.subheader("⚠️ Untapped States (Low Adoption)")
            st.dataframe(df)

            fig = px.bar(df,
                        x="total_policies",
                        y="State",
                        orientation="h",
                        title="Low Insurance Adoption States")
            st.plotly_chart(fig, use_container_width=True)

            fig = px.pie(
                df,
                names="State",
                values="total_policies",
                hole=0.5,
                title="Untapped States Share"
            )
            st.plotly_chart(fig, use_container_width=True)

            fig = px.treemap(
                df,
                path=["State"],
                values="total_policies",
                title="Untapped States Distribution"
            )
            st.plotly_chart(fig, use_container_width=True)

            df["total_policies"] = pd.to_numeric(df["total_policies"], errors="coerce")

            fig = px.scatter(
                df,
                x="State",
                y="total_policies",
                size="total_policies",
                color="State",
                title="Untapped States Opportunity View"
            )
            st.plotly_chart(fig, use_container_width=True)
    #--------------------------------------------------------------------------------------------------------------------

    elif option == "4. Transaction Analysis Across States and Districts":

        st.header("💳 Transaction Analysis")

        sub_option = st.selectbox(
            "Select Sub Analysis",
            [
                "Top States (Volume)",
                "Top States (Value)",
                "State Growth Analysis",
                "High Value States",
                "State Contribution"
            ]
        )

        if sub_option == "Top States (Volume)":

            query = """
            SELECT state, SUM(transaction_count) AS total_count
            FROM agg_transaction
            GROUP BY state
            ORDER BY total_count DESC
            LIMIT 10;
            """

            df = run_query(query)

            st.subheader("📊 Top 10 States by Transaction Volume")
            st.dataframe(df)

            # ---------------- BAR CHART ----------------
            fig1 = px.bar(
                df,
                x="state",
                y="total_count",
                color="state",
                title="Top States - Transaction Volume"
            )
            st.plotly_chart(fig1, use_container_width=True)

            # ---------------- HORIZONTAL BAR ----------------
            fig2 = px.bar(
                df,
                x="total_count",
                y="state",
                orientation="h",
                title="Top States Ranking"
            )
            st.plotly_chart(fig2, use_container_width=True)

            # ---------------- PIE / DONUT ----------------
            fig3 = px.pie(
                df,
                names="state",
                values="total_count",
                hole=0.5,
                title="Transaction Share by State"
            )
            st.plotly_chart(fig3, use_container_width=True)

            # ---------------- TREEMAP ----------------
            fig4 = px.treemap(
                df,
                path=["state"],
                values="total_count",
                title="State Contribution (Treemap)"
            )
            st.plotly_chart(fig4, use_container_width=True)
        #-------------------------------------------------------------------------------------------------------

        elif sub_option == "Top States (Value)":

            query = """
            SELECT state, SUM(transaction_amount) AS total_amount
            FROM agg_transaction
            GROUP BY state
            ORDER BY total_amount DESC
            LIMIT 10;
            """

            df = run_query(query)

            st.subheader("💰 Top 10 States by Transaction Value")
            st.dataframe(df)

            # ---------------- BAR CHART ----------------
            fig1 = px.bar(
                df,
                x="state",
                y="total_amount",
                color="state",
                title="Top States - Transaction Value"
            )
            st.plotly_chart(fig1, use_container_width=True)

            # ---------------- HORIZONTAL BAR ----------------
            fig2 = px.bar(
                df,
                x="total_amount",
                y="state",
                orientation="h",
                title="Top States Ranking (Value)"
            )
            st.plotly_chart(fig2, use_container_width=True)

            # ---------------- DONUT CHART ----------------
            fig3 = px.pie(
                df,
                names="state",
                values="total_amount",
                hole=0.5,
                title="Transaction Value Share"
            )
            st.plotly_chart(fig3, use_container_width=True)

            # ---------------- TREEMAP ----------------
            fig4 = px.treemap(
                df,
                path=["state"],
                values="total_amount",
                title="State Contribution (Value)"
            )
            st.plotly_chart(fig4, use_container_width=True)
        #---------------------------------------------------------------------------

        elif sub_option == "State Growth Analysis":

            query = """
            SELECT State, Year, SUM(Transaction_count) AS total_count
            FROM map_trans
            GROUP BY State, Year
            ORDER BY State, Year;
            """

            df = run_query(query)

            st.subheader("📈 State-wise Transaction Growth")
            st.dataframe(df)
    #-------------line chart----------
            fig_line = px.line(
                df,
                x="Year",
                y="total_count",
                color="State",
                markers=True,
                title="State-wise Growth Trend"
            )

            st.plotly_chart(fig_line, use_container_width=True)
    #--------------grouped bar chart------------------------------
            fig_bar = px.bar(
                df,
                x="Year",
                y="total_count",
                color="State",
                barmode="group",
                title="Year-wise State Comparison"
            )

            st.plotly_chart(fig_bar, use_container_width=True)
    #-----------------stacked area chart-----------------------------
            fig_area = px.area(
                df,
                x="Year",
                y="total_count",
                color="State",
                title="State Contribution Over Time"
            )

            st.plotly_chart(fig_area, use_container_width=True)
    #-------------------------------------------------------------
            fig_anim = px.bar(
                df,
                x="State",
                y="total_count",
                color="State",
                animation_frame="Year",
                range_y=[0, df["total_count"].max()],
                title="State Growth Animation"
            )

            st.plotly_chart(fig_anim, use_container_width=True)
    #-------------------------------------------------------------------------------------------------------------------
        if sub_option == "High Value States":

            query = """
            SELECT 
                State,
                SUM(Transacion_amount) / SUM(Transacion_count) AS avg_value
            FROM top_trans
            GROUP BY State
            ORDER BY avg_value DESC
            LIMIT 10;
            """
            df= run_query(query)
            st.dataframe(df)
            df = df.sort_values("avg_value", ascending=False)

            fig_bar = px.bar(
                df,
                x="State",
                y="avg_value",
                color="State",
                title="Top States by Average Transaction Value"
            )

            st.plotly_chart(fig_bar, use_container_width=True)

            fig_hbar = px.bar(
                df,
                x="avg_value",
                y="State",
                orientation='h',
                color="avg_value",
                title="Average Transaction Value (Horizontal View)"
            )

            st.plotly_chart(fig_hbar, use_container_width=True)

            fig_donut = px.pie(
                df,
                names="State",
                values="avg_value",
                hole=0.5,
                title="Share of Average Transaction Value"
            )

            st.plotly_chart(fig_donut, use_container_width=True)

            fig_tree = px.treemap(
                df,
                path=["State"],
                values="avg_value",
                title="Treemap of Average Transaction Value"
            )

            st.plotly_chart(fig_tree, use_container_width=True)
    #----------------------------------------------------------------------
        if sub_option == "State Contribution":

            query = """  SELECT 
            State,
            SUM(Transacion_count) AS total_count,
            ROUND(
                SUM(Transacion_count) * 100.0 /
                SUM(SUM(Transacion_count)) OVER (), 2
            ) AS contribution_percent
            FROM top_trans
            GROUP BY State
            ORDER BY total_count DESC; """
            df = run_query(query)

            st.subheader("📊 State Contribution to Total Transactions")
            st.dataframe(df)

            fig = px.pie(
                df,
                names="State",
                values="contribution_percent",
                hole=0.5,
                title="State-wise Contribution (%)"
            )

            st.plotly_chart(fig, use_container_width=True)

            fig_hbar = px.bar(
                df.sort_values("contribution_percent", ascending=True),
                x="contribution_percent",
                y="State",
                orientation='h',
                color="contribution_percent",
                title="State Contribution (%) - Ranked"
            )

            st.plotly_chart(fig_hbar, use_container_width=True)

            fig_tree = px.treemap(
                df,
                path=["State"],
                values="contribution_percent",
                title="State Contribution Treemap"
            )

            st.plotly_chart(fig_tree, use_container_width=True)

            df["total_count"] = pd.to_numeric(df["total_count"], errors="coerce")
            df["contribution_percent"] = pd.to_numeric(df["contribution_percent"], errors="coerce")
            fig_scatter = px.scatter(
                df,
                x="total_count",
                y="contribution_percent",
                size="total_count",
                color="State",
                title="Contribution (%) vs Transaction Volume"
            )

            st.plotly_chart(fig_scatter, use_container_width=True)
    #--------------------------------------------------------------------------------------------------------------
    if option == "5. User Registration Analysis":

        st.header("👤 User Registration Analysis")

        sub_option = st.selectbox(
            "Select Sub Analysis",
            [
                "Top States (Users)",
                "Top States (App Opens)",
                "Engagement Analysis",
                "Quarterly Trend",
                "Growth Analysis"
            ]
        )

        if sub_option == "Top States (Users)":

            query = """
            SELECT 
                State,
                SUM(Registered_Users) AS total_users
            FROM map_user
            GROUP BY State
            ORDER BY total_users DESC
            LIMIT 10;
            """

            df = run_query(query)

            st.subheader("🏆 Top States by Registered Users")
            st.dataframe(df)

            fig = px.bar(df, x="State", y="total_users", color="State")
            st.plotly_chart(fig, use_container_width=True)
            df["total_users"] = pd.to_numeric(df["total_users"], errors="coerce")

            fig_donut = px.pie(
                df,
                names="State",
                values="total_users",
                hole=0.5,
                title="State-wise User Share"
            )

            st.plotly_chart(fig_donut, use_container_width=True)

            fig_hbar = px.bar(
                df.sort_values("total_users", ascending=True),
                x="total_users",
                y="State",
                orientation='h',
                color="total_users",
                title="Top States (Horizontal View)"
            )

            st.plotly_chart(fig_hbar, use_container_width=True)

            fig_scatter = px.scatter(
                df,
                x="State",
                y="total_users",
                size="total_users",
                color="State",
                title="User Distribution (Bubble Chart)"
            )

            st.plotly_chart(fig_scatter, use_container_width=True)
        #------------------------------------------------------------------------------------
        elif sub_option == "Top States (App Opens)":

            query = """
            SELECT 
                State,
                SUM(App_Opens) AS total_opens
            FROM map_user
            GROUP BY State
            ORDER BY total_opens DESC
            LIMIT 10;
            """

            df = run_query(query)

            st.subheader("📱 Top States by App Opens")
            st.dataframe(df)

            fig = px.bar(df, x="State", y="total_opens", color="State")
            st.plotly_chart(fig, use_container_width=True)
            df["total_opens"] = pd.to_numeric(df["total_opens"], errors="coerce")

            fig_donut = px.pie(
                df,
                names="State",
                values="total_opens",
                hole=0.5,
                title="State-wise Share of App Opens"
            )

            st.plotly_chart(fig_donut, use_container_width=True)

            fig_hbar = px.bar(
                df.sort_values("total_opens", ascending=True),
                x="total_opens",
                y="State",
                orientation='h',
                color="total_opens",
                title="Top States by App Opens (Horizontal)"
            )

            st.plotly_chart(fig_hbar, use_container_width=True)

            fig_tree = px.treemap(
                df,
                path=["State"],
                values="total_opens",
                title="App Opens Distribution Treemap"
            )

            st.plotly_chart(fig_tree, use_container_width=True)
    #-----------------------------------------------------------------------------------
        elif sub_option == "Engagement Analysis":

            query = """
            SELECT 
                State,
                SUM(App_Opens) / SUM(Registered_Users) AS engagement_ratio
            FROM map_user
            GROUP BY State
            ORDER BY engagement_ratio DESC
            LIMIT 10;
            """

            df = run_query(query)

            st.subheader("🔥 Engagement Ratio (App Opens per User)")
            st.dataframe(df)

            fig = px.bar(df, x="State", y="engagement_ratio", color="State")
            st.plotly_chart(fig, use_container_width=True)
            df["engagement_ratio"] = pd.to_numeric(df["engagement_ratio"], errors="coerce")

            fig_hbar = px.bar(
                df.sort_values("engagement_ratio", ascending=True),
                x="engagement_ratio",
                y="State",
                orientation='h',
                color="engagement_ratio",
                title="Engagement Ratio Ranking"
            )

            st.plotly_chart(fig_hbar, use_container_width=True)

            fig_donut = px.pie(
                df,
                names="State",
                values="engagement_ratio",
                hole=0.5,
                title="Engagement Share by State"
            )

            st.plotly_chart(fig_donut, use_container_width=True)

            fig_scatter = px.scatter(
                df,
                x="State",
                y="engagement_ratio",
                size="engagement_ratio",
                color="State",
                title="Engagement Distribution (Bubble Chart)"
            )

            st.plotly_chart(fig_scatter, use_container_width=True)
    #-----------------------------------------------------------------------------------------
        elif sub_option == "Quarterly Trend":

            query = """
            SELECT 
                Year,
                Quater,
                SUM(Registered_Users) AS total_users
            FROM map_user
            GROUP BY Year, Quater
            ORDER BY Year, Quater;
            """

            df = run_query(query)

            st.subheader("📈 Quarterly User Growth")
            st.dataframe(df)

            df["time"] = df["Year"].astype(str) + "-Q" + df["Quater"].astype(str)

            fig = px.line(df, x="time", y="total_users", markers=True)
            st.plotly_chart(fig, use_container_width=True)        
            df["total_users"] = pd.to_numeric(df["total_users"], errors="coerce")
            df = df.sort_values(["Year", "Quater"])

            fig_area = px.area(
                df,
                x="time",
                y="total_users",
                title="Quarterly User Growth (Area Chart)"
            )

            st.plotly_chart(fig_area, use_container_width=True)

            fig_bar = px.bar(
                df,
                x="time",
                y="total_users",
                color="total_users",
                title="Quarterly User Comparison"
            )

            st.plotly_chart(fig_bar, use_container_width=True)

            pivot_df = df.pivot(index="Year", columns="Quater", values="total_users")

            fig_heatmap = px.imshow(
                pivot_df,
                text_auto=True,
                aspect="auto",
                title="Quarterly User Growth Heatmap"
            )

            st.plotly_chart(fig_heatmap, use_container_width=True)
    #--------------------------------------------------------------------------------------
        elif sub_option == "Growth Analysis":

            query = """
            SELECT 
                State,
                Year,
                SUM(Registered_Users) AS total_users
            FROM map_user
            GROUP BY State, Year
            ORDER BY State, Year;
            """

            df = run_query(query)

            st.subheader("📊 State-wise Growth")
            st.dataframe(df)

            fig = px.line(df, x="Year", y="total_users", color="State", markers=True)
            st.plotly_chart(fig, use_container_width=True)
            df["total_users"] = pd.to_numeric(df["total_users"], errors="coerce")
            df["Year"] = df["Year"].astype(int)
            df = df.sort_values(["State", "Year"])

            fig_area = px.area(
                df,
                x="Year",
                y="total_users",
                color="State",
                title="State Contribution Over Time"
            )

            st.plotly_chart(fig_area, use_container_width=True)

            fig_bar = px.bar(
                df,
                x="Year",
                y="total_users",
                color="State",
                barmode="group",
                title="Year-wise State Comparison"
            )

            st.plotly_chart(fig_bar, use_container_width=True)

            fig_anim = px.bar(
                df,
                x="State",
                y="total_users",
                color="State",
                animation_frame="Year",
                range_y=[0, df["total_users"].max()],
                title="State-wise Growth Animation"
            )

            st.plotly_chart(fig_anim, use_container_width=True)