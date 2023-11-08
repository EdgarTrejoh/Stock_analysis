# Importar las librerias requeridas

import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

start = st.text_input("Fecha de inicio:", key="start")
end = st.text_input("Fecha de fin:", key="end")
ticker = st.text_input("Ticker:", key="ticker")

#st.session_state.name

st.write("Ejemplo de uso de un Dataframe y Chart")

data = yf.download(ticker, start=start, end = end, progress = True )

st.table(data)

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