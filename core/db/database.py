from sqlmodel import create_engine, Session


engine = create_engine('postgresql://postgres:postgres@database:5432/fast')
session = Session(engine)


# используется с pandas to_sql
legacy_engine = create_engine('postgresql://postgres:postgres@database:5432/fast', future=False)