from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models.chat import ChatMessage

class ConversationMemory:
    def __init__(self, db: Session, session_id: str, window_size: int = 5):
        self.db = db
        self.session_id = session_id
        self.window_size = window_size

    def add(self, role: str, content: str):
        message = ChatMessage(
            session_id=self.session_id,
            role=role,
            content=content
        )
        self.db.add(message)
        self.db.commit()

    def get_context(self) -> str:
        # Fetch the last N messages for this specific session
        messages = self.db.query(ChatMessage)\
            .filter(ChatMessage.session_id == self.session_id)\
            .order_by(desc(ChatMessage.created_at))\
            .limit(self.window_size)\
            .all()
        
        # Reverse to get chronological order
        messages.reverse()
        
        context = ""
        for msg in messages:
            context += f"{msg.role.capitalize()}: {msg.content}\n"
            
        return context.strip()