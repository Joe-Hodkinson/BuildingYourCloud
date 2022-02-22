import asyncio
import nest_asyncio
from azure.eventhub.aio import EventHubProducerClient
from azure.eventhub import EventData
import json
from datetime import datetime
import random
import time
import requests
from requests.models import Response

x=0
while (x < 10):
    async def run():
        ## You need to update the line below with your connection string:
        producer = EventHubProducerClient.from_connection_string("Endpoint=sb://MYEVENTHUB.servicebus.windows.net/;SharedAccessKeyName=tado;SharedAccessKey=MYKEY=;EntityPath=tadohub", eventhub_name="tadohub")
        async with producer:
            # Get actual Tado Info
            time.sleep(15)
            response = requests.get("https://my.tado.com/api/v2/homes/MYHOMEID/zones/5/state?username=MYUSERNAME&password=MYPASSWORD")     
            json_object = response.json()
            print(json_object["sensorDataPoints"]["insideTemperature"]["celsius"])
            t = (json_object["sensorDataPoints"]["insideTemperature"]["celsius"])

            # Create a batch.
            event_data_batch = await producer.create_batch()
            now = datetime.now()
            currenttime = now.strftime("%Y-%m-%dT%H:%M:%SZ")
            r = random.randint(1,100)
            a = random.randint(1,1000)

            # Add events to the batch.
            json_obj = {"deviceId":"1234567890","temp":r,"airquality":a,"actual":t,"timestamp":currenttime}
            body2= json.dumps(json_obj)
            event_data_batch.add(EventData(body2))


            # Send the batch of events to the event hub.
            await producer.send_batch(event_data_batch)

    x = x+ 1
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
