import reflex as rx
from app.components.layout import authenticated_layout
from app.states.data_state import DataState, Entrega, DetalleEntrega


def stat_pill(label: str, value: rx.Var | str, color: str) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="text-xs text-gray-500"),
        rx.el.p(value, class_name=f"text-lg font-semibold {color} mt-1"),
        class_name="bg-white border border-gray-200 rounded-xl px-4 py-3",
    )


def toolbar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Buscar por N\u00b0 o cliente...",
                    default_value=DataState.entrega_search,
                    on_change=DataState.set_entrega_search.debounce(300),
                    class_name="pl-9 pr-3 py-2 bg-white border border-gray-200 rounded-lg text-sm w-full md:w-72 focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                    color="black",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("Todos", value="Todos"),
                    rx.foreach(
                        DataState.cliente_filter_options,
                        lambda o: rx.el.option(o["label"], value=o["value"]),
                    ),
                    default_value="Todos",
                    class_name="pl-3 pr-8 py-2 bg-white border border-gray-200 rounded-lg text-sm appearance-none focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                    color="black",
                ),
                rx.icon(
                    "chevron-down",
                    class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("Todos", value="Todos"),
                    rx.foreach(
                        DataState.pedido_filter_options,
                        lambda o: rx.el.option(o["label"], value=o["value"]),
                    ),
                    default_value="Todos",
                    class_name="pl-3 pr-8 py-2 bg-white border border-gray-200 rounded-lg text-sm appearance-none focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                    color="black",
                ),
                rx.icon(
                    "chevron-down",
                    class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                ),
                class_name="relative",
            ),
            rx.el.button(
                rx.icon("x", class_name="h-3.5 w-3.5"),
                "Limpiar",
                on_click=DataState.clear_entrega_filters,
                class_name="flex items-center gap-1.5 px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg transition-colors",
            ),
            class_name="flex flex-wrap items-center gap-2 flex-1",
        ),
        rx.el.button(
            rx.icon("plus", class_name="h-4 w-4"),
            "Nueva entrega",
            on_click=DataState.open_new_entrega,
            class_name="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors shrink-0",
        ),
        class_name="flex flex-col md:flex-row md:items-center gap-3 mb-4",
    )


def entrega_row(e: Entrega) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.p(
                "# " + e["IdEntrega"].to_string(),
                class_name="text-sm font-semibold text-gray-900",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(
                rx.cond(
                    e["cliente"],
                    e["cliente"]["NombreCliente"],
                    "Sin cliente",
                ),
                class_name="text-sm text-gray-700",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(
                "# " + e["IdPedido"].to_string(),
                class_name="text-sm text-gray-700",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(
                rx.cond(e["FechaVenta"], e["FechaVenta"], "\u2014"),
                class_name="text-sm text-gray-700",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(
                rx.cond(e["FechaEsperada"], e["FechaEsperada"], "\u2014"),
                class_name="text-sm text-gray-700",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.span(
                e["Estado"],
                class_name="text-xs font-medium px-2 py-1 rounded-full w-fit "
                + rx.cond(
                    e["Estado"] == "Pendiente",
                    "text-yellow-700 bg-yellow-50",
                    rx.cond(
                        e["Estado"] == "Preparando",
                        "text-indigo-700 bg-indigo-50",
                        rx.cond(
                            e["Estado"] == "En transito",
                            "text-blue-700 bg-blue-50",
                            rx.cond(
                                e["Estado"] == "Entregado",
                                "text-green-700 bg-green-50",
                                rx.cond(
                                    e["Estado"] == "No entregado",
                                    "text-orange-700 bg-orange-50",
                                    "text-red-700 bg-red-50",
                                ),
                            ),
                        ),
                    ),
                ),
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.span(
                e["detalles"].length().to_string() + " items",
                class_name="text-xs font-medium text-gray-600 bg-gray-100 px-2 py-1 rounded-full w-fit",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("eye", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_entrega_detail(e),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors",
                    title="Ver",
                ),
                rx.cond(
                    e["Estado"] == "Pendiente",
                    rx.el.button(
                        rx.icon("package", class_name="h-4 w-4"),
                        on_click=lambda: DataState.cambiar_estado_entrega(e, "Preparando"),
                        class_name="p-1.5 text-indigo-600 hover:text-indigo-700 hover:bg-indigo-50 rounded transition-colors",
                        title="Preparar",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    e["Estado"] == "Preparando",
                    rx.el.button(
                        rx.icon("truck", class_name="h-4 w-4"),
                        on_click=lambda: DataState.cambiar_estado_entrega(e, "En transito"),
                        class_name="p-1.5 text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded transition-colors",
                        title="Despachar",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    e["Estado"] == "En transito",
                    rx.el.button(
                        rx.el.div(
                            rx.icon("check-circle", class_name="h-4 w-4"),
                            class_name="flex items-center gap-1",
                        ),
                        on_click=lambda: DataState.cambiar_estado_entrega(e, "Entregado"),
                        class_name="p-1.5 text-emerald-600 hover:text-emerald-700 hover:bg-emerald-50 rounded transition-colors",
                        title="Entregado",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    e["Estado"] != "Entregado",
                    rx.cond(
                        e["Estado"] != "No entregado",
                        rx.cond(
                            e["Estado"] != "Cancelado",
                            rx.el.button(
                                rx.icon("x-circle", class_name="h-4 w-4"),
                                on_click=lambda: DataState.cambiar_estado_entrega(e, "Cancelado"),
                                class_name="p-1.5 text-red-500 hover:text-red-600 hover:bg-red-50 rounded transition-colors",
                                title="Cancelar",
                            ),
                            rx.fragment(),
                        ),
                        rx.fragment(),
                    ),
                    rx.fragment(),
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_delete_entrega(e),
                    class_name="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded transition-colors",
                    title="Eliminar",
                ),
                class_name="flex items-center gap-1 justify-end",
            ),
            class_name="px-4 py-3",
        ),
        class_name="border-b border-gray-100 hover:bg-gray-50 transition-colors",
    )


def empty_state() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("truck", class_name="h-6 w-6 text-gray-400"),
            class_name="h-12 w-12 rounded-xl bg-gray-100 flex items-center justify-center mb-4",
        ),
        rx.el.p(
            "No hay entregas que coincidan",
            class_name="text-sm font-medium text-gray-900 mb-1",
        ),
        rx.el.p(
            "Intenta ajustar los filtros o crea una entrega nueva.",
            class_name="text-xs text-gray-500",
        ),
        class_name="flex flex-col items-center justify-center py-16",
    )


def entregas_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "N\u00b0",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Cliente",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Pedido",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "F. Venta",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "F. Esperada",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Estado",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Detalles",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th("", class_name="px-4 py-3"),
                        class_name="bg-gray-50 border-b border-gray-200",
                    ),
                ),
                rx.el.tbody(
                    rx.foreach(DataState.filtered_entregas, entrega_row),
                ),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        rx.cond(
            DataState.filtered_entregas.length() == 0,
            empty_state(),
            rx.fragment(),
        ),
        class_name="bg-white border border-gray-200 rounded-xl overflow-hidden",
    )


def detail_row(label: str, value: rx.Var | str) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="text-xs text-gray-500"),
        rx.el.p(value, class_name="text-sm font-medium text-gray-900 mt-0.5"),
        class_name="",
    )


def entrega_detail_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        "Entrega #"
                        + DataState.selected_entrega["IdEntrega"].to_string(),
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Detalle de la entrega al cliente.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4 pb-4 border-b border-gray-100",
                ),
                rx.el.div(
                    detail_row(
                        "Cliente",
                        rx.cond(
                            DataState.selected_entrega["cliente"],
                            DataState.selected_entrega["cliente"]["NombreCliente"],
                            "Sin cliente",
                        ),
                    ),
                    detail_row(
                        "Pedido",
                        "# "
                        + DataState.selected_entrega["IdPedido"].to_string(),
                    ),
                    detail_row(
                        "Fecha venta",
                        rx.cond(DataState.selected_entrega["FechaVenta"], DataState.selected_entrega["FechaVenta"], "\u2014"),
                    ),
                    detail_row(
                        "Fecha esperada",
                        rx.cond(DataState.selected_entrega["FechaEsperada"], DataState.selected_entrega["FechaEsperada"], "\u2014"),
                    ),
                    detail_row(
                        "Fecha real",
                        rx.cond(DataState.selected_entrega["FechaReal"], DataState.selected_entrega["FechaReal"], "\u2014"),
                    ),
                    detail_row(
                        "Estado",
                        DataState.selected_entrega["Estado"],
                    ),
                    class_name="grid grid-cols-3 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.h4(
                        "Detalles de la entrega",
                        class_name="text-sm font-semibold text-gray-900 mb-3",
                    ),
                    rx.cond(
                        DataState.selected_entrega["detalles"].length() > 0,
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(
                                            "Producto",
                                            class_name="px-3 py-2 text-left text-xs font-semibold text-gray-500 uppercase",
                                        ),
                                        rx.el.th(
                                            "Cantidad",
                                            class_name="px-3 py-2 text-left text-xs font-semibold text-gray-500 uppercase",
                                        ),
                                        rx.el.th(
                                            "P. Unitario",
                                            class_name="px-3 py-2 text-left text-xs font-semibold text-gray-500 uppercase",
                                        ),
                                        rx.el.th(
                                            "Subtotal",
                                            class_name="px-3 py-2 text-left text-xs font-semibold text-gray-500 uppercase",
                                        ),
                                        class_name="bg-gray-50 border-b border-gray-200",
                                    ),
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        DataState.selected_entrega["detalles"],
                                        lambda d: rx.el.tr(
                                            rx.el.td(
                                                rx.cond(
                                                    d["producto"],
                                                    d["producto"]["NombreProducto"],
                                                    "\u2014",
                                                ),
                                                class_name="px-3 py-2 text-sm text-gray-900",
                                            ),
                                            rx.el.td(
                                                d["CantidadEntregada"].to_string(),
                                                class_name="px-3 py-2 text-sm text-gray-700",
                                            ),
                                            rx.el.td(
                                                "S/."
                                                + d[
                                                    "PrecioUnitario"
                                                ].to_string(),
                                                class_name="px-3 py-2 text-sm text-gray-700",
                                            ),
                                            rx.el.td(
                                                "S/."
                                                + (
                                                    d["CantidadEntregada"]
                                                    * d["PrecioUnitario"]
                                                ).to_string(),
                                                class_name="px-3 py-2 text-sm font-medium text-gray-900",
                                            ),
                                            rx.el.td(
                                                rx.el.button(
                                                    rx.icon("trash-2", class_name="h-3.5 w-3.5"),
                                                    on_click=lambda did=d["IdDetalleEntrega"]: DataState.delete_detalle_entrega(
                                                        DataState.selected_entrega["IdEntrega"], did
                                                    ),
                                                    class_name="p-1 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded transition-colors",
                                                    title="Eliminar",
                                                ),
                                                class_name="px-3 py-2",
                                            ),
                                            class_name="border-b border-gray-100 hover:bg-gray-50",
                                        ),
                                    ),
                                ),
                                class_name="table-auto w-full",
                            ),
                            class_name="overflow-x-auto bg-white border border-gray-200 rounded-lg",
                        ),
                        rx.el.p(
                            "Esta entrega no tiene detalles.",
                            class_name="text-sm text-gray-500 italic",
                        ),
                    ),
                ),
                rx.el.div(
                    rx.el.h4(
                        "Agregar detalle",
                        class_name="text-sm font-semibold text-gray-900 mb-3 mt-4",
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.el.div(
                                rx.el.label("Producto", class_name="block text-xs font-medium text-gray-700 mb-1"),
                                rx.el.div(
                                    rx.el.select(
                                        rx.el.option("Seleccionar...", value="", disabled=True),
                                        rx.foreach(
                                            DataState.producto_filter_options,
                                            lambda o: rx.el.option(o["label"], value=o["value"]),
                                        ),
                                        name="IdProducto",
                                        class_name="w-full pl-3 pr-8 py-1.5 bg-white border border-gray-200 rounded-lg text-sm appearance-none focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                        color="black",
                                    ),
                                    rx.icon("chevron-down", class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none"),
                                    class_name="relative",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label("Cantidad", class_name="block text-xs font-medium text-gray-700 mb-1"),
                                rx.el.input(
                                    name="CantidadEntregada",
                                    type="number",
                                    defaultValue="1",
                                    class_name="w-full px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                    color="black",
                                ),
                            ),
                            rx.el.div(
                                rx.el.label("Precio Unit.", class_name="block text-xs font-medium text-gray-700 mb-1"),
                                rx.el.input(
                                    name="PrecioUnitario",
                                    type="number",
                                    step="0.01",
                                    defaultValue="0",
                                    class_name="w-full px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                    color="black",
                                ),
                            ),
                            rx.el.button(
                                rx.icon("plus", class_name="h-4 w-4"),
                                "Agregar",
                                type="submit",
                                class_name="flex items-center gap-1 px-3 py-1.5 mt-5 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 transition-colors",
                            ),
                            class_name="grid grid-cols-4 gap-3 items-end",
                        ),
                        on_submit=lambda form_data: DataState.add_detalle_entrega(
                            DataState.selected_entrega["IdEntrega"], form_data
                        ),
                        reset_on_submit=True,
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.cond(
                            DataState.selected_entrega["Estado"] == "Pendiente",
                            rx.el.button(
                                rx.icon("package", class_name="h-4 w-4"),
                                "Preparar",
                                class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-indigo-600 rounded-lg hover:bg-indigo-700 transition-colors",
                                on_click=lambda: DataState.cambiar_estado_entrega(DataState.selected_entrega, "Preparando"),
                            ),
                            rx.fragment(),
                        ),
                        rx.cond(
                            DataState.selected_entrega["Estado"] == "Preparando",
                            rx.el.button(
                                rx.icon("truck", class_name="h-4 w-4"),
                                "Despachar",
                                class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors",
                                on_click=lambda: DataState.cambiar_estado_entrega(DataState.selected_entrega, "En transito"),
                            ),
                            rx.fragment(),
                        ),
                        rx.cond(
                            DataState.selected_entrega["Estado"] == "En transito",
                            rx.el.button(
                                rx.icon("check-circle", class_name="h-4 w-4"),
                                "Entregado",
                                class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-emerald-600 rounded-lg hover:bg-emerald-700 transition-colors",
                                on_click=lambda: DataState.cambiar_estado_entrega(DataState.selected_entrega, "Entregado"),
                            ),
                            rx.fragment(),
                        ),
                        rx.cond(
                            (DataState.selected_entrega["Estado"] != "Entregado") & (DataState.selected_entrega["Estado"] != "No entregado") & (DataState.selected_entrega["Estado"] != "Cancelado"),
                            rx.el.button(
                                rx.icon("x-circle", class_name="h-4 w-4"),
                                "Cancelar",
                                class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors",
                                on_click=lambda: DataState.cambiar_estado_entrega(DataState.selected_entrega, "Cancelado"),
                            ),
                            rx.fragment(),
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.button(
                        "Cerrar",
                        on_click=DataState.close_entrega_detail,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    class_name="flex items-center justify-between pt-4 border-t border-gray-100 mt-4",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-4xl z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_entrega_detail,
        on_open_change=DataState.close_entrega_detail,
    )


def entrega_delete_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "triangle-alert", class_name="h-5 w-5 text-red-600"
                        ),
                        class_name="h-10 w-10 rounded-full bg-red-50 flex items-center justify-center mb-3",
                    ),
                    rx.radix.primitives.dialog.title(
                        "Eliminar entrega",
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "\u00bfSeguro que deseas eliminar la Entrega #"
                        + DataState.selected_entrega["IdEntrega"].to_string()
                        + "? Esta acci\u00f3n no se puede deshacer.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        on_click=DataState.close_delete_entrega,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    rx.el.button(
                        "Eliminar",
                        on_click=DataState.confirm_delete_entrega,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700",
                    ),
                    class_name="flex justify-end gap-2",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-md z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_entrega_delete,
        on_open_change=DataState.close_delete_entrega,
    )


def entrega_create_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        rx.cond(
                            DataState.is_editing_entrega,
                            "Editar entrega",
                            "Nueva entrega",
                        ),
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        rx.cond(
                            DataState.is_editing_entrega,
                            "Actualiza el estado y fechas de la entrega.",
                            "Selecciona el cliente, pedido y fechas de la entrega.",
                        ),
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Cliente",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option(
                                        "Seleccionar cliente...",
                                        value="",
                                        disabled=True,
                                    ),
                                    rx.foreach(
                                        DataState.cliente_filter_options,
                                        lambda o: rx.el.option(
                                            o["label"], value=o["value"]
                                        ),
                                    ),
                                    name="IdCliente",
                                    default_value=DataState.editing_entrega["IdCliente"].to_string(),
                                    class_name="w-full pl-3 pr-8 py-2 bg-white border border-gray-200 rounded-lg text-sm appearance-none focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                    color="black",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                            class_name="",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Pedido",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option(
                                        "Seleccionar pedido...",
                                        value="",
                                        disabled=True,
                                    ),
                                    rx.foreach(
                                        DataState.pedido_filter_options,
                                        lambda o: rx.el.option(
                                            o["label"], value=o["value"]
                                        ),
                                    ),
                                    name="IdPedido",
                                    default_value=DataState.editing_entrega["IdPedido"].to_string(),
                                    class_name="w-full pl-3 pr-8 py-2 bg-white border border-gray-200 rounded-lg text-sm appearance-none focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                    color="black",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                            class_name="",
                        ),
                        class_name="grid grid-cols-2 gap-3 mb-3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Fecha venta",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.input(
                                name="FechaVenta",
                                type="date",
                                default_value=DataState.editing_entrega_fecha_venta_iso,
                                key=DataState.editing_entrega["IdEntrega"].to_string() + "_fv",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                            class_name="",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Fecha esperada",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.input(
                                name="FechaEsperada",
                                type="date",
                                default_value=DataState.editing_entrega_fecha_esperada_iso,
                                key=DataState.editing_entrega["IdEntrega"].to_string() + "_fe",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                            class_name="",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Estado",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option(
                                        "Pendiente", value="Pendiente"
                                    ),
                                    rx.el.option(
                                        "En transito", value="En transito"
                                    ),
                                    rx.el.option(
                                        "Entregado", value="Entregado"
                                    ),
                                    rx.el.option(
                                        "Cancelado", value="Cancelado"
                                    ),
                                    name="Estado",
                                    default_value=DataState.editing_entrega["Estado"],
                                    class_name="w-full pl-3 pr-8 py-2 bg-white border border-gray-200 rounded-lg text-sm appearance-none focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                    color="black",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                            class_name="",
                        ),
                        class_name="grid grid-cols-3 gap-3 mb-4",
                    ),
                    rx.cond(
                        DataState.entrega_form_error != "",
                        rx.el.div(
                            rx.icon(
                                "triangle-alert",
                                class_name="h-4 w-4 text-red-500 shrink-0",
                            ),
                            rx.el.p(
                                DataState.entrega_form_error,
                                class_name="text-sm text-red-700",
                            ),
                            class_name="flex items-center gap-2 p-3 bg-red-50 border border-red-100 rounded-lg mb-4",
                        ),
                        rx.fragment(),
                    ),
                    rx.el.div(
                        rx.el.button(
                            "Cancelar",
                            type="button",
                            on_click=DataState.close_entrega_form,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors",
                        ),
                        rx.el.button(
                            rx.cond(
                                DataState.is_editing_entrega,
                                "Guardar cambios",
                                "Crear entrega",
                            ),
                            type="submit",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t border-gray-100",
                    ),
                    on_submit=DataState.submit_entrega,
                    reset_on_submit=False,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-lg z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_entrega_form,
        on_open_change=DataState.close_entrega_form,
    )


def entregas_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stat_pill(
                "Total entregas",
                DataState.total_entregas.to_string(),
                "text-gray-900",
            ),
            stat_pill(
                "Filtrados",
                DataState.filtered_entregas.length().to_string(),
                "text-blue-600",
            ),
            stat_pill(
                "Pendientes",
                DataState.entregas_pendientes_count.to_string(),
                "text-yellow-600",
            ),
            stat_pill(
                "Entregadas",
                DataState.entregas_entregadas_count.to_string(),
                "text-green-600",
            ),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6",
        ),
        toolbar(),
        entregas_table(),
        entrega_create_dialog(),
        entrega_delete_dialog(),
        entrega_detail_dialog(),
    )


def entregas_page() -> rx.Component:
    return authenticated_layout(
        entregas_content(),
        title="Entregas",
        subtitle="Gestiona las entregas a clientes",
    )
