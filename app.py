from flask import Flask, render_template, request, redirect, url_for, session, flash, make_response
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import datetime

# Inicializar la aplicación y la base de datos
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto'  # Cambia por un valor seguro
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask.db'  # Usa la URI de tu base de datos
db = SQLAlchemy(app)

# Definir el modelo de usuario
class User(db.Model):
    id_user = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# Formulario de inicio de sesión
class LoginForm(FlaskForm):
    username = StringField('Usuari', validators=[DataRequired()])
    password = PasswordField('Contrasenya', validators=[DataRequired()])
    submit = SubmitField('Iniciar sessió')

@app.route('/information', methods=['GET', 'POST'])
def information():
    # Crear la instancia del formulario de inicio de sesión
    login_form = LoginForm()
    
    # Inicializar los mensajes de error y éxito
    error_message = None
    success_message = None
    
    # Obtener la IP de la cookie si existe, o establecer una nueva cookie si no existe
    user_ip = request.cookies.get('user_ip')
    
    if not user_ip:
        user_ip = request.remote_addr
        resp = make_response(redirect(url_for('information')))  # Redirigir a la misma ruta
        resp.set_cookie('user_ip', user_ip, expires=datetime.datetime.now() + datetime.timedelta(days=30))  # Crear cookie con la IP
        session.clear()  # Reiniciar la sesión
        flash("No s'ha trobat cap cookie de sessió. Una nova ha estat creada.", category='warning')  # Mostrar mensaje de advertencia
        return resp
    
    # Si el formulario ha sido enviado y es válido
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data

        # Buscar el usuario en la base de datos
        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                session['username'] = user.username  # Guardar el nombre de usuario en la sesión
                success_message = "Has iniciat sessió correctament."  # Mensaje de éxito
                flash(success_message, category='success')  # Mensaje flash de éxito
                return redirect(url_for('information'))  # Redirigir a la misma página
            else:
                error_message = "La contrasenya és incorrecta."
                flash(error_message, category='danger')
        else:
            error_message = "No s'ha trobat cap usuari amb aquest nom."
            flash(error_message, category='danger')
    
    # Preparar los datos para la plantilla
    items = []  # Aquí puedes agregar la lógica para obtener items de la base de datos

    # Renderizar la plantilla y pasar el contexto
    return render_template('information.html', login_form=login_form, error_message=error_message, success_message=success_message, ip=user_ip, items=items)

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('username', None)  # Eliminar el usuario de la sesión
    resp = make_response(redirect(url_for('information')))
    resp.delete_cookie('user_ip')  # Eliminar la cookie de la IP
    return resp

# Ruta para la página principal
@app.route('/')
def index():
    return redirect(url_for('information'))

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)

# Creacionde tablas
# Crea las tablas si no existen
with app.app_context():
    db.create_all()

