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

st.write("Linear Regression")

st.write("https://pypi.org/project/yfinance/")

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

# 4.3 Rendimiento anual

data['DeltaD'] = data.Close.pct_change(1)
rendimiento_anual_simple = round(data['DeltaD'].mean()*252, 2)*100

# 4.4 CARG

CAGR = round((((data['Close'].iloc[-1] / (data['Close'].iloc[0])) ** (1/ len(data['Close'])) -1)*100)*252,2)

# 4.5 Varianza

var = data['DeltaD'].var()
volatilidad = round(data['DeltaD'].std()*252**0.5,4)*100



st.write(f"Rendimiento histórico anual simple es de: " + str(rendimiento_anual_simple)+ "%")

st.write(f"La volatildiad anual es de: " + str(volatilidad)+ "%")

st.write(f"CAGR: " + str(CAGR)+ "%")

metricas = data['Close'].loc['2023': ].describe() 

st.markdown("**Estadísticas 2023 - Precio de Cierre**")

st.text(metricas)

st.markdown("**Gráficas**")

# 5. Generar las gráficas:

st.line_chart(data, x= 'Date', y='IncBase5Y', color="#FF0000")

st.line_chart(data, x= 'Date', y=['Close'], color="#338AFF")

st.write("Predictor")
fig, ax = plt.subplots() 
data['Pred'].plot(ax=ax, linestyle = "-", lw=2)
data['Close'].plot(ax=ax, lw=2)
ax.set_title(f'Predict prices: {ticker}')
st.pyplot(fig)

st.write(r2_score(data['Close'], data['Pred']))
st.write(lin_model.coef_ * len(data) + 5 + lin_model.intercept_)

# 5.3 Candlesticks
figura  = go.Figure(data = [go.Candlestick(x=data_2022['Date'], 
                                open = data_2022['Open'],
                                high = data_2022['High'],
                                low = data_2022['Low'],
                                close = data_2022['Close'])])

st.plotly_chart(figura, use_container_width = True)

# 5.4 Rendimientos

datos = data['DeltaD']
figura_2, ejes = plt.subplots()
ejes.hist(datos, bins=40, color="#FF4C33", edgecolor="#635E5D")
figura_2

if st.checkbox("Show Dataframe and Chart"):
    chart_data = pd.DataFrame(
     np.random.randn(20, 3),
     columns=['first', 'second', 'third'])
    st.dataframe(chart_data.style.highlight_max(axis=0))
    st.write("Gráfico o Chart")
    st.line_chart(chart_data)
else:
    st.write("Nothing to show")


st.write('De DataFrame a Table')

st.table(chart_data)

st.write("Drawing a Map")

map_data = pd.DataFrame(
    np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
    columns=['lat', 'lon'])

st.map(map_data)

x = st.slider('x')
st.write(x, 'squared is:', x*x)
st.write(x, 'sum x plus x is:', x+x)

option = st.selectbox(
    'Which number do you like best?',
     chart_data['first'])

'You selected: ', option

add_selectbox = st.sidebar.selectbox(
    'How would you like to be contacted?',
    ('Email', 'Home phone', 'Mobile phone')
)

add_slider = st.sidebar.slider(
    'Select a range of values',
    0.0, 100.0, (25.0, 75.0)
)

left_column, right_column = st.columns(2)
# You can use a column just like st.sidebar:
left_column.button('Press me!')

# Or even better, call Streamlit functions inside a "with" block:
with right_column:
    chosen = st.radio(
        'Sorting hat',
        ("Gryffindor", "Ravenclaw", "Hufflepuff", "Slytherin"))
    st.write(f"You are in {chosen} house!")