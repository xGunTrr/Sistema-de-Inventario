import reflex as rx
import httpx
from typing import TypedDict

class Product(TypedDict):
    id: int
    name: str
    sku: str
    type: str
    supplier: str
    stock: int
    min_stock: int
    price: float

class ProductType(TypedDict):
    id: int
    name: str
    description: str
    product_count: int

class Supplier(TypedDict):
    id: int
    name: str
    contact: str
    email: str
    phone: str
    product_count: int

EMPTY_PRODUCT: Product = {
    "id": 0,
    "name": "",
    "sku": "",
    "type": "",
    "supplier": "",
    "stock": 0,
    "min_stock": 0,
    "price": 0.0,
}

EMPTY_TYPE: ProductType = {
    "id": 0,
    "name": "",
    "description": "",
    "product_count": 0,
}

EMPTY_SUPPLIER: Supplier = {
    "id": 0,
    "name": "",
    "contact": "",
    "email": "",
    "phone": "",
    "product_count": 0,
}

API_URL = "http://localhost:8000/api"

class DataState(rx.State):
    products = []
    product_types: list[ProductType] = []
    suppliers: list[Supplier] = []

    @rx.event
    async def load_products(self):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(f"{API_URL}/products")

            response.raise_for_status()

            self.products = [
                self.normalize_product(product)
                for product in response.json().get("data", [])
            ]

        except httpx.RequestError as error:
            print(f"Error de conexión: {error}")

        except httpx.HTTPStatusError as error:
            print(f"Error HTTP: {error.response.text}")

    @rx.event
    async def load_types(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/types")

        if response.status_code == 200:
            self.product_types = response.json()["data"]

    @rx.event
    async def load_suppliers(self):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/suppliers")

        if response.status_code == 200:
            self.suppliers = response.json()["data"]

    @rx.event
    async def load_data(self):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                products_response = await client.get(
                    f"{API_URL}/products"
                )
                types_response = await client.get(
                    f"{API_URL}/types"
                )
                suppliers_response = await client.get(
                    f"{API_URL}/suppliers"
                )

            products_response.raise_for_status()
            types_response.raise_for_status()
            suppliers_response.raise_for_status()

            products_data = products_response.json().get("data", [])

            self.products = [
                self.normalize_product(product)
                for product in products_data
            ]

            self.product_types = types_response.json().get("data", [])
            self.suppliers = suppliers_response.json().get("data", [])

        except httpx.RequestError as error:
            print(f"No se pudo conectar con la API: {error}")

        except httpx.HTTPStatusError as error:
            print(f"Error HTTP: {error.response.text}")

        except Exception as error:
            print(f"Error inesperado cargando datos: {error}")

    @rx.var
    def total_products(self) -> int:
        return len(self.products)

    @rx.var
    def total_types(self) -> int:
        return len(self.product_types)

    @rx.var
    def total_suppliers(self) -> int:
        return len(self.suppliers)

    @rx.var
    def total_stock_value(self) -> float:
        return round(sum(p["stock"] * p["price"] for p in self.products), 2)

    @rx.var
    def low_stock_products(self) -> list[Product]:
        return [p for p in self.products if p["stock"] < p["min_stock"]]

    @rx.var
    def low_stock_count(self) -> int:
        return len(self.low_stock_products)

    @rx.var
    def type_distribution(self) -> list[dict[str, str | int]]:
        return [
            {"name": t["name"], "value": t["product_count"]}
            for t in self.product_types
        ]

    @rx.var
    def top_suppliers(self) -> list[Supplier]:
        sorted_s = sorted(
            self.suppliers, key=lambda s: s["product_count"], reverse=True
        )
        return sorted_s[:4]

    product_search: str = ""
    product_type_filter: str = "Todos"
    product_supplier_filter: str = "Todos"
    product_stock_filter: str = "Todos"

    type_search: str = ""
    supplier_search: str = ""

    show_product_form: bool = False
    show_product_delete: bool = False
    show_product_detail: bool = False
    editing_product: Product = EMPTY_PRODUCT
    selected_product: Product = EMPTY_PRODUCT
    is_editing_product: bool = False
    product_form_error: str = ""

    show_type_form: bool = False
    show_type_delete: bool = False
    show_type_detail: bool = False
    editing_type: ProductType = EMPTY_TYPE
    selected_type: ProductType = EMPTY_TYPE
    is_editing_type: bool = False
    type_form_error: str = ""

    show_supplier_form: bool = False
    show_supplier_delete: bool = False
    show_supplier_detail: bool = False
    editing_supplier: Supplier = EMPTY_SUPPLIER
    selected_supplier: Supplier = EMPTY_SUPPLIER
    is_editing_supplier: bool = False
    supplier_form_error: str = ""

    @rx.var
    def type_names(self) -> list[str]:
        return [t["name"] for t in self.product_types]

    @rx.var
    def supplier_names(self) -> list[str]:
        return [s["name"] for s in self.suppliers]

    @rx.var
    def type_filter_options(self) -> list[str]:
        return ["Todos"] + [t["name"] for t in self.product_types]

    @rx.var
    def supplier_filter_options(self) -> list[str]:
        return ["Todos"] + [s["name"] for s in self.suppliers]

    @rx.var
    def filtered_products(self) -> list[Product]:
        q = self.product_search.lower().strip()
        result = []
        for p in self.products:
            if q and q not in p["name"].lower() and q not in p["sku"].lower():
                continue
            if (
                self.product_type_filter != "Todos"
                and p["type"] != self.product_type_filter
            ):
                continue
            if (
                self.product_supplier_filter != "Todos"
                and p["supplier"] != self.product_supplier_filter
            ):
                continue
            if (
                self.product_stock_filter == "Bajo"
                and p["stock"] >= p["min_stock"]
            ):
                continue
            if (
                self.product_stock_filter == "OK"
                and p["stock"] < p["min_stock"]
            ):
                continue
            result.append(p)
        return result

    @rx.var
    def filtered_types(self) -> list[ProductType]:
        q = self.type_search.lower().strip()
        if not q:
            return self.product_types
        return [
            t
            for t in self.product_types
            if q in t["name"].lower() or q in t["description"].lower()
        ]

    @rx.var
    def filtered_suppliers(self) -> list[Supplier]:
        q = self.supplier_search.lower().strip()
        if not q:
            return self.suppliers
        return [
            s
            for s in self.suppliers
            if q in s["name"].lower()
            or q in s["contact"].lower()
            or q in s["email"].lower()
        ]

    def _recount_types(self):
        counts: dict[str, int] = {}
        for p in self.products:
            counts[p["type"]] = counts.get(p["type"], 0) + 1
        for t in self.product_types:
            t["product_count"] = counts.get(t["name"], 0)

    def _recount_suppliers(self):
        counts: dict[str, int] = {}
        for p in self.products:
            counts[p["supplier"]] = counts.get(p["supplier"], 0) + 1
        for s in self.suppliers:
            s["product_count"] = counts.get(s["name"], 0)

    def _next_product_id(self) -> int:
        return max((p["id"] for p in self.products), default=0) + 1

    def _next_type_id(self) -> int:
        return max((t["id"] for t in self.product_types), default=0) + 1

    def _next_supplier_id(self) -> int:
        return max((s["id"] for s in self.suppliers), default=0) + 1

    @rx.event
    def set_product_search(self, v: str):
        self.product_search = v

    @rx.event
    def set_product_type_filter(self, v: str):
        self.product_type_filter = v

    @rx.event
    def set_product_supplier_filter(self, v: str):
        self.product_supplier_filter = v

    @rx.event
    def set_product_stock_filter(self, v: str):
        self.product_stock_filter = v

    @rx.event
    def clear_product_filters(self):
        self.product_search = ""
        self.product_type_filter = "Todos"
        self.product_supplier_filter = "Todos"
        self.product_stock_filter = "Todos"

    @rx.event
    def open_new_product(self):
        default_type = (
            self.product_types[0]["name"] if self.product_types else ""
        )
        default_supplier = self.suppliers[0]["name"] if self.suppliers else ""
        self.editing_product = {
            "id": 0,
            "name": "",
            "sku": "",
            "type": default_type,
            "supplier": default_supplier,
            "stock": 0,
            "min_stock": 0,
            "price": 0.0,
        }
        self.is_editing_product = False
        self.product_form_error = ""
        self.show_product_form = True

    @rx.event
    def open_edit_product(self, product: Product):
        self.editing_product = dict(product)
        self.is_editing_product = True
        self.product_form_error = ""
        self.show_product_form = True

    @rx.event
    def close_product_form(self):
        self.show_product_form = False
        self.product_form_error = ""

    @rx.event
    def open_product_detail(self, product: Product):
        self.selected_product = dict(product)
        self.show_product_detail = True

    @rx.event
    def close_product_detail(self):
        self.show_product_detail = False

    @rx.event
    def open_delete_product(self, product: Product):
        self.selected_product = dict(product)
        self.show_product_delete = True

    @rx.event
    def close_delete_product(self):
        self.show_product_delete = False

    @rx.event
    async def confirm_delete_product(self):
        product_id = self.selected_product["id"]
        name = self.selected_product["name"]

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(
                    f"{API_URL}/products/{product_id}"
                )

            if response.status_code >= 400:
                try:
                    detail = response.json().get(
                        "detail",
                        "No se pudo eliminar el producto",
                    )
                except ValueError:
                    detail = "No se pudo eliminar el producto"

                self.show_product_delete = False

                yield rx.toast(
                    title="Error al eliminar",
                    description=(
                        detail if isinstance(detail, str) else str(detail)
                    ),
                    duration=4000,
                    close_button=True,
                )
                return

            await self.load_data()

            self.show_product_delete = False
            self.selected_product = EMPTY_PRODUCT

            yield rx.toast(
                title="Producto eliminado",
                description=f"'{name}' se eliminó correctamente.",
                duration=3000,
                close_button=True,
            )

        except httpx.RequestError:
            self.show_product_delete = False

            yield rx.toast(
                title="Error de conexión",
                description="No se pudo conectar con la API.",
                duration=4000,
                close_button=True,
            )

        except Exception as error:
            self.show_product_delete = False

            yield rx.toast(
                title="Error inesperado",
                description=str(error),
                duration=4000,
                close_button=True,
            )

    def normalize_product(self, product: dict) -> Product:
        product_type = product.get("type")
        supplier = product.get("supplier")

        return {
            "id": product["id"],
            "name": product["name"],
            "sku": product["sku"],
            "type": (
                product_type.get("name", "")
                if isinstance(product_type, dict)
                else product_type or ""
            ),
            "supplier": (
                supplier.get("name", "")
                if isinstance(supplier, dict)
                else supplier or ""
            ),
            "stock": product["stock"],
            "min_stock": product["min_stock"],
            "price": float(product["price"]),
        }

    @rx.event
    async def submit_product(self, form_data: dict):
        name = form_data.get("name", "").strip()
        sku = form_data.get("sku", "").strip()

        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/suppliers")

        type_name = form_data.get("type")

        type_id = next(
            (
                t["id"]
                for t in self.product_types
                if t["name"] == type_name
            ),
            None,
        )

        if type_id is None:
            self.product_form_error = "Tipo inválido"
            return

        supplier_name = form_data.get("supplier")

        supplier_id = next(
            (
                s["id"]
                for s in self.suppliers
                if s["name"] == supplier_name
            ),
            None,
        )

        if supplier_id is None:
            self.product_form_error = "Proveedor inválido"
            return

        stock_s = form_data.get("stock", "0").strip()
        min_stock_s = form_data.get("min_stock", "0").strip()
        price_s = form_data.get("price", "0").strip()

        if not name or not sku:
            self.product_form_error = "Nombre y SKU son obligatorios"
            return

        try:
            stock = int(stock_s)
            min_stock = int(min_stock_s)
            price = float(price_s)
        except ValueError:
            self.product_form_error = "Valores numéricos inválidos"
            return

        if stock < 0 or min_stock < 0 or price < 0:
            self.product_form_error = "Los valores no pueden ser negativos"
            return

        body = {
            "name": name,
            "sku": sku,
            "type_id": type_id,
            "supplier_id": supplier_id,
            "stock": stock,
            "min_stock": min_stock,
            "price": price,
        }

        try:
            async with httpx.AsyncClient() as client:
                if self.is_editing_product:

                    pid = self.editing_product["id"]

                    response = await client.put(
                        f"{API_URL}/products/{pid}",
                        json=body,
                    )

                    msg = "Producto actualizado"

                else:

                    response = await client.post(
                        f"{API_URL}/products",
                        json=body,
                    )

                    msg = "Producto creado"

            if response.status_code >= 400:
                self.product_form_error = response.json()["detail"]
                return

            await self.load_data()

            self.show_product_form = False
            self.product_form_error = ""

            yield rx.toast(
                title=msg,
                duration=3000,
                close_button=True,
            )

        except Exception as e:
            self.product_form_error = str(e)

    @rx.event
    def set_type_search(self, v: str):
        self.type_search = v

    @rx.event
    def open_new_type(self):
        self.editing_type = {
            "id": 0,
            "name": "",
            "description": "",
            "product_count": 0,
        }
        self.is_editing_type = False
        self.type_form_error = ""
        self.show_type_form = True

    @rx.event
    def open_edit_type(self, t: ProductType):
        self.editing_type = dict(t)
        self.is_editing_type = True
        self.type_form_error = ""
        self.show_type_form = True

    @rx.event
    def close_type_form(self):
        self.show_type_form = False

    @rx.event
    def open_type_detail(self, t: ProductType):
        self.selected_type = dict(t)
        self.show_type_detail = True

    @rx.event
    def close_type_detail(self):
        self.show_type_detail = False

    @rx.event
    def open_delete_type(self, t: ProductType):
        self.selected_type = dict(t)
        self.show_type_delete = True

    @rx.event
    def close_delete_type(self):
        self.show_type_delete = False

    @rx.event
    async def confirm_delete_type(self):
        type_id = self.selected_type["id"]
        name = self.selected_type["name"]
        product_count = self.selected_type["product_count"]

        if product_count > 0:
            self.show_type_delete = False

            yield rx.toast(
                title="No se puede eliminar",
                description=f"Hay {product_count} producto(s) usando este tipo.",
                duration=4000,
                close_button=True,
            )
            return

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(
                    f"{API_URL}/types/{type_id}",
                )

            if response.status_code >= 400:
                try:
                    detail = response.json().get(
                        "detail",
                        "No se pudo eliminar el tipo",
                    )
                except ValueError:
                    detail = "No se pudo eliminar el tipo"

                self.show_type_delete = False

                yield rx.toast(
                    title="Error al eliminar",
                    description=(
                        detail if isinstance(detail, str) else str(detail)
                    ),
                    duration=4000,
                    close_button=True,
                )
                return

            await self.load_data()

            self.show_type_delete = False
            self.selected_type = EMPTY_TYPE

            yield rx.toast(
                title="Tipo eliminado",
                description=f"'{name}' se eliminó correctamente.",
                duration=3000,
                close_button=True,
            )

        except httpx.RequestError:
            self.show_type_delete = False

            yield rx.toast(
                title="Error de conexión",
                description="No se pudo conectar con la API.",
                duration=4000,
                close_button=True,
            )

    @rx.event
    async def submit_type(self, form_data: dict):
        name = form_data.get("name", "").strip()
        description = form_data.get("description", "").strip()

        if not name:
            self.type_form_error = "El nombre es obligatorio"
            return

        body = {
            "name": name,
            "description": description,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if self.is_editing_type:
                    type_id = self.editing_type["id"]

                    response = await client.put(
                        f"{API_URL}/types/{type_id}",
                        json=body,
                    )

                    message = "Tipo actualizado"
                else:
                    response = await client.post(
                        f"{API_URL}/types",
                        json=body,
                    )

                    message = "Tipo creado"

            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo guardar el tipo")
                except ValueError:
                    detail = "No se pudo guardar el tipo"

                self.type_form_error = (
                    detail if isinstance(detail, str) else str(detail)
                )
                return

            # Recarga tipos, productos y proveedores desde PostgreSQL.
            await self.load_data()

            self.show_type_form = False
            self.type_form_error = ""
            self.is_editing_type = False

            yield rx.toast(
                title=message,
                duration=3000,
                close_button=True,
            )

        except httpx.RequestError:
            self.type_form_error = "No se pudo conectar con la API"

        except Exception as error:
            self.type_form_error = f"Error inesperado: {error}"

    @rx.event
    def set_supplier_search(self, v: str):
        self.supplier_search = v

    @rx.event
    def open_new_supplier(self):
        self.editing_supplier = {
            "id": 0,
            "name": "",
            "contact": "",
            "email": "",
            "phone": "",
            "product_count": 0,
        }
        self.is_editing_supplier = False
        self.supplier_form_error = ""
        self.show_supplier_form = True

    @rx.event
    def open_edit_supplier(self, s: Supplier):
        self.editing_supplier = dict(s)
        self.is_editing_supplier = True
        self.supplier_form_error = ""
        self.show_supplier_form = True

    @rx.event
    def close_supplier_form(self):
        self.show_supplier_form = False

    @rx.event
    def open_supplier_detail(self, s: Supplier):
        self.selected_supplier = dict(s)
        self.show_supplier_detail = True

    @rx.event
    def close_supplier_detail(self):
        self.show_supplier_detail = False

    @rx.event
    def open_delete_supplier(self, s: Supplier):
        self.selected_supplier = dict(s)
        self.show_supplier_delete = True

    @rx.event
    def close_delete_supplier(self):
        self.show_supplier_delete = False

    @rx.event
    async def confirm_delete_supplier(self):
        supplier_id = self.selected_supplier["id"]
        name = self.selected_supplier["name"]
        product_count = self.selected_supplier["product_count"]

        if product_count > 0:
            self.show_supplier_delete = False

            yield rx.toast(
                title="No se puede eliminar",
                description=f"Hay {product_count} producto(s) de este proveedor.",
                duration=4000,
                close_button=True,
            )
            return

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(
                    f"{API_URL}/suppliers/{supplier_id}",
                )

            if response.status_code >= 400:
                try:
                    detail = response.json().get(
                        "detail",
                        "No se pudo eliminar el proveedor",
                    )
                except ValueError:
                    detail = "No se pudo eliminar el proveedor"

                self.show_supplier_delete = False

                yield rx.toast(
                    title="Error al eliminar",
                    description=detail if isinstance(detail, str) else str(detail),
                    duration=4000,
                    close_button=True,
                )
                return

            await self.load_data()

            self.show_supplier_delete = False
            self.selected_supplier = EMPTY_SUPPLIER

            yield rx.toast(
                title="Proveedor eliminado",
                description=f"'{name}' se eliminó correctamente.",
                duration=3000,
                close_button=True,
            )

        except httpx.RequestError:
            self.show_supplier_delete = False

            yield rx.toast(
                title="Error de conexión",
                description="No se pudo conectar con la API.",
                duration=4000,
                close_button=True,
            )

    @rx.event
    async def submit_supplier(self, form_data: dict):
        name = form_data.get("name", "").strip()
        contact = form_data.get("contact", "").strip()
        email = form_data.get("email", "").strip()
        phone = form_data.get("phone", "").strip()

        if not name:
            self.supplier_form_error = "El nombre es obligatorio"
            return

        if email and "@" not in email:
            self.supplier_form_error = "Email inválido"
            return

        body = {
            "name": name,
            "contact": contact,
            "email": email,
            "phone": phone,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if self.is_editing_supplier:
                    supplier_id = self.editing_supplier["id"]

                    response = await client.put(
                        f"{API_URL}/suppliers/{supplier_id}",
                        json=body,
                    )

                    message = "Proveedor actualizado"
                else:
                    response = await client.post(
                        f"{API_URL}/suppliers",
                        json=body,
                    )

                    message = "Proveedor creado"

            if response.status_code >= 400:
                try:
                    detail = response.json().get(
                        "detail",
                        "No se pudo guardar el proveedor",
                    )
                except ValueError:
                    detail = "No se pudo guardar el proveedor"

                self.supplier_form_error = (
                    detail if isinstance(detail, str) else str(detail)
                )
                return

            await self.load_data()

            self.show_supplier_form = False
            self.supplier_form_error = ""
            self.is_editing_supplier = False

            yield rx.toast(
                title=message,
                duration=3000,
                close_button=True,
            )

        except httpx.RequestError:
            self.supplier_form_error = "No se pudo conectar con la API"

        except Exception as error:
            self.supplier_form_error = f"Error inesperado: {error}"