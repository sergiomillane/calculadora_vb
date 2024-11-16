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

# Tablas de acumulado para cada plazo
tablas_acumulado = {
    3: [0, 50, 100],
    6: [0, 51, 70, 85, 95, 100],
    9: [0, 35, 50, 63, 75, 85, 92, 97, 100],
    12: [0, 30, 42, 52, 62, 72, 80, 87, 93, 97, 99, 100],
    18: [0, 11, 21, 30, 39, 48, 55, 62, 68, 74, 79, 84, 88, 92, 97, 99, 100],
    24: [0, 8, 16, 23, 30, 37, 43, 48, 53, 58, 63, 68, 72, 76, 80, 84, 87, 90, 93, 95, 97, 98, 99, 100],
}

# Validar enganche
if enganche > precio_oferta:
    st.error("El enganche no puede ser mayor que el precio de oferta.")
else:
    # Calcular monto base financiado
    monto_base_financiado = precio_oferta - enganche

    # Determinar la tasa de interés según el precio de oferta
    def determinar_tasa(precio):
        if 201 <= precio <= 2500:
            return 25
        elif 2501 <= precio <= 5000:
            return 60
        elif 5001 <= precio <= 8000:
            return 60
        elif 8001 <= precio <= 11000:
            return 65
        elif 11001 <= precio <= 14000:
            return 75
        elif precio > 14000:
            return 85
        else:
            return 0  # No válido

    # Calcular la tasa de interés
    tasa_interes = determinar_tasa(precio_oferta)

    # Calcular interés total y cantidad financiada total
    interes_calculado = monto_base_financiado * (tasa_interes / 100)
    cantidad_financiada_total = monto_base_financiado + interes_calculado

    # Aplicar promoción extra al monto final
    descuento_promocional = precio_oferta * (promocion_extra / 100)
    final_a_pagar = cantidad_financiada_total - descuento_promocional

    # Determinar plazo según la cantidad financiada total
    def determinar_plazo(cantidad_financiada_total):
        if 201 <= cantidad_financiada_total <= 2500:
            return 3
        elif 2501 <= cantidad_financiada_total <= 5000:
            return 6
        elif 5001 <= cantidad_financiada_total <= 8000:
            return 9
        elif 8001 <= cantidad_financiada_total <= 11000:
            return 12
        elif 11001 <= cantidad_financiada_total <= 14000:
            return 18
        elif cantidad_financiada_total > 14000:
            return 24
        else:
            return 0  # No válido

    # Validación del plazo antes de usarlo
    plazo_meses = determinar_plazo(cantidad_financiada_total)
    plazo_semanas = plazo_meses * 4  # Cada mes equivale a 4 semanas

    if plazo_meses == 0:
        st.error("No se encontró un plazo válido para la cantidad financiada total. Verifica los valores ingresados.")
    else:
        # Calcular pagos
        pago_mensual = final_a_pagar / plazo_meses
        pago_semanal = final_a_pagar / plazo_semanas

        # Calcular "Liquide con"
        if mes_liquidacion == 0 or mes_liquidacion == "":
            liquida_con = final_a_pagar  # Pagar todo al final del plazo
        elif mes_liquidacion > plazo_meses:
            st.error("El mes de liquidación no puede ser mayor al plazo total.")
        else:
            # Obtener porcentaje acumulado
            porcentaje_acumulado = tablas_acumulado[plazo_meses][mes_liquidacion - 1] / 100

            # Calcular interés ajustado para el mes de liquidación
            interes_ajustado = interes_calculado * porcentaje_acumulado

            # Calcular pagos acumulados hasta el mes anterior
            pagos_acumulados = pago_mensual * (mes_liquidacion - 1)

            # Calcular "Liquide con" considerando la promoción extra
            liquida_con = (monto_base_financiado + interes_ajustado) - pagos_acumulados - descuento_promocional

        # Mostrar resultados
        st.markdown(
            f"""
            <div class="result-box">
            <h2>Resultados:</h2>
            <p><strong>Tasa de interés:</strong> {tasa_interes}%</p>
            <p><strong>Plazo:</strong> {plazo_meses} meses ({plazo_semanas} semanas)</p>
            <p><strong>Enganche:</strong> ${enganche:.2f}</p>
            <p><strong>Monto base financiado:</strong> ${monto_base_financiado:.2f}</p>
            <p><strong>Interés calculado:</strong> ${interes_calculado:.2f}</p>
            <p><strong>Cantidad financiada total:</strong> ${cantidad_financiada_total:.2f}</p>
            <p><strong>Descuento promocional:</strong> ${descuento_promocional:.2f}</p>
            <p><strong>Final a pagar (con promoción):</strong> ${final_a_pagar:.2f}</p>
            <p><strong>Pago mensual:</strong> ${pago_mensual:.2f}</p>
            <p><strong>Pago semanal:</strong> ${pago_semanal:.2f}</p>
            <p><strong>Liquide con (mes {mes_liquidacion if mes_liquidacion != 0 else "final"}):</strong> ${liquida_con:.2f}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
