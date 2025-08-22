import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

INSTAGRAM_API_VERSION="v19.0"
INSTAGRAM_BUSINESS_ACCOUNT_ID="17841440146948099"
MOCK_DATA_PATH='backend/data/example_channel.json'

def safe_read_json(file_path:str)->dict|None:
    try:
        with open(file_path,'r',encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError,json.JSONDecodeError) as e:
        print(f"Error with JSON file at {file_path}:{e}")
        return None

def safe_write_json(data:dict,file_path:str)->bool:
    try:
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w',encoding='utf-8') as f:
            json.dump(data,f,indent=4)
        return True
    except (TypeError,OSError) as e:
        print(f"Error with JSON file at {file_path}:{e}")
        return False

def get_instagram_data(channel_name:str)->dict|None:
    api_token=os.getenv("INSTAGRAM_API_TOKEN")
    if not api_token:
        print("INSTAGRAM_API_TOKEN not found,using mock data.")
        return safe_read_json(MOCK_DATA_PATH)

    fields="username,followers_count,media{caption,like_count,comments_count,id}"
    url=(
        f"https://graph.facebook.com/{INSTAGRAM_API_VERSION}/{INSTAGRAM_BUSINESS_ACCOUNT_ID}"
        f"?fields={fields}&access_token={api_token}"
    )
    try:
        response=requests.get(url,timeout=30)
        response.raise_for_status()
        api_data=response.json()
        formatted_data={
            "profile":{
                "username":api_data.get("username"),
                "followers_count":api_data.get("followers_count"),
            },
            "posts":[
                {
                    "id":post.get("id"),
                    "caption":post.get("caption","No caption available."),
                    "likes_count":post.get("like_count", 0),
                    "comments_count":post.get("comments_count", 0),
                }
                for post in api_data.get("media",{}).get("data",[])
            ],
        }
        return formatted_data
    except requests.exceptions.RequestException as e:
        print(f"Instagram API call failed:{e},using mock data.")
        return safe_read_json(MOCK_DATA_PATH)