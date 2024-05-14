from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
  __tablename__ = 'user'
  id = Column(Integer, unique=True, primary_key=True, autoincrement="auto")
  email = Column(String, unique=True)
  password = Column(String(120))

  def __init__(self, email, password):
    self.email = email
    self.password = password