from pyrogram import Client

from config import API_ID, API_HASH

app = Client(
    "session", api_id=API_ID, api_hash=API_HASH
)
app.start()