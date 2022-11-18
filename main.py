from fastapi import FastAPI
from db.main import PurplePandaDB
from pydantic import BaseModel
app = FastAPI()

# Initialising the Database Connection as well as SQLAlchemy object
obj = PurplePandaDB()

# Create Models for Request Body
class AddProduct(BaseModel):
    product_name : str 
    product_desc : str  
    product_gender : str 
    product_category : str 

class AddProductItem(BaseModel):
    product_id : int 
    item_size : str 
    color : str 
    quantity : int 
    discount : float 
    price : float 

# defining for inventory route
inventory_api_route = "/api/inventory/"

@app.get(inventory_api_route+'products')
def product_list():
    products = obj.SelectProducts()
    return products

@app.post(inventory_api_route+'add/product')
def add_product(prod: AddProduct):
    return obj.InsertRowToProductDetails(product_name=prod.product_name,product_desc=prod.product_desc,product_category=prod.product_category,product_gender=prod.product_gender)  

@app.post(inventory_api_route+'add/product/item')
def add_product_item(prod: AddProductItem):
    return obj.InsertItemintoProductInfo(product_id=prod.product_id,item_size=prod.item_size,color=prod.color,quantity=prod.quantity,discount=prod.discount,price=prod.price) 

@app.get(inventory_api_route+'delete/product/item/'+'{item_id}')
def delete_product_item(item_id):
    return obj.DeleteItemFromProductInfo(item_id=item_id)
