import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="Fundamental Analysis",
    page_icon="📊"
    )

st.markdown("# :green[2. Fundamental Analysis 📊 ]")

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

"----------"

image = Image.open("./main/img/workin.gif")

#st.markdown(
#    "<img src=main/img/workin.gif height="333" style= "border: 5 solid orange">",
#    unsafe_allow_html=True,
#)

st.image(image, width=325, output_format="GIF")


