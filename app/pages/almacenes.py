import reflex as rx

from app.components.layout import authenticated_layout
from app.states.data_state import DataState, Almacen, Ubicacion

def almacen_card(a: Almacen) -> rx.Component:
    """
        ui: Carta de almacenes
    """
    ubic_name = rx.cond(
        a["ubicacion"],
        rx.cond(a["ubicacion"]["NombreUbicacion"], a["ubicacion"]["NombreUbicacion"], "Sin ubicación"),
        "Sin ubicación",
    )
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("warehouse", class_name="h-5 w-5 text-amber-700"),
                class_name="h-10 w-10 rounded-lg bg-amber-50 flex items-center justify-center",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("eye", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_almacen_detail(a),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded",
                ),
                rx.el.button(
                    rx.icon("pencil", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_edit_almacen(a),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_delete_almacen(a),
                    class_name="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded",
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.p(a["NombreAlmacen"], class_name="text-base font-semibold text-gray-900"),
        rx.el.p(ubic_name, class_name="text-sm text-gray-500 mt-1"),
        rx.el.div(
            rx.el.div(
                rx.icon("map-pin", class_name="h-3.5 w-3.5 text-gray-400"),
                rx.el.span(ubic_name, class_name="text-xs text-gray-600 truncate"),
                class_name="flex items-center gap-2 min-w-0",
            ),
            rx.el.div(
                rx.cond(
                    a["EsRefrigerado"],
                    rx.el.span(
                        "Refrigerado",
                        class_name="text-xs font-medium text-blue-700 bg-blue-50 px-2 py-1 rounded-full",
                    ),
                    rx.el.span(
                        "Ambiente",
                        class_name="text-xs font-medium text-gray-600 bg-gray-100 px-2 py-1 rounded-full",
                    ),
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex flex-col gap-1.5 mt-3",
        ),
        class_name="bg-white border border-gray-200 rounded-xl p-5 hover:border-gray-300 transition-colors",
    )

def almacenes_empty() -> rx.Component:
    """
        ui: Se muestra esta interfaz en caso de que no existan almacenes
    """
    return rx.el.div(
        rx.el.div(
            rx.icon("warehouse", class_name="h-6 w-6 text-gray-400"),
            class_name="h-12 w-12 rounded-xl bg-gray-100 flex items-center justify-center mb-4",
        ),
        rx.el.p(
            "No hay almacenes",
            class_name="text-sm font-medium text-gray-900 mb-1",
        ),
        rx.el.p(
            "Añade un almacén para gestionar tu inventario.",
            class_name="text-xs text-gray-500",
        ),
        class_name="flex flex-col items-center justify-center py-16 bg-white border border-gray-200 rounded-xl",
    )

def almacen_form_dialog() -> rx.Component:
    """
        ui: Pop up formulario de registro de almacen
    """
    ubic = DataState.editing_almacen["ubicacion"]
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        rx.cond(
                            DataState.is_editing_almacen,
                            "Editar almacén",
                            "Nuevo almacén",
                        ),
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Información del almacén.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Nombre del almacén",
                            class_name="block text-xs font-medium text-gray-700 mb-1.5",
                        ),
                        rx.el.input(
                            name="NombreAlmacen",
                            default_value=DataState.editing_almacen["NombreAlmacen"],
                            key=DataState.editing_almacen["IdAlmacen"].to_string()
                                + "_NombreAlmacen",
                            placeholder="Ej. Almacén Central",
                            class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                            color="black",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Ubicación",
                            class_name="block text-xs font-medium text-gray-700 mb-1.5",
                        ),
                        rx.el.select(
                            rx.el.option("Seleccionar ubicación", value=""),
                            rx.foreach(
                                DataState.ubicacion_filter_options,
                                lambda opt: rx.el.option(opt["label"], value=opt["value"]),
                            ),
                            name="IdUbicacion",
                            key=DataState.editing_almacen["IdAlmacen"].to_string()
                                + "_IdUbicacion",
                            default_value=DataState.editing_almacen["IdUbicacion"].to_string(),
                            class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                            color="black",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Refrigerado",
                            class_name="block text-xs font-medium text-gray-700 mb-1.5",
                        ),
                        rx.el.div(
                            rx.el.input(
                                name="EsRefrigerado",
                                type="checkbox",
                                default_checked=DataState.editing_almacen["EsRefrigerado"],
                                key=DataState.editing_almacen["IdAlmacen"].to_string()
                                    + "_EsRefrigerado",
                                class_name="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500",
                            ),
                            rx.el.span("Sí", class_name="text-sm text-gray-700 ml-2"),
                            class_name="flex items-center",
                        ),
                        class_name="mb-4",
                    ),
                    rx.cond(
                        DataState.almacen_form_error != "",
                        rx.el.div(
                            rx.icon(
                                "triangle-alert",
                                class_name="h-4 w-4 text-red-500 shrink-0",
                            ),
                            rx.el.p(
                                DataState.almacen_form_error,
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
                            on_click=DataState.close_almacen_form,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                        ),
                        rx.el.button(
                            rx.cond(
                                DataState.is_editing_almacen,
                                "Guardar",
                                "Crear",
                            ),
                            type="submit",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t border-gray-100",
                    ),
                    on_submit=DataState.submit_almacen,
                    reset_on_submit=False,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-lg z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_almacen_form,
        on_open_change=DataState.close_almacen_form,
    )

def almacen_delete_dialog() -> rx.Component:
    """
        ui: Pop up de advertencia de eliminación de almacen
    """
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
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
                        "Eliminar almacén",
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "¿Eliminar '"
                        + DataState.selected_almacen["NombreAlmacen"]
                        + "'? Esta acción no se puede deshacer.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        on_click=DataState.close_delete_almacen,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    rx.el.button(
                        "Eliminar",
                        on_click=DataState.confirm_delete_almacen,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700",
                    ),
                    class_name="flex justify-end gap-2",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-md z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_almacen_delete,
        on_open_change=DataState.close_delete_almacen,
    )

def almacen_detail_dialog() -> rx.Component:
    """
        ui: Detalles del almacen (nombre, ubicacion, refrigerado, activo)
    """
    ubic = DataState.selected_almacen["ubicacion"]
    ubic_name = rx.cond(
        ubic,
        rx.cond(ubic["NombreUbicacion"], ubic["NombreUbicacion"], "N/A"),
        "N/A",
    )
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        DataState.selected_almacen["NombreAlmacen"],
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Detalles del almacén.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4 pb-4 border-b border-gray-100",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Ubicación", class_name="text-xs text-gray-500"),
                        rx.el.p(
                            ubic_name,
                            class_name="text-sm font-medium text-gray-900 mt-0.5",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p("Refrigerado", class_name="text-xs text-gray-500"),
                        rx.el.p(
                            rx.cond(
                                DataState.selected_almacen["EsRefrigerado"],
                                "Sí",
                                "No",
                            ),
                            class_name="text-sm font-medium text-gray-900 mt-0.5",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p("Estado", class_name="text-xs text-gray-500"),
                        rx.el.p(
                            rx.cond(
                                DataState.selected_almacen["Activo"],
                                "Activo",
                                "Inactivo",
                            ),
                            class_name="text-sm font-medium text-gray-900 mt-0.5",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cerrar",
                        on_click=DataState.close_almacen_detail,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    class_name="flex justify-end pt-4 border-t border-gray-100",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-lg z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_almacen_detail,
        on_open_change=DataState.close_almacen_detail,
    )

def almacenes_content() -> rx.Component:
    """
        ui: Contenido completo de la pestaña de almacenes
    """
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Buscar almacenes...",
                    color="black",
                    default_value=DataState.almacen_search,
                    on_change=DataState.set_almacen_search.debounce(300),
                    class_name="pl-9 pr-3 py-2 bg-white border border-gray-200 rounded-lg text-sm w-full md:w-72 focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                ),
                class_name="relative flex-1",
            ),
            rx.el.select(
                rx.el.option("Todas las ubicaciones", value="Todos"),
                rx.foreach(
                    DataState.ubicacion_filter_options,
                    lambda opt: rx.el.option(opt["label"], value=opt["value"]),
                ),
                value=DataState.ubicacion_filter,
                on_change=DataState.set_ubicacion_filter,
                color="black",
                class_name="px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
            ),
            rx.el.button(
                rx.icon("x", class_name="h-3.5 w-3.5"),
                "Limpiar",
                on_click=DataState.clear_almacen_filters,
                class_name="flex items-center gap-1.5 px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg transition-colors",
            ),
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4"),
                "Nuevo almacén",
                on_click=DataState.open_new_almacen,
                class_name="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700",
            ),
            class_name="flex flex-col md:flex-row gap-3 mb-6",
        ),
        rx.cond(
            DataState.filtered_almacenes.length() == 0,
            almacenes_empty(),
            rx.el.div(
                rx.foreach(DataState.filtered_almacenes, almacen_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
            ),
        ),
        almacen_form_dialog(),
        almacen_delete_dialog(),
        almacen_detail_dialog(),
    )

def almacenes_page() -> rx.Component:
    """
        ui-details: Detalles generales de la pestañana de almacenes (TITLE, SUBTITLE)
    """
    return authenticated_layout(
        almacenes_content(),
        title="Almacenes",
        subtitle="Administra tus almacenes",
    )
