import reflex as rx
from app.components.layout import authenticated_layout
from app.states.data_state import DataState


TYPE_COLORS = ["#2563eb", "#7c3aed", "#10b981", "#f59e0b", "#ef4444"]


def metric_card(
    icon: str,
    label: str,
    value: rx.Var | str,
    change: str,
    positive: bool = True,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-4 w-4 text-blue-600"),
                class_name="h-8 w-8 rounded-lg bg-blue-50 flex items-center justify-center",
            ),
            rx.el.span(
                change,
                class_name=rx.cond(
                    positive,
                    "text-xs font-medium text-green-700 bg-green-50 px-2 py-0.5 rounded-full",
                    "text-xs font-medium text-red-700 bg-red-50 px-2 py-0.5 rounded-full",
                ),
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.p(label, class_name="text-sm text-gray-500 mb-1"),
        rx.el.p(value, class_name="text-2xl font-semibold text-gray-900"),
        class_name="bg-white border border-gray-200 rounded-xl p-5 hover:border-gray-300 transition-colors",
    )


def low_stock_row(product: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("triangle-alert", class_name="h-4 w-4 text-amber-600"),
                class_name="h-8 w-8 rounded-lg bg-amber-50 flex items-center justify-center shrink-0",
            ),
            rx.el.div(
                rx.el.p(
                    product["name"],
                    class_name="text-sm font-medium text-gray-900",
                ),
                rx.el.p(
                    f"SKU: {product['sku']} · {product['type']}",
                    class_name="text-xs text-gray-500",
                ),
                class_name="min-w-0",
            ),
            class_name="flex items-center gap-3 min-w-0",
        ),
        rx.el.div(
            rx.el.p(
                product["stock"].to_string()
                + " / "
                + product["min_stock"].to_string(),
                class_name="text-sm font-semibold text-red-600",
            ),
            rx.el.p("stock actual / mín", class_name="text-xs text-gray-400"),
            class_name="text-right shrink-0",
        ),
        class_name="flex items-center justify-between py-3 border-b border-gray-100 last:border-0",
    )


def supplier_row(supplier: dict, index: int) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    supplier["name"][0],
                    class_name="text-sm font-semibold text-blue-700",
                ),
                class_name="h-9 w-9 rounded-lg bg-blue-50 flex items-center justify-center shrink-0",
            ),
            rx.el.div(
                rx.el.p(
                    supplier["name"],
                    class_name="text-sm font-medium text-gray-900",
                ),
                rx.el.p(
                    supplier["contact"], class_name="text-xs text-gray-500"
                ),
                class_name="min-w-0",
            ),
            class_name="flex items-center gap-3 min-w-0",
        ),
        rx.el.div(
            rx.el.p(
                supplier["product_count"].to_string() + " productos",
                class_name="text-sm font-medium text-gray-900",
            ),
            class_name="text-right shrink-0",
        ),
        class_name="flex items-center justify-between py-3 border-b border-gray-100 last:border-0",
    )


def activity_row(activity: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(activity["icon"], class_name="h-4 w-4 text-gray-600"),
            class_name="h-8 w-8 rounded-full bg-gray-100 flex items-center justify-center shrink-0",
        ),
        rx.el.div(
            rx.el.p(
                rx.el.span(
                    activity["action"], class_name="font-medium text-gray-900"
                ),
                rx.el.span(" · ", class_name="text-gray-400"),
                rx.el.span(activity["entity"], class_name="text-gray-700"),
                class_name="text-sm",
            ),
            rx.el.p(
                activity["user"] + " · " + activity["time"],
                class_name="text-xs text-gray-500 mt-0.5",
            ),
            class_name="min-w-0 flex-1",
        ),
        class_name="flex items-start gap-3 py-3 border-b border-gray-100 last:border-0",
    )


def type_distribution_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Distribución por tipo",
                    class_name="text-sm font-semibold text-gray-900",
                ),
                rx.el.p(
                    "Productos agrupados por categoría",
                    class_name="text-xs text-gray-500 mt-0.5",
                ),
            ),
            rx.icon("chart-pie", class_name="h-4 w-4 text-gray-400"),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.recharts.pie_chart(
            rx.recharts.graphing_tooltip(),
            rx.recharts.pie(
                data=DataState.type_distribution,
                data_key="value",
                name_key="name",
                inner_radius="55%",
                outer_radius="80%",
                fill="#2563eb",
                stroke="#ffffff",
                stroke_width=2,
            ),
            width="100%",
            height=220,
        ),
        rx.el.div(
            rx.foreach(
                DataState.product_types,
                lambda t, i: rx.el.div(
                    rx.el.div(
                        class_name=rx.match(
                            i,
                            (0, "h-2.5 w-2.5 rounded-full bg-blue-600"),
                            (1, "h-2.5 w-2.5 rounded-full bg-violet-600"),
                            (2, "h-2.5 w-2.5 rounded-full bg-emerald-500"),
                            (3, "h-2.5 w-2.5 rounded-full bg-amber-500"),
                            "h-2.5 w-2.5 rounded-full bg-red-500",
                        ),
                    ),
                    rx.el.p(
                        t["name"], class_name="text-xs text-gray-600 flex-1"
                    ),
                    rx.el.p(
                        t["product_count"],
                        class_name="text-xs font-medium text-gray-900",
                    ),
                    class_name="flex items-center gap-2",
                ),
            ),
            class_name="grid grid-cols-2 gap-2 mt-4",
        ),
        class_name="bg-white border border-gray-200 rounded-xl p-5",
    )


def quick_action(
    icon: str, label: str, desc: str, href: str, color: str
) -> rx.Component:
    return rx.el.a(
        rx.el.div(
            rx.icon(icon, class_name=f"h-4 w-4 {color}"),
            class_name=f"h-8 w-8 rounded-lg flex items-center justify-center shrink-0 "
            + color.replace("text-", "bg-").replace("-600", "-50"),
        ),
        rx.el.div(
            rx.el.p(label, class_name="text-sm font-medium text-gray-900"),
            rx.el.p(desc, class_name="text-xs text-gray-500"),
        ),
        rx.icon("chevron-right", class_name="h-4 w-4 text-gray-400 ml-auto"),
        href=href,
        class_name="flex items-center gap-3 bg-white border border-gray-200 rounded-xl p-4 hover:border-blue-300 hover:shadow-sm transition-all",
    )


def quick_actions_section() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Acciones rápidas",
            class_name="text-sm font-semibold text-gray-900 mb-3",
        ),
        rx.el.div(
            quick_action(
                "package-plus",
                "Nuevo producto",
                "Añadir al catálogo",
                "/productos",
                "text-blue-600",
            ),
            quick_action(
                "tag",
                "Nuevo tipo",
                "Categorizar productos",
                "/tipos",
                "text-violet-600",
            ),
            quick_action(
                "truck",
                "Nuevo proveedor",
                "Registrar contacto",
                "/proveedores",
                "text-emerald-600",
            ),
            quick_action(
                "code",
                "Explorar API",
                "Endpoints REST",
                "/api",
                "text-amber-600",
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3",
        ),
        class_name="mb-6",
    )


def dashboard_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            metric_card(
                "package",
                "Total productos",
                DataState.total_products.to_string(),
                "+12%",
                True,
            ),
            metric_card(
                "tag",
                "Tipos de producto",
                DataState.total_types.to_string(),
                "+2",
                True,
            ),
            metric_card(
                "truck",
                "Proveedores",
                DataState.total_suppliers.to_string(),
                "+1",
                True,
            ),
            metric_card(
                "triangle-alert",
                "Stock crítico",
                DataState.low_stock_count.to_string(),
                "-3",
                False,
            ),
            class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6",
        ),
        quick_actions_section(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Alertas de stock",
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.p(
                            "Productos por debajo del mínimo",
                            class_name="text-xs text-gray-500 mt-0.5",
                        ),
                    ),
                    rx.el.span(
                        DataState.low_stock_count.to_string() + " alertas",
                        class_name="text-xs font-medium text-red-700 bg-red-50 px-2 py-1 rounded-full",
                    ),
                    class_name="flex items-center justify-between mb-2",
                ),
                rx.el.div(
                    rx.cond(
                        DataState.low_stock_count > 0,
                        rx.el.div(
                            rx.foreach(
                                DataState.low_stock_products, low_stock_row
                            ),
                            class_name="mt-2",
                        ),
                        rx.el.div(
                            rx.icon(
                                "circle-check",
                                class_name="h-8 w-8 text-emerald-500 mb-2",
                            ),
                            rx.el.p(
                                "Todo en orden",
                                class_name="text-sm font-medium text-gray-900",
                            ),
                            rx.el.p(
                                "Ningún producto por debajo del mínimo.",
                                class_name="text-xs text-gray-500 mt-1",
                            ),
                            class_name="flex flex-col items-center justify-center py-8 text-center",
                        ),
                    ),
                    class_name="mt-2",
                ),
                class_name="bg-white border border-gray-200 rounded-xl p-5 lg:col-span-2",
            ),
            type_distribution_chart(),
            class_name="grid grid-cols-1 lg:grid-cols-3 gap-4 mb-6",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Proveedores destacados",
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.p(
                            "Con mayor cantidad de productos",
                            class_name="text-xs text-gray-500 mt-0.5",
                        ),
                    ),
                    rx.el.a(
                        "Ver todos",
                        href="/proveedores",
                        class_name="text-xs font-medium text-blue-600 hover:text-blue-700",
                    ),
                    class_name="flex items-center justify-between mb-2",
                ),
                rx.el.div(
                    rx.foreach(
                        DataState.top_suppliers, lambda s, i: supplier_row(s, i)
                    ),
                    class_name="mt-2",
                ),
                class_name="bg-white border border-gray-200 rounded-xl p-5",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.h3(
                            "Actividad reciente",
                            class_name="text-sm font-semibold text-gray-900",
                        ),
                        rx.el.p(
                            "Últimos cambios en el sistema",
                            class_name="text-xs text-gray-500 mt-0.5",
                        ),
                    ),
                    rx.icon("activity", class_name="h-4 w-4 text-gray-400"),
                    class_name="flex items-center justify-between mb-2",
                ),
                rx.el.div(
                    rx.foreach(DataState.activities, activity_row),
                    class_name="mt-2",
                ),
                class_name="bg-white border border-gray-200 rounded-xl p-5",
            ),
            class_name="grid grid-cols-1 lg:grid-cols-2 gap-4",
        ),
    )


def dashboard_page() -> rx.Component:
    return authenticated_layout(
        dashboard_content(),
        title="Dashboard",
        subtitle="Vista general de tu inventario y actividad reciente",
    )
