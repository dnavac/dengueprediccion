from flask import Flask, render_template, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import BooleanField, SubmitField
from wtforms.validators import DataRequired
import joblib

# Cargar el modelo de predicción
# with open('modelo_prediccion.pkl', 'rb') as f:
#     modelo = pickle.load(f)
modelo = joblib.load('best_model.pkl')

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

class SintomasForm(FlaskForm):
    febre = BooleanField('Febre', validators=[DataRequired()])
    mialgia = BooleanField('Mialgia', validators=[DataRequired()])
    cefaleia = BooleanField('Cefaleia', validators=[DataRequired()])
    exantema = BooleanField('Exantema', validators=[DataRequired()])
    vomito = BooleanField('Vómito', validators=[DataRequired()])
    nausea = BooleanField('Náusea', validators=[DataRequired()])
    dor_costas = BooleanField('Dor nas Costas', validators=[DataRequired()])
    conjuntvit = BooleanField('Conjuntivite', validators=[DataRequired()])
    artrite = BooleanField('Artrite', validators=[DataRequired()])
    artralgia = BooleanField('Artralgia', validators=[DataRequired()])
    petequia_n = BooleanField('Petéquias', validators=[DataRequired()])
    laco = BooleanField('Laceração', validators=[DataRequired()])
    dor_retro = BooleanField('Dor Retroocular', validators=[DataRequired()])
    diabetes = BooleanField('Diabetes', validators=[DataRequired()])
    hematolog = BooleanField('Doença Hematológica', validators=[DataRequired()])
    hepatopat = BooleanField('Hepatopatia', validators=[DataRequired()])
    renal = BooleanField('Doença Renal', validators=[DataRequired()])
    hipertensa = BooleanField('Hipertensão', validators=[DataRequired()])
    acido_pept = BooleanField('Úlcera Péptica', validators=[DataRequired()])
    auto_imune = BooleanField('Doença Autoimune', validators=[DataRequired()])
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
        prediccion = modelo.predict([sintomas])
        
        # Determinar el resultado basado en la predicción
        resultado = 'Dengue' if prediccion[0] == 1 else 'Chikungunya'
        
        return render_template('result', resultado=resultado)
    return render_template('index.html', form=form)

@app.route('/result/<resultado>', methods=['GET'])
def result(resultado):
    return render_template('resultado.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
