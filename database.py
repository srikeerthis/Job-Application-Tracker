from sqlalchemy import create_engine, Column, Integer, String, Date,TIMESTAMP, ForeignKey
from datetime import datetime,date
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

declarative_base = declarative_base()

class Application(declarative_base):
    __tablename__ = 'applications'
    
    id = Column(Integer, primary_key=True)
    company_name = Column(String, nullable=False)
    role = Column(String, nullable=False)
    experience_level = Column(String, nullable=False)
    job_id = Column(String, nullable=False)
    work_type = Column(String, nullable=False)
    location = Column(String, nullable=False)
    country = Column(String, nullable=False)
    date_added = Column(TIMESTAMP, nullable=False)

    status_history = relationship("StatusHistory", back_populates="application")

class StatusHistory(declarative_base):
    __tablename__ = 'status_history'
    
    history_id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey('applications.id'), nullable=False)
    status = Column(String, nullable=False)
    status_date = Column(Date, nullable=False)

    application = relationship("Application", back_populates="status_history")

def create_database():
    engine = create_engine('sqlite:///job_applications.db', echo=True)
    declarative_base.metadata.create_all(engine)
    print("Database and tables created successfully.")

def save_application(application_data):
    engine = create_engine('sqlite:///job_applications.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    new_application = Application(
        company_name=application_data['company_name'],
        role=application_data['role'],
        experience_level=application_data['experience_level'],
        job_id=application_data['job_id'],
        work_type=application_data['work_type'],
        location=application_data['location'],
        country=application_data['country'],
        date_added=datetime.now()
    )
    
    session.add(new_application)
    session.flush()

    new_status = StatusHistory(
        application_id=new_application.id,
        status=application_data['status'],
        status_date=date.today()
    )
    session.add(new_status)
    session.commit()
    session.close()
    print("Application saved successfully.")

if __name__ == "__main__":
    create_database()
    print("Database setup complete.")