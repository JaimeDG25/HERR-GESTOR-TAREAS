#IMPORTACIONES NECESARIAS DE CLASES Y METODOS NECESARIOS
from flask import Flask, render_template,request,url_for,redirect,session
from flask_marshmallow import Marshmallow
from Settings.setting import get_sqlalchemy_uri ,get_connection
from Controllers.ctr_usuario import listar_usuario
from FireStore.fs_contrasena import generar_clave, convertir_hash
from FireStore.fs_enviar_correo import Enviar_correo
from FireStore.fs_usuario import usuarios_listado,usuario_registrado
from FireStore.fs_rutas import login_required
from Models.model import db, anuncio,Usuario

#INICIALIZACION DE LA APP FLASK
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_sqlalchemy_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'tu_clave_secreta'
db.init_app(app)
ma = Marshmallow(app)

#GENERACION DE LOS MODELOS DE BASE DE DATOS
with app.app_context():
    db.create_all()


@app.route('/index')
@login_required
def index():
    listar_usuarios= usuarios_listado()
    print(get_sqlalchemy_uri())
    print(anuncio.saludar())
    print(get_connection())
    #password = input("Ingresa una contraseña")
    password ='contraseña'
    print("Clave generada suprema:", generar_clave())
    print("Hash SHA256 incognito:", convertir_hash(password))
    return render_template('index.html',listar_usuarios=listar_usuarios)

@app.route('/correo')
def correo ():
    password= generar_clave()
    hasheado=convertir_hash(password)
    resultado=Enviar_correo("jorshwild@gmail.com",password)
    print(resultado)
    return resultado


# ===================================== RUTA RAIZ DIRIGIENDO A UNA RUTA ESPECIFICA ==========================================
@app.route('/')
def home():
    return redirect(url_for('login'))
# ===================================== RUTA RAIZ DIRIGIENDO A UNA RUTA ESPECIFICA ==========================================


# ====================================== RUTA PARA EL LOGIN PRINCIPAL ======================================================
@app.route('/login',methods=['GET', 'POST'] )
def login():
    query = Usuario.query.all()
    # for usuario in query:
    #     print("ID:", usuario.id_usuario)
    #     print("Nombre:", usuario.nombre_usuario)
    #     print("Apellido:", usuario.apellido_usuario)
    #     print("Correo:", usuario.correo_usuario)
    #     print("Contraseña:", usuario.contraseña_usuario)
    #     print("---------------------")
    correo = request.args.get('correo') 
    return render_template('login.html', query=query,correo=correo)

#RUTA PARA ENVIAR DATOS 
@app.route('/enviar_datos', methods=['GET', 'POST'])
def enviar_datos():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        contraseña = convertir_hash(contraseña)
        usuario = Usuario.query.filter_by(correo_usuario=correo, contraseña_usuario=contraseña).first()
        if usuario:
            session['correo_usuario'] = correo  
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login', mensaje='Correo o contraseña incorrectos'))
    return redirect(url_for('login',correo=correo))

#RUTA PARA CERRAR LA SESSION
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login')) 
# ====================================== RUTA PARA EL LOGIN PRINCIPAL ======================================================


# ================================================ SECCION REGISTRO ===========================================
#RUTA PARA PODER REGISTRARTE 
@app.route('/registro_vista', methods=['GET', 'POST'])
def registro_vista():
    return render_template('registro.html')

#RUTA PARA REALIZAR EL REGISTRO
@app.route('/registro_usuario', methods=['GET', 'POST'])
def registro_usuario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        conf_contraseña = request.form ['conf_contraseña']
        if contraseña != conf_contraseña :
            mensaje = "La contraseña debe ser la misma"
            return render_template('registro.html',mensaje=mensaje)
        obj_user = Usuario(
            nombre_usuario=nombre,
            apellido_usuario=apellido,
            correo_usuario=correo,
            contraseña_usuario=convertir_hash(contraseña)
        )
        mensaje = usuario_registrado(obj_user)
        if mensaje == "usuario creado exitosamente":
            Enviar_correo(correo,convertir_hash(contraseña))
            mensaje_bueno = "Felicidades, usuario creado exitosamente"
            db.session.add(obj_user)
            db.session.commit()
            return render_template('registro.html',mensaje=mensaje_bueno)
    return render_template('registro.html',mensaje=mensaje)
# ================================================ SECCION REGISTRO ===========================================

if __name__ == '__main__':
    app.run(debug=True, port=9000)