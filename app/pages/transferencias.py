import reflex as rx
from app.components.layout import authenticated_layout
from app.states.data_state import DataState, Transferencia


def estat_pill(label: str, value: rx.Var | str, color: str) -> rx.Component:
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
                    placeholder="Buscar por almacén origen...",
                    default_value=DataState.transferencia_search,
                    on_change=DataState.set_transferencia_search.debounce(300),
                    class_name="pl-9 pr-3 py-2 bg-white border border-gray-200 rounded-lg text-sm w-full md:w-72 focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                    color="black",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("Todos", value="Todos"),
                    rx.el.option("Pendiente", value="Pendiente"),
                    rx.el.option("En transito", value="En transito"),
                    rx.el.option("Completada", value="Completada"),
                    default_value=DataState.transferencia_estado_filter,
                    on_change=DataState.set_transferencia_estado_filter,
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
                on_click=DataState.clear_transferencia_filters,
                class_name="flex items-center gap-1.5 px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg transition-colors",
            ),
            class_name="flex flex-wrap items-center gap-2 flex-1",
        ),
        rx.el.button(
            rx.icon("plus", class_name="h-4 w-4"),
            "Nueva transferencia",
            on_click=DataState.open_new_transferencia,
            class_name="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors shrink-0",
        ),
        class_name="flex flex-col md:flex-row md:items-center gap-3 mb-4",
    )


def estado_badge(estado: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        estado,
        class_name="text-xs font-medium px-2 py-1 rounded-full w-fit "
        + rx.cond(
            estado == "Pendiente",
            "text-yellow-700 bg-yellow-50",
            rx.cond(
                estado == "En transito",
                "text-blue-700 bg-blue-50",
                rx.cond(
                    estado == "Completada",
                    "text-green-700 bg-green-50",
                    "text-gray-700 bg-gray-50",
                ),
            ),
        ),
    )


def transferencia_row(t: Transferencia) -> rx.Component:
    origen = t["almacen_origen"]
    destino = t["almacen_destino"]
    return rx.el.tr(
        rx.el.td(
            rx.el.p(
                t["IdTransferencia"].to_string(),
                class_name="text-sm font-medium text-gray-900",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(
                rx.cond(origen, rx.cond(origen["NombreAlmacen"], origen["NombreAlmacen"], "---"), "---"),
                class_name="text-sm text-gray-700",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(
                rx.cond(destino, rx.cond(destino["NombreAlmacen"], destino["NombreAlmacen"], "---"), "---"),
                class_name="text-sm text-gray-700",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(
                t["CantidadTransferida"].to_string(),
                class_name="text-sm text-gray-700",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(
                rx.cond(
                    t["FechaEnvio"] == "", "---",
                    t["FechaEnvio"],
                ),
                class_name="text-sm text-gray-700",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(
                rx.cond(
                    t["FechaRecepcion"] == "", "---",
                    t["FechaRecepcion"],
                ),
                class_name="text-sm text-gray-700",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            estado_badge(t["Estado"]),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("eye", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_transferencia_detail(t),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors",
                    title="Ver",
                ),
                rx.cond(
                    t["Estado"] == "Pendiente",
                    rx.el.button(
                        rx.icon("pencil", class_name="h-4 w-4"),
                        on_click=lambda: DataState.open_edit_transferencia(t),
                        class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors",
                        title="Editar",
                    ),
                    rx.fragment(),
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_delete_transferencia(t),
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
            rx.icon("arrow-left-right", class_name="h-6 w-6 text-gray-400"),
            class_name="h-12 w-12 rounded-xl bg-gray-100 flex items-center justify-center mb-4",
        ),
        rx.el.p(
            "No hay transferencias que coincidan",
            class_name="text-sm font-medium text-gray-900 mb-1",
        ),
        rx.el.p(
            "Intenta ajustar los filtros o crea una transferencia nueva.",
            class_name="text-xs text-gray-500",
        ),
        class_name="flex flex-col items-center justify-center py-16",
    )


def transferencias_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "N°",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Origen",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Destino",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Cantidad",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "F. Envío",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "F. Recepción",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Estado",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th("", class_name="px-4 py-3"),
                        class_name="bg-gray-50 border-b border-gray-200",
                    ),
                ),
                rx.el.tbody(
                    rx.foreach(DataState.filtered_transferencias, transferencia_row),
                ),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        rx.cond(
            DataState.filtered_transferencias.length() == 0,
            empty_state(),
            rx.fragment(),
        ),
        class_name="bg-white border border-gray-200 rounded-xl overflow-hidden",
    )


def form_field(label: str, input_el: rx.Component) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label, class_name="block text-xs font-medium text-gray-700 mb-1.5"
        ),
        input_el,
        class_name="",
    )


def detail_row(label: str, value: rx.Var | str) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="text-xs text-gray-500"),
        rx.el.p(value, class_name="text-sm font-medium text-gray-900 mt-0.5"),
        class_name="",
    )


def transferencia_detail_dialog() -> rx.Component:
    origen = DataState.selected_transferencia["almacen_origen"]
    destino = DataState.selected_transferencia["almacen_destino"]
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        "Transferencia #"
                        + DataState.selected_transferencia[
                            "IdTransferencia"
                        ].to_string(),
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Detalles de la transferencia entre almacenes.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4 pb-4 border-b border-gray-100",
                ),
                rx.el.div(
                    detail_row(
                        "Almacén Origen",
                        rx.cond(origen, rx.cond(origen["NombreAlmacen"], origen["NombreAlmacen"], "---"), "---"),
                    ),
                    detail_row(
                        "Almacén Destino",
                        rx.cond(destino, rx.cond(destino["NombreAlmacen"], destino["NombreAlmacen"], "---"), "---"),
                    ),
                    detail_row(
                        "Cantidad Transferida",
                        DataState.selected_transferencia[
                            "CantidadTransferida"
                        ].to_string(),
                    ),
                    detail_row(
                        "Fecha de Envío",
                        rx.cond(
                            DataState.selected_transferencia["FechaEnvio"] == "",
                            "---",
                            DataState.selected_transferencia["FechaEnvio"],
                        ),
                    ),
                    detail_row(
                        "Fecha de Recepción",
                        rx.cond(
                            DataState.selected_transferencia["FechaRecepcion"] == "",
                            "---",
                            DataState.selected_transferencia["FechaRecepcion"],
                        ),
                    ),
                    detail_row(
                        "Estado",
                        DataState.selected_transferencia["Estado"],
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.h4(
                        "Productos transferidos",
                        class_name="text-sm font-semibold text-gray-900 mb-3",
                    ),
                    rx.cond(
                        DataState.selected_transferencia["detalles"].length() > 0,
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
                                        class_name="bg-gray-50 border-b border-gray-200",
                                    ),
                                ),
                                rx.el.tbody(
                                    rx.foreach(
                                        DataState.selected_transferencia["detalles"],
                                        lambda d: rx.el.tr(
                                            rx.el.td(
                                                rx.cond(
                                                    d["producto"],
                                                    d["producto"]["NombreProducto"],
                                                    "---",
                                                ),
                                                class_name="px-3 py-2 text-sm text-gray-900",
                                            ),
                                            rx.el.td(
                                                d["CantidadTransferida"].to_string(),
                                                class_name="px-3 py-2 text-sm text-gray-700",
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
                            "Esta transferencia no tiene productos registrados.",
                            class_name="text-sm text-gray-500 italic",
                        ),
                    ),
                ),
                rx.el.div(
                    rx.el.button(
                        "Cerrar",
                        on_click=DataState.close_transferencia_detail,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    class_name="flex justify-end gap-2 pt-4 border-t border-gray-100 mt-4",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-2xl z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_transferencia_detail,
        on_open_change=DataState.close_transferencia_detail,
    )


def transferencia_delete_dialog() -> rx.Component:
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
                        "Eliminar transferencia",
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "¿Seguro que deseas eliminar la transferencia #"
                        + DataState.selected_transferencia[
                            "IdTransferencia"
                        ].to_string()
                        + "? Esta acción no se puede deshacer.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        on_click=DataState.close_delete_transferencia,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    rx.el.button(
                        "Eliminar",
                        on_click=DataState.confirm_delete_transferencia,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700",
                    ),
                    class_name="flex justify-end gap-2",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-md z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_transferencia_delete,
        on_open_change=DataState.close_delete_transferencia,
    )


def transferencia_form_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        rx.cond(
                            DataState.is_editing_transferencia,
                            "Editar transferencia",
                            "Nueva transferencia",
                        ),
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Completa la información de la transferencia.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4",
                ),
                rx.el.form(
                    rx.el.div(
                        form_field(
                            "Almacén Origen",
                            rx.el.div(
                                rx.el.select(
                                    rx.foreach(
                                        DataState.almacen_filter_options,
                                        lambda o: rx.el.option(
                                            o["label"], value=o["value"]
                                        ),
                                    ),
                                    name="IdAlmacenOrigen",
                                    default_value=DataState.editing_transferencia[
                                        "IdAlmacenOrigen"
                                    ].to_string(),
                                    key=DataState.editing_transferencia[
                                        "IdTransferencia"
                                    ].to_string()
                                    + "_origen",
                                    class_name="w-full pl-3 pr-8 py-2 bg-white border border-gray-200 rounded-lg text-sm appearance-none focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                    color="black",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                        ),
                        form_field(
                            "Almacén Destino",
                            rx.el.div(
                                rx.el.select(
                                    rx.foreach(
                                        DataState.almacen_filter_options,
                                        lambda o: rx.el.option(
                                            o["label"], value=o["value"]
                                        ),
                                    ),
                                    name="IdAlmacenDestino",
                                    default_value=DataState.editing_transferencia[
                                        "IdAlmacenDestino"
                                    ].to_string(),
                                    key=DataState.editing_transferencia[
                                        "IdTransferencia"
                                    ].to_string()
                                    + "_destino",
                                    class_name="w-full pl-3 pr-8 py-2 bg-white border border-gray-200 rounded-lg text-sm appearance-none focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                    color="black",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-3 mb-3",
                    ),
                    rx.el.div(
                        form_field(
                            "Estado",
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option("Pendiente", value="Pendiente"),
                                    rx.el.option("En transito", value="En transito"),
                                    rx.el.option("Completada", value="Completada"),
                                    name="Estado",
                                    default_value=DataState.editing_transferencia[
                                        "Estado"
                                    ],
                                    class_name="w-full pl-3 pr-8 py-2 bg-white border border-gray-200 rounded-lg text-sm appearance-none focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                    color="black",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        form_field(
                            "Fecha de Envío",
                            rx.el.input(
                                name="FechaEnvio",
                                type="date",
                                default_value=DataState.editing_transferencia_fecha_envio_iso,
                                key=DataState.editing_transferencia[
                                    "IdTransferencia"
                                ].to_string()
                                + "_fenvio",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                        ),
                        form_field(
                            "Fecha de Recepción",
                            rx.el.input(
                                name="FechaRecepcion",
                                type="date",
                                default_value=DataState.editing_transferencia_fecha_recepcion_iso,
                                key=DataState.editing_transferencia[
                                    "IdTransferencia"
                                ].to_string()
                                + "_frecep",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-3 mb-4",
                    ),
                    rx.el.div(
                        rx.el.h4(
                            "Productos a transferir",
                            class_name="text-sm font-semibold text-gray-900 mb-2",
                        ),
                        rx.cond(
                            DataState.transferencia_form_detalles.length() > 0,
                            rx.el.div(
                                rx.el.table(
                                    rx.el.thead(
                                        rx.el.tr(
                                            rx.el.th("Producto", class_name="px-3 py-2 text-left text-xs font-semibold text-gray-500 uppercase"),
                                            rx.el.th("Cantidad", class_name="px-3 py-2 text-left text-xs font-semibold text-gray-500 uppercase"),
                                            rx.el.th("", class_name="px-3 py-2"),
                                            class_name="bg-gray-50 border-b border-gray-200",
                                        ),
                                    ),
                                    rx.el.tbody(
                                        rx.foreach(
                                            DataState.transferencia_form_detalles,
                                            lambda d: rx.el.tr(
                                                rx.el.td(d["_nombre_producto"], class_name="px-3 py-2 text-sm text-gray-900"),
                                                rx.el.td(d["CantidadTransferida"].to_string(), class_name="px-3 py-2 text-sm text-gray-700"),
                                                rx.el.td(
                                                    rx.el.button(
                                                        rx.icon("trash-2", class_name="h-3.5 w-3.5"),
                                                        on_click=lambda d=d: DataState.remove_transferencia_detalle_temp(d["_idx"]),
                                                        class_name="p-1 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded transition-colors",
                                                    ),
                                                    class_name="px-3 py-2",
                                                ),
                                                class_name="border-b border-gray-100",
                                            ),
                                        ),
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
                                        value=DataState.transferencia_detalle_temp_producto,
                                        on_change=DataState.set_transferencia_detalle_temp_producto,
                                        class_name="w-full pl-3 pr-8 py-1.5 bg-white border border-gray-200 rounded-lg text-sm appearance-none focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                        color="black",
                                    ),
                                    rx.icon("chevron-down", class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none"),
                                    class_name="relative",
                                ),
                                class_name="col-span-8",
                            ),
                            rx.el.div(
                                rx.el.label("Cantidad", class_name="block text-xs font-medium text-gray-700 mb-1"),
                                rx.el.input(
                                    value=DataState.transferencia_detalle_temp_cantidad,
                                    on_change=DataState.set_transferencia_detalle_temp_cantidad,
                                    type="number",
                                    min="1",
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
                                on_click=DataState.add_transferencia_detalle_temp,
                                class_name="col-span-2 px-3 py-1.5 mt-5 text-sm font-medium text-white bg-green-600 rounded-lg hover:bg-green-700 transition-colors",
                            ),
                            class_name="grid grid-cols-12 gap-3 items-end",
                        ),
                        class_name="mb-4 p-3 bg-gray-50 border border-gray-200 rounded-lg",
                    ),
                    rx.cond(
                        DataState.transferencia_form_error != "",
                        rx.el.div(
                            rx.icon(
                                "triangle-alert",
                                class_name="h-4 w-4 text-red-500 shrink-0",
                            ),
                            rx.el.p(
                                DataState.transferencia_form_error,
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
                            on_click=DataState.close_transferencia_form,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors",
                        ),
                        rx.el.button(
                            rx.cond(
                                DataState.is_editing_transferencia,
                                "Guardar cambios",
                                "Crear transferencia",
                            ),
                            type="submit",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t border-gray-100",
                    ),
                    on_submit=DataState.submit_transferencia,
                    reset_on_submit=False,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-lg z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_transferencia_form,
        on_open_change=DataState.close_transferencia_form,
    )


def transferencias_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            estat_pill(
                "Total transferencias",
                DataState.total_transferencias.to_string(),
                "text-gray-900",
            ),
            estat_pill(
                "Filtrados",
                DataState.filtered_transferencias.length().to_string(),
                "text-blue-600",
            ),
            estat_pill(
                "Pendientes",
                DataState.transferencias_pendientes_count.to_string(),
                "text-yellow-600",
            ),
            estat_pill(
                "Completadas",
                DataState.transferencias_completadas_count.to_string(),
                "text-green-600",
            ),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6",
        ),
        toolbar(),
        transferencias_table(),
        transferencia_form_dialog(),
        transferencia_delete_dialog(),
        transferencia_detail_dialog(),
    )


def transferencias_page() -> rx.Component:
    return authenticated_layout(
        transferencias_content(),
        title="Transferencias",
        subtitle="Gestiona las transferencias entre almacenes",
    )
