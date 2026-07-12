import reflex as rx
from app.components.sidebar import sidebar
from app.states.auth_state import AuthState


def page_header(title: str, subtitle: str) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h1(title, class_name="text-2xl font-semibold text-gray-900"),
            rx.el.p(subtitle, class_name="text-sm text-gray-500 mt-1"),
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2",
                ),
                rx.el.input(
                    placeholder="Buscar...",
                    class_name="pl-9 pr-3 py-2 bg-white border border-gray-200 rounded-lg text-sm focus:outline-hidden focus:ring-2 focus:ring-blue-500 focus:border-transparent w-64",
                ),
                class_name="relative hidden md:block",
            ),
            rx.el.button(
                rx.icon("bell", class_name="h-4 w-4"),
                class_name="p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors relative",
            ),
            class_name="flex items-center gap-2",
        ),
        class_name="flex items-start justify-between mb-6",
    )


def authenticated_layout(
    content: rx.Component, title: str = "", subtitle: str = ""
) -> rx.Component:
    return rx.el.div(
        sidebar(),
        rx.el.main(
            rx.el.div(
                page_header(title, subtitle),
                content,
                class_name="max-w-7xl mx-auto p-6 md:p-8",
            ),
            class_name="flex-1 min-w-0 bg-gray-50 min-h-screen",
        ),
        class_name="flex min-h-screen bg-gray-50 font-['Inter']",
    )
