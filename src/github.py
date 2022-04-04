import json

import requests

url = "https://api.github.com/repos/HighError/Eviloma-Ukraine-News-Client/releases"


async def get_release():
    request = requests.get(url).json()
    for files in request[0]["assets"]:
        if files["content_type"] == "application/vnd.android.package-archive":
            return json.dumps({
                "version": request[0]["name"],
                "link": files["browser_download_url"]
            })