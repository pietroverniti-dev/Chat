from bson import ObjectId
from datetime import datetime

class DatabaseInterface:
    def __init__(self, db):
        self._users = db["users"]
        self._messages = db["messages"]

    # ---------- UTENTI ----------
    async def get_user_by_email(self, email: str):
        return await self._users.find_one({"email": email})

    async def create_user(self, email: str, hashed_password: bytes):
        return await self._users.insert_one({
            "email": email,
            "password": hashed_password
        })

    # ---------- MESSAGGI ----------
    async def get_all_messages(self):
        # Restituisce tutti i messaggi ordinati per data crescente
        cursor = self._messages.find({}).sort("timestamp", 1)
        return [m async for m in cursor]

    async def create_message(self, user_id: str, email: str, text: str):
        return await self._messages.insert_one({
            "user_id": ObjectId(user_id),
            "author_email": email,
            "text": text,
            "timestamp": datetime.now()
        })

    async def delete_message(self, message_id: str, user_id: str):
        # Elimina solo se l'ID del messaggio E l'ID dell'utente corrispondono
        return await self._messages.delete_one({
            "_id": ObjectId(message_id),
            "user_id": ObjectId(user_id)
        })