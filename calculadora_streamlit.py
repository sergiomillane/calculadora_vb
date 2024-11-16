import streamlit as st

# Configurar estilos globales para fondo y texto
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background-color: #FFFACD; /* Fondo amarillo claro */
    }

    .result-box {
        background-color: #ffffff;
        padding: 15px;
        margin-bottom: 10px;
        border-radius: 10px;
        border: 2px solid #FFD700; /* Borde dorado */
        box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
    }
    .result-box h2 {
        font-size: 22px;
        color: #000000; /* Texto negro */
        font-weight: bold;
    }
    .result-box p {
        font-size: 18px;
        color: #000000; /* Texto negro */
    }

    .title {
        color: #000000; /* Texto negro */
        font-size: 32px;
        font-weight: bold;
        margin-bottom: 20px;
    }

    label {
        color: #000000 !important; /* Asegura que las etiquetas sean negras */
        font-size: 16px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Título principal
st.markdown('<div class="title">Calculadora de Financiamiento 💵</div>', unsafe_allow_html=True)

# Inputs del usuario
col1, col2, col3, col4 = st.columns(4)

with col1:
    precio_oferta = st.number_input("Precio de oferta ($)", min_value=0.0, format="%.2f")

with col2:
    enganche = st.number_input("Enganche ($)", min_value=0.0, format="%.2f")

with col3:
    promocion_extra = st.number_input("Promoción extra (%)", min_value=0.0, max_value=100.0, format="%.2f")

with col4:
    mes_liquidacion = st.number_input("Mes de liquidación (0 para pagar todo el plazo)", min_value=0, step=1)

# Validar enganche
if enganche > precio_oferta:
    st.error("El enganche no puede ser mayor que el precio de oferta.")
else:
    # Determinar el plazo y el interés según la tabla proporcionada
    def determinar_plazo_interes(precio):
        if 201 <= precio <= 2500:
            return 3, 1.25
        elif 2501 <= precio <= 5000:
            return 6, 1.60
        elif 5001 <= precio <= 8000:
            return 9, 1.60
        elif 8001 <= precio <= 11000:
            return 12, 1.65
        elif 11001 <= precio <= 14000:
            return 18, 1.75
        elif precio > 14000:
            return 24, 1.85
        else:
            return 0, 0  # No válido

    # Obtener plazo y porcentaje de interés
    plazo_meses, tasa_interes_factor = determinar_plazo_interes(precio_oferta)
    plazo_semanas = plazo_meses * 4  # Cada mes equivale a 4 semanas
    tasa_interes_porcentaje = (tasa_interes_factor - 1) * 100  # Convertir factor a porcentaje

    if plazo_meses == 0:
        st.error("El precio de oferta no se encuentra en un rango válido.")
    else:
        # Calcular monto base financiado
        monto_base_financiado = precio_oferta - enganche

        # Calcular interés total
        interes_calculado = monto_base_financiado * (tasa_interes_factor - 1)

        # Calcular cantidad financiada total
        cantidad_financiada_total = monto_base_financiado + interes_calculado

        # Aplicar promoción extra al monto final
        descuento_promocional = precio_oferta * (promocion_extra / 100)
        final_a_pagar = cantidad_financiada_total - descuento_promocional

        # Calcular pagos
        pago_mensual = final_a_pagar / plazo_meses
        pago_semanal = final_a_pagar / plazo_semanas

        # Mostrar resultados
        st.markdown(
            f"""
            <div class="result-box">
            <h2>Resultados:</h2>
            <p><strong>Tasa de interés:</strong> {tasa_interes_porcentaje:.2f}%</p>
            <p><strong>Plazo:</strong> {plazo_meses} meses ({plazo_semanas} semanas)</p>
            <p><strong>Enganche:</strong> ${enganche:.2f}</p>
            <p><strong>Monto base financiado:</strong> ${monto_base_financiado:.2f}</p>
            <p><strong>Interés calculado:</strong> ${interes_calculado:.2f}</p>
            <p><strong>Cantidad financiada total:</strong> ${cantidad_financiada_total:.2f}</p>
            <p><strong>Descuento promocional:</strong> ${descuento_promocional:.2f}</p>
            <p><strong>Final a pagar (con promoción):</strong> ${final_a_pagar:.2f}</p>
            <p><strong>Pago mensual:</strong> ${pago_mensual:.2f}</p>
            <p><strong>Pago semanal:</strong> ${pago_semanal:.2f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
