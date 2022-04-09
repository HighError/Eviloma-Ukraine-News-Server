import datetime
import os

import pymongo
from bs4 import BeautifulSoup
from markdown import markdown
from telethon import TelegramClient
from telethon.sessions import StringSession


async def update_telegram():
    # Connect to MongoDb
    mongo_client = pymongo.MongoClient(os.getenv('MONGO'))
    mongo_db = mongo_client["ukraine_news"]

    # Connect to Collections
    mongo_collection_channels = mongo_db["channels"]
    mongo_collection_posts = mongo_db["posts"]

    # Get channels list from DB
    channels = list(mongo_collection_channels.find())

    # Check if channels length == 0 - return
    if len(channels) == 0:
        return

    # Get posts from telegram
    telegram_client = TelegramClient(StringSession(os.getenv("TELEGRAM_SESSION")), int(os.getenv("TELEGRAM_API_ID")),
                                     os.getenv("TELEGRAM_API_HASH"))

    count = 0
    await telegram_client.start()
    async with telegram_client:
        # Get DateTime now - 30 minutes
        date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=32)
        for channel in channels:
            if channel["social"] == "telegram":
                # Update avatar
                # temp = await telegram_client.download_profile_photo(channel["channel_id"])
                #
                # with open(temp, 'rb') as image:
                #     photo = base64.b64encode(image.read())
                #     mongo_collection_channels.update_one({'channel_id': channel["channel_id"]},
                #                                          {"$set": {"avatar": photo}})
                #
                # os.remove(temp)

                async for message in telegram_client.iter_messages(channel["channel_id"], offset_date=date, reverse=True):
                    if message.text == "":
                        # If message text empty miss post
                        continue
                    if mongo_collection_posts.count_documents(
                            {'social': 'telegram', 'channel_id': channel["channel_id"], 'message_id': message.id}) == 0:
                        # Parse markdown
                        html = markdown(message.text)
                        text = "".join(BeautifulSoup(html, "html.parser").findAll(text=True))

                        # Generate post data
                        post = {
                            "social": 'telegram',
                            "channel_id": channel["channel_id"],
                            "message_id": message.id,
                            "message": text,
                            "date": message.date,
                            "url": f"{channel['link']}/{message.id}"
                        }

                        # Put data to db
                        mongo_collection_posts.insert_one(post)
                        count += 1

    return f"[LOG]: Successfully added {count} posts from telegram!"
