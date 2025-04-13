from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from marshmallow import fields, validates, ValidationError
from ..models.usuario_model import Usuario
from ..models.rol_model import Rol

class UsuarioSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Usuario
        load_instance = True
        include_fk = True

    rol_nombre = fields.String()  # Ya no es obligatorio, solo es un paso para obtener el rol_id

    # Validación para convertir el nombre del rol en 'rol_id'
    @validates('rol_nombre')
    def validar_rol(self, value):
        if value:  # Si hay un valor en rol_nombre, buscamos el rol
            # Buscar el rol por nombre
            rol = Rol.query.filter_by(nombre=value).first()
            if not rol:
                raise ValidationError(f"El rol '{value}' no existe.")
            # Asignamos el id del rol al campo rol_id
            self.rol_id = rol.id
        else:
            raise ValidationError("El nombre del rol es obligatorio.")
    
    # Método para serializar el nombre del rol (esto es opcional)
    rol = fields.Method("get_rol_nombre")

    def get_rol_nombre(self, obj):
        return obj.rol.nombre if obj.rol else None
