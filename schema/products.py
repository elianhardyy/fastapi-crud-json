def product_serial(product) -> dict :
    return {
        "id":str(product["_id"]),
        "name":str(product["name"]),
        "price":int(product["price"]),
        "qty":int(product["qty"]),
    }

def list_serial(products) -> list:
    return[product_serial(product) for product in products]