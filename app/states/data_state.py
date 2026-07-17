import reflex as rx
import httpx
from typing import Optional, TypedDict


API_URL = "http://localhost:8000/api"


class PedidoDetalleForm(TypedDict):
    IdProducto: int
    NombreProducto: str
    Cantidad: int
    PrecioUnitario: float
    Subtotal: float
    ApiId: int


def _format_date(value: str) -> str:
    if not value or not isinstance(value, str):
        return ""
    try:
        if "T" in value:
            date_part, time_part = value.split("T", 1)
            time_part = time_part.rstrip("Z").split("+")[0].split(".")[0]
            d, m, y = date_part.split("-")
            return f"{d}/{m}/{y} {time_part}"
        else:
            d, m, y = value.split("-")
            return f"{d}/{m}/{y}"
    except (ValueError, IndexError):
        return value


def _to_iso_date(value: str) -> str:
    if not value or not isinstance(value, str):
        return ""
    try:
        date_part = value.split(" ")[0]
        parts = date_part.split("/")
        if len(parts) == 3 and len(parts[2]) == 4:
            return f"{parts[2]}-{parts[1]}-{parts[0]}"
        return value
    except (ValueError, IndexError):
        return value


class Proveedor(TypedDict):
    IdProveedor: int
    NombreProveedor: str
    DireccionProveedor: str
    Telefono: str
    Email: str
    Activo: bool
    FechaCreacion: str
    FechaModificacion: str


class Producto(TypedDict):
    IdProducto: int
    IdProveedor: int
    CodigoProducto: str
    CodigoBarras: Optional[str]
    NombreProducto: str
    DescripcionProducto: Optional[str]
    CategoriaProducto: Optional[str]
    PrecioCompra: float
    PrecioVenta: float
    CantidadReorden: int
    PesoEmpaque: Optional[float]
    AltoEmpaque: Optional[float]
    AnchoEmpaque: Optional[float]
    ProfundidadEmpaque: Optional[float]
    Refrigerado: bool
    Activo: bool
    proveedor: Optional[dict]


class Cliente(TypedDict):
    IdCliente: int
    NombreCliente: str
    DireccionCliente: str
    Telefono: str
    Email: str
    Activo: bool
    entregas: Optional[list]


class DetallePedido(TypedDict):
    IdDetallePedido: int
    IdProducto: int
    Cantidad: int
    CantidadRecibida: int
    PrecioUnitario: float
    producto: Optional[dict]


class Pedido(TypedDict):
    IdPedido: int
    IdProveedor: int
    IdAlmacen: Optional[int]
    FechaPedido: str
    Estado: str
    Activo: bool
    proveedor: Optional[dict]
    detalles: list[DetallePedido]


class DetalleEntrega(TypedDict):
    IdDetalleEntrega: int
    IdProducto: int
    CantidadEntregada: int
    PrecioUnitario: float
    producto: Optional[dict]


class Entrega(TypedDict):
    IdEntrega: int
    IdCliente: int
    IdPedido: int
    IdAlmacen: Optional[int]
    FechaVenta: str
    FechaEsperada: str
    FechaReal: Optional[str]
    Estado: str
    Activo: bool
    cliente: Optional[dict]
    pedido: Optional[dict]
    detalles: list[DetalleEntrega]


class Ubicacion(TypedDict):
    IdUbicacion: int
    NombreUbicacion: str
    DireccionUbicacion: str
    Ciudad: str
    Referencia: Optional[str]
    TelefonoContacto: Optional[str]
    Activo: bool
    almacenes: Optional[list]


class Almacen(TypedDict):
    IdAlmacen: int
    IdUbicacion: int
    NombreAlmacen: str
    EsRefrigerado: bool
    Activo: bool
    ubicacion: Optional[dict]


class Inventario(TypedDict):
    IdInventario: int
    IdProducto: int
    IdAlmacen: int
    CantidadDisponible: int
    StockMinimo: int
    StockMaximo: int
    PuntoReorden: int
    Activo: bool
    producto: Optional[dict]
    almacen: Optional[dict]


class DetalleTransferencia(TypedDict):
    IdDetalleTransferencia: int
    IdTransferencia: int
    IdProducto: int
    CantidadTransferida: int
    producto: Optional[dict]


class Transferencia(TypedDict):
    IdTransferencia: int
    IdAlmacenOrigen: int
    IdAlmacenDestino: int
    CantidadTransferida: int
    FechaEnvio: str
    FechaRecepcion: Optional[str]
    Estado: str
    Activo: bool
    almacen_origen: Optional[dict]
    almacen_destino: Optional[dict]
    detalles: list[DetalleTransferencia]


EMPTY_PROVEEDOR: Proveedor = {
    "IdProveedor": 0, "NombreProveedor": "", "DireccionProveedor": "",
    "Telefono": "", "Email": "", "Activo": True,
    "FechaCreacion": "", "FechaModificacion": "",
}

EMPTY_PRODUCTO: Producto = {
    "IdProducto": 0, "IdProveedor": 0, "CodigoProducto": "",
    "CodigoBarras": "", "NombreProducto": "", "DescripcionProducto": "",
    "CategoriaProducto": "", "PrecioCompra": 0.0, "PrecioVenta": 0.0,
    "CantidadReorden": 0, "PesoEmpaque": 0.0, "AltoEmpaque": 0.0,
    "AnchoEmpaque": 0.0, "ProfundidadEmpaque": 0.0,
    "Refrigerado": False, "Activo": True, "proveedor": None,
}

EMPTY_CLIENTE: Cliente = {
    "IdCliente": 0, "NombreCliente": "", "DireccionCliente": "",
    "Telefono": "", "Email": "", "Activo": True, "entregas": [],
}

EMPTY_PEDIDO: Pedido = {
    "IdPedido": 0, "IdProveedor": 0, "IdAlmacen": None, "FechaPedido": "", "Estado": "",
    "Activo": True, "proveedor": None, "detalles": [],
}

EMPTY_ENTREGA: Entrega = {
    "IdEntrega": 0, "IdCliente": 0, "IdPedido": 0, "IdAlmacen": None,
    "FechaVenta": "", "FechaEsperada": "", "FechaReal": "",
    "Estado": "", "Activo": True, "cliente": None,
    "pedido": None, "detalles": [],
}

EMPTY_UBICACION: Ubicacion = {
    "IdUbicacion": 0, "NombreUbicacion": "", "DireccionUbicacion": "",
    "Ciudad": "", "Referencia": "", "TelefonoContacto": "", "Activo": True,
    "almacenes": [],
}

EMPTY_ALMACEN: Almacen = {
    "IdAlmacen": 0, "IdUbicacion": 0, "NombreAlmacen": "",
    "EsRefrigerado": False, "Activo": True, "ubicacion": None,
}

EMPTY_INVENTARIO: Inventario = {
    "IdInventario": 0, "IdProducto": 0, "IdAlmacen": 0,
    "CantidadDisponible": 0, "StockMinimo": 0, "StockMaximo": 0,
    "PuntoReorden": 0, "Activo": True, "producto": None, "almacen": None,
}

EMPTY_TRANSFERENCIA: Transferencia = {
    "IdTransferencia": 0, "IdAlmacenOrigen": 0, "IdAlmacenDestino": 0,
    "CantidadTransferida": 0, "FechaEnvio": "", "FechaRecepcion": "",
    "Estado": "", "Activo": True, "almacen_origen": None, "almacen_destino": None,
    "detalles": [],
}


class DataState(rx.State):

    proveedores: list[Proveedor] = []
    productos: list[Producto] = []
    clientes: list[Cliente] = []
    pedidos: list[Pedido] = []
    entregas: list[Entrega] = []
    ubicaciones: list[Ubicacion] = []
    almacenes: list[Almacen] = []
    inventarios: list[Inventario] = []
    transferencias: list[Transferencia] = []

    proveedor_filter_options: list[dict] = []
    cliente_filter_options: list[dict] = []
    ubicacion_filter_options: list[dict] = []
    producto_filter_options: list[dict] = []
    almacen_filter_options: list[dict] = []
    pedido_filter_options: list[dict] = []

    proveedor_search: str = ""
    producto_search: str = ""
    cliente_search: str = ""
    pedido_search: str = ""
    entrega_search: str = ""
    ubicacion_search: str = ""
    almacen_search: str = ""
    inventario_search: str = ""
    transferencia_search: str = ""

    proveedor_filter: str = "Todos"
    cliente_filter: str = "Todos"
    ubicacion_filter: str = "Todos"
    producto_filter: str = "Todos"
    almacen_filter: str = "Todos"
    pedido_estado_filter: str = "Todos"
    entrega_estado_filter: str = "Todos"
    transferencia_estado_filter: str = "Todos"
    categoria_filter: str = "Todos"
    producto_proveedor_filter: str = "Todos"

    show_proveedor_form: bool = False
    show_proveedor_delete: bool = False
    show_proveedor_detail: bool = False
    editing_proveedor: Proveedor = EMPTY_PROVEEDOR
    selected_proveedor: Proveedor = EMPTY_PROVEEDOR
    is_editing_proveedor: bool = False
    proveedor_form_error: str = ""

    show_producto_form: bool = False
    show_producto_delete: bool = False
    show_producto_detail: bool = False
    editing_producto: Producto = EMPTY_PRODUCTO
    selected_producto: Producto = EMPTY_PRODUCTO
    is_editing_producto: bool = False
    producto_form_error: str = ""

    show_cliente_form: bool = False
    show_cliente_delete: bool = False
    show_cliente_detail: bool = False
    editing_cliente: Cliente = EMPTY_CLIENTE
    selected_cliente: Cliente = EMPTY_CLIENTE
    is_editing_cliente: bool = False
    cliente_form_error: str = ""

    show_pedido_form: bool = False
    show_pedido_delete: bool = False
    show_pedido_detail: bool = False
    editing_pedido: Pedido = EMPTY_PEDIDO
    selected_pedido: Pedido = EMPTY_PEDIDO
    is_editing_pedido: bool = False
    pedido_form_error: str = ""
    pedido_form_detalles: list[PedidoDetalleForm] = []
    pedido_detalle_temp_producto: str = ""
    pedido_detalle_temp_cantidad: str = "1"
    pedido_detalle_temp_precio: str = "0"
    pedido_recepcion_almacen: str = ""
    show_pedido_recepcion_modal: bool = False
    pedido_recepcion_almacen_id: str = ""

    show_entrega_form: bool = False
    show_entrega_delete: bool = False
    show_entrega_detail: bool = False
    editing_entrega: Entrega = EMPTY_ENTREGA
    selected_entrega: Entrega = EMPTY_ENTREGA
    is_editing_entrega: bool = False
    entrega_form_error: str = ""
    entrega_despacho_almacen: str = ""

    show_ubicacion_form: bool = False
    show_ubicacion_delete: bool = False
    show_ubicacion_detail: bool = False
    editing_ubicacion: Ubicacion = EMPTY_UBICACION
    selected_ubicacion: Ubicacion = EMPTY_UBICACION
    is_editing_ubicacion: bool = False
    ubicacion_form_error: str = ""

    show_almacen_form: bool = False
    show_almacen_delete: bool = False
    show_almacen_detail: bool = False
    editing_almacen: Almacen = EMPTY_ALMACEN
    selected_almacen: Almacen = EMPTY_ALMACEN
    is_editing_almacen: bool = False
    almacen_form_error: str = ""

    show_inventario_form: bool = False
    show_inventario_delete: bool = False
    show_inventario_detail: bool = False
    editing_inventario: Inventario = EMPTY_INVENTARIO
    selected_inventario: Inventario = EMPTY_INVENTARIO
    is_editing_inventario: bool = False
    inventario_form_error: str = ""

    show_transferencia_form: bool = False
    show_transferencia_delete: bool = False
    show_transferencia_detail: bool = False
    editing_transferencia: Transferencia = EMPTY_TRANSFERENCIA
    selected_transferencia: Transferencia = EMPTY_TRANSFERENCIA
    is_editing_transferencia: bool = False
    transferencia_form_error: str = ""
    transferencia_form_detalles: list[dict] = []
    transferencia_detalle_temp_producto: str = ""
    transferencia_detalle_temp_cantidad: str = "1"
    transferencia_recepcion_almacen: str = ""

    @rx.event
    async def load_data(self):
        try:
            async with httpx.AsyncClient(timeout=15.0) as client:
                resp_prov = await client.get(f"{API_URL}/proveedores")
                resp_prod = await client.get(f"{API_URL}/productos")
                resp_clie = await client.get(f"{API_URL}/clientes")
                resp_pedi = await client.get(f"{API_URL}/pedidos")
                resp_ent = await client.get(f"{API_URL}/entregas")
                resp_ubic = await client.get(f"{API_URL}/ubicaciones")
                resp_alm = await client.get(f"{API_URL}/almacenes")
                resp_inv = await client.get(f"{API_URL}/inventarios")
                resp_tran = await client.get(f"{API_URL}/transferencias")

            self.proveedores = resp_prov.json().get("data", [])
            self.productos = resp_prod.json().get("data", [])
            self.clientes = resp_clie.json().get("data", [])
            self.pedidos = resp_pedi.json().get("data", [])
            self.entregas = resp_ent.json().get("data", [])
            self.ubicaciones = resp_ubic.json().get("data", [])
            self.almacenes = resp_alm.json().get("data", [])
            self.inventarios = resp_inv.json().get("data", [])
            self.transferencias = resp_tran.json().get("data", [])

            for p in self.proveedores:
                p["FechaCreacion"] = _format_date(p.get("FechaCreacion") or "")
                p["FechaModificacion"] = _format_date(p.get("FechaModificacion") or "")
            for p in self.pedidos:
                p["FechaPedido"] = _format_date(p.get("FechaPedido") or "")
            for e in self.entregas:
                e["FechaVenta"] = _format_date(e.get("FechaVenta") or "")
                e["FechaEsperada"] = _format_date(e.get("FechaEsperada") or "")
                e["FechaReal"] = _format_date(e.get("FechaReal") or "")
            for t in self.transferencias:
                t["FechaEnvio"] = _format_date(t.get("FechaEnvio") or "")
                t["FechaRecepcion"] = _format_date(t.get("FechaRecepcion") or "")

            self.proveedor_filter_options = [
                {"label": p["NombreProveedor"], "value": str(p["IdProveedor"])}
                for p in self.proveedores if p.get("Activo", True)
            ]
            self.cliente_filter_options = [
                {"label": c["NombreCliente"], "value": str(c["IdCliente"])}
                for c in self.clientes if c.get("Activo", True)
            ]
            self.ubicacion_filter_options = [
                {"label": u["NombreUbicacion"], "value": str(u["IdUbicacion"])}
                for u in self.ubicaciones if u.get("Activo", True)
            ]
            self.producto_filter_options = [
                {"label": p["NombreProducto"], "value": str(p["IdProducto"])}
                for p in self.productos if p.get("Activo", True)
            ]
            self.almacen_filter_options = [
                {"label": a["NombreAlmacen"], "value": str(a["IdAlmacen"])}
                for a in self.almacenes if a.get("Activo", True)
            ]
            self.pedido_filter_options = [
                {"label": f"Pedido #{p['IdPedido']}", "value": str(p["IdPedido"])}
                for p in self.pedidos if p.get("Activo", True)
            ]

        except httpx.RequestError as error:
            print(f"Error de conexion: {error}")
        except Exception as error:
            print(f"Error inesperado cargando datos: {error}")

    @rx.var
    def total_proveedores(self) -> int:
        return len(self.proveedores)

    @rx.var
    def total_productos(self) -> int:
        return len(self.productos)

    @rx.var
    def total_clientes(self) -> int:
        return len(self.clientes)

    @rx.var
    def total_pedidos(self) -> int:
        return len(self.pedidos)

    @rx.var
    def total_entregas(self) -> int:
        return len(self.entregas)

    @rx.var
    def total_ubicaciones(self) -> int:
        return len(self.ubicaciones)

    @rx.var
    def total_almacenes(self) -> int:
        return len(self.almacenes)

    @rx.var
    def total_inventarios(self) -> int:
        return len(self.inventarios)

    @rx.var
    def total_transferencias(self) -> int:
        return len(self.transferencias)

    @rx.var
    def categoria_filter_options(self) -> list[dict]:
        cats = sorted({
            (p.get("CategoriaProducto") or "").strip()
            for p in self.productos
            if p.get("CategoriaProducto")
        })
        return [{"label": c, "value": c} for c in cats]

    @rx.var
    def total_stock_value(self) -> float:
        total = 0.0
        for inv in self.inventarios:
            prod = inv.get("producto") or {}
            cantidad = inv.get("CantidadDisponible", 0) or 0
            precio = prod.get("PrecioCompra", 0) or 0
            total += float(cantidad) * float(precio)
        return total

    @rx.var
    def stock_bajo_count(self) -> int:
        return sum(
            1 for i in self.filtered_inventarios
            if (i.get("CantidadDisponible") or 0) <= (i.get("StockMinimo") or 0)
        )

    @rx.var
    def stock_ok_count(self) -> int:
        return sum(
            1 for i in self.filtered_inventarios
            if (i.get("CantidadDisponible") or 0) > (i.get("StockMinimo") or 0)
        )

    @rx.var
    def pedidos_pendientes_count(self) -> int:
        return sum(1 for p in self.pedidos if p.get("Estado") == "Pendiente")

    @rx.var
    def pedidos_completados_count(self) -> int:
        return sum(1 for p in self.pedidos if p.get("Estado") == "Completado")

    @rx.var
    def entregas_pendientes_count(self) -> int:
        return sum(1 for e in self.entregas if e.get("Estado") == "Pendiente")

    @rx.var
    def entregas_entregadas_count(self) -> int:
        return sum(1 for e in self.entregas if e.get("Estado") == "Entregado")

    @rx.var
    def transferencias_pendientes_count(self) -> int:
        return sum(1 for t in self.transferencias if t.get("Estado") == "Pendiente")

    @rx.var
    def transferencias_completadas_count(self) -> int:
        return sum(1 for t in self.transferencias if t.get("Estado") == "Completada")

    @rx.var
    def filtered_proveedores(self) -> list[Proveedor]:
        q = self.proveedor_search.lower().strip()
        return [
            p for p in self.proveedores
            if (
                not q
                or q in p["NombreProveedor"].lower()
                or q in p["Email"].lower()
                or q in p["Telefono"].lower()
            )
        ]

    @rx.var
    def filtered_productos(self) -> list[Producto]:
        q = self.producto_search.lower().strip()
        result = []
        for p in self.productos:
            if q and q not in p["NombreProducto"].lower() and q not in p["CodigoProducto"].lower():
                continue
            if self.categoria_filter != "Todos" and (p.get("CategoriaProducto") or "") != self.categoria_filter:
                continue
            if self.producto_proveedor_filter != "Todos":
                prov = p.get("proveedor") or {}
                if str(prov.get("IdProveedor", "")) != self.producto_proveedor_filter:
                    continue
            result.append(p)
        return result

    @rx.var
    def filtered_clientes(self) -> list[Cliente]:
        q = self.cliente_search.lower().strip()
        return [
            c for c in self.clientes
            if (
                not q
                or q in c["NombreCliente"].lower()
                or q in c["Email"].lower()
                or q in c["Telefono"].lower()
            )
        ]

    @rx.var
    def filtered_pedidos(self) -> list[Pedido]:
        q = self.pedido_search.lower().strip()
        result = []
        for p in self.pedidos:
            if q and q not in str(p["IdPedido"]).lower():
                prov = p.get("proveedor") or {}
                if q not in (prov.get("NombreProveedor") or "").lower():
                    continue
            if (
                self.pedido_estado_filter != "Todos"
                and p["Estado"] != self.pedido_estado_filter
            ):
                continue
            result.append(p)
        return result

    @rx.var
    def filtered_entregas(self) -> list[Entrega]:
        q = self.entrega_search.lower().strip()
        result = []
        for e in self.entregas:
            if q and q not in str(e["IdEntrega"]).lower():
                clie = e.get("cliente") or {}
                if q not in (clie.get("NombreCliente") or "").lower():
                    continue
            if (
                self.entrega_estado_filter != "Todos"
                and e["Estado"] != self.entrega_estado_filter
            ):
                continue
            result.append(e)
        return result

    @rx.var
    def filtered_ubicaciones(self) -> list[Ubicacion]:
        q = self.ubicacion_search.lower().strip()
        return [
            u for u in self.ubicaciones
            if (
                not q
                or q in u["NombreUbicacion"].lower()
                or q in u["Ciudad"].lower()
            )
        ]

    @rx.var
    def filtered_almacenes(self) -> list[Almacen]:
        q = self.almacen_search.lower().strip()
        result = []
        for a in self.almacenes:
            if q and q not in a["NombreAlmacen"].lower():
                continue
            if self.ubicacion_filter != "Todos":
                ubic = a.get("ubicacion") or {}
                if str(ubic.get("IdUbicacion", "")) != self.ubicacion_filter:
                    continue
            result.append(a)
        return result

    @rx.var
    def filtered_inventarios(self) -> list[Inventario]:
        q = self.inventario_search.lower().strip()
        result = []
        for i in self.inventarios:
            if q:
                prod = i.get("producto") or {}
                alm = i.get("almacen") or {}
                if (
                    q not in (prod.get("NombreProducto") or "").lower()
                    and q not in (alm.get("NombreAlmacen") or "").lower()
                ):
                    continue
            if self.producto_filter != "Todos":
                if str(i.get("IdProducto", "")) != self.producto_filter:
                    continue
            if self.almacen_filter != "Todos":
                if str(i.get("IdAlmacen", "")) != self.almacen_filter:
                    continue
            result.append(i)
        return result

    @rx.var
    def filtered_transferencias(self) -> list[Transferencia]:
        q = self.transferencia_search.lower().strip()
        result = []
        for t in self.transferencias:
            if q:
                origen = t.get("almacen_origen") or {}
                if q not in (origen.get("NombreAlmacen") or "").lower():
                    continue
            if (
                self.transferencia_estado_filter != "Todos"
                and t["Estado"] != self.transferencia_estado_filter
            ):
                continue
            detalles = t.get("detalles") or []
            t["CantidadTransferida"] = sum(d.get("CantidadTransferida", 0) for d in detalles)
            result.append(t)
        return result

    @rx.var
    def editing_entrega_fecha_venta_iso(self) -> str:
        return _to_iso_date(self.editing_entrega.get("FechaVenta") or "")

    @rx.var
    def editing_entrega_fecha_esperada_iso(self) -> str:
        return _to_iso_date(self.editing_entrega.get("FechaEsperada") or "")

    @rx.var
    def editing_transferencia_fecha_envio_iso(self) -> str:
        return _to_iso_date(self.editing_transferencia.get("FechaEnvio") or "")

    @rx.var
    def editing_transferencia_fecha_recepcion_iso(self) -> str:
        return _to_iso_date(self.editing_transferencia.get("FechaRecepcion") or "")

    @rx.event
    def set_proveedor_search(self, v: str):
        self.proveedor_search = v

    @rx.event
    def set_producto_search(self, v: str):
        self.producto_search = v

    @rx.event
    def set_cliente_search(self, v: str):
        self.cliente_search = v

    @rx.event
    def set_pedido_search(self, v: str):
        self.pedido_search = v

    @rx.event
    def set_entrega_search(self, v: str):
        self.entrega_search = v

    @rx.event
    def set_ubicacion_search(self, v: str):
        self.ubicacion_search = v

    @rx.event
    def set_almacen_search(self, v: str):
        self.almacen_search = v

    @rx.event
    def set_inventario_search(self, v: str):
        self.inventario_search = v

    @rx.event
    def set_transferencia_search(self, v: str):
        self.transferencia_search = v

    @rx.event
    def set_proveedor_filter(self, v: str):
        self.proveedor_filter = v

    @rx.event
    def set_cliente_filter(self, v: str):
        self.cliente_filter = v

    @rx.event
    def set_ubicacion_filter(self, v: str):
        self.ubicacion_filter = v

    @rx.event
    def set_producto_filter(self, v: str):
        self.producto_filter = v

    @rx.event
    def set_almacen_filter(self, v: str):
        self.almacen_filter = v

    @rx.event
    def set_pedido_estado_filter(self, v: str):
        self.pedido_estado_filter = v

    @rx.event
    def set_entrega_estado_filter(self, v: str):
        self.entrega_estado_filter = v

    @rx.event
    def set_transferencia_estado_filter(self, v: str):
        self.transferencia_estado_filter = v

    @rx.event
    def set_categoria_filter(self, v: str):
        self.categoria_filter = v

    @rx.event
    def set_producto_proveedor_filter(self, v: str):
        self.producto_proveedor_filter = v

    @rx.event
    def clear_product_filters(self):
        self.producto_search = ""
        self.categoria_filter = "Todos"
        self.producto_proveedor_filter = "Todos"

    @rx.event
    def clear_proveedor_filters(self):
        self.proveedor_search = ""

    @rx.event
    def clear_cliente_filters(self):
        self.cliente_search = ""

    @rx.event
    def clear_ubicacion_filters(self):
        self.ubicacion_search = ""

    @rx.event
    def clear_almacen_filters(self):
        self.almacen_search = ""
        self.ubicacion_filter = "Todos"

    @rx.event
    def clear_pedido_filters(self):
        self.pedido_search = ""
        self.pedido_estado_filter = "Todos"

    @rx.event
    def clear_entrega_filters(self):
        self.entrega_search = ""
        self.entrega_estado_filter = "Todos"

    @rx.event
    def clear_transferencia_filters(self):
        self.transferencia_search = ""
        self.transferencia_estado_filter = "Todos"

    @rx.event
    def clear_inventario_filters(self):
        self.inventario_search = ""
        self.producto_filter = "Todos"
        self.almacen_filter = "Todos"

    # =====================================================================
    #  PEDIDO DETALLE TEMP (for create form)
    # =====================================================================

    @rx.event
    def set_pedido_detalle_temp_producto(self, v: str):
        self.pedido_detalle_temp_producto = str(v)

    @rx.event
    def set_pedido_detalle_temp_cantidad(self, v: str):
        self.pedido_detalle_temp_cantidad = str(v)

    @rx.event
    def set_pedido_detalle_temp_precio(self, v: str):
        self.pedido_detalle_temp_precio = str(v)

    @rx.event
    def add_pedido_detalle_temp(self):
        id_producto = str(self.pedido_detalle_temp_producto or "")
        if not id_producto or id_producto == "0":
            self.pedido_form_error = "Selecciona un producto para el detalle"
            return
        for d in self.pedido_form_detalles:
            if d["IdProducto"] == int(id_producto):
                self.pedido_form_error = "Este producto ya esta en el detalle"
                return
        cantidad = int(self.pedido_detalle_temp_cantidad or "1")
        precio = float(self.pedido_detalle_temp_precio or "0")
        nombre = ""
        for p in self.productos:
            if str(p["IdProducto"]) == id_producto:
                nombre = p["NombreProducto"]
                break
        self.pedido_form_detalles = self.pedido_form_detalles + [{
            "IdProducto": int(id_producto),
            "NombreProducto": nombre,
            "Cantidad": cantidad,
            "PrecioUnitario": precio,
            "Subtotal": round(cantidad * precio, 2),
            "ApiId": 0,
        }]
        self.pedido_detalle_temp_producto = ""
        self.pedido_detalle_temp_cantidad = "1"
        self.pedido_detalle_temp_precio = "0"
        self.pedido_form_error = ""

    @rx.event
    def remove_pedido_detalle_temp(self, idx: int):
        target = int(idx)
        if 0 <= target < len(self.pedido_form_detalles):
            self.pedido_form_detalles = [
                d for i, d in enumerate(self.pedido_form_detalles) if i != target
            ]

    # =====================================================================
    #  PROVEEDOR CRUD
    # =====================================================================

    @rx.event
    def open_new_proveedor(self):
        self.editing_proveedor = dict(EMPTY_PROVEEDOR)
        self.is_editing_proveedor = False
        self.proveedor_form_error = ""
        self.show_proveedor_form = True

    @rx.event
    def open_edit_proveedor(self, item: Proveedor):
        self.editing_proveedor = dict(item)
        self.is_editing_proveedor = True
        self.proveedor_form_error = ""
        self.show_proveedor_form = True

    @rx.event
    def close_proveedor_form(self):
        self.show_proveedor_form = False
        self.proveedor_form_error = ""

    @rx.event
    def open_proveedor_detail(self, item: Proveedor):
        self.selected_proveedor = dict(item)
        self.show_proveedor_detail = True

    @rx.event
    def close_proveedor_detail(self):
        self.show_proveedor_detail = False

    @rx.event
    def open_delete_proveedor(self, item: Proveedor):
        self.selected_proveedor = dict(item)
        self.show_proveedor_delete = True

    @rx.event
    def close_delete_proveedor(self):
        self.show_proveedor_delete = False

    @rx.event
    async def confirm_delete_proveedor(self):
        item_id = self.selected_proveedor["IdProveedor"]
        name = self.selected_proveedor["NombreProveedor"]
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(f"{API_URL}/proveedores/{item_id}")
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo eliminar")
                except ValueError:
                    detail = "No se pudo eliminar"
                self.show_proveedor_delete = False
                yield rx.toast(title="Error al eliminar", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            self.show_proveedor_delete = False
            self.selected_proveedor = dict(EMPTY_PROVEEDOR)
            yield rx.toast(title="Proveedor eliminado", description=f"'{name}' eliminado.", duration=3000, close_button=True)
        except httpx.RequestError:
            self.show_proveedor_delete = False
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)
        except Exception as error:
            self.show_proveedor_delete = False
            yield rx.toast(title="Error inesperado", description=str(error), duration=4000, close_button=True)

    @rx.event
    async def submit_proveedor(self, form_data: dict):
        nombre = form_data.get("NombreProveedor", "").strip()
        if not nombre:
            self.proveedor_form_error = "El nombre es obligatorio"
            return
        body = {
            "NombreProveedor": nombre,
            "DireccionProveedor": form_data.get("DireccionProveedor", "").strip(),
            "Telefono": form_data.get("Telefono", "").strip(),
            "Email": form_data.get("Email", "").strip(),
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if self.is_editing_proveedor:
                    pid = self.editing_proveedor["IdProveedor"]
                    response = await client.put(f"{API_URL}/proveedores/{pid}", json=body)
                    msg = "Proveedor actualizado"
                else:
                    response = await client.post(f"{API_URL}/proveedores", json=body)
                    msg = "Proveedor creado"
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo guardar")
                except ValueError:
                    detail = "No se pudo guardar"
                self.proveedor_form_error = str(detail)
                return
            await self.load_data()
            self.show_proveedor_form = False
            self.proveedor_form_error = ""
            self.is_editing_proveedor = False
            yield rx.toast(title=msg, duration=3000, close_button=True)
        except httpx.RequestError:
            self.proveedor_form_error = "No se pudo conectar con la API"
        except Exception as error:
            self.proveedor_form_error = str(error)

    # =====================================================================
    #  PRODUCTO CRUD
    # =====================================================================

    @rx.event
    def open_new_producto(self):
        self.editing_producto = dict(EMPTY_PRODUCTO)
        self.is_editing_producto = False
        self.producto_form_error = ""
        self.show_producto_form = True

    @rx.event
    def open_edit_producto(self, item: Producto):
        self.editing_producto = dict(item)
        self.is_editing_producto = True
        self.producto_form_error = ""
        self.show_producto_form = True

    @rx.event
    def close_producto_form(self):
        self.show_producto_form = False
        self.producto_form_error = ""

    @rx.event
    def open_producto_detail(self, item: Producto):
        self.selected_producto = dict(item)
        self.show_producto_detail = True

    @rx.event
    def close_producto_detail(self):
        self.show_producto_detail = False

    @rx.event
    def open_delete_producto(self, item: Producto):
        self.selected_producto = dict(item)
        self.show_producto_delete = True

    @rx.event
    def close_delete_producto(self):
        self.show_producto_delete = False

    @rx.event
    async def confirm_delete_producto(self):
        item_id = self.selected_producto["IdProducto"]
        name = self.selected_producto["NombreProducto"]
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(f"{API_URL}/productos/{item_id}")
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo eliminar")
                except ValueError:
                    detail = "No se pudo eliminar"
                self.show_producto_delete = False
                yield rx.toast(title="Error al eliminar", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            self.show_producto_delete = False
            self.selected_producto = dict(EMPTY_PRODUCTO)
            yield rx.toast(title="Producto eliminado", description=f"'{name}' eliminado.", duration=3000, close_button=True)
        except httpx.RequestError:
            self.show_producto_delete = False
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)
        except Exception as error:
            self.show_producto_delete = False
            yield rx.toast(title="Error inesperado", description=str(error), duration=4000, close_button=True)

    @rx.event
    async def submit_producto(self, form_data: dict):
        codigo = form_data.get("CodigoProducto", "").strip()
        nombre = form_data.get("NombreProducto", "").strip()
        if not codigo or not nombre:
            self.producto_form_error = "Codigo y Nombre son obligatorios"
            return
        idProveedor = form_data.get("IdProveedor")
        if not idProveedor:
            self.producto_form_error = "El proveedor es obligatorio"
            return
        body = {
            "IdProveedor": int(idProveedor),
            "CodigoProducto": codigo,
            "CodigoBarras": form_data.get("CodigoBarras", "").strip() or None,
            "NombreProducto": nombre,
            "DescripcionProducto": form_data.get("DescripcionProducto", "").strip() or None,
            "CategoriaProducto": form_data.get("CategoriaProducto", "").strip() or None,
            "PrecioCompra": float(form_data.get("PrecioCompra", 0)),
            "PrecioVenta": float(form_data.get("PrecioVenta", 0)),
            "CantidadReorden": int(form_data.get("CantidadReorden", 0)),
            "PesoEmpaque": float(form_data.get("PesoEmpaque", 0) or 0),
            "AltoEmpaque": float(form_data.get("AltoEmpaque", 0) or 0),
            "AnchoEmpaque": float(form_data.get("AnchoEmpaque", 0) or 0),
            "ProfundidadEmpaque": float(form_data.get("ProfundidadEmpaque", 0) or 0),
            "Refrigerado": bool(form_data.get("Refrigerado", False)),
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if self.is_editing_producto:
                    pid = self.editing_producto["IdProducto"]
                    response = await client.put(f"{API_URL}/productos/{pid}", json=body)
                    msg = "Producto actualizado"
                else:
                    response = await client.post(f"{API_URL}/productos", json=body)
                    msg = "Producto creado"
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo guardar")
                except ValueError:
                    detail = "No se pudo guardar"
                self.producto_form_error = str(detail)
                return
            await self.load_data()
            self.show_producto_form = False
            self.producto_form_error = ""
            self.is_editing_producto = False
            yield rx.toast(title=msg, duration=3000, close_button=True)
        except httpx.RequestError:
            self.producto_form_error = "No se pudo conectar con la API"
        except Exception as error:
            self.producto_form_error = str(error)

    # =====================================================================
    #  CLIENTE CRUD
    # =====================================================================

    @rx.event
    def open_new_cliente(self):
        self.editing_cliente = dict(EMPTY_CLIENTE)
        self.is_editing_cliente = False
        self.cliente_form_error = ""
        self.show_cliente_form = True

    @rx.event
    def open_edit_cliente(self, item: Cliente):
        self.editing_cliente = dict(item)
        self.is_editing_cliente = True
        self.cliente_form_error = ""
        self.show_cliente_form = True

    @rx.event
    def close_cliente_form(self):
        self.show_cliente_form = False
        self.cliente_form_error = ""

    @rx.event
    def open_cliente_detail(self, item: Cliente):
        self.selected_cliente = dict(item)
        self.show_cliente_detail = True

    @rx.event
    def close_cliente_detail(self):
        self.show_cliente_detail = False

    @rx.event
    def open_delete_cliente(self, item: Cliente):
        self.selected_cliente = dict(item)
        self.show_cliente_delete = True

    @rx.event
    def close_delete_cliente(self):
        self.show_cliente_delete = False

    @rx.event
    async def confirm_delete_cliente(self):
        item_id = self.selected_cliente["IdCliente"]
        name = self.selected_cliente["NombreCliente"]
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(f"{API_URL}/clientes/{item_id}")
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo eliminar")
                except ValueError:
                    detail = "No se pudo eliminar"
                self.show_cliente_delete = False
                yield rx.toast(title="Error al eliminar", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            self.show_cliente_delete = False
            self.selected_cliente = dict(EMPTY_CLIENTE)
            yield rx.toast(title="Cliente eliminado", description=f"'{name}' eliminado.", duration=3000, close_button=True)
        except httpx.RequestError:
            self.show_cliente_delete = False
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)
        except Exception as error:
            self.show_cliente_delete = False
            yield rx.toast(title="Error inesperado", description=str(error), duration=4000, close_button=True)

    @rx.event
    async def submit_cliente(self, form_data: dict):
        nombre = form_data.get("NombreCliente", "").strip()
        if not nombre:
            self.cliente_form_error = "El nombre es obligatorio"
            return
        body = {
            "NombreCliente": nombre,
            "DireccionCliente": form_data.get("DireccionCliente", "").strip(),
            "Telefono": form_data.get("Telefono", "").strip(),
            "Email": form_data.get("Email", "").strip(),
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if self.is_editing_cliente:
                    pid = self.editing_cliente["IdCliente"]
                    response = await client.put(f"{API_URL}/clientes/{pid}", json=body)
                    msg = "Cliente actualizado"
                else:
                    response = await client.post(f"{API_URL}/clientes", json=body)
                    msg = "Cliente creado"
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo guardar")
                except ValueError:
                    detail = "No se pudo guardar"
                self.cliente_form_error = str(detail)
                return
            await self.load_data()
            self.show_cliente_form = False
            self.cliente_form_error = ""
            self.is_editing_cliente = False
            yield rx.toast(title=msg, duration=3000, close_button=True)
        except httpx.RequestError:
            self.cliente_form_error = "No se pudo conectar con la API"
        except Exception as error:
            self.cliente_form_error = str(error)

    # =====================================================================
    #  PEDIDO CRUD
    # =====================================================================

    @rx.event
    def open_new_pedido(self):
        self.editing_pedido = dict(EMPTY_PEDIDO)
        self.is_editing_pedido = False
        self.pedido_form_error = ""
        self.pedido_form_detalles = []
        self.pedido_detalle_temp_producto = ""
        self.pedido_detalle_temp_cantidad = "1"
        self.pedido_detalle_temp_precio = "0"
        self.show_pedido_form = True

    @rx.event
    def open_edit_pedido(self, item: Pedido):
        self.editing_pedido = dict(item)
        self.is_editing_pedido = True
        self.pedido_form_error = ""
        self.pedido_detalle_temp_producto = ""
        self.pedido_detalle_temp_cantidad = "1"
        self.pedido_detalle_temp_precio = "0"
        existing_detalles = item.get("detalles") or []
        self.pedido_form_detalles = [
            {
                "ApiId": int(d["IdDetallePedido"]),
                "IdProducto": int(d["IdProducto"]),
                "NombreProducto": (d.get("producto") or {}).get("NombreProducto", "---"),
                "Cantidad": int(d["Cantidad"]),
                "PrecioUnitario": float(d["PrecioUnitario"]),
                "Subtotal": round(float(d["Cantidad"]) * float(d["PrecioUnitario"]), 2),
            }
            for d in existing_detalles
            if (d.get("producto") or {}).get("Activo", True)
        ]
        self.show_pedido_form = True

    @rx.event
    def close_pedido_form(self):
        self.show_pedido_form = False
        self.pedido_form_error = ""

    @rx.event
    def open_pedido_detail(self, item: Pedido):
        pedido = dict(item)
        pedido["detalles"] = [
            d for d in (pedido.get("detalles") or [])
            if (d.get("producto") or {}).get("Activo", True)
        ]
        self.selected_pedido = pedido
        self.show_pedido_detail = True

    @rx.event
    def close_pedido_detail(self):
        self.show_pedido_detail = False

    @rx.event
    async def cambiar_estado_pedido(self, item: Pedido, nuevo_estado: str, id_almacen: Optional[int] = None):
        pid = item["IdPedido"]
        body: dict = {"Estado": nuevo_estado}
        if nuevo_estado in ("Entregado", "Parcial") and id_almacen:
            body["IdAlmacen"] = id_almacen
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.put(f"{API_URL}/pedidos/{pid}", json=body)
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo actualizar")
                except ValueError:
                    detail = "No se pudo actualizar"
                yield rx.toast(title="Error", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            self.selected_pedido = dict(item)
            self.selected_pedido["Estado"] = nuevo_estado
            yield rx.toast(title=f"Pedido #{pid} → {nuevo_estado}", duration=3000, close_button=True)
        except httpx.RequestError:
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)

    @rx.event
    def open_pedido_recepcion_modal(self, item: Pedido):
        self.selected_pedido = dict(item)
        self.pedido_recepcion_almacen_id = ""
        self.show_pedido_recepcion_modal = True

    @rx.event
    def close_pedido_recepcion_modal(self):
        self.show_pedido_recepcion_modal = False
        self.pedido_recepcion_almacen_id = ""

    @rx.event
    def set_pedido_recepcion_almacen_id(self, v: str):
        self.pedido_recepcion_almacen_id = v

    @rx.event
    async def confirm_pedido_recepcion(self):
        id_almacen = self.pedido_recepcion_almacen_id
        if not id_almacen:
            yield rx.toast(title="Error", description="Selecciona un almacen de destino", duration=3000, close_button=True)
            return
        self.show_pedido_recepcion_modal = False
        async for result in self.cambiar_estado_pedido(self.selected_pedido, "Entregado", int(id_almacen)):
            yield result

    @rx.event
    def open_delete_pedido(self, item: Pedido):
        self.selected_pedido = dict(item)
        self.show_pedido_delete = True

    @rx.event
    def close_delete_pedido(self):
        self.show_pedido_delete = False

    @rx.event
    async def confirm_delete_pedido(self):
        item_id = self.selected_pedido["IdPedido"]
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(f"{API_URL}/pedidos/{item_id}")
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo eliminar")
                except ValueError:
                    detail = "No se pudo eliminar"
                self.show_pedido_delete = False
                yield rx.toast(title="Error al eliminar", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            self.show_pedido_delete = False
            self.selected_pedido = dict(EMPTY_PEDIDO)
            yield rx.toast(title="Pedido eliminado", description=f"Pedido #{item_id} eliminado.", duration=3000, close_button=True)
        except httpx.RequestError:
            self.show_pedido_delete = False
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)
        except Exception as error:
            self.show_pedido_delete = False
            yield rx.toast(title="Error inesperado", description=str(error), duration=4000, close_button=True)

    @rx.event
    async def submit_pedido(self, form_data: dict):
        fd = form_data if isinstance(form_data, dict) else {}
        if self.is_editing_pedido:
            pid = self.editing_pedido["IdPedido"]
            body = {}
            id_prov = fd.get("IdProveedor") or self.editing_pedido.get("IdProveedor")
            if id_prov:
                body["IdProveedor"] = int(id_prov)
            if not body and not self.pedido_form_detalles:
                self.pedido_form_error = "No hay cambios para guardar"
                return
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    if body:
                        response = await client.put(f"{API_URL}/pedidos/{pid}", json=body)
                        if response.status_code >= 400:
                            try:
                                detail = response.json().get("detail", "No se pudo actualizar")
                            except ValueError:
                                detail = "No se pudo actualizar"
                            self.pedido_form_error = str(detail)
                            return
                    existing_res = await client.get(f"{API_URL}/pedidos/{pid}/detalles")
                    existing_json = existing_res.json() if existing_res.status_code == 200 else {}
                    existing = existing_json.get("data", existing_json) if isinstance(existing_json, dict) else existing_json
                form_api_ids = set()
                for d in self.pedido_form_detalles:
                    if isinstance(d, dict) and d.get("ApiId"):
                        form_api_ids.add(int(d["ApiId"]))
                async with httpx.AsyncClient(timeout=10.0) as client:
                    for det in existing:
                        if not isinstance(det, dict):
                            continue
                        did = det.get("IdDetallePedido")
                        if did and int(did) not in form_api_ids:
                            await client.delete(f"{API_URL}/pedidos/{pid}/detalles/{did}")
                    for d in self.pedido_form_detalles:
                        if not isinstance(d, dict):
                            continue
                        payload = {
                            "IdProducto": int(d.get("IdProducto", 0)),
                            "Cantidad": int(d.get("Cantidad", 0)),
                            "PrecioUnitario": float(d.get("PrecioUnitario", 0)),
                        }
                        api_id = d.get("ApiId")
                        if api_id and int(api_id) > 0:
                            await client.put(f"{API_URL}/pedidos/{pid}/detalles/{api_id}", json=payload)
                        else:
                            await client.post(f"{API_URL}/pedidos/{pid}/detalles", json=payload)
                await self.load_data()
                self.show_pedido_form = False
                self.pedido_form_error = ""
                self.is_editing_pedido = False
                yield rx.toast(title="Pedido actualizado", duration=3000, close_button=True)
            except httpx.RequestError:
                self.pedido_form_error = "No se pudo conectar con la API"
            except Exception as error:
                self.pedido_form_error = str(error)
        else:
            idProveedor = fd.get("IdProveedor") or self.editing_pedido.get("IdProveedor")
            if not idProveedor:
                self.pedido_form_error = "El proveedor es obligatorio"
                return
            body = {
                "IdProveedor": int(idProveedor),
                "Estado": "Pendiente",
                "detalles": [
                    {"IdProducto": d["IdProducto"], "Cantidad": d["Cantidad"], "PrecioUnitario": d["PrecioUnitario"]}
                    for d in self.pedido_form_detalles
                    if isinstance(d, dict)
                ],
            }
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(f"{API_URL}/pedidos", json=body)
                if response.status_code >= 400:
                    try:
                        detail = response.json().get("detail", "No se pudo crear el pedido")
                    except ValueError:
                        detail = "No se pudo crear el pedido"
                    self.pedido_form_error = str(detail)
                    return
                await self.load_data()
                self.show_pedido_form = False
                self.pedido_form_error = ""
                self.is_editing_pedido = False
                yield rx.toast(title="Pedido creado", duration=3000, close_button=True)
            except httpx.RequestError:
                self.pedido_form_error = "No se pudo conectar con la API"
            except Exception as error:
                self.pedido_form_error = str(error)

    # =====================================================================
    #  ENTREGA CRUD
    # =====================================================================

    @rx.event
    def open_new_entrega(self):
        self.editing_entrega = dict(EMPTY_ENTREGA)
        self.is_editing_entrega = False
        self.entrega_form_error = ""
        self.show_entrega_form = True

    @rx.event
    def open_edit_entrega(self, item: Entrega):
        self.editing_entrega = dict(item)
        self.is_editing_entrega = True
        self.entrega_form_error = ""
        self.show_entrega_form = True

    @rx.event
    def close_entrega_form(self):
        self.show_entrega_form = False
        self.entrega_form_error = ""

    @rx.event
    def open_entrega_detail(self, item: Entrega):
        self.selected_entrega = dict(item)
        self.show_entrega_detail = True

    @rx.event
    def close_entrega_detail(self):
        self.show_entrega_detail = False

    @rx.event
    async def cambiar_estado_entrega(self, item: Entrega, nuevo_estado: str, id_almacen: Optional[int] = None):
        eid = item["IdEntrega"]
        body: dict = {"Estado": nuevo_estado}
        if nuevo_estado == "En transito" and id_almacen:
            body["IdAlmacen"] = id_almacen
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.put(f"{API_URL}/entregas/{eid}", json=body)
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo actualizar")
                except ValueError:
                    detail = "No se pudo actualizar"
                yield rx.toast(title="Error", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            self.selected_entrega = dict(item)
            self.selected_entrega["Estado"] = nuevo_estado
            yield rx.toast(title=f"Entrega #{eid} → {nuevo_estado}", duration=3000, close_button=True)
        except httpx.RequestError:
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)

    @rx.event
    def open_delete_entrega(self, item: Entrega):
        self.selected_entrega = dict(item)
        self.show_entrega_delete = True

    @rx.event
    def close_delete_entrega(self):
        self.show_entrega_delete = False

    @rx.event
    async def confirm_delete_entrega(self):
        item_id = self.selected_entrega["IdEntrega"]
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(f"{API_URL}/entregas/{item_id}")
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo eliminar")
                except ValueError:
                    detail = "No se pudo eliminar"
                self.show_entrega_delete = False
                yield rx.toast(title="Error al eliminar", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            self.show_entrega_delete = False
            self.selected_entrega = dict(EMPTY_ENTREGA)
            yield rx.toast(title="Entrega eliminada", description=f"Entrega #{item_id} eliminada.", duration=3000, close_button=True)
        except httpx.RequestError:
            self.show_entrega_delete = False
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)
        except Exception as error:
            self.show_entrega_delete = False
            yield rx.toast(title="Error inesperado", description=str(error), duration=4000, close_button=True)

    @rx.event
    async def submit_entrega(self, form_data: dict):
        if self.is_editing_entrega:
            eid = self.editing_entrega["IdEntrega"]
            body = {
                "IdCliente": int(form_data["IdCliente"]) if form_data.get("IdCliente") else None,
                "IdPedido": int(form_data["IdPedido"]) if form_data.get("IdPedido") else None,
                "FechaVenta": form_data.get("FechaVenta") or None,
                "FechaEsperada": form_data.get("FechaEsperada") or None,
                "FechaReal": form_data.get("FechaReal") or None,
                "Estado": form_data.get("Estado") or None,
            }
            body = {k: v for k, v in body.items() if v is not None}
            if not body:
                self.entrega_form_error = "No hay cambios para guardar"
                return
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.put(f"{API_URL}/entregas/{eid}", json=body)
                if response.status_code >= 400:
                    try:
                        detail = response.json().get("detail", "No se pudo actualizar")
                    except ValueError:
                        detail = "No se pudo actualizar"
                    self.entrega_form_error = str(detail)
                    return
                await self.load_data()
                self.show_entrega_form = False
                self.entrega_form_error = ""
                self.is_editing_entrega = False
                yield rx.toast(title="Entrega actualizada", duration=3000, close_button=True)
            except httpx.RequestError:
                self.entrega_form_error = "No se pudo conectar con la API"
            except Exception as error:
                self.entrega_form_error = str(error)
        else:
            idCliente = form_data.get("IdCliente")
            idPedido = form_data.get("IdPedido")
            if not idCliente or not idPedido:
                self.entrega_form_error = "Cliente y Pedido son obligatorios"
                return
            body = {
                "IdCliente": int(idCliente),
                "IdPedido": int(idPedido),
                "FechaVenta": form_data.get("FechaVenta", ""),
                "FechaEsperada": form_data.get("FechaEsperada", ""),
                "FechaReal": form_data.get("FechaReal", "") or None,
                "Estado": form_data.get("Estado", "Pendiente"),
            }
            try:
                async with httpx.AsyncClient(timeout=10.0) as client:
                    response = await client.post(f"{API_URL}/entregas", json=body)
                if response.status_code >= 400:
                    try:
                        detail = response.json().get("detail", "No se pudo crear la entrega")
                    except ValueError:
                        detail = "No se pudo crear la entrega"
                    self.entrega_form_error = str(detail)
                    return
                await self.load_data()
                self.show_entrega_form = False
                self.entrega_form_error = ""
                self.is_editing_entrega = False
                yield rx.toast(title="Entrega creada", duration=3000, close_button=True)
            except httpx.RequestError:
                self.entrega_form_error = "No se pudo conectar con la API"
            except Exception as error:
                self.entrega_form_error = str(error)

    # =====================================================================
    #  UBICACION CRUD
    # =====================================================================

    @rx.event
    def open_new_ubicacion(self):
        self.editing_ubicacion = dict(EMPTY_UBICACION)
        self.is_editing_ubicacion = False
        self.ubicacion_form_error = ""
        self.show_ubicacion_form = True

    @rx.event
    def open_edit_ubicacion(self, item: Ubicacion):
        self.editing_ubicacion = dict(item)
        self.is_editing_ubicacion = True
        self.ubicacion_form_error = ""
        self.show_ubicacion_form = True

    @rx.event
    def close_ubicacion_form(self):
        self.show_ubicacion_form = False
        self.ubicacion_form_error = ""

    @rx.event
    def open_ubicacion_detail(self, item: Ubicacion):
        self.selected_ubicacion = dict(item)
        self.show_ubicacion_detail = True

    @rx.event
    def close_ubicacion_detail(self):
        self.show_ubicacion_detail = False

    @rx.event
    def open_delete_ubicacion(self, item: Ubicacion):
        self.selected_ubicacion = dict(item)
        self.show_ubicacion_delete = True

    @rx.event
    def close_delete_ubicacion(self):
        self.show_ubicacion_delete = False

    @rx.event
    async def confirm_delete_ubicacion(self):
        item_id = self.selected_ubicacion["IdUbicacion"]
        name = self.selected_ubicacion["NombreUbicacion"]
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(f"{API_URL}/ubicaciones/{item_id}")
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo eliminar")
                except ValueError:
                    detail = "No se pudo eliminar"
                self.show_ubicacion_delete = False
                yield rx.toast(title="Error al eliminar", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            self.show_ubicacion_delete = False
            self.selected_ubicacion = dict(EMPTY_UBICACION)
            yield rx.toast(title="Ubicacion eliminada", description=f"'{name}' eliminada.", duration=3000, close_button=True)
        except httpx.RequestError:
            self.show_ubicacion_delete = False
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)
        except Exception as error:
            self.show_ubicacion_delete = False
            yield rx.toast(title="Error inesperado", description=str(error), duration=4000, close_button=True)

    @rx.event
    async def submit_ubicacion(self, form_data: dict):
        nombre = form_data.get("NombreUbicacion", "").strip()
        if not nombre:
            self.ubicacion_form_error = "El nombre es obligatorio"
            return
        body = {
            "NombreUbicacion": nombre,
            "DireccionUbicacion": form_data.get("DireccionUbicacion", "").strip(),
            "Ciudad": form_data.get("Ciudad", "").strip(),
            "Referencia": form_data.get("Referencia", "").strip() or None,
            "TelefonoContacto": form_data.get("TelefonoContacto", "").strip() or None,
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if self.is_editing_ubicacion:
                    pid = self.editing_ubicacion["IdUbicacion"]
                    response = await client.put(f"{API_URL}/ubicaciones/{pid}", json=body)
                    msg = "Ubicacion actualizada"
                else:
                    response = await client.post(f"{API_URL}/ubicaciones", json=body)
                    msg = "Ubicacion creada"
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo guardar")
                except ValueError:
                    detail = "No se pudo guardar"
                self.ubicacion_form_error = str(detail)
                return
            await self.load_data()
            self.show_ubicacion_form = False
            self.ubicacion_form_error = ""
            self.is_editing_ubicacion = False
            yield rx.toast(title=msg, duration=3000, close_button=True)
        except httpx.RequestError:
            self.ubicacion_form_error = "No se pudo conectar con la API"
        except Exception as error:
            self.ubicacion_form_error = str(error)

    # =====================================================================
    #  ALMACEN CRUD
    # =====================================================================

    @rx.event
    def open_new_almacen(self):
        self.editing_almacen = dict(EMPTY_ALMACEN)
        self.is_editing_almacen = False
        self.almacen_form_error = ""
        self.show_almacen_form = True

    @rx.event
    def open_edit_almacen(self, item: Almacen):
        self.editing_almacen = dict(item)
        self.is_editing_almacen = True
        self.almacen_form_error = ""
        self.show_almacen_form = True

    @rx.event
    def close_almacen_form(self):
        self.show_almacen_form = False
        self.almacen_form_error = ""

    @rx.event
    def open_almacen_detail(self, item: Almacen):
        self.selected_almacen = dict(item)
        self.show_almacen_detail = True

    @rx.event
    def close_almacen_detail(self):
        self.show_almacen_detail = False

    @rx.event
    def open_delete_almacen(self, item: Almacen):
        self.selected_almacen = dict(item)
        self.show_almacen_delete = True

    @rx.event
    def close_delete_almacen(self):
        self.show_almacen_delete = False

    @rx.event
    async def confirm_delete_almacen(self):
        item_id = self.selected_almacen["IdAlmacen"]
        name = self.selected_almacen["NombreAlmacen"]
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(f"{API_URL}/almacenes/{item_id}")
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo eliminar")
                except ValueError:
                    detail = "No se pudo eliminar"
                self.show_almacen_delete = False
                yield rx.toast(title="Error al eliminar", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            self.show_almacen_delete = False
            self.selected_almacen = dict(EMPTY_ALMACEN)
            yield rx.toast(title="Almacen eliminado", description=f"'{name}' eliminado.", duration=3000, close_button=True)
        except httpx.RequestError:
            self.show_almacen_delete = False
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)
        except Exception as error:
            self.show_almacen_delete = False
            yield rx.toast(title="Error inesperado", description=str(error), duration=4000, close_button=True)

    @rx.event
    async def submit_almacen(self, form_data: dict):
        nombre = form_data.get("NombreAlmacen", "").strip()
        idUbicacion = form_data.get("IdUbicacion")
        if not nombre or not idUbicacion:
            self.almacen_form_error = "Nombre y Ubicacion son obligatorios"
            return
        body = {
            "IdUbicacion": int(idUbicacion),
            "NombreAlmacen": nombre,
            "EsRefrigerado": bool(form_data.get("EsRefrigerado", False)),
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if self.is_editing_almacen:
                    pid = self.editing_almacen["IdAlmacen"]
                    response = await client.put(f"{API_URL}/almacenes/{pid}", json=body)
                    msg = "Almacen actualizado"
                else:
                    response = await client.post(f"{API_URL}/almacenes", json=body)
                    msg = "Almacen creado"
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo guardar")
                except ValueError:
                    detail = "No se pudo guardar"
                self.almacen_form_error = str(detail)
                return
            await self.load_data()
            self.show_almacen_form = False
            self.almacen_form_error = ""
            self.is_editing_almacen = False
            yield rx.toast(title=msg, duration=3000, close_button=True)
        except httpx.RequestError:
            self.almacen_form_error = "No se pudo conectar con la API"
        except Exception as error:
            self.almacen_form_error = str(error)

    # =====================================================================
    #  INVENTARIO CRUD
    # =====================================================================

    @rx.event
    def open_new_inventario(self):
        self.editing_inventario = dict(EMPTY_INVENTARIO)
        self.is_editing_inventario = False
        self.inventario_form_error = ""
        self.show_inventario_form = True

    @rx.event
    def open_edit_inventario(self, item: Inventario):
        self.editing_inventario = dict(item)
        self.is_editing_inventario = True
        self.inventario_form_error = ""
        self.show_inventario_form = True

    @rx.event
    def close_inventario_form(self):
        self.show_inventario_form = False
        self.inventario_form_error = ""

    @rx.event
    def open_inventario_detail(self, item: Inventario):
        self.selected_inventario = dict(item)
        self.show_inventario_detail = True

    @rx.event
    def close_inventario_detail(self):
        self.show_inventario_detail = False

    @rx.event
    def open_delete_inventario(self, item: Inventario):
        self.selected_inventario = dict(item)
        self.show_inventario_delete = True

    @rx.event
    def close_delete_inventario(self):
        self.show_inventario_delete = False

    @rx.event
    async def confirm_delete_inventario(self):
        item_id = self.selected_inventario["IdInventario"]
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(f"{API_URL}/inventarios/{item_id}")
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo eliminar")
                except ValueError:
                    detail = "No se pudo eliminar"
                self.show_inventario_delete = False
                yield rx.toast(title="Error al eliminar", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            self.show_inventario_delete = False
            self.selected_inventario = dict(EMPTY_INVENTARIO)
            yield rx.toast(title="Inventario eliminado", description=f"Inventario #{item_id} eliminado.", duration=3000, close_button=True)
        except httpx.RequestError:
            self.show_inventario_delete = False
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)
        except Exception as error:
            self.show_inventario_delete = False
            yield rx.toast(title="Error inesperado", description=str(error), duration=4000, close_button=True)

    @rx.event
    async def submit_inventario(self, form_data: dict):
        idProducto = form_data.get("IdProducto")
        idAlmacen = form_data.get("IdAlmacen")
        if not idProducto or not idAlmacen:
            self.inventario_form_error = "Producto y Almacen son obligatorios"
            return
        body = {
            "IdProducto": int(idProducto),
            "IdAlmacen": int(idAlmacen),
            "CantidadDisponible": int(form_data.get("CantidadDisponible", 0)),
            "StockMinimo": int(form_data.get("StockMinimo", 0)),
            "StockMaximo": int(form_data.get("StockMaximo", 0)),
            "PuntoReorden": int(form_data.get("PuntoReorden", 0)),
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if self.is_editing_inventario:
                    pid = self.editing_inventario["IdInventario"]
                    response = await client.put(f"{API_URL}/inventarios/{pid}", json=body)
                    msg = "Inventario actualizado"
                else:
                    response = await client.post(f"{API_URL}/inventarios", json=body)
                    msg = "Inventario creado"
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo guardar")
                except ValueError:
                    detail = "No se pudo guardar"
                self.inventario_form_error = str(detail)
                return
            await self.load_data()
            self.show_inventario_form = False
            self.inventario_form_error = ""
            self.is_editing_inventario = False
            yield rx.toast(title=msg, duration=3000, close_button=True)
        except httpx.RequestError:
            self.inventario_form_error = "No se pudo conectar con la API"
        except Exception as error:
            self.inventario_form_error = str(error)

    # =====================================================================
    #  TRANSFERENCIA CRUD
    # =====================================================================

    @rx.event
    def open_new_transferencia(self):
        self.editing_transferencia = dict(EMPTY_TRANSFERENCIA)
        self.is_editing_transferencia = False
        self.transferencia_form_error = ""
        self.transferencia_form_detalles = []
        self.transferencia_detalle_temp_producto = ""
        self.transferencia_detalle_temp_cantidad = "1"
        self.show_transferencia_form = True

    @rx.event
    def open_edit_transferencia(self, item: Transferencia):
        self.editing_transferencia = dict(item)
        self.is_editing_transferencia = True
        self.transferencia_form_error = ""
        self.transferencia_detalle_temp_producto = ""
        self.transferencia_detalle_temp_cantidad = "1"
        existing_detalles = item.get("detalles") or []
        self.transferencia_form_detalles = [
            {
                "_idx": i,
                "IdProducto": int(d["IdProducto"]),
                "_nombre_producto": (d.get("producto") or {}).get("NombreProducto", "---"),
                "CantidadTransferida": int(d["CantidadTransferida"]),
            }
            for i, d in enumerate(existing_detalles)
        ]
        self.show_transferencia_form = True

    @rx.event
    def close_transferencia_form(self):
        self.show_transferencia_form = False
        self.transferencia_form_error = ""

    @rx.event
    def open_transferencia_detail(self, item: Transferencia):
        self.selected_transferencia = dict(item)
        self.transferencia_recepcion_almacen = ""
        self.show_transferencia_detail = True

    @rx.event
    def close_transferencia_detail(self):
        self.show_transferencia_detail = False

    @rx.event
    def open_delete_transferencia(self, item: Transferencia):
        self.selected_transferencia = dict(item)
        self.show_transferencia_delete = True

    @rx.event
    def close_delete_transferencia(self):
        self.show_transferencia_delete = False

    @rx.event
    async def confirm_delete_transferencia(self):
        item_id = self.selected_transferencia["IdTransferencia"]
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(f"{API_URL}/transferencias/{item_id}")
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo eliminar")
                except ValueError:
                    detail = "No se pudo eliminar"
                self.show_transferencia_delete = False
                yield rx.toast(title="Error al eliminar", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            self.show_transferencia_delete = False
            self.selected_transferencia = dict(EMPTY_TRANSFERENCIA)
            yield rx.toast(title="Transferencia eliminada", description=f"Transferencia #{item_id} eliminada.", duration=3000, close_button=True)
        except httpx.RequestError:
            self.show_transferencia_delete = False
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)
        except Exception as error:
            self.show_transferencia_delete = False
            yield rx.toast(title="Error inesperado", description=str(error), duration=4000, close_button=True)

    @rx.event
    async def cambiar_estado_transferencia(self, item: Transferencia, nuevo_estado: str):
        tid = item["IdTransferencia"]
        body: dict = {"Estado": nuevo_estado}
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.put(f"{API_URL}/transferencias/{tid}", json=body)
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo actualizar")
                except ValueError:
                    detail = "No se pudo actualizar"
                yield rx.toast(title="Error", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            self.selected_transferencia["Estado"] = nuevo_estado
            yield rx.toast(title=f"Transferencia #{tid} → {nuevo_estado}", duration=3000, close_button=True)
        except httpx.RequestError:
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)

    @rx.event
    async def submit_transferencia(self, form_data: dict):
        idOrigen = form_data.get("IdAlmacenOrigen")
        idDestino = form_data.get("IdAlmacenDestino")
        if not idOrigen or not idDestino:
            self.transferencia_form_error = "Almacen origen y destino son obligatorios"
            return
        if int(idOrigen) == int(idDestino):
            self.transferencia_form_error = "Los almacenes origen y destino deben ser diferentes"
            return
        if not self.is_editing_transferencia and len(self.transferencia_form_detalles) == 0:
            self.transferencia_form_error = "Agrega al menos un producto a transferir"
            return
        detalles_payload = [{"IdProducto": int(d["IdProducto"]), "CantidadTransferida": int(d["CantidadTransferida"])} for d in self.transferencia_form_detalles]
        total_cantidad = sum(int(d["CantidadTransferida"]) for d in self.transferencia_form_detalles)
        body = {
            "IdAlmacenOrigen": int(idOrigen),
            "IdAlmacenDestino": int(idDestino),
            "CantidadTransferida": total_cantidad,
            "FechaEnvio": form_data.get("FechaEnvio", "") or None,
            "FechaRecepcion": form_data.get("FechaRecepcion", "") or None,
            "Estado": form_data.get("Estado", "Pendiente"),
            "detalles": detalles_payload,
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                if self.is_editing_transferencia:
                    pid = self.editing_transferencia["IdTransferencia"]
                    response = await client.put(f"{API_URL}/transferencias/{pid}", json=body)
                    msg = "Transferencia actualizada"
                else:
                    response = await client.post(f"{API_URL}/transferencias", json=body)
                    msg = "Transferencia creada"
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo guardar")
                except ValueError:
                    detail = "No se pudo guardar"
                self.transferencia_form_error = str(detail)
                return
            await self.load_data()
            self.show_transferencia_form = False
            self.transferencia_form_error = ""
            self.is_editing_transferencia = False
            yield rx.toast(title=msg, duration=3000, close_button=True)
        except httpx.RequestError:
            self.transferencia_form_error = "No se pudo conectar con la API"
        except Exception as error:
            self.transferencia_form_error = str(error)

    @rx.event
    def add_transferencia_detalle_temp(self):
        id_producto = str(self.transferencia_detalle_temp_producto).strip()
        if not id_producto:
            self.transferencia_form_error = "Selecciona un producto para el detalle"
            return
        cantidad = int(self.transferencia_detalle_temp_cantidad or "1")
        nombre = ""
        for p in self.productos:
            if str(p["IdProducto"]) == id_producto:
                nombre = p["NombreProducto"]
                break
        idx = len(self.transferencia_form_detalles)
        self.transferencia_form_detalles = self.transferencia_form_detalles + [{
            "_idx": idx,
            "IdProducto": int(id_producto),
            "_nombre_producto": nombre,
            "CantidadTransferida": cantidad,
        }]
        self.transferencia_detalle_temp_producto = ""
        self.transferencia_detalle_temp_cantidad = "1"
        self.transferencia_form_error = ""

    @rx.event
    def remove_transferencia_detalle_temp(self, idx: int):
        self.transferencia_form_detalles = [
            {**d, "_idx": i} for i, d in enumerate(self.transferencia_form_detalles) if d.get("_idx") != idx
        ]

    @rx.event
    def set_transferencia_detalle_temp_producto(self, v: str):
        self.transferencia_detalle_temp_producto = v

    @rx.event
    def set_transferencia_detalle_temp_cantidad(self, v: str):
        self.transferencia_detalle_temp_cantidad = v

    @rx.event
    async def add_detalle_transferencia(self, transferencia_id: int, form_data: dict):
        idProducto = form_data.get("IdProducto")
        if not idProducto:
            yield rx.toast(title="Error", description="Producto es obligatorio", duration=3000, close_button=True)
            return
        body = {
            "IdProducto": int(idProducto),
            "CantidadTransferida": int(form_data.get("CantidadTransferida", 1)),
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(f"{API_URL}/transferencias/{transferencia_id}/detalles", json=body)
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo agregar")
                except ValueError:
                    detail = "No se pudo agregar"
                yield rx.toast(title="Error", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            yield rx.toast(title="Detalle agregado", duration=3000, close_button=True)
        except httpx.RequestError:
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)

    @rx.event
    async def delete_detalle_transferencia(self, transferencia_id: int, detalle_id: int):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(f"{API_URL}/transferencias/{transferencia_id}/detalles/{detalle_id}")
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo eliminar")
                except ValueError:
                    detail = "No se pudo eliminar"
                yield rx.toast(title="Error", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            yield rx.toast(title="Detalle eliminado", duration=3000, close_button=True)
        except httpx.RequestError:
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)

    # =====================================================================
    #  DETALLE PEDIDO CRUD
    # =====================================================================

    @rx.event
    async def add_detalle_pedido(self, pedido_id: int, form_data: dict):
        idProducto = form_data.get("IdProducto")
        if not idProducto:
            yield rx.toast(title="Error", description="Producto es obligatorio", duration=3000, close_button=True)
            return
        body = {
            "IdProducto": int(idProducto),
            "Cantidad": int(form_data.get("Cantidad", 0)),
            "PrecioUnitario": float(form_data.get("PrecioUnitario", 0)),
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(f"{API_URL}/pedidos/{pedido_id}/detalles", json=body)
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo agregar")
                except ValueError:
                    detail = "No se pudo agregar"
                yield rx.toast(title="Error", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            yield rx.toast(title="Detalle agregado", duration=3000, close_button=True)
        except httpx.RequestError:
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)

    @rx.event
    async def update_detalle_pedido(self, pedido_id: int, detalle_id: int, form_data: dict):
        body = {}
        if form_data.get("IdProducto"):
            body["IdProducto"] = int(form_data["IdProducto"])
        if form_data.get("Cantidad") is not None:
            body["Cantidad"] = int(form_data["Cantidad"])
        if form_data.get("PrecioUnitario") is not None:
            body["PrecioUnitario"] = float(form_data["PrecioUnitario"])
        if not body:
            return
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.put(f"{API_URL}/pedidos/{pedido_id}/detalles/{detalle_id}", json=body)
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo actualizar")
                except ValueError:
                    detail = "No se pudo actualizar"
                yield rx.toast(title="Error", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            yield rx.toast(title="Detalle actualizado", duration=3000, close_button=True)
        except httpx.RequestError:
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)

    @rx.event
    async def delete_detalle_pedido(self, pedido_id: int, detalle_id: int):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(f"{API_URL}/pedidos/{pedido_id}/detalles/{detalle_id}")
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo eliminar")
                except ValueError:
                    detail = "No se pudo eliminar"
                yield rx.toast(title="Error", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            yield rx.toast(title="Detalle eliminado", duration=3000, close_button=True)
        except httpx.RequestError:
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)

    # =====================================================================
    #  DETALLE ENTREGA CRUD
    # =====================================================================

    @rx.event
    async def add_detalle_entrega(self, entrega_id: int, form_data: dict):
        idProducto = form_data.get("IdProducto")
        if not idProducto:
            yield rx.toast(title="Error", description="Producto es obligatorio", duration=3000, close_button=True)
            return
        body = {
            "IdProducto": int(idProducto),
            "CantidadEntregada": int(form_data.get("CantidadEntregada", 0)),
            "PrecioUnitario": float(form_data.get("PrecioUnitario", 0)),
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(f"{API_URL}/entregas/{entrega_id}/detalles", json=body)
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo agregar")
                except ValueError:
                    detail = "No se pudo agregar"
                yield rx.toast(title="Error", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            yield rx.toast(title="Detalle agregado", duration=3000, close_button=True)
        except httpx.RequestError:
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)

    @rx.event
    async def update_detalle_entrega(self, entrega_id: int, detalle_id: int, form_data: dict):
        body = {}
        if form_data.get("IdProducto"):
            body["IdProducto"] = int(form_data["IdProducto"])
        if form_data.get("CantidadEntregada") is not None:
            body["CantidadEntregada"] = int(form_data["CantidadEntregada"])
        if form_data.get("PrecioUnitario") is not None:
            body["PrecioUnitario"] = float(form_data["PrecioUnitario"])
        if not body:
            return
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.put(f"{API_URL}/entregas/{entrega_id}/detalles/{detalle_id}", json=body)
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo actualizar")
                except ValueError:
                    detail = "No se pudo actualizar"
                yield rx.toast(title="Error", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            yield rx.toast(title="Detalle actualizado", duration=3000, close_button=True)
        except httpx.RequestError:
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)

    @rx.event
    async def delete_detalle_entrega(self, entrega_id: int, detalle_id: int):
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.delete(f"{API_URL}/entregas/{entrega_id}/detalles/{detalle_id}")
            if response.status_code >= 400:
                try:
                    detail = response.json().get("detail", "No se pudo eliminar")
                except ValueError:
                    detail = "No se pudo eliminar"
                yield rx.toast(title="Error", description=str(detail), duration=4000, close_button=True)
                return
            await self.load_data()
            yield rx.toast(title="Detalle eliminado", duration=3000, close_button=True)
        except httpx.RequestError:
            yield rx.toast(title="Error de conexion", description="No se pudo conectar con la API.", duration=4000, close_button=True)
