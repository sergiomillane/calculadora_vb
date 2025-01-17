import streamlit as st

# Título principal
st.title("Calculadora de Financiamiento 💵")

# Tablas de acumulado por plazo
tablas_acumulado = {
    3: [0, 50, 100],
    6: [0, 51, 70, 85, 95, 100],
    9: [0, 35, 50, 63, 75, 85, 92, 97, 100],
    12: [0, 30, 42, 52, 62, 72, 80, 87, 93, 97, 99, 100],
    18: [0, 11, 21, 30, 39, 48, 55, 62, 68, 74, 79, 84, 88, 92, 97, 99, 100],
    24: [0, 8, 16, 23, 30, 37, 43, 48, 53, 58, 63, 68, 72, 76, 80, 84, 87, 90, 93, 95, 97, 98, 99, 100],
}

# Inicializar la lista de artículos en el estado de la sesión
if "articulos" not in st.session_state:
    st.session_state["articulos"] = []

# Función para restaurar valores
def restaurar_valores():
    st.session_state["articulos"] = []
    st.session_state["descuento"] = 0.0

# Botón para restaurar valores
if st.button("Restaurar"):
    restaurar_valores()

# Botón para añadir artículo
if st.button("Añadir artículo"):
    st.session_state["articulos"].append({"precio_oferta": 0.0, "enganche": 0.0})

# Mostrar inputs para cada artículo
precio_total_oferta = 0
enganche_total = 0
for i, articulo in enumerate(st.session_state["articulos"]):
    st.subheader(f"Artículo {i + 1}")
    col1, col2 = st.columns(2)
    with col1:
        articulo["precio_oferta"] = st.number_input(
            f"Precio de oferta ($) - Artículo {i + 1}",
            min_value=0.0,
            format="%.2f",
            key=f"precio_oferta_{i}",
        )
    with col2:
        articulo["enganche"] = st.number_input(
            f"Enganche ($) - Artículo {i + 1}",
            min_value=0.0,
            format="%.2f",
            key=f"enganche_{i}",
        )

    # Acumular los totales
    precio_total_oferta += articulo["precio_oferta"]
    enganche_total += articulo["enganche"]

# Input de descuento global
st.subheader("Descuento %")
descuento = st.number_input(
    "Descuento (%) para toda la factura",
    min_value=0.0,
    max_value=100.0,
    format="%.2f",
    key="descuento",
)

# Input para el mes de liquidación
st.subheader("Mes de Liquidación")
mes_liquidacion = st.number_input(
    "Introduce el mes en el que deseas liquidar (1 a plazo máximo):",
    min_value=0,
    max_value=24,
    format="%d",
    key="mes_liquidacion",
)

# Botón para calcular factura total
if st.button("Calcular factura"):
    if precio_total_oferta == 0:
        st.error("Por favor, ingresa al menos un artículo con un precio de oferta válido.")
    elif enganche_total > precio_total_oferta:
        st.error("El enganche total no puede ser mayor que el precio total de oferta.")
    else:
        # Determinar plazo e interés global
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

        plazo_meses, tasa_interes_factor = determinar_plazo_interes(precio_total_oferta)
        plazo_semanas = plazo_meses * 4
        tasa_interes_porcentaje = (tasa_interes_factor - 1) * 100

        if plazo_meses == 0:
            st.error("El precio total de oferta no está en un rango válido.")
        else:
            # Cálculos globales
            monto_base_financiado_total = precio_total_oferta - enganche_total
            interes_calculado_total = monto_base_financiado_total * (tasa_interes_factor - 1)
            cantidad_financiada_total = monto_base_financiado_total + interes_calculado_total
            descuento_total = precio_total_oferta * (descuento / 100)
            final_a_pagar_total = cantidad_financiada_total - descuento_total
            pago_mensual_total = final_a_pagar_total / plazo_meses
            pago_semanal_total = final_a_pagar_total / plazo_semanas

            # Cálculo del "liquida con"
            if mes_liquidacion > 0 and mes_liquidacion <= plazo_meses:
                porcentaje_acumulado = tablas_acumulado[plazo_meses][mes_liquidacion - 1] / 100
                monto_pagado = pago_mensual_total * (mes_liquidacion - 1)
                liquida_con = (
                    monto_base_financiado_total + interes_calculado_total * porcentaje_acumulado - monto_pagado
                )
            else:
                liquida_con = "N/A"

            # Mostrar resultados totales en un recuadro
            st.markdown(
                f"""
                <div style="background-color: #D3D3D3; padding: 15px; border-radius: 10px; border: 1px solid #ddd; color: #000000;">
                <h2 style="color: #000000;">Resultados Totales de la Factura:</h2>
                <p><strong>Tasa de interés:</strong> {tasa_interes_porcentaje:.2f}%</p>
                <p><strong>Plazo:</strong> {plazo_meses} meses ({plazo_semanas} semanas)</p>
                <p><strong>Enganche Total:</strong> ${enganche_total:.2f}</p>
                <p><strong>Interés Total:</strong> ${interes_calculado_total:.2f}</p>
                <p><strong>Cantidad Total Financiada:</strong> ${cantidad_financiada_total:.2f}</p>
                <p><strong>Descuento Total:</strong> ${descuento_total:.2f}</p>
                <p><strong>A Pagar (con Descuento):</strong> ${final_a_pagar_total:.2f}</p>
                <p><strong>Pago Mensual Total:</strong> ${pago_mensual_total:.2f}</p>
                <p><strong>Pago Semanal Total:</strong> ${pago_semanal_total:.2f}</p>
                <p style="color: red; font-weight: bold; font-size: 18px;"><strong>TOTAL FACTURA:</strong> ${final_a_pagar_total + enganche_total:.2f}</p>
                <p style="color: green; font-weight: bold;"><strong>Liquida con (Mes {mes_liquidacion}):</strong> ${liquida_con:.2f}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
