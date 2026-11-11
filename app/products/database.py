from tinydb import TinyDB
from pathlib import Path

data_dir = Path(__file__).resolve().parents[2] / "data"
data_dir.mkdir(exist_ok=True)

db = TinyDB(data_dir / "products.json")
products_table = db.table("products")
