#1. Instalar las librerías
import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import plotly.graph_objects as go
import plotly.express as px 

#2. Definir las variables
stocks = ("Microsoft", "Apple", "Google", "Amazon", "Tesla", "Walmart")
empresa =st.selectbox(":blue[***Please select an option:***]", stocks) 

if empresa == "Microsoft":
     ticker = "MSFT"
elif empresa == "Apple":
     ticker = "AAPL"
elif empresa == "Google":
     ticker = "GOOG"
elif empresa == "Amazon":
     ticker = "AMZN" 
elif empresa == "Tesla":
     ticker = "TSLA"
elif empresa == "Walmart":
     ticker =  "WMT"

#3. Generar la información:

data = yf.download(ticker, period = "5Y", progress = False)
data_2022 = data.loc["07-2023":]
data_2022.reset_index(inplace=True)
data.reset_index(inplace=True)

#4. Realizar los modelos:
#4.1 Modelo de Regresión lineal:
data['Numbers']  = list(range(0, len(data)))
X = np.array(data[['Numbers']])
Y = data["Close"].values
lin_model = LinearRegression().fit(X ,Y)
print ('Intercept:', lin_model.intercept_)
print ('Slope:' , lin_model.coef_)
y_pred = lin_model.coef_ * X + lin_model.intercept_
data['Pred'] = y_pred

#4.2 Crecimiento base - 5Y
data['IncBase5Y'] = data.Close.div(data.Close.iloc[0]).mul(100)

#4.3 Rendimiento anual simple
data['DailyReturn'] = data.Close.pct_change(1)
rendimiento_anual_simple = round(data['DailyReturn'].mean()*252, 2)*100

#4.4 CARG
CAGR = round((((data['Close'].iloc[-1] / (data['Close'].iloc[0])) ** (1/ len(data['Close'])) -1)*100)*252,2)

#4.5 Varianza
var = data['DailyReturn'].var()
volatilidad = round(data['DailyReturn'].std()*252**0.5,4)*100

#4.6 SMA
SMA_S = 10
SMA_L = 50
data['SMA_S'] = data['Close'].rolling(SMA_S).mean()
data['SMA_L'] = data['Close'].rolling(SMA_L).mean()
data_SMA = data.loc["2022":]

#4.7 Maximum Drawdown
rolling_max = data['Close'].cummax()
daily_drawdown = data['Close'] / rolling_max - 1
max_drawdown = daily_drawdown.cummin().iloc[-1]

#4.8 Standard Deviation
standard_deviation = data['DailyReturn'].std()
standard_deviation_price = data['Close'].std()

#4.9 Estadísticas 
start = data['Date'].iloc[0]
end = data['Date'].iloc[-1]
mean = str(round(data['Close'].mean(),2))
max = str(round(data['Close'].max(),2))
min = str(round(data['Close'].min(),2))
count = str(round(data['Close'].count(),2))
standard_deviation = str(round(standard_deviation,2))
standard_deviation_price = str(round(standard_deviation_price,2))

#4.9.1 Dataframe Resumen de Indicadores 
data_resume = {'Start Date': [start],
               'End Date': [end],
               "Period (days)":[count],
               "Avg. Close Price": [mean],
               "Max. Close Price": [max],
               "Min. Close Price": [min],
               "Std (Close Price)": [standard_deviation_price],
               "RoR": [str(rendimiento_anual_simple)+ "%"],
               "Volatility": [str(round(volatilidad,2))+ "%"],
               "CAGR": [str(CAGR)+ "%"],
               "Maximum Drawdown": [round(max_drawdown,2)]
            }

resume = pd.DataFrame(data_resume, index=["Valor"]) 
resume = resume.T

#5. Visualización de resultados
#5.1 Estadísticas
st.markdown(
     """
     > ### 📊 Statistics

     """
     )

st.title(empresa)

st.dataframe(resume, hide_index= False, width=340, height=422)

#metricas = data['Close'].describe() 
#st.text(metricas)

#5.2 Gráficos:
#5.2.1 Time Series

st.markdown(
     """
     > ### 📈 Technichal Charts
     
     **1. Time Series**

     """
     )

config = {
     'modeBarButtonsToRemove': ['zoom', 'pan'],
    
}

figura_line = px.line(x=data['Date'], y=data['Close'])
figura_line.update_xaxes(title_text="Date")
figura_line.update_yaxes(title_text="Close Price",
                         tickprefix="$")
figura_line.update_layout(title_text=f"{empresa} - Time Series",
                         title_font=dict(color="#08123E", 
                                         size=18))

st.plotly_chart(figura_line, use_container_width=True)

#5.2.2 Crecimiento en 5Y

st.markdown(
     """
         
    **2. Crecimiento de 5Y a la fecha**

     """
     )

grafica_5Y = go.Figure()
grafica_5Y.add_trace(go.Scatter(
                     x=data['Date'],
                     y=data['IncBase5Y'],
                     mode="lines",
                     ))
grafica_5Y.update_xaxes(title_text="Date")
grafica_5Y.update_yaxes(title_text="Crecimiento (%)")
grafica_5Y.update_layout(title_text=f"{empresa} - Crecimiento 5Y",
                         title_font=dict(color="#08123E", 
                                         size=18))

st.plotly_chart(grafica_5Y, use_container_width=True)

#5.2.3 Gràfico de Vela Candlesticks
st.markdown(
     """   
    **3. Candlestick**
    
    *Información de Julio 2023 a la fecha.*

     """
     )

figura  = go.Figure(data = [go.Candlestick(x=data_2022['Date'], 
                                open = data_2022['Open'],
                                high = data_2022['High'],
                                low = data_2022['Low'],
                                close = data_2022['Close'])])

st.plotly_chart(figura, use_container_width = True)

st.markdown(
     """
    
    **4. Hitograms**

     """
     )

#5.2.4 Histograma precio de cierres
histogram_price = px.histogram(data, x=data['Close'], 
                         nbins=150,
                         color_discrete_sequence=['indianred'],
                         marginal='box',

                         title=f"Histogram Close Price: {empresa}" )
st.plotly_chart(histogram_price, use_container_width = True)

#5.2.5 Histograma con rendimientos
histogram = px.histogram(data, x=data['DailyReturn'], 
                         nbins=30,
                         color_discrete_sequence=['indianred'],
                         marginal='box',

                         title=f"Histogram Daily Returns: {empresa}" )
st.plotly_chart(histogram, use_container_width = True)

st.markdown(
     """
    
    **5. Simple Moving Average (SMA)**
    
     """
     )

#5.2.6 SIMPLE MOVING AVERAGE 
fig_SMA =  px.line(data, x='Date',y=['Close', 'SMA_S','SMA_L'],
                   title=f"SMA: {empresa} ")

fig_SMA.update_layout(title_font=dict(color="#3408D9", 
                                         size=18))

st.plotly_chart(fig_SMA)

#st.line_chart(data_SMA, x= 'Date', y=['Close', 'SMA_S','SMA_L'])

st.markdown(
     """
    
    **5. Tendencia Precio de Cierre**
    
     """
     )

fig, ax = plt.subplots() 
data['Pred'].plot(ax=ax, linestyle = "-", lw=2)
data['Close'].plot(ax=ax, lw=2)
ax.set_title(f'Predict prices: {ticker}')
st.pyplot(fig)

st.write(r2_score(data['Close'], data['Pred']))
st.write(lin_model.coef_ * len(data) + 5 + lin_model.intercept_)