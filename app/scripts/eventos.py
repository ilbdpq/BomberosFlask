from scripts.db import Get_DB

class Evento:
    def __init__(self, id, nombre, puntos):
        self.id = id
        self.nombre = nombre
        self.puntos = puntos

    def Get_Evento_By_ID(id):
        DB = Get_DB()
        evento_data = DB.execute(
            'SELECT * FROM eventos WHERE id = ?',
            (id,)
        ).fetchone()
        
        if evento_data is None:
            return None
        
        return Evento(
            id=evento_data['id'],
            nombre=evento_data['nombre'],
            puntos=evento_data['puntos']
        )
        
    def Get_Evento_By_Nombre(nombre):
        DB = Get_DB()
        evento_data = DB.execute(
            'SELECT * FROM eventos WHERE nombre = ?',
            (nombre,)
        ).fetchone()
        
        if evento_data is None:
            return None
        
        return Evento(
            id=evento_data['id'],
            nombre=evento_data['nombre'],
            puntos=evento_data['puntos']
        )

    def Get_Eventos():
        DB = Get_DB()
        eventos_data = DB.execute(
            'SELECT * FROM eventos WHERE nombre != "Conducta"'
        ).fetchall()
        
        eventos = []
        for evento_data in eventos_data:
            eventos.append(
                Evento(
                    id=evento_data['id'],
                    nombre=evento_data['nombre'],
                    puntos=evento_data['puntos']
                )
            )
        
        return eventos

    def Set(self):
        DB = Get_DB()
        DB.execute(
            'UPDATE eventos SET nombre = ?, puntos = ? WHERE id = ?',
            (self.nombre, self.puntos, self.id)
        )
        DB.commit()

    def Add(self):
        DB = Get_DB()
        DB.execute(
            'INSERT INTO eventos (nombre, puntos) VALUES (?, ?)',
            (self.nombre, self.puntos)
        )
        DB.commit()