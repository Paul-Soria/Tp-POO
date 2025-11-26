import csv
import os
import json

class Cliente:
    def __init__(self, nombre, telefono, email, id_cliente=None):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email
        self.id_cliente = id_cliente
    
    def mostrar_info(self):
        return {
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.email,
            "id_cliente": self.id_cliente
        }

class Turno:
    def __init__(self, cliente, fecha, hora, servicio, estado="pendiente", id_turno=None):
        self.cliente = cliente
        self.fecha = fecha
        self.hora = hora
        self.servicio = servicio
        self.estado = estado
        self.id_turno = id_turno
    
    def mostrar_info(self):
        return {
            "id_turno": self.id_turno,
            "cliente": self.cliente.mostrar_info(),
            "fecha": self.fecha,
            "hora": self.hora,
            "servicio": self.servicio,
            "estado": self.estado
        }
    
    def modificar_turno(self, nueva_fecha=None, nueva_hora=None, nuevo_servicio=None):
        if nueva_fecha:
            self.fecha = nueva_fecha
        if nueva_hora:
            self.hora = nueva_hora
        if nuevo_servicio:
            self.servicio = nuevo_servicio
        return "decidite amigo"
    
    def cambiar_estado(self, nuevo_estado):
        estados_validos = ["pendiente", "confirmado", "cancelado", "completado"]
        if nuevo_estado in estados_validos:
            self.estado = nuevo_estado
            return f"Estado cambiado a: {nuevo_estado}"
        else:
            return "Estado no válido"

class GestorTurnos:
    def __init__(self):
        self.clientes = []
        self.turnos = []
        self.archivo_csv_turnos = "turnos.csv"
        self.archivo_csv_clientes = "clientes.csv"
        self.archivo_dict = "datos.json"
        self.proximo_id_turno = 1
        self.proximo_id_cliente = 1
        
        self.servicios_disponibles = {
            "1": "corte",
            "2": "barba", 
            "3": "corte y barba",
            "4": "tintura",
            "5": "tintura y corte",
            "6": "tintura, corte y barba",
            "7": "tintura y barba"
        }
        
        self.cargar_desde_csv()
    
    def generar_id_turno(self):
        id_actual = self.proximo_id_turno
        self.proximo_id_turno = self.proximo_id_turno + 1
        return id_actual
    
    def generar_id_cliente(self):
        id_actual = self.proximo_id_cliente
        self.proximo_id_cliente = self.proximo_id_cliente + 1
        return id_actual
    
    def validar_email(self, email):
        if "@" not in email:
            return False
        return True
    
    def validar_telefono(self, telefono):
        if len(telefono) < 8:
            return False
        if not telefono.isdigit():
            return False
        return True
    
    def mostrar_servicios(self):
        print("\nServicios disponibles:")
        print("1. Corte")
        print("2. Barba")
        print("3. Corte y Barba")
        print("4. Tintura")
        print("5. Tintura y Corte")
        print("6. Tintura, Corte y Barba")
        print("7. Tintura y Barba")
    
    def obtener_servicio_por_numero(self, numero):
        return self.servicios_disponibles.get(numero)
    
    def registrar_cliente(self, nombre, telefono, email):
        if not all([nombre, telefono, email]):
            return "Error: No seas bago y completa los datos"
        
        if not self.validar_email(email):
            return "Error: no te olvides el @ culiao"
        
        if not self.validar_telefono(telefono):
            return "Error: El teléfono debe tener al menos 8 números"
        
        i = 0
        while i < len(self.clientes):
            cliente = self.clientes[i]
            if cliente.email == email:
                return "Error: Este email ya está registrado"
            i = i + 1
        
        nuevo_cliente = Cliente(nombre, telefono, email, self.generar_id_cliente())
        self.clientes.append(nuevo_cliente)
        
        self.guardar_clientes_en_csv()
        
        return f"Pelados abstenerse. ID: {nuevo_cliente.id_cliente}"
    
    def buscar_cliente(self, email=None, id_cliente=None):
        i = 0
        while i < len(self.clientes):
            cliente = self.clientes[i]
            if (email and cliente.email == email) or (id_cliente and cliente.id_cliente == id_cliente):
                return cliente
            i = i + 1
        return None
    
    def buscar_cliente_por_nombre(self, nombre):
        i = 0
        while i < len(self.clientes):
            cliente = self.clientes[i]
            if cliente.nombre.lower() == nombre.lower():
                return cliente
            i = i + 1
        return None

    def buscar_turnos_por_cliente(self, nombre_cliente):
        turnos_cliente = []
        cliente = self.buscar_cliente_por_nombre(nombre_cliente)
        if cliente:
            i = 0
            while i < len(self.turnos):
                turno = self.turnos[i]
                if turno.cliente.id_cliente == cliente.id_cliente and turno.estado != "cancelado":
                    turnos_cliente.append(turno)
                i = i + 1
        return turnos_cliente
    
    def solicitar_turno(self, nombre_cliente, fecha, hora, servicio):
        cliente = self.buscar_cliente_por_nombre(nombre_cliente)
        if not cliente:
            return "Error: Cliente no registrado"
        
        i = 0
        while i < len(self.turnos):
            turno = self.turnos[i]
            if (turno.fecha == fecha and 
                turno.hora == hora and 
                turno.estado != "cancelado"):
                return "Error: Ya existe un turno en ese horario"
            i = i + 1
        
        nuevo_turno = Turno(cliente, fecha, hora, servicio, "pendiente", self.generar_id_turno())
        self.turnos.append(nuevo_turno)
        
        self.guardar_turnos_en_csv()
        
        return f"Turno solicitado exitosamente. ID Turno: {nuevo_turno.id_turno}"
    
    def listar_turnos(self, filtro_cliente=None, filtro_fecha=None, filtro_estado=None):
        turnos_filtrados = []
        i = 0
        
        while i < len(self.turnos):
            turno = self.turnos[i]
            cumple_filtro = True
            
            if filtro_cliente:
                nombre_min = turno.cliente.nombre.lower()
                email_min = turno.cliente.email.lower()
                filtro_min = filtro_cliente.lower()
                
                if (filtro_min not in nombre_min and 
                    filtro_min not in email_min):
                    cumple_filtro = False
            
            if filtro_fecha and turno.fecha != filtro_fecha:
                cumple_filtro = False
            
            if filtro_estado and turno.estado != filtro_estado:
                cumple_filtro = False
            
            if cumple_filtro:
                turnos_filtrados.append(turno.mostrar_info())
            
            i = i + 1
        
        return turnos_filtrados
    

    def modificar_turno_por_cliente(self, nombre_cliente, nueva_fecha=None, nueva_hora=None, nuevo_servicio=None):
        turnos_cliente = self.buscar_turnos_por_cliente(nombre_cliente)
        
        if not turnos_cliente:
            return "Error: No se encontraron turnos para este cliente"
        
        if len(turnos_cliente) == 1:
            turno = turnos_cliente[0]
            
            fecha_a_validar = nueva_fecha if nueva_fecha else turno.fecha
            hora_a_validar = nueva_hora if nueva_hora else turno.hora
            
            j = 0
            while j < len(self.turnos):
                otro_turno = self.turnos[j]
                if (otro_turno.id_turno != turno.id_turno and 
                    otro_turno.fecha == fecha_a_validar and 
                    otro_turno.hora == hora_a_validar and 
                    otro_turno.estado != "cancelado"):
                    return "Error: Ya existe un turno en ese horario"
                j = j + 1
            
            resultado = turno.modificar_turno(nueva_fecha, nueva_hora, nuevo_servicio)
            self.guardar_turnos_en_csv()
            return f"Turno modificado: {resultado}"
        else:
            print(f"\nSe encontraron {len(turnos_cliente)} turnos para {nombre_cliente}:")
            i = 0
            while i < len(turnos_cliente):
                turno = turnos_cliente[i]
                info = turno.mostrar_info()
                print(f"{i+1}. ID: {info['id_turno']} - Fecha: {info['fecha']} - Hora: {info['hora']} - Servicio: {info['servicio']} - Estado: {info['estado']}")
                i = i + 1
            
            try:
                seleccion = int(input("Seleccione el número del turno a modificar: ")) - 1
                if 0 <= seleccion < len(turnos_cliente):
                    turno = turnos_cliente[seleccion]
                    
                    fecha_a_validar = nueva_fecha if nueva_fecha else turno.fecha
                    hora_a_validar = nueva_hora if nueva_hora else turno.hora
                    
                    j = 0
                    while j < len(self.turnos):
                        otro_turno = self.turnos[j]
                        if (otro_turno.id_turno != turno.id_turno and 
                            otro_turno.fecha == fecha_a_validar and 
                            otro_turno.hora == hora_a_validar and 
                            otro_turno.estado != "cancelado"):
                            return "Error: Ya existe un turno en ese horario"
                        j = j + 1
                    
                    resultado = turno.modificar_turno(nueva_fecha, nueva_hora, nuevo_servicio)
                    self.guardar_turnos_en_csv()
                    return f"Turno modificado: {resultado}"
                else:
                    return "Error: Selección no válida"
            except ValueError:
                return "Error: Debe ingresar un número válido"

    def cancelar_turno_por_cliente(self, nombre_cliente):
        turnos_cliente = self.buscar_turnos_por_cliente(nombre_cliente)
        
        if not turnos_cliente:
            return "Error: No se encontraron turnos para este cliente"
        
        if len(turnos_cliente) == 1:
            turno = turnos_cliente[0]
            resultado = turno.cambiar_estado("cancelado")
            self.guardar_turnos_en_csv()
            return f"Turno cancelado: {resultado}"
        else:
            print(f"\nSe encontraron {len(turnos_cliente)} turnos para {nombre_cliente}:")
            i = 0
            while i < len(turnos_cliente):
                turno = turnos_cliente[i]
                info = turno.mostrar_info()
                print(f"{i+1}. ID: {info['id_turno']} - Fecha: {info['fecha']} - Hora: {info['hora']} - Servicio: {info['servicio']} - Estado: {info['estado']}")
                i = i + 1
            
            try:
                seleccion = int(input("Seleccione el número del turno a cancelar: ")) - 1
                if 0 <= seleccion < len(turnos_cliente):
                    turno = turnos_cliente[seleccion]
                    resultado = turno.cambiar_estado("cancelado")
                    self.guardar_turnos_en_csv()
                    return f"Turno cancelado: {resultado}"
                else:
                    return "Error: Selección no válida"
            except ValueError:
                return "Error: Debe ingresar un número válido"    
    
    def guardar_turnos_en_csv(self):
        try:
            with open(self.archivo_csv_turnos, 'w', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                
                writer.writerow(["id_turno", "id_cliente", "fecha", "hora", "servicio", "estado"])
                
                i = 0
                while i < len(self.turnos):
                    turno = self.turnos[i]
                    writer.writerow([
                        turno.id_turno,
                        turno.cliente.id_cliente,
                        turno.fecha,
                        turno.hora,
                        turno.servicio,
                        turno.estado
                    ])
                    i = i + 1
            
            return "Turnos guardados exitosamente en CSV"
        
        except Exception as e:
            return f"Error al guardar turnos en CSV: {str(e)}"
    
    def guardar_clientes_en_csv(self):
        try:
            with open(self.archivo_csv_clientes, 'w', newline='', encoding='utf-8') as archivo:
                writer = csv.writer(archivo)
                
                writer.writerow(["id_cliente", "nombre", "telefono", "email"])
                
                i = 0
                while i < len(self.clientes):
                    cliente = self.clientes[i]
                    writer.writerow([
                        cliente.id_cliente,
                        cliente.nombre,
                        cliente.telefono,
                        cliente.email
                    ])
                    i = i + 1
            
            return "Clientes guardados exitosamente en CSV"
        
        except Exception as e:
            return f"Error al guardar clientes en CSV: {str(e)}"
    
    def cargar_desde_csv(self):
        max_id_turno = 0
        max_id_cliente = 0
        
        if os.path.exists(self.archivo_csv_clientes):
            try:
                with open(self.archivo_csv_clientes, 'r', encoding='utf-8') as archivo:
                    reader = csv.DictReader(archivo)
                    filas = list(reader)
                    i = 0
                    while i < len(filas):
                        fila = filas[i]
                        id_cliente = int(fila["id_cliente"])
                        if id_cliente > max_id_cliente:
                            max_id_cliente = id_cliente
                        
                        nuevo_cliente = Cliente(
                            fila["nombre"],
                            fila["telefono"],
                            fila["email"],
                            id_cliente
                        )
                        self.clientes.append(nuevo_cliente)
                        i = i + 1
            except Exception as e:
                print(f"Error al cargar clientes: {str(e)}")
        
        if os.path.exists(self.archivo_csv_turnos):
            try:
                with open(self.archivo_csv_turnos, 'r', encoding='utf-8') as archivo:
                    reader = csv.DictReader(archivo)
                    filas = list(reader)
                    i = 0
                    while i < len(filas):
                        fila = filas[i]
                        id_turno = int(fila["id_turno"])
                        id_cliente = int(fila["id_cliente"])
                        
                        if id_turno > max_id_turno:
                            max_id_turno = id_turno
                        
                        cliente_turno = None
                        j = 0
                        while j < len(self.clientes):
                            if self.clientes[j].id_cliente == id_cliente:
                                cliente_turno = self.clientes[j]
                                break
                            j = j + 1
                        
                        if cliente_turno:
                            nuevo_turno = Turno(
                                cliente_turno,
                                fila["fecha"],
                                fila["hora"],
                                fila["servicio"],
                                fila["estado"],
                                id_turno
                            )
                            self.turnos.append(nuevo_turno)
                        
                        i = i + 1
            except Exception as e:
                print(f"Error al cargar turnos: {str(e)}")
        
        self.proximo_id_turno = max_id_turno + 1
        self.proximo_id_cliente = max_id_cliente + 1
        
        return "Datos cargados exitosamente desde CSV"
    
    def guardar_en_dict(self):
        try:
            datos_dict = self.convertir_a_dict()
            
            with open(self.archivo_dict, 'w', encoding='utf-8') as archivo:
                json.dump(datos_dict, archivo, indent=4)
            
            return "Datos guardados exitosamente en archivo dict (JSON)"
        
        except Exception as e:
            return f"Error al guardar en dict: {str(e)}"
    
    def convertir_a_dict(self):
        clientes_dict = []
        i = 0
        while i < len(self.clientes):
            clientes_dict.append(self.clientes[i].mostrar_info())
            i = i + 1
        
        turnos_dict = []
        i = 0
        while i < len(self.turnos):
            turnos_dict.append(self.turnos[i].mostrar_info())
            i = i + 1
        
        return {
            "clientes": clientes_dict,
            "turnos": turnos_dict,
            "proximo_id_turno": self.proximo_id_turno,
            "proximo_id_cliente": self.proximo_id_cliente
        }
    
    def cargar_desde_dict(self):
        if not os.path.exists(self.archivo_dict):
            return "No existe archivo dict previo"
        
        try:
            with open(self.archivo_dict, 'r', encoding='utf-8') as archivo:
                datos_dict = json.load(archivo)
            
            self.clientes = []
            self.turnos = []
            
            i = 0
            while i < len(datos_dict["clientes"]):
                cliente_data = datos_dict["clientes"][i]
                nuevo_cliente = Cliente(
                    cliente_data["nombre"],
                    cliente_data["telefono"],
                    cliente_data["email"],
                    cliente_data["id_cliente"]
                )
                self.clientes.append(nuevo_cliente)
                i = i + 1
            
            i = 0
            while i < len(datos_dict["turnos"]):
                turno_data = datos_dict["turnos"][i]
                
                cliente_turno = None
                j = 0
                while j < len(self.clientes):
                    if self.clientes[j].id_cliente == turno_data["cliente"]["id_cliente"]:
                        cliente_turno = self.clientes[j]
                        break
                    j = j + 1
                
                if cliente_turno:
                    nuevo_turno = Turno(
                        cliente_turno,
                        turno_data["fecha"],
                        turno_data["hora"],
                        turno_data["servicio"],
                        turno_data["estado"],
                        turno_data["id_turno"]
                    )
                    self.turnos.append(nuevo_turno)
                
                i = i + 1
            
            self.proximo_id_turno = datos_dict["proximo_id_turno"]
            self.proximo_id_cliente = datos_dict["proximo_id_cliente"]
            
            return "Datos cargados exitosamente desde dict"
        
        except Exception as e:
            return f"Error al cargar desde dict: {str(e)}"

def main():
    gestor = GestorTurnos()
    print("Sistema de Gestión de Turnos para Peluquería")
    print("Datos cargados automáticamente desde CSV si existe")
    
    while True:
        print("\n" + "="*50)
        print("MENÚ PRINCIPAL")
        print("Pelados abstenerse")
        print("="*50)
        print("1. Registrar nuevo cliente")
        print("2. Solicitar turno")
        print("3. Listar turnos existentes")
        print("4. Modificar turno")
        print("5. Cancelar turno")
        print("6. Guardar datos en CSV")
        print("7. Guardar datos en archivo dict (JSON)")
        print("8. Cargar datos desde archivo dict (JSON)")
        print("9. Salir")
        
        opcion = input("\nSeleccione una opción (1-9): ").strip()
        
        if opcion == "1":
            print("\n--- REGISTRAR NUEVO CLIENTE ---")
            nombre = input("Nombre completo: ").strip()
            telefono = input("Teléfono: ").strip()
            email = input("Email: ").strip()
            
            resultado = gestor.registrar_cliente(nombre, telefono, email)
            print(resultado)
        
        elif opcion == "2":
            print("\n--- SOLICITAR TURNO ---")
            nombre = input("Nombre completo: ").strip()
            fecha = input("Fecha (DD-MM-AAAA): ").strip()
            hora = input("Hora (HH:MM): ").strip()
            
            gestor.mostrar_servicios()
            opcion_servicio = input("\nSeleccione el número del servicio: ").strip()
            
            servicio = gestor.obtener_servicio_por_numero(opcion_servicio)
            if not servicio:
                print("Error: Número de servicio no válido")
                continue
            
            resultado = gestor.solicitar_turno(nombre, fecha, hora, servicio)
            print(resultado)
        
        elif opcion == "3":
            print("\n--- LISTAR TURNOS ---")
            print("Filtros (dejar en blanco para ver todos):")
            filtro_cliente = input("Filtrar por cliente (nombre o email): ").strip()
            filtro_fecha = input("Filtrar por fecha (DD-MM-AAAA): ").strip()
            filtro_estado = input("Filtrar por estado: ").strip()
            
            filtro_cliente = filtro_cliente if filtro_cliente else None
            filtro_fecha = filtro_fecha if filtro_fecha else None
            filtro_estado = filtro_estado if filtro_estado else None
            
            turnos = gestor.listar_turnos(filtro_cliente, filtro_fecha, filtro_estado)
            
            if turnos:
                print(f"\nSe encontraron {len(turnos)} turno(s):")
                i = 0
                while i < len(turnos):
                    turno = turnos[i]
                    print(f"\n--- Turno {i+1} ---")
                    print(f"ID Turno: {turno['id_turno']}")
                    print(f"Cliente: {turno['cliente']['nombre']}")
                    print(f"Email: {turno['cliente']['email']}")
                    print(f"Teléfono: {turno['cliente']['telefono']}")
                    print(f"Fecha: {turno['fecha']} - Hora: {turno['hora']}")
                    print(f"Servicio: {turno['servicio']}")
                    print(f"Estado: {turno['estado']}")
                    i = i + 1
            else:
                print("aca no están (0.o)")
        
        elif opcion == "4":
            print("\n--- MODIFICAR TURNO ---")
            nombre_cliente = input("Nombre del cliente: ").strip()
            
            print("Dejar en blanco los campos que no desea modificar:")
            nueva_fecha = input("Nueva fecha (DD-MM-AAAA): ").strip()
            nueva_hora = input("Nueva hora (HH:MM): ").strip()
            
            gestor.mostrar_servicios()
            opcion_servicio = input("Nuevo servicio (dejar en blanco para no modificar): ").strip()
            
            nueva_fecha = nueva_fecha if nueva_fecha else None
            nueva_hora = nueva_hora if nueva_hora else None
            nuevo_servicio = None
            
            if opcion_servicio:
                nuevo_servicio = gestor.obtener_servicio_por_numero(opcion_servicio)
                if not nuevo_servicio:
                    print("Error: Número de servicio no válido")
                    continue
            
            resultado = gestor.modificar_turno_por_cliente(nombre_cliente, nueva_fecha, nueva_hora, nuevo_servicio)
            print(resultado)
        
        elif opcion == "5":
            print("\n--- CANCELAR TURNO ---")
            nombre_cliente = input("Nombre del cliente: ").strip()
            
            resultado = gestor.cancelar_turno_por_cliente(nombre_cliente)
            print(resultado)
        
        elif opcion == "6":
            resultado_turnos = gestor.guardar_turnos_en_csv()
            resultado_clientes = gestor.guardar_clientes_en_csv()
            print(f"\n{resultado_turnos}")
            print(f"{resultado_clientes}")
        
        elif opcion == "7":
            resultado = gestor.guardar_en_dict()
            print(f"\n{resultado}")
        
        elif opcion == "8":
            resultado = gestor.cargar_desde_dict()
            print(f"\n{resultado}")
        
        elif opcion == "9":
            print("\n¡Gracias por usar el sistema de gestión de turnos!")
            print("¡Hasta pronto!")
            break
        
        else:
            print("\nOpción no válida. Por favor, seleccione una opción del 1 al 9.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    main()