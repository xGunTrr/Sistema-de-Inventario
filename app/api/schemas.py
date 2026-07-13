from pydantic import BaseModel

class TypeIn(BaseModel):
    name: str
    description: str = ""

class TypeOut(TypeIn):
    id: int

    class Config:
        from_attributes = True

class SupplierIn(BaseModel):
    name: str
    contact: str = ""
    email: str = ""
    phone: str = ""

class SupplierOut(SupplierIn):
    id: int

    class Config:
        from_attributes = True

class ProductIn(BaseModel):
    name: str
    sku: str

    type_id: int
    supplier_id: int

    stock: int = 0
    min_stock: int = 0

    price: float = 0.0

class ProductOut(BaseModel):
    id: int

    name: str
    sku: str

    stock: int
    min_stock: int
    price: float

    type: TypeOut
    supplier: SupplierOut

    class Config:
        from_attributes = True