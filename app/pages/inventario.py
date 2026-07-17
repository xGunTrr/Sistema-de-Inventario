import reflex as rx
from app.components.layout import authenticated_layout
from app.states.data_state import DataState, Inventario

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
                    placeholder="Buscar por producto o almacén...",
                    default_value=DataState.inventario_search,
                    on_change=DataState.set_inventario_search.debounce(300),
                    class_name="pl-9 pr-3 py-2 bg-white border border-gray-200 rounded-lg text-sm w-full md:w-72 focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                    color="black",
                ),
                class_name="relative",
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("Todos los productos", value="Todos"),
                    rx.foreach(
                        DataState.producto_filter_options,
                        lambda o: rx.el.option(o["label"], value=o["value"]),
                    ),
                    default_value=DataState.producto_filter,
                    on_change=DataState.set_producto_filter,
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
                    rx.el.option("Todos los almacenes", value="Todos"),
                    rx.foreach(
                        DataState.almacen_filter_options,
                        lambda o: rx.el.option(o["label"], value=o["value"]),
                    ),
                    default_value=DataState.almacen_filter,
                    on_change=DataState.set_almacen_filter,
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
                on_click=DataState.clear_inventario_filters,
                class_name="flex items-center gap-1.5 px-3 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg transition-colors",
            ),
            class_name="flex flex-wrap items-center gap-2 flex-1",
        ),
        rx.el.button(
            rx.icon("plus", class_name="h-4 w-4"),
            "Nuevo inventario",
            on_click=DataState.open_new_inventario,
            class_name="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors shrink-0",
        ),
        class_name="flex flex-col md:flex-row md:items-center gap-3 mb-4",
    )


def inventario_row(inv: Inventario, idx: rx.Var[int]) -> rx.Component:
    prod = inv["producto"]
    alm = inv["almacen"]
    prod_name = rx.cond(prod, rx.cond(prod["NombreProducto"], prod["NombreProducto"], "N/A"), "N/A")
    alm_name = rx.cond(alm, rx.cond(alm["NombreAlmacen"], alm["NombreAlmacen"], "N/A"), "N/A")
    return rx.el.tr(
        rx.el.td(
            rx.el.p((idx + 1).to_string(), class_name="text-sm text-gray-700"),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(prod_name, class_name="text-sm font-medium text-gray-900"),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(alm_name, class_name="text-sm text-gray-700"),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.cond(
                inv["CantidadDisponible"] <= inv["StockMinimo"],
                rx.el.div(
                    rx.icon(
                        "triangle-alert", class_name="h-3.5 w-3.5 text-red-500"
                    ),
                    rx.el.span(
                        inv["CantidadDisponible"].to_string(),
                        class_name="text-sm font-semibold text-red-600",
                    ),
                    class_name="flex items-center gap-1.5",
                ),
                rx.el.span(
                    inv["CantidadDisponible"].to_string(),
                    class_name="text-sm text-gray-700",
                ),
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(inv["StockMinimo"].to_string(), class_name="text-sm text-gray-700"),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(inv["StockMaximo"].to_string(), class_name="text-sm text-gray-700"),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.p(inv["PuntoReorden"].to_string(), class_name="text-sm text-gray-700"),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.cond(
                inv["CantidadDisponible"] <= inv["StockMinimo"],
                rx.el.span(
                    "Bajo",
                    class_name="text-xs font-medium text-red-700 bg-red-50 px-2 py-1 rounded-full",
                ),
                rx.el.span(
                    "OK",
                    class_name="text-xs font-medium text-green-700 bg-green-50 px-2 py-1 rounded-full",
                ),
            ),
            class_name="px-4 py-3",
        ),
        rx.el.td(
            rx.el.div(
                rx.el.button(
                    rx.icon("eye", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_inventario_detail(inv),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors",
                    title="Ver",
                ),
                rx.el.button(
                    rx.icon("pencil", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_edit_inventario(inv),
                    class_name="p-1.5 text-gray-500 hover:text-blue-600 hover:bg-blue-50 rounded transition-colors",
                    title="Editar",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=lambda: DataState.open_delete_inventario(inv),
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
            rx.icon("database", class_name="h-6 w-6 text-gray-400"),
            class_name="h-12 w-12 rounded-xl bg-gray-100 flex items-center justify-center mb-4",
        ),
        rx.el.p(
            "No hay registros de inventario",
            class_name="text-sm font-medium text-gray-900 mb-1",
        ),
        rx.el.p(
            "Intenta ajustar los filtros o crea un registro nuevo.",
            class_name="text-xs text-gray-500",
        ),
        class_name="flex flex-col items-center justify-center py-16",
    )

def inventarios_table() -> rx.Component:
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
                            "Producto",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Almacén",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Disponible",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Mín",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Máx",
                            class_name="px-4 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "P. Reorden",
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
                    rx.foreach(DataState.filtered_inventarios, inventario_row),
                ),
                class_name="table-auto w-full",
            ),
            class_name="overflow-x-auto",
        ),
        rx.cond(
            DataState.filtered_inventarios.length() == 0,
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

def inventario_detail_dialog() -> rx.Component:
    prod = DataState.selected_inventario["producto"]
    alm = DataState.selected_inventario["almacen"]
    prod_name = rx.cond(prod, rx.cond(prod["NombreProducto"], prod["NombreProducto"], "N/A"), "N/A")
    alm_name = rx.cond(alm, rx.cond(alm["NombreAlmacen"], alm["NombreAlmacen"], "N/A"), "N/A")
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        "Detalle de Inventario #" + DataState.selected_inventario["IdInventario"].to_string(),
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Información completa del registro de inventario.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4 pb-4 border-b border-gray-100",
                ),
                rx.el.div(
                    detail_row("Producto", prod_name),
                    detail_row("Almacén", alm_name),
                    detail_row(
                        "Cantidad disponible",
                        DataState.selected_inventario["CantidadDisponible"].to_string(),
                    ),
                    detail_row(
                        "Stock mínimo",
                        DataState.selected_inventario["StockMinimo"].to_string(),
                    ),
                    detail_row(
                        "Stock máximo",
                        DataState.selected_inventario["StockMaximo"].to_string(),
                    ),
                    detail_row(
                        "Punto de reorden",
                        DataState.selected_inventario["PuntoReorden"].to_string(),
                    ),
                    detail_row(
                        "Estado",
                        rx.cond(
                            DataState.selected_inventario["CantidadDisponible"]
                            <= DataState.selected_inventario["StockMinimo"],
                            "Stock Bajo",
                            "OK",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cerrar",
                        on_click=DataState.close_inventario_detail,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    rx.el.button(
                        rx.icon("pencil", class_name="h-4 w-4"),
                        "Editar",
                        on_click=[
                            DataState.close_inventario_detail,
                            lambda: DataState.open_edit_inventario(
                                DataState.selected_inventario
                            ),
                        ],
                        class_name="flex items-center gap-2 px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700",
                    ),
                    class_name="flex justify-end gap-2 pt-4 border-t border-gray-100",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-lg z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_inventario_detail,
        on_open_change=DataState.close_inventario_detail,
    )


def inventario_delete_dialog() -> rx.Component:
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
                        "Eliminar inventario",
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "¿Seguro que deseas eliminar el inventario #"
                        + DataState.selected_inventario["IdInventario"].to_string()
                        + "? Esta acción no se puede deshacer.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancelar",
                        on_click=DataState.close_delete_inventario,
                        class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50",
                    ),
                    rx.el.button(
                        "Eliminar",
                        on_click=DataState.confirm_delete_inventario,
                        class_name="px-4 py-2 text-sm font-medium text-white bg-red-600 rounded-lg hover:bg-red-700",
                    ),
                    class_name="flex justify-end gap-2",
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-md z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_inventario_delete,
        on_open_change=DataState.close_delete_inventario,
    )


def inventario_form_dialog() -> rx.Component:
    inv = DataState.editing_inventario
    default_prod_id = inv["IdProducto"].to_string()
    default_alm_id = inv["IdAlmacen"].to_string()
    return rx.radix.primitives.dialog.root(
        rx.radix.primitives.dialog.portal(
            rx.radix.primitives.dialog.overlay(
                class_name="fixed inset-0 bg-black/40 backdrop-blur-sm z-40",
            ),
            rx.radix.primitives.dialog.content(
                rx.el.div(
                    rx.radix.primitives.dialog.title(
                        rx.cond(
                            DataState.is_editing_inventario,
                            "Editar inventario",
                            "Nuevo inventario",
                        ),
                        class_name="text-lg font-semibold text-gray-900",
                    ),
                    rx.radix.primitives.dialog.description(
                        "Completa la información del inventario.",
                        class_name="text-sm text-gray-500 mt-1",
                    ),
                    class_name="mb-4",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Producto",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option("Seleccionar producto", value=""),
                                    rx.foreach(
                                        DataState.producto_filter_options,
                                        lambda o: rx.el.option(o["label"], value=o["value"]),
                                    ),
                                    name="IdProducto",
                                    default_value=default_prod_id,
                                    key=inv["IdInventario"].to_string() + "_IdProducto",
                                    class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm appearance-none focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                    color="black",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                            class_name="mb-3",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Almacén",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.div(
                                rx.el.select(
                                    rx.el.option("Seleccionar almacén", value=""),
                                    rx.foreach(
                                        DataState.almacen_filter_options,
                                        lambda o: rx.el.option(o["label"], value=o["value"]),
                                    ),
                                    name="IdAlmacen",
                                    default_value=default_alm_id,
                                    key=inv["IdInventario"].to_string() + "_IdAlmacen",
                                    class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm appearance-none focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                    color="black",
                                ),
                                rx.icon(
                                    "chevron-down",
                                    class_name="h-4 w-4 text-gray-400 absolute right-2 top-1/2 -translate-y-1/2 pointer-events-none",
                                ),
                                class_name="relative",
                            ),
                            class_name="mb-3",
                        ),
                        class_name="grid grid-cols-2 gap-3",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Cantidad Disponible",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.input(
                                name="CantidadDisponible",
                                type="number",
                                min="0",
                                default_value=inv["CantidadDisponible"].to_string(),
                                key=inv["IdInventario"].to_string() + "_CD",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                            class_name="mb-3",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Stock Mínimo",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.input(
                                name="StockMinimo",
                                type="number",
                                min="0",
                                default_value=inv["StockMinimo"].to_string(),
                                key=inv["IdInventario"].to_string() + "_SMin",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                            class_name="mb-3",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Stock Máximo",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.input(
                                name="StockMaximo",
                                type="number",
                                min="0",
                                default_value=inv["StockMaximo"].to_string(),
                                key=inv["IdInventario"].to_string() + "_SMax",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                            class_name="mb-3",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Punto de Reorden",
                                class_name="block text-xs font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.input(
                                name="PuntoReorden",
                                type="number",
                                min="0",
                                default_value=inv["PuntoReorden"].to_string(),
                                key=inv["IdInventario"].to_string() + "_PR",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500",
                                color="black",
                            ),
                            class_name="mb-3",
                        ),
                        class_name="grid grid-cols-2 gap-3 mb-4",
                    ),
                    rx.cond(
                        DataState.inventario_form_error != "",
                        rx.el.div(
                            rx.icon(
                                "triangle-alert",
                                class_name="h-4 w-4 text-red-500 shrink-0",
                            ),
                            rx.el.p(
                                DataState.inventario_form_error,
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
                            on_click=DataState.close_inventario_form,
                            class_name="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-200 rounded-lg hover:bg-gray-50 transition-colors",
                        ),
                        rx.el.button(
                            rx.cond(
                                DataState.is_editing_inventario,
                                "Guardar cambios",
                                "Crear inventario",
                            ),
                            type="submit",
                            class_name="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-lg hover:bg-blue-700 transition-colors",
                        ),
                        class_name="flex justify-end gap-2 pt-4 border-t border-gray-100",
                    ),
                    on_submit=DataState.submit_inventario,
                    reset_on_submit=False,
                ),
                class_name="fixed top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 bg-white rounded-xl shadow-xl p-6 w-full max-w-lg z-50 font-['Inter']",
            ),
        ),
        open=DataState.show_inventario_form,
        on_open_change=DataState.close_inventario_form,
    )


def inventarios_content() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            stat_pill(
                "Total inventario",
                DataState.total_inventarios.to_string(),
                "text-gray-900",
            ),
            stat_pill(
                "Filtrados",
                DataState.filtered_inventarios.length().to_string(),
                "text-blue-600",
            ),
            stat_pill(
                "Stock bajo",
                DataState.stock_bajo_count.to_string(),
                "text-red-600",
            ),
            stat_pill(
                "Stock OK",
                DataState.stock_ok_count.to_string(),
                "text-emerald-600",
            ),
            class_name="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6",
        ),
        toolbar(),
        inventarios_table(),
        inventario_form_dialog(),
        inventario_delete_dialog(),
        inventario_detail_dialog(),
    )

def inventario_page() -> rx.Component:
    return authenticated_layout(
        inventarios_content(),
        title="Inventario",
        subtitle="Controla el stock de tus productos",
    )
