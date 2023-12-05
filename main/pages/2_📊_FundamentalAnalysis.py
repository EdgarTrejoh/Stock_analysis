#1. Instalar las librerías y configurar la página inicial
import streamlit as st
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import plotly.express as px 
from PIL import Image

# Liga para obtener la información 

layout = "https://bit.ly/financial_statements_analysis"

# Configurar la página inicial

st.set_page_config(
    page_title="Fundamental Analysis",
    page_icon="📊"
    )

st.markdown("# :green[2. Fundamental Analysis 📊]")

"----------"

st.title(st.session_state["selected_company"])

#@st.cache_data
def load_financial_statements(): #historical data
    data_fs = pd.read_excel(layout, sheet_name="Income_statement")
    data_fs = data_fs[data_fs["Empresa"]==st.session_state["selected_company"]]
    return data_fs

#@st.cache_data
def load_financial_statements_2023(): #historical data
    data_fs2023 = pd.read_excel(layout, sheet_name="Income_statement_2023")
    data_fs2023 = data_fs2023[data_fs2023["Empresa"]== st.session_state["selected_company"]]
    return data_fs2023

#@st.cache_data
def load_balance_sheet(): #historical data
    data_bs = pd.read_excel(layout, sheet_name="Balance_Sheet")
    data_bs = data_bs[data_bs["Empresa"]==st.session_state["selected_company"]]
    return data_bs

#@st.cache_data
def load_balance_2023(): 
    data_bs2023 = pd.read_excel(layout, sheet_name="Balance_Sheet_2023")
    data_bs2023 = data_bs2023[data_bs2023["Empresa"]==st.session_state["selected_company"]]
    return data_bs2023

data_load_state = st.markdown(":red[Loading data...]")
income_statement = load_financial_statements()
income_statement_2023 = load_financial_statements_2023()
balance_sheet = load_balance_sheet()
balance_sheet_2023 = load_balance_2023()
data_load_state.markdown(':blue[Loading data... done!]')

income_statement['Periodo'] = income_statement['Periodo'].astype(str)
income_statement_2023['Periodo'] = income_statement_2023['Periodo'].astype(str)
balance_sheet['Periodo'] = balance_sheet['Periodo'].astype(str)
balance_sheet_2023['Periodo'] = balance_sheet_2023['Periodo'].astype(str)

st.dataframe(income_statement)
st.dataframe(income_statement_2023)

st.dataframe(balance_sheet)
st.dataframe(balance_sheet_2023)

# CAGR 
# Revenues

div = np.divide (
    (income_statement['Revenues'].iloc[-1]),
    (income_statement['Revenues'].iloc[0])
)

exp = np.divide(1,
                len(
                    income_statement['Revenues']
                    )-1
)


CAGR_Revenues = round(((div**exp)-1)*100,2)

# Total current Assets

div01 = np.divide (
        (balance_sheet['Totalcurrentassets'].iloc[-1]),
        (balance_sheet['Totalcurrentassets'].iloc[0])
    )

exp01 = np.divide(1,
                    len(
                        balance_sheet['Totalcurrentassets']
                        )-1
                        )

CAGR_Current_Asets = round(((div01**exp01)-1)*100,2)

# Financial ratios
# Profit Margin 

pf_margin = (income_statement['Net income'] / income_statement['Revenues']) *100
Profit_margin = pd.DataFrame(pf_margin, columns=["Profit Margin"])
Profit_margin['Periodo'] = income_statement['Periodo']
column_order = ['Periodo', 'Profit Margin']
Profit_margin = Profit_margin[column_order]

# CAGR Dataframe 

financial_ratios = {
    "Revenues":[str(CAGR_Revenues) + "%"],
    "Current Assets": [str(CAGR_Current_Asets) + "%"]   
}

resume_financial = pd.DataFrame(financial_ratios, index=["CAGR"]) 
resume_financial = resume_financial.T

st.markdown("### :green[CARG]")

st.dataframe(resume_financial)

# Visualization 
#Profit Margin

st.markdown("### :green[Profit Margin]")

#Gráficos

empresa = st.session_state["selected_company"]

ProfitMarginChart = px.line(
     Profit_margin, 
     x='Periodo', 
     y = ['Profit Margin']
     )

ProfitMarginChart.update_xaxes(title_text="Year",
                        )

ProfitMarginChart.update_yaxes(
    title_text="Texto",
    tickprefix="%",
    range=[5, max(Profit_margin['Profit Margin'])])


ProfitMarginChart.update_layout(
     title_text = (f"{empresa} - Profit Margin"),
     height = 400,
     width=500,
     showlegend= False,
     title_font=dict(
          color="#027034",
          size=20
          )
     )

ProfitMarginChart.update_traces(line=dict(color='red'))


col1, col2 = st.columns([5,2])

with col1:
    st.subheader("Line Chart")
    st.plotly_chart(ProfitMarginChart)

with col2:
    st.subheader("Data")
    st.dataframe(Profit_margin, hide_index=True)
    


#image = Image.open("./main/img/workin.gif")

#st.image(image, width=325, output_format="GIF")


