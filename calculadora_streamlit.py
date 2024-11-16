import streamlit as st

# Configuración del tema claro con estilos adicionales
st.markdown(
    """
    <style>
    body {
        background-color: #FFF8DC; /* Amarillo claro */
        color: #333333; /* Texto oscuro */
    }
    .stApp {
        background-color: #FFF8DC; /* Fondo amarillo claro */
    }
    label {
        color: #333333 !important; /* Texto oscuro para los nombres de los inputs */
        font-weight: bold; /* Negrita para resaltar */
        font-size: 16px; /* Tamaño de letra más grande */
    }
    .result-box {
        border: 1px solid #333333; /* Borde oscuro */
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
        background-color: #FFFACD; /* Amarillo más claro */
        color: #333333; /* Texto oscuro */
        font-weight: bold;
        font-size: 18px;
    }
    input {
        color: #333333 !important; /* Texto oscuro dentro de los campos */
        background-color: #FFFFFF !important; /* Fondo blanco */
        border: 1px solid #CCCCCC; /* Borde gris claro */
        border-radius: 5px;
        padding: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Calculadora de Financiamiento 💵")

# Colocar los inputs en una fila
col1, col2, col3, col4 = st.columns(4)

with col1:
    precio_oferta = st.number_input("Precio de oferta ($)", min_value=0.0, format="%.2f")

with col2:
    enganche = st.number_input("Enganche ($)", min_value=0.0, format="%.2f")

with col3:
    promocion_extra = st.number_input("Promoción extra (%)", min_value=0.0, max_value=100.0, format="%.2f")

with col4:
    mes_liquidacion = st.number_input("Mes de liquidación (0 para pagar todo el plazo)", min_value=0, step=1)

# Tablas de acumulado por plazo
tablas_acumulado = {
    3: [0, 50, 100],
    6: [0, 51, 70, 85, 95, 100],
    9: [0, 35, 50, 63, 75, 85, 92, 97, 100],
    12: [0, 30, 42, 52, 62, 72, 80, 87, 93, 97, 99, 100],
    18: [0, 11, 21, 30, 39, 48, 55, 62, 68, 74, 79, 84, 88, 92, 97, 99, 100],
    24: [0, 8, 16, 23, 30, 37, 43, 48, 53, 58, 63, 68, 72, 76, 80, 84, 87, 90, 93, 95, 97, 98, 99, 100],
}

# Validación del enganche
if enganche > precio_oferta:
    st.error("El enganche no puede ser mayor que el precio de oferta.")
else:
    # Determinar el plazo y el interés según el precio de oferta
    if 201 <= precio_oferta <= 2500:
        plazo_meses = 3
        interes = 25
    elif 2501 <= precio_oferta <= 5000:
        plazo_meses = 6
        interes = 60
    elif 5001 <= precio_oferta <= 8000:
        plazo_meses = 9
        interes = 60
    elif 8001 <= precio_oferta <= 11000:
        plazo_meses = 12
        interes = 65
    elif 11001 <= precio_oferta <= 14000:
        plazo_meses = 18
        interes = 75
    elif precio_oferta > 14000:
        plazo_meses = 24
        interes = 85
    else:
        st.error("El precio de oferta debe ser al menos $201 para aplicar financiamiento.")
        st.stop()

    # Calcular la cantidad financiada
    monto_base_financiado = precio_oferta - enganche
    interes_calculado = monto_base_financiado * (interes / 100)
    cantidad_financiada = monto_base_financiado + interes_calculado

    # Calcular el descuento por promoción
    descuento_por_promocion = precio_oferta * (promocion_extra / 100)

    # Calcular el total a pagar
    total_a_pagar = cantidad_financiada - descuento_por_promocion

    # Calcular pagos
    pago_mensual = total_a_pagar / plazo_meses
    pago_semanal = total_a_pagar / (plazo_meses * 4)

    # Determinar el monto para liquidar
    if mes_liquidacion == 0 or mes_liquidacion == "":
        # Si el mes de liquidación es 0, el cliente pagará todo el plazo
        liquida_con = total_a_pagar
    elif mes_liquidacion > plazo_meses:
        st.error("El mes de liquidación no puede ser mayor al plazo total.")
    else:
        # Obtener el porcentaje acumulado para el mes de liquidación
        porcentaje_acumulado = tablas_acumulado[plazo_meses][mes_liquidacion - 1] / 100

        # Calcular el monto pagado hasta el mes anterior
        monto_pagado = pago_mensual * (mes_liquidacion - 1)

        # Calcular el monto para liquidar considerando el interés acumulado hasta ese mes
        liquida_con = (
            monto_base_financiado + (interes_calculado * porcentaje_acumulado) - monto_pagado
        )

    # Mostrar los resultados
    st.markdown(
        f"""
        <div class="result-box">Tasa de interés aplicada: <span style="color:#333333;">{interes}%</span></div>
        <div class="result-box">Plazo: <span style="color:#333333;">{plazo_meses} meses ({plazo_meses * 4} semanas)</span></div>
        <div class="result-box">Monto base financiado: <span style="color:#333333;">${monto_base_financiado:.2f}</span></div>
        <div class="result-box">Interés calculado: <span style="color:#333333;">${interes_calculado:.2f}</span></div>
        <div class="result-box">Cantidad financiada total: <span style="color:#333333;">${cantidad_financiada:.2f}</span></div>
        <div class="result-box">Descuento por promoción: <span style="color:#333333;">-${descuento_por_promocion:.2f}</span></div>
        <div class="result-box">Total a pagar: <span style="color:#333333;">${total_a_pagar:.2f}</span></div>
        <div class="result-box">Pago mensual: <span style="color:#333333;">${pago_mensual:.2f}</span></div>
        <div class="result-box">Pago semanal: <span style="color:#333333;">${pago_semanal:.2f}</span></div>
        <div class="result-box">Monto para liquidar en el mes {mes_liquidacion if mes_liquidacion != 0 else "final"}: <span style="color:#333333;">${liquida_con:.2f}</span></div>
        """,
        unsafe_allow_html=True,
    )
