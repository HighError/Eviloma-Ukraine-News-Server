import os

import pymongo
import requests
import datetime


async def update_twitter():
    api = os.getenv("TWITTER_API")

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

    # Get DateTime now - 15 minutes and set in request params
    date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=17)
    date_string = date.strftime("%Y-%m-%d") + "T" + date.strftime("%H:%M:%S") + "Z"
    params = {"start_time": date_string, 'tweet.fields': 'created_at', 'exclude': 'retweets,replies', 'expansions': 'attachments.media_keys', 'media.fields': 'type,url'}

    for channel in channels:
        if channel["social"] == "Twitter":
            response = requests.get(f'https://api.twitter.com/2/users/{channel["channel_id"]}/tweets', headers={
                'Authorization': api}, params=params).json()
            if not ('meta' in response):
                continue

            if not ('result_count' in response['meta']):
                continue

            if response['meta']['result_count'] <= 0:
                continue

            data = response['data']

            for post in data:

                if mongo_collection_posts.count_documents(
                        {'social': 'Twitter', 'channel_id': channel["channel_id"], 'message_id': post['id']}) == 0:

                    medias = []

                    if 'attachments' in post:
                        if 'media_keys' in post['attachments']:
                            if len(post['attachments']['media_keys']) > 0:
                                for media_key in post['attachments']['media_keys']:
                                    for media in response['includes']['media']:
                                        if media_key == media['media_key']:
                                            if media['type'] == 'photo':
                                                medias.append(media['url'])

                    post_data = {
                        'social': 'Twitter',
                        'channel_id': channel['channel_id'],
                        'message_id': post['id'],
                        'message': post['text'],
                        'date': date.strptime(post['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                        'url': channel['link'] + '/status/' + post['id'],
                        'images': medias
                    }

                    mongo_collection_posts.insert_one(post_data)
