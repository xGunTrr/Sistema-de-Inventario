"""Shared in-memory data store for internal API endpoints."""

from threading import Lock


_lock = Lock()

products: list[dict] = [
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
]

product_types: list[dict] = [
    {
        "id": 1,
        "name": "Electrónica",
        "description": "Dispositivos electrónicos",
    },
    {"id": 2, "name": "Mobiliario", "description": "Muebles"},
    {"id": 3, "name": "Papelería", "description": "Suministros de oficina"},
    {"id": 4, "name": "Alimentos", "description": "Comestibles"},
]

suppliers: list[dict] = [
    {
        "id": 1,
        "name": "TechCorp",
        "contact": "Juan Martínez",
        "email": "juan@techcorp.com",
        "phone": "+34 600 111 222",
    },
    {
        "id": 2,
        "name": "OfficeMax",
        "contact": "María López",
        "email": "maria@officemax.com",
        "phone": "+34 600 333 444",
    },
    {
        "id": 3,
        "name": "DisplayCo",
        "contact": "Carlos Ruiz",
        "email": "carlos@displayco.com",
        "phone": "+34 600 555 666",
    },
]


def next_id(items: list[dict]) -> int:
    return max((i["id"] for i in items), default=0) + 1


def get_lock() -> Lock:
    return _lock
