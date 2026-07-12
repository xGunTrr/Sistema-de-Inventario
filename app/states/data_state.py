import reflex as rx
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


class Activity(TypedDict):
    id: int
    action: str
    entity: str
    user: str
    time: str
    icon: str


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


class DataState(rx.State):
    products: list[Product] = [
        {
            "id": 1,
            "name": 'Laptop Pro 14"',
            "sku": "LP-001",
            "type": "Electrónica",
            "supplier": "TechCorp",
            "stock": 24,
            "min_stock": 10,
            "price": 1299.00,
        },
        {
            "id": 2,
            "name": "Mouse Inalámbrico",
            "sku": "MI-002",
            "type": "Electrónica",
            "supplier": "TechCorp",
            "stock": 5,
            "min_stock": 15,
            "price": 29.99,
        },
        {
            "id": 3,
            "name": "Silla Ergonómica",
            "sku": "SE-003",
            "type": "Mobiliario",
            "supplier": "OfficeMax",
            "stock": 12,
            "min_stock": 5,
            "price": 249.00,
        },
        {
            "id": 4,
            "name": "Escritorio Ajustable",
            "sku": "EA-004",
            "type": "Mobiliario",
            "supplier": "OfficeMax",
            "stock": 3,
            "min_stock": 8,
            "price": 449.00,
        },
        {
            "id": 5,
            "name": 'Monitor 27" 4K',
            "sku": "MN-005",
            "type": "Electrónica",
            "supplier": "DisplayCo",
            "stock": 18,
            "min_stock": 10,
            "price": 399.00,
        },
        {
            "id": 6,
            "name": "Teclado Mecánico",
            "sku": "TM-006",
            "type": "Electrónica",
            "supplier": "TechCorp",
            "stock": 32,
            "min_stock": 20,
            "price": 89.99,
        },
        {
            "id": 7,
            "name": "Papel A4 (500h)",
            "sku": "PA-007",
            "type": "Papelería",
            "supplier": "PaperPlus",
            "stock": 150,
            "min_stock": 50,
            "price": 8.50,
        },
        {
            "id": 8,
            "name": "Bolígrafos Pack x12",
            "sku": "BP-008",
            "type": "Papelería",
            "supplier": "PaperPlus",
            "stock": 4,
            "min_stock": 30,
            "price": 12.00,
        },
        {
            "id": 9,
            "name": "Cámara Web HD",
            "sku": "CW-009",
            "type": "Electrónica",
            "supplier": "DisplayCo",
            "stock": 22,
            "min_stock": 10,
            "price": 79.00,
        },
        {
            "id": 10,
            "name": "Lámpara LED",
            "sku": "LL-010",
            "type": "Mobiliario",
            "supplier": "OfficeMax",
            "stock": 15,
            "min_stock": 8,
            "price": 39.99,
        },
        {
            "id": 11,
            "name": "Café Premium 1kg",
            "sku": "CP-011",
            "type": "Alimentos",
            "supplier": "GourmetCo",
            "stock": 45,
            "min_stock": 20,
            "price": 18.50,
        },
        {
            "id": 12,
            "name": "Agua Mineral 24pk",
            "sku": "AM-012",
            "type": "Alimentos",
            "supplier": "GourmetCo",
            "stock": 8,
            "min_stock": 25,
            "price": 15.00,
        },
    ]

    product_types: list[ProductType] = [
        {
            "id": 1,
            "name": "Electrónica",
            "description": "Dispositivos y accesorios electrónicos",
            "product_count": 5,
        },
        {
            "id": 2,
            "name": "Mobiliario",
            "description": "Muebles de oficina y hogar",
            "product_count": 3,
        },
        {
            "id": 3,
            "name": "Papelería",
            "description": "Suministros de oficina y papelería",
            "product_count": 2,
        },
        {
            "id": 4,
            "name": "Alimentos",
            "description": "Productos comestibles y bebidas",
            "product_count": 2,
        },
    ]

    suppliers: list[Supplier] = [
        {
            "id": 1,
            "name": "TechCorp",
            "contact": "Juan Martínez",
            "email": "juan@techcorp.com",
            "phone": "+34 600 111 222",
            "product_count": 3,
        },
        {
            "id": 2,
            "name": "OfficeMax",
            "contact": "María López",
            "email": "maria@officemax.com",
            "phone": "+34 600 333 444",
            "product_count": 3,
        },
        {
            "id": 3,
            "name": "DisplayCo",
            "contact": "Carlos Ruiz",
            "email": "carlos@displayco.com",
            "phone": "+34 600 555 666",
            "product_count": 2,
        },
        {
            "id": 4,
            "name": "PaperPlus",
            "contact": "Ana García",
            "email": "ana@paperplus.com",
            "phone": "+34 600 777 888",
            "product_count": 2,
        },
        {
            "id": 5,
            "name": "GourmetCo",
            "contact": "Luis Fernández",
            "email": "luis@gourmetco.com",
            "phone": "+34 600 999 000",
            "product_count": 2,
        },
    ]

    activities: list[Activity] = [
        {
            "id": 1,
            "action": "Producto agregado",
            "entity": 'Monitor 27" 4K',
            "user": "Admin",
            "time": "Hace 5 min",
            "icon": "plus",
        },
        {
            "id": 2,
            "action": "Stock actualizado",
            "entity": "Mouse Inalámbrico",
            "user": "Admin",
            "time": "Hace 22 min",
            "icon": "refresh-cw",
        },
        {
            "id": 3,
            "action": "Proveedor editado",
            "entity": "TechCorp",
            "user": "Admin",
            "time": "Hace 1 hora",
            "icon": "pencil",
        },
        {
            "id": 4,
            "action": "Tipo creado",
            "entity": "Alimentos",
            "user": "Admin",
            "time": "Hace 3 horas",
            "icon": "tag",
        },
        {
            "id": 5,
            "action": "Producto eliminado",
            "entity": "Producto obsoleto",
            "user": "Admin",
            "time": "Hace 5 horas",
            "icon": "trash-2",
        },
        {
            "id": 6,
            "action": "Stock crítico",
            "entity": "Escritorio Ajustable",
            "user": "Sistema",
            "time": "Hace 1 día",
            "icon": "triangle-alert",
        },
    ]

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
        return sum(p["stock"] * p["price"] for p in self.products)

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
    def confirm_delete_product(self):
        pid = self.selected_product["id"]
        name = self.selected_product["name"]
        self.products = [p for p in self.products if p["id"] != pid]
        self._recount_types()
        self._recount_suppliers()
        self.show_product_delete = False
        yield rx.toast(
            title="Producto eliminado",
            description=f"'{name}' se eliminó correctamente.",
            duration=3000,
            close_button=True,
        )

    @rx.event
    def submit_product(self, form_data: dict):
        name = form_data.get("name", "").strip()
        sku = form_data.get("sku", "").strip()
        type_ = form_data.get("type", "").strip()
        supplier = form_data.get("supplier", "").strip()
        stock_s = form_data.get("stock", "0").strip()
        min_stock_s = form_data.get("min_stock", "0").strip()
        price_s = form_data.get("price", "0").strip()

        if not name or not sku:
            self.product_form_error = "Nombre y SKU son obligatorios"
            return
        if not type_ or not supplier:
            self.product_form_error = "Selecciona tipo y proveedor"
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

        if self.is_editing_product:
            pid = self.editing_product["id"]
            for p in self.products:
                if p["sku"] == sku and p["id"] != pid:
                    self.product_form_error = "El SKU ya existe"
                    return
            for i, p in enumerate(self.products):
                if p["id"] == pid:
                    self.products[i] = {
                        "id": pid,
                        "name": name,
                        "sku": sku,
                        "type": type_,
                        "supplier": supplier,
                        "stock": stock,
                        "min_stock": min_stock,
                        "price": price,
                    }
                    break
            msg = "Producto actualizado"
        else:
            for p in self.products:
                if p["sku"] == sku:
                    self.product_form_error = "El SKU ya existe"
                    return
            new_p: Product = {
                "id": self._next_product_id(),
                "name": name,
                "sku": sku,
                "type": type_,
                "supplier": supplier,
                "stock": stock,
                "min_stock": min_stock,
                "price": price,
            }
            self.products.append(new_p)
            msg = "Producto creado"

        self._recount_types()
        self._recount_suppliers()
        self.show_product_form = False
        self.product_form_error = ""
        yield rx.toast(title=msg, duration=3000, close_button=True)

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
    def confirm_delete_type(self):
        tid = self.selected_type["id"]
        name = self.selected_type["name"]
        count = sum(1 for p in self.products if p["type"] == name)
        if count > 0:
            self.show_type_delete = False
            yield rx.toast(
                title="No se puede eliminar",
                description=f"Hay {count} producto(s) usando este tipo.",
                duration=4000,
                close_button=True,
            )
            return
        self.product_types = [t for t in self.product_types if t["id"] != tid]
        self.show_type_delete = False
        yield rx.toast(title="Tipo eliminado", duration=3000, close_button=True)

    @rx.event
    def submit_type(self, form_data: dict):
        name = form_data.get("name", "").strip()
        description = form_data.get("description", "").strip()
        if not name:
            self.type_form_error = "El nombre es obligatorio"
            return

        if self.is_editing_type:
            tid = self.editing_type["id"]
            for t in self.product_types:
                if t["name"].lower() == name.lower() and t["id"] != tid:
                    self.type_form_error = "Ya existe un tipo con ese nombre"
                    return
            old_name = ""
            for t in self.product_types:
                if t["id"] == tid:
                    old_name = t["name"]
                    break
            for i, t in enumerate(self.product_types):
                if t["id"] == tid:
                    self.product_types[i] = {
                        "id": tid,
                        "name": name,
                        "description": description,
                        "product_count": t["product_count"],
                    }
                    break
            if old_name and old_name != name:
                for p in self.products:
                    if p["type"] == old_name:
                        p["type"] = name
            msg = "Tipo actualizado"
        else:
            for t in self.product_types:
                if t["name"].lower() == name.lower():
                    self.type_form_error = "Ya existe un tipo con ese nombre"
                    return
            self.product_types.append(
                {
                    "id": self._next_type_id(),
                    "name": name,
                    "description": description,
                    "product_count": 0,
                }
            )
            msg = "Tipo creado"

        self._recount_types()
        self.show_type_form = False
        self.type_form_error = ""
        yield rx.toast(title=msg, duration=3000, close_button=True)

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
    def confirm_delete_supplier(self):
        sid = self.selected_supplier["id"]
        name = self.selected_supplier["name"]
        count = sum(1 for p in self.products if p["supplier"] == name)
        if count > 0:
            self.show_supplier_delete = False
            yield rx.toast(
                title="No se puede eliminar",
                description=f"Hay {count} producto(s) de este proveedor.",
                duration=4000,
                close_button=True,
            )
            return
        self.suppliers = [s for s in self.suppliers if s["id"] != sid]
        self.show_supplier_delete = False
        yield rx.toast(
            title="Proveedor eliminado", duration=3000, close_button=True
        )

    @rx.event
    def submit_supplier(self, form_data: dict):
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

        if self.is_editing_supplier:
            sid = self.editing_supplier["id"]
            for s in self.suppliers:
                if s["name"].lower() == name.lower() and s["id"] != sid:
                    self.supplier_form_error = (
                        "Ya existe un proveedor con ese nombre"
                    )
                    return
            old_name = ""
            for s in self.suppliers:
                if s["id"] == sid:
                    old_name = s["name"]
                    break
            for i, s in enumerate(self.suppliers):
                if s["id"] == sid:
                    self.suppliers[i] = {
                        "id": sid,
                        "name": name,
                        "contact": contact,
                        "email": email,
                        "phone": phone,
                        "product_count": s["product_count"],
                    }
                    break
            if old_name and old_name != name:
                for p in self.products:
                    if p["supplier"] == old_name:
                        p["supplier"] = name
            msg = "Proveedor actualizado"
        else:
            for s in self.suppliers:
                if s["name"].lower() == name.lower():
                    self.supplier_form_error = (
                        "Ya existe un proveedor con ese nombre"
                    )
                    return
            self.suppliers.append(
                {
                    "id": self._next_supplier_id(),
                    "name": name,
                    "contact": contact,
                    "email": email,
                    "phone": phone,
                    "product_count": 0,
                }
            )
            msg = "Proveedor creado"

        self._recount_suppliers()
        self.show_supplier_form = False
        self.supplier_form_error = ""
        yield rx.toast(title=msg, duration=3000, close_button=True)
