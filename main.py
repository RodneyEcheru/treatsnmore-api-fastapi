# micro service for translation api

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

import ugandaui
import rwandaui
import kenyaui
import navbar
import website
import translate
import category
import product
import notification

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

app.include_router(ugandaui.api)
app.include_router(rwandaui.api)
app.include_router(kenyaui.api)
app.include_router(website.api)
app.include_router(navbar.api)
app.include_router(category.api)
app.include_router(product.api)
app.include_router(translate.api)
app.include_router(notification.api)


@app.get("/")
def welcome():
    return {"message": "You have reached the treatsnmore api, Please specify the resources I can serve you"}


if __name__ == "__main__":
    host = "0.0.0.0"  # 62.171.141.19
    port = 7013  # Use PORT from PM2, default to 7013
    uvicorn.run("main:app", host=host, port=port, reload=True)  # reload=False for production


# if __name__ == "__main__":
#     uvicorn.run("main:app", host="185.217.127.125", port=2001, reload=True)
#     #uvicorn.run("main:app", host="127.0.0.1", port=7012, reload=True)
