from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import post, user, auth, vote

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# models.Base.metadata.create_all(bind=engine)

app.include_router(post.router, tags=["Posts"])
app.include_router(user.router, tags=["Users"])
app.include_router(auth.router, tags=["Auth"])
app.include_router(vote.router, tags=["Votes"])


@app.get("/", tags=["Fun"])
def root():
    return {"message": "Hello sun!"}


@app.get("/hello/{name}", tags=["Fun"])
def say_hello(name: str):
    return {"message": f"Helloo, {name}!"}
