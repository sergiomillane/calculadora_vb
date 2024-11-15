from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/calculadora', methods=['GET'])
def calculadora():
    try:
        # Obtén los parámetros desde la URL
        precio_oferta = float(request.args.get('precio_oferta'))
        enganche = float(request.args.get('enganche'))
        interes = float(request.args.get('interes'))
        plazo = int(request.args.get('plazo'))

        # Realiza los cálculos
        precio_menos_enganche = precio_oferta - enganche
        interes_financiero = precio_menos_enganche * (interes / 100)
        total_precio_credito = precio_menos_enganche + interes_financiero
        abono_mensual = total_precio_credito / plazo

        # Devuelve los resultados en formato JSON
        return jsonify({
            "total_credito": round(total_precio_credito, 2),
            "abono_mensual": round(abono_mensual, 2)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
