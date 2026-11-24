from fastapi import FastAPI
app = FastAPI()
USERS = [{"id": 1, "name": "Sekiro"}, {"id": 2, "name": "Usha"}]

@app.get("/users")
def users(): return USERS

@app.get("/health")
def health(): return {"status": "ok"}