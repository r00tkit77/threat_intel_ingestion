from OTXv2 import OTXv2
from datetime import datetime, timezone
import requests
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


#OTX API

API_KEY = ""   #Enter here
otx = OTXv2(API_KEY)


#Splunk HEC

SPLUNK_HEC_URL = f""   #Enter here
SPLUNK_TOKEN = ""   #Enter here
HEADERS = {
    "Authorization": f"Splunk {SPLUNK_TOKEN}",
    "Content-Type": "application/json"
}


#Pulse Processing

pulses = otx.getsince("2026-03-08T00:00:00")   #Change this
seen_iocs = set()

for pulse in pulses:

    pulse_name = pulse.get("name")
    tags = pulse.get("tags", [])

    for indicator in pulse.get("indicators", []):

        ioc_type = indicator.get("type")
        ioc_value = indicator.get("indicator")

        key = (ioc_type, ioc_value)   #Deduplicate
        if key in seen_iocs:
            continue
        seen_iocs.add(key)

        now = datetime.now(timezone.utc)

        event_data = {
            "timestamp": now.isoformat(),
            "source": "OTX",
            "pulse_name": pulse_name,
            "ioc_type": ioc_type,
            "ioc_value": ioc_value,
            "tags": tags
        }

        payload = {
            "time": int(now.timestamp()),
            "host": "otx-ingestor",
            "source": "otx",
            "sourcetype": "otx:ioc",
            "event": event_data
        }

        try:
            response = requests.post(
                SPLUNK_HEC_URL,
                headers=HEADERS,
                json=payload,
                verify=False,
                timeout=5
            )

            if response.status_code != 200:
                print("Error:", response.text)

        except requests.exceptions.RequestException as e:
            print("Connection error:", e)
