from fastapi import FastAPI

from api.routers import main_router

app = FastAPI(
    title="MedKitAPI",
    version="0.0.1",
)
app.include_router(main_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=777)
