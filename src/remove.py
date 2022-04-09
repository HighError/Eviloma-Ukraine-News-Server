import os

import pymongo
import datetime


async def remove_old_data():
    # Connect to MongoDb
    mongo_client = pymongo.MongoClient(os.getenv('MONGO'))
    mongo_db = mongo_client["ukraine_news"]

    # Connect to Collections
    mongo_collection_posts = mongo_db["posts"]

    date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=1440)

    query = {"date": {"$lte": date}}
    x = mongo_collection_posts.delete_many(query)
    print(x.deleted_count, " documents deleted.")
