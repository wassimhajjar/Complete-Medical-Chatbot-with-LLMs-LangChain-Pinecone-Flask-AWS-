from app.core.database import Base,engine
from app.db.models import message,user

def create_tables():
    Base.metadata.create_all(bind=engine)
    print("Created")
    
