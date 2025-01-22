import json
from cart import dao
from products import Product, get_product


class Cart:
    def __init__(self, id: int, username: str, contents: list[Product], cost: float):
        self.id = id
        self.username = username
        self.contents = contents
        self.cost = cost

    @staticmethod
    def load(data):
        return Cart(data['id'], data['username'], data['contents'], data['cost'])


def get_cart(username: str) -> list:
    """
    Fetch the cart details for a user. Parse and fetch product details efficiently.
    """
    # Fetch the cart details from the DAO
    cart_details = dao.get_cart(username)
    if not cart_details:
        return []

    try:
        # Extract all product IDs from the contents of the cart
        product_ids = []
        for cart_detail in cart_details:
            contents = cart_detail.get("contents", "[]")
            product_ids.extend(json.loads(contents))  # Parse JSON safely

        # Fetch each product's details (individual call for now)
        products_list = [get_product(pid) for pid in product_ids]
        return products_list

    except Exception as e:
        print(f"Error fetching cart details: {e}")
        return []


def add_to_cart(username: str, product_id: int):
    """
    Add a product to the user's cart.
    """
    dao.add_to_cart(username, product_id)


def remove_from_cart(username: str, product_id: int):
    """
    Remove a product from the user's cart.
    """
    dao.remove_from_cart(username, product_id)


def delete_cart(username: str):
    """
    Delete the entire cart for a user.
    """
    dao.delete_cart(username)

