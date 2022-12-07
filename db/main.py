'''
 TODO:
    [Inventory, Cart and Orders]
    1. Fix Exception Messages 
    2. Fix Edge Cases 
'''
import sqlalchemy as db 
from datetime import datetime 

class StoreFrontDB:
    error_message = {"status": "ERROR","message": "An Error Occured"}
    success_message = {"status": "OK","message": "Row Updated Successfully"}
    def __init__(self):
        try:
            self.engine = db.create_engine("postgresql+psycopg2://localhost:5432/pandadb")
            self.connection = self.engine.connect()
            self.metadata = db.MetaData()
        except:
            return {"status": "ERROR", "message": "Database Error has Occured."}

    # Functions for Product Details Table:

    # Not neccessary but useful during tests
    def SelectAllFromProductDetails(self):
        try:
            ResultSet = []
            product_details = self.getProductDetails()
            query = db.select([product_details])
            result = self.connection.execute(query)
            for i in result:
                ResultSet.append(i._asdict())
            return ResultSet
        except:
            return self.error_message

    def SelectItemsByCategory(self,product_gender,product_category):
        try:
            ResultSet = []
            product_details = self.getProductDetails()
            product_info = self.getProductInfo()
            query = db.select([product_details,product_info]).where((product_details.c.product_id == product_info.c.product_id) & (product_details.c.product_gender == product_gender) & (product_details.c.product_category == product_category) & (product_info.c.primary == True) & (product_info.c.quantity > 0))
            result = self.connection.execute(query)
            for i in result: 
                ResultSet.append(i._asdict())
            return ResultSet 
        except:
            return self.error_message

    def SelectRowFromProductDetailsByProductID(self,product_id):
        try:
            ResultSet = []
            product_details = self.getProductDetails()
            query = db.select([product_details]).where(product_details.c.product_id == product_id)
            result = self.connection.execute(query)
            for row in result:
                ResultSet.append(row._asdict())
            return ResultSet[0]
        except:
            return self.error_message

    def InsertRowToProductDetails(self, product_name, product_desc, product_gender, product_category):
        product_details = self.getProductDetails()
        if(len(product_name) == 0 or len(product_gender)  == 0  or len(product_desc)  == 0  or len(product_category)  == 0 ):
            print("All Details are Required, Please make sure to fill all arguments")
            return False 
        else:
            all_product_names = self.getAllProductName()
            if(product_name not in all_product_names):
                query = db.insert(product_details).values(product_name=product_name,product_desc=product_desc,product_gender=product_gender,product_category=product_category)
                self.connection.execute(query)
                return self.success_message
            else:
                return {"status": "ERROR", "message": "Product Already Exists"}


    def UpdateRowFromProductDetails(self,product_name=None,product_desc=None,product_gender=None,product_category=None,product_id=None):
        product_details = self.getProductDetails()
        if product_details is not False:
            if product_id is None:
                print("Product ID is mandatory.")
                return False
            else:
                if(self.checkIfProductIDExists(product_id=product_id,table=product_details)):
                    row = self.SelectRowFromProductDetailsByProductID(product_id=product_id)
                    if(product_name is not None):
                        row["product_name"] = product_name
                    if(product_category is not None):
                        row["product_category"] = product_category
                    if(product_desc is not None):
                        row["product_desc"] = product_desc
                    if(product_gender is not None):
                        row["product_gender"] = product_gender
                    query = db.update(product_details).values(product_name = row["product_name"], product_desc = row["product_desc"], product_gender = row["product_gender"], product_category = row["product_category"]).where(product_details.c.product_id == product_id)
                    self.connection.execute(query)
                    print("Row Updated Successfully")
                    return True
        else:
            return self.error_message 

    def DeleteRowFromProductDetails(self,product_id=None):
        product_details = self.getProductDetails()
        if product_id is None:
            print("Product ID is mandatory.")
            return False
        else:
            if(self.checkIfProductIDExists(product_id=product_id,table=product_details)):
                query = db.delete(product_details).where(product_details.c.product_id == product_id)
                self.connection.execute(query)
                print("Row Deleted Successfully")
                return True 
    
    # Product Info Page
    def SelectAllfromProductInfo(self):
        try:
            ResultSet = []
            product_info = self.getProductInfo()
            query = db.select([product_info])
            result = self.connection.execute(query)
            for i in result:
                ResultSet.append(i._asdict())
            return ResultSet
        except:
            return self.error_message

    def SelectRowsBySameProductID(self,product_id):
        try:
            ResultSet = []
            product_info = self.getProductInfo()
            query = db.select([product_info]).where(product_info.c.product_id == product_id)
            result = self.connection.execute(query)
            for row in result:
                ResultSet.append(row._asdict())
            return ResultSet
        except:
            return self.error_message

    def SelectRowByItemID(self,item_id):
        try:
            ResultSet = []
            product_info = self.getProductInfo()
            query = db.select([product_info]).where(product_info.c.item_id == item_id)
            result = self.connection.execute(query)
            for row in result:
                ResultSet.append(row._asdict())
            return ResultSet[0]
        except: 
            return self.error_message

    def InsertItemintoProductInfo(self,product_id,item_size,color,quantity,discount,price):
        try:
            product_info = self.getProductInfo()
            items = self.SelectRowsBySameProductID(product_id=product_id)
            filtered_item = [x for x in items if x['item_size'] == item_size and x['color'] == color]
            if(len(items) == 0 or len(filtered_item) == 0):
                query = db.insert(product_info).values(product_id=product_id,item_size=item_size,color=color,quantity=quantity,discount=discount,price=price)
                self.connection.execute(query)
                return self.success_message
            else:
                item_id = filtered_item[0]["item_id"]
                original_quantity = filtered_item[0]["quantity"]
                query = db.update(product_info).values(quantity = quantity + original_quantity).where(product_info.c.item_id == item_id)
                self.connection.execute(query)
                return self.success_message
        except:
            return self.error_message

    def DeleteItemFromProductInfo(self,item_id):
        product_info =  self.getProductInfo()
        if(self.checkIfItemIDExists(item_id=item_id)):
            query = db.delete(product_info).where(product_info.c.item_id == item_id)
            self.connection.execute(query)
            return self.success_message
        

    def UpdateItemFromProductInfo(self, item_id=None, item_size=None, color=None, quantity=None, price=None, discount=None,product_id = None):
        try:
            product_info =  self.getProductInfo()
            if(self.checkIfItemIDExists(item_id=item_id)):
                row = self.SelectRowByItemID(item_id=item_id)
                if(item_size is not None):
                    row["item_size"] = item_size 
                if(color is not None):
                    row["color"] = color 
                if(quantity is not None): 
                    row["quantity"] = quantity 
                if(price is not None): 
                    row["price"] = price 
                if(discount is not None): 
                    row["discount"] = discount 
                query = db.update(product_info).values(item_size=row["item_size"],color=row["color"],quantity=row["quantity"], price = row["price"], discount = row["discount"]).where(product_info.c.item_id == item_id)
                self.connection.execute(query)
                return self.success_message
        except:
            return self.error_message

    # Core Functions       
    def SelectProducts(self):
        try:
            ResultSet = []
            product_info = self.getProductInfo()
            product_details = self.getProductDetails()
            query = db.select([product_details.c.product_name,product_details.c.product_desc,product_info.c.item_size,product_info.c.color,product_details.c.product_gender,product_details.c.product_category,product_info.c.quantity,product_info.c.discount,product_info.c.price,product_info.c.rating])
            query = query.select_from(product_details.join(product_info, product_details.c.product_id == product_info.c.product_id))
            results = self.connection.execute(query)
            for row in results:
                ResultSet.append(row._asdict())
            return ResultSet
        except: 
            return self.error_message
    
    def AddToCart(self,quantity,item_id,user_id=None):
        cart = self.getCart()
        if(self.checkIfItemIDExists(item_id=item_id)):
            quantity_available = self.checkIfQuantityIsPresent(item_id=item_id)
            if(quantity_available - quantity >= 0):
                if(self.checkIfItemIDExistsinCart(item_id=item_id)):
                    self.UpdateQuantityFromCartItem(item_id=item_id, quantity=quantity,user_id=user_id)
                else:
                    query = db.insert(cart).values(quantity=quantity,item_id=item_id,user_id=user_id)
                    self.connection.execute(query)
                self.UpdateItemFromProductInfo(quantity=(quantity_available-quantity), item_id=item_id)

                return {"status": "SUCCESS","message": "Item Added To Cart"}
            else: 
                return {"status": "ERROR","message": "Quantity is unavailable"}
        else:
            return self.error_message

    def ViewCart(self, user_id):
        ResultSet = []
        # check if user id exists
        cart = self.getCart()
        product_info = self.getProductInfo()
        product_details = self.getProductDetails()
        query = db.select([cart,product_info,product_details]).join(product_info, product_info.c.item_id == cart.c.item_id).join(product_details, product_details.c.product_id == product_info.c.product_id).where(cart.c.user_id == user_id)
        results = self.connection.execute(query)
        for row in results:
            ResultSet.append(row._asdict())
        return ResultSet 

    def DeleteItemFromCart(self, item_id, user_id):
        cart = self.getCart()
        quantity = self.getQuantityFromCart(item_id=item_id, user_id=user_id)
        self.UpdateItemFromProductInfo(item_id=item_id, quantity=quantity)
        query = db.delete(cart).where((cart.c.user_id == user_id) & (cart.c.item_id == item_id))
        self.connection.execute(query)
        return self.success_message

    def UpdateQuantityFromCartItem(self, quantity, user_id, item_id):
        cart = self.getCart()
        query = db.update(cart).values(quantity = quantity).where((cart.c.user_id == user_id) & (cart.c.item_id == item_id))
        self.connection.execute(query)
        return self.success_message

    # Orders 
    def CreateOrder(self,user_id):
        # filter through cart items by user id [v]
        # prepare order and retrieve order_id [v]
        # add items to order_details with order_id [v]
        # and remove the items from cart [v]
        # update status (optional)
        # need rectification and debugging
        cart = self.getCartByUserId(user_id=user_id)
        order_details = self.getOrderDetails()
        order = self.getOrder()
        buy_timestamp = datetime.now()
        query = db.insert(order).values(user_id=user_id, date_of_purchase=buy_timestamp)
        self.connection.execute(query)
        order_id = self.retrieveOrderId(user_id=user_id)
        for i in cart:
            query = db.insert(order_details).values(order_id = order_id, item_id = i["item_id"], quantity = i["quantity"])
            self.connection.execute(query)
        self.DeleteAllCartItems(user_id=user_id)
        # change status to Active 
        self.ChangeOrderStatus(user_id=user_id,status_id=1)
        return self.success_message

    def ChangeOrderStatus(self,user_id,status_id):
        order = self.getOrder()
        query = db.update(order).values(status_id = status_id).where(order.c.user_id == user_id)
        self.connection.execute(query)
        return self.success_message 

    # Additional Functions
    def getProductDetails(self):
        product_details = db.Table('product_details', self.metadata, autoload=True, autoload_with=self.engine)
        return product_details

    def getProductInfo(self):
        product_info = db.Table('product_info',self.metadata,autoload=True, autoload_with=self.engine)
        return product_info

    def getCart(self):
        cart = db.Table('cart',self.metadata,autoload=True, autoload_with=self.engine)
        return cart 

    def getCartByUserId(self,user_id):
        ResultSet = []
        cart = self.getCart()
        query = db.select([cart]).where(cart.c.user_id == user_id)
        results = self.connection.execute(query) 
        for row in results:
            ResultSet.append(row._asdict())
        return ResultSet 

    def getOrder(self):
        order = db.Table('orders',self.metadata,autoload=True, autoload_with=self.engine)
        return order 
    
    def getOrderDetails(self):
        order_details = db.Table('order_details',self.metadata,autoload=True, autoload_with=self.engine)
        return order_details

    def retrieveOrderId(self,user_id):
        ResultSet = []
        order = self.getOrder()
        query = db.select([order.c.order_id]).where(order.c.user_id == user_id)
        results = self.connection.execute(query)
        for row in results:
            ResultSet.append(row._asdict())
        return ResultSet[0]['order_id']

    def viewKeysforProductDetails(self):
        try:
            product_details = self.getProductDetails()
            return product_details.columns.keys()
        except:
            print("Some Error Occured")
            return False
    
    def getAllProductName(self):
        ResultSet = []
        product_details = self.getProductDetails()
        query = db.select([product_details.c.product_name])
        results = self.connection.execute(query)
        for item in results:
            ResultSet.append(item[0])
        return ResultSet

    def checkIfItemIDExists(self,item_id):
        product_info = self.getProductInfo()
        query = db.select([product_info.c.item_id]).where(product_info.c.item_id == item_id)
        result = self.connection.execute(query).fetchall()
        if(len(result) == 0):
            print("Item ID does not exist")
            return False 
        else:
            return True

    def checkIfItemIDExistsinCart(self,item_id):
        cart = self.getCart()
        query = db.select([cart.c.item_id]).where(cart.c.item_id == item_id)
        result = self.connection.execute(query).fetchall()
        if(len(result) == 0):
            print("Item ID does not exist")
            return False 
        else:
            return True  

    def DeleteAllCartItems(self, user_id):
        print("Reached Delete Cart Items")
        cart_items = self.getCartByUserId(user_id=user_id)
        cart = self.getCart()
        for i in cart_items:
            query = db.delete(cart).where(cart.c.item_id == i["item_id"])
            self.connection.execute(query)
                    
    def checkIfProductIDExists(self,product_id,table=None):
        query = db.select([table.c.product_id]).where(table.c.product_id == product_id)
        result = self.connection.execute(query).fetchall()
        if(len(result) == 0):
            print("Product ID does not exist")
            return False 
        else:
            return True

    def checkIfQuantityIsPresent(self, item_id):
        product_info = self.getProductInfo()
        query = db.select([product_info.c.quantity]).where(product_info.c.item_id == item_id)
        result = self.connection.execute(query).fetchall()
        return result[0][0]

    def getQuantityFromCart(self, item_id, user_id):
        cart = self.getCart()
        query = db.select([cart.c.quantity]).where((cart.c.item_id == item_id) & (cart.c.user_id == user_id))
        result = self.connection.execute(query).fetchall()
        return result[0][0]

