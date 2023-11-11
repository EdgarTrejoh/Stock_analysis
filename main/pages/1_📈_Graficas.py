# 1. Instalar las librerías
import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
import plotly.graph_objects as go

# 2. Definir las variables
ticker = st.text_input("Ticker:", key="ticker")

# 3. Generar la información:
if ticker !="" :   
    data = yf.download(ticker, period = "5Y", progress = False)
    data_2022 = data.loc["07-2023":]
    data_2022.reset_index(inplace=True)
    data.reset_index(inplace=True)
    #st.table(data)
else:
        st.write("Nothing to show")

# 4. Realizar los Cálculos:
# 4.1 Modelo de Regresión lineal:
data['Numbers']  = list(range(0, len(data)))
X = np.array(data[['Numbers']])
Y = data["Close"].values
lin_model = LinearRegression().fit(X ,Y)
print ('Intercept:', lin_model.intercept_)
print ('Slope:' , lin_model.coef_)
y_pred = lin_model.coef_ * X + lin_model.intercept_
data['Pred'] = y_pred

# 4.2 Crecimiento base - 5Y
data['IncBase5Y'] = data.Close.div(data.Close.iloc[0]).mul(100)

# 4.3 Rendimiento anual simple
data['DeltaD'] = data.Close.pct_change(1)
rendimiento_anual_simple = round(data['DeltaD'].mean()*252, 2)*100

# 4.4 CARG
CAGR = round((((data['Close'].iloc[-1] / (data['Close'].iloc[0])) ** (1/ len(data['Close'])) -1)*100)*252,2)

# 4.5 Varianza
var = data['DeltaD'].var()
volatilidad = round(data['DeltaD'].std()*252**0.5,4)*100

# 4.6 SMA
SMA_S = 10
SMA_L = 50
data['SMA_S'] = data['Close'].rolling(SMA_S).mean()
data['SMA_L'] = data['Close'].rolling(SMA_L).mean()
data_SMA = data.loc["2022":]

st.markdown(
     """
     > ### 📂 Indicadores Financieros 
    
     """
     )

st.markdown(f" **- Rendimiento histórico anual simple** es de: " + str(rendimiento_anual_simple)+ "%")
st.markdown(f" **- VolatilIdad anual** es de: " + str(volatilidad)+ "%")
st.markdown(f" **- CAGR** es de: " + str(CAGR)+ "%")

metricas = data['Close'].loc['2023': ].describe() 

st.markdown(
     """
     > ### 📊 Estadísticas 2023 - Precio de Cierre

     """
     )

st.text(metricas)

# 5. Generar las gráficas:
# 5.1 Serie de tiempo del precio de cierre
st.markdown(
     """
     > ### 📈 Gráficas

    **1. Serie de tiempo**
    
    *Precio de cierre*

     """
     )
st.line_chart(data, x= 'Date', y=['Close'], color="#338AFF")

st.markdown(
     """
    
    **2. Crecimiento de 5Y a la fecha**

     """
     )

st.line_chart(data, x= 'Date', y='IncBase5Y', color="#FF0000")

st.markdown(
     """
    
    **3. Gráfico de velas**
    
    *Información de Julio 2023 a la fecha.*

     """
     )

# 5.3 Candlesticks
figura  = go.Figure(data = [go.Candlestick(x=data_2022['Date'], 
                                open = data_2022['Open'],
                                high = data_2022['High'],
                                low = data_2022['Low'],
                                close = data_2022['Close'])])

st.plotly_chart(figura, use_container_width = True)

st.markdown(
     """
    
    **4. Hitograma de rendimiento diario**

     """
     )

# 5.4 Histograma con rendimientos
datos = data['DeltaD']
figura_2, ejes = plt.subplots()
ejes.hist(datos, bins=40, color="#FF4C33", edgecolor="#635E5D")
figura_2

st.markdown(
     """
    
    **5. Simple Moving Average (SMA)**
    
    *Información de Enero 2020 a la fecha.*

     """
     )

# 5.5 SIMPLE MOVING AVERAGE 
st.line_chart(data_SMA, x= 'Date', y=['Close', 'SMA_S','SMA_L'])

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