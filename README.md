# Sistema de Inventario
SIstema de inventario para proyecto final del curso  de Lenguajes de Programación.

## Requisistos
- Python 3.10+
- Postgresql

# Configuración
1. Clonar el repositorio
```commandline
git clone https://github.com/xGunTrr/Sistema-de-Inventario.git
cd Sistema-de-Inventario
```
2. Creamos y activamos un entorno virtual
- Windows
```commandline
python -m venv .venv
venv\Scripts\activate.bat

```
- Linux
```commandline
python3 -m venv .venv
source .venv/bin/activate
```
3. Instalamos los requerimientos
```commandline
pip install -r requirements.txt
```
## Ejecutamos el proyecto
1. Duplica el archivo `.env.example` y cambiale el nombre a `.env`, finalmente rellenala con tus credenciales:
```commandline
# Example
__DATABASE_URL__="postgresql://user:password@server:5432/database_name"
```
2. Ejecutamos el proyecto
```commandline
uv run reflex run
```
