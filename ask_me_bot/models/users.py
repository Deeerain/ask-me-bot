from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column
from db import BaseModel


class User(BaseModel):
    telegram_id = mapped_column(
        BigInteger, nullable=False, index=True, unique=True
    )
    chat_id = mapped_column(
        BigInteger,
        nullable=False,
        index=True,
        unique=True,
    )
