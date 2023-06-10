# imports
import streamlit as st
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import seaborn as sns
import plotly.express as px



#Load Data
@st.cache_data
def load_data(data):
    df = pd.read_csv(data)
    return df


def run_eda_app():
    st.subheader("Data Analysis")
    # df = pd.read_csv("data/diabetes_data_upload.csv")
    df = load_data("data/diabetes_data_upload.csv")
    df_encoded = load_data("data/diabetes_data_clean.csv")
    freq_df = load_data("data/freqdist_of_age_data.csv")

    submenu = st.sidebar.selectbox("Submenu",
                                    ["Descriptive Analysis", 
                                     "Plots"])
    
    if submenu =="Descriptive Analysis":
        st.dataframe(df)

        with st.expander("Data Types"):
            st.dataframe(df.dtypes)

        with st.expander("Statistical Summary"):
            st.dataframe(df_encoded.describe())

        with st.expander("Class Distribution"):
            st.dataframe(df["class"].value_counts())

        with st.expander("Gender Distribution"):
            st.dataframe(df["Gender"].value_counts())


    elif submenu == "Plots":
        st.subheader("Plots")

        # Layouts

        col1, col2 = st.columns([2,1]) # first column 2 times size of second

        with col1:
            # Gender Distibution
            with st.expander("Distribution Plot of Gender"):
                fig = plt.figure()
                sns.countplot(x = df["Gender"])
                st.pyplot(fig)
                
                gen_df = df["Gender"].value_counts().to_frame()
                gen_df = gen_df.reset_index()
                gen_df.columns = ["Gender","Count"]
                # st.dataframe(gen_df)

                p1 = px.pie(gen_df, names="Gender",values="Count")
                st.plotly_chart(p1, use_container_width=True)
            
            # Class Distribution
            with st.expander("Distribution Plot of Class"):
                fig = plt.figure()
                sns.countplot(x = df["class"])
                st.pyplot(fig)

        with col2:
            with st.expander("Gender Distribution"):
                st.dataframe(gen_df)

            with st.expander("Class Distribution"):
                gen_df = df["class"].value_counts().to_frame()
                st.dataframe(gen_df)

        # Freq Distribution
        with st.expander("Frequency Distribution of Age"):
            st.dataframe(freq_df)
            p2 = px.bar(freq_df, x="Age" , y ="count")
            st.plotly_chart(p2)

        # Outlier Detection
        with st.expander("Outlier Detection"):
        #    fig = plt.figure()
        #    sns.boxplot(df["Age"])
        #    st.pyplot(fig)
            p3 = px.box(df, x="Age", color="Gender")
            st.plotly_chart(p3, use_container_width=True)

        # Correlation
        with st.expander("Correlations & Heatmap"):
            corr_matrix = df_encoded.corr()
            fig = plt.figure(figsize=(15,13), dpi=300)
            sns.heatmap(corr_matrix, annot=True)
            st.pyplot(fig)

            p4 = px.imshow(corr_matrix)
            st.plotly_chart(p4, use_container_width=True)