from fastapi import FastAPI
from db.main import PandaDB

app = FastAPI()

# Initialising the Database Connection as well as SQLAlchemy object
obj = PandaDB()

# defining for inventory route
inventory_api_route = "/api/inventory/"

@app.get(inventory_api_route+'products')
def product_list():
    products = obj.SelectProducts()
    return products