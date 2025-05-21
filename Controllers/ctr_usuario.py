from Models.model import Usuario

def listar_usuario():
    usuarios= Usuario.query.all()
    lista_usuario=[]

    # for usuario in usuarios:
    #     lista_usuario.append({
    #         "id_usuario": usuario.id,
    #         "nombre_usuario": usuario.nombre,
    #         "apellido_usuario":usuario.apellido,
    #         "correo_usuario": usuario.correo,
    #         "contraseña_usuario":usuario.contraseña
    #         # Agrega más campos según el modelo
    #     })
    return usuarios

# def registrar_usuario():
#     Usuario.add()
#     return pass