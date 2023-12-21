import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
)

st.markdown(
    """
    <style>
    .css-1jc7ptx, .e1ewe7hr3, .viewerBadge_container__1QSob,
    .styles_viewerBadge__1yB5_, .viewerBadge_link__1S137,
    .viewerBadge_text__1JaDK {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


#st.write("# Welcome to Financials analysis for the main stocks in the S&P 500 v1.0 ! 🚀")

st.markdown("# :green[Welcome to Financials analysis for the main stocks in the S&P 500 🚀]")

st.markdown("""
            #### :green[Developed by:]🐢 [Edgar Trejo](https://www.linkedin.com/in/edgar-trejo-03077748) 🐢
            """
)

st.markdown("##### :green[v2.0. Technical & Fundamental Anaylsis]")

st.markdown(
    """
    **This demo shows the use of *Streamlit* 
    for data analysis and data visualization with Python code, 
    powered with libraries such as yfinance, Plotly, and others.**
    """
)
"----------"

st.markdown(
    """
    >> ### :red[Important Information] ✅
    """
    )

"----------"

st.markdown(
    """
    The information provided below has been prepared for academic and  informational purposes. 
    
    Any opinions, analyses, prices, or other content do not constitute investment advice and do not represent an investment recommendation. 
    
    Past performance is not indicative of future results, and anyone acting on this information does so at their own risk. 
    
    For a specific evaluation, it is essential to consider aspects such as:
    
    - Investor profile
    - Investment goals
    - Risk management approach: appetite, tolerance, unacceptable levels
    - Liquidity needs
    - Investment timeframe
    - And other relevant factors. 
    
    Undertaking any form of investment is not recommended without specialized guidance and without having conducted a thorough analysis and assessment, including the investment instrument and market conditions (macro and microeconomic analysis), among other relvant indicators.


 
    >> ### :red[Key Features]

    

    | Technical Analysis | Fudamental Analysis |
    |-----------|-----------|
    |MACD| Profitability Ratios|
    |SMA| Profit Margin|
    |EMA| Turnover-control ratios|
    |Bollinger Bands| Leverage and liquity ratios|

    ### And more
    
     """
     )  


#st.markdown("[![Microsoft](https://www.microsoft.com/investor/reports/ar22/img/site-logo.svg)](https://www.microsoft.com/investor/reports/ar22/index.html#home)")

#st.markdown(
#    "[![Alphabet](https://www.abc.xyz/assets/4d/68/600ef2c64455b2f1aafdd81b1732/ir-logo-2x.png=n-w400-h94)](https://abc.xyz/investor/)"
#)