import os
import json
import requests
from dotenv import load_dotenv

import google.generativeai as genai
import openai


load_dotenv()

try:
    gemini_api_key=os.loadenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found")
    genai.configure(gemini_api_key=gemini_api_key)
    gemini_model=genai.GenerativeModel("gemini-1.5-flash")
except Exception as e:
    gemini_model=None
    print(f"Error initializing gemini AI model:{e}")


try:
    openai_api_key=os.loadenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found")
    openai_client=openai.OpenAI(openai_api_key=openai_api_key)
except Exception as e:
    openai_client = None
    print(f"Error initializing openAI client:{e}")

def generate_text(prompt:str)->str:
    if not gemini_model:
        print("Text generation is not possible rn due to unavailability of gemini model")
    try:
        response=gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred during gemini text generation:{e}")
        return "An error occurred while generating the AI response."

def generate_image(prompt:str,output_path:str="backend/outputs/next_post.png")->str:
    if not openai_client:
        print("Text generation is not possible rn due to unavailability of openai model")
    try:
        image_prompt=(
        f"A vibrant, high-resolution, visually stunning image for an Instagram post about '{prompt}'. "
        "The style should be modern and engaging. Do not include any text, letters, or watermarks in the image."
        )
        response=openai_client(model="dall-e-3",prompt=image_prompt,n=1,size="1024x1024",quality="standard")
        image_url=response.data[0].url
        image_response=requests.get(image_url,timeout=60)
        image_response.raise_for_status()
        os.makedirs(os.path.dirname(output_path),exist_ok=True)
        with open(output_path,"wb") as f:
            f.write(image_response.content)
        return output_path
    except Exception as e:
        print(f"An error occurred during DALL-E image generation:{e}")
        return None

            

