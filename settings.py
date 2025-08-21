from sqlalchemy import Column, Integer, String, Boolean
from linkedin_agent.db import Base

class Settings(Base):
    __tablename__ = "settings"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, default="AI Agentic Engineer")
    handle = Column(String, default="@username")
    website = Column(String, default="https://stark-ai-agents.netlify.app/")
    enable_promotion = Column(Boolean, default=False)
    enable_auto_comment_own = Column(Boolean, default=False)
    enable_comment_other = Column(Boolean, default=False)
