import reflex as rx
from app.components.layout import authenticated_layout
from app.states.data_state import DataState, ProductType

def type_card(t: ProductType) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("tag", class_name="h-4 w-4 text-blue-600"),
                class_name="h-9 w-9 rounded-lg bg-blue-50 flex items-center justify-center",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("eye", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_type_detail(t),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded",
                ),
                rx.el.button(
                    rx.icon("pencil", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_edit_type(t),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_delete_type(t),
                    class_name="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded",
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.p(t["name"], class_name="text-base font-semibold text-gray-900"),
        rx.el.p(
            rx.cond(
                t["description"] != "", t["description"], "Sin descripción"
            ),
            class_name="text-sm text-gray-500 mt-1 line-clamp-2",
        ),
        rx.el.div(
            rx.el.span(
                t["product_count"].to_string() + " productos",
                class_name="text-xs font-medium text-blue-700 bg-blue-50 px-2 py-1 rounded-full w-fit",
            ),
            class_name="mt-4 pt-4 border-t border-gray-100",
        ),
        class_name="bg-white border border-gray-200 rounded-xl p-5 hover:border-gray-300 transition-colors",
    )


def types_empty() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("tag", class_name="h-6 w-6 text-gray-400"),
            class_name="h-12 w-12 rounded-xl bg-gray-100 flex items-center justify-center mb-4",
        ),
        rx.el.p(
                "No hay tipos", class_name="text-sm font-medium text-gray-900 mb-1"
        ),
        rx.el.p(
            "Crea un tipo para comenzar a categorizar tus productos.",
            class_name="text-xs text-gray-500",
        ),
        class_name="flex flex-col items-center justify-center py-16 bg-white border border-gray-200 rounded-xl",
    )

def type_form_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        rx.cond(
                            DataState.is_editing_type,
                            "Editar tipo",
                            "Nuevo tipo",
                        ),
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Categoría para agrupar productos.",
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
                            name="name",
                            default_value=DataState.editing_type["name"],
                            key=DataState.editing_type["id"].to_string()
                            + "_name",
                            placeholder="Ej. Electrónica",
                            class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                            color="black",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Descripción",
                            class_name="block text-xs font-medium text-gray-700 mb-1.5",
                        ),
                        rx.el.textarea(
                            name="description",
                            default_value=DataState.editing_type["description"],
                            key=DataState.editing_type["id"].to_string()
                            + "_desc",
                            placeholder="Descripción opcional",
                            rows="3",
                            class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500 resize-none",
                            color="black",
                        ),
                        class_name="mb-4",
                    ),
                    rx.cond(
                        DataState.type_form_error != "",
                        rx.el.div(
                            rx.icon(
                                "triangle-alert",
                                class_name="h-4 w-4 text-red-500 shrink-0",
                            ),
                            rx.el.p(
                                DataState.type_form_error,
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
                            on_click=DataState.close_type_form,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                        ),
                        rx.el.button(
                            rx.cond(
                                DataState.is_editing_type, "Guardar", "Crear"
                            ),
                            type="submit",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t border-gray-100",
                    ),
                    on_submit=DataState.submit_type,
                    reset_on_submit=False,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-md z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_type_form,
        on_open_change=DataState.close_type_form,
    )

def type_delete_dialog() -> rx.Component:
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
                        "Eliminar tipo",
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "¿Eliminar '"
                        + DataState.selected_type["name"]
                        + "'? Solo se puede eliminar si no tiene productos asociados.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        on_click=DataState.close_delete_type,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    rx.el.button(
                        "Eliminar",
                        on_click=DataState.confirm_delete_type,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700",
                    ),
                    class_name="flex justify-end gap-2",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-md z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_type_delete,
        on_open_change=DataState.close_delete_type,
    )


def type_detail_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        DataState.selected_type["name"],
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        rx.cond(
                            DataState.selected_type["description"] != "",
                            DataState.selected_type["description"],
                            "Sin descripción",
                        ),
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4 pb-4 border-b border-gray-100",
                ),
                rx.el.div(
                    rx.el.p(
                        "Productos asociados",
                        class_name="text-xs text-gray-500 mb-2",
                    ),
                    rx.el.p(
                        DataState.selected_type["product_count"].to_string(),
                        class_name="text-2xl font-semibold text-gray-900",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cerrar",
                        on_click=DataState.close_type_detail,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    class_name="flex justify-end pt-4 border-t border-gray-100",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-md z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_type_detail,
        on_open_change=DataState.close_type_detail,
    )

def tipos_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Buscar tipos...",
                    default_value=DataState.type_search,
                    on_change=DataState.set_type_search.debounce(300),
                    class_name="pl-9 pr-3 py-2 bg-white border border-gray-200 rounded-lg text-sm w-full md:w-72 focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                    color="black",
                ),
                class_name="relative flex-1",
            ),
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4"),
                "Nuevo tipo",
                on_click=DataState.open_new_type,
                class_name="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700",
            ),
            class_name="flex flex-col md:flex-row gap-3 mb-6",
        ),
        rx.cond(
            DataState.filtered_types.length() == 0,
            types_empty(),
            rx.el.div(
                rx.foreach(DataState.filtered_types, type_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
            ),
        ),
        type_form_dialog(),
        type_delete_dialog(),
        type_detail_dialog(),
    )

def tipos_page() -> rx.Component:
    return authenticated_layout(
        tipos_content(),
        title="Tipos",
        subtitle="Categoriza tus productos por tipo",
    )
