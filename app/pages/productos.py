import reflex as rx
from app.components.layout import authenticated_layout
from app.states.data_state import DataState, Product

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
                    placeholder="Buscar por nombre o SKU...",
                    default_value=DataState.product_search,
                    on_change=DataState.set_product_search.debounce(300),
                    class_name="pl-9 pr-3 py-2 bg-white border border-gray-200 rounded-lg text-sm w-full md:w-72 focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                    color="black",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.select(
                    rx.foreach(
                        DataState.type_filter_options,
                        lambda o: rx.el.option(o, value=o),
                    ),
                    default_value=DataState.product_type_filter,
                    on_change=DataState.set_product_type_filter,
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
                    rx.foreach(
                        DataState.supplier_filter_options,
                        lambda o: rx.el.option(o, value=o),
                    ),
                    default_value=DataState.product_supplier_filter,
                    on_change=DataState.set_product_supplier_filter,
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
                    rx.el.option("Stock bajo", value="Bajo"),
                    rx.el.option("Stock OK", value="OK"),
                    default_value=DataState.product_stock_filter,
                    on_change=DataState.set_product_stock_filter,
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
                on_click=DataState.clear_product_filters,
                class_name="flex items-center gap-1.5 px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg transition-colors",
            ),
            class_name="flex flex-wrap items-center gap-2 flex-1",
        ),
        rx.el.button(
            rx.icon("plus", class_name="h-4 w-4"),
            "Nuevo producto",
            on_click=DataState.open_new_product,
            class_name="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors shrink-0",
        ),
        class_name="flex flex-col md:flex-row md:items-center gap-3 mb-4",
    )


def product_row(p: Product) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    p["name"], class_name="text-sm font-medium text-gray-900"
                ),
                rx.el.p(f"SKU: {p['sku']}", class_name="text-xs text-gray-500"),
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.span(
                p["type"],
                class_name="text-xs font-medium text-blue-700 bg-blue-50 px-2 py-1 rounded-full w-fit",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(p["supplier"], class_name="text-sm text-gray-700"),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.cond(
                p["stock"] < p["min_stock"],
                rx.el.div(
                    rx.icon(
                        "triangle-alert", class_name="h-3.5 w-3.5 text-red-500"
                    ),
                    rx.el.span(
                        p["stock"].to_string()
                        + " / "
                        + p["min_stock"].to_string(),
                        class_name="text-sm font-semibold text-red-600",
                    ),
                    class_name="flex items-center gap-1.5",
                ),
                rx.el.span(
                    p["stock"].to_string() + " / " + p["min_stock"].to_string(),
                    class_name="text-sm text-gray-700",
                ),
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(
                "S/." + p["price"].to_string(),
                class_name="text-sm font-medium text-gray-900",
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("eye", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_product_detail(p),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors",
                    title="Ver",
                ),
                rx.el.button(
                    rx.icon("pencil", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_edit_product(p),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors",
                    title="Editar",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_delete_product(p),
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
            rx.icon("package", class_name="h-6 w-6 text-gray-400"),
            class_name="h-12 w-12 rounded-xl bg-gray-100 flex items-center justify-center mb-4",
        ),
        rx.el.p(
            "No hay productos que coincidan",
            class_name="text-sm font-medium text-gray-900 mb-1",
        ),
        rx.el.p(
            "Intenta ajustar los filtros o crea un producto nuevo.",
            class_name="text-xs text-gray-500",
        ),
        class_name="flex flex-col items-center justify-center py-16",
    )

def products_table() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th(
                            "Producto",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Tipo",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Proveedor",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Stock",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Precio",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th("", class_name="px-4 py-3"),
                        class_name="bg-gray-50 border-b border-gray-200",
                    ),
                ),
                rx.el.tbody(
                    rx.foreach(DataState.filtered_products, product_row),
                ),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        rx.cond(
            DataState.filtered_products.length() == 0,
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


def product_form_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        rx.cond(
                            DataState.is_editing_product,
                            "Editar producto",
                            "Nuevo producto",
                        ),
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Completa la información del producto.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4",
                ),
                rx.el.form(
                    rx.el.div(
                        form_field(
                            "Nombre",
                            rx.el.input(
                                name="name",
                                default_value=DataState.editing_product["name"],
                                key=DataState.editing_product["id"].to_string()
                                + "_name",
                                placeholder="Ej. Laptop Pro",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                        ),
                        form_field(
                            "SKU",
                            rx.el.input(
                                name="sku",
                                default_value=DataState.editing_product["sku"],
                                key=DataState.editing_product["id"].to_string()
                                + "_sku",
                                placeholder="Ej. LP-001",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                        ),
                        class_name="grid grid-cols-2 gap-3 mb-3",
                    ),
                    rx.el.div(
                        form_field(
                            "Tipo",
                            rx.el.div(
                                rx.el.select(
                                    rx.foreach(
                                        DataState.type_names,
                                        lambda n: rx.el.option(n, value=n),
                                    ),
                                    name="type",
                                    default_value=DataState.editing_product[
                                        "type"
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
                        form_field(
                            "Proveedor",
                            rx.el.div(
                                rx.el.select(
                                    rx.foreach(
                                        DataState.supplier_names,
                                        lambda n: rx.el.option(n, value=n),
                                    ),
                                    name="supplier",
                                    default_value=DataState.editing_product[
                                        "supplier"
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
                        class_name="grid grid-cols-2 gap-3 mb-3",
                    ),
                    rx.el.div(
                        form_field(
                            "Stock",
                            rx.el.input(
                                name="stock",
                                type="number",
                                min="0",
                                default_value=DataState.editing_product[
                                    "stock"
                                ].to_string(),
                                key=DataState.editing_product["id"].to_string()
                                + "_stock",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                        ),
                        form_field(
                            "Stock mínimo",
                            rx.el.input(
                                name="min_stock",
                                type="number",
                                min="0",
                                default_value=DataState.editing_product[
                                    "min_stock"
                                ].to_string(),
                                key=DataState.editing_product["id"].to_string()
                                + "_ms",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                        ),
                        form_field(
                            "Precio (S/.)",
                            rx.el.input(
                                name="price",
                                type="number",
                                min="0",
                                step="0.01",
                                default_value=DataState.editing_product[
                                    "price"
                                ].to_string(),
                                key=DataState.editing_product["id"].to_string()
                                + "_price",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                        ),
                        class_name="grid grid-cols-3 gap-3 mb-4",
                    ),
                    rx.cond(
                        DataState.product_form_error != "",
                        rx.el.div(
                            rx.icon(
                                "triangle-alert",
                                class_name="h-4 w-4 text-red-500 shrink-0",
                            ),
                            rx.el.p(
                                DataState.product_form_error,
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
                            on_click=DataState.close_product_form,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors",
                        ),
                        rx.el.button(
                            rx.cond(
                                DataState.is_editing_product,
                                "Guardar cambios",
                                "Crear producto",
                            ),
                            type="submit",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t border-gray-100",
                    ),
                    on_submit=DataState.submit_product,
                    reset_on_submit=False,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-lg z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_product_form,
        on_open_change=DataState.close_product_form,
    )


def product_delete_dialog() -> rx.Component:
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
                        "Eliminar producto",
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "¿Seguro que deseas eliminar '"
                        + DataState.selected_product["name"]
                        + "'? Esta acción no se puede deshacer.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        on_click=DataState.close_delete_product,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    rx.el.button(
                        "Eliminar",
                        on_click=DataState.confirm_delete_product,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700",
                    ),
                    class_name="flex justify-end gap-2",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-md z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_product_delete,
        on_open_change=DataState.close_delete_product,
    )


def detail_row(label: str, value: rx.Var | str) -> rx.Component:
    return rx.el.div(
        rx.el.p(label, class_name="text-xs text-gray-500"),
        rx.el.p(value, class_name="text-sm font-medium text-gray-900 mt-0.5"),
        class_name="",
    )

def product_detail_dialog() -> rx.Component:
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        DataState.selected_product["name"],
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "SKU: " + DataState.selected_product["sku"],
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4 pb-4 border-b border-gray-100",
                ),
                rx.el.div(
                    detail_row("Tipo", DataState.selected_product["type"]),
                    detail_row(
                        "Proveedor", DataState.selected_product["supplier"]
                    ),
                    detail_row(
                        "Stock actual",
                        DataState.selected_product["stock"].to_string(),
                    ),
                    detail_row(
                        "Stock mínimo",
                        DataState.selected_product["min_stock"].to_string(),
                    ),
                    detail_row(
                        "Precio",
                        "$" + DataState.selected_product["price"].to_string(),
                    ),
                    detail_row(
                        "Valor total",
                        "S/."
                        + (
                            DataState.selected_product["price"]
                            * DataState.selected_product["stock"]
                        ).to_string(),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cerrar",
                        on_click=DataState.close_product_detail,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    rx.el.button(
                        rx.icon("pencil", class_name="h-4 w-4"),
                        "Editar",
                        on_click=[
                            DataState.close_product_detail,
                            lambda: DataState.open_edit_product(
                                DataState.selected_product
                            ),
                        ],
                        class_name="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700",
                    ),
                    class_name="flex justify-end gap-2 pt-4 border-t border-gray-100",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-lg z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_product_detail,
        on_open_change=DataState.close_product_detail,
    )


def productos_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stat_pill(
                "Total productos",
                DataState.total_products.to_string(),
                "text-gray-900",
            ),
            stat_pill(
                "Filtrados",
                DataState.filtered_products.length().to_string(),
                "text-blue-600",
            ),
            stat_pill(
                "Stock crítico",
                DataState.low_stock_count.to_string(),
                "text-red-600",
            ),
            stat_pill(
                "Valor inventario",
                "S/." + DataState.total_stock_value.to_string(),
                "text-emerald-600",
            ),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6",
        ),
        toolbar(),
        products_table(),
        product_form_dialog(),
        product_delete_dialog(),
        product_detail_dialog(),
    )

def productos_page() -> rx.Component:
    return authenticated_layout(
        productos_content(),
        title="Productos",
        subtitle="Gestiona tu catálogo de productos",
    )
