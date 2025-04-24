from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base


class Validation(Base):
    __tablename__ = "validations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    validated = Column(Boolean, default=False, nullable=False)
    is_valid = Column(Boolean, default=False, nullable=False)

    # Relationships
    document = relationship("Document", back_populates="validations")
    errors = relationship("Error", back_populates="validation")
