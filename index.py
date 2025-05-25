#IMPORTACIONES NECESARIAS DE CLASES Y METODOS NECESARIOS
from flask import Flask, render_template,request,url_for,redirect,session
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

#IMPORTACION DE MODELS
from Models.model import db,Proyecto, Usuario, Tarea, Estado, Prioridad, Categoria

#IMPORTACION DE SETTINGS
from Settings.setting import get_sqlalchemy_uri

#IMPORTACION DE CONTROLLERS
from Controllers.ctr_usuario import Controll_Usuario

#IMPORTACIONES DE FIRESTORE
from FireStore.fs_usuario import usuarios_listado,usuario_registrado,confirmar_contraseña

#IMPORTACIONES DE SOURCES
from Sources.sr_contraseña import generar_clave,convertir_hash
from Sources.sr_enviar_correo import Enviar_correo
from Sources.sr_rutas import login_required

#INICIALIZACION DE LA APP FLASK
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = get_sqlalchemy_uri()
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'tu_clave_secreta'
db.init_app(app)
migrate = Migrate(app, db) 
ma = Marshmallow(app)

#GENERACION DE LOS MODELOS DE BASE DE DATOS
with app.app_context():
    db.create_all()

# ===================================== RUTA RAIZ DIRIGIENDO A UNA RUTA ESPECIFICA ==========================================
@app.route('/')
def home():
    return redirect(url_for('login'))
# ===================================== RUTA RAIZ DIRIGIENDO A UNA RUTA ESPECIFICA ==========================================

# ====================================== RUTA PARA EL LOGIN PRINCIPAL ======================================================
@app.route('/login',methods=['GET', 'POST'] )
def login():
    nombre="asdf"
    correo="qwer"
    #query = listar_usuario()
    query = Controll_Usuario().listar_usuario()
    #print("Importando en metodo: ",query)
    print("Importante en clase: ",query)
    #escribir_usuario(nombre,correo)
    Controll_Usuario().escribir_usuario(nombre,correo)
    return render_template('login.html', query=query)


#RUTA PARA ENVIAR DATOS 
@app.route('/enviar_datos', methods=['GET', 'POST'])
def enviar_datos():
    if request.method == 'POST':
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        contraseña = convertir_hash(contraseña)
        usuario = Controll_Usuario().consultar_usuario(correo,contraseña)
        if usuario:
            session['nombre_usuario'] = usuario.nombre_usuario
            session['correo_usuario'] = usuario.correo_usuario
            session['apellido_usuario'] = usuario.apellido_usuario
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login', mensaje='Correo o contraseña incorrectos'))
    return redirect(url_for('login'))

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

        if confirmar_contraseña(contraseña,conf_contraseña):
            mensaje = confirmar_contraseña(contraseña,conf_contraseña)
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

@app.route('/index')
@login_required
def index():
    listar_usuarios= usuarios_listado()
    correo = session.get('correo_usuario', 'Usuario no identificado')
    nombre = session.get('nombre_usuario', 'Usuario no identificado')
    apellido = session.get('apellido_usuario', 'Usuario no identificado')
    print("==============ESTADO=================")
    estado = Estado.query.all()
    for est in estado:
        print(est.nombre_estado)
    print("===============PRIORIDAD================")
    prioridad = Prioridad.query.all()
    for prio in prioridad:
        print(prio.nombre_prioridad)
    print("===============CATEGORIA================")
    categoria = Categoria.query.all()
    for cate in categoria:
        print(cate.nombre_categoria)
    return render_template('index.html',
                            listar_usuarios=listar_usuarios, correo=correo, nombre=nombre,
                            apellido=apellido, estado=estado, prioridad=prioridad, categoria=categoria)

@app.route('/correo')
def correo ():
    password= generar_clave()
    hasheado=convertir_hash(password)
    resultado=Enviar_correo("jorshwild@gmail.com",password)
    print(resultado)
    return resultado
# ===================================== RUTA RAIZ DIRIGIENDO A LA RUTA CONTENIDO ==========================================

# ===================================== RUTA RAIZ DIRIGIENDO A LA RUTA CONTENIDO ==========================================


if __name__ == '__main__':
    app.run(debug=True, port=9000)