from sqlalchemy import BigInteger
from sqlalchemy.orm import mapped_column
from ask_me_bot.db import BaseModel


class User(BaseModel):
    telegram_id = mapped_column(
        BigInteger, nullable=False, index=True, unique=True
    )
