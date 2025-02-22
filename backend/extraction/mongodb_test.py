uri = "mongodb+srv://rthippar:TJl8bbai6BVV07cJ@cluster0.s9zrz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
import ssl
import certifi
from pymongo import MongoClient

client = MongoClient(
    uri,
    tls=True,
    tlsCAFile=certifi.where()
)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
