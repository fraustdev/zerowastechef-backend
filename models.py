from sqlalchemy import Column, String, Integer
from database import Base  # Import Base from database.py

# Define Ingredient Model
class Ingredient(Base):
    __tablename__ = "ingredients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    quantity = Column(String)
