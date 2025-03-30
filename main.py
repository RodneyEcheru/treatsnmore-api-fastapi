# micro service for translation api

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import settings
import os

# initialise global settings
settings.init()

# initialise app
app = FastAPI()

# register CORS / allow sites to access api
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    import time
    start_time = time.time()

    print(settings.global_values['localhost'])

    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)

    return response


@app.get("/")
def welcome():
    return {"message": "You have reached the treatsnmore api, Please specify the resources I can serve you"}


if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")  # Use HOST from PM2, default to 0.0.0.0
    port = int(os.getenv("PORT", "7013"))  # Use PORT from PM2, default to 7013
    uvicorn.run("main:app", host=host, port=port, reload=True)  # reload=False for production
