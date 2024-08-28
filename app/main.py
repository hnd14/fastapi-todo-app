from fastapi import FastAPI

from routers import company, auth, user

app = FastAPI()
app.include_router(company.router)
app.include_router(auth.router)
app.include_router(user.router)


@app.get("/")
def health_check():
    return "Server is up and running"