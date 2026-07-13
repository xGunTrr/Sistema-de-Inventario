from fastapi import FastAPI
from fastapi import HTTPException
from fastapi import Depends
from sqlalchemy.orm import joinedload
from sqlalchemy.orm import Session
from sqlalchemy import text

from .dependencies import get_db
from .database import Base, engine
from .models import  Type, Product, Supplier
from .schemas import  TypeIn, ProductIn, SupplierIn

Base.metadata.create_all(bind=engine)

async def list_types(db: Session = Depends(get_db)):
    types = db.query(Type).all()

    return {
        "data": [
            {
                "id": t.id,
                "name": t.name,
                "description": t.description,
                "product_count": len(t.products),
            }
            for t in types
        ],
        "count": len(types),
    }

async def create_type(body: TypeIn, db: Session = Depends(get_db),):
    exists = (
        db.query(Type)
        .filter(Type.name == body.name)
        .first()
    )

    if exists:
        raise HTTPException(400, "Nombre ya existe")

    obj = Type(**body.model_dump())

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj

async def update_type(type_id: int, body: TypeIn, db: Session = Depends(get_db),):
    type = db.get(Type, type_id)

    if type is None:
        raise HTTPException(404, "Producto no encontrado")

    for key, value in body.model_dump().items():
        setattr(type, key, value)

    db.commit()
    db.refresh(type)

    return type

async def delete_type(type_id: int,db: Session = Depends(get_db),):
    obj = db.get(Type, type_id)

    if obj is None:
        raise HTTPException(404, "Tipo no encontrado")

    db.delete(obj)
    db.commit()

    return {
        "ok": True,
        "id": type_id,
    }

async def list_products(db: Session = Depends(get_db),):
    products = (
        db.query(Product)
        .options(
            joinedload(Product.type),
            joinedload(Product.supplier),
        )
        .all()
    )

    return {
        "data": products,
        "count": len(products),
    }

async def get_product(product_id: int,db: Session = Depends(get_db),):
    product = (
        db.query(Product)
        .options(
            joinedload(Product.type),
            joinedload(Product.supplier),
        )
        .filter(Product.id == product_id)
        .first()
    )

    if product is None:
        raise HTTPException(404, "Producto no encontrado")

    return product

async def create_product(body: ProductIn, db: Session = Depends(get_db),):
    sku = (
        db.query(Product)
        .filter(Product.sku == body.sku)
        .first()
    )

    if sku:
        raise HTTPException(400, "SKU ya existe")

    if db.get(Type, body.type_id) is None:
        raise HTTPException(404, "Tipo no encontrado")

    if db.get(Supplier, body.supplier_id) is None:
        raise HTTPException(404, "Proveedor no encontrado")

    product = Product(**body.model_dump())

    db.add(product)
    db.commit()
    db.refresh(product)

    return product

async def update_product(product_id: int, body: ProductIn, db: Session = Depends(get_db),):
    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(404, "Producto no encontrado")

    if db.get(Type, body.type_id) is None:
        raise HTTPException(404, "Tipo no encontrado")

    if db.get(Supplier, body.supplier_id) is None:
        raise HTTPException(404, "Proveedor no encontrado")

    for key, value in body.model_dump().items():
        setattr(product, key, value)

    db.commit()
    db.refresh(product)

    return product

async def delete_product(product_id: int, db: Session = Depends(get_db),):
    product = db.get(Product, product_id)

    if product is None:
        raise HTTPException(404, "Producto no encontrado")

    db.delete(product)
    db.commit()

    return {
        "ok": True,
        "id": product_id,
    }

async def list_suppliers(db: Session = Depends(get_db),):
    suppliers = db.query(Supplier).all()

    return {
        "data": [
            {
                "id": s.id,
                "name": s.name,
                "contact": s.contact,
                "email": s.email,
                "phone": s.phone,
                "product_count": len(s.products),
            }
            for s in suppliers
        ],
        "count": len(suppliers),
    }

async def create_supplier(body: SupplierIn,db: Session = Depends(get_db),):
    exists = (
        db.query(Supplier)
        .filter(Supplier.name == body.name)
        .first()
    )

    if exists:
        raise HTTPException(
            status_code=400,
            detail="Proveedor ya existe",
        )

    supplier = Supplier(**body.model_dump())

    db.add(supplier)
    db.commit()
    db.refresh(supplier)

    return supplier

async def update_supplier(
    supplier_id: int,
    body: SupplierIn,
    db: Session = Depends(get_db),
):
    supplier = db.get(Supplier, supplier_id)

    if supplier is None:
        raise HTTPException(
            status_code=404,
            detail="Proveedor no encontrado",
        )

    for key, value in body.model_dump().items():
        setattr(supplier, key, value)

    db.commit()
    db.refresh(supplier)

    return supplier

async def delete_supplier(supplier_id: int,db: Session = Depends(get_db),):
    supplier = db.get(Supplier, supplier_id)

    if supplier is None:
        raise HTTPException(
            status_code=404,
            detail="Proveedor no encontrado",
        )

    db.delete(supplier)
    db.commit()

    return {
        "ok": True,
        "id": supplier_id,
    }

async def api_status(db: Session = Depends(get_db),):
    try:
        db.execute(text("SELECT 1"))

        return {
            "status": "ok",
            "database": "connected",
        }

    except Exception:
        raise HTTPException(
            status_code=503,
            detail={
                "status": "error",
                "database": "disconnected",
            },
        )

def create_api_router() -> FastAPI:
    api_app = FastAPI()
    api_app.add_api_route("/api/status", api_status, methods=["GET"])

    api_app.add_api_route("/api/products", list_products, methods=["GET"])
    api_app.add_api_route("/api/products/{product_id}", get_product, methods=["GET"])
    api_app.add_api_route("/api/products", create_product, methods=["POST"])
    api_app.add_api_route("/api/products/{product_id}", update_product, methods=["PUT"])
    api_app.add_api_route("/api/products/{product_id}", delete_product, methods=["DELETE"])

    api_app.add_api_route("/api/types", list_types, methods=["GET"])
    api_app.add_api_route("/api/types", create_type, methods=["POST"])
    api_app.add_api_route("/api/types/{type_id}", update_type, methods=["PUT"])
    api_app.add_api_route("/api/types/{type_id}", delete_type, methods=["DELETE"])

    api_app.add_api_route("/api/suppliers", list_suppliers, methods=["GET"])
    api_app.add_api_route("/api/suppliers", create_supplier, methods=["POST"])
    api_app.add_api_route("/api/suppliers/{supplier_id}", update_supplier, methods=["PUT"])
    api_app.add_api_route("/api/suppliers/{supplier_id}", delete_supplier, methods=["DELETE"])

    return api_app
