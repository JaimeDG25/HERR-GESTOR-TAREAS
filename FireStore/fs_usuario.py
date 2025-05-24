from Controllers.ctr_usuario import listar_usuario
from Models.model import Usuario
from flask import session,render_template

def usuarios_listado():
    listar_usuario()
    return listar_usuario()

def usuario_registrado( obj_user:Usuario):
    mensaje_registrar = ""
    if(obj_user.nombre_usuario== "" ):
        mensaje_registrar = "El nombre no puede estar vacio"
        return mensaje_registrar
    if(obj_user.apellido_usuario== "" ):
        mensaje_registrar = "El apellido no puede estar vacio"
        return mensaje_registrar
    if(obj_user.correo_usuario== "" ):
        mensaje_registrar = "El correo no puede estar vacio"
        return mensaje_registrar
    return "usuario creado exitosamente"

def confirmar_contraseña(contraseña,conf_contraseña):
    if contraseña != conf_contraseña :
        mensaje_contraseña = "La contraseña debe ser la misma 2 3"
        return mensaje_contraseña