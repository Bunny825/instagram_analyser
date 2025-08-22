import json
import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles

from .ai import generate_text, generate_image
from .models import CollectDataRequest,RecommendationResponse,SummaryResponse,ThumbnailRequest
from .utils import get_instagram_data, safe_read_json, safe_write_json

app=FastAPI(
    title="Instagram Channel Analyzer API",
    description="An API that analyzes Instagram data and provides AI-powered content recommendations",
)

os.makedirs("backend/outputs", exist_ok=True)
app.mount("/outputs",StaticFiles(directory="backend/outputs"),name="outputs")

CHANNEL_DATA_PATH = "backend/data/channel_data.json"

@app.get("/health")
def health_check():
    return {"status":"ok"}

@app.get("/metrics")
def get_metrics():
    return {"info":"Metrics tracking can be implemented here."}

@app.post("/collect-data")
def collect_data(request:CollectDataRequest):
    data=get_instagram_data(request.channel_name)
    if not data:
        raise HTTPException(status_code=404,detail="Could not retrieve channel data.")

    if not safe_write_json(data,CHANNEL_DATA_PATH):
        raise HTTPException(status_code=500,detail="Failed to write channel data")

    return {"message":f"Data for '{request.channel_name}' collected and stored."}

@app.get("/summarize",response_model=SummaryResponse)
def get_summary():
    channel_data = safe_read_json(CHANNEL_DATA_PATH)
    if not channel_data or "profile" not in channel_data:
        raise HTTPException(status_code=404,detail="Channel data not found.Please run data collection first.")

    profile=channel_data.get("profile",{})
    posts = channel_data.get("posts",[])
    prompt = f"""
    Analyze this Instagram account data and give me a concise performance summary.
    Focus on content strategy, engagement trends, and overall health.

    - Username: {profile.get("username", "N/A")}
    - Followers: {profile.get("followers_count", 0)}
    - Posts Analyzed: {len(posts)}
    - Total Likes: {sum(p.get("likes_count", 0) for p in posts)}
    - Total Comments: {sum(p.get("comments_count", 0) for p in posts)}

    Summary:
    """
    summary_text=generate_text(prompt)
    return SummaryResponse(summary=summary_text)

@app.get("/recommend", response_model=RecommendationResponse)
def get_recommendation():
    channel_data=safe_read_json(CHANNEL_DATA_PATH)
    if not channel_data or not channel_data.get("posts"):
        raise HTTPException(status_code=404,detail="No post data found.Please run data collection first")

    performance_snippets=[
        f'- Post about "{p.get("caption", "N/A")[:80]}..." got {p.get("likes_count", 0)} likes.'
        for p in channel_data["posts"][:10]
    ]
    performance_text ="\n".join(performance_snippets)

    prompt = f"""
    You are an expert Instagram strategist.Analyze the performance of these recent posts:
    {performance_text}

    Based on the posts that got the most likes, what topic or style is working best?
    Generate a new post recommendation (caption, hashtags, justification) that leans into that successful style.

    Respond with ONLY a JSON object in this exact format:
    {{
      "caption": "Your new, creative caption.",
      "hashtags": "#relevant #hashtags #here",
      "justification": "A brief explanation of why this post will work well based on the data."
    }}
    """
    response_str = generate_text(prompt)
    try:
        clean_str=response_str.strip().removeprefix("```json").removesuffix("```")
        data = json.loads(clean_str)
        return RecommendationResponse(**data)
    except (json.JSONDecodeError, TypeError) as e:
        print(f"Error:{e}")
        raise HTTPException(status_code=500,detail="The AI returned an invalid recommendation format")

@app.post("/generate-thumbnail")
def create_thumbnail(request:ThumbnailRequest):
    if not request.caption:
        raise HTTPException(status_code=400,detail="Caption is required to generate the thumbnail")
    output_file_path=generate_image(prompt=request.caption)
    if not output_file_path:
        raise HTTPException(status_code=500,detail="The AI image model failed to generate the thumbnail")
    file_url=f"/outputs/{os.path.basename(output_file_path)}"
    return {"message":"Thumbnail generated successfully","image_url": file_url}