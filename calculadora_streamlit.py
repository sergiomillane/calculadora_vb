import streamlit as st

# Configuración del tema oscuro con estilos adicionales
st.markdown(
    """
    <style>
    body {
        background-color: #1E3A5F; /* Azul marino oscuro */
        color: white; /* Texto blanco */
    }
    .stApp {
        background-color: #1E3A5F; /* Fondo azul marino */
    }
    label {
        color: white; /* Color blanco para los nombres de los inputs */
        font-weight: bold; /* Negrita para resaltar */
    }
    .result-box {
        border: 1px solid #4CAF50; /* Verde claro */
        border-radius: 5px;
        padding: 10px;
        margin: 10px 0;
        background-color: #2A5470; /* Azul intermedio */
        color: white; /* Texto blanco */
        font-weight: bold;
        font-size: 18px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("Calculadora de Financiamiento 💵")

# Entradas del usuario
precio_oferta = st.number_input("Precio de oferta ($)", min_value=0.0, format="%.2f")
enganche = st.number_input("Enganche ($)", min_value=0.0, format="%.2f")
promocion_extra = st.number_input("Promoción extra (%)", min_value=0.0, max_value=100.0, format="%.2f")

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

    # Mostrar los resultados en recuadros
    st.markdown(
        f"""
        <div class="result-box">Tasa de interés aplicada: <span style="color:#4CAF50;">{interes}%</span></div>
        <div class="result-box">Plazo: <span style="color:#4CAF50;">{plazo_meses} meses ({plazo_meses * 4} semanas)</span></div>
        <div class="result-box">Monto base financiado: <span style="color:#4CAF50;">${monto_base_financiado:.2f}</span></div>
        <div class="result-box">Interés calculado: <span style="color:#4CAF50;">${interes_calculado:.2f}</span></div>
        <div class="result-box">Cantidad financiada total: <span style="color:#4CAF50;">${cantidad_financiada:.2f}</span></div>
        <div class="result-box">Descuento por promoción: <span style="color:#4CAF50;">-${descuento_por_promocion:.2f}</span></div>
        <div class="result-box">Total a pagar: <span style="color:#4CAF50;">${total_a_pagar:.2f}</span></div>
        <div class="result-box">Pago mensual: <span style="color:#4CAF50;">${pago_mensual:.2f}</span></div>
        <div class="result-box">Pago semanal: <span style="color:#4CAF50;">${pago_semanal:.2f}</span></div>
        """,
        unsafe_allow_html=True,
    )
