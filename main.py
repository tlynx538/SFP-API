from fastapi import FastAPI
from db.main import PurplePandaDB
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
origins = [
    "http://localhost:3000",
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
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

class AddCart(BaseModel):
    user_id : int 
    item_id : int 
    quantity : int 

class ViewCart(BaseModel):
    user_id : int

class DeleteCart(BaseModel):
    user_id : int 
    item_id : int 

class UpdateCart(BaseModel):
    user_id : int 
    item_id : int 
    quantity : int    

class CreateOrder(BaseModel):
    user_id : int

class ChangeOrderStatus(BaseModel):
    user_id : int 
    status_id :int 

# defining for inventory route
inventory_api_route = "/api/inventory/"

@app.get(inventory_api_route+'products')
def product_list():
    products = obj.SelectProducts()
    return products

@app.get(inventory_api_route+'products/'+'{gender}/'+'{category}/')
def product_list(category, gender): 
    products = obj.SelectItemsByCategory(product_category=category,product_gender=gender)
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

@app.get(inventory_api_route+'delete/product/'+'{product_id}')
def delete_product(product_id):
    return obj.DeleteRowFromProductDetails(product_id=product_id)

@app.post(inventory_api_route+'add/cart')
def add_to_cart(cart: AddCart):
    return obj.AddToCart(item_id=cart.item_id, user_id=cart.user_id, quantity= cart.quantity)

@app.get(inventory_api_route+'view/cart/'+'{user_id}')
def view_cart(user_id):
    return obj.ViewCart(user_id=user_id)

@app.get(inventory_api_route+'delete/cart')
def delete_item_cart(cart: DeleteCart):
    return obj.DeleteItemFromCart(item_id=cart.item_id, user_id=cart.user_id)

@app.post(inventory_api_route+'update/cart')
def update_item_cart(cart: UpdateCart):
    return obj.UpdateQuantityFromCartItem(item_id=cart.item_id, quantity=cart.quantity, user_id=cart.user_id)

@app.post(inventory_api_route+'create/order')
def create_order(order: CreateOrder):
    return obj.CreateOrder(user_id=order.user_id)

@app.post(inventory_api_route+'status/order')
def order_status_change(order: ChangeOrderStatus):
    return obj.ChangeOrderStatus(user_id=order.user_id, status_id=order.status_id)

