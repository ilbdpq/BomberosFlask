import datetime

from scripts.db import Get_DB

class Asistencia_Cabecera:
    def __init__(self, id, id_evento, fecha_creada, fecha_aceptada = None, legajo_responsable = None, descripcion = None):
        self.id = int(id)
        self.id_evento = int(id_evento)
        self.fecha_creada = str(fecha_creada)
        self.fecha_aceptada = str(fecha_aceptada) if fecha_aceptada else None
        self.legajo_responsable = str(legajo_responsable) if legajo_responsable else None
        self.descripcion = str(descripcion) if descripcion else None
        self.detalles = []
        
    def Get_Asistencias(self):
        pass

    def Get_By_ID(id_cabecera):
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
        self.id = int(id) if id else None
        self.id_cab = int(id_cab)
        self.legajo = str(legajo)
        self.id_unidad = int(id_unidad) if id_unidad else None
        self.estado = int(estado)
        
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