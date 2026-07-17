import reflex as rx
from app.pages.login import login_page
from app.pages.dashboard import dashboard_page
from app.pages.productos import productos_page
from app.pages.proveedores import proveedores_page
from app.pages.clientes import clientes_page
from app.pages.pedidos import pedidos_page
from app.pages.entregas import entregas_page
from app.pages.ubicaciones import ubicaciones_page
from app.pages.almacenes import almacenes_page
from app.pages.inventario import inventario_page
from app.pages.transferencias import transferencias_page
from app.pages.placeholder import configuracion_page
from app.states.auth_state import AuthState
from app.api.endpoints import create_api_router
from app.states.data_state import DataState

def index() -> rx.Component:
    return login_page()

api_app = create_api_router()

app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap",
            rel="stylesheet",
        ),
    ],
    stylesheets=[],
    api_transformer=api_app,
)

app.add_page(index, route="/")
app.add_page(dashboard_page, route="/dashboard", on_load=[AuthState.check_auth, DataState.load_data])
app.add_page(productos_page, route="/productos", on_load=[AuthState.check_auth, DataState.load_data])
app.add_page(proveedores_page, route="/proveedores", on_load=[AuthState.check_auth, DataState.load_data])
app.add_page(clientes_page, route="/clientes", on_load=[AuthState.check_auth, DataState.load_data])
app.add_page(pedidos_page, route="/pedidos", on_load=[AuthState.check_auth, DataState.load_data])
app.add_page(entregas_page, route="/entregas", on_load=[AuthState.check_auth, DataState.load_data])
app.add_page(ubicaciones_page, route="/ubicaciones", on_load=[AuthState.check_auth, DataState.load_data])
app.add_page(almacenes_page, route="/almacenes", on_load=[AuthState.check_auth, DataState.load_data])
app.add_page(inventario_page, route="/inventario", on_load=[AuthState.check_auth, DataState.load_data])
app.add_page(transferencias_page, route="/transferencias", on_load=[AuthState.check_auth, DataState.load_data])
app.add_page(configuracion_page, route="/configuracion", on_load=[AuthState.check_auth, DataState.load_data])
