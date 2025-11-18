from scripts.db import Get_DB

class Unidad:
    def __init__(self, id, nombre, patente, estado):
        self.id = id
        self.nombre = nombre
        self.patente = patente
        self.estado = estado

    def Get_Unidad_By_ID(id):
        DB = Get_DB()
        unidad_data = DB.execute(
            'SELECT * FROM unidades WHERE id = ?',
            (id,)
        ).fetchone()
        
        if unidad_data is None:
            return None
        
        return Unidad(
            id=unidad_data['id'],
            nombre=unidad_data['nombre'],
            patente=unidad_data['patente'],
            estado=unidad_data['estado']
        )

    def Get_Unidades():
        DB = Get_DB()
        unidades_data = DB.execute(
            'SELECT * FROM unidades'
        ).fetchall()
        
        unidades = []
        for unidad_data in unidades_data:
            unidades.append(
                Unidad(
                    id=unidad_data['id'],
                    nombre=unidad_data['nombre'],
                    patente=unidad_data['patente'],
                    estado=unidad_data['estado']
                )
            )
        
        return unidades

    def Set(self):
        DB = Get_DB()
        DB.execute(
            'UPDATE unidades SET nombre = ?, patente = ?, estado = ? WHERE id = ?',
            (self.nombre, self.patente, self.estado, self.id)
        )
        DB.commit()

    def Add(self):
        DB = Get_DB()
        DB.execute(
            'INSERT INTO unidades (nombre, patente, estado) VALUES (?, ?, ?)',
            (self.nombre, self.patente, self.estado)
        )
        DB.commit()