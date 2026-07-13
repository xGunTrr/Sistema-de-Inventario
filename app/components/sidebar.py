import reflex as rx
from app.states.auth_state import AuthState

def nav_link(
    icon: str, label: str, href: str, active: bool = False
) -> rx.Component:
    return rx.el.a(
        rx.icon(icon, class_name="h-4 w-4"),
        rx.el.span(label, class_name="text-sm font-medium"),
        href=href,
        class_name=rx.cond(
            rx.State.router.page.path == href,
            "flex items-center gap-3 px-3 py-2 rounded-lg bg-blue-50 text-blue-700 transition-colors",
            "flex items-center gap-3 px-3 py-2 rounded-lg text-gray-600 hover:bg-gray-100 hover:text-gray-900 transition-colors",
        ),
    )

def sidebar() -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon("box", class_name="h-5 w-5 text-white"),
                    class_name="h-8 w-8 rounded-lg bg-blue-600 flex items-center justify-center",
                ),
                rx.el.div(
                    rx.el.p(
                        "Inventario",
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.p(
                        "Sistema de gestión", class_name="text-xs text-gray-500"
                    ),
                ),
                class_name="flex items-center gap-3 px-4 py-4 border-b border-gray-200",
            ),
            rx.el.nav(
                rx.el.div(
                    rx.el.p(
                        "PRINCIPAL",
                        class_name="px-3 py-2 text-xs font-semibold text-gray-400 tracking-wider",
                    ),
                    nav_link("layout-dashboard", "Dashboard", "/dashboard"),
                    nav_link("package", "Productos", "/productos"),
                    nav_link("tag", "Tipos", "/tipos"),
                    nav_link("truck", "Proveedores", "/proveedores"),
                    class_name="flex flex-col gap-1",
                ),
                rx.el.div(
                    rx.el.p(
                        "SISTEMA",
                        class_name="px-3 py-2 mt-4 text-xs font-semibold text-gray-400 tracking-wider",
                    ),
                    nav_link("settings", "Configuración", "/configuracion"),
                    class_name="flex flex-col gap-1",
                ),
                class_name="flex flex-col p-3 flex-1",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.span(
                                AuthState.initials,
                                class_name="text-xs font-semibold text-blue-700",
                            ),
                            class_name="h-9 w-9 rounded-full bg-blue-50 flex items-center justify-center shrink-0",
                        ),
                        rx.el.div(
                            rx.el.p(
                                AuthState.username,
                                class_name="text-sm font-medium text-gray-900 truncate",
                            ),
                            rx.el.p(
                                AuthState.email,
                                class_name="text-xs text-gray-500 truncate",
                            ),
                            class_name="flex-1 min-w-0",
                        ),
                        rx.el.button(
                            rx.icon("log-out", class_name="h-4 w-4"),
                            on_click=AuthState.logout,
                            class_name="p-2 text-gray-500 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors shrink-0",
                            title="Cerrar sesión",
                        ),
                        class_name="flex items-center gap-3",
                    ),
                    class_name="p-4 border-t border-gray-200",
                ),
                class_name="flex flex-col h-full",
            ),
            class_name="w-64 h-screen bg-white border-r border-gray-200 shrink-0 hidden md:flex flex-col sticky top-0",
        ),
    )
