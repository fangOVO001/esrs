from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
  __tablename__ = 'favorite'
  email = Column(String, unique=True, primary_key=True)
  password = Column(String(120))

  def __init__(self, email, password):
    self.email = email
    self.password = password