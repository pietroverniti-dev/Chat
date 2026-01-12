from pymongo import AsyncMongoClient
from .db_interface import DatabaseInterface

# Configurazione
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "bacheca_db"
PORT = 9001
COOKIE_SECRET = "chiave_segreta_molto_lunga_e_sicura"

# Inizializzazione Client
client = AsyncMongoClient(MONGO_URL)
db = client[DB_NAME]

# Istanza globale dell'interfaccia
db_interface = DatabaseInterface(db)