import datetime

from scripts.db import Get_DB

class Calificacion:
    def __init__(self, legajo, puntaje):
        self.legajo = legajo
        self.puntaje = float(puntaje)
        
    def Get_Mensual():
        DB = Get_DB()
        CUR = DB.cursor()
        
        fecha_inicio = datetime.datetime.now().strftime('%Y-%m-01')
        fecha_fin = datetime.datetime.now().strftime('%Y-%m-31')
        
        CUR.execute('''
            WITH
                cte_eventos AS (
                    SELECT
                        asistencias_cab.id_evento AS id,
                        eventos.puntos,
                        COUNT(*) AS total
                    FROM
                        asistencias_cab
                        JOIN eventos ON eventos.id = asistencias_cab.id_evento
                    WHERE
                        asistencias_cab.fecha_aceptada IS NOT NULL
                        AND eventos.nombre != 'Conducta'
                        AND asistencias_cab.fecha_creada BETWEEN :fecha_inicio AND :fecha_fin
                    GROUP BY
                        asistencias_cab.id_evento
                ),
                cte_puntos AS (
                    SELECT
                        asistencias_det.legajo,
                        COUNT(
                            NULLIF(asistencias_det.estado, 0)
                        ) AS asistencias,
                        cte_eventos.total,
                        cte_eventos.puntos
                    FROM
                        asistencias_cab
                        JOIN asistencias_det ON asistencias_det.id_cab = asistencias_cab.id
                        JOIN cte_eventos ON cte_eventos.id = asistencias_cab.id_evento
                    WHERE
                        asistencias_cab.fecha_aceptada IS NOT NULL
                        AND asistencias_cab.fecha_creada BETWEEN :fecha_inicio AND :fecha_fin
                    GROUP BY
                        asistencias_det.legajo,
                        asistencias_cab.id_evento
                )
            SELECT
                legajo,
                ROUND(
                    SUM(asistencias * 1.0 / total * puntos),
                    2
                ) AS puntaje
            FROM
                cte_puntos
            GROUP BY
                cte_puntos.legajo
            ORDER BY
                cte_puntos.legajo;
            ''', {'fecha_inicio': f'{fecha_inicio}', 'fecha_fin': f'{fecha_fin}'})
        
        rows = CUR.fetchall()
        calificaciones = []
        
        for row in rows:
            calificacion = Calificacion(row[0], row[1])
            calificaciones.append(calificacion)
            
        return calificaciones

    def Get_Desglose_Mensual(legajo):
        DB = Get_DB()
        CUR = DB.cursor()
        
        fecha_inicio = datetime.datetime.now().strftime('%Y-%m-01')
        fecha_fin = datetime.datetime.now().strftime('%Y-%m-31')
        
        CUR.execute('''
            WITH
                cte_eventos AS (
                    SELECT
                        asistencias_cab.id_evento AS id,
                        eventos.puntos,
                        COUNT(*) AS total
                    FROM
                        asistencias_cab
                        JOIN eventos ON eventos.id = asistencias_cab.id_evento
                    WHERE
                        asistencias_cab.fecha_aceptada IS NOT NULL
                        AND eventos.nombre != 'Conducta'
                        AND asistencias_cab.fecha_creada BETWEEN '2025-11-01' AND '2025-11-31'
                    GROUP BY
                        asistencias_cab.id_evento
                )
                    SELECT
                        cte_eventos.id,
                        cte_eventos.puntos,
                        COUNT(
                            NULLIF(asistencias_det.estado, 0)
                        ) AS asistencias,
                        cte_eventos.total,
                        ROUND(
                            (COUNT(NULLIF(asistencias_det.estado, 0)) * 1.0 / total * puntos),
                            2
                        ) AS puntaje
                    FROM
                        asistencias_cab
                        JOIN asistencias_det ON asistencias_det.id_cab = asistencias_cab.id
                        JOIN cte_eventos ON cte_eventos.id = asistencias_cab.id_evento
                    WHERE
                        asistencias_cab.fecha_aceptada IS NOT NULL
                        AND asistencias_cab.fecha_creada BETWEEN :fecha_inicio AND :fecha_fin
                        AND asistencias_det.legajo == :legajo
                    GROUP BY
                        asistencias_det.legajo,
                        asistencias_cab.id_evento
            ''', {'legajo': legajo, 'fecha_inicio': f'{fecha_inicio}', 'fecha_fin': f'{fecha_fin}'})
        
        rows = CUR.fetchall()
        desglose = []
        
        for row in rows:
            desglose.append({
                'id_evento': row[0],
                'puntos': row[1],
                'asistencias': row[2],
                'total': row[3],
                'puntaje': row[4]
            })
            
        return desglose

    def Get_Semestral():
        DB = Get_DB()
        CUR = DB.cursor()
        
        fecha_inicio = datetime.datetime.now().strftime('%Y-01-01')
        fecha_fin = datetime.datetime.now().strftime('%Y-12-31')
        
        CUR.execute('''
            WITH
                cte_eventos AS (
                    SELECT
                        asistencias_cab.id_evento AS id,
                        eventos.puntos,
                        COUNT(*) AS total
                    FROM
                        asistencias_cab
                        JOIN eventos ON eventos.id = asistencias_cab.id_evento
                    WHERE
                        asistencias_cab.fecha_aceptada IS NOT NULL
                        AND eventos.nombre != 'Conducta'
                        AND asistencias_cab.fecha_creada BETWEEN :fecha_inicio AND :fecha_fin
                    GROUP BY
                        asistencias_cab.id_evento
                ),
                cte_puntos AS (
                    SELECT
                        asistencias_det.legajo,
                        COUNT(
                            NULLIF(asistencias_det.estado, 0)
                        ) AS asistencias,
                        cte_eventos.total,
                        cte_eventos.puntos
                    FROM
                        asistencias_cab
                        JOIN asistencias_det ON asistencias_det.id_cab = asistencias_cab.id
                        JOIN cte_eventos ON cte_eventos.id = asistencias_cab.id_evento
                    WHERE
                        asistencias_cab.fecha_aceptada IS NOT NULL
                        AND asistencias_cab.fecha_creada BETWEEN :fecha_inicio AND :fecha_fin
                    GROUP BY
                        asistencias_det.legajo,
                        asistencias_cab.id_evento
                )
            SELECT
                legajo,
                ROUND(
                    SUM(asistencias * 1.0 / total * puntos),
                    2
                ) AS puntaje
            FROM
                cte_puntos
            GROUP BY
                cte_puntos.legajo
            ORDER BY
                cte_puntos.legajo;
            ''', {'fecha_inicio': f'{fecha_inicio}', 'fecha_fin': f'{fecha_fin}'})
        
        rows = CUR.fetchall()
        calificaciones = []
        
        for row in rows:
            calificacion = Calificacion(row[0], row[1])
            calificaciones.append(calificacion)
            
        return calificaciones
    
    def Get_Anual():
        DB = Get_DB()
        CUR = DB.cursor()
        
        fecha_inicio = datetime.datetime.now().strftime('%Y-01-01')
        fecha_fin = datetime.datetime.now().strftime('%Y-12-31')
        
        CUR.execute('''
            WITH
                cte_eventos AS (
                    SELECT
                        asistencias_cab.id_evento AS id,
                        eventos.puntos,
                        COUNT(*) AS total
                    FROM
                        asistencias_cab
                        JOIN eventos ON eventos.id = asistencias_cab.id_evento
                    WHERE
                        asistencias_cab.fecha_aceptada IS NOT NULL
                        AND eventos.nombre != 'Conducta'
                        AND asistencias_cab.fecha_creada BETWEEN :fecha_inicio AND :fecha_fin
                    GROUP BY
                        asistencias_cab.id_evento
                ),
                cte_puntos AS (
                    SELECT
                        asistencias_det.legajo,
                        COUNT(
                            NULLIF(asistencias_det.estado, 0)
                        ) AS asistencias,
                        cte_eventos.total,
                        cte_eventos.puntos
                    FROM
                        asistencias_cab
                        JOIN asistencias_det ON asistencias_det.id_cab = asistencias_cab.id
                        JOIN cte_eventos ON cte_eventos.id = asistencias_cab.id_evento
                    WHERE
                        asistencias_cab.fecha_aceptada IS NOT NULL
                        AND asistencias_cab.fecha_creada BETWEEN :fecha_inicio AND :fecha_fin
                    GROUP BY
                        asistencias_det.legajo,
                        asistencias_cab.id_evento
                )
            SELECT
                legajo,
                ROUND(
                    SUM(asistencias * 1.0 / total * puntos),
                    2
                ) AS puntaje
            FROM
                cte_puntos
            GROUP BY
                cte_puntos.legajo
            ORDER BY
                cte_puntos.legajo;
            ''', {'fecha_inicio': f'{fecha_inicio}', 'fecha_fin': f'{fecha_fin}'})
        
        rows = CUR.fetchall()
        calificaciones = []
        
        for row in rows:
            calificacion = Calificacion(row[0], row[1])
            calificaciones.append(calificacion)
            
        return calificaciones