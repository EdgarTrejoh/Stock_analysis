import streamlit as st

st.set_page_config(page_title="References", page_icon="🌎")

st.markdown("# :green[3. References 📚 ]")

"----------"

st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""

)

"----------"

columna_1, columna_2 = st.columns(2)

with columna_1:
    #Rate of Return
    st.markdown(
     """   
    **:green[1. RoR - Rate Of Return]**

     """)
    
    st.latex(
       r'''

        RoR = (\frac{V_f -V_{init}}{V_{init}})-1         
         
         '''
    )
    st.markdown(
          """
          - $V_{init}$: Initial value
          - $V_f$: Final value
          - $n$: number of period

          
          [Source: Investopedia](https://www.investopedia.com/terms/r/rateofreturn.asp)
          
          """
    )

    "----------"
    
    #CAGR
    st.markdown(
          """
          **:green[3. Compound Annual Growth Rate]**
          """
     )
    
    st.latex(
        r'''

        CAGR = (\frac{V_f}{V_{init}})^\frac{1}{n}-1         
         
         '''
     )
    st.markdown(
        """   
          - $V_{init}$: Initial value
          - $V_f$: Final value
          - $n$: number of period

          [Source: Investopedia](https://www.investopedia.com/terms/c/cagr.asp)
     """
     )
    
    "----------"
     
    #Bollinger Bands
    st.markdown(
        """
        **:green[5. Bollinger Bands]**
        """
     )
    st.markdown(
        """
        
        
        [Source: Investopedia](https://www.investopedia.com/terms/b/bollingerbands.asp)
        
        """
     )
    

    "----------"

with columna_2:
    #Log Return
    st.markdown(
     """   
     **:green[2. Logarithmic Return]**
     """
     )
    
    st.latex(r"""
             R_log = ln(\frac{V_t}{V_{t-1}}) 
             """    
    )

    st.markdown(
          """
          - $V_t$: The price of an asset at time: *t*
          - $V_{t-1}$: The price of an asset at time: *t-1*
          - $ln$: The natural logarithm log is the inverse of the exponential function. 
          
          [Source: Wikipedia](https://en.wikipedia.org/wiki/Rate_of_return)
          [Numpy](https://numpy.org/doc/stable/reference/generated/numpy.log.html)

          """
    )

    "----------"

     #Desviación Estándar
    st.markdown(
        """
        **:green[4. Standard Deviation]**
        """
     )
    st.write(
        """
        $sigma_{p} = \sigma_{daily}\times \sqrt{p}$
        - $\sigma_{annually} = \sigma_{daily}\times \sqrt{252}$
        """
     )


st.title(":green[Additional Information:]")

st.markdown(
    """
    1. [Simple Moving Average (SMA): Investopedia](https://www.investopedia.com/terms/s/sma.asp)
    2. [Gregory Gundersen](https://gregorygundersen.com/blog/2022/02/06/log-returns/")
    3. [yfinance](https://pypi.org/project/yfinance/)
    """
)
