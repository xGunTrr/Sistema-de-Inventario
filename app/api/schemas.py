from datetime import datetime
from typing import Optional

from pydantic import BaseModel


# ---------- Proveedor ----------

class ProveedorIn(BaseModel):
    NombreProveedor: str
    DireccionProveedor: str = ""
    Telefono: str = ""
    Email: str = ""
    Activo: bool = True


class ProveedorOut(BaseModel):
    IdProveedor: int
    NombreProveedor: str
    DireccionProveedor: str
    Telefono: str
    Email: str
    Activo: bool
    FechaCreacion: Optional[datetime] = None
    FechaModificacion: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------- Producto ----------

class ProductoIn(BaseModel):
    IdProveedor: int
    CodigoProducto: str
    CodigoBarras: Optional[str] = ""
    NombreProducto: str
    DescripcionProducto: Optional[str] = ""
    CategoriaProducto: Optional[str] = ""
    PrecioCompra: float = 0
    PrecioVenta: float = 0
    CantidadReorden: int = 0
    PesoEmpaque: float = 0
    AltoEmpaque: float = 0
    AnchoEmpaque: float = 0
    ProfundidadEmpaque: float = 0
    Refrigerado: bool = False
    Activo: bool = True


class ProductoOut(BaseModel):
    IdProducto: int
    IdProveedor: int
    CodigoProducto: str
    CodigoBarras: str
    NombreProducto: str
    DescripcionProducto: str
    CategoriaProducto: str
    PrecioCompra: float
    PrecioVenta: float
    CantidadReorden: int
    PesoEmpaque: float
    AltoEmpaque: float
    AnchoEmpaque: float
    ProfundidadEmpaque: float
    Refrigerado: bool
    Activo: bool
    FechaCreacion: Optional[datetime] = None
    FechaModificacion: Optional[datetime] = None
    Proveedor: Optional[ProveedorOut] = None

    class Config:
        from_attributes = True


# ---------- Cliente ----------

class ClienteIn(BaseModel):
    NombreCliente: str
    DireccionCliente: str = ""
    Telefono: str = ""
    Email: str = ""
    Activo: bool = True


class ClienteOut(BaseModel):
    IdCliente: int
    NombreCliente: str
    DireccionCliente: str
    Telefono: str
    Email: str
    Activo: bool
    FechaCreacion: Optional[datetime] = None
    FechaModificacion: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------- DetallePedido ----------

class DetallePedidoIn(BaseModel):
    IdProducto: int
    Cantidad: int = 0
    PrecioUnitario: float = 0


class DetallePedidoUpdate(BaseModel):
    IdProducto: Optional[int] = None
    Cantidad: Optional[int] = None
    CantidadRecibida: Optional[int] = None
    PrecioUnitario: Optional[float] = None


class DetallePedidoOut(BaseModel):
    IdDetallePedido: int
    IdPedido: int
    IdProducto: int
    Cantidad: int
    CantidadRecibida: int
    PrecioUnitario: float
    Activo: bool
    FechaCreacion: Optional[datetime] = None
    FechaModificacion: Optional[datetime] = None
    Producto: Optional[ProductoOut] = None

    class Config:
        from_attributes = True


# ---------- Pedido ----------

class DetalleRecepcionIn(BaseModel):
    IdDetallePedido: int
    CantidadRecibida: int


class PedidoIn(BaseModel):
    IdProveedor: int
    IdAlmacen: Optional[int] = None
    FechaPedido: Optional[datetime] = None
    Estado: str = "Pendiente"
    Activo: bool = True
    detalles: list[DetallePedidoIn] = []


class PedidoUpdate(BaseModel):
    IdProveedor: Optional[int] = None
    IdAlmacen: Optional[int] = None
    FechaPedido: Optional[datetime] = None
    Estado: Optional[str] = None
    detalles_recepcion: Optional[list[DetalleRecepcionIn]] = None


class PedidoOut(BaseModel):
    IdPedido: int
    IdProveedor: int
    FechaPedido: Optional[datetime] = None
    Estado: str
    Activo: bool
    FechaCreacion: Optional[datetime] = None
    FechaModificacion: Optional[datetime] = None
    Proveedor: Optional[ProveedorOut] = None
    detalles: list[DetallePedidoOut] = []

    class Config:
        from_attributes = True


# ---------- DetalleEntrega ----------

class DetalleEntregaIn(BaseModel):
    IdProducto: int
    CantidadEntregada: int = 0
    PrecioUnitario: float = 0


class DetalleEntregaUpdate(BaseModel):
    IdProducto: Optional[int] = None
    CantidadEntregada: Optional[int] = None
    PrecioUnitario: Optional[float] = None


class DetalleEntregaOut(BaseModel):
    IdDetalleEntrega: int
    IdEntrega: int
    IdProducto: int
    CantidadEntregada: int
    PrecioUnitario: float
    Activo: bool
    FechaCreacion: Optional[datetime] = None
    FechaModificacion: Optional[datetime] = None
    Producto: Optional[ProductoOut] = None

    class Config:
        from_attributes = True


# ---------- Entrega ----------

class EntregaIn(BaseModel):
    IdCliente: int
    IdPedido: int
    IdAlmacen: Optional[int] = None
    FechaVenta: Optional[datetime] = None
    FechaEsperada: Optional[datetime] = None
    FechaReal: Optional[datetime] = None
    Estado: str = "Pendiente"
    Activo: bool = True
    detalles: list[DetalleEntregaIn] = []


class EntregaUpdate(BaseModel):
    IdCliente: Optional[int] = None
    IdPedido: Optional[int] = None
    IdAlmacen: Optional[int] = None
    FechaVenta: Optional[datetime] = None
    FechaEsperada: Optional[datetime] = None
    FechaReal: Optional[datetime] = None
    Estado: Optional[str] = None


class EntregaOut(BaseModel):
    IdEntrega: int
    IdCliente: int
    IdPedido: int
    FechaVenta: Optional[datetime] = None
    FechaEsperada: Optional[datetime] = None
    FechaReal: Optional[datetime] = None
    Estado: str
    Activo: bool
    FechaCreacion: Optional[datetime] = None
    FechaModificacion: Optional[datetime] = None
    Cliente: Optional[ClienteOut] = None
    Pedido: Optional[PedidoOut] = None
    detalles: list[DetalleEntregaOut] = []

    class Config:
        from_attributes = True


# ---------- Ubicacion ----------

class UbicacionIn(BaseModel):
    NombreUbicacion: str
    DireccionUbicacion: Optional[str] = ""
    Ciudad: Optional[str] = ""
    Referencia: Optional[str] = ""
    TelefonoContacto: Optional[str] = ""
    Activo: bool = True


class UbicacionOut(BaseModel):
    IdUbicacion: int
    NombreUbicacion: str
    DireccionUbicacion: str
    Ciudad: str
    Referencia: str
    TelefonoContacto: str
    Activo: bool
    FechaCreacion: Optional[datetime] = None
    FechaModificacion: Optional[datetime] = None

    class Config:
        from_attributes = True


# ---------- Almacen ----------

class AlmacenIn(BaseModel):
    IdUbicacion: int
    NombreAlmacen: str
    EsRefrigerado: bool = False
    Activo: bool = True


class AlmacenOut(BaseModel):
    IdAlmacen: int
    IdUbicacion: int
    NombreAlmacen: str
    EsRefrigerado: bool
    Activo: bool
    FechaCreacion: Optional[datetime] = None
    FechaModificacion: Optional[datetime] = None
    Ubicacion: Optional[UbicacionOut] = None

    class Config:
        from_attributes = True


# ---------- Inventario ----------

class InventarioIn(BaseModel):
    IdProducto: int
    IdAlmacen: int
    CantidadDisponible: int = 0
    StockMinimo: int = 0
    StockMaximo: int = 0
    PuntoReorden: int = 0
    Activo: bool = True


class InventarioOut(BaseModel):
    IdInventario: int
    IdProducto: int
    IdAlmacen: int
    CantidadDisponible: int
    StockMinimo: int
    StockMaximo: int
    PuntoReorden: int
    Activo: bool
    FechaCreacion: Optional[datetime] = None
    FechaModificacion: Optional[datetime] = None
    Producto: Optional[ProductoOut] = None
    Almacen: Optional[AlmacenOut] = None

    class Config:
        from_attributes = True


# ---------- Transferencia ----------

class DetalleTransferenciaIn(BaseModel):
    IdProducto: int
    CantidadTransferida: int = 0


class DetalleTransferenciaUpdate(BaseModel):
    IdProducto: Optional[int] = None
    CantidadTransferida: Optional[int] = None


class DetalleTransferenciaOut(BaseModel):
    IdDetalleTransferencia: int
    IdTransferencia: int
    IdProducto: int
    CantidadTransferida: int
    Activo: bool
    FechaCreacion: Optional[datetime] = None
    FechaModificacion: Optional[datetime] = None
    Producto: Optional[ProductoOut] = None

    class Config:
        from_attributes = True


class TransferenciaIn(BaseModel):
    IdAlmacenOrigen: int
    IdAlmacenDestino: int
    CantidadTransferida: int = 0
    FechaEnvio: Optional[datetime] = None
    FechaRecepcion: Optional[datetime] = None
    Estado: str = "Pendiente"
    Activo: bool = True
    detalles: list[DetalleTransferenciaIn] = []


class TransferenciaUpdate(BaseModel):
    IdAlmacenOrigen: Optional[int] = None
    IdAlmacenDestino: Optional[int] = None
    FechaEnvio: Optional[datetime] = None
    FechaRecepcion: Optional[datetime] = None
    Estado: Optional[str] = None


class TransferenciaOut(BaseModel):
    IdTransferencia: int
    IdAlmacenOrigen: int
    IdAlmacenDestino: int
    FechaEnvio: Optional[datetime] = None
    FechaRecepcion: Optional[datetime] = None
    Estado: str
    Activo: bool
    FechaCreacion: Optional[datetime] = None
    FechaModificacion: Optional[datetime] = None
    AlmacenOrigen: Optional[AlmacenOut] = None
    AlmacenDestino: Optional[AlmacenOut] = None
    detalles: list[DetalleTransferenciaOut] = []

    class Config:
        from_attributes = True
