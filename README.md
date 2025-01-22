 >>Why and how you have optimised the code. 
1. /checkout Route Optimization
>Why Optimize?
The original code for calculating the total cost in the checkout route was inefficient because it used a nested loop to repeatedly decrement the item.cost variable:
for item in cart:
    while item.cost > 0:
        total += 1
        item.cost -= 1
This approach has a time complexity of O(n × cost), where n is the number of items in the cart. This is unnecessarily repetitive and slows down the execution.
>How It Was Optimized
The code was replaced with:
for item in cart:
    total += item.cost
This simplified logic has a time complexity of O(n), significantly improving the efficiency of the route by eliminating the nested loop.

2. /cart Route Optimization
>Why Optimize?
The get_cart function in the cart module had multiple inefficiencies:
It used eval() to evaluate the string representation of the cart contents, which is a security risk and slower.
It performed unnecessary loops, first iterating through cart details, then through evaluated contents, and again to fetch product details.
>How It Was Optimized
Replaced eval(): Used json.loads instead of eval to parse the contents safely.
Reduced Loops: Combined loops into a single pass to fetch product details directly.
Optimized code:
def get_cart(username: str) -> list:
    cart_details = dao.get_cart(username)
    if cart_details is None:
        return []

    items = json.loads(cart_details[0]['contents'])  # Parse JSON safely
    return [products.get_product(item_id) for item_id in items]
This reduces redundant processing and improves security and speed.

3. /browse Route Optimization
>Why Optimize?
The list_products function in the products module had inefficiencies:

It iterated through the products fetched from the database and created Product objects one by one in a loop.
>How It Was Optimized
The loop for loading Product objects was replaced with a list comprehension, which is more concise and faster.
Optimized code:
def list_products() -> list[Product]:
    return [Product.load(product) for product in dao.list_products()]
This minimizes function call overhead and makes the code cleaner and faster.


Results of Optimization
After optimizing these routes:
•	The average response time decreased, leading to faster API responses.
•	The number of requests processed by the system increased significantly, as evident from the Locust performance testing results.
•	The overall code became cleaner, easier to maintain, and more secure.
