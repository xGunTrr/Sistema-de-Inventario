import reflex as rx
from app.components.layout import authenticated_layout
from app.states.data_state import DataState


def metric_card(
    icon: str,
    label: str,
    value: rx.Var | str,
    color: str = "text-blue-600",
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon, class_name=f"h-4 w-4 {color}"),
            class_name=f"h-8 w-8 rounded-lg flex items-center justify-center {color.replace('text-', 'bg-').replace('-600', '-50')}",
        ),
        rx.el.p(label, class_name="text-sm text-gray-500 mb-1"),
        rx.el.p(value, class_name="text-2xl font-semibold text-gray-900"),
        class_name="bg-white border border-gray-200 rounded-xl p-5 hover:border-gray-300 transition-colors",
    )


def quick_action(
    icon: str, label: str, desc: str, href: str, color: str
) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name=f"h-4 w-4 {color}"),
            class_name=f"h-8 w-8 rounded-lg flex items-center justify-center shrink-0 {color.replace('text-', 'bg-').replace('-600', '-50')}",
        ),
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-gray-900"),
            rx.el.p(desc, class_name="text-xs text-gray-500"),
        ),
        rx.icon("chevron-right", class_name="h-4 w-4 text-gray-400 ml-auto"),
        href=href,
        class_name="flex items-center gap-3 bg-white border border-gray-200 rounded-xl p-4 hover:border-blue-300 hover:shadow-sm transition-all",
    )


def entity_row(name: str, count: rx.Var | str, icon: str, href: str) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name="h-4 w-4 text-gray-400"),
            class_name="h-8 w-8 rounded-lg bg-gray-50 flex items-center justify-center shrink-0",
        ),
        rx.el.p(name, class_name="text-sm font-medium text-gray-900"),
        rx.el.p(
            count.to_string() + " registros",
            class_name="text-xs text-gray-500",
        ),
        rx.icon("chevron-right", class_name="h-4 w-4 text-gray-400 ml-auto"),
        href=href,
        class_name="flex items-center gap-3 py-3 border-b border-gray-100 last:border-0 hover:bg-gray-50 rounded-lg px-2 transition-colors",
    )


def dashboard_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            metric_card(
                "package",
                "Productos",
                DataState.total_productos.to_string(),
                "text-blue-600",
            ),
            metric_card(
                "truck",
                "Proveedores",
                DataState.total_proveedores.to_string(),
                "text-emerald-600",
            ),
            metric_card(
                "users",
                "Clientes",
                DataState.total_clientes.to_string(),
                "text-violet-600",
            ),
            metric_card(
                "warehouse",
                "Almacenes",
                DataState.total_almacenes.to_string(),
                "text-amber-600",
            ),
            class_name="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Acciones rápidas",
                    class_name="text-sm font-semibold text-gray-900 mb-3",
                ),
                rx.el.div(
                    quick_action("package-plus", "Nuevo producto", "Añadir al catálogo", "/productos", "text-blue-600"),
                    quick_action("shopping-cart", "Nuevo pedido", "Pedir a proveedor", "/pedidos", "text-emerald-600"),
                    quick_action("map-pin", "Nueva ubicación", "Registrar ubicación", "/ubicaciones", "text-violet-600"),
                    quick_action("arrow-left-right", "Transferencia", "Mover entre almacenes", "/transferencias", "text-amber-600"),
                    class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3",
                ),
                class_name="bg-white border border-gray-200 rounded-xl p-5 mb-6",
            ),
        ),
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Resumen del sistema",
                    class_name="text-sm font-semibold text-gray-900 mb-3",
                ),
                rx.el.div(
                    entity_row("Productos", DataState.total_productos, "package", "/productos"),
                    entity_row("Proveedores", DataState.total_proveedores, "truck", "/proveedores"),
                    entity_row("Clientes", DataState.total_clientes, "users", "/clientes"),
                    entity_row("Pedidos", DataState.total_pedidos, "shopping-cart", "/pedidos"),
                    entity_row("Entregas", DataState.total_entregas, "truck", "/entregas"),
                    entity_row("Ubicaciones", DataState.total_ubicaciones, "map-pin", "/ubicaciones"),
                    entity_row("Almacenes", DataState.total_almacenes, "warehouse", "/almacenes"),
                    entity_row("Inventario", DataState.total_inventarios, "database", "/inventario"),
                    entity_row("Transferencias", DataState.total_transferencias, "arrow-left-right", "/transferencias"),
                    class_name="divide-y divide-gray-100",
                ),
                class_name="bg-white border border-gray-200 rounded-xl p-5",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-1 gap-4",
        ),
    )


def dashboard_page(on_load=DataState.load_data) -> rx.Component:
    return authenticated_layout(
        dashboard_content(),
        title="Dashboard",
        subtitle="Vista general de tu inventario",
    )
