class Usuario:
    def __init__(self, id_usuario, usuario, contrasena, activo, id_rol, nombre, rol):
        self.id_usuario = id_usuario
        self.usuario = usuario
        self.contrasena = contrasena
        self.activo = activo
        self.id_rol = id_rol
        self.nombre = nombre
        self.rol = rol

    def __str__(self):
        return f"Usuario(id_usuario={self.id_usuario}, usuario='{self.usuario}', contrasena='{self.contrasena}', activo={self.activo}, id_rol={self.id_rol}, nombre='{self.nombre}', rol='{self.rol}')"
