from sqlalchemy import Column, Integer, String
from database import Base

class Favorite(Base):
  __tablename__ = 'favorite'
  id = Column(Integer, unique=True, primary_key=True, autoincrement="auto")
  email = Column(String)
  content_id = Column(Integer)

  def __init__(self, email, content_id):
    self.email = email
    self.content_id = content_id