import streamlit as st

st.set_page_config(page_title="Referencias", page_icon="📈")

st.markdown("# Conceptos")

st.markdown(
     """   
    **:green[2. RoR - Rate Of Return]**

     """
     )

st.latex(r'''

        RoR = (\frac{V_f -V_{init}}{V_{init}})-1         
         
         ''')

st.markdown(
     """   

- $V_{init}$: Initial value
- $V_f$: Final value
- $RoR$: Rate of Return

[Source: Investopedia](https://www.investopedia.com/terms/r/rateofreturn.asp)

     """
     )

st.markdown(
     """   
    **:green[3. Compound Annual Growth Rate]**

     """
     )

st.latex(r'''

        CAGR = (\frac{V_f}{V_{init}})^\frac{1}{n}-1         
         
         ''')

st.markdown(
     """   

- $V_{init}$: Initial value
- $V_f$: Final value
- $n$: number of period

[Source: Investopedia](https://www.investopedia.com/terms/c/cagr.asp)

     """
     )


st.write(
    """This demo illustrates a combination of plotting and animation with
Streamlit. We're generating a bunch of random numbers in a loop for around
5 seconds. Enjoy!"""

)

st.markdown(
     """   
    **:green[4. Desviación Estándar]**

     """
     )

st.write("""
          
$sigma_{p} = \sigma_{daily}\times \sqrt{p}$

- $\sigma_{annually} = \sigma_{daily}\times \sqrt{252}$


"""
         )

st.text(
     """   

$ln(\frac{P_t}{P_{t-1}})$


# :green[Additional Information:]

1. [Simple Moving Average (SMA): Investopedia](https://www.investopedia.com/terms/s/sma.asp)

     """
     )
