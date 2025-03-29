import json
from pathlib import Path

def cargar_configuracion():
    config_path = Path(__file__).parent.parent / "config" / "db_config.json"
    with open(config_path, 'r') as f:
        return json.load(f)

def obtener_esquema_tabla(nombre_tabla):
    config = cargar_configuracion()
    return config['tables'].get(nombre_tabla, None)

def generar_sql_creacion_tabla(nombre_tabla):
    esquema = obtener_esquema_tabla(nombre_tabla)
    if not esquema:
        return None
    
    campos = []
    for nombre_campo, propiedades in esquema['fields'].items():
        campo_sql = f"{nombre_campo} {propiedades['type']}"
        if 'constraints' in propiedades:
            campo_sql += f" {propiedades['constraints']}"
        campos.append(campo_sql)
    
    if 'foreign_keys' in esquema:
        campos.extend(esquema['foreign_keys'])
    
    return f"CREATE TABLE {nombre_tabla} ({', '.join(campos)})"