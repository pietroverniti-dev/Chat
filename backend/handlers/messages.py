import tornado.escape
from .base import BaseHandler
from backend.db.db import db_interface

class MessagesHandler(BaseHandler):
    async def get(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        messages = await db_interface.get_all_messages()
        
        # Formattiamo i dati per il frontend
        out = []
        for m in messages:
            is_mine = str(m["user_id"]) == user["id"]
            out.append({
                "id": str(m["_id"]),
                "text": m["text"],
                "author": m["author_email"],
                "date": m["timestamp"].strftime("%d/%m/%Y %H:%M"),
                "is_mine": is_mine
            })
            
        self.write_json({"items": out})

    async def post(self):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        body = tornado.escape.json_decode(self.request.body)
        text = body.get("text", "").strip()

        if not text:
            return self.write_json({"error": "Testo obbligatorio"}, 400)

        await db_interface.create_message(user["id"], user["email"], text)
        self.write_json({"message": "Messaggio pubblicato"}, 201)

class MessageDeleteHandler(BaseHandler):
    async def delete(self, msg_id):
        user = self.get_current_user()
        if not user:
            return self.write_json({"error": "Non autenticato"}, 401)

        result = await db_interface.delete_message(msg_id, user["id"])
        
        if result.deleted_count == 0:
            return self.write_json({"error": "Impossibile eliminare (non tuo o non esiste)"}, 403)
            
        self.write_json({"message": "Messaggio eliminato"})