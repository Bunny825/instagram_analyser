import requests
import json
ig_user_id=17841440146948099
long_access_token="EAAQx5jHBZCp4BPIuwwRZC80iF1vB0xpJh2Ai0arDLtps8kGyGbYqJ1wd7pn52fYRVuLfswoKnZCuA0oZAlZAJyRdG43OPhX4pglIt6wsjktYOs3ZCJu4ZCapVzpm0bGvaHAgSZCWXm1XHQEMeP5TMUZB2Em5k68iJr7oxJLGZC09MyrCZCHBXB4sTDoOZAk0UGjZA"
username = "chinnibaladityasai"
required_param = "followers_count,media_count"
url = f"https://graph.facebook.com/v17.0/{ig_user_id}?fields=business_discovery.username({username}){{{required_param}}}&access_token={long_access_token}"
response = requests.get(url)
metadata = response.json()
#print(response.json())
followers_count = metadata["business_discovery"]["followers_count"]
media_count = metadata["business_discovery"]["media_count"]
print(json.dumps(metadata, indent=4))