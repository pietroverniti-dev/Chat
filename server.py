import tornado.ioloop
import tornado.web
import os

# Importazione delle configurazioni e degli handler secondo il tuo path
from backend.db.db import PORT, COOKIE_SECRET
from backend.handlers.auth import LoginHandler, RegisterHandler, LogoutHandler
from backend.handlers.messages import MessagesHandler, MessageDeleteHandler

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        # Serve l'index.html dalla cartella static
        self.render("static/index.html")

def make_app():
    # Definiamo i percorsi per i file statici
    settings = {
        "cookie_secret": COOKIE_SECRET,
        "static_path": os.path.join(os.path.dirname(__file__), "static"),
        "template_path": os.path.dirname(__file__),
        "debug": True,
        "autoreload": True
    }

    return tornado.web.Application([
        (r"/", MainHandler),
        
        # Rotte API
        (r"/api/register", RegisterHandler),
        (r"/api/login", LoginHandler),
        (r"/api/logout", LogoutHandler),
        (r"/api/messages", MessagesHandler),
        (r"/api/messages/([^/]+)/delete", MessageDeleteHandler),
        
        # Gestione automatica di /static/css/ e /static/js/
        (r"/static/(.*)", tornado.web.StaticFileHandler, {"path": settings["static_path"]}),
    ], **settings)

if __name__ == "__main__":
    app = make_app()
    print(f"Server in esecuzione su http://localhost:{PORT}")
    app.listen(PORT)
    tornado.ioloop.IOLoop.current().start()