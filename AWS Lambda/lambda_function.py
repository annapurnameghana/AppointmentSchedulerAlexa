# -- coding: utf-8 --

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta

scope = ["https://www.googleapis.com/auth/calendar"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
API_NAME = 'calendar'
API_VERSION = 'v3'

# google calendar service
service = build(API_NAME, API_VERSION, credentials=creds)

calendar_id = "5c8c54f12f19973c10d714e7dceef8c8b65b3965b2b491dd24b2ee74728fbc2b@group.calendar.google.com"

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Welcome, you can book your appointment!!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

        
        
class ScheduleIntentHandler(AbstractRequestHandler):
    """Handler for Scheduler Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ScheduleIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        date = str(slots["date"].value)
        time = str(slots["time"].value)
        reason = str(slots["reason"].value)
        nn = int(slots["nn"].value)
        dateSlot = datetime.strptime(date, "%Y-%m-%d")
        hour = int(time.split(":")[0])
        mins = int(time.split(":")[1])
        time_min = datetime(dateSlot.year, dateSlot.month, dateSlot.day, hour, mins)
        time_max = time_min + timedelta(hours=nn)
        if check_free_busy(time_min, time_max):
            reserve_appointment(time_min, time_max,reason)
            
            speak_output = f"Your appointment on {date} at {time} for {reason} for {nn} hours is successfully scheduled."
        else :
            speak_output = f"Sorry, the selected time is not available. Please choose a different time."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


        
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Single handler for Fallback Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
        speech = "Hmm, I'm not sure. You can say Hello or Help. What would you like to do?"
        reprompt = "I didn't catch that. What can I help you with?"

        return handler_input.response_builder.speak(speech).ask(reprompt).response

class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(ScheduleIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()

import pytz
from datetime import datetime, timedelta

def reserve_appointment(time_min, time_max,reason):
    # Specify the time zone as IST
    timezone = pytz.timezone('Asia/Kolkata')

    # Convert the start and end times to IST
    time_min_ist = time_min.astimezone(timezone)
    time_max_ist = time_max.astimezone(timezone)

    event = {
        'summary': reason,
        'description': "description test",
        'start': {
            'dateTime': time_min_ist.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': time_max_ist.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': 'Asia/Kolkata',
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
                {'method': 'popup', 'minutes': 30},
            ],
        },
    }

    service.events().insert(calendarId=calendar_id, body=event).execute()


import logging

import pytz
from datetime import datetime

import pytz
from datetime import datetime

def check_free_busy(time_min, time_max):
    try:
        # Convert time_min and time_max to IST timezone
        ist_timezone = pytz.timezone('Asia/Kolkata')
        time_min_ist = time_min.astimezone(ist_timezone)
        time_max_ist = time_max.astimezone(ist_timezone)
        
        calendar_id = "5c8c54f12f19973c10d714e7dceef8c8b65b3965b2b491dd24b2ee74728fbc2b@group.calendar.google.com"

        free_busy_query = {
            'timeMin': time_min_ist.isoformat(),
            'timeMax': time_max_ist.isoformat(),
            'timeZone': 'Asia/Kolkata',
            'items': [{'id': calendar_id}]
        }
        response = service.freebusy().query(body=free_busy_query).execute()
        calendars = response.get('calendars', {})
        calendar = calendars.get(calendar_id, {})
        busy_slots = calendar.get('busy', [])
        return len(busy_slots) == 0
    except Exception as e:
        logging.error(f"Error querying free/busy: {str(e)}")
        return False





def can_schedule_appointment(time_min, time_max):
    return check_free_busy(time_min, time_max)



def schedule_appointment(time_min, time_max):
    if can_schedule_appointment(time_min, time_max):
        reserve_appointment(time_min, time_max)
        return True
    return False