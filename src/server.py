from fastapi import FastAPI
from api.routes import users, posts

app = FastAPI()

app.include_router(users.router)
app.include_router(posts.router)

@app.get("/")
async def root():
    return {"message": "to be or not to be. that is the bot's question."}