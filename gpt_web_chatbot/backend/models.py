from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing_extensions import final

db = SQLAlchemy()

@final
class User(db.Model):  # type: ignore
    """
    A user model for storing user data.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username chosen by the user.
        password (str): The password chosen by the user.
    """
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(db.String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(120), nullable=False)
    chats: Mapped[list["Chat"]] = relationship('Chat', backref='user', lazy=True)

@final
class Chat(db.Model):  # type: ignore
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message: Mapped[str] = mapped_column(db.Text, nullable=False)
    reply: Mapped[str] = mapped_column(db.Text, nullable=False)
    timestamp: Mapped[datetime] = mapped_column(db.DateTime, default=lambda: datetime.now(timezone.utc))
