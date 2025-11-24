"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel


import pandas as pd
import re

def pregunta_01():
    with open("files/input/clusters_report.txt", encoding="utf-8") as f:
        lines = f.readlines()

    data = []
    cluster = None
    cantidad = None
    porcentaje = None
    palabras = ""

    for line in lines[1:]:  
        line = line.rstrip()
        if not line:  
            continue

        # Detectar inicio de un cluster: línea que empieza con un número
        match = re.match(r"\s*(\d+)\s+(\d+)\s+([\d,]+)\s*%\s*(.*)", line)
        if match:
            # Guardar cluster anterior si existe
            if cluster is not None:
                # Limpiar texto de palabras clave
                palabras = re.sub(r"\s+", " ", palabras)              
                palabras = re.sub(r"\s*,\s*", ", ", palabras).strip()  
                palabras = palabras.rstrip(".")                        
                data.append({
                    "cluster": cluster,
                    "cantidad_de_palabras_clave": cantidad,
                    "porcentaje_de_palabras_clave": float(str(porcentaje).replace(",", ".")),
                    "principales_palabras_clave": palabras
                })

            # Extraer datos del nuevo cluster
            cluster = int(match.group(1))
            cantidad = int(match.group(2))
            porcentaje = match.group(3)
            palabras = match.group(4)  
        else:
            palabras += " " + line.strip()

    # Guardar el último cluster
    if cluster is not None:
        palabras = re.sub(r"\s+", " ", palabras)
        palabras = re.sub(r"\s*,\s*", ", ", palabras).strip()
        palabras = palabras.rstrip(".")
        data.append({
            "cluster": cluster,
            "cantidad_de_palabras_clave": cantidad,
            "porcentaje_de_palabras_clave": float(str(porcentaje).replace(",", ".")),
            "principales_palabras_clave": palabras
        })

    # Crear DataFrame
    df = pd.DataFrame(data)
    df = df[["cluster", "cantidad_de_palabras_clave", "porcentaje_de_palabras_clave", "principales_palabras_clave"]]

    return df

