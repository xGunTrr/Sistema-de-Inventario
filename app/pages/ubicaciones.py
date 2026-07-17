import reflex as rx

from app.components.layout import authenticated_layout
from app.states.data_state import DataState, Ubicacion

def ubicacion_card(u: Ubicacion) -> rx.Component:
    """
        ui: Carta de ubicaciones
    """
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    u["NombreUbicacion"][0].upper(),
                    class_name="text-base font-semibold text-blue-700",
                ),
                class_name="h-10 w-10 rounded-lg bg-blue-50 flex items-center justify-center",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("eye", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_ubicacion_detail(u),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded",
                ),
                rx.el.button(
                    rx.icon("pencil", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_edit_ubicacion(u),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_delete_ubicacion(u),
                    class_name="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded",
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.p(u["NombreUbicacion"], class_name="text-base font-semibold text-gray-900"),
        rx.el.p(u["DireccionUbicacion"], class_name="text-sm text-gray-500 mt-1"),
        rx.el.div(
            rx.el.div(
                rx.icon("map-pin", class_name="h-3.5 w-3.5 text-gray-400"),
                rx.el.span(
                    u["Ciudad"], class_name="text-xs text-gray-600 truncate"
                ),
                class_name="flex items-center gap-2 min-w-0",
            ),
            rx.el.div(
                rx.icon("phone", class_name="h-3.5 w-3.5 text-gray-400"),
                rx.el.span(u["TelefonoContacto"], class_name="text-xs text-gray-600"),
                class_name="flex items-center gap-2",
            ),
            class_name="flex flex-col gap-1.5 mt-3",
        ),
        rx.el.div(
            rx.el.span(
                u["Referencia"],
                class_name="text-xs font-medium text-blue-700 bg-blue-50 px-2 py-1 rounded-full w-fit",
            ),
            class_name="mt-4 pt-4 border-t border-gray-100",
        ),
        class_name="bg-white border border-gray-200 rounded-xl p-5 hover:border-gray-300 transition-colors",
    )

def ubicaciones_empty() -> rx.Component:
    """
        ui: Se muestra esta interfaz en caso de que no existan ubicaciones
    """
    return rx.el.div(
        rx.el.div(
            rx.icon("map-pin", class_name="h-6 w-6 text-gray-400"),
            class_name="h-12 w-12 rounded-xl bg-gray-100 flex items-center justify-center mb-4",
        ),
        rx.el.p(
            "No hay ubicaciones",
            class_name="text-sm font-medium text-gray-900 mb-1",
        ),
        rx.el.p(
            "Añade una ubicación para asociarla a tus almacenes.",
            class_name="text-xs text-gray-500",
        ),
        class_name="flex flex-col items-center justify-center py-16 bg-white border border-gray-200 rounded-xl",
    )

def ubicacion_form_dialog() -> rx.Component:
    """
        ui: Pop up formulario de registro de ubicacion
    """
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        rx.cond(
                            DataState.is_editing_ubicacion,
                            "Editar ubicación",
                            "Nueva ubicación",
                        ),
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Información de la ubicación del almacén.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.label(
                            "Nombre",
                            class_name="block text-xs font-medium text-gray-700 mb-1.5",
                        ),
                        rx.el.input(
                            name="NombreUbicacion",
                            default_value=DataState.editing_ubicacion["NombreUbicacion"],
                            key=DataState.editing_ubicacion["IdUbicacion"].to_string()
                                + "_NombreUbicacion",
                            placeholder="Ej. Almacén Central",
                            class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                            color="black",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Dirección",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.input(
                                name="DireccionUbicacion",
                                default_value=DataState.editing_ubicacion["DireccionUbicacion"],
                                key=DataState.editing_ubicacion["IdUbicacion"].to_string()
                                    + "_DireccionUbicacion",
                                placeholder="Ej. Av. Industrial 123",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Ciudad",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.input(
                                name="Ciudad",
                                default_value=DataState.editing_ubicacion["Ciudad"],
                                key=DataState.editing_ubicacion["IdUbicacion"].to_string()
                                    + "_Ciudad",
                                placeholder="Ej. Lima",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-3 mb-3",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Referencia",
                            class_name="block text-xs font-medium text-gray-700 mb-1.5",
                        ),
                        rx.el.input(
                            name="Referencia",
                            default_value=DataState.editing_ubicacion["Referencia"],
                            key=DataState.editing_ubicacion["IdUbicacion"].to_string()
                                + "_Referencia",
                            placeholder="Ej. Frente al parque industrial",
                            class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                            color="black",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Teléfono de contacto",
                            class_name="block text-xs font-medium text-gray-700 mb-1.5",
                        ),
                        rx.el.input(
                            name="TelefonoContacto",
                            default_value=DataState.editing_ubicacion["TelefonoContacto"],
                            key=DataState.editing_ubicacion["IdUbicacion"].to_string()
                                + "_TelefonoContacto",
                            placeholder="+51 999 999 999",
                            class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                            color="black",
                        ),
                        class_name="mb-4",
                    ),
                    rx.cond(
                        DataState.ubicacion_form_error != "",
                        rx.el.div(
                            rx.icon(
                                "triangle-alert",
                                class_name="h-4 w-4 text-red-500 shrink-0",
                            ),
                            rx.el.p(
                                DataState.ubicacion_form_error,
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
                            on_click=DataState.close_ubicacion_form,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                        ),
                        rx.el.button(
                            rx.cond(
                                DataState.is_editing_ubicacion,
                                "Guardar",
                                "Crear",
                            ),
                            type="submit",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t border-gray-100",
                    ),
                    on_submit=DataState.submit_ubicacion,
                    reset_on_submit=False,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-lg z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_ubicacion_form,
        on_open_change=DataState.close_ubicacion_form,
    )

def ubicacion_delete_dialog() -> rx.Component:
    """
        ui: Pop up de advertencia de eliminación de ubicacion
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
                        "Eliminar ubicación",
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "¿Eliminar '"
                        + DataState.selected_ubicacion["NombreUbicacion"]
                        + "'? Solo se puede eliminar si no tiene almacenes asociados.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        on_click=DataState.close_delete_ubicacion,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    rx.el.button(
                        "Eliminar",
                        on_click=DataState.confirm_delete_ubicacion,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700",
                    ),
                    class_name="flex justify-end gap-2",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-md z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_ubicacion_delete,
        on_open_change=DataState.close_delete_ubicacion,
    )

def ubicacion_detail_dialog() -> rx.Component:
    """
        ui: Detalles de la ubicacion
    """
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        DataState.selected_ubicacion["NombreUbicacion"],
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Dirección: " + DataState.selected_ubicacion["DireccionUbicacion"],
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4 pb-4 border-b border-gray-100",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Ciudad", class_name="text-xs text-gray-500"),
                        rx.el.p(
                            DataState.selected_ubicacion["Ciudad"],
                            class_name="text-sm font-medium text-gray-900 mt-0.5",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p("Referencia", class_name="text-xs text-gray-500"),
                        rx.el.p(
                            DataState.selected_ubicacion["Referencia"],
                            class_name="text-sm font-medium text-gray-900 mt-0.5",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Teléfono", class_name="text-xs text-gray-500"
                        ),
                        rx.el.p(
                            DataState.selected_ubicacion["TelefonoContacto"],
                            class_name="text-sm font-medium text-gray-900 mt-0.5",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cerrar",
                        on_click=DataState.close_ubicacion_detail,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    class_name="flex justify-end pt-4 border-t border-gray-100",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-lg z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_ubicacion_detail,
        on_open_change=DataState.close_ubicacion_detail,
    )

def ubicaciones_content() -> rx.Component:
    """
        ui: Contenido completo de la pestaña de ubicaciones
    """
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Buscar ubicaciones...",
                    color="black",
                    default_value=DataState.ubicacion_search,
                    on_change=DataState.set_ubicacion_search.debounce(300),
                    class_name="pl-9 pr-3 py-2 bg-white border border-gray-200 rounded-lg text-sm w-full md:w-72 focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                ),
                class_name="relative flex-1",
            ),
            rx.el.button(
                rx.icon("x", class_name="h-3.5 w-3.5"),
                "Limpiar",
                on_click=DataState.clear_ubicacion_filters,
                class_name="flex items-center gap-1.5 px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg transition-colors",
            ),
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4"),
                "Nueva ubicación",
                on_click=DataState.open_new_ubicacion,
                class_name="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700",
            ),
            class_name="flex flex-col md:flex-row gap-3 mb-6",
        ),
        rx.cond(
            DataState.filtered_ubicaciones.length() == 0,
            ubicaciones_empty(),
            rx.el.div(
                rx.foreach(DataState.filtered_ubicaciones, ubicacion_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
            ),
        ),
        ubicacion_form_dialog(),
        ubicacion_delete_dialog(),
        ubicacion_detail_dialog(),
    )

def ubicaciones_page() -> rx.Component:
    """
        ui-details: Detalles generales de la pestañana de ubicaciones (TITLE, SUBTITLE)
    """
    return authenticated_layout(
        ubicaciones_content(),
        title="Ubicaciones",
        subtitle="Administra las ubicaciones de tus almacenes",
    )
