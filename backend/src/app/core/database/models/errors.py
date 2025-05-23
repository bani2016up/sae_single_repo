from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base


class Error(Base):
    __tablename__ = "errors"

    id = Column(Integer, primary_key=True, autoincrement=True)
    validation_id = Column(Integer, ForeignKey("validations.id"), nullable=False)
    error = Column(String, nullable=False)
    resolved = Column(Boolean, default=False, nullable=False)

    # Relationships
    validation = relationship("Validation", back_populates="errors")
