import reflex as rx
from app.components.layout import authenticated_layout
from app.states.data_state import DataState, Supplier


def supplier_card(s: Supplier) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    s["name"][0].upper(),
                    class_name="text-base font-semibold text-blue-700",
                ),
                class_name="h-10 w-10 rounded-lg bg-blue-50 flex items-center justify-center",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("eye", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_supplier_detail(s),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded",
                ),
                rx.el.button(
                    rx.icon("pencil", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_edit_supplier(s),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_delete_supplier(s),
                    class_name="p-1.5 text-gray-500 hover:text-red-600 hover:bg-red-50 rounded",
                ),
                class_name="flex items-center gap-1",
            ),
            class_name="flex items-center justify-between mb-4",
        ),
        rx.el.p(s["name"], class_name="text-base font-semibold text-gray-900"),
        rx.el.p(s["contact"], class_name="text-sm text-gray-500 mt-1"),
        rx.el.div(
            rx.el.div(
                rx.icon("mail", class_name="h-3.5 w-3.5 text-gray-400"),
                rx.el.span(
                    s["email"], class_name="text-xs text-gray-600 truncate"
                ),
                class_name="flex items-center gap-2 min-w-0",
            ),
            rx.el.div(
                rx.icon("phone", class_name="h-3.5 w-3.5 text-gray-400"),
                rx.el.span(s["phone"], class_name="text-xs text-gray-600"),
                class_name="flex items-center gap-2",
            ),
            class_name="flex flex-col gap-1.5 mt-3",
        ),
        rx.el.div(
            rx.el.span(
                s["product_count"].to_string() + " productos",
                class_name="text-xs font-medium text-blue-700 bg-blue-50 px-2 py-1 rounded-full w-fit",
            ),
            class_name="mt-4 pt-4 border-t border-gray-100",
        ),
        class_name="bg-white border border-gray-200 rounded-xl p-5 hover:border-gray-300 transition-colors",
    )


def suppliers_empty() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("truck", class_name="h-6 w-6 text-gray-400"),
            class_name="h-12 w-12 rounded-xl bg-gray-100 flex items-center justify-center mb-4",
        ),
        rx.el.p(
            "No hay proveedores",
            class_name="text-sm font-medium text-gray-900 mb-1",
        ),
        rx.el.p(
            "Añade un proveedor para asociarlo a tus productos.",
            class_name="text-xs text-gray-500",
        ),
        class_name="flex flex-col items-center justify-center py-16 bg-white border border-gray-200 rounded-xl",
    )


def supplier_form_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        rx.cond(
                            DataState.is_editing_supplier,
                            "Editar proveedor",
                            "Nuevo proveedor",
                        ),
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Información de contacto del proveedor.",
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
                            default_value=DataState.editing_supplier["name"],
                            key=DataState.editing_supplier["id"].to_string()
                            + "_name",
                            placeholder="Ej. TechCorp",
                            class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Contacto",
                            class_name="block text-xs font-medium text-gray-700 mb-1.5",
                        ),
                        rx.el.input(
                            name="contact",
                            default_value=DataState.editing_supplier["contact"],
                            key=DataState.editing_supplier["id"].to_string()
                            + "_contact",
                            placeholder="Nombre del contacto",
                            class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                        ),
                        class_name="mb-3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Email",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.input(
                                name="email",
                                type="email",
                                default_value=DataState.editing_supplier[
                                    "email"
                                ],
                                key=DataState.editing_supplier["id"].to_string()
                                + "_email",
                                placeholder="email@ejemplo.com",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                            ),
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Teléfono",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.input(
                                name="phone",
                                default_value=DataState.editing_supplier[
                                    "phone"
                                ],
                                key=DataState.editing_supplier["id"].to_string()
                                + "_phone",
                                placeholder="+34 600 000 000",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-3 mb-4",
                    ),
                    rx.cond(
                        DataState.supplier_form_error != "",
                        rx.el.div(
                            rx.icon(
                                "triangle-alert",
                                class_name="h-4 w-4 text-red-500 shrink-0",
                            ),
                            rx.el.p(
                                DataState.supplier_form_error,
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
                            on_click=DataState.close_supplier_form,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                        ),
                        rx.el.button(
                            rx.cond(
                                DataState.is_editing_supplier,
                                "Guardar",
                                "Crear",
                            ),
                            type="submit",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t border-gray-100",
                    ),
                    on_submit=DataState.submit_supplier,
                    reset_on_submit=False,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-lg z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_supplier_form,
        on_open_change=DataState.close_supplier_form,
    )


def supplier_delete_dialog() -> rx.Component:
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
                        "Eliminar proveedor",
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "¿Eliminar '"
                        + DataState.selected_supplier["name"]
                        + "'? Solo se puede eliminar si no tiene productos asociados.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        on_click=DataState.close_delete_supplier,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    rx.el.button(
                        "Eliminar",
                        on_click=DataState.confirm_delete_supplier,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700",
                    ),
                    class_name="flex justify-end gap-2",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-md z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_supplier_delete,
        on_open_change=DataState.close_delete_supplier,
    )


def supplier_detail_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40"
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        DataState.selected_supplier["name"],
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Contacto: " + DataState.selected_supplier["contact"],
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4 pb-4 border-b border-gray-100",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p("Email", class_name="text-xs text-gray-500"),
                        rx.el.p(
                            DataState.selected_supplier["email"],
                            class_name="text-sm font-medium text-gray-900 mt-0.5",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p("Teléfono", class_name="text-xs text-gray-500"),
                        rx.el.p(
                            DataState.selected_supplier["phone"],
                            class_name="text-sm font-medium text-gray-900 mt-0.5",
                        ),
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Productos", class_name="text-xs text-gray-500"
                        ),
                        rx.el.p(
                            DataState.selected_supplier[
                                "product_count"
                            ].to_string(),
                            class_name="text-sm font-medium text-gray-900 mt-0.5",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cerrar",
                        on_click=DataState.close_supplier_detail,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    class_name="flex justify-end pt-4 border-t border-gray-100",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-lg z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_supplier_detail,
        on_open_change=DataState.close_supplier_detail,
    )


def proveedores_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Buscar proveedores...",
                    default_value=DataState.supplier_search,
                    on_change=DataState.set_supplier_search.debounce(300),
                    class_name="pl-9 pr-3 py-2 bg-white border border-gray-200 rounded-lg text-sm w-full md:w-72 focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                ),
                class_name="relative flex-1",
            ),
            rx.el.button(
                rx.icon("plus", class_name="h-4 w-4"),
                "Nuevo proveedor",
                on_click=DataState.open_new_supplier,
                class_name="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700",
            ),
            class_name="flex flex-col md:flex-row gap-3 mb-6",
        ),
        rx.cond(
            DataState.filtered_suppliers.length() == 0,
            suppliers_empty(),
            rx.el.div(
                rx.foreach(DataState.filtered_suppliers, supplier_card),
                class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4",
            ),
        ),
        supplier_form_dialog(),
        supplier_delete_dialog(),
        supplier_detail_dialog(),
    )


def proveedores_page() -> rx.Component:
    return authenticated_layout(
        proveedores_content(),
        title="Proveedores",
        subtitle="Administra tus proveedores y contactos",
    )
