from flask import Flask, request, jsonify

app = Flask(__name__)

def validar_cedula(cedula):
    """
    Valida si una cédula ecuatoriana es válida.
    """
    if len(cedula) != 10 or not cedula.isdigit():
        return False

    provincia = int(cedula[:2])
    if provincia < 1 or (provincia > 24 and provincia != 30):
        return False

    tercer_digito = int(cedula[2])
    if tercer_digito < 0 or tercer_digito > 6:
        return False

    coeficientes = [2, 1]  # Alternan entre 2 y 1
    suma = 0

    for i in range(9):  # Recorrer los primeros 9 dígitos
        digito = int(cedula[i])
        producto = digito * coeficientes[i % 2]
        if producto >= 10:
            producto -= 9
        suma += producto

    digito_verificador = int(cedula[9])
    siguiente_decena = (suma + 9) // 10 * 10
    calculado = siguiente_decena - suma

    return calculado == digito_verificador


@app.route('/validar_cedula', methods=['POST'])
def validar_cedula_endpoint():
    """
    Endpoint para validar una cédula.
    """
    try:
        data = request.get_json()
        cedula = data.get("cedula")

        if not cedula:
            return jsonify({"error": "La cédula es requerida"}), 400

        if validar_cedula(cedula):
            return jsonify({"cedula": cedula, "valida": True})
        else:
            return jsonify({"cedula": cedula, "valida": False})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
