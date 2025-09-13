from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager

from src.infra.api.routes import PlansRouter, SubscriptionRouter, UserAccountRouter
from src.infra.db import create_db_and_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup event.
    """

    create_db_and_tables()
    yield


app = FastAPI(title="Subscription Service API", lifespan=lifespan)

app.include_router(PlansRouter)
app.include_router(UserAccountRouter)
app.include_router(SubscriptionRouter)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
