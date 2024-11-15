import streamlit as st

st.title("Calculadora de Financiamiento")

# Entradas del usuario
precio_oferta = st.number_input("Precio de oferta ($)", min_value=0.0, format="%.2f")
enganche = st.number_input("Enganche ($)", min_value=0.0, format="%.2f")
promocion = st.number_input("Promoción del cliente (%)", min_value=0.0, max_value=100.0, format="%.2f")
promocion_extra = st.number_input("Promoción extra (%)", min_value=0.0, max_value=100.0, format="%.2f")

# Validación del enganche
if enganche > precio_oferta:
    st.error("El enganche no puede ser mayor que el precio de oferta.")
else:
    # Aplicar la promoción al precio de oferta
    descuento_promocion = precio_oferta * (promocion / 100)
    precio_con_descuento = precio_oferta - descuento_promocion

    # Determinar el plazo y el interés según el precio con descuento
    if 201 <= precio_con_descuento <= 2500:
        plazo_meses = 3
        interes = 25
    elif 2501 <= precio_con_descuento <= 5000:
        plazo_meses = 6
        interes = 60
    elif 5001 <= precio_con_descuento <= 8000:
        plazo_meses = 9
        interes = 60
    elif 8001 <= precio_con_descuento <= 11000:
        plazo_meses = 12
        interes = 65
    elif 11001 <= precio_con_descuento <= 14000:
        plazo_meses = 18
        interes = 75
    elif precio_con_descuento > 14000:
        plazo_meses = 24
        interes = 85
    else:
        st.error("El precio de oferta debe ser al menos $201 para aplicar financiamiento.")
        st.stop()

    # Calcular la cantidad financiada
    monto_base_financiado = precio_con_descuento - enganche
    interes_calculado = monto_base_financiado * (interes / 100)
    cantidad_financiada = monto_base_financiado + interes_calculado

    # Calcular la cantidad de descuento promocional
    base_promocion = cantidad_financiada - precio_oferta
    cantidad_descuento_promocional = base_promocion * (promocion_extra / 100)

    # Calcular pagos
    pago_mensual = cantidad_financiada / plazo_meses
    pago_semanal = cantidad_financiada / (plazo_meses * 4)

    # Mostrar los resultados
    st.write(f"**Tasa de interés aplicada:** {interes}%")
    st.write(f"**Plazo:** {plazo_meses} meses ({plazo_meses * 4} semanas)")
    st.write(f"**Monto base financiado:** ${monto_base_financiado:.2f}")
    st.write(f"**Interés calculado:** ${interes_calculado:.2f}")
    st.write(f"**Cantidad financiada total:** ${cantidad_financiada:.2f}")
    st.write(f"**Cantidad de descuento promocional:** ${cantidad_descuento_promocional:.2f}")
    st.write(f"**Pago mensual:** ${pago_mensual:.2f}")
    st.write(f"**Pago semanal:** ${pago_semanal:.2f}")
