import json
import os

# Ruta del archivo JSON
FILE_PATH = 'data.json'  # Cambia la ruta si prefieres que esté en una carpeta específica

# Cargar datos del archivo JSON o inicializar con valores predeterminados
def load_data():
    if os.path.exists(FILE_PATH):
        # Si el archivo existe, cargar los datos existentes
        with open(FILE_PATH, 'r') as file:
            data = json.load(file)
    else:
        # Si el archivo no existe, iniciar con valores predeterminados o vacíos
        data = {
            "scoreboard": [],
            "coins": 0,
            "unlocked_characters": []
        }
        save_data(data)  # Guardar los datos iniciales en un archivo nuevo
    return data

# Guardar datos en el archivo JSON
def save_data(data):
    with open(FILE_PATH, 'w') as file:
        json.dump(data, file, indent=4)
