from dotenv import load_dotenv
from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
from .routers import post, user, auth, votes

load_dotenv()

app = FastAPI()

origins = ["*"]
 
# The alloo all website to talk to the api 
app.add_middleware(
    CORSMiddleware, 
    allow_origins=origins, 
    allow_credentials=True, 
    allow_methods=["*"], 
    allow_headers=["*"]
)
 
app.include_router(post.router, tags=["post"])
app.include_router(user.router, tags=["user"])
app.include_router(auth.router)
app.include_router(votes.router)

# .get is the method while `/` is the path 
@app.get("/")
async def root(): 
    return {"message": "Hello World from Ubuntu"}


