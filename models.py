from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    # Один-до-багатьох: одна група має багато студентів
    students = relationship("Student", back_populates="group")

    def __repr__(self):
        return f"<Group(name={self.name})>"


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))

    # Зв’язки
    group = relationship("Group", back_populates="students")
    grades = relationship("Grade", back_populates="student")

    def __repr__(self):
        return f"<Student(fullname={self.fullname})>"


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True)
    fullname = Column(String(100), nullable=False)

    # Один-до-багатьох: викладач має кілька предметів
    subjects = relationship("Subject", back_populates="teacher")

    def __repr__(self):
        return f"<Teacher(fullname={self.fullname})>"


class Subject(Base):
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teachers.id"))

    # Зв’язки
    teacher = relationship("Teacher", back_populates="subjects")
    grades = relationship("Grade", back_populates="subject")

    def __repr__(self):
        return f"<Subject(name={self.name})>"


class Grade(Base):
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subject_id = Column(Integer, ForeignKey("subjects.id"))
    grade = Column(Integer, nullable=False)
    date_received = Column(DateTime(timezone=True), server_default=func.now())

    # Зв’язки
    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

    def __repr__(self):
        return f"<Grade(student_id={self.student_id}, subject_id={self.subject_id}, grade={self.grade})>"
