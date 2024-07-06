from sqlalchemy import Column, Integer, String, Text, BigInteger, ForeignKey, LargeBinary, Boolean
from sqlalchemy.dialects.postgresql import TIMESTAMP, TIME
from sqlalchemy.orm import declarative_base, relationship, backref

Base = declarative_base()


class Notification(Base):
    __tablename__ = 'notifications'

    notification_id = Column(BigInteger, primary_key=True)
    tgchat_id = Column(BigInteger, nullable=False)
    is_repeating = Column(Boolean, nullable=False)
    day_of_week = Column(Integer, nullable=True)
    time = Column(TIME(timezone=False), nullable=True)
    week_parity = Column(Text, nullable=True)
    message = Column(Text, nullable=False)
    date = Column(TIMESTAMP(timezone=False), nullable=True)
    created_at = Column(TIMESTAMP(timezone=False), nullable=False)
