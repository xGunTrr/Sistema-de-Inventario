import reflex as rx

from app.components.layout import authenticated_layout
from app.states.data_state import DataState, Cliente

def cliente_card(c: Cliente) -> rx.Component:
    """
        ui: Carta de clientes
    """
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    c["NombreCliente"][0].upper(),
                    class_name="text-base font-semibold text-blue-700",
                ),
                class_name="h-10 w-10 rounded-lg bg-blue-50 flex items-center justify-center",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("eye", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_cliente_detail(c),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded",
                ),
                rx.el.button(
                    rx.icon("pencil", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_edit_cliente(c),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_delete_cliente(c),
                    class_name="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded",
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.p(c["NombreCliente"], class_name="text-base font-semibold text-gray-900"),
        rx.el.p(c["DireccionCliente"], class_name="text-sm text-gray-500 mt-1"),
        rx.el.div(
            rx.el.div(
                rx.icon("mail", class_name="h-3.5 w-3.5 text-gray-400"),
                rx.el.span(
                    c["Email"], class_name="text-xs text-gray-600 truncate"
                ),
                class_name="flex items-center gap-2 min-w-0",
            ),
            rx.el.div(
                rx.icon("phone", class_name="h-3.5 w-3.5 text-gray-400"),
                rx.el.span(c["Telefono"], class_name="text-xs text-gray-600"),
                class_name="flex items-center gap-2",
            ),
            class_name="flex flex-col gap-1.5 mt-3",
        ),
        class_name="bg-white border border-gray-200 rounded-xl p-5 hover:border-gray-300 transition-colors",
    )

def clientes_empty() -> rx.Component:
    """
        ui: Se muestra esta interfaz en caso de que no existan clientes
    """
    return rx.el.div(
        rx.el.div(
            rx.icon("users", class_name="h-6 w-6 text-gray-400"),
            class_name="h-12 w-12 rounded-xl bg-gray-100 flex items-center justify-center mb-4",
        ),
        rx.el.p(
            "No hay clientes",
            class_name="text-sm font-medium text-gray-900 mb-1",
        ),
        rx.el.p(
            "Añade un cliente para registrar sus datos de contacto.",
            class_name="text-xs text-gray-500",
        ),
        class_name="flex flex-col items-center justify-center py-16 bg-white border border-gray-200 rounded-xl",
    )

def cliente_form_dialog() -> rx.Component:
    """
        ui: Pop up formulario de registro de cliente
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
                            DataState.is_editing_cliente,
                            "Editar cliente",
                            "Nuevo cliente",
                        ),
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Información de contacto del cliente.",
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
                            name="NombreCliente",
                            default_value=DataState.editing_cliente["NombreCliente"],
                            key=DataState.editing_cliente["IdCliente"].to_string()
                                + "_NombreCliente",
                            placeholder="Ej. Juan Pérez",
                            class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                            color="black",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Dirección",
                            class_name="block text-xs font-medium text-gray-700 mb-1.5",
                        ),
                        rx.el.input(
                            name="DireccionCliente",
                            default_value=DataState.editing_cliente["DireccionCliente"],
                            key=DataState.editing_cliente["IdCliente"].to_string()
                                + "_DireccionCliente",
                            placeholder="Dirección del cliente",
                            class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                            color="black",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Teléfono",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.input(
                                name="Telefono",
                                default_value=DataState.editing_cliente[
                                    "Telefono"
                                ],
                                key=DataState.editing_cliente["IdCliente"].to_string()
                                    + "_Telefono",
                                placeholder="+51 999 999 999",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Email",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.input(
                                name="Email",
                                type="email",
                                default_value=DataState.editing_cliente[
                                    "Email"
                                ],
                                key=DataState.editing_cliente["IdCliente"].to_string()
                                    + "_Email",
                                placeholder="email@ejemplo.com",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-3 mb-4",
                    ),
                    rx.cond(
                        DataState.cliente_form_error != "",
                        rx.el.div(
                            rx.icon(
                                "triangle-alert",
                                class_name="h-4 w-4 text-red-500 shrink-0",
                            ),
                            rx.el.p(
                                DataState.cliente_form_error,
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
                            on_click=DataState.close_cliente_form,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                        ),
                        rx.el.button(
                            rx.cond(
                                DataState.is_editing_cliente,
                                "Guardar",
                                "Crear",
                            ),
                            type="submit",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t border-gray-100",
                    ),
                    on_submit=DataState.submit_cliente,
                    reset_on_submit=False,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-lg z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_cliente_form,
        on_open_change=DataState.close_cliente_form,
    )

def cliente_delete_dialog() -> rx.Component:
    """
        ui: Pop up de advertencia de eliminación de cliente
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
                        "Eliminar cliente",
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "¿Eliminar '"
                        + DataState.selected_cliente["NombreCliente"]
                        + "'? Esta acción no se puede deshacer.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        on_click=DataState.close_delete_cliente,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    rx.el.button(
                        "Eliminar",
                        on_click=DataState.confirm_delete_cliente,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700",
                    ),
                    class_name="flex justify-end gap-2",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-md z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_cliente_delete,
        on_open_change=DataState.close_delete_cliente,
    )

def cliente_detail_dialog() -> rx.Component:
    """
        ui: Detalles del cliente (nombre, dirección, teléfono, email)
    """
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        DataState.selected_cliente["NombreCliente"],
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Dirección: " + DataState.selected_cliente["DireccionCliente"],
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4 pb-4 border-b border-gray-100",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Teléfono", class_name="text-xs text-gray-500"),
                        rx.el.p(
                            DataState.selected_cliente["Telefono"],
                            class_name="text-sm font-medium text-gray-900 mt-0.5",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p("Email", class_name="text-xs text-gray-500"),
                        rx.el.p(
                            DataState.selected_cliente["Email"],
                            class_name="text-sm font-medium text-gray-900 mt-0.5",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Activo", class_name="text-xs text-gray-500"
                        ),
                        rx.el.p(
                            rx.cond(
                                DataState.selected_cliente["Activo"],
                                "Sí",
                                "No",
                            ),
                            class_name="text-sm font-medium text-gray-900 mt-0.5",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cerrar",
                        on_click=DataState.close_cliente_detail,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    class_name="flex justify-end pt-4 border-t border-gray-100",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-lg z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_cliente_detail,
        on_open_change=DataState.close_cliente_detail,
    )

def clientes_content() -> rx.Component:
    """
        ui: Contenido completo de la pestaña de clientes
    """
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Buscar clientes...",
                    color="black",
                    default_value=DataState.cliente_search,
                    on_change=DataState.set_cliente_search.debounce(300),
                    class_name="pl-9 pr-3 py-2 bg-white border border-gray-200 rounded-lg text-sm w-full md:w-72 focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                ),
                class_name="relative flex-1",
            ),
            rx.el.button(
                rx.icon("x", class_name="h-3.5 w-3.5"),
                "Limpiar",
                on_click=DataState.clear_cliente_filters,
                class_name="flex items-center gap-1.5 px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg transition-colors",
            ),
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4"),
                "Nuevo cliente",
                on_click=DataState.open_new_cliente,
                class_name="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700",
            ),
            class_name="flex flex-col md:flex-row gap-3 mb-6",
        ),
        rx.cond(
            DataState.filtered_clientes.length() == 0,
            clientes_empty(),
            rx.el.div(
                rx.foreach(DataState.filtered_clientes, cliente_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
            ),
        ),
        cliente_form_dialog(),
        cliente_delete_dialog(),
        cliente_detail_dialog(),
    )

def clientes_page() -> rx.Component:
    """
        ui-details: Detalles generales de la pestañana de clientes (TITLE, SUBTITLE)
    """
    return authenticated_layout(
        clientes_content(),
        title="Clientes",
        subtitle="Administra tus clientes",
    )
