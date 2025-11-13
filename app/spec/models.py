from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base



class Spec(Base):

    __tablename__ = "specs"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    institute = Column(String, nullable=False)
    description = Column(String, nullable=False)
    cost_of_education = Column(Integer, nullable=False)
    total_hours = Column(Integer, nullable=False)
    practical_hours = Column(Integer, nullable=False)
    average_hours = Column(Integer, nullable=False)
    count_exams = Column(Integer, nullable=False)
    count_coursework = Column(Integer, nullable=False)
    count_budget = Column(Integer, nullable=False)
    min_mark = Column(Integer, nullable=False)
    average_mark = Column(Integer, nullable=False)
    university_id = Column(
        Integer,
        ForeignKey("universities.id", ondelete="CASCADE"),
        nullable=False,
    )
    university = relationship("University", back_populates="specs")

