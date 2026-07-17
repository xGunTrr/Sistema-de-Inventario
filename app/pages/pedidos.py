import reflex as rx
from app.components.layout import authenticated_layout
from app.states.data_state import DataState, Pedido, DetallePedido

MAX_DETALLE_ROWS = 50


def _detalle_rows():
    return [
        rx.cond(
            DataState.pedido_form_detalles.length() > i,
            rx.el.tr(
                rx.el.td(
                    DataState.pedido_form_detalles[i]["NombreProducto"],
                    class_name="px-3 py-2 text-sm text-gray-900",
                ),
                rx.el.td(
                    DataState.pedido_form_detalles[i]["Cantidad"].to_string(),
                    class_name="px-3 py-2 text-sm text-gray-700",
                ),
                rx.el.td(
                    "S/. " + DataState.pedido_form_detalles[i]["PrecioUnitario"].to_string(),
                    class_name="px-3 py-2 text-sm text-gray-700",
                ),
                rx.el.td(
                    "S/. " + DataState.pedido_form_detalles[i]["Subtotal"].to_string(),
                    class_name="px-3 py-2 text-sm font-medium text-gray-900",
                ),
                    rx.el.td(
                    rx.el.button(
                        rx.icon("trash-2", class_name="h-3.5 w-3.5"),
                        type="button",
                        on_click=DataState.remove_pedido_detalle_temp(i),
                        class_name="p-1 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded transition-colors",
                    ),
                    class_name="px-3 py-2",
                ),
                class_name="border-b border-gray-100",
            ),
        )
        for i in range(MAX_DETALLE_ROWS)
    ]


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
                    placeholder="Buscar por N\u00b0 o proveedor...",
                    default_value=DataState.pedido_search,
                    on_change=DataState.set_pedido_search.debounce(300),
                    class_name="pl-9 pr-3 py-2 bg-white border border-gray-200 rounded-lg text-sm w-full md:w-72 focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                    color="black",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.select(
                    rx.foreach(
                        DataState.proveedor_filter_options,
                        lambda o: rx.el.option(o["label"], value=o["value"]),
                    ),
                    default_value="",
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
                    rx.el.option("Pendiente", value="Pendiente"),
                    rx.el.option("Enviado", value="Enviado"),
                    rx.el.option("Completado", value="Completado"),
                    rx.el.option("Cancelado", value="Cancelado"),
                    default_value=DataState.pedido_estado_filter,
                    on_change=DataState.set_pedido_estado_filter,
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
                on_click=DataState.clear_pedido_filters,
                class_name="flex items-center gap-1.5 px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg transition-colors",
            ),
            class_name="flex flex-wrap items-center gap-2 flex-1",
        ),
        rx.el.button(
            rx.icon("plus", class_name="h-4 w-4"),
            "Nuevo pedido",
            on_click=DataState.open_new_pedido,
            class_name="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors shrink-0",
        ),
        class_name="flex flex-col md:flex-row md:items-center gap-3 mb-4",
    )


def pedido_row(p: Pedido) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.p(
                "# " + p["IdPedido"].to_string(),
                class_name="text-sm font-semibold text-gray-900",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(
                rx.cond(
                    p["proveedor"],
                    p["proveedor"]["NombreProveedor"],
                    "Sin proveedor",
                ),
                class_name="text-sm text-gray-700",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(
                rx.cond(p["FechaPedido"], p["FechaPedido"], "—"),
                class_name="text-sm text-gray-700",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.span(
                p["Estado"],
                class_name="text-xs font-medium px-2 py-1 rounded-full w-fit "
                + rx.cond(
                    p["Estado"] == "Pendiente",
                    "text-yellow-700 bg-yellow-50",
                    rx.cond(
                        p["Estado"] == "Enviado",
                        "text-blue-700 bg-blue-50",
                        rx.cond(
                            p["Estado"] == "Confirmado",
                            "text-purple-700 bg-purple-50",
                            rx.cond(
                                p["Estado"] == "En camino",
                                "text-amber-700 bg-amber-50",
                                rx.cond(
                                    p["Estado"] == "Entregado",
                                    "text-green-700 bg-green-50",
                                    rx.cond(
                                        p["Estado"] == "Parcial",
                                        "text-teal-700 bg-teal-50",
                                        "text-red-700 bg-red-50",
                                    ),
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
                p["detalles"].length().to_string() + " items",
                class_name="text-xs font-medium text-gray-600 bg-gray-100 px-2 py-1 rounded-full w-fit",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("eye", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_pedido_detail(p),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors",
                    title="Ver",
                ),
                rx.cond(
                    p["Estado"] == "Pendiente",
                    rx.el.button(
                        rx.icon("send", class_name="h-4 w-4"),
                        on_click=lambda: DataState.cambiar_estado_pedido(p, "Enviado"),
                        class_name="p-1.5 text-blue-600 hover:text-blue-700 hover:bg-blue-50 rounded transition-colors",
                        title="Enviar a proveedor",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    p["Estado"] == "Enviado",
                    rx.el.button(
                        rx.icon("check-circle", class_name="h-4 w-4"),
                        on_click=lambda: DataState.cambiar_estado_pedido(p, "Confirmado"),
                        class_name="p-1.5 text-purple-600 hover:text-purple-700 hover:bg-purple-50 rounded transition-colors",
                        title="Proveedor confirma",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    p["Estado"] == "Confirmado",
                    rx.el.button(
                        rx.icon("truck", class_name="h-4 w-4"),
                        on_click=lambda: DataState.cambiar_estado_pedido(p, "En camino"),
                        class_name="p-1.5 text-amber-600 hover:text-amber-700 hover:bg-amber-50 rounded transition-colors",
                        title="En camino",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    p["Estado"] == "En camino",
                    rx.el.button(
                        rx.icon("package-check", class_name="h-4 w-4"),
                        on_click=lambda: DataState.open_pedido_recepcion_modal(p),
                        class_name="p-1.5 text-emerald-600 hover:text-emerald-700 hover:bg-emerald-50 rounded transition-colors",
                        title="Recibir todo",
                    ),
                    rx.fragment(),
                ),
                rx.cond(
                    (p["Estado"] != "Entregado") & (p["Estado"] != "Parcial") & (p["Estado"] != "Cancelado"),
                    rx.el.button(
                        rx.icon("x-circle", class_name="h-4 w-4"),
                        on_click=lambda: DataState.cambiar_estado_pedido(p, "Cancelado"),
                        class_name="p-1.5 text-red-500 hover:text-red-600 hover:bg-red-50 rounded transition-colors",
                        title="Cancelar",
                    ),
                    rx.fragment(),
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_delete_pedido(p),
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
            rx.icon("clipboard-list", class_name="h-6 w-6 text-gray-400"),
            class_name="h-12 w-12 rounded-xl bg-gray-100 flex items-center justify-center mb-4",
        ),
        rx.el.p(
            "No hay pedidos que coincidan",
            class_name="text-sm font-medium text-gray-900 mb-1",
        ),
        rx.el.p(
            "Intenta ajustar los filtros o crea un pedido nuevo.",
            class_name="text-xs text-gray-500",
        ),
        class_name="flex flex-col items-center justify-center py-16",
    )


def pedidos_table() -> rx.Component:
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
                            "Proveedor",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Fecha",
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
                    rx.foreach(DataState.filtered_pedidos, pedido_row),
                ),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        rx.cond(
            DataState.filtered_pedidos.length() == 0,
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


def pedido_detail_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        "Pedido #"
                        + DataState.selected_pedido["IdPedido"].to_string(),
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Detalle del pedido a proveedor.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4 pb-4 border-b border-gray-100",
                ),
                rx.el.div(
                    detail_row(
                        "Proveedor",
                        rx.cond(
                            DataState.selected_pedido["proveedor"],
                            DataState.selected_pedido["proveedor"]["NombreProveedor"],
                            "Sin proveedor",
                        ),
                    ),
                    detail_row(
                        "Fecha",
                        rx.cond(DataState.selected_pedido["FechaPedido"], DataState.selected_pedido["FechaPedido"], "—"),
                    ),
                    detail_row(
                        "Estado",
                        DataState.selected_pedido["Estado"],
                    ),
                    class_name="grid grid-cols-3 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.h4(
                        "Detalles del pedido",
                        class_name="text-sm font-semibold text-gray-900 mb-3",
                    ),
                    rx.cond(
                        DataState.selected_pedido["detalles"].length() > 0,
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
                                        DataState.selected_pedido["detalles"],
                                        lambda d: rx.el.tr(
                                            rx.el.td(
                                                rx.cond(
                                                    d["producto"],
                                                    d["producto"]["NombreProducto"],
                                                    "—",
                                                ),
                                                class_name="px-3 py-2 text-sm text-gray-900",
                                            ),
                                            rx.el.td(
                                                d["Cantidad"].to_string(),
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
                                                    d["Cantidad"]
                                                    * d["PrecioUnitario"]
                                                ).to_string(),
                                                class_name="px-3 py-2 text-sm font-medium text-gray-900",
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
                            "Este pedido no tiene detalles.",
                            class_name="text-sm text-gray-500 italic",
                        ),
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.cond(
                            DataState.selected_pedido["Estado"] == "Pendiente",
                            rx.el.button(
                                rx.icon("send", class_name="h-4 w-4"),
                                "Enviar a proveedor",
                                class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors",
                                on_click=lambda: DataState.cambiar_estado_pedido(DataState.selected_pedido, "Enviado"),
                            ),
                            rx.fragment(),
                        ),
                        rx.cond(
                            DataState.selected_pedido["Estado"] == "Enviado",
                            rx.el.button(
                                rx.icon("check-circle", class_name="h-4 w-4"),
                                "Proveedor confirma",
                                class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-purple-600 rounded-lg hover:bg-purple-700 transition-colors",
                                on_click=lambda: DataState.cambiar_estado_pedido(DataState.selected_pedido, "Confirmado"),
                            ),
                            rx.fragment(),
                        ),
                        rx.cond(
                            DataState.selected_pedido["Estado"] == "Confirmado",
                            rx.el.button(
                                rx.icon("truck", class_name="h-4 w-4"),
                                "En camino",
                                class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-amber-600 rounded-lg hover:bg-amber-700 transition-colors",
                                on_click=lambda: DataState.cambiar_estado_pedido(DataState.selected_pedido, "En camino"),
                            ),
                            rx.fragment(),
                        ),
                        rx.cond(
                            DataState.selected_pedido["Estado"] == "En camino",
                            rx.el.button(
                                rx.icon("package-check", class_name="h-4 w-4"),
                                "Recibir todo",
                                class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-emerald-600 rounded-lg hover:bg-emerald-700 transition-colors",
                                on_click=lambda: DataState.open_pedido_recepcion_modal(DataState.selected_pedido),
                            ),
                            rx.fragment(),
                        ),
                        rx.cond(
                            (DataState.selected_pedido["Estado"] != "Entregado") & (DataState.selected_pedido["Estado"] != "Parcial") & (DataState.selected_pedido["Estado"] != "Cancelado"),
                            rx.el.button(
                                rx.icon("x", class_name="h-4 w-4"),
                                "Cancelar",
                                class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700 transition-colors",
                                on_click=lambda: DataState.cambiar_estado_pedido(DataState.selected_pedido, "Cancelado"),
                            ),
                            rx.fragment(),
                        ),
                        class_name="flex items-center gap-2",
                    ),
                    rx.el.button(
                        "Cerrar",
                        on_click=DataState.close_pedido_detail,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    class_name="flex items-center justify-between pt-4 border-t border-gray-100 mt-4",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-4xl z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_pedido_detail,
        on_open_change=DataState.close_pedido_detail,
    )


def pedido_delete_dialog() -> rx.Component:
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
                        "Eliminar pedido",
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "\u00bfSeguro que deseas eliminar el Pedido #"
                        + DataState.selected_pedido["IdPedido"].to_string()
                        + "? Esta acci\u00f3n no se puede deshacer.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        on_click=DataState.close_delete_pedido,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    rx.el.button(
                        "Eliminar",
                        on_click=DataState.confirm_delete_pedido,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700",
                    ),
                    class_name="flex justify-end gap-2",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-md z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_pedido_delete,
        on_open_change=DataState.close_delete_pedido,
    )


def pedido_recepcion_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.el.div(
                        rx.icon(
                            "warehouse", class_name="h-5 w-5 text-emerald-600"
                        ),
                        class_name="h-10 w-10 rounded-full bg-emerald-50 flex items-center justify-center mb-3",
                    ),
                    rx.radix.primitives.dialog.title(
                        "Seleccionar almacen de destino",
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Selecciona el almacen donde se recibira el Pedido #"
                        + DataState.selected_pedido["IdPedido"].to_string(),
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.label(
                        "Almacen destino",
                        class_name="block text-xs font-medium text-gray-700 mb-1.5",
                    ),
                    rx.el.div(
                        rx.el.select(
                            rx.el.option(
                                "Seleccionar almacen...",
                                value="",
                                disabled=True,
                            ),
                            rx.foreach(
                                DataState.almacen_filter_options,
                                lambda o: rx.el.option(
                                    o["label"], value=o["value"]
                                ),
                            ),
                            value=DataState.pedido_recepcion_almacen_id,
                            on_change=DataState.set_pedido_recepcion_almacen_id,
                            class_name="w-full pl-3 pr-8 py-2 bg-white border border-gray-200 rounded-lg text-sm appearance-none focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                            color="black",
                        ),
                        rx.icon(
                            "chevron-down",
                            class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                        ),
                        class_name="relative",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("x", class_name="h-4 w-4"),
                        "Cancelar",
                        on_click=DataState.close_pedido_recepcion_modal,
                        class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors",
                    ),
                    rx.el.button(
                        rx.icon("package-check", class_name="h-4 w-4"),
                        "Confirmar recepcion",
                        on_click=DataState.confirm_pedido_recepcion,
                        class_name="flex items-center gap-1.5 px-4 py-2 text-sm font-medium text-white bg-emerald-600 rounded-lg hover:bg-emerald-700 transition-colors",
                    ),
                    class_name="flex justify-end gap-2 pt-4 border-t border-gray-100",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-md z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_pedido_recepcion_modal,
        on_open_change=DataState.close_pedido_recepcion_modal,
    )


def pedido_create_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        rx.cond(
                            DataState.is_editing_pedido,
                            "Editar pedido",
                            "Nuevo pedido",
                        ),
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        rx.cond(
                            DataState.is_editing_pedido,
                            "Solo puedes editar pedidos en estado Pendiente.",
                            "Selecciona el proveedor y agrega los productos al pedido. El estado sera Pendiente.",
                        ),
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Proveedor",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option(
                                        "Seleccionar proveedor...",
                                        value="",
                                        disabled=True,
                                    ),
                                    rx.foreach(
                                        DataState.proveedor_filter_options,
                                        lambda o: rx.el.option(
                                            o["label"], value=o["value"]
                                        ),
                                    ),
                                    name="IdProveedor",
                                    default_value=DataState.editing_pedido["IdProveedor"].to_string(),
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
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.el.h4(
                            "Detalles del pedido",
                            class_name="text-sm font-semibold text-gray-900 mb-2",
                        ),
                        rx.cond(
                            DataState.pedido_form_detalles.length() > 0,
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th("Producto", class_name="px-3 py-2 text-left text-xs font-semibold text-gray-500 uppercase"),
                                            rx.el.th("Cant.", class_name="px-3 py-2 text-left text-xs font-semibold text-gray-500 uppercase"),
                                            rx.el.th("P. Unit.", class_name="px-3 py-2 text-left text-xs font-semibold text-gray-500 uppercase"),
                                            rx.el.th("Subtotal", class_name="px-3 py-2 text-left text-xs font-semibold text-gray-500 uppercase"),
                                            rx.el.th("", class_name="px-3 py-2"),
                                            class_name="bg-gray-50 border-b border-gray-200",
                                        ),
                                    ),
                                    rx.el.tbody(
                                        *_detalle_rows(),
                                    ),
                                    class_name="table-auto w-full mb-3",
                                ),
                                class_name="overflow-x-auto bg-white border border-gray-200 rounded-lg mb-3",
                            ),
                            rx.fragment(),
                        ),
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
                                        value=DataState.pedido_detalle_temp_producto,
                                        on_change=DataState.set_pedido_detalle_temp_producto,
                                        class_name="w-full pl-3 pr-8 py-1.5 bg-white border border-gray-200 rounded-lg text-sm appearance-none focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                        color="black",
                                    ),
                                    rx.icon("chevron-down", class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none"),
                                    class_name="relative",
                                ),
                                class_name="col-span-6",
                            ),
                            rx.el.div(
                                rx.el.label("Cantidad", class_name="block text-xs font-medium text-gray-700 mb-1"),
                                rx.el.input(
                                    value=DataState.pedido_detalle_temp_cantidad,
                                    on_change=DataState.set_pedido_detalle_temp_cantidad,
                                    type="number",
                                    class_name="w-full px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                    color="black",
                                ),
                                class_name="col-span-2",
                            ),
                            rx.el.div(
                                rx.el.label("Precio Unit. (S/.)", class_name="block text-xs font-medium text-gray-700 mb-1"),
                                rx.el.input(
                                    value=DataState.pedido_detalle_temp_precio,
                                    on_change=DataState.set_pedido_detalle_temp_precio,
                                    type="number",
                                    step="0.01",
                                    class_name="w-full px-3 py-1.5 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                    color="black",
                                ),
                                class_name="col-span-2",
                            ),
                            rx.el.button(
                                rx.el.div(
                                    rx.icon("plus", class_name="h-3.5 w-3.5"),
                                    "Agregar linea",
                                    class_name="flex items-center gap-1",
                                ),
                                type="button",
                                on_click=DataState.add_pedido_detalle_temp,
                                class_name="col-span-2 px-3 py-1.5 mt-5 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 transition-colors",
                            ),
                            class_name="grid grid-cols-12 gap-3 items-end",
                        ),
                        class_name="mb-4 p-3 bg-gray-50 border border-gray-200 rounded-lg",
                    ),
                    rx.cond(
                        DataState.pedido_form_error != "",
                        rx.el.div(
                            rx.icon(
                                "triangle-alert",
                                class_name="h-4 w-4 text-red-500 shrink-0",
                            ),
                            rx.el.p(
                                DataState.pedido_form_error,
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
                            on_click=DataState.close_pedido_form,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors",
                        ),
                        rx.el.button(
                            rx.cond(
                                DataState.is_editing_pedido,
                                "Guardar cambios",
                                "Crear pedido",
                            ),
                            type="submit",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t border-gray-100",
                    ),
                    on_submit=DataState.submit_pedido,
                    reset_on_submit=False,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-4xl z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_pedido_form,
        on_open_change=DataState.close_pedido_form,
    )


def pedidos_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stat_pill(
                "Total pedidos",
                DataState.total_pedidos.to_string(),
                "text-gray-900",
            ),
            stat_pill(
                "Filtrados",
                DataState.filtered_pedidos.length().to_string(),
                "text-blue-600",
            ),
            stat_pill(
                "Pendientes",
                DataState.pedidos_pendientes_count.to_string(),
                "text-yellow-600",
            ),
            stat_pill(
                "Completados",
                DataState.pedidos_completados_count.to_string(),
                "text-green-600",
            ),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6",
        ),
        toolbar(),
        pedidos_table(),
        pedido_create_dialog(),
        pedido_delete_dialog(),
        pedido_detail_dialog(),
        pedido_recepcion_dialog(),
    )


def pedidos_page() -> rx.Component:
    return authenticated_layout(
        pedidos_content(),
        title="Pedidos",
        subtitle="Gestiona tus pedidos a proveedores",
    )
