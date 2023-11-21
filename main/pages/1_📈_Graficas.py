#1. Instalar las librerías
import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px 
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from plotly.subplots import make_subplots

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

def load_stock(stock):
  data = yf.download(stock, period = "5Y", progress = False)
  data.reset_index(inplace=True)
  return data

data_load_state = st.markdown(":red[Loading data...]")
data = load_stock(ticker)
data.reset_index(inplace=True)
data_load_state.markdown(':blue[Loading data... done!]')

#data = yf.download(ticker, period = "5Y", progress = False)
data23 = data.loc[data['Date'] > "07-2023"]
#data_2022 = data.loc["01-07-2023":]
data23.reset_index(inplace=True)
#data.reset_index(inplace=True)

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

#4.3.1 Rendimiento logarítmico
data['LogReturn'] = np.log(data.Close/data.Close.shift(1)).dropna() 
rendimiento_anual_simple = round(data['DailyReturn'].mean()*252, 2)*100
log_return = data['LogReturn'].mean()*252

#4.4 CARG
CAGR = round((((data['Close'].iloc[-1] / (data['Close'].iloc[0])) ** (1/ len(data['Close'])) -1)*100)*252,2)

#4.5 Varianza
var = data['DailyReturn'].var()
volatilidad = round(data['DailyReturn'].std()*252**0.5,4)*100

#4.6 SMA
SMA10 = 10
SMA50 = 50
data['SMA10'] = data['Close'].rolling(SMA10).mean()
data['SMA50'] = data['Close'].rolling(SMA50).mean()
data_SMA = data.loc["2022":]

#4.7 Maximum Drawdown
rolling_max = data['Close'].cummax()
daily_drawdown = data['Close'] / rolling_max - 1
max_drawdown = (daily_drawdown.cummin().iloc[-1])*100

#4.8 Standard Deviation
standard_deviation = data['DailyReturn'].std()
standard_deviation_price = data['Close'].std()

#4.9 MACD (Moving Average Convergence Divergence)
exponential_small = data['Close'].ewm(span=8, adjust= False).mean() # ewm = Provide exponentially weighted (EW) calculations.
exponental_large =  data['Close'].ewm(span=17, adjust= False).mean()
data['MACD'] = exponential_small - exponental_large 
data['MACD_Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

#4.10 MACD (Moving Average Convergence Divergence)
data['TypicalPrice'] =(data['Close'] + data['High']+ data['Low']) / 3 
data['Std'] = data['TypicalPrice'].rolling(20).std(ddof=0)
data['MA-Close'] = data['TypicalPrice'].rolling(20).mean()
data['BOLU'] = data['MA-Close'] + 2 * data['Std'] 
data['BOLD'] = data['MA-Close'] - 2 * data['Std']

#4.10 Estadísticas 
start = data['Date'].iloc[0]
end = data['Date'].iloc[-1]
mean = str(round(data['Close'].mean(),2))
max = str(round(data['Close'].max(),2))
min = str(round(data['Close'].min(),2))
count = str(round(data['Close'].count(),2))
standard_deviation = str(round(standard_deviation,2))
standard_deviation_price = str(round(standard_deviation_price,2))
log_return = str(round(log_return,2)*100)

#4.10.1 Dataframe Resumen de Indicadores 
data_resume = {'Start Date': [start],
               'End Date': [end],
               "Period (days)":[count],
               "Avg. Close Price": [mean],
               "Max. Close Price": [max],
               "Min. Close Price": [min],
               "Std (Close Price)": [standard_deviation_price],
               "RoR": [str(rendimiento_anual_simple)+ "%"],
               "Log. Return": [str(log_return) + "%"],
               "Volatility": [str(round(volatilidad,2))+ "%"],
               "CAGR": [str(CAGR)+ "%"],
               "Maximum Drawdown": [str(round(max_drawdown,2))+"%"]
            }

resume = pd.DataFrame(data_resume, index=["Valor"]) 
resume = resume.T

#5. Visualización de resultados
#5.1 Estadísticas
st.markdown(
     """
     > ### 📊 :blue[Statistics]

     """
     )

st.title(empresa)

st.dataframe(resume, hide_index= False, width=340, height=455)

#metricas = data['Close'].describe() 
#st.text(metricas)
#st.dataframe(data)

#5.2 Gráficos:
#5.2.1 Time Series
st.markdown(
     """
     > ### 📈 :blue[Technichal Charts]
     
     >> ### :green[1. Time Series]

     """
     )

config = {
     'modeBarButtonsToRemove': ['zoom', 'pan'],
}

figura_line = px.line(data, x='Date', y=['Close', 'Open', 'High', 'Low'])
figura_line.update_xaxes(title_text="Date")
figura_line.update_yaxes(title_text="Price USD($)",
                         tickprefix="$")
figura_line.update_layout(title_text=f"{empresa} - Time Series",
                         title_font=dict(color="#08123E", 
                                         size=18))

st.plotly_chart(figura_line, use_container_width=True)

#5.2.2 Crecimiento en 5Y
st.markdown(
     """
         
    >> ### :green[2. Crecimiento de 5Y a la fecha]

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

#5.2.3 Gráfico de Vela Candlesticks
st.markdown(
     """   
    >> ### :green[3. Candlestick]
    
    *Información de Julio 2023 a la fecha.*

     """
     )

figura  = go.Figure(data = [go.Candlestick(x=data23['Date'], 
                                open = data23['Open'],
                                high = data23['High'],
                                low = data23['Low'],
                                close = data23['Close'])])

st.plotly_chart(figura, use_container_width = True)

#5.2.4 Histogramas
st.markdown(
     """
    
    >> ### :green[4. Hitograms]

     """
     
     )

#5.2.4.1 Histograma precio de cierre
histogram_price = px.histogram(data, x=data['Close'], 
                         nbins=150,
                         color_discrete_sequence=['indianred'],
                         marginal='box',

                         title=f"Histogram Close Price: {empresa}" )
st.plotly_chart(histogram_price, use_container_width = True)

#5.2.4.2 Histograma rendimiento diario
histogram = px.histogram(data, x=data['DailyReturn'], 
                         nbins=30,
                         color_discrete_sequence=['indianred'],
                         marginal='box',

                         title=f"Histogram Daily Returns: {empresa}" )
st.plotly_chart(histogram, use_container_width = True)

#5.2.5 Moving Average
st.markdown(
     """
          
     >> ### :green[5. Moving Average]

     """
     )
#:green[Additional Information:]
periods = st.slider(":red[**Selecciona el periodo (Días)**]", 10 ,100, step=10)
data['MA'] = data['Close'].rolling(periods).mean()

fig_MA =  px.line(data, 
                  x='Date',
                  y=['Close', 'MA'],
                  color_discrete_sequence= px.colors.sequential.GnBu_r, 
                  #px.colors.sequential.Plasma_r,
                  title=f"Moving Average: {empresa}  \n Periods: {periods}")

fig_MA.update_layout(title_font=dict(color="#3408D9", 
                                         size=18))

st.plotly_chart(fig_MA)

#5.2.5 Simple Moving Average (SMA)
st.markdown(
     """
    
    >> ### :green[6. Simple Moving Average (SMA)]
    
     """
     )

fig_SMA =  px.line(data, x='Date',y=['Close', 'SMA_S','SMA_L'],
                   title=f"SMA: {empresa} ")

fig_SMA.update_layout(title_font=dict(color="#3408D9", 
                                         size=18))

st.plotly_chart(fig_SMA)

#st.line_chart(data_SMA, x= 'Date', y=['Close', 'SMA_S','SMA_L'])

#5.2.6 MACD (Moving Average Convergence Divergence)

st.markdown(
     """
    
    >> ### :green[7. MACD (Moving Average Convergence Divergence)]
    
     """
     )

fig_MACD = make_subplots(specs= [[{"secondary_y": True}]])

fig_MACD.add_trace(
     go.Scatter(x=data['Date'], y=data['MACD'], name = "MACD"),
     secondary_y =False, 
)

fig_MACD.add_trace(
     go.Scatter(x=data['Date'], y=data['MACD_Signal_Line'], name = "Signal Line"),
     secondary_y =False, 
)

fig_MACD.add_trace(
     go.Line(x=data['Date'], y=data['Close'], name = "Close Price"),
     secondary_y =True, 
)

fig_MACD.update_layout(
     title_text = f"MACD: {empresa} "
)

fig_MACD.update_xaxes(title_text="xaxis title")

fig_MACD.update_yaxes(title_text="<b>primary</b> yaxis title", secondary_y=False)
fig_MACD.update_yaxes(title_text="<b>secondary</b> yaxis title", secondary_y=True)

st.plotly_chart(fig_MACD)


#5.2.7 Bollinger bands
st.markdown(
     """
    
    >> ### :green[8. Bollinger Bands]
    
     """
     )

fig_bollinger_band = go.Figure()

fig_bollinger_band.add_trace(go.Scatter(x=data['Date'], y=data['TypicalPrice'],
                        fill=None,
                        mode='lines',
                        line_color='#EA6E43',
                        name = "Close"
                         ))
fig_bollinger_band.add_trace(go.Scatter(x=data['Date'], y=data['BOLU'],
                         fill = 'tonexty',
                         #fill="toself",
                         mode = "lines",
                         line_color= "#4380EA",
                         name= "BOLU"))
fig_bollinger_band.add_trace(go.Scatter(x=data['Date'], y=data['BOLD'],
                         fill = 'tonexty',
                         #fill='tozeroy',
                         mode = "lines",
                         line_color= "#4380EA",
                         name= "BOLD"))
fig_bollinger_band.update_xaxes(title_text="Date")
fig_bollinger_band.update_yaxes(title_text="Price",
                         tickprefix="$")
fig_bollinger_band.update_layout(title_text=f"{empresa} - Bollinger Bands",
                         title_font=dict(color="#08123E", 
                                         size=18))

st.plotly_chart(fig_bollinger_band, use_container_width=True)


#6 Gráfico Tendencia precio de cierre
st.markdown(
     """
     
    > ### :blue[Trending - Close Price]
    
     """
     )

fig, ax = plt.subplots() 
data['Pred'].plot(ax=ax, linestyle = "-", lw=2)
data['Close'].plot(ax=ax, lw=2)
ax.set_title(f'Predict prices: {ticker}')
st.pyplot(fig)

st.write(r2_score(data['Close'], data['Pred']))
st.write(lin_model.coef_ * len(data) + 5 + lin_model.intercept_)