from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Mapped, mapped_column
from datetime import date
import os

# Environment variables for secure credentials management
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql+psycopg2://postgres:Riskey001@localhost/HELPDESK')

engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Define Department
class Department(Base):
    __tablename__ = 'department'

    D_ID = Column(Integer, primary_key=True)
    D_Name = Column(String)
    D_Location = Column(String)
    employees = relationship("Employee", back_populates="department")
    projects = relationship("Project", back_populates="department")

    def __repr__(self):
        return f"Department(D_ID={self.D_ID}, D_Name='{self.D_Name}', D_Location='{self.D_Location}')"

# Define Employee
class Employee(Base):
    __tablename__ = 'employee'

    E_ID = Column(Integer, primary_key=True)
    E_Pos = Column(String)
    E_First = Column(String)
    E_Last = Column(String)
    E_St = Column(String)
    E_City = Column(String)
    E_State = Column(String)
    E_Zip = Column(String)
    D_ID = Column(Integer, ForeignKey('department.D_ID'))
    department = relationship("Department", back_populates="employees")

    def __repr__(self):
        return (f"Employee(E_ID={self.E_ID}, E_Pos='{self.E_Pos}', E_First='{self.E_First}', "
                f"E_Last='{self.E_Last}', E_St='{self.E_St}', E_City='{self.E_City}', "
                f"E_State='{self.E_State}', E_Zip='{self.E_Zip}', D_ID={self.D_ID})")

# Define Customer
class Customer(Base):
    __tablename__ = 'customer'

    c_email = Column(String, primary_key=True)
    c_number = Column(String(15))
    c_last = Column(String(30))
    c_first = Column(String(30))

    def __repr__(self):
        return f"Customer(c_email={self.c_email}, c_number={self.c_number}, c_last={self.c_last}, c_first={self.c_first})"

# Define Project
class Project(Base):
    __tablename__ = 'project'

    P_ID = Column(Integer, primary_key=True)
    P_Name = Column(String)
    P_Start = Column(Date, default=date.today())
    P_End = Column(Date)
    D_ID = Column(Integer, ForeignKey('department.D_ID'))
    department = relationship("Department", back_populates="projects")

    def __repr__(self):
        return f"Project(P_ID={self.P_ID}, P_Name='{self.P_Name}', P_Start={self.P_Start}, P_End={self.P_End})"

# Define Databases
class Databases(Base):
    __tablename__ = "databases"

    DB_ID = Column(Integer, primary_key=True)
    DB_Faculty = Column(String)
    DB_Student = Column(String)
    DB_Alumni = Column(String)

    def __repr__(self):
        return f"Databases(DB_ID={self.DB_ID}, DB_Faculty='{self.DB_Faculty}', DB_Student='{self.DB_Student}', DB_Alumni='{self.DB_Alumni}')"

# Create tables
Base.metadata.create_all(engine)

# Sample data insertion
Session = sessionmaker(bind=engine)

with Session() as session:
    # Add employees
    employees = [
        Employee(E_ID=1, E_Pos='Manager', E_First='John', E_Last='Doe', E_St='123 Maple St.', E_City='Springfield', E_State='IL', E_Zip='62704'),
        Employee(E_ID=2, E_Pos='Analyst', E_First='Jane', E_Last='Smith', E_St='456 Oak St.', E_City='Decatur', E_State='IL', E_Zip='62521'),
        Employee(E_ID=3, E_Pos='Developer', E_First='Mike', E_Last='Brown', E_St='789 Pine St.', E_City='Champaign', E_State='IL', E_Zip='61820')
    ]
    session.add_all(employees)

    # Add customers
    customers = [
        Customer(c_email='ladams@luc.edu', c_number='555-123-4567', c_last='Adams', c_first='Lucy'),
        Customer(c_email='jbaker@luc.edu', c_number='555-987-6543', c_last='Baker', c_first='Justin')
    ]
    session.add_all(customers)

    # Add departments and projects
    it_department = Department(D_ID=1, D_Name='IT', D_Location='Building A')
    hr_department = Department(D_ID=2, D_Name='HR', D_Location='Building B')
    departments = [it_department, hr_department]
    session.add_all(departments)

    projects = [
        Project(P_Name='Website Redesign', D_ID=1),
        Project(P_Name='Employee Wellness Program', D_ID=2)
    ]
    session.add_all(projects)

    session.commit()

employee_details = session.query(Employee.E_ID, Employee.E_First, Employee.E_Last,
                              	Employee.E_Pos, Department.D_Name, Department.D_Location)\
                           .join(Department, Employee.D_ID == Department.D_ID).all()

for emp in employee_details:
 	print(f'Employee ID: {emp.E_ID}, Name: {emp.E_First} {emp.E_Last}, '
  	     f'Position: {emp.E_Pos}, Department: {emp.D_Name}, Location: {emp.D_Location}')
