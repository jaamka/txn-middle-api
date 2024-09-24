import os
import json
import traceback
from fastapi import FastAPI, Request
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from grpc_requests import Client
from grpc import RpcError

app = FastAPI()
load_dotenv()
origins = os.environ.get('ALLOWED_ORIGINS') or ""
if len(origins) !=0:
    origins = origins.replace(", ", ",").split(",")
txn_endpoint = os.environ.get('TXN_ENDPOINT') or '127.0.0.1:8001'
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def status_check():
    return {
        "statusCode": 200,
        "statusMessage" : "OK"
    }


@app.post("/transaction/apply_event")
async def applyEvent(request: Request):
    try:
        client = request.client.host
        method = request.method
        txn_client = Client.get_by_endpoint(txn_endpoint)
        print('Received request client: %s, method: %s', client, method)
        item = await request.body()
        item = json.loads(item)
        print(item)
        
        res = txn_client.request(txn_client.service_names[0], 'ApplyEvent', item)
        return {
            "statusCode": 200, "message": res
        }
    except RpcError as rpc_error:
        traceback.print_exc()
        print('[Error] in txn endpoint: %s', rpc_error)
        return {"statusCode": 500, "error": "[Error] Txn engine endpoint"}
    except Exception as e:
        traceback.print_exc()
        print('[Error] applying event: %s', e)
        return {"statusCode": 500, "error": "[Error] Server error"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=2000)