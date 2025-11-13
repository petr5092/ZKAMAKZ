from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from spec.models import Spec


class University(Base):

    __tablename__ = "universities"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
    count_students = Column(Integer, default=0, nullable=False)
    count_campus = Column(Integer, default=0, nullable=False)
    count_branches = Column(Integer, default=0, nullable=False)
    specs = relationship(
        "Spec",
        back_populates="university",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

