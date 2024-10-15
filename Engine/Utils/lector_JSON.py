import json

def extractData(path:str):
    try:
        with open(path, 'r', encoding='utf-8') as archivo:
            articulos = json.load(archivo)

        id = [item["Id"] for item in articulos]
        contenido = [item["Contenido"].lower() for item in articulos]
        meta = [item["Metadato"] for item in articulos]
        return id, contenido, meta
    except FileNotFoundError:
        print(f"El archivo '{path}' no se encontró.")
        return None, None, None
    except json.JSONDecodeError:
        print(f"El archivo '{path}' no parece ser un archivo JSON válido.")
        return None, None, None
    except Exception as e:
        print(f"Se produjo un error inesperado: {e}")
        return None, None, None