from fastapi import APIRouter, Request, BackgroundTasks

import emailsapi
import orm
import sms

api = APIRouter(
    prefix="/notification",
    tags=["notification"],
    responses={404: {"message": "Request for a valid notification resource"}}
)


@api.get("/")
async def method():
    return {
        "status": "info",
        "message": "You have reached the notification api, specify the resources I can serve you",
        "data_status": False,
    }


@api.post("/notifyme")
async def method(request: Request, background_tasks: BackgroundTasks):

    # get form data
    form_data = await request.form()

    # validate form

    # require quantity
    if not(form_data["quantity"].strip() and int(form_data["quantity"].strip())):
        return {
            "status": "validation_error",
            "message": "Please Enter your desired quantity"
        }

    # require quantity
    if not(form_data["product_id"] and int(form_data["product_id"].strip())):
        return {
            "status": "validation_error",
            "message": "Please select a product"
        }

    # require name
    if not(form_data["name"].strip()):
        return {
            "status": "validation_error",
            "message": "Please Enter your name"
        }

    # require email
    if not(form_data["email"].strip()):
        return {
            "status": "validation_error",
            "message": "Please Enter your email"
        }

    # require phone
    if not(form_data["phone"] and form_data["phone"].strip()):
        return {
            "status": "validation_error",
            "message": "Please Enter your phone"
        }

    # validate email address
    if await emailsapi.is_valid(form_data["email"]) and await emailsapi.is_not_blacklisted(form_data["email"]):

        # fields to add: add_inventory_message_received_status
        formatted_data = await orm.format_dict(form_data)  # convert dict to assignable object & format int properties
        formatted_data["inventory_message_received_status"] = "no"

        # insert data into table
        notification_id = await orm.save("stockrequest", formatted_data)
        
        if notification_id:
        
            # send email notifications
            # background_tasks.add_task(write_notification, email, message="some notification")
            await emailsapi.notification_request(formatted_data)
        
            # send customer sms notifications
            await sms.send({
                "message": f"Hi {formatted_data['name']}, Treats N More {formatted_data['country']} has received your request for addition of {formatted_data['quantity']} {formatted_data['product_name']} (Details in email), Thanks for reaching out to us. Chat with us on 0200909059 in case you need assistance",
                "reciever": f"{formatted_data['phone']},0773185503,0700458811,0701793092,0771883513,0788860145"
            })            
            
            return { "status": "successful", "message": "Request received" }
        else:            
            return { "status": "validation_error", "message": "Request not received, Error occured, please try again" }
