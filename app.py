import time
from flask import Flask, request
from flask.json import jsonify
from dateutil import parser
from collections import deque
from datetime import datetime

app = Flask(__name__)

# List to store all alerts
ALERTS = {}

ALERT_COUNT = 1 # Integer to track alers
ALERT_DURATION_TIME = 300 # 5 * 60 Seconds i.e 5 Minutes
PREV_ALERT_TIME = None

EVENTS = deque([])


# ------------------------------------------ #

# Helper function

def convert_string_timestamp_to_epoch(string_timestamp):
    epoch = parser.parse(string_timestamp).timestamp()
    return int(epoch)

def convert_epoch_to_datetime(epoch_time):
    human_time = datetime.fromtimestamp(1347517370).strftime('%c')
    return human_time

def add_event_and_check_for_alert(epoch_time):
    global ALERT_COUNT

    print("DEBUG", "BEFORE", EVENTS, len(EVENTS))

    events_count = len(EVENTS)

    if events_count < 2:
        EVENTS.append(epoch_time)
        return None # Adding event

    else:
        if events_count == 3:
            EVENTS.popleft()

        EVENTS.append(epoch_time)
    
    print("DEBUG", EVENTS, len(EVENTS))

    # time difference between current event and 3rd event including current
    delta_time = epoch_time - EVENTS[0]
    print("DEBUG", EVENTS[0], delta_time)
    
    # Current alert time will be equal to event time
    current_alert_time = epoch_time 

    # Generating alert only if no alert generated in past 5 mins and
    # 3 unsafe driving events happened in the same duration

    if PREV_ALERT_TIME == None: # First alert
        alert_generated_in_5_mins = False
    else:
        if current_alert_time-PREV_ALERT_TIME > ALERT_DURATION_TIME:
            alert_generated_in_5_mins = True

    # Storing alert data into db
    if alert_generated_in_5_mins is False and  delta_time <= ALERT_DURATION_TIME:
        alert_id = f"alert_{ALERT_COUNT}"
        ALERTS[alert_id] = {
            "alert_creation_time": convert_epoch_to_datetime(current_alert_time),
            "event_1_time": convert_epoch_to_datetime(EVENTS[0]), 
            "event_2_time": convert_epoch_to_datetime(EVENTS[1]),
            "event_3_time": convert_epoch_to_datetime(EVENTS[2])
        }
        print(f"Alert generated with ALERT_ID:{alert_id} at {current_alert_time}")
        ALERT_COUNT += 1

# ------------------------------------------ #

@app.route("/")
def index():
    return "<h1>I keep track of bad driving incidents</h1>"


@app.route("/event", methods=('POST',))
def event():
    """
    Takes timestamp and is_driving_safe flag in request param
    checks for previous unsafe driving event and generates alert if there
    are more than 3 unsafe driving events in less than 5 minutes 

    Request Sample:

    {
        "timestamp": "2023-05-24T05:55:00+00:00",
        "is_driving_safe": true
    }

    """
    try:
        event_data = request.json

        timestamp = event_data.get('timestamp')
        is_driving_safe = event_data.get('is_driving_safe')

        if timestamp is None and is_driving_safe is None:
            return f"timestamp and is_driving_safe are mandatory parameters"
        
        epoch_time = convert_string_timestamp_to_epoch(timestamp)
        
        if is_driving_safe is False:
            add_event_and_check_for_alert(epoch_time)

        return f"event recorded at {timestamp}"
    
    except Exception as e:
        return f"Error in saving event data. Exc: {e}"



@app.route("/alert/<alert_id>", methods=('GET',))
def get_alert(alert_id):
    try:
        if alert_id not in ALERTS.keys():
            return f"Invalid alert_id:{alert_id}, pick from {ALERTS.keys()}"
        
        return jsonify(ALERTS[alert_id])

    except Exception as e:
        return f"Error in getting alert data for {alert_id}"


@app.route("/all_alerts", methods=('GET',))
def get_all_alerts():
    try:
        return ALERTS
    except Exception as e:
        return "Error while getting all alerts"

if __name__ == "__main__":
    pass # Driver function 