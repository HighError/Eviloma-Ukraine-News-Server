import json
import os

import requests

base_url = "https://api.codemagic.io"


async def get_latest_build_json(app_type):
    headers = {'X-Auth-Token': os.getenv('CODEMAGIC_API')}
    request = requests.get(f"https://api.codemagic.io/builds?appId={os.getenv('CODEMAGIC_APP_ID')}",
                           headers=headers).json()

    if len(request["builds"]) == 0:
        return {
            "version": "",
            "link": ""
        }
    for build in request["builds"][0]["artefacts"]:
        if build["type"] == app_type:
            return {
                "version": build["versionName"],
                "link": build["url"]
            }
