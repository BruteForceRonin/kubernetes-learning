from fastapi import FastAPI
app = FastAPI()
ORDERS = [{"id": 1, "item": "Laptop", "user_id": 1},
          {"id": 2, "item": "Phone", "user_id": 1},
          {"id": 3, "item": "Book", "user_id": 2}]

@app.get("/orders")
def orders(): return ORDERS

@app.get("/health")
def health(): return {"status": "ok"}