#1. Instalar las librerías y configurar la página inicial
import streamlit as st
import pandas as pd 
import numpy as np
import plotly.graph_objects as go
import plotly.express as px 

# Liga de acceso 

layout = "https://bit.ly/financial_statements_analysis"

# Configuración de la página inicial

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
# Income Statement

final_revenues = income_statement['Revenues'].iloc[-1]
initial_revenues = income_statement['Revenues'].iloc[0]
years = len(income_statement['Revenues'])-1

CAGR_Revenues = round(((final_revenues/initial_revenues)**(1/years)-1)*100,2)

final_CoR = income_statement['Cost of revenues'].iloc[-1]
initial_CoR = income_statement['Cost of revenues'].iloc[0]

CAGR_CoR = round(((final_CoR/initial_CoR)**(1/years)-1)*100,2)

final_TCE = income_statement['Total costs and expenses'].iloc[-1]
initial_TCE = income_statement['Total costs and expenses'].iloc[0]

CAGR_TCE = round(((final_TCE/initial_TCE)**(1/years)-1)*100,2)

final_Net_Income = income_statement['Net income'].iloc[-1]
initial_Net_Income = income_statement['Net income'].iloc[0]

CAGR_Net_Income = round(((final_Net_Income/initial_Net_Income)**(1/years)-1)*100,2)

# Balance Sheeet

final_current_assets = balance_sheet['Totalcurrentassets'].iloc[-1]
initial_current_assets = balance_sheet['Totalcurrentassets'].iloc[0]
years_balance = len(balance_sheet['Totalcurrentassets'])-1

CAGR_Current_Asets = round(((final_current_assets/initial_current_assets)**(1/years_balance)-1)*100,2)

final_total_assets = balance_sheet['Totalassets'].iloc[-1]
initial_total_assets = balance_sheet['Totalassets'].iloc[0]

CAGR_Total_Asets = round(((final_total_assets/initial_total_assets)**(1/years_balance)-1)*100,2)

final_current_liabilities = balance_sheet['Totalcurrentliabilities'].iloc[-1]
initial_current_liabilities = balance_sheet['Totalcurrentliabilities'].iloc[0]

CAGR_Current_Liabilities = round(((final_current_liabilities/initial_current_liabilities)**(1/years_balance)-1)*100,2)

final_total_liabilities = balance_sheet['Totalliabilities'].iloc[-1]
initial_total_liabilities = balance_sheet['Totalliabilities'].iloc[0]

CAGR_Total_Liabilities = round(((final_total_liabilities/initial_total_liabilities)**(1/years_balance)-1)*100,2)


# Financial Ratios
# ROE REturn on Equity 

# A. Profit Margin 

Profit_margin = pd.DataFrame({
    'Periodo': income_statement['Periodo'],
    'Profit Margin': (income_statement['Net income'] / income_statement['Revenues']).map('{:.2%}'.format)
})

Profit_margin_bis = pd.DataFrame({
    'Periodo': income_statement['Periodo'],
    'Profit Margin': (income_statement['Net income'] / income_statement['Revenues'])
})

# B. Asset Turnover

Asset_turnover = pd.DataFrame({
    'Periodo': income_statement['Periodo'],
    'Asset Turnover': (income_statement['Revenues']/balance_sheet['Totalassets'])
})

# C. Financial Leverage

Financial_leverage = pd.DataFrame({
    'Periodo': income_statement['Periodo'],
    "Financial Leverage": (balance_sheet['Totalassets']/balance_sheet['Totalstockholders’equity']) 
})

# ROE
ROE_components = pd.DataFrame({
    'Periodo': Financial_leverage['Periodo'],
    "Financial Leverage": Financial_leverage['Financial Leverage'],
    "Asset Turnover":Asset_turnover['Asset Turnover'],
    "Profit Margin" : Profit_margin_bis["Profit Margin"]
})

ROE_components['ROE'] = ROE_components['Financial Leverage'] * ROE_components['Asset Turnover'] * ROE_components['Profit Margin']
ROE_components['ROE'] = ROE_components['ROE'].map('{:.2%}'.format)

# ROA
ROE_components['ROA'] = ROE_components['Asset Turnover'] * ROE_components['Profit Margin']
ROE_components['ROA'] = ROE_components['ROA'].map('{:.2%}'.format)

st.dataframe(ROE_components, hide_index=True)

# CAGR Dataframe 

CAGR = {
    "Revenues":[str(CAGR_Revenues) + "%"],
    "Current Assets": [str(CAGR_Current_Asets) + "%"],
    "Total Assets": [str(CAGR_Total_Asets) + "%"],
    "Current Liabilities": [str(CAGR_Current_Liabilities) + "%"],
    "Total Liabilities": [str(CAGR_Total_Liabilities) + "%"],
    "Cost of Revenues": [str(CAGR_CoR) + "%"] ,
    "Total Cost and Expenses": [str(CAGR_TCE) + "%"],
    "Net Income": [str(CAGR_Net_Income) + "%"]
}

resume_financial = pd.DataFrame(CAGR, index=["CAGR"]) 
resume_financial = resume_financial.T

st.markdown("### :green[CARG]")

st.dataframe(resume_financial)

# Visualization 

#Gráficos

empresa = st.session_state["selected_company"]

#************************************
        # Profit Margin Chart
#************************************

ProfitMarginChart = px.line(
     Profit_margin, 
     x='Periodo', 
     y = ['Profit Margin'],
     title = f"{empresa} - Profit Margin",
     )

ProfitMarginChart.update_xaxes(title_text="Year")

ProfitMarginChart.update_yaxes(
    title_text="%",
    #range=[5, max(Profit_margin['Profit Margin'])]
    )

ProfitMarginChart.update_layout(
     height = 380,
     width=480,
     showlegend= False,
     title_font=dict(
          color="#027034",
          size=20
          )
     )

ProfitMarginChart.update_traces(line=dict(color='red'),
                                          mode= "markers+lines")

#************************************
        # Asset Turnover Chart
#************************************

AssetTurnoverChart = px.line(
    Asset_turnover, 
    x='Periodo', 
    y = ['Asset Turnover'],
    title = f"{empresa} - Asset Turnover",
    )

AssetTurnoverChart.update_xaxes(title_text="Year")

AssetTurnoverChart.update_yaxes(title_text="Times")
    
AssetTurnoverChart.update_layout(
    height = 380,
    width=480,
    showlegend= False,
    title_font=dict(
        color="#027034",
        size=20
        )
    )

AssetTurnoverChart.update_traces(line=dict(color='#581845'),
                                line_width=2.8,
                                line_shape ="linear",
                                mode= "markers+lines")

#************************************
        # Financial Leverage Chart
#************************************

FinancialLeverageChart = px.line(
    Financial_leverage, 
    x='Periodo', 
    y = ['Financial Leverage'],
    title = f"{empresa} - Financial Leverage",
    )

FinancialLeverageChart.update_xaxes(title_text="Year")

FinancialLeverageChart.update_yaxes(
    title_text="Times")
    
FinancialLeverageChart.update_layout(
    height = 380,
    width=480,
    showlegend= False,
    title_font=dict(
        color="#027034",
        size=20
        )
    )

FinancialLeverageChart.update_traces(line=dict(color='#581845'),
                                line_width=2.8,
                                line_shape ="linear",
                                mode= "markers+lines")

#************************************
        # ROE Chart
#************************************

ROEChart = px.line(
    ROE_components, 
    x='Periodo', 
    y = ['ROE', 'ROA'],
    title = f"{empresa} - ROE and ROA",
    color_discrete_map={'ROE': 'blue', 'ROA': 'green'}
    )

ROEChart.update_xaxes(title_text="Year")

ROEChart.update_yaxes(title_text="%")

ROEChart.update_layout(
    height = 380,
    width=480,
    title_font=dict(color="#027034",
        size=20
        )
    )

ROEChart.update_traces(line=dict(),
                                line_width=2.8,
                                line_shape ="linear",
                                mode= "markers+lines")

#************************************
        # Show Info
#************************************

st.markdown("## :green[The Levels of Financial Performance]")

st.markdown("## :green[The Three Determinats of ROE]")

st.markdown("### :green[1. Profit Margin]")

col1, col2 = st.columns([5,2])

with col1:
    st.plotly_chart(ProfitMarginChart)

with col2:
    st.subheader("Data")
    st.dataframe(Profit_margin, hide_index=True)
    

st.markdown("### :green[2. Asset Turnover]")

col3, col4 = st.columns([5,2])

with col3:
    st.plotly_chart(AssetTurnoverChart)

with col4:
    st.subheader("Data")
    st.dataframe(Asset_turnover, hide_index=True)

st.markdown("### :green[3. Financial Leverage]")

col5, col6 = st.columns([5,2])

with col5:
    st.plotly_chart(FinancialLeverageChart)

with col6:
    st.subheader("Data")
    st.dataframe(Financial_leverage, hide_index=True)

st.markdown("### :green[ROE - ROA]")

col7, col8 = st.columns([5,2])

with col7:
    st.plotly_chart(ROEChart)

with col8:
    st.subheader("Data")
    st.dataframe(ROE_components[['Periodo', 'ROE', 'ROA']], hide_index=True)

