from Models.model import *

def listar_categorias():
    query= Categoria.query.all()
    lista_categoria = []

    return lista_categoria