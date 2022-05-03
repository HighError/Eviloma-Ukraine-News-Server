import facebook_scraper
import os

import pymongo
from facebook_scraper import *
from facebook_scraper import _scraper
import pytz


async def update_facebook():
    set_user_agent("Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)")

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

    for channel in channels:
        if channel["social"] == "Facebook":
            for post in get_posts(channel["channel_id"], pages=3):
                if mongo_collection_posts.count_documents(
                        {'social': 'Facebook', 'channel_id': channel['channel_id'],
                         'message_id': post['post_id']}) == 0:
                    post_data = {
                        'channel_id': channel['channel_id'],
                        'date': post['time'].astimezone(pytz.utc),
                        'message_id': post['post_id'],
                        'message': post["text"],
                        'social': 'Facebook',
                        'url': post['post_url'],
                        'images': post['images'],
                    }
                    mongo_collection_posts.insert_one(post_data)
