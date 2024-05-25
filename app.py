from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField
import joblib

# Cargar el modelo de predicción con manejo de errores
try:
    modelo = joblib.load('best_model.pkl')
except Exception as e:
    print(f"Error al cargar el modelo: {e}")
    modelo = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

class SintomasForm(FlaskForm):
    febre = BooleanField('Febre')
    mialgia = BooleanField('Mialgia')
    cefaleia = BooleanField('Cefaleia')
    exantema = BooleanField('Exantema')
    vomito = BooleanField('Vómito')
    nausea = BooleanField('Náusea')
    dor_costas = BooleanField('Dor nas Costas')
    conjuntvit = BooleanField('Conjuntivite')
    artrite = BooleanField('Artrite')
    artralgia = BooleanField('Artralgia')
    petequia_n = BooleanField('Petéquias')
    laco = BooleanField('Laceração')
    dor_retro = BooleanField('Dor Retroocular')
    diabetes = BooleanField('Diabetes')
    hematolog = BooleanField('Doença Hematológica')
    hepatopat = BooleanField('Hepatopatia')
    renal = BooleanField('Doença Renal')
    hipertensa = BooleanField('Hipertensão')
    acido_pept = BooleanField('Úlcera Péptica')
    auto_imune = BooleanField('Doença Autoimune')
    submit = SubmitField('Enviar')

@app.route('/', methods=['GET', 'POST'])
def index():
    form = SintomasForm()
    if form.validate_on_submit():
        sintomas = [int(form.febre.data), int(form.mialgia.data), int(form.cefaleia.data), int(form.exantema.data),
                    int(form.vomito.data), int(form.nausea.data), int(form.dor_costas.data), int(form.conjuntvit.data),
                    int(form.artrite.data), int(form.artralgia.data), int(form.petequia_n.data), int(form.laco.data),
                    int(form.dor_retro.data), int(form.diabetes.data), int(form.hematolog.data), int(form.hepatopat.data),
                    int(form.renal.data), int(form.hipertensa.data), int(form.acido_pept.data), int(form.auto_imune.data)]
        
        # Hacer la predicción
        if modelo:
            prediccion = modelo.predict([sintomas])
            resultado = 'Dengue' if prediccion[0] == 1 else 'Chikungunya'
        else:
            resultado = 'Error en la predicción debido a problemas con el modelo'
        
        return redirect(url_for('result', resultado=resultado))
    return render_template('index.html', form=form)

@app.route('/result/<resultado>', methods=['GET'])
def result(resultado):
    return render_template('resultado.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
