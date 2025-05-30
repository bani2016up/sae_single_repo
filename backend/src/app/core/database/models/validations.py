from enum import StrEnum
from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..db.database import Base


class Status(StrEnum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    ENDED_SUCCESS = "ENDED_SUCCESS"
    ENDED_WITH_ERRORS = "ENDED_WITH_ERRORS"



class Validation(Base):
    __tablename__ = "validations"


    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(Integer, ForeignKey("documents.id"), nullable=False)
    status_id = Column(Integer)

    # Relationships
    document = relationship("Document", back_populates="validations")
    errors = relationship("Error", back_populates="validation")

    @property
    def status(self) -> Status:
        return Status(self.status_id) if self.status_id else Status.NOT_STARTED
