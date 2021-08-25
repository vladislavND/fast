from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('postgresql://postgres:postgres@localhost:5432/fast')
Session = sessionmaker(bind=engine)
sessions = Session()
Base = declarative_base()

