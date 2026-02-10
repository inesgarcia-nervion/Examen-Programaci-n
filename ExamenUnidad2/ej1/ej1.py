import multiprocessing
import random
import os

# Esta linea de codigo es para asegurarnos de que los ficheros se crean en la misma carpeta que el script
CARPETA = os.path.dirname(os.path.abspath(__file__))

# Proceso 1: Genera 24 temperaturas aleatorias y las guarda en un fichero
def proceso1(dia):
    # Nombre del fichero con formato DD-12.txt (diciembre)
    nombre_fichero = os.path.join(CARPETA, f"{dia:02d}-12.txt")
    
    # Generar 24 temperaturas (una por hora) entre 0 y 20 con 2 decimales
    with open(nombre_fichero, "w") as f:
        for _ in range(24):
            temperatura = round(random.uniform(0, 20), 2)
            f.write(f"{temperatura}\n")


# Proceso 2: Lee temperaturas de un fichero y escribe la máxima en maximas.txt
def proceso2(dia):
    nombre_fichero = os.path.join(CARPETA, f"{dia:02d}-12.txt")
    fecha = f"{dia:02d}-12"
    
    # Leer todas las temperaturas del fichero
    with open(nombre_fichero, "r") as f:
        temperaturas = [float(linea.strip()) for linea in f]
    
    # Escribir fecha y temperatura máxima separadas por ':'
    maxima = max(temperaturas)
    with open(os.path.join(CARPETA, "maximas.txt"), "a") as f:
        f.write(f"{fecha}:{maxima}\n")


# Proceso 3: Lee temperaturas de un fichero y escribe la mínima en minimas.txt
def proceso3(dia):
    nombre_fichero = os.path.join(CARPETA, f"{dia:02d}-12.txt")
    fecha = f"{dia:02d}-12"
    
    # Leer todas las temperaturas del fichero
    with open(nombre_fichero, "r") as f:
        temperaturas = [float(linea.strip()) for linea in f]
    
    # Escribir fecha y temperatura mínima separadas por ':'
    minima = min(temperaturas)
    with open(os.path.join(CARPETA, "minimas.txt"), "a") as f:
        f.write(f"{fecha}:{minima}\n")



if __name__ == "__main__":

    # Se crean 31 ficheros DD-12.txt con 24 temperaturas cada uno (aleatorias entre 0 y 20 con 2 decimales)
    procesos_generacion = []
    for dia in range(1, 32):
        p = multiprocessing.Process(target=proceso1, args=(dia,))
        procesos_generacion.append(p)
        p.start()
    
    # Esperar a que terminen antes de leer los ficheros
    for p in procesos_generacion:
        p.join()
    print("Se han generado los 31 ficheros de temperaturas.")
    
    # Lanzamos simultáneamente Proceso2 y Proceso3. Leen los mismos ficheros pero escriben en ficheros distintos
    procesos_maxmin = []
    
    # 31 procesos para máximas
    for dia in range(1, 32):
        p = multiprocessing.Process(target=proceso2, args=(dia,))
        procesos_maxmin.append(p)
        p.start()
    
    # 31 procesos para mínimas
    for dia in range(1, 32):
        p = multiprocessing.Process(target=proceso3, args=(dia,))
        procesos_maxmin.append(p)
        p.start()
    
    # Esperar a que todos terminen
    for p in procesos_maxmin:
        p.join()
    print("Se han generado los ficheros maximas.txt y minimas.txt.")
