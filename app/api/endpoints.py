from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from sqlalchemy import text

from .dependencies import get_db
from .models import (
    Proveedor,
    Producto,
    Cliente,
    Pedido,
    DetallePedido,
    Entrega,
    DetalleEntrega,
    Ubicacion,
    Almacen,
    Inventario,
    Transferencia,
    DetalleTransferencia,
)
from .schemas import (
    ProveedorIn,
    ProductoIn,
    ClienteIn,
    PedidoIn,
    PedidoUpdate,
    EntregaIn,
    EntregaUpdate,
    DetallePedidoIn,
    DetallePedidoUpdate,
    DetalleEntregaIn,
    DetalleEntregaUpdate,
    DetalleTransferenciaIn,
    DetalleTransferenciaUpdate,
    TransferenciaIn,
    TransferenciaUpdate,
    UbicacionIn,
    AlmacenIn,
    InventarioIn,
)



def _now():
    return datetime.now(timezone.utc)


# =====================================================================
#  Proveedor
# =====================================================================

async def list_proveedores(db: Session = Depends(get_db)):
    items = db.query(Proveedor).filter(Proveedor.Activo == True).all()
    return {"data": items, "count": len(items)}


async def get_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    obj = db.query(Proveedor).filter(Proveedor.IdProveedor == proveedor_id).first()
    if obj is None:
        raise HTTPException(404, "Proveedor no encontrado")
    return obj


async def create_proveedor(body: ProveedorIn, db: Session = Depends(get_db)):
    now = _now()
    data = body.model_dump()
    data["FechaCreacion"] = now
    data["FechaModificacion"] = now
    obj = Proveedor(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


async def update_proveedor(proveedor_id: int, body: ProveedorIn, db: Session = Depends(get_db)):
    obj = db.query(Proveedor).filter(Proveedor.IdProveedor == proveedor_id).first()
    if obj is None:
        raise HTTPException(404, "Proveedor no encontrado")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    obj.FechaModificacion = _now()
    db.commit()
    db.refresh(obj)
    return obj


async def delete_proveedor(proveedor_id: int, db: Session = Depends(get_db)):
    obj = db.query(Proveedor).filter(Proveedor.IdProveedor == proveedor_id).first()
    if obj is None:
        raise HTTPException(404, "Proveedor no encontrado")
    obj.Activo = False
    obj.FechaModificacion = _now()
    db.commit()
    return {"ok": True, "id": proveedor_id}


# =====================================================================
#  Producto
# =====================================================================

async def list_productos(db: Session = Depends(get_db)):
    items = (
        db.query(Producto)
        .options(joinedload(Producto.proveedor))
        .filter(Producto.Activo == True)
        .all()
    )
    return {"data": items, "count": len(items)}


async def get_producto(producto_id: int, db: Session = Depends(get_db)):
    obj = (
        db.query(Producto)
        .options(joinedload(Producto.proveedor))
        .filter(Producto.IdProducto == producto_id)
        .first()
    )
    if obj is None:
        raise HTTPException(404, "Producto no encontrado")
    return obj


async def create_producto(body: ProductoIn, db: Session = Depends(get_db)):
    if db.query(Proveedor).filter(Proveedor.IdProveedor == body.IdProveedor, Proveedor.Activo == True).first() is None:
        raise HTTPException(404, "Proveedor no encontrado")
    now = _now()
    data = body.model_dump()
    data["FechaCreacion"] = now
    data["FechaModificacion"] = now
    obj = Producto(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


async def update_producto(producto_id: int, body: ProductoIn, db: Session = Depends(get_db)):
    obj = db.query(Producto).filter(Producto.IdProducto == producto_id).first()
    if obj is None:
        raise HTTPException(404, "Producto no encontrado")
    if db.query(Proveedor).filter(Proveedor.IdProveedor == body.IdProveedor, Proveedor.Activo == True).first() is None:
        raise HTTPException(404, "Proveedor no encontrado")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    obj.FechaModificacion = _now()
    db.commit()
    db.refresh(obj)
    return obj


async def delete_producto(producto_id: int, db: Session = Depends(get_db)):
    obj = db.query(Producto).filter(Producto.IdProducto == producto_id).first()
    if obj is None:
        raise HTTPException(404, "Producto no encontrado")
    obj.Activo = False
    obj.FechaModificacion = _now()
    db.commit()
    return {"ok": True, "id": producto_id}


# =====================================================================
#  Cliente
# =====================================================================

async def list_clientes(db: Session = Depends(get_db)):
    items = db.query(Cliente).filter(Cliente.Activo == True).all()
    return {"data": items, "count": len(items)}


async def get_cliente(cliente_id: int, db: Session = Depends(get_db)):
    obj = db.query(Cliente).filter(Cliente.IdCliente == cliente_id).first()
    if obj is None:
        raise HTTPException(404, "Cliente no encontrado")
    return obj


async def create_cliente(body: ClienteIn, db: Session = Depends(get_db)):
    now = _now()
    data = body.model_dump()
    data["FechaCreacion"] = now
    data["FechaModificacion"] = now
    obj = Cliente(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


async def update_cliente(cliente_id: int, body: ClienteIn, db: Session = Depends(get_db)):
    obj = db.query(Cliente).filter(Cliente.IdCliente == cliente_id).first()
    if obj is None:
        raise HTTPException(404, "Cliente no encontrado")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    obj.FechaModificacion = _now()
    db.commit()
    db.refresh(obj)
    return obj


async def delete_cliente(cliente_id: int, db: Session = Depends(get_db)):
    obj = db.query(Cliente).filter(Cliente.IdCliente == cliente_id).first()
    if obj is None:
        raise HTTPException(404, "Cliente no encontrado")
    obj.Activo = False
    obj.FechaModificacion = _now()
    db.commit()
    return {"ok": True, "id": cliente_id}


# =====================================================================
#  Pedido (with DetallePedido)
# =====================================================================

async def list_pedidos(db: Session = Depends(get_db)):
    items = (
        db.query(Pedido)
        .options(
            joinedload(Pedido.proveedor),
            joinedload(Pedido.almacen),
            joinedload(Pedido.detalles).joinedload(DetallePedido.producto),
        )
        .filter(Pedido.Activo == True)
        .all()
    )
    return {"data": items, "count": len(items)}


async def get_pedido(pedido_id: int, db: Session = Depends(get_db)):
    obj = (
        db.query(Pedido)
        .options(
            joinedload(Pedido.proveedor),
            joinedload(Pedido.almacen),
            joinedload(Pedido.detalles).joinedload(DetallePedido.producto),
        )
        .filter(Pedido.IdPedido == pedido_id)
        .first()
    )
    if obj is None:
        raise HTTPException(404, "Pedido no encontrado")
    return obj


async def create_pedido(body: PedidoIn, db: Session = Depends(get_db)):
    if db.query(Proveedor).filter(Proveedor.IdProveedor == body.IdProveedor, Proveedor.Activo == True).first() is None:
        raise HTTPException(404, "Proveedor no encontrado")
    now = _now()
    pedido_data = body.model_dump(exclude={"detalles"})
    pedido_data["FechaCreacion"] = now
    pedido_data["FechaModificacion"] = now
    if pedido_data.get("FechaPedido") is None:
        pedido_data["FechaPedido"] = now
    pedido = Pedido(**pedido_data)
    db.add(pedido)
    db.flush()

    for det in body.detalles:
        if db.query(Producto).filter(Producto.IdProducto == det.IdProducto, Producto.Activo == True).first() is None:
            raise HTTPException(404, f"Producto {det.IdProducto} no encontrado")
        det_data = det.model_dump()
        det_data["IdPedido"] = pedido.IdPedido
        det_data["FechaCreacion"] = now
        det_data["FechaModificacion"] = now
        db.add(DetallePedido(**det_data))

    db.commit()

    pedido = (
        db.query(Pedido)
        .options(
            joinedload(Pedido.proveedor),
            joinedload(Pedido.detalles).joinedload(DetallePedido.producto),
        )
        .filter(Pedido.IdPedido == pedido.IdPedido)
        .first()
    )
    return pedido


async def delete_pedido(pedido_id: int, db: Session = Depends(get_db)):
    obj = db.query(Pedido).filter(Pedido.IdPedido == pedido_id).first()
    if obj is None:
        raise HTTPException(404, "Pedido no encontrado")
    obj.Activo = False
    obj.FechaModificacion = _now()
    for det in db.query(DetallePedido).filter(DetallePedido.IdPedido == pedido_id).all():
        det.Activo = False
        det.FechaModificacion = _now()
    db.commit()
    return {"ok": True, "id": pedido_id}


async def update_pedido(pedido_id: int, body: PedidoUpdate, db: Session = Depends(get_db)):
    obj = db.query(Pedido).filter(Pedido.IdPedido == pedido_id, Pedido.Activo == True).first()
    if obj is None:
        raise HTTPException(404, "Pedido no encontrado")
    updates = body.model_dump(exclude_unset=True, exclude={"detalles_recepcion"})
    if "IdProveedor" in updates and updates["IdProveedor"] is not None:
        if db.query(Proveedor).filter(Proveedor.IdProveedor == updates["IdProveedor"], Proveedor.Activo == True).first() is None:
            raise HTTPException(404, "Proveedor no encontrado")
    if "IdAlmacen" in updates and updates["IdAlmacen"] is not None:
        if db.query(Almacen).filter(Almacen.IdAlmacen == updates["IdAlmacen"], Almacen.Activo == True).first() is None:
            raise HTTPException(404, "Almacen no encontrado")

    nuevo_estado = updates.get("Estado")
    estado_anterior = obj.Estado
    id_almacen = updates.get("IdAlmacen") or obj.IdAlmacen

    for key, value in updates.items():
        setattr(obj, key, value)
    obj.FechaModificacion = _now()

    if nuevo_estado and nuevo_estado != estado_anterior:
        detalles = db.query(DetallePedido).filter(
            DetallePedido.IdPedido == pedido_id, DetallePedido.Activo == True
        ).all()

        if nuevo_estado in ("Entregado", "Parcial"):
            if not id_almacen:
                db.rollback()
                raise HTTPException(400, "Se requiere especificar el almacen de destino (IdAlmacen) para recibir el pedido")

            if nuevo_estado == "Entregado":
                for det in detalles:
                    det.CantidadRecibida = det.Cantidad
            elif nuevo_estado == "Parcial" and body.detalles_recepcion:
                for rec in body.detalles_recepcion:
                    for det in detalles:
                        if det.IdDetallePedido == rec.IdDetallePedido:
                            det.CantidadRecibida = rec.CantidadRecibida
                            break

            for det in detalles:
                if det.CantidadRecibida > 0:
                    inv = db.query(Inventario).filter(
                        Inventario.IdProducto == det.IdProducto,
                        Inventario.IdAlmacen == id_almacen,
                        Inventario.Activo == True,
                    ).first()
                    if inv:
                        inv.CantidadDisponible += det.CantidadRecibida
                        inv.FechaModificacion = _now()
                    else:
                        inv = Inventario(
                            IdProducto=det.IdProducto,
                            IdAlmacen=id_almacen,
                            CantidadDisponible=det.CantidadRecibida,
                            FechaCreacion=_now(),
                            FechaModificacion=_now(),
                        )
                        db.add(inv)
            db.commit()
        else:
            db.commit()
    else:
        db.commit()

    pedido = (
        db.query(Pedido)
        .options(
            joinedload(Pedido.proveedor),
            joinedload(Pedido.almacen),
            joinedload(Pedido.detalles).joinedload(DetallePedido.producto),
        )
        .filter(Pedido.IdPedido == pedido_id)
        .first()
    )
    return pedido


# ---------- DetallePedido CRUD ----------

async def list_detalle_pedido(pedido_id: int, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.IdPedido == pedido_id, Pedido.Activo == True).first()
    if pedido is None:
        raise HTTPException(404, "Pedido no encontrado")
    items = (
        db.query(DetallePedido)
        .options(joinedload(DetallePedido.producto))
        .filter(DetallePedido.IdPedido == pedido_id, DetallePedido.Activo == True)
        .all()
    )
    return {"data": items, "count": len(items)}


async def get_detalle_pedido(pedido_id: int, detalle_id: int, db: Session = Depends(get_db)):
    obj = (
        db.query(DetallePedido)
        .options(joinedload(DetallePedido.producto))
        .filter(DetallePedido.IdDetallePedido == detalle_id, DetallePedido.IdPedido == pedido_id, DetallePedido.Activo == True)
        .first()
    )
    if obj is None:
        raise HTTPException(404, "Detalle no encontrado")
    return obj


async def create_detalle_pedido(pedido_id: int, body: DetallePedidoIn, db: Session = Depends(get_db)):
    pedido = db.query(Pedido).filter(Pedido.IdPedido == pedido_id, Pedido.Activo == True).first()
    if pedido is None:
        raise HTTPException(404, "Pedido no encontrado")
    if db.query(Producto).filter(Producto.IdProducto == body.IdProducto, Producto.Activo == True).first() is None:
        raise HTTPException(404, "Producto no encontrado")
    now = _now()
    data = body.model_dump()
    data["IdPedido"] = pedido_id
    data["FechaCreacion"] = now
    data["FechaModificacion"] = now
    obj = DetallePedido(**data)
    db.add(obj)
    db.commit()

    obj = (
        db.query(DetallePedido)
        .options(joinedload(DetallePedido.producto))
        .filter(DetallePedido.IdDetallePedido == obj.IdDetallePedido)
        .first()
    )
    return obj


async def update_detalle_pedido(pedido_id: int, detalle_id: int, body: DetallePedidoUpdate, db: Session = Depends(get_db)):
    obj = db.query(DetallePedido).filter(
        DetallePedido.IdDetallePedido == detalle_id,
        DetallePedido.IdPedido == pedido_id,
        DetallePedido.Activo == True,
    ).first()
    if obj is None:
        raise HTTPException(404, "Detalle no encontrado")
    updates = body.model_dump(exclude_unset=True)
    if "IdProducto" in updates and updates["IdProducto"] is not None:
        if db.query(Producto).filter(Producto.IdProducto == updates["IdProducto"], Producto.Activo == True).first() is None:
            raise HTTPException(404, "Producto no encontrado")
    for key, value in updates.items():
        setattr(obj, key, value)
    obj.FechaModificacion = _now()
    db.commit()

    obj = (
        db.query(DetallePedido)
        .options(joinedload(DetallePedido.producto))
        .filter(DetallePedido.IdDetallePedido == detalle_id)
        .first()
    )
    return obj


async def delete_detalle_pedido(pedido_id: int, detalle_id: int, db: Session = Depends(get_db)):
    obj = db.query(DetallePedido).filter(
        DetallePedido.IdDetallePedido == detalle_id,
        DetallePedido.IdPedido == pedido_id,
    ).first()
    if obj is None:
        raise HTTPException(404, "Detalle no encontrado")
    obj.Activo = False
    obj.FechaModificacion = _now()
    db.commit()
    return {"ok": True, "id": detalle_id}


# =====================================================================
#  Entrega (with DetalleEntrega)
# =====================================================================

async def list_entregas(db: Session = Depends(get_db)):
    items = (
        db.query(Entrega)
        .options(
            joinedload(Entrega.cliente),
            joinedload(Entrega.pedido),
            joinedload(Entrega.almacen),
            joinedload(Entrega.detalles).joinedload(DetalleEntrega.producto),
        )
        .filter(Entrega.Activo == True)
        .all()
    )
    return {"data": items, "count": len(items)}


async def get_entrega(entrega_id: int, db: Session = Depends(get_db)):
    obj = (
        db.query(Entrega)
        .options(
            joinedload(Entrega.cliente),
            joinedload(Entrega.pedido),
            joinedload(Entrega.almacen),
            joinedload(Entrega.detalles).joinedload(DetalleEntrega.producto),
        )
        .filter(Entrega.IdEntrega == entrega_id)
        .first()
    )
    if obj is None:
        raise HTTPException(404, "Entrega no encontrada")
    return obj


async def create_entrega(body: EntregaIn, db: Session = Depends(get_db)):
    if db.query(Cliente).filter(Cliente.IdCliente == body.IdCliente, Cliente.Activo == True).first() is None:
        raise HTTPException(404, "Cliente no encontrado")
    if db.query(Pedido).filter(Pedido.IdPedido == body.IdPedido, Pedido.Activo == True).first() is None:
        raise HTTPException(404, "Pedido no encontrado")
    now = _now()
    entrega_data = body.model_dump(exclude={"detalles"})
    entrega_data["FechaCreacion"] = now
    entrega_data["FechaModificacion"] = now
    entrega = Entrega(**entrega_data)
    db.add(entrega)
    db.flush()

    for det in body.detalles:
        if db.query(Producto).filter(Producto.IdProducto == det.IdProducto, Producto.Activo == True).first() is None:
            raise HTTPException(404, f"Producto {det.IdProducto} no encontrado")
        det_data = det.model_dump()
        det_data["IdEntrega"] = entrega.IdEntrega
        det_data["FechaCreacion"] = now
        det_data["FechaModificacion"] = now
        db.add(DetalleEntrega(**det_data))

    db.commit()

    entrega = (
        db.query(Entrega)
        .options(
            joinedload(Entrega.cliente),
            joinedload(Entrega.pedido),
            joinedload(Entrega.detalles).joinedload(DetalleEntrega.producto),
        )
        .filter(Entrega.IdEntrega == entrega.IdEntrega)
        .first()
    )
    return entrega


async def delete_entrega(entrega_id: int, db: Session = Depends(get_db)):
    obj = db.query(Entrega).filter(Entrega.IdEntrega == entrega_id).first()
    if obj is None:
        raise HTTPException(404, "Entrega no encontrada")
    obj.Activo = False
    obj.FechaModificacion = _now()
    for det in db.query(DetalleEntrega).filter(DetalleEntrega.IdEntrega == entrega_id).all():
        det.Activo = False
        det.FechaModificacion = _now()
    db.commit()
    return {"ok": True, "id": entrega_id}


async def update_entrega(entrega_id: int, body: EntregaUpdate, db: Session = Depends(get_db)):
    obj = db.query(Entrega).filter(Entrega.IdEntrega == entrega_id, Entrega.Activo == True).first()
    if obj is None:
        raise HTTPException(404, "Entrega no encontrada")
    updates = body.model_dump(exclude_unset=True)
    if "IdCliente" in updates and updates["IdCliente"] is not None:
        if db.query(Cliente).filter(Cliente.IdCliente == updates["IdCliente"], Cliente.Activo == True).first() is None:
            raise HTTPException(404, "Cliente no encontrado")
    if "IdPedido" in updates and updates["IdPedido"] is not None:
        if db.query(Pedido).filter(Pedido.IdPedido == updates["IdPedido"], Pedido.Activo == True).first() is None:
            raise HTTPException(404, "Pedido no encontrado")
    if "IdAlmacen" in updates and updates["IdAlmacen"] is not None:
        if db.query(Almacen).filter(Almacen.IdAlmacen == updates["IdAlmacen"], Almacen.Activo == True).first() is None:
            raise HTTPException(404, "Almacen no encontrado")

    nuevo_estado = updates.get("Estado")
    estado_anterior = obj.Estado
    id_almacen = updates.get("IdAlmacen") or obj.IdAlmacen

    for key, value in updates.items():
        setattr(obj, key, value)
    obj.FechaModificacion = _now()

    if nuevo_estado and nuevo_estado != estado_anterior:
        detalles = db.query(DetalleEntrega).filter(
            DetalleEntrega.IdEntrega == entrega_id, DetalleEntrega.Activo == True
        ).all()

        if nuevo_estado == "En transito":
            if not id_almacen:
                db.rollback()
                raise HTTPException(400, "Se requiere especificar el almacen de origen (IdAlmacen) para despachar la entrega")
            for det in detalles:
                if det.CantidadEntregada > 0:
                    inv = db.query(Inventario).filter(
                        Inventario.IdProducto == det.IdProducto,
                        Inventario.IdAlmacen == id_almacen,
                        Inventario.Activo == True,
                    ).first()
                    if inv:
                        if inv.CantidadDisponible < det.CantidadEntregada:
                            db.rollback()
                            raise HTTPException(400, f"Stock insuficiente para {det.IdProducto}: disponible {inv.CantidadDisponible}, requerido {det.CantidadEntregada}")
                        inv.CantidadDisponible -= det.CantidadEntregada
                        inv.FechaModificacion = _now()
                    else:
                        db.rollback()
                        raise HTTPException(400, f"No existe registro de inventario para el producto {det.IdProducto} en el almacen {id_almacen}")

        elif nuevo_estado == "No entregado":
            if id_almacen:
                for det in detalles:
                    if det.CantidadEntregada > 0:
                        inv = db.query(Inventario).filter(
                            Inventario.IdProducto == det.IdProducto,
                            Inventario.IdAlmacen == id_almacen,
                            Inventario.Activo == True,
                        ).first()
                        if inv:
                            inv.CantidadDisponible += det.CantidadEntregada
                            inv.FechaModificacion = _now()

        db.commit()
    else:
        db.commit()

    entrega = (
        db.query(Entrega)
        .options(
            joinedload(Entrega.cliente),
            joinedload(Entrega.pedido),
            joinedload(Entrega.almacen),
            joinedload(Entrega.detalles).joinedload(DetalleEntrega.producto),
        )
        .filter(Entrega.IdEntrega == entrega_id)
        .first()
    )
    return entrega


# ---------- DetalleEntrega CRUD ----------

async def list_detalle_entrega(entrega_id: int, db: Session = Depends(get_db)):
    entrega = db.query(Entrega).filter(Entrega.IdEntrega == entrega_id, Entrega.Activo == True).first()
    if entrega is None:
        raise HTTPException(404, "Entrega no encontrada")
    items = (
        db.query(DetalleEntrega)
        .options(joinedload(DetalleEntrega.producto))
        .filter(DetalleEntrega.IdEntrega == entrega_id, DetalleEntrega.Activo == True)
        .all()
    )
    return {"data": items, "count": len(items)}


async def get_detalle_entrega(entrega_id: int, detalle_id: int, db: Session = Depends(get_db)):
    obj = (
        db.query(DetalleEntrega)
        .options(joinedload(DetalleEntrega.producto))
        .filter(DetalleEntrega.IdDetalleEntrega == detalle_id, DetalleEntrega.IdEntrega == entrega_id, DetalleEntrega.Activo == True)
        .first()
    )
    if obj is None:
        raise HTTPException(404, "Detalle no encontrado")
    return obj


async def create_detalle_entrega(entrega_id: int, body: DetalleEntregaIn, db: Session = Depends(get_db)):
    entrega = db.query(Entrega).filter(Entrega.IdEntrega == entrega_id, Entrega.Activo == True).first()
    if entrega is None:
        raise HTTPException(404, "Entrega no encontrada")
    if db.query(Producto).filter(Producto.IdProducto == body.IdProducto, Producto.Activo == True).first() is None:
        raise HTTPException(404, "Producto no encontrado")
    now = _now()
    data = body.model_dump()
    data["IdEntrega"] = entrega_id
    data["FechaCreacion"] = now
    data["FechaModificacion"] = now
    obj = DetalleEntrega(**data)
    db.add(obj)
    db.commit()

    obj = (
        db.query(DetalleEntrega)
        .options(joinedload(DetalleEntrega.producto))
        .filter(DetalleEntrega.IdDetalleEntrega == obj.IdDetalleEntrega)
        .first()
    )
    return obj


async def update_detalle_entrega(entrega_id: int, detalle_id: int, body: DetalleEntregaUpdate, db: Session = Depends(get_db)):
    obj = db.query(DetalleEntrega).filter(
        DetalleEntrega.IdDetalleEntrega == detalle_id,
        DetalleEntrega.IdEntrega == entrega_id,
        DetalleEntrega.Activo == True,
    ).first()
    if obj is None:
        raise HTTPException(404, "Detalle no encontrado")
    updates = body.model_dump(exclude_unset=True)
    if "IdProducto" in updates and updates["IdProducto"] is not None:
        if db.query(Producto).filter(Producto.IdProducto == updates["IdProducto"], Producto.Activo == True).first() is None:
            raise HTTPException(404, "Producto no encontrado")
    for key, value in updates.items():
        setattr(obj, key, value)
    obj.FechaModificacion = _now()
    db.commit()

    obj = (
        db.query(DetalleEntrega)
        .options(joinedload(DetalleEntrega.producto))
        .filter(DetalleEntrega.IdDetalleEntrega == detalle_id)
        .first()
    )
    return obj


async def delete_detalle_entrega(entrega_id: int, detalle_id: int, db: Session = Depends(get_db)):
    obj = db.query(DetalleEntrega).filter(
        DetalleEntrega.IdDetalleEntrega == detalle_id,
        DetalleEntrega.IdEntrega == entrega_id,
    ).first()
    if obj is None:
        raise HTTPException(404, "Detalle no encontrado")
    obj.Activo = False
    obj.FechaModificacion = _now()
    db.commit()
    return {"ok": True, "id": detalle_id}


# =====================================================================
#  Ubicacion
# =====================================================================

async def list_ubicaciones(db: Session = Depends(get_db)):
    items = db.query(Ubicacion).filter(Ubicacion.Activo == True).all()
    return {"data": items, "count": len(items)}


async def get_ubicacion(ubicacion_id: int, db: Session = Depends(get_db)):
    obj = db.query(Ubicacion).filter(Ubicacion.IdUbicacion == ubicacion_id).first()
    if obj is None:
        raise HTTPException(404, "Ubicacion no encontrada")
    return obj


async def create_ubicacion(body: UbicacionIn, db: Session = Depends(get_db)):
    now = _now()
    data = body.model_dump()
    data["FechaCreacion"] = now
    data["FechaModificacion"] = now
    obj = Ubicacion(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


async def update_ubicacion(ubicacion_id: int, body: UbicacionIn, db: Session = Depends(get_db)):
    obj = db.query(Ubicacion).filter(Ubicacion.IdUbicacion == ubicacion_id).first()
    if obj is None:
        raise HTTPException(404, "Ubicacion no encontrada")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    obj.FechaModificacion = _now()
    db.commit()
    db.refresh(obj)
    return obj


async def delete_ubicacion(ubicacion_id: int, db: Session = Depends(get_db)):
    obj = db.query(Ubicacion).filter(Ubicacion.IdUbicacion == ubicacion_id).first()
    if obj is None:
        raise HTTPException(404, "Ubicacion no encontrada")
    obj.Activo = False
    obj.FechaModificacion = _now()
    db.commit()
    return {"ok": True, "id": ubicacion_id}


# =====================================================================
#  Almacen
# =====================================================================

async def list_almacenes(db: Session = Depends(get_db)):
    items = (
        db.query(Almacen)
        .options(joinedload(Almacen.ubicacion))
        .filter(Almacen.Activo == True)
        .all()
    )
    return {"data": items, "count": len(items)}


async def get_almacen(almacen_id: int, db: Session = Depends(get_db)):
    obj = (
        db.query(Almacen)
        .options(joinedload(Almacen.ubicacion))
        .filter(Almacen.IdAlmacen == almacen_id)
        .first()
    )
    if obj is None:
        raise HTTPException(404, "Almacen no encontrado")
    return obj


async def create_almacen(body: AlmacenIn, db: Session = Depends(get_db)):
    if db.query(Ubicacion).filter(Ubicacion.IdUbicacion == body.IdUbicacion, Ubicacion.Activo == True).first() is None:
        raise HTTPException(404, "Ubicacion no encontrada")
    now = _now()
    data = body.model_dump()
    data["FechaCreacion"] = now
    data["FechaModificacion"] = now
    obj = Almacen(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


async def update_almacen(almacen_id: int, body: AlmacenIn, db: Session = Depends(get_db)):
    obj = db.query(Almacen).filter(Almacen.IdAlmacen == almacen_id).first()
    if obj is None:
        raise HTTPException(404, "Almacen no encontrado")
    if db.query(Ubicacion).filter(Ubicacion.IdUbicacion == body.IdUbicacion, Ubicacion.Activo == True).first() is None:
        raise HTTPException(404, "Ubicacion no encontrada")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    obj.FechaModificacion = _now()
    db.commit()
    db.refresh(obj)
    return obj


async def delete_almacen(almacen_id: int, db: Session = Depends(get_db)):
    obj = db.query(Almacen).filter(Almacen.IdAlmacen == almacen_id).first()
    if obj is None:
        raise HTTPException(404, "Almacen no encontrado")
    obj.Activo = False
    obj.FechaModificacion = _now()
    db.commit()
    return {"ok": True, "id": almacen_id}


# =====================================================================
#  Inventario
# =====================================================================

async def list_inventarios(db: Session = Depends(get_db)):
    items = (
        db.query(Inventario)
        .options(
            joinedload(Inventario.producto),
            joinedload(Inventario.almacen),
        )
        .filter(Inventario.Activo == True)
        .all()
    )
    return {"data": items, "count": len(items)}


async def get_inventario(inventario_id: int, db: Session = Depends(get_db)):
    obj = (
        db.query(Inventario)
        .options(
            joinedload(Inventario.producto),
            joinedload(Inventario.almacen),
        )
        .filter(Inventario.IdInventario == inventario_id)
        .first()
    )
    if obj is None:
        raise HTTPException(404, "Inventario no encontrado")
    return obj


async def create_inventario(body: InventarioIn, db: Session = Depends(get_db)):
    if db.query(Producto).filter(Producto.IdProducto == body.IdProducto, Producto.Activo == True).first() is None:
        raise HTTPException(404, "Producto no encontrado")
    if db.query(Almacen).filter(Almacen.IdAlmacen == body.IdAlmacen, Almacen.Activo == True).first() is None:
        raise HTTPException(404, "Almacen no encontrado")
    now = _now()
    data = body.model_dump()
    data["FechaCreacion"] = now
    data["FechaModificacion"] = now
    obj = Inventario(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


async def update_inventario(inventario_id: int, body: InventarioIn, db: Session = Depends(get_db)):
    obj = db.query(Inventario).filter(Inventario.IdInventario == inventario_id).first()
    if obj is None:
        raise HTTPException(404, "Inventario no encontrado")
    if db.query(Producto).filter(Producto.IdProducto == body.IdProducto, Producto.Activo == True).first() is None:
        raise HTTPException(404, "Producto no encontrado")
    if db.query(Almacen).filter(Almacen.IdAlmacen == body.IdAlmacen, Almacen.Activo == True).first() is None:
        raise HTTPException(404, "Almacen no encontrado")
    for key, value in body.model_dump(exclude_unset=True).items():
        setattr(obj, key, value)
    obj.FechaModificacion = _now()
    db.commit()
    db.refresh(obj)
    return obj


async def delete_inventario(inventario_id: int, db: Session = Depends(get_db)):
    obj = db.query(Inventario).filter(Inventario.IdInventario == inventario_id).first()
    if obj is None:
        raise HTTPException(404, "Inventario no encontrado")
    obj.Activo = False
    obj.FechaModificacion = _now()
    db.commit()
    return {"ok": True, "id": inventario_id}


# =====================================================================
#  Transferencia
# =====================================================================

async def list_transferencias(db: Session = Depends(get_db)):
    items = (
        db.query(Transferencia)
        .options(
            joinedload(Transferencia.almacen_origen),
            joinedload(Transferencia.almacen_destino),
            joinedload(Transferencia.detalles).joinedload(DetalleTransferencia.producto),
        )
        .filter(Transferencia.Activo == True)
        .all()
    )
    return {"data": items, "count": len(items)}


async def get_transferencia(transferencia_id: int, db: Session = Depends(get_db)):
    obj = (
        db.query(Transferencia)
        .options(
            joinedload(Transferencia.almacen_origen),
            joinedload(Transferencia.almacen_destino),
            joinedload(Transferencia.detalles).joinedload(DetalleTransferencia.producto),
        )
        .filter(Transferencia.IdTransferencia == transferencia_id)
        .first()
    )
    if obj is None:
        raise HTTPException(404, "Transferencia no encontrada")
    return obj


async def create_transferencia(body: TransferenciaIn, db: Session = Depends(get_db)):
    if body.IdAlmacenOrigen == body.IdAlmacenDestino:
        raise HTTPException(400, "El almacen de origen y destino no pueden ser el mismo")
    if db.query(Almacen).filter(Almacen.IdAlmacen == body.IdAlmacenOrigen, Almacen.Activo == True).first() is None:
        raise HTTPException(404, "Almacen de origen no encontrado")
    if db.query(Almacen).filter(Almacen.IdAlmacen == body.IdAlmacenDestino, Almacen.Activo == True).first() is None:
        raise HTTPException(404, "Almacen de destino no encontrado")
    now = _now()
    data = body.model_dump(exclude={"detalles"})
    data["FechaCreacion"] = now
    data["FechaModificacion"] = now
    obj = Transferencia(**data)
    db.add(obj)
    db.flush()

    for det in body.detalles:
        if db.query(Producto).filter(Producto.IdProducto == det.IdProducto, Producto.Activo == True).first() is None:
            raise HTTPException(404, f"Producto {det.IdProducto} no encontrado")
        det_data = det.model_dump()
        det_data["IdTransferencia"] = obj.IdTransferencia
        det_data["FechaCreacion"] = now
        det_data["FechaModificacion"] = now
        db.add(DetalleTransferencia(**det_data))

    db.commit()

    obj = (
        db.query(Transferencia)
        .options(
            joinedload(Transferencia.almacen_origen),
            joinedload(Transferencia.almacen_destino),
            joinedload(Transferencia.detalles).joinedload(DetalleTransferencia.producto),
        )
        .filter(Transferencia.IdTransferencia == obj.IdTransferencia)
        .first()
    )
    return obj


async def update_transferencia(transferencia_id: int, body: TransferenciaUpdate, db: Session = Depends(get_db)):
    obj = db.query(Transferencia).filter(Transferencia.IdTransferencia == transferencia_id, Transferencia.Activo == True).first()
    if obj is None:
        raise HTTPException(404, "Transferencia no encontrada")
    updates = body.model_dump(exclude_unset=True)
    if "IdAlmacenOrigen" in updates and updates["IdAlmacenOrigen"] is not None:
        if db.query(Almacen).filter(Almacen.IdAlmacen == updates["IdAlmacenOrigen"], Almacen.Activo == True).first() is None:
            raise HTTPException(404, "Almacen de origen no encontrado")
    if "IdAlmacenDestino" in updates and updates["IdAlmacenDestino"] is not None:
        if db.query(Almacen).filter(Almacen.IdAlmacen == updates["IdAlmacenDestino"], Almacen.Activo == True).first() is None:
            raise HTTPException(404, "Almacen de destino no encontrado")

    nuevo_estado = updates.get("Estado")
    estado_anterior = obj.Estado

    for key, value in updates.items():
        setattr(obj, key, value)
    obj.FechaModificacion = _now()

    if nuevo_estado and nuevo_estado != estado_anterior and nuevo_estado == "Completada":
        id_origen = obj.IdAlmacenOrigen
        id_destino = obj.IdAlmacenDestino
        detalles = db.query(DetalleTransferencia).filter(
            DetalleTransferencia.IdTransferencia == transferencia_id,
            DetalleTransferencia.Activo == True,
        ).all()
        for det in detalles:
            if det.CantidadTransferida > 0:
                inv_origen = db.query(Inventario).filter(
                    Inventario.IdProducto == det.IdProducto,
                    Inventario.IdAlmacen == id_origen,
                    Inventario.Activo == True,
                ).first()
                if inv_origen:
                    if inv_origen.CantidadDisponible < det.CantidadTransferida:
                        db.rollback()
                        raise HTTPException(400, f"Stock insuficiente en origen para producto {det.IdProducto}: disponible {inv_origen.CantidadDisponible}, requerido {det.CantidadTransferida}")
                    inv_origen.CantidadDisponible -= det.CantidadTransferida
                    inv_origen.FechaModificacion = _now()

                inv_destino = db.query(Inventario).filter(
                    Inventario.IdProducto == det.IdProducto,
                    Inventario.IdAlmacen == id_destino,
                    Inventario.Activo == True,
                ).first()
                if inv_destino:
                    inv_destino.CantidadDisponible += det.CantidadTransferida
                    inv_destino.FechaModificacion = _now()
                else:
                    inv_destino = Inventario(
                        IdProducto=det.IdProducto,
                        IdAlmacen=id_destino,
                        CantidadDisponible=det.CantidadTransferida,
                        FechaCreacion=_now(),
                        FechaModificacion=_now(),
                    )
                    db.add(inv_destino)
        db.commit()
    else:
        db.commit()

    transferencia = (
        db.query(Transferencia)
        .options(
            joinedload(Transferencia.almacen_origen),
            joinedload(Transferencia.almacen_destino),
            joinedload(Transferencia.detalles).joinedload(DetalleTransferencia.producto),
        )
        .filter(Transferencia.IdTransferencia == transferencia_id)
        .first()
    )
    return transferencia


async def delete_transferencia(transferencia_id: int, db: Session = Depends(get_db)):
    obj = db.query(Transferencia).filter(Transferencia.IdTransferencia == transferencia_id).first()
    if obj is None:
        raise HTTPException(404, "Transferencia no encontrada")
    obj.Activo = False
    obj.FechaModificacion = _now()
    for det in db.query(DetalleTransferencia).filter(DetalleTransferencia.IdTransferencia == transferencia_id).all():
        det.Activo = False
        det.FechaModificacion = _now()
    db.commit()
    return {"ok": True, "id": transferencia_id}


# ---------- DetalleTransferencia CRUD ----------

async def list_detalle_transferencia(transferencia_id: int, db: Session = Depends(get_db)):
    transferencia = db.query(Transferencia).filter(Transferencia.IdTransferencia == transferencia_id, Transferencia.Activo == True).first()
    if transferencia is None:
        raise HTTPException(404, "Transferencia no encontrada")
    items = (
        db.query(DetalleTransferencia)
        .options(joinedload(DetalleTransferencia.producto))
        .filter(DetalleTransferencia.IdTransferencia == transferencia_id, DetalleTransferencia.Activo == True)
        .all()
    )
    return {"data": items, "count": len(items)}


async def create_detalle_transferencia(transferencia_id: int, body: DetalleTransferenciaIn, db: Session = Depends(get_db)):
    transferencia = db.query(Transferencia).filter(Transferencia.IdTransferencia == transferencia_id, Transferencia.Activo == True).first()
    if transferencia is None:
        raise HTTPException(404, "Transferencia no encontrada")
    if db.query(Producto).filter(Producto.IdProducto == body.IdProducto, Producto.Activo == True).first() is None:
        raise HTTPException(404, "Producto no encontrado")
    now = _now()
    data = body.model_dump()
    data["IdTransferencia"] = transferencia_id
    data["FechaCreacion"] = now
    data["FechaModificacion"] = now
    obj = DetalleTransferencia(**data)
    db.add(obj)
    db.commit()

    obj = (
        db.query(DetalleTransferencia)
        .options(joinedload(DetalleTransferencia.producto))
        .filter(DetalleTransferencia.IdDetalleTransferencia == obj.IdDetalleTransferencia)
        .first()
    )
    return obj


async def delete_detalle_transferencia(transferencia_id: int, detalle_id: int, db: Session = Depends(get_db)):
    obj = db.query(DetalleTransferencia).filter(
        DetalleTransferencia.IdDetalleTransferencia == detalle_id,
        DetalleTransferencia.IdTransferencia == transferencia_id,
    ).first()
    if obj is None:
        raise HTTPException(404, "Detalle no encontrado")
    obj.Activo = False
    obj.FechaModificacion = _now()
    db.commit()
    return {"ok": True, "id": detalle_id}


# =====================================================================
#  Health / status
# =====================================================================

async def api_status(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok", "database": "connected"}
    except Exception:
        raise HTTPException(
            status_code=503,
            detail={"status": "error", "database": "disconnected"},
        )


# =====================================================================
#  Router
# =====================================================================

def create_api_router() -> FastAPI:
    api_app = FastAPI()

    api_app.add_api_route("/api/status", api_status, methods=["GET"])

    # Proveedor
    api_app.add_api_route("/api/proveedores", list_proveedores, methods=["GET"])
    api_app.add_api_route("/api/proveedores/{proveedor_id}", get_proveedor, methods=["GET"])
    api_app.add_api_route("/api/proveedores", create_proveedor, methods=["POST"])
    api_app.add_api_route("/api/proveedores/{proveedor_id}", update_proveedor, methods=["PUT"])
    api_app.add_api_route("/api/proveedores/{proveedor_id}", delete_proveedor, methods=["DELETE"])

    # Producto
    api_app.add_api_route("/api/productos", list_productos, methods=["GET"])
    api_app.add_api_route("/api/productos/{producto_id}", get_producto, methods=["GET"])
    api_app.add_api_route("/api/productos", create_producto, methods=["POST"])
    api_app.add_api_route("/api/productos/{producto_id}", update_producto, methods=["PUT"])
    api_app.add_api_route("/api/productos/{producto_id}", delete_producto, methods=["DELETE"])

    # Cliente
    api_app.add_api_route("/api/clientes", list_clientes, methods=["GET"])
    api_app.add_api_route("/api/clientes/{cliente_id}", get_cliente, methods=["GET"])
    api_app.add_api_route("/api/clientes", create_cliente, methods=["POST"])
    api_app.add_api_route("/api/clientes/{cliente_id}", update_cliente, methods=["PUT"])
    api_app.add_api_route("/api/clientes/{cliente_id}", delete_cliente, methods=["DELETE"])

    # Pedido
    api_app.add_api_route("/api/pedidos", list_pedidos, methods=["GET"])
    api_app.add_api_route("/api/pedidos/{pedido_id}", get_pedido, methods=["GET"])
    api_app.add_api_route("/api/pedidos", create_pedido, methods=["POST"])
    api_app.add_api_route("/api/pedidos/{pedido_id}", update_pedido, methods=["PUT"])
    api_app.add_api_route("/api/pedidos/{pedido_id}", delete_pedido, methods=["DELETE"])

    # DetallePedido
    api_app.add_api_route("/api/pedidos/{pedido_id}/detalles", list_detalle_pedido, methods=["GET"])
    api_app.add_api_route("/api/pedidos/{pedido_id}/detalles/{detalle_id}", get_detalle_pedido, methods=["GET"])
    api_app.add_api_route("/api/pedidos/{pedido_id}/detalles", create_detalle_pedido, methods=["POST"])
    api_app.add_api_route("/api/pedidos/{pedido_id}/detalles/{detalle_id}", update_detalle_pedido, methods=["PUT"])
    api_app.add_api_route("/api/pedidos/{pedido_id}/detalles/{detalle_id}", delete_detalle_pedido, methods=["DELETE"])

    # Entrega
    api_app.add_api_route("/api/entregas", list_entregas, methods=["GET"])
    api_app.add_api_route("/api/entregas/{entrega_id}", get_entrega, methods=["GET"])
    api_app.add_api_route("/api/entregas", create_entrega, methods=["POST"])
    api_app.add_api_route("/api/entregas/{entrega_id}", update_entrega, methods=["PUT"])
    api_app.add_api_route("/api/entregas/{entrega_id}", delete_entrega, methods=["DELETE"])

    # DetalleEntrega
    api_app.add_api_route("/api/entregas/{entrega_id}/detalles", list_detalle_entrega, methods=["GET"])
    api_app.add_api_route("/api/entregas/{entrega_id}/detalles/{detalle_id}", get_detalle_entrega, methods=["GET"])
    api_app.add_api_route("/api/entregas/{entrega_id}/detalles", create_detalle_entrega, methods=["POST"])
    api_app.add_api_route("/api/entregas/{entrega_id}/detalles/{detalle_id}", update_detalle_entrega, methods=["PUT"])
    api_app.add_api_route("/api/entregas/{entrega_id}/detalles/{detalle_id}", delete_detalle_entrega, methods=["DELETE"])

    # Ubicacion
    api_app.add_api_route("/api/ubicaciones", list_ubicaciones, methods=["GET"])
    api_app.add_api_route("/api/ubicaciones/{ubicacion_id}", get_ubicacion, methods=["GET"])
    api_app.add_api_route("/api/ubicaciones", create_ubicacion, methods=["POST"])
    api_app.add_api_route("/api/ubicaciones/{ubicacion_id}", update_ubicacion, methods=["PUT"])
    api_app.add_api_route("/api/ubicaciones/{ubicacion_id}", delete_ubicacion, methods=["DELETE"])

    # Almacen
    api_app.add_api_route("/api/almacenes", list_almacenes, methods=["GET"])
    api_app.add_api_route("/api/almacenes/{almacen_id}", get_almacen, methods=["GET"])
    api_app.add_api_route("/api/almacenes", create_almacen, methods=["POST"])
    api_app.add_api_route("/api/almacenes/{almacen_id}", update_almacen, methods=["PUT"])
    api_app.add_api_route("/api/almacenes/{almacen_id}", delete_almacen, methods=["DELETE"])

    # Inventario
    api_app.add_api_route("/api/inventarios", list_inventarios, methods=["GET"])
    api_app.add_api_route("/api/inventarios/{inventario_id}", get_inventario, methods=["GET"])
    api_app.add_api_route("/api/inventarios", create_inventario, methods=["POST"])
    api_app.add_api_route("/api/inventarios/{inventario_id}", update_inventario, methods=["PUT"])
    api_app.add_api_route("/api/inventarios/{inventario_id}", delete_inventario, methods=["DELETE"])

    # Transferencia
    api_app.add_api_route("/api/transferencias", list_transferencias, methods=["GET"])
    api_app.add_api_route("/api/transferencias/{transferencia_id}", get_transferencia, methods=["GET"])
    api_app.add_api_route("/api/transferencias", create_transferencia, methods=["POST"])
    api_app.add_api_route("/api/transferencias/{transferencia_id}", update_transferencia, methods=["PUT"])
    api_app.add_api_route("/api/transferencias/{transferencia_id}", delete_transferencia, methods=["DELETE"])

    # DetalleTransferencia
    api_app.add_api_route("/api/transferencias/{transferencia_id}/detalles", list_detalle_transferencia, methods=["GET"])
    api_app.add_api_route("/api/transferencias/{transferencia_id}/detalles", create_detalle_transferencia, methods=["POST"])
    api_app.add_api_route("/api/transferencias/{transferencia_id}/detalles/{detalle_id}", delete_detalle_transferencia, methods=["DELETE"])

    return api_app
