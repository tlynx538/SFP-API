import sqlalchemy as db 
class PandaDB:
    def __init__(self):
        try:
            self.engine = db.create_engine("postgresql+psycopg2://localhost:5432/pandadb")
            self.connection = self.engine.connect()
            self.metadata = db.MetaData()
        except:
            print("Some Error has Occured")

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
            print("Some Error Occured")
            return False  

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
            print("Some Error Occured")
            return False 

    def InsertRowToProductDetails(self, product_name, product_desc, product_gender, product_category):
        product_details = self.getProductDetails()
        if(len(product_name) == 0 or len(product_gender)  == 0  or len(product_desc)  == 0  or len(product_category)  == 0 ):
            print("All Details are Required, Please make sure to fill all arguments")
            return False 
        else:
            try:
                query = db.insert(product_details).values(product_name=product_name,product_desc=product_desc,product_gender=product_gender,product_category=product_category)
                self.connection.execute(query)
                print("Row Inserted Successfully")
                return True
            except:
                print("Please check if the name is unique, if not the item already exists")
                return False 

    def UpdateRowFromProductDetails(self,product_name=None,product_desc=None,product_gender=None,product_category=None,product_id=None):
        product_details = self.getProductDetails()
        if product_details is not False:
            if product_id is None:
                print("Product ID is mandatory.")
                return False
            else:
                if(self.checkIfProductIDExists(product_id=product_id,table=product_details)):
                    row = self.SelectRowFromProductDetailsByProductID(product_id=product_id)
                    print(row)
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
            print("An Error Occured")
            return False  

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

    # Additional Functions
    def getProductDetails(self):
        product_details = db.Table('product_details', self.metadata, autoload=True, autoload_with=self.engine)
        return product_details

    def viewKeysforProductDetails(self):
        try:
            product_details = self.getProductDetails()
            return product_details.columns.keys()
        except:
            print("Some Error Occured")
            return False

    def checkIfProductIDExists(self,product_id,table=None):
        query = db.select([table.c.product_id]).where(table.c.product_id == product_id)
        result = self.connection.execute(query).fetchall()
        if(len(result) == 0):
            print("Product ID does not exist")
            return False 
        else:
            return True
