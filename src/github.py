import requests


async def get_release():
    request = requests.get(f"https://api.github.com/repos/HighError/Eviloma-Ukraine-News-Client/releases").json()
    for files in request[0]["assets"]:
        if files["content_type"] == "application/vnd.android.package-archive":
            return files["browser_download_url"]