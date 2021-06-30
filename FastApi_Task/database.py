from sqlalchemy import create_engine



DATABASE_URL = "postgresql://postgres:postgrepass@localhost:5432/taskdb"
engine = create_engine(DATABASE_URL)