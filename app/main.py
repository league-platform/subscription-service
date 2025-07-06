from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson.objectid import ObjectId
import os

app = FastAPI()
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
client = AsyncIOMotorClient(MONGO_URI)
db = client["subscriptions_db"]
collection = db["subscriptions"]

class Subscription(BaseModel):
    user: str
    plan: str
    amount: float

@app.post("/subscriptions")
async def create_subscription(subscription: Subscription):
    result = await collection.insert_one(subscription.dict())
    print("EVENT: subscription.created ->", result.inserted_id)
    return {"message": "Subscription created", "id": str(result.inserted_id)}

@app.get("/subscriptions")
async def list_subscriptions():
    subs = []
    async for s in collection.find():
        s["_id"] = str(s["_id"])
        subs.append(s)
    return subs
