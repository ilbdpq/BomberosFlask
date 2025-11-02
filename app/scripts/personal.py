from scripts.db import Get_DB

class Bombero:
    def __init__(self, legajo, dni, username, password, apellido_nombre, telefono, fecha_nacimiento, provincia, lugar, permisos):
        self.legajo = legajo
        self.dni = dni
        self.username = username
        self.password = password
        self.apellido_nombre = apellido_nombre
        self.telefono = telefono
        self.fecha_nacimiento = fecha_nacimiento
        self.provincia = provincia
        self.lugar = lugar
        self.permisos = permisos
    
    def Get_Bombero_By_Username(username):
        DB = Get_DB()
        bombero_data = DB.execute(
            'SELECT * FROM personal WHERE username = ?',
            (username,)
        ).fetchone()
        
        if bombero_data is None:
            return None
        
        return Bombero(
            legajo=bombero_data['legajo'],
            dni=bombero_data['dni'],
            username=bombero_data['username'],
            password=bombero_data['password'],
            apellido_nombre=bombero_data['apellido_nombre'],
            telefono=bombero_data['telefono'],
            fecha_nacimiento=bombero_data['fecha_nacimiento'],
            provincia=bombero_data['provincia'],
            lugar=bombero_data['lugar'],
            permisos=bombero_data['permisos']
        )
        
    def Get_Bombero_By_Legajo(legajo):
        DB = Get_DB()
        bombero_data = DB.execute(
            'SELECT * FROM personal WHERE legajo = ?',
            (legajo,)
        ).fetchone()
        
        if bombero_data is None:
            return None
        
        return Bombero(
            legajo=bombero_data['legajo'],
            dni=bombero_data['dni'],
            username=bombero_data['username'],
            password=bombero_data['password'],
            apellido_nombre=bombero_data['apellido_nombre'],
            telefono=bombero_data['telefono'],
            fecha_nacimiento=bombero_data['fecha_nacimiento'],
            provincia=bombero_data['provincia'],
            lugar=bombero_data['lugar'],
            permisos=bombero_data['permisos']
        )
    
    def Get_Bombero_By_DNI(dni):
        DB = Get_DB()
        bombero_data = DB.execute(
            'SELECT * FROM personal WHERE dni = ?',
            (dni,)
        ).fetchone()
        
        if bombero_data is None:
            return None
        
        return Bombero(
            legajo=bombero_data['legajo'],
            dni=bombero_data['dni'],
            username=bombero_data['username'],
            password=bombero_data['password'],
            apellido_nombre=bombero_data['apellido_nombre'],
            telefono=bombero_data['telefono'],
            fecha_nacimiento=bombero_data['fecha_nacimiento'],
            provincia=bombero_data['provincia'],
            lugar=bombero_data['lugar'],
            permisos=bombero_data['permisos']
        )
        
    def Get_Bomberos():
        DB = Get_DB()
        bomberos_data = DB.execute(
            'SELECT * FROM personal'
        ).fetchall()
        
        bomberos_list = []
        
        for bombero_data in bomberos_data:
            bombero = Bombero(
                legajo=bombero_data['legajo'],
                dni=bombero_data['dni'],
                username=bombero_data['username'],
                password=bombero_data['password'],
                apellido_nombre=bombero_data['apellido_nombre'],
                telefono=bombero_data['telefono'],
                fecha_nacimiento=bombero_data['fecha_nacimiento'],
                provincia=bombero_data['provincia'],
                lugar=bombero_data['lugar'],
                permisos=bombero_data['permisos']
            )
            bomberos_list.append(bombero)
        
        return bomberos_list

    def Add(self):
        DB = Get_DB()
        DB.execute(
            'INSERT INTO personal (legajo, dni, username, password, apellido_nombre, telefono, fecha_nacimiento, provincia, lugar, permisos) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (self.legajo, self.dni, self.username, self.password, self.apellido_nombre, self.telefono, self.fecha_nacimiento, self.provincia, self.lugar, self.permisos)
        )
        DB.commit()

    def Set(self):
        DB = Get_DB()
        DB.execute(
            'UPDATE personal SET dni = ?, username = ?, password = ?, apellido_nombre = ?, telefono = ?, fecha_nacimiento = ?, provincia = ?, lugar = ?, permisos = ? WHERE legajo = ?',
            (self.dni, self.username, self.password, self.apellido_nombre, self.telefono, self.fecha_nacimiento, self.provincia, self.lugar, self.permisos, self.legajo)
        )
        DB.commit()