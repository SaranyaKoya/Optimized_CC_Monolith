import redis
import json
from products import dao

# Initialize Redis cache
cache = redis.StrictRedis(host='localhost', port=6379, db=0)

class Product:
    def __init__(self, id: int, name: str, description: str, cost: float, qty: int = 0):
        self.id = id
        self.name = name
        self.description = description
        self.cost = cost
        self.qty = qty

    @staticmethod
    def load(data):
        return Product(data['id'], data['name'], data['description'], data['cost'], data['qty'])

    def to_dict(self):
        # Convert the product object to dictionary for easy caching
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'cost': self.cost,
            'qty': self.qty
        }

def get_product_from_cache(product_id: int):
    # Try fetching from cache first
    cached_product = cache.get(f"product:{product_id}")
    if cached_product:
        return Product.load(json.loads(cached_product))  # Deserialize cached data
    
    # If not found in cache, fetch from DB and cache it
    product_data = dao.get_product(product_id)
    if product_data:
        product = Product.load(product_data)
        cache.set(f"product:{product_id}", json.dumps(product.to_dict()))  # Cache the product
        return product
    return None

def list_products_from_cache():
    # Try fetching all products from cache
    cached_products = cache.get("all_products")
    if cached_products:
        products_data = json.loads(cached_products)  # Deserialize cached data
        return [Product.load(p) for p in products_data]
    
    # If not found in cache, fetch from DB and cache it
    products_data = dao.list_products()
    if products_data:
        products = [Product.load(product) for product in products_data]
        cache.set("all_products", json.dumps([p.to_dict() for p in products]))  # Cache all products
        return products
    return []

def list_products() -> list[Product]:
    # Use the cache-first strategy
    return list_products_from_cache()

def get_product(product_id: int) -> Product:
    # Use the cache-first strategy
    return get_product_from_cache(product_id)

