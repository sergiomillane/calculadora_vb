import streamlit as st

st.title("Calculadora de Financiamiento")

precio_oferta = st.number_input("Precio de oferta", min_value=0.0)
enganche = st.number_input("Enganche", min_value=0.0)
interes = st.number_input("Interés (%)", min_value=0.0)
plazo = st.number_input("Plazo (meses)", min_value=1, step=1)

if st.button("Calcular"):
    precio_menos_enganche = precio_oferta - enganche
    interes_financiero = precio_menos_enganche * (interes / 100)
    total_precio_credito = precio_menos_enganche + interes_financiero
    abono_mensual = total_precio_credito / plazo

    st.write(f"**Total a crédito:** ${total_precio_credito:.2f}")
    st.write(f"**Abono mensual:** ${round(abono_mensual, 2)}")
