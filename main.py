# micro service for translation api

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import settings

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
    # production url, confirm using the right ip address, update to contabo ip address
    # uvicorn.run("main:app", host="159.89.87.57", port=7013, reload=True)

    """
    development port and url http://localhost:7013, confirm using the right ip address, update to contabo ip 
    address on production 
    """
    uvicorn.run("main:app", host="127.0.0.1", port=7013, reload=True)
