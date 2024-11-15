import streamlit as st
import pandas as pd

st.title("Calculadora de Financiamiento")

# Entradas del usuario
precio_oferta = st.number_input("Precio de oferta ($)", min_value=0.0, format="%.2f")
enganche = st.number_input("Enganche ($)", min_value=0.0, format="%.2f")
promociones_cliente = st.number_input("Promociones del cliente (%)", min_value=0.0, max_value=100.0, format="%.2f")
plazo = st.number_input("Plazo (meses)", min_value=1, step=1)
redondeo = st.checkbox("Redondear abono mensual hacia arriba")

# Validación del enganche
if enganche > precio_oferta:
    st.error("El enganche no puede ser mayor que el precio de oferta.")
else:
    # Aplicar el descuento de promociones al precio de oferta
    descuento_promocion = precio_oferta * (promociones_cliente / 100)
    precio_con_descuento = precio_oferta - descuento_promocion

    # Determinación de la tasa de interés según el precio con descuento
    if precio_con_descuento >= 201 and precio_con_descuento <= 2500:
        interes = 25
    elif precio_con_descuento > 2500 and precio_con_descuento <= 5000:
        interes = 60
    elif precio_con_descuento > 5000 and precio_con_descuento <= 8000:
        interes = 60
    elif precio_con_descuento > 8000 and precio_con_descuento <= 11000:
        interes = 65
    elif precio_con_descuento > 11000 and precio_con_descuento <= 14000:
        interes = 75
    else:
        interes = 85

    st.write(f"Tasa de interés aplicada: {interes}%")

    # Cálculos
    precio_menos_enganche = precio_con_descuento - enganche
    interes_financiero = precio_menos_enganche * (interes / 100)
    total_precio_credito = precio_menos_enganche + interes_financiero
    abono_mensual = total_precio_credito / plazo

    # Aplicar redondeo si está seleccionado
    if redondeo:
        abono_mensual = round(abono_mensual)

    # Resultados
    st.write(f"**Total a crédito:** ${total_precio_credito:.2f}")
    st.write(f"**Abono mensual:** ${round(abono_mensual, 2)}")

    # Tabla de resultados
    resultados = {
        "Precio Oferta": [precio_oferta],
        "Descuento Promoción": [descuento_promocion],
        "Precio con Descuento": [precio_con_descuento],
        "Enganche": [enganche],
        "Interés Financiero": [interes_financiero],
        "Total a Crédito": [total_precio_credito],
        "Abono Mensual": [abono_mensual]
    }
    df_resultados = pd.DataFrame(resultados)
    st.write("### Desglose del Financiamiento")
    st.table(df_resultados)
