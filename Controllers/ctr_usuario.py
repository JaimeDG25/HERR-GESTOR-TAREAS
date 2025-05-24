from Models.model import Usuario
from flask import session,render_template
def listar_usuario():
    usuarios= Usuario.query.all()
    return usuarios
def consultar_usuario(correo,contraseña):
    usuario_encontrado = Usuario.query.filter_by(correo_usuario=correo, contraseña_usuario=contraseña).first()
    return usuario_encontrado


def escribir_usuario(nombre,correo):
    verificar = print(f"Tu nombre de usuario: {nombre} ; tu correo: {correo}")
    return verificar