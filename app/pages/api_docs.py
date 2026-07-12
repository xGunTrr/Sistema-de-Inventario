import reflex as rx
from app.components.layout import authenticated_layout


ENDPOINTS: list[dict[str, str]] = [
    {
        "method": "GET",
        "path": "/api/status",
        "desc": "Estado del API y conteos",
    },
    {"method": "GET", "path": "/api/products", "desc": "Listar productos"},
    {
        "method": "GET",
        "path": "/api/products/{id}",
        "desc": "Obtener un producto",
    },
    {"method": "POST", "path": "/api/products", "desc": "Crear producto"},
    {
        "method": "PUT",
        "path": "/api/products/{id}",
        "desc": "Actualizar producto",
    },
    {
        "method": "DELETE",
        "path": "/api/products/{id}",
        "desc": "Eliminar producto",
    },
    {"method": "GET", "path": "/api/types", "desc": "Listar tipos"},
    {"method": "POST", "path": "/api/types", "desc": "Crear tipo"},
    {"method": "DELETE", "path": "/api/types/{id}", "desc": "Eliminar tipo"},
    {"method": "GET", "path": "/api/suppliers", "desc": "Listar proveedores"},
    {"method": "POST", "path": "/api/suppliers", "desc": "Crear proveedor"},
    {
        "method": "DELETE",
        "path": "/api/suppliers/{id}",
        "desc": "Eliminar proveedor",
    },
]


def method_badge(method: str) -> rx.Component:
    return rx.el.span(
        method,
        class_name=rx.match(
            method,
            (
                "GET",
                "text-xs font-semibold text-blue-700 bg-blue-50 px-2 py-1 rounded w-16 text-center",
            ),
            (
                "POST",
                "text-xs font-semibold text-emerald-700 bg-emerald-50 px-2 py-1 rounded w-16 text-center",
            ),
            (
                "PUT",
                "text-xs font-semibold text-amber-700 bg-amber-50 px-2 py-1 rounded w-16 text-center",
            ),
            (
                "DELETE",
                "text-xs font-semibold text-red-700 bg-red-50 px-2 py-1 rounded w-16 text-center",
            ),
            "text-xs font-semibold text-gray-700 bg-gray-50 px-2 py-1 rounded w-16 text-center",
        ),
    )


def endpoint_row(e: dict[str, str]) -> rx.Component:
    return rx.el.div(
        method_badge(e["method"]),
        rx.el.code(
            e["path"],
            class_name="text-sm font-mono text-gray-900 bg-gray-50 px-2 py-1 rounded border border-gray-200",
        ),
        rx.el.p(e["desc"], class_name="text-sm text-gray-600 flex-1"),
        class_name="flex items-center gap-3 py-3 border-b border-gray-100 last:border-0 flex-wrap",
    )


def api_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("code", class_name="h-4 w-4 text-blue-600"),
                    class_name="h-8 w-8 rounded-lg bg-blue-50 flex items-center justify-center",
                ),
                rx.el.div(
                    rx.el.h3(
                        "API interna disponible",
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.p(
                        "Endpoints REST para integrar el inventario con otras herramientas.",
                        class_name="text-xs text-gray-500 mt-0.5",
                    ),
                ),
                class_name="flex items-start gap-3 mb-4",
            ),
            rx.el.div(
                rx.foreach(ENDPOINTS, endpoint_row),
                class_name="mt-2",
            ),
            class_name="bg-white border border-gray-200 rounded-xl p-5",
        ),
        rx.el.div(
            rx.el.h3(
                "Ejemplo de uso",
                class_name="text-sm font-semibold text-gray-900 mb-3",
            ),
            rx.el.pre(
                rx.el.code(
                    "# Listar productos\ncurl http://localhost:8000/api/products\n\n"
                    "# Crear producto\ncurl -X POST http://localhost:8000/api/products \\\n"
                    "  -H 'Content-Type: application/json' \\\n"
                    '  -d \'{"name":"Nuevo","sku":"NV-001","type":"Electrónica",'
                    '"supplier":"TechCorp","stock":10,"min_stock":2,"price":99.99}\'',
                    class_name="text-xs font-mono text-gray-800 leading-relaxed",
                ),
                class_name="bg-gray-50 border border-gray-200 rounded-lg p-4 overflow-x-auto",
            ),
            class_name="bg-white border border-gray-200 rounded-xl p-5 mt-4",
        ),
    )


def api_page() -> rx.Component:
    return authenticated_layout(
        api_content(),
        title="API interna",
        subtitle="Endpoints REST disponibles para tu inventario",
    )
