# Sistema de Inventario

Sistema de inventario para proyecto final del curso de Lenguajes de Programación.

## Requisitos

- Python 3.10+
- PostgreSQL 14+
- Node.js 18+ (requerido por Reflex)

## Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/xGunTrr/Sistema-de-Inventario.git
cd Sistema-de-Inventario
```

### 2. Crear y activar entorno virtual

**Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

**Linux / macOS:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar la base de datos

Crear una base de datos en PostgreSQL y ejecutar el script SQL:

```bash
# Crear la base de datos (desde psql o pgAdmin)
CREATE DATABASE RAPIMARKET;

# Importar el esquema
psql -U postgres -d RAPIMARKET -f database_full.sql
```

### 5. Configurar variables de entorno

Copiar el archivo `.env.example` y completar con tus credenciales:

**Raíz del proyecto** (`.env`):
```bash
cp .env.example .env
```

```
__DATABASE_URL__="postgresql://USUARIO:CONTRASENA@localhost:5432/NOMBRE_DB"
```

**Dentro de `app/`** (`app/.env`):
```bash
cp app/.env.example app/.env
```

```
__DATABASE_URL__="postgresql://USUARIO:CONTRASENA@localhost:5432/NOMBRE_DB"
```

> Ambos archivos `.env` deben tener la misma URL de conexión.

### Variables de entorno

| Variable | Descripción |
|---|---|
| `__DATABASE_URL__` | URL de conexión a PostgreSQL con formato `postgresql://user:password@host:port/dbname` |

## Ejecutar el proyecto

```bash
uv run reflex run
```

La aplicación estará disponible en `http://localhost:3000`.

## Estructura del proyecto

```
Sistema-de-Inventario/
├── app/
│   ├── api/            # Endpoints FastAPI y schemas Pydantic
│   ├── components/     # Componentes reutilizables (layout, sidebar)
│   ├── pages/          # Páginas de la aplicación
│   ├── states/         # Estados de Reflex (data_state, auth_state)
│   ├── app.py          # Configuración de rutas y arranque de la app
│   └── .env            # Variables de entorno para la app
├── assets/             # Imágenes y recursos estáticos
├── database_full.sql   # Script SQL con el esquema completo
├── requirements.txt    # Dependencias de Python
├── rxconfig.py         # Configuración de Reflex
└── .env                # Variables de entorno en la raíz
```

## Módulos

| Módulo | Ruta | Descripción |
|---|---|---|
| Dashboard | `/dashboard` | Resumen general y estadísticas |
| Productos | `/productos` | Catálogo de productos |
| Proveedores | `/proveedores` | Gestión de proveedores |
| Clientes | `/clientes` | Gestión de clientes |
| Pedidos | `/pedidos` | Pedidos a proveedores |
| Entregas | `/entregas` | Entregas a clientes |
| Ubicaciones | `/ubicaciones` | Ubicaciones geográficas |
| Almacenes | `/almacenes` | Gestión de almacenes |
| Inventario | `/inventario` | Stock por almacén |
| Transferencias | `/transferencias` | Transferencias entre almacenes |
