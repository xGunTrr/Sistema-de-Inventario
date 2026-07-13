import reflex as rx

class AuthState(rx.State):
    is_authenticated: bool = False
    username: str = ""
    email: str = ""
    login_error: str = ""
    is_loading: bool = False

    @rx.var
    def initials(self) -> str:
        if not self.username:
            return "?"
        parts = self.username.split(" ")
        if len(parts) > 1:
            return (parts[0][0] + parts[1][0]).upper()
        return self.username[:2].upper()

    @rx.event
    def login(self, form_data: dict):
        email = form_data.get("email", "").strip()
        password = form_data.get("password", "").strip()
        if not email or not password:
            self.login_error = "Por favor ingresa email y contraseña"
            return
        if "@" not in email:
            self.login_error = "El email no tiene un formato válido"
            return
        if len(password) < 3:
            self.login_error = "Contraseña muy corta"
            return
        self.is_authenticated = True
        self.email = email
        self.username = email.split("@")[0].replace(".", " ").title()
        self.login_error = ""
        return [
            rx.redirect("/dashboard"),
            rx.toast(
                title=f"Bienvenido, {self.username}",
                description="Sesión iniciada correctamente.",
                duration=3000,
                close_button=True,
            ),
        ]

    @rx.event
    def logout(self):
        name = self.username
        self.is_authenticated = False
        self.username = ""
        self.email = ""
        return [
            rx.redirect("/"),
            rx.toast(
                title="Sesión cerrada",
                description=f"Hasta pronto, {name}." if name else "",
                duration=3000,
                close_button=True,
            ),
        ]

    @rx.event
    def check_auth(self):
        if not self.is_authenticated:
            return rx.redirect("/")
