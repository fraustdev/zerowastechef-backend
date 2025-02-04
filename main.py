from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from database import SessionLocal, engine
import models  # Import models instead of database.py

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for request validation
class IngredientCreate(BaseModel):
    name: str
    quantity: str

# Home route
@app.get("/")
def home():
    return {"message": "Welcome to ZeroWasteChef API"}

# Get all ingredients
@app.get("/ingredients", response_model=List[IngredientCreate])
def get_ingredients(db: Session = Depends(get_db)):
    return db.query(models.Ingredient).all()

# Add a new ingredient
@app.post("/ingredients")
def add_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    db_ingredient = models.Ingredient(name=ingredient.name, quantity=ingredient.quantity)
    db.add(db_ingredient)
    db.commit()
    return {"message": f"{ingredient.name} added!"}

# Delete an ingredient
@app.delete("/ingredients/{ingredient_name}")
def delete_ingredient(ingredient_name: str, db: Session = Depends(get_db)):
    db.query(models.Ingredient).filter(models.Ingredient.name == ingredient_name).delete()
    db.commit()
    return {"message": f"{ingredient_name} removed!"}
