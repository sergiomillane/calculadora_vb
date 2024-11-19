import streamlit as st

# Título principal
st.title("Calculadora de Financiamiento 💵")

# Inicializar la lista de artículos en el estado de la sesión
if "articulos" not in st.session_state:
    st.session_state["articulos"] = []

# Función para restaurar valores
def restaurar_valores():
    st.session_state["articulos"] = []
    st.session_state["promocion_extra"] = 0.0

# Botón para restaurar valores
if st.button("Restaurar"):
    restaurar_valores()

# Botón para añadir artículo
if st.button("Añadir artículo"):
    st.session_state["articulos"].append(
        {"precio_oferta": 0.0, "enganche": 0.0}
    )

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

# Input de promoción global
st.subheader("Promoción Global")
promocion_extra = st.number_input(
    "Promoción extra (%) para toda la factura",
    min_value=0.0,
    max_value=100.0,
    format="%.2f",
    key="promocion_extra",
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
            descuento_promocional_total = precio_total_oferta * (promocion_extra / 100)
            final_a_pagar_total = cantidad_financiada_total - descuento_promocional_total
            pago_mensual_total = final_a_pagar_total / plazo_meses
            pago_semanal_total = final_a_pagar_total / plazo_semanas

            # Calcular TOTAL FACTURA
            total_factura = final_a_pagar_total + enganche_total

            # Mostrar resultados totales
            st.subheader("Resultados Totales de la Factura")
            st.write(f"Tasa de interés: {tasa_interes_porcentaje:.2f}%")
            st.write(f"Plazo: {plazo_meses} meses ({plazo_semanas} semanas)")
            st.write(f"Enganche Total: ${enganche_total:.2f}")
            st.write(f"Interés Total: ${interes_calculado_total:.2f}")
            st.write(f"Cantidad Total Financiada: ${cantidad_financiada_total:.2f}")
            st.write(f"Descuento Promocional Total: ${descuento_promocional_total:.2f}")
            st.write(f"A Pagar (con Promoción): ${final_a_pagar_total:.2f}")
            st.write(f"Pago Mensual Total: ${pago_mensual_total:.2f}")
            st.write(f"Pago Semanal Total: ${pago_semanal_total:.2f}")
            st.markdown(f"### TOTAL FACTURA: **${total_factura:.2f}**")

