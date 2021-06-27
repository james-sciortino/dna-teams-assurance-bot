# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
from datetime import datetime
import json
import ssl
import sys
import traceback
import uuid
from datetime import datetime
from http import HTTPStatus
from typing import Dict
import os
from aiohttp import web
from aiohttp.web import Request, Response, json_response
from botbuilder.core import (
    BotFrameworkAdapterSettings,
    TurnContext,
    BotFrameworkAdapter,
    CardFactory, 
    MessageFactory,
    conversation_reference_extension
)
from botbuilder.core.integration import aiohttp_error_middleware
from botbuilder.schema import Activity, ActivityTypes, ConversationReference, Attachment

from bots import ProactiveBot
from config import DefaultConfig

CONFIG = DefaultConfig()

# Create adapter.
# See https://aka.ms/about-bot-adapter to learn more about how bots work.
SETTINGS = BotFrameworkAdapterSettings(CONFIG.APP_ID, CONFIG.APP_PASSWORD)
ADAPTER = BotFrameworkAdapter(SETTINGS)


# Catch-all for errors.
async def on_error(context: TurnContext, error: Exception):
    # This check writes out errors to console log .vs. app insights.
    # NOTE: In production environment, you should consider logging this to Azure
    #       application insights.
    print(f"/n [on_turn_error] unhandled error: {error}", file=sys.stderr)
    traceback.print_exc()

    # Send a message to the user
    await context.send_activity("The bot encountered an error or bug.")
    await context.send_activity(
        "To continue to run this bot, please fix the bot source code."
    )
    # Send a trace activity if we're talking to the Bot Framework Emulator
    if context.activity.channel_id == "emulator":
        # Create a trace activity that contains the error object
        trace_activity = Activity(
            label="TurnError",
            name="on_turn_error Trace",
            timestamp=datetime.utcnow(),
            type=ActivityTypes.trace,
            value=f"{error}",
            value_type="https://www.botframework.com/schemas/error",
        )
        # Send a trace activity, which will be displayed in Bot Framework Emulator
        await context.send_activity(trace_activity)
CARDS = [os.getcwd() + "/1-template.json"]

ADAPTER.on_turn_error = on_error

# Create a shared dictionary.  The Bot will add conversation references when users
# join the conversation and send messages.
CONVERSATION_REFERENCES: Dict[str, ConversationReference] = dict()

# If the channel is the Emulator, and authentication is not in use, the AppId will be null.
# We generate a random AppId for this case only. This is not required for production, since
# the AppId will have a value.
APP_ID = SETTINGS.app_id if SETTINGS.app_id else uuid.uuid4()

# Create the Bot
BOT = ProactiveBot(CONVERSATION_REFERENCES)

# Listen for incoming requests on /api/messages.
async def messages(req: Request) -> Response:
    # Main bot message handler.
    if "application/json" in req.headers["Content-Type"]:
        body = await req.json()
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE) 
    activity = Activity().deserialize(body)

    auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""

    response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    if response:
        return json_response(data=response.body, status=response.status)
    return Response(status=HTTPStatus.OK)

def _create_adaptive_card_attachment(event, index) -> Attachment:
    card_path = os.path.join(os.getcwd(), CARDS[index])
    with open(card_path, "rb") as in_file:
        card_data = json.load(in_file)
        realtime = datetime.fromtimestamp(event["timestamp"]/1000)
        event_time = realtime.strftime("%x-%X") # Set  data and time format 
        
        for condition in event:
            print(condition["details"]["Assurance Issue Status"])
            if condition["details"]["Assurance Issue Status"] == "active":
                if condition["details"]["Assurance Issue Category"] == "availability":
                    if condition["severity"] == (1 or 2):
                        color = "red"

            elif condition["details"]["Assurance Issue Status"] == "active":
                if condition["details"]["Assurance Issue Category"] == "availability":
                    if condition["severity"] == (1 or 2):
                        color = "red"

            else:
                color = "red"
        card_data["body"][1]["columns"][1]["items"][1]["text"] = ("Time: " + str(event_time))
        card_data["body"][3]["text"] = ("Assurance Issue Details: " + event["details"]["Assurance Issue Details"])
        card_data["body"][4]["text"] = ("Assurance Issue Priority: " + event["details"]["Assurance Issue Category"])
        card_data["body"][5]["text"] = ("Device: " + event["details"]["Device"])
        card_data["body"][6]["text"] = ("Assurance Issue Name: " + event["details"]["Assurance Issue Name"])
        card_data["body"][7]["text"] = ("Assurance Issue Category: " + event["details"]["Assurance Issue Category"])
        card_data["body"][8]["text"] = ("Assurance Issue Status: " + event["details"]["Assurance Issue Status"])
        card_data["actions"][0]["url"] = event["ciscoDnaEventLink"]
    
    return CardFactory.adaptive_card(card_data)

# Listen for incoming requests on /api/assurance.
async def assurance(req: Request) -> Response:
    if "application/json" in req.headers["Content-Type"]:
        test = await req.text()
        r = test.replace("None",'"Empty"')
        body = json.loads(r)
        print(body)
        
    else:
        return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

  #  if "application/json" in req.headers["Content-Type"]:
  #      body = await req.json()
  #      print(body)
  #      print(type(body))
  #  else:
  #      return Response(status=HTTPStatus.UNSUPPORTED_MEDIA_TYPE)

    #activity = Activity().deserialize(body)
    #auth_header = req.headers["Authorization"] if "Authorization" in req.headers else ""
    #response = await ADAPTER.process_activity(activity, auth_header, BOT.on_turn)
    #if response:
        #return json_response(data=response.body, status=response.status)

    await _send_proactive_message(body)
    return Response(status=HTTPStatus.OK)

# Listen for requests on /api/notify, and send a messages to all conversation members.
async def notify(req: Request) -> Response:  # pylint: disable=unused-argumentTSH
    await _send_proactive_message()
    return Response(status=HTTPStatus.OK, text="Proactive messages have been sent")

# Send a message to all conversation members.
# This uses the shared Dictionary that the Bot adds conversation references to.
async def _send_proactive_message(event):
    message = Activity(
        text="Assurance Alert!",
        type=ActivityTypes.message,
        attachments=[_create_adaptive_card_attachment(event, 0)])

    for conversation_reference in CONVERSATION_REFERENCES.values():
        await ADAPTER.continue_conversation(
            conversation_reference,
            lambda turn_context: turn_context.send_activity(message),
            APP_ID,
            )

#APP = web.Application(middlewares=[aiohttp_error_middleware])
APP = web.Application(middlewares=None)
APP.router.add_post("/api/messages", messages)
APP.router.add_get("/api/notify", notify)
APP.router.add_post("/api/assurance", assurance)

if __name__ == "__main__":
    sslcontext = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
    sslcontext.load_cert_chain(os.getcwd() + "/server.crt", os.getcwd() + "/server.key")
    try:
        web.run_app(APP, host="0.0.0.0", port=CONFIG.PORT, ssl_context=sslcontext)
    except Exception as error:
        raise error

