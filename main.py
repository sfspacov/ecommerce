import uvicorn
from fastapi import FastAPI
from database import session, engine
from models.todo import Todo
from models.product import Base, Product
from schemas.products import Products

app = FastAPI()
Base.metadata.create_all(engine)

@app.get("/")
async def get_all_todos():
    todos_query = session.query(Todo)
    return todos_query.all()

@app.post("/product")
def create(product: Products):
    new_product = Product(**product.model_dump())
    session.add(new_product)
    session.commit()
    return new_product

@app.post("/create")
async def create_todo(text: str, is_complete: bool = False):
    todo = Todo(text=text, is_done=is_complete)
    session.add(todo)
    session.commit()
    return {"todo added": todo.text}

@app.get("/done")
async def list_done_todos():
    todos_query = session.query(Todo)
    done_todos_query = todos_query.filter(Todo.is_done==True)
    return done_todos_query.all()

@app.put("/update/{id}")
async def update_todo(
    id: int,
    new_text: str = "",
    is_complete: bool = False
):
    todo_query = session.query(Todo).filter(Todo.id==id)
    todo = todo_query.first()
    if new_text:
        todo.text = new_text
    todo.is_done = is_complete
    session.add(todo)
    session.commit()

@app.delete("/delete/{id}")
async def delete_todo(id: int):
    todo = session.query(Todo).filter(Todo.id==id).first() # Todo object
    session.delete(todo)
    session.commit()
    return {"todo deleted": todo.text}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)