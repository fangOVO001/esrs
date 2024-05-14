from sqlalchemy import Column, Integer, String, Text
from database import Base

class Content(Base):
  __tablename__ = 'content'
  id = Column(Integer, unique=True, primary_key=True, autoincrement="auto")
  title = Column(String)
  content = Column(Text)
  category = Column(String)
  from_url = Column(Text)

  def __init__(self,title, content, category, from_url):
    self.title = title
    self.content = content
    self.category = category
    self.from_url = from_url