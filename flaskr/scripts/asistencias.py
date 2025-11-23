import datetime

from .db import Get_DB
from .eventos import Evento

class Asistencia_Cabecera:
    def __init__(self, id, id_evento, fecha_creada, fecha_aceptada = None, legajo_responsable = None, descripcion = None):
        self.id = int(id)
        self.id_evento = int(id_evento)
        self.fecha_creada = str(fecha_creada)
        self.fecha_aceptada = str(fecha_aceptada) if fecha_aceptada else None
        self.legajo_responsable = str(legajo_responsable) if legajo_responsable else None
        self.descripcion = str(descripcion) if descripcion else None
        self.detalles = self.Get_Detalles()
        
    def Get_Detalles(self):
        DB = Get_DB()
        CUR = DB.cursor()
        CUR.execute('SELECT id, id_cab, legajo, id_unidad, estado FROM asistencias_det WHERE id_cab = ?', (self.id,))
        rows = CUR.fetchall()

        detalles = []
        for row in rows:
            detalle = Asistencia_Detalle(row[0], row[1], row[2], row[3], row[4])
            detalles.append(detalle)

        return detalles

    def Get_By_ID(id_cabecera):
        DB = Get_DB()
        CUR = DB.cursor()
        CUR.execute('SELECT id, id_evento, fecha_creada, fecha_aceptada, legajo_responsable, descripcion FROM asistencias_cab WHERE id = ?', (id_cabecera,))
        row = CUR.fetchone()

        if row is None:
            return None

        return Asistencia_Cabecera(row[0], row[1], row[2], row[3], row[4], row[5])

    def Get_Aceptadas():
        DB = Get_DB()
        CUR = DB.cursor()
        CUR.execute('SELECT id, id_evento, fecha_creada, fecha_aceptada, legajo_responsable, descripcion FROM asistencias_cab WHERE fecha_aceptada IS NOT NULL')
        rows = CUR.fetchall()

        cabeceras = []
        for row in rows:
            cabecera = Asistencia_Cabecera(row[0], row[1], row[2], row[3], row[4], row[5])
            cabeceras.append(cabecera)

        return cabeceras

    def Get_Pendientes():
        DB = Get_DB()
        CUR = DB.cursor()
        CUR.execute('SELECT id, id_evento, fecha_creada, fecha_aceptada, legajo_responsable, descripcion FROM asistencias_cab WHERE fecha_aceptada IS NULL')
        rows = CUR.fetchall()

        cabeceras = []
        for row in rows:
            cabecera = Asistencia_Cabecera(row[0], row[1], row[2], row[3], row[4], row[5])
            cabeceras.append(cabecera)

        return cabeceras
    
    def Get_Aceptadas_Rango(fecha_inicio, fecha_fin):
        print('Fecha Inicio:', fecha_inicio, 'Fecha Fin:', fecha_fin)
        DB = Get_DB()
        CUR = DB.cursor()
        CUR.execute('SELECT id, id_evento, fecha_creada, fecha_aceptada, legajo_responsable, descripcion FROM asistencias_cab WHERE fecha_aceptada NOT NULL AND fecha_creada BETWEEN ? AND ?', (fecha_inicio, fecha_fin))
        rows = CUR.fetchall()

        cabeceras = []
        for row in rows:
            cabecera = Asistencia_Cabecera(row[0], row[1], row[2], row[3], row[4], row[5])
            cabeceras.append(cabecera)

        return cabeceras

    def Set(self):
        DB = Get_DB()
        DB.execute('UPDATE asistencias_cab SET fecha_aceptada = ?, legajo_responsable = ?, descripcion = ? WHERE id = ?', (self.fecha_aceptada, self.legajo_responsable, self.descripcion, self.id))
        DB.commit()

    def Add_Detalle(self, detalle):
        self.detalles.append(detalle)

    def Del(self):
        DB = Get_DB()
        DB.execute('DELETE FROM asistencias_cab WHERE id = ?', (self.id,))
        DB.execute('DELETE FROM asistencias_det WHERE id_cab = ?', (self.id,))
        DB.commit()
        
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
        
def Add_Cabecera(id_evento, fecha_creada=None):
    if not fecha_creada:
        fecha_creada = datetime.datetime.now().strftime('%Y-%m-%d')
    
    DB = Get_DB()
    CUR = DB.cursor()
        
    CUR.execute('INSERT INTO asistencias_cab (id_evento, fecha_creada) VALUES (?, ?)', (id_evento, fecha_creada))
    DB.commit()
    
    return CUR.lastrowid

def Verificar_Conducta_Mes():
    '''True si se cargo la conducta del mes actual'''
    
    DB = Get_DB()
    CUR = DB.cursor()
    fecha_inicio = datetime.datetime.now().strftime('%Y-%m-01')
    fecha_fin = datetime.datetime.now().strftime('%Y-%m-31')
    
    CUR.execute('''
        SELECT
            COUNT(*)
        FROM
            asistencias_cab
        WHERE
            id_evento = (
                SELECT
                    id
                FROM
                    eventos
                WHERE
                    nombre = "Conducta"
            )
            AND fecha_creada BETWEEN :fecha_inicio AND :fecha_fin;
        ''', {'fecha_inicio': fecha_inicio, 'fecha_fin': fecha_fin})
    row = CUR.fetchone()
    
    return row[0] > 0