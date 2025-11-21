from app.database import Base, engine

print("Creating tables in database...")
Base.metadata.create_all(bind=engine)
print("Done.")