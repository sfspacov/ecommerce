import uvicorn
from fastapi import FastAPI
from database import session, engine
from models.product import Base, Product
from schemas.products import Products

app = FastAPI()
Base.metadata.create_all(engine)

@app.get("/products")
async def get():
    products = session.query(Product)
    return products.all()

@app.post("/products")
def post(product: Products):
    new_product = Product(**product.model_dump())
    session.add(new_product)
    session.commit()
    return new_product.id

@app.put("/products/{id}")
async def update_todo(product: Products, id: int):
    query = session.query(Product).filter(Product.id==id)
    first = query.first()
    if (first == None):
        return {"message": "Invalid id"}
    first.at_sale = product.at_sale
    first.description = product.description
    first.inventory = product.inventory
    first.title = product.title
    session.add(first)
    session.commit()

@app.delete("/products/{id}")
async def delete_todo(id: int):
    product = session.query(Product).filter(Product.id==id).first()
    if (product == None):
        return {"message": "Invalid id"}
    session.delete(product)
    session.commit()
    return {f"Product '{product.title}' deleted"}

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)