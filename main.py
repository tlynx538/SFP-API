from fastapi import FastAPI

app = FastAPI()

@app.get('/')
def home():
    return {"Message":"Welcome to Purple Panda Backend API"}