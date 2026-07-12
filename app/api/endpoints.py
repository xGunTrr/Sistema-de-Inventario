"""Internal API endpoints for products, types, and suppliers."""

import logging
from fastapi import HTTPException
from pydantic import BaseModel
from app.api import store


class ProductIn(BaseModel):
    name: str
    sku: str
    type: str
    supplier: str
    stock: int = 0
    min_stock: int = 0
    price: float = 0.0


class TypeIn(BaseModel):
    name: str
    description: str = ""


class SupplierIn(BaseModel):
    name: str
    contact: str = ""
    email: str = ""
    phone: str = ""


async def list_products():
    with store.get_lock():
        return {"data": list(store.products), "count": len(store.products)}


async def get_product(product_id: int):
    with store.get_lock():
        for p in store.products:
            if p["id"] == product_id:
                return p
    raise HTTPException(status_code=404, detail="Producto no encontrado")


async def create_product(body: ProductIn):
    try:
        with store.get_lock():
            for p in store.products:
                if p["sku"] == body.sku:
                    raise HTTPException(status_code=400, detail="SKU ya existe")
            new_p = body.model_dump()
            new_p["id"] = store.next_id(store.products)
            store.products.append(new_p)
            return new_p
    except HTTPException:
        logging.exception("Unexpected error")
        raise
    except Exception as e:
        logging.exception(f"Error creating product: {e}")
        raise HTTPException(status_code=500, detail="Error interno")


async def update_product(product_id: int, body: ProductIn):
    with store.get_lock():
        for i, p in enumerate(store.products):
            if p["id"] == product_id:
                updated = body.model_dump()
                updated["id"] = product_id
                store.products[i] = updated
                return updated
    raise HTTPException(status_code=404, detail="Producto no encontrado")


async def delete_product(product_id: int):
    with store.get_lock():
        for i, p in enumerate(store.products):
            if p["id"] == product_id:
                store.products.pop(i)
                return {"ok": True, "id": product_id}
    raise HTTPException(status_code=404, detail="Producto no encontrado")


async def list_types():
    with store.get_lock():
        return {
            "data": list(store.product_types),
            "count": len(store.product_types),
        }


async def create_type(body: TypeIn):
    with store.get_lock():
        for t in store.product_types:
            if t["name"].lower() == body.name.lower():
                raise HTTPException(status_code=400, detail="Nombre ya existe")
        new_t = body.model_dump()
        new_t["id"] = store.next_id(store.product_types)
        store.product_types.append(new_t)
        return new_t


async def delete_type(type_id: int):
    with store.get_lock():
        for i, t in enumerate(store.product_types):
            if t["id"] == type_id:
                store.product_types.pop(i)
                return {"ok": True, "id": type_id}
    raise HTTPException(status_code=404, detail="Tipo no encontrado")


async def list_suppliers():
    with store.get_lock():
        return {"data": list(store.suppliers), "count": len(store.suppliers)}


async def create_supplier(body: SupplierIn):
    with store.get_lock():
        for s in store.suppliers:
            if s["name"].lower() == body.name.lower():
                raise HTTPException(
                    status_code=400, detail="Proveedor ya existe"
                )
        new_s = body.model_dump()
        new_s["id"] = store.next_id(store.suppliers)
        store.suppliers.append(new_s)
        return new_s


async def delete_supplier(supplier_id: int):
    with store.get_lock():
        for i, s in enumerate(store.suppliers):
            if s["id"] == supplier_id:
                store.suppliers.pop(i)
                return {"ok": True, "id": supplier_id}
    raise HTTPException(status_code=404, detail="Proveedor no encontrado")


async def api_status():
    with store.get_lock():
        return {
            "status": "ok",
            "products": len(store.products),
            "types": len(store.product_types),
            "suppliers": len(store.suppliers),
        }


from fastapi import FastAPI


def create_api_router() -> FastAPI:
    api_app = FastAPI()
    api_app.add_api_route("/api/status", api_status, methods=["GET"])
    api_app.add_api_route("/api/products", list_products, methods=["GET"])
    api_app.add_api_route(
        "/api/products/{product_id}", get_product, methods=["GET"]
    )
    api_app.add_api_route("/api/products", create_product, methods=["POST"])
    api_app.add_api_route(
        "/api/products/{product_id}", update_product, methods=["PUT"]
    )
    api_app.add_api_route(
        "/api/products/{product_id}", delete_product, methods=["DELETE"]
    )
    api_app.add_api_route("/api/types", list_types, methods=["GET"])
    api_app.add_api_route("/api/types", create_type, methods=["POST"])
    api_app.add_api_route(
        "/api/types/{type_id}", delete_type, methods=["DELETE"]
    )
    api_app.add_api_route("/api/suppliers", list_suppliers, methods=["GET"])
    api_app.add_api_route("/api/suppliers", create_supplier, methods=["POST"])
    api_app.add_api_route(
        "/api/suppliers/{supplier_id}", delete_supplier, methods=["DELETE"]
    )
    return api_app
