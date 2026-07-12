import reflex as rx
from app.states.auth_state import AuthState


def login_page() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("box", class_name="h-6 w-6 text-white"),
                        class_name="h-12 w-12 rounded-xl bg-blue-600 flex items-center justify-center mb-6",
                    ),
                    rx.el.h1(
                        "Bienvenido de nuevo",
                        class_name="text-2xl font-semibold text-gray-900",
                    ),
                    rx.el.p(
                        "Ingresa tus credenciales para acceder al sistema de inventario",
                        class_name="text-sm text-gray-500 mt-2 mb-8",
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.el.label(
                                "Email",
                                class_name="block text-sm font-medium text-gray-700 mb-1.5",
                            ),
                            rx.el.input(
                                type="email",
                                name="email",
                                placeholder="tu@empresa.com",
                                default_value="admin@empresa.com",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.label(
                                    "Contraseña",
                                    class_name="block text-sm font-medium text-gray-700",
                                ),
                                rx.el.a(
                                    "¿Olvidaste?",
                                    href="#",
                                    class_name="text-xs text-blue-600 hover:text-blue-700",
                                ),
                                class_name="flex justify-between items-center mb-1.5",
                            ),
                            rx.el.input(
                                type="password",
                                name="password",
                                placeholder="••••••••",
                                default_value="admin123",
                                class_name="w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500 focus:border-transparent",
                            ),
                            class_name="mb-4",
                        ),
                        rx.cond(
                            AuthState.login_error != "",
                            rx.el.div(
                                rx.icon(
                                    "triangle-alert",
                                    class_name="h-4 w-4 text-red-500 shrink-0",
                                ),
                                rx.el.p(
                                    AuthState.login_error,
                                    class_name="text-sm text-red-700",
                                ),
                                class_name="flex items-center gap-2 p-3 bg-red-50 border border-red-100 rounded-lg mb-4",
                            ),
                            rx.fragment(),
                        ),
                        rx.el.div(
                            rx.el.input(
                                type="checkbox",
                                name="remember",
                                class_name="h-4 w-4 text-blue-600 border-gray-300 rounded",
                            ),
                            rx.el.label(
                                "Mantener sesión iniciada",
                                class_name="text-sm text-gray-600",
                            ),
                            class_name="flex items-center gap-2 mb-6",
                        ),
                        rx.el.button(
                            "Iniciar sesión",
                            rx.icon("arrow-right", class_name="h-4 w-4 ml-2"),
                            type="submit",
                            class_name="w-full flex items-center justify-center px-4 py-2.5 bg-blue-600 text-white text-sm font-medium rounded-lg hover:bg-blue-700 transition-colors",
                        ),
                        on_submit=AuthState.login,
                    ),
                    rx.el.div(
                        rx.el.div(class_name="flex-1 h-px bg-gray-200"),
                        rx.el.span("o", class_name="text-xs text-gray-400"),
                        rx.el.div(class_name="flex-1 h-px bg-gray-200"),
                        class_name="flex items-center gap-3 my-6",
                    ),
                    rx.el.p(
                        "¿No tienes cuenta? ",
                        rx.el.a(
                            "Contacta al administrador",
                            href="#",
                            class_name="text-blue-600 hover:text-blue-700 font-medium",
                        ),
                        class_name="text-sm text-gray-600 text-center",
                    ),
                    class_name="p-8",
                ),
                class_name="w-full max-w-md bg-white rounded-2xl border border-gray-200 shadow-sm",
            ),
            rx.el.p(
                "© 2024 Sistema de Inventario. Todos los derechos reservados.",
                class_name="text-xs text-gray-400 mt-8 text-center",
            ),
            class_name="flex flex-col items-center justify-center min-h-screen p-4",
        ),
        class_name="min-h-screen bg-gray-50 font-['Inter']",
    )
