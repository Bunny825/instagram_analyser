import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai
import openai

load_dotenv()

try:
    gemini_api_key=os.getenv("GEMINI_API_KEY")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY not found")
    genai.configure(api_key=gemini_api_key)
    gemini_model=genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    gemini_model=None
    print(f"Error initializing gemini AI model:{e}")

try:
    openai_api_key=os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found")
    openai_client=openai.OpenAI(api_key=openai_api_key)
except Exception as e:
    openai_client=None
    print(f"Error initializing OpenAI:{e}")


def generate_text(prompt:str)->str:
    if not gemini_model:
        return "AI text generation is currently unavailable"
    try:
        response=gemini_model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"An error occurred during Gemini text generation: {e}")
        return "An error occurred while generating the AI response."

def generate_image(prompt:str,output_path:str="backend/outputs/next_post.png")->str|None:
    if not openai_client:
        return "AI image generation is currently unavailable"
    try:
        image_prompt=(
            f"A vibrant, high-resolution, visually stunning image for an Instagram post about '{prompt}'. "
            "The style should be modern and engaging. Do not include any text, letters, or watermarks in the image."
        )
        response=openai_client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
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