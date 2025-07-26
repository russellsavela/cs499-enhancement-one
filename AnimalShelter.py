
## Python CRUD layer
##
##  Modified to use boto3 / DynamoDB
##
## Russ Savela, russell.savela@snhu.edu, 2025

#from pymongo import MongoClient
import boto3
# needed to get behavior similar to pymongo
from boto3.dynamodb.conditions import Key
from boto3.dynamodb.conditions import Attr
import botocore
from bson.objectid import ObjectId

class AnimalShelter(object):
    """ CRUD operations for Animal collection in MongoDB """

    def __init__(self, username, password):
        # Initializing the MongoClient. This helps to 
        # access the MongoDB databases and collections.
        # This is hard-wired to use the aac database, the 
        # animals collection, and the aac user.
        # Definitions of the connection string variables are
        # unique to the individual Apporto environment.
        #
        # You must edit the connection variables below to reflect
        # your own instance of MongoDB!
        #
        # Connection Variables
        #
        #USER = 'aacuser'
        #PASS = 'aacuser'
        #HOST = 'nv-desktop-services.apporto.com'
        #PORT = 30243
        #DB = 'AAC'
        #COL = 'animals'

        # override username / password
        #USER = username
        #PASS = password

        #
        # Initialize Connection
        #
        # self.client = MongoClient('mongodb://%s:%s@%s:%d' % (USER,PASS,HOST,PORT))
        # self.database = self.client['%s' % (DB)]
        # self.collection = self.database['%s' % (COL)]

        # Using DynamoDB now

        try: 
            self.dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

        except botocore.exceptions.ClientError as e:
                    print("Found a problem", e)

        self.database = self.dynamodb.Table('animals')

# Complete this create method to implement the C in CRUD.
    def create(self, data):
        if data is not None:
            result = self.database.insert_one(data)  # data should be dictionary
            #print(f"Insert result was id = {result.inserted_id} , ack =  {result.acknowledged} ");
        else:
            raise Exception("Nothing to save, because data parameter is empty")
        return(result.acknowledged)

# Create method to implement the R in CRUD
    def read(self, key):
        try:
            if key:
                # Build FilterExpression only if key is non-empty
                filter_expression = None
                for k, v in key.items():
                    condition = Attr(k).eq(v)
                    filter_expression = condition if filter_expression is None else filter_expression & condition

                response = self.database.scan(
                    FilterExpression=filter_expression
                # Optionally add ProjectionExpression here
                )
            else:
                # No filter – scan everything (be careful with large tables!)
                response = self.database.scan()

            return response['Items']

        except Exception as e:
            raise Exception("Error reading from database: ", e)

# Update method to implement the U in CRUD
#  expects key to update and data to update, returns # of items updated
    def update(self, query, data):

        # an empty filter key will update every row
        # since we probably don't want that, throw
        # an exception instead
        if query == {}:
            raise Exception("Empty key used for filter in update")
        
        if data is not None:
            newdata = {'$set': data}
            result = self.database.update_many(query, newdata)
        else:
            raise Exception("Nothing updated")

        return(result.modified_count)


# Delete method to implement the D in CRUD
#  expects a key to delete, returns number of items deleted
    def delete(self, key):
        
        if key is not None:
            result = self.database.delete_many(key)

        return(result.deleted_count)

