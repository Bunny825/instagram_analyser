from pydantic import BaseModel

class CollectDataRequest(BaseModel):
    channel_name:str


class SummaryResponse(BaseModel):
    summary:str

class RecommendationResponse(BaseModel):
    caption:str
    hashtags:str
    justification:str

class ThumbnailRequest(BaseModel):
    caption:str



'''
from pydantic import BaseModel

class CollectDataRequest(BaseModel):
    channel_name: str

class SummaryResponse(BaseModel):
    summary: str

class RecommendationResponse(BaseModel):
    caption: str
    hashtags: str
    justification: str

class ThumbnailRequest(BaseModel):
    caption: str
'''