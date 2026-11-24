import os, httpx, strawberry
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter

USER_URL = os.getenv("USER_URL", "http://user-service:8000")
ORDER_URL = os.getenv("ORDER_URL", "http://order-service:8000")

@strawberry.type
class Order:
    id: int
    item: str
    user_id: int

@strawberry.type
class User:
    id: int
    name: str

    @strawberry.field
    def orders(self) -> list[Order]:
        data = httpx.get(f"{ORDER_URL}/orders").json()
        return [Order(**o) for o in data if o["user_id"] == self.id]

@strawberry.type
class Query:
    @strawberry.field
    def users(self) -> list[User]:
        return [User(**u) for u in httpx.get(f"{USER_URL}/users").json()]

app = FastAPI()
app.include_router(GraphQLRouter(strawberry.Schema(Query)), prefix="/graphql")