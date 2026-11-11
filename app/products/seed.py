from datetime import datetime
from .database import products_table

if not products_table.all():
    products = [
        {
            "id": 1,
            "name": "Laptop",
            "content": "Потужний ноутбук Intel Core i7, 16 ГБ RAM, SSD 512 ГБ.",
            "price": 1200.0,
            "category": "electronics",
            "quantity": 5,
            "image": "",
            "created_at": datetime.now().isoformat()
        },
        {
            "id": 2,
            "name": "Phone",
            "content": "Смартфон з OLED-дисплеєм та акумулятором 5000 мА·год.",
            "price": 800.0,
            "category": "electronics",
            "quantity": 10,
            "image": "",
            "created_at": datetime.now().isoformat()
        },
        {
            "id": 3,
            "name": "PC",
            "content": "Настільний комп'ютер з RTX 4070 та 32 ГБ RAM.",
            "price": 1800.0,
            "category": "electronics",
            "quantity": 3,
            "image": "",
            "created_at": datetime.now().isoformat()
        }
    ]

    products_table.insert_multiple(products)
    print("Товари додано до TinyDB")
else:
    print("База вже містить товари")
