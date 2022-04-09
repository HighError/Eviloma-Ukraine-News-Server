import requests
import datetime

api = "Bearer AAAAAAAAAAAAAAAAAAAAACUvaQEAAAAAdk9yw2RRtnQPE16UN7BpU9UCgok" \
      "%3DuFSw5Lpdyr810z8ALOFCAzQ4spVtFo6lIPsPCchilb4jCpIcTe "


def main():
    date = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(minutes=999999)
    date_string = date.strftime("%Y-%m-%d") + "T" + date.strftime("%H:%M:%S") + "Z"
    params = {"start_time": date_string}

    response = requests.get('https://api.twitter.com/2/users/732521058507620356/tweets', headers={
        'Authorization': api}, params=params).json()

    # if "data" in response:
    #     for post in response["data"]:
    #         print(post)
    #         post = {
    #             "social": 'tweeter',
    #             "channel_id": post["channel_id"],
    #             "message_id": message.id,
    #             "message": text,
    #             "date": message.date,
    #             "url": f"{channel['link']}/{message.id}"
    #         }


if __name__ == '__main__':
    main()
