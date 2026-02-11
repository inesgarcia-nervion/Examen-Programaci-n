import multiprocessing
import os

# Asegurarnos de que los ficheros se crean en la misma carpeta que el script
CARPETA = os.path.dirname(os.path.abspath(__file__))

# Proceso 1: Lee el fichero salarios.txt y envía al Proceso 2 las líneas del departamento indicado
def proceso1(departamento, pipe1a2):
    fichero_salarios = os.path.join(CARPETA, "salarios.txt")
    
    # Leer el fichero línea por línea
    with open(fichero_salarios, "r", encoding="utf-8") as f:
        for linea in f:
            # Separaramos usando ';' para obtener los campos
            campos = linea.strip().split(";")
            
            # Comprobar que tenemos los 4 campos necesarios: Nombre, Apellido, Salario, Departamento
            if len(campos) == 4:
                nombre, apellido, salario, depto = campos
                
                # Si el departamento coincide, enviamos la línea SIN el departamento
                if depto == departamento:
                    # Enviamos: Nombre;Apellido;Salario usando send del pipe
                    linea_sin_depto = f"{nombre};{apellido};{salario}"
                    pipe1a2.send(linea_sin_depto)
    
    # Indicar que ya terminamos de enviar datos
    pipe1a2.send(None)
    pipe1a2.close()


# Proceso 2: Recibe líneas del Proceso 1 y envía al Proceso 3 solo las que cumplan con el salario mínimo
def proceso2(salario_minimo, pipe1a2, pipe2a3):
    while True:
        # Recibir línea del Proceso 1
        linea = pipe1a2.recv()
        
        # Si recibimos None, significa que el Proceso 1 terminó
        if linea is None:
            break
        
        # Separaramos usando ';' para obtener el salario
        campos = linea.split(";")
        nombre, apellido, salario = campos
        
        # Comprobar si el salario es mayor o igual al mínimo
        if float(salario) >= salario_minimo:
            # Enviar la línea tal cual al Proceso 3
            pipe2a3.send(linea)
    
    # Indicar que ya terminamos
    pipe2a3.send(None)
    pipe2a3.close()


# Proceso 3: Recibe líneas del Proceso 2 y las escribe en empleados.txt con el formato solicitado (Apellido Nombre, Salario)
def proceso3(pipe2a3):
    fichero_empleados = os.path.join(CARPETA, "empleados.txt")
    
    # Abrir el fichero para escribir
    with open(fichero_empleados, "w", encoding="utf-8") as f:
        while True:
            # Recibir línea del Proceso 2 usando recv del pipe
            linea = pipe2a3.recv()
            
            # Si recibimos None, significa que el Proceso 2 terminó
            if linea is None:
                break
            
            # Separaramos usando ';'
            campos = linea.split(";")
            nombre, apellido, salario = campos
            
            # Escribir en el formato: Apellido Nombre, Salario
            f.write(f"{apellido} {nombre}, {salario}\n")


if __name__ == "__main__":
    # Pedir al usuario el departamento y el salario mínimo
    departamento = input("Introduce el nombre del departamento: ")
    salario_minimo = float(input("Introduce el salario mínimo: "))
    
    # Crear pipes para comunicar los procesos
    # Pipe entre Proceso 1 y Proceso 2
    pipe1a2_recv, pipe1a2_send = multiprocessing.Pipe(duplex=False)
    
    # Pipe entre Proceso 2 y Proceso 3
    pipe2a3_recv, pipe2a3_send = multiprocessing.Pipe(duplex=False)
    
    # Crear los procesos CON LOS PIPES CORRECTOS
    p1 = multiprocessing.Process(target=proceso1, args=(departamento, pipe1a2_send))
    p2 = multiprocessing.Process(target=proceso2, args=(salario_minimo, pipe1a2_recv, pipe2a3_send))
    p3 = multiprocessing.Process(target=proceso3, args=(pipe2a3_recv,))
    
    # Iniciar los procesos en orden
    p1.start()
    p2.start()
    p3.start()
    
    # Esperar a que terminen todos
    p1.join()
    p2.join()
    p3.join()
    
    print(f"Proceso completado")