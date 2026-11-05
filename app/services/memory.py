from sqlalchemy.orm import Session
from app.models import ChatHistory

def save_message(db: Session, user_id: str, role: str, content: str):
    msg = ChatHistory(user_id=user_id, role=role, content=content)
    db.add(msg)
    db.commit()

def get_recent_history(db: Session, user_id: str, limit: int = 5) -> str:
    records = db.query(ChatHistory).filter(ChatHistory.user_id == user_id).order_by(ChatHistory.id.desc()).limit(limit).all()
    return "".join(f"{r.role}: {r.content}\n" for r in reversed(records))