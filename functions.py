from product_catalog import catalog

def getProductInfo(productName: str) -> dict:
    for product in catalog:
        if productName.lower() in product["name"].lower():
            return product
    return {"error": "Product not found"}

def checkStock(productName: str) -> dict:
    for product in catalog:
        if productName.lower() in product["name"].lower():
            return {"stock": product["stock"]}
    return {"error": "Product not found"}

