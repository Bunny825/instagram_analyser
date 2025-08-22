import requests
import json

ig_user_id       = "17841440146948099"
app_id           = "1180764653878942"
app_secret       = "3057f1b060decd7a99020e3d14131a80"
user_access_token = "EAAQx5jHBZCp4BPHtJ19R6vDZAfuM3qoZBfRrBVzGz1azobmSsVf0MySKV0M9ZAYITbmrp1JZCZB4VfVhBFBZB4bD6epekcAoEC7ECi6TVkBS9PjXH7N7bznU74mZCSrPUOxGGHNlcPSPz4S3c6RDaWcuu3qGDPLvWjw3q2fp6fhZARciiO0pBegNUO9CVPLbBnlwl5wZDZD"


url = f"https://graph.facebook.com/v17.0/oauth/access_token?grant_type=fb_exchange_token&client_id={app_id}&client_secret={app_secret}&fb_exchange_token={user_access_token}"
response = requests.get(url)
#print(response.content)
long_access_token = response.json()["access_token"]
print(long_access_token)