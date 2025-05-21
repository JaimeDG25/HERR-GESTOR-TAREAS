from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
db = SQLAlchemy()


class Estado(db.Model):
    __tablename__ = 'estado'
    id_estado = db.Column(db.Integer, primary_key=True)
    nombre_estado = db.Column(db.String(100), nullable=False)

class Prioridad(db.Model):
    __tablename__ = 'prioridad'
    id_prioridad = db.Column(db.Integer, primary_key=True)
    nombre_prioridad = db.Column(db.String(100), nullable=False)

class Categoria(db.Model):
    __tablename__ = 'categoria'
    id_categoria = db.Column(db.Integer, primary_key=True)
    nombre_categoria = db.Column(db.String(100), nullable=False)

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True,autoincrement=True)
    nombre_usuario = db.Column(db.String(100), nullable=False)
    apellido_usuario = db.Column(db.String(100), nullable=False)
    correo_usuario = db.Column(db.String(150), nullable=False)
    contraseña_usuario = db.Column(db.String(130), nullable=False)

class Tarea(db.Model):
    __tablename__ = 'tarea'
    id_tarea = db.Column(db.Integer, primary_key=True,autoincrement=True)
    titulo_tarea = db.Column(db.String(150), nullable=False)
    descripcion_tarea = db.Column(db.String(500), nullable=True)
    fcreacion_tarea = db.Column(db.DateTime, default=datetime.utcnow)
    fvencimiento_tarea = db.Column(db.DateTime, nullable=True)

    prioridad_id = db.Column(db.Integer, db.ForeignKey('prioridad.id_prioridad'), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey('estado.id_estado'), nullable=False)
    catalogo_id = db.Column(db.Integer, db.ForeignKey('categoria.id_categoria'), nullable=False)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)

    # Relaciones (opcional, pero recomendable)
    prioridad = db.relationship('Prioridad', backref='tareas')
    estado = db.relationship('Estado', backref='tareas')
    categoria = db.relationship('Categoria', backref='tareas')
    usuario = db.relationship('Usuario', backref='tareas')

class anuncio ():
    def saludar():
        saludo = 'hola'
        return saludo