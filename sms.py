from fastapi import APIRouter
import requests

api = APIRouter(
    prefix="/sms",
    tags=["sms"],
    responses={404: {"message": "Request for a valid sms resource"}}
)


# send sms
async def send(sms):

    url = 'http://boxuganda.com/api.php'
    myobj = {'user': 'ivilleinc','password':'ivi11einc','sender':'Treatsnmore','message':sms["message"],'reciever':sms["reciever"]}

    response = requests.post(url, data=myobj)

    # response from sms
    return response.json()


@api.get("/")
async def method():
    return {
        "status": "info",
        "message": "You have reached the sms api, specify the resources I can serve you",
        "data_status": False,
    }

