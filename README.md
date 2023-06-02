***NOTE: Open this file in markdown preview editor to have clear understanding of the content***

### Prerequistes : python3

## Steps
- cd to `driving_alerts_rule_engine/` directory.
- Run ***`python3 -m pip install flask`*** command to install flask.
- run ***`export FLASK_ENV=development`*** in terminal in order to run the server in development mode. 
- Execute ***`python3 -m flask run`*** to start the flask app server from the directory where `app.py` is present.
- Import the collections into postman by importing `driving_alerts.postman_collection.json` 
- create 3 events first within 5 mins timeframe to generate an alert.

<br>

## Endpoints
<br>

**BASE URL = http://127.0.0.1:5000**
returns "I keep track of bad driving incidents"

<br>

1. ***POST: /event***
- This api expect a input of request payload in the below mentioned format to uplaod the events to database.
```json
{
        "timestamp": "2023-05-24T05:55:00+00:00",
        "is_driving_safe": true
}
```
- For simplicity purpose we are running the rule for every packet from 3rd packet onwards.
- This can be converted into an async task which runs in the background without interrupting the execution of the update event.
<br>

2. ***GET: alert/<alert_id>***
- This api returns the alert information for the specified **<alert_id>**

<br>

3. ***GET : /all_alerts***
- This api returns all the alerts that has been created by the rule engine till this point of time.