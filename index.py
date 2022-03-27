import asyncio
import json
import os
import pymongo
import logging
from flask import Flask, Response, request, redirect
from flask_cors import CORS
from src.telegram import update_telegram
from src.github import get_release
from bson.json_util import dumps
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app)


@app.route("/")
def index():
    return Response("", status=204, mimetype="application/json")


@app.route("/app")
def get_app_xml():
    return Response("", status=204, mimetype="application/json")


@app.route("/update")
def update():
    # agent = request.headers.get("User-Agent")
    # need_agent = "Mozilla/5.0+(compatible; UptimeRobot/2.0; http://www.uptimerobot.com/)"
    # if not (agent == need_agent):
    #     return Response("", status=403, mimetype="application/json")

    try:
        msg = asyncio.run(update_telegram())
    except Exception as e:
        print(f'Telegram update error: {e}')
        app.logger.error("Telegram not parse!")
        return Response("", status=500, mimetype="application/json")

    app.logger.info(msg)
    return Response("", status=200, mimetype="application/json")


@app.route("/get/posts")
def get_posts():
    mongo_client = pymongo.MongoClient(os.getenv('MONGO'))
    mongo_db = mongo_client["ukraine_news"]
    mongo_collection_posts = mongo_db["posts"]

    posts = dumps(list(mongo_collection_posts.find()), ensure_ascii=False)
    # "GET /data HTTP/1.1" 200 201141 "-" "Dart/2.16 (dart:io)"
    return Response(posts, status=200, mimetype='application/json; charset=utf-8')


@app.route("/get/channels")
def get_channels():
    mongo_client = pymongo.MongoClient(os.getenv('MONGO'))
    mongo_db = mongo_client["ukraine_news"]
    mongo_collection_channels = mongo_db["channels"]

    # channels = dumps(list(mongo_collection_channels.find()), ensure_ascii=False)
    channels = list(mongo_collection_channels.find())
    for channel in channels:
        if 'avatar' in channel:
            image = channel['avatar']
            decode = image.decode('utf-8')
            del (channel['avatar'])
            channel['avatar'] = decode
    json = dumps(channels, ensure_ascii=False)
    return Response(json, status=200, mimetype='application/json; charset=utf-8')


@app.route("/get/socials")
def get_socials():
    mongo_client = pymongo.MongoClient(os.getenv('MONGO'))
    mongo_db = mongo_client["ukraine_news"]
    mongo_collection_socials = mongo_db["socials"]

    socials = dumps(list(mongo_collection_socials.find()), ensure_ascii=False)
    return Response(socials, status=200, mimetype='application/json; charset=utf-8')


@app.route("/app/apk")
def apk():
    apk_link = asyncio.run(get_release())
    data = json.dumps({
        "version": "0.1.0",
        "link": apk_link
    })
    return Response(data, status=200, mimetype="application/json")


@app.route("/app/apk/download")
def apk_download():
    apk_link = asyncio.run(get_release())
    return redirect(apk_link)
