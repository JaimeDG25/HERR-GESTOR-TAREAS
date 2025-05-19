from flask import Flask, render_template
from flask_marshmallow import Marshmallow
from Settings.setting import get_sqlalchemy_uri ,get_connection
from Controllers.ctr_usuario import listar_usuario
from Models.model import db, anuncio


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_sqlalchemy_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
ma = Marshmallow(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():
    listar_usuarios= listar_usuario()
    print(get_sqlalchemy_uri())
    print(anuncio.saludar())
    print(get_connection())
    return render_template('index.html',listar_usuarios=listar_usuarios)

if __name__ == '__main__':
    app.run(debug=True)