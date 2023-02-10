from app import db
from app.routes import app
from app.model_dir.user import User
from app.model_dir.people import People
from app.model_dir.gallery import Gallery

@app.shell_context_processor
def make_shell_context():
    return dict(db=db, User=User, People=People, Gallery=Gallery )