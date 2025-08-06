from flask import Flask, render_template, request
from pysentimiento import create_analyzer
from deep_translator import GoogleTranslator
import os

app = Flask(__name__)
analyzer = create_analyzer(task="sentiment", lang="es")
historial = []

@app.route("/", methods=["GET", "POST"])
def index():
    resultado = None
    polaridad = None
    texto = None
    traduccion = None

    if request.method == "POST":
        texto = request.form["texto"]
        try:
            traduccion = GoogleTranslator(source='es', target='en').translate(texto)
            result = analyzer.predict(texto)
            polaridad = round(result.probas[result.output], 3)

            if result.output == "POS":
                resultado = "😄 Es feliz"
            elif result.output == "NEG":
                resultado = "😢 Es triste"
            else:
                resultado = "😐 Neutral"

            historial.append({
                "texto": texto,
                "traduccion": traduccion,
                "resultado": resultado,
                "polaridad": polaridad
            })

        except Exception as e:
            resultado = f"⚠️ Error: {e}"

    return render_template("index.html", resultado=resultado, polaridad=polaridad,
                           texto=texto, texto_traducido=traduccion, historial=historial)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
