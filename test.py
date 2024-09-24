import logging
from grpc_requests import Client
import fastapi
import random
import time

    

if __name__ == "__main__":
    vehicles = ["HT2028",
"395#1",
"HT2026",
"HT2048",
"HT2035"]
    # while 1:
request_data = {
  "namespace": "dev",
  "table": "entities",
  "event": {
    "emZoneUpdate": {
      "deviceId": random.choice(vehicles),
      "position": {
        "x": 653736.77 + random.uniform(-100, 100),
        "y": 4447456.64 + random.uniform(-100, 100),
        "z": -136.4 + random.uniform(-5, 5)
      },
      "zone": [
        {
          "zoneId": "tumee-test",
          "status": "INSIDE",
          "namelom": "N1-9HLL-HD01-VC01"
        }
      ]
    }
  }
}
client = Client.get_by_endpoint('localhost:8001')
print(client.service_names[0])
res = client.request('transaction_service.TransactionService', 'ApplyEvent', request_data)
time.sleep(1)

def send_request(request, client):
  res = client.request('transaction_service.TransactionService', 'ApplyEvent', request_data)
  time.sleep(1)
   