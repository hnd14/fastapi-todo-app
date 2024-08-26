from fastapi import FastAPI

from routers import company

app = FastAPI()
app.include_router(company.router)


@app.get("/")
def health_check():
    return "Server is up and running"