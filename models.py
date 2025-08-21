from sqlalchemy import Column, Integer, String, Text, DateTime
from linkedin_agent.db import Base

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    status = Column(String, default="draft")  # draft | approved | posted | rejected | scheduled
    linkedin_url = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    scheduled_time = Column(DateTime, nullable=True)
