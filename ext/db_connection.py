from pymongo import MongoClient

client = MongoClient("mongodb+srv://adru:adru123@cluster0.ih5qq0z.mongodb.net/?retryWrites=true&w=majority")
db = client['EasyChat']
users_collection = db['User']
session_store = db['Session']
