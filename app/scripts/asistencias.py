import datetime

from scripts.db import Get_DB

class Asistencia_Cabecera:
    def __init__(self, id, id_evento, fecha_creada, fecha_aceptada = None, legajo_responsable = None, descripcion = None):
        self.id = id
        self.id_evento = id_evento
        self.fecha_creada = fecha_creada
        self.fecha_aceptada = fecha_aceptada
        self.legajo_responsable = legajo_responsable
        self.descripcion = descripcion
        self.detalles = []
        
    def Get_Asistencias(self):
        pass

    def Get_Asistencia_By_ID(id_cabecera):
        DB = Get_DB()
        CUR = DB.cursor()
        CUR.execute('SELECT id, id_evento, fecha_creada, fecha_aceptada, legajo_responsable, descripcion FROM asistencias_cab WHERE id = ?', (id_cabecera,))
        row = CUR.fetchone()

        if row is None:
            return None

        return Asistencia_Cabecera(row[0], row[1], row[2], row[3], row[4], row[5])
    
    def Add_Detalle(self, detalle):
        self.detalles.append(detalle)
        
class Asistencia_Detalle:
    def __init__(self, id, id_cab, legajo, id_unidad, estado):
        self.id = id
        self.id_cab = id_cab
        self.legajo = legajo
        self.id_unidad = id_unidad
        self.estado = estado
        
    def Add(self):
        DB = Get_DB()
        DB.execute('INSERT INTO asistencias_det (id_cab, legajo, id_unidad, estado) VALUES (?, ?, ?, ?)', (self.id_cab, self.legajo, self.id_unidad, self.estado))
        DB.commit()
        
def Add_Cabecera(id_evento):
    fecha_creada = datetime.datetime.now().strftime('%Y-%m-%d')
    
    DB = Get_DB()
    CUR = DB.cursor()
    CUR.execute('INSERT INTO asistencias_cab (id_evento, fecha_creada) VALUES (?, ?)', (id_evento, fecha_creada))
    DB.commit()
    
    return CUR.lastrowid