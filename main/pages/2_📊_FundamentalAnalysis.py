import streamlit as st
import pandas as pd 
from PIL import Image

st.set_page_config(
    page_title="Fundamental Analysis",
    page_icon="📊"
    )

st.markdown("# :green[2. Fundamental Analysis 📊 ]")

layout = "https://bit.ly/financial_statements_analysis"

"----------"

st.title( st.session_state["selected_company"])

#@st.cache_data
def load_financial_statements(): #historical data
    data_fs = pd.read_excel(layout, index_col=0, sheet_name="Income_statement")
    data_fs = data_fs[data_fs["Empresa"]==st.session_state["selected_company"]]
    return data_fs

#@st.cache_data
def load_financial_statements_2023(): #historical data
    data_fs2023 = pd.read_excel(layout, index_col=0, sheet_name="Income_statement_2023")
    data_fs2023 = data_fs2023[data_fs2023["Empresa"]==st.session_state["selected_company"]]
    return data_fs2023

#@st.cache_data
def load_balance_sheet(): #historical data
    data_bs = pd.read_excel(layout, index_col=0, sheet_name="Balance_Sheet")
    data_bs = data_bs[data_bs["Empresa"]==st.session_state["selected_company"]]
    return data_bs

#@st.cache_data
def load_balance_2023(): 
    data_bs2023 = pd.read_excel(layout, index_col=0, sheet_name="Balance_Sheet_2023")
    data_bs2023 = data_bs2023[data_bs2023["Empresa"]==st.session_state["selected_company"]]
    return data_bs2023


data_load_state = st.markdown(":red[Loading data...]")
income_statement = load_financial_statements()
income_statement_2023 = load_financial_statements_2023()
balance_sheet = load_balance_sheet()
balance_sheet_2023 = load_balance_2023()
data_load_state.markdown(':blue[Loading data... done!]')

st.dataframe(income_statement)
st.dataframe(income_statement_2023)

st.dataframe(balance_sheet)
st.dataframe(balance_sheet_2023)


#image = Image.open("./main/img/workin.gif")

#st.image(image, width=325, output_format="GIF")


