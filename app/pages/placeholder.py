import reflex as rx
from app.components.layout import authenticated_layout
from app.states.auth_state import AuthState


def setting_row(
    icon: str, label: str, value: rx.Var | str, action_label: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-4 w-4 text-gray-600"),
                class_name="h-8 w-8 rounded-lg bg-gray-100 flex items-center justify-center shrink-0",
            ),
            rx.el.div(
                rx.el.p(label, class_name="text-sm font-medium text-gray-900"),
                rx.el.p(value, class_name="text-xs text-gray-500 mt-0.5"),
                class_name="min-w-0",
            ),
            class_name="flex items-center gap-3 min-w-0",
        ),
        class_name="flex items-center justify-between py-4 border-b border-gray-100 last:border-0",
    )


def configuracion_page() -> rx.Component:
    return authenticated_layout(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Perfil",
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.p(
                        "Información de tu cuenta",
                        class_name="text-xs text-gray-500 mt-0.5",
                    ),
                    class_name="mb-2",
                ),
                setting_row("user", "Nombre", AuthState.username),
                setting_row("mail", "Email", AuthState.email),
                setting_row("shield", "Rol", "Administrador"),
                class_name="bg-white border border-gray-200 rounded-xl p-5 mb-4",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h3(
                        "Sesión",
                        class_name="text-sm font-semibold text-gray-900",
                    ),
                    rx.el.p(
                        "Gestiona tu sesión activa",
                        class_name="text-xs text-gray-500 mt-0.5",
                    ),
                    class_name="mb-4",
                ),
                rx.el.button(
                    rx.icon("log-out", class_name="h-4 w-4"),
                    "Cerrar sesión",
                    on_click=AuthState.logout,
                    class_name="flex items-center gap-2 px-4 py-2 text-sm font-medium text-red-600 bg-red-50 hover:bg-red-100 rounded-lg transition-colors",
                ),
                class_name="bg-white border border-gray-200 rounded-xl p-5",
            ),
        ),
        title="Configuración",
        subtitle="Ajusta las preferencias de tu cuenta",
    )
