from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Float
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import Numeric
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .database import Base


class Proveedor(Base):
    __tablename__ = "proveedor"

    IdProveedor = Column("idproveedor", Integer, primary_key=True, index=True)
    NombreProveedor = Column("nombreproveedor", String(200), nullable=False)
    DireccionProveedor = Column("direccionproveedor", String(300), default="")
    Telefono = Column("telefono", String(50), default="")
    Email = Column("email", String(150), default="")
    Activo = Column("activo", Boolean, default=True)
    FechaCreacion = Column("fechacreacion", DateTime)
    FechaModificacion = Column("fechamodificacion", DateTime)

    productos = relationship("Producto", back_populates="proveedor")
    pedidos = relationship("Pedido", back_populates="proveedor")


class Producto(Base):
    __tablename__ = "producto"

    IdProducto = Column("idproducto", Integer, primary_key=True, index=True)
    IdProveedor = Column("idproveedor", Integer, ForeignKey("proveedor.idproveedor"), nullable=False)
    CodigoProducto = Column("codigoproducto", String(50), nullable=False)
    CodigoBarras = Column("codigobarras", String(100), default="")
    NombreProducto = Column("nombreproducto", String(200), nullable=False)
    DescripcionProducto = Column("descripcionproducto", String(500), default="")
    CategoriaProducto = Column("categoriaproducto", String(100), default="")
    PrecioCompra = Column("preciocompra", Numeric(10, 2), default=0)
    PrecioVenta = Column("precioventa", Numeric(10, 2), default=0)
    CantidadReorden = Column("cantidadreorden", Integer, default=0)
    PesoEmpaque = Column("pesoempaque", Numeric(10, 2), default=0)
    AltoEmpaque = Column("altoempaque", Numeric(10, 2), default=0)
    AnchoEmpaque = Column("anchoempaque", Numeric(10, 2), default=0)
    ProfundidadEmpaque = Column("profundidadempaque", Numeric(10, 2), default=0)
    Refrigerado = Column("refrigerado", Boolean, default=False)
    Activo = Column("activo", Boolean, default=True)
    FechaCreacion = Column("fechacreacion", DateTime)
    FechaModificacion = Column("fechamodificacion", DateTime)

    proveedor = relationship("Proveedor", back_populates="productos")
    inventarios = relationship("Inventario", back_populates="producto")
    detalles_pedido = relationship("DetallePedido", back_populates="producto")
    detalles_entrega = relationship("DetalleEntrega", back_populates="producto")
    detalles_transferencia = relationship("DetalleTransferencia", back_populates="producto")


class Cliente(Base):
    __tablename__ = "cliente"

    IdCliente = Column("idcliente", Integer, primary_key=True, index=True)
    NombreCliente = Column("nombrecliente", String(200), nullable=False)
    DireccionCliente = Column("direccioncliente", String(300), default="")
    Telefono = Column("telefono", String(50), default="")
    Email = Column("email", String(150), default="")
    Activo = Column("activo", Boolean, default=True)
    FechaCreacion = Column("fechacreacion", DateTime)
    FechaModificacion = Column("fechamodificacion", DateTime)

    entregas = relationship("Entrega", back_populates="cliente")


class Pedido(Base):
    __tablename__ = "pedido"

    IdPedido = Column("idpedido", Integer, primary_key=True, index=True)
    IdProveedor = Column("idproveedor", Integer, ForeignKey("proveedor.idproveedor"), nullable=False)
    IdAlmacen = Column("idalmacen", Integer, ForeignKey("almacen.idalmacen"), nullable=True)
    FechaPedido = Column("fechapedido", DateTime)
    Estado = Column("estado", String(50), default="Pendiente")
    Activo = Column("activo", Boolean, default=True)
    FechaCreacion = Column("fechacreacion", DateTime)
    FechaModificacion = Column("fechamodificacion", DateTime)

    proveedor = relationship("Proveedor", back_populates="pedidos")
    almacen = relationship("Almacen", back_populates="pedidos", foreign_keys=[IdAlmacen])
    detalles = relationship("DetallePedido", back_populates="pedido")
    entregas = relationship("Entrega", back_populates="pedido")


class DetallePedido(Base):
    __tablename__ = "detallepedido"

    IdDetallePedido = Column("iddetallepedido", Integer, primary_key=True, index=True)
    IdPedido = Column("idpedido", Integer, ForeignKey("pedido.idpedido"), nullable=False)
    IdProducto = Column("idproducto", Integer, ForeignKey("producto.idproducto"), nullable=False)
    Cantidad = Column("cantidad", Integer, default=0)
    CantidadRecibida = Column("cantidadrecibida", Integer, default=0)
    PrecioUnitario = Column("preciounitario", Numeric(10, 2), default=0)
    Activo = Column("activo", Boolean, default=True)
    FechaCreacion = Column("fechacreacion", DateTime)
    FechaModificacion = Column("fechamodificacion", DateTime)

    pedido = relationship("Pedido", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_pedido")


class Entrega(Base):
    __tablename__ = "entrega"

    IdEntrega = Column("identrega", Integer, primary_key=True, index=True)
    IdCliente = Column("idcliente", Integer, ForeignKey("cliente.idcliente"), nullable=False)
    IdPedido = Column("idpedido", Integer, ForeignKey("pedido.idpedido"), nullable=False)
    IdAlmacen = Column("idalmacen", Integer, ForeignKey("almacen.idalmacen"), nullable=True)
    FechaVenta = Column("fechaventa", DateTime)
    FechaEsperada = Column("fechaesperada", DateTime)
    FechaReal = Column("fechareal", DateTime)
    Estado = Column("estado", String(50), default="Pendiente")
    Activo = Column("activo", Boolean, default=True)
    FechaCreacion = Column("fechacreacion", DateTime)
    FechaModificacion = Column("fechamodificacion", DateTime)

    cliente = relationship("Cliente", back_populates="entregas")
    pedido = relationship("Pedido", back_populates="entregas")
    almacen = relationship("Almacen", back_populates="entregas", foreign_keys=[IdAlmacen])
    detalles = relationship("DetalleEntrega", back_populates="entrega")


class DetalleEntrega(Base):
    __tablename__ = "detalleentrega"

    IdDetalleEntrega = Column("iddetalleentrega", Integer, primary_key=True, index=True)
    IdEntrega = Column("identrega", Integer, ForeignKey("entrega.identrega"), nullable=False)
    IdProducto = Column("idproducto", Integer, ForeignKey("producto.idproducto"), nullable=False)
    CantidadEntregada = Column("cantidadentregada", Integer, default=0)
    PrecioUnitario = Column("preciounitario", Numeric(10, 2), default=0)
    Activo = Column("activo", Boolean, default=True)
    FechaCreacion = Column("fechacreacion", DateTime)
    FechaModificacion = Column("fechamodificacion", DateTime)

    entrega = relationship("Entrega", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_entrega")


class DetalleTransferencia(Base):
    __tablename__ = "detalletransferencia"

    IdDetalleTransferencia = Column("iddetalletransferencia", Integer, primary_key=True, index=True)
    IdTransferencia = Column("idtransferencia", Integer, ForeignKey("transferencia.idtransferencia"), nullable=False)
    IdProducto = Column("idproducto", Integer, ForeignKey("producto.idproducto"), nullable=False)
    CantidadTransferida = Column("cantidadtransferida", Integer, default=0)
    Activo = Column("activo", Boolean, default=True)
    FechaCreacion = Column("fechacreacion", DateTime)
    FechaModificacion = Column("fechamodificacion", DateTime)

    transferencia = relationship("Transferencia", back_populates="detalles")
    producto = relationship("Producto", back_populates="detalles_transferencia")


class Ubicacion(Base):
    __tablename__ = "ubicacion"

    IdUbicacion = Column("idubicacion", Integer, primary_key=True, index=True)
    NombreUbicacion = Column("nombreubicacion", String(200), nullable=False)
    DireccionUbicacion = Column("direccionubicacion", String(300), default="")
    Ciudad = Column("ciudad", String(100), default="")
    Referencia = Column("referencia", String(300), default="")
    TelefonoContacto = Column("telefonocontacto", String(50), default="")
    Activo = Column("activo", Boolean, default=True)
    FechaCreacion = Column("fechacreacion", DateTime)
    FechaModificacion = Column("fechamodificacion", DateTime)

    almacenes = relationship("Almacen", back_populates="ubicacion")


class Almacen(Base):
    __tablename__ = "almacen"

    IdAlmacen = Column("idalmacen", Integer, primary_key=True, index=True)
    IdUbicacion = Column("idubicacion", Integer, ForeignKey("ubicacion.idubicacion"), nullable=False)
    NombreAlmacen = Column("nombrealmacen", String(200), nullable=False)
    EsRefrigerado = Column("esrefrigerado", Boolean, default=False)
    Activo = Column("activo", Boolean, default=True)
    FechaCreacion = Column("fechacreacion", DateTime)
    FechaModificacion = Column("fechamodificacion", DateTime)

    ubicacion = relationship("Ubicacion", back_populates="almacenes")
    inventarios = relationship("Inventario", back_populates="almacen")
    pedidos = relationship("Pedido", back_populates="almacen", foreign_keys="[Pedido.IdAlmacen]")
    entregas = relationship("Entrega", back_populates="almacen", foreign_keys="[Entrega.IdAlmacen]")
    transferencias_origen = relationship(
        "Transferencia",
        back_populates="almacen_origen",
        foreign_keys="Transferencia.IdAlmacenOrigen",
    )
    transferencias_destino = relationship(
        "Transferencia",
        back_populates="almacen_destino",
        foreign_keys="Transferencia.IdAlmacenDestino",
    )


class Inventario(Base):
    __tablename__ = "inventario"

    IdInventario = Column("idinventario", Integer, primary_key=True, index=True)
    IdProducto = Column("idproducto", Integer, ForeignKey("producto.idproducto"), nullable=False)
    IdAlmacen = Column("idalmacen", Integer, ForeignKey("almacen.idalmacen"), nullable=False)
    CantidadDisponible = Column("cantidaddisponible", Integer, default=0)
    StockMinimo = Column("stockminimo", Integer, default=0)
    StockMaximo = Column("stockmaximo", Integer, default=0)
    PuntoReorden = Column("puntoreorden", Integer, default=0)
    Activo = Column("activo", Boolean, default=True)
    FechaCreacion = Column("fechacreacion", DateTime)
    FechaModificacion = Column("fechamodificacion", DateTime)

    producto = relationship("Producto", back_populates="inventarios")
    almacen = relationship("Almacen", back_populates="inventarios")


class Transferencia(Base):
    __tablename__ = "transferencia"

    IdTransferencia = Column("idtransferencia", Integer, primary_key=True, index=True)
    IdAlmacenOrigen = Column("idalmacenorigen", Integer, ForeignKey("almacen.idalmacen"), nullable=False)
    IdAlmacenDestino = Column("idalmacendestino", Integer, ForeignKey("almacen.idalmacen"), nullable=False)
    CantidadTransferida = Column("cantidadtransferida", Integer, default=0)
    FechaEnvio = Column("fechaenvio", DateTime)
    FechaRecepcion = Column("fecharecepcion", DateTime)
    Estado = Column("estado", String(50), default="Pendiente")
    Activo = Column("activo", Boolean, default=True)
    FechaCreacion = Column("fechacreacion", DateTime)
    FechaModificacion = Column("fechamodificacion", DateTime)

    almacen_origen = relationship(
        "Almacen",
        back_populates="transferencias_origen",
        foreign_keys=[IdAlmacenOrigen],
    )
    almacen_destino = relationship(
        "Almacen",
        back_populates="transferencias_destino",
        foreign_keys=[IdAlmacenDestino],
    )
    detalles = relationship("DetalleTransferencia", back_populates="transferencia")
