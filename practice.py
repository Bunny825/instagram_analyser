import os
import requests
from dotenv import load_dotenv
import google.generativeai as genai
import openai

import io
import textwrap
from PIL import Image, ImageDraw, ImageFont

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
        image_prompt = (
            "THIS IS VERY IMPORTANT: IN THE VERTICAL VERSION,MAINTAIN THE BOTTOM 1/3rd OF THE IMAGE AS A BLACK SPACE.THE BOTTOM 1/3rd OF THE IMAGE BUT BE ---BLACK--- .PLEASE MAINTAIN THIS AS I NEED TO ADD THE TEXT AND CAPTIONS THERE."
            "CRITICAL:THIS IS VERY VERY IMPORTANT TO FOLLOW: The final image must be ONLY the scene itself. Absolutely DO NOT include any camera, viewfinder, screen overlays, frame lines, text, or logos."
            # 1. The Narrative Core
            f"Create a single, captivating frame from a film that tells a story about '{prompt}'. "
            "The image must feel like a candid, fleeting moment, not a posed photograph. "

            # 2. Cinematographic & Technical Specification
            "Visually, this must be indistinguishable from a frame shot on an proffesional camera. "
            "The aperture should be realistic for a shallow depth of field. The image must have a subtle, organic look. "

            # 3. The Human Element & Emotion
            "If a person is the subject, their presence must be profoundly human. Capture a micro-expression. "
            "Skin texture must be hyper-realistic, showing pores and natural light reflection. "

            # 4. Artistic Direction: Lighting, Color, and COMPOSITION
            "Lighting must be natural and motivated. The color grade should be deep and cinematic. "
            "Composition follows the rule of thirds, with the main subject placed in the upper part of the frame. "
            "The bottom third of the image must be intentionally left as clean, minimalist negative space (copy space) for text. "

            # 5. Absolute Mandates (Negative Prompts)
            "Under no circumstances should this look like digital art, a 3D render, or CGI. "
            # CHANGE: Added specific instruction to avoid film borders.
            "AVOID film strip borders, sprocket holes, film mattes, text, and logos."
            "CRITICAL: The final image must be ONLY the scene itself. Absolutely DO NOT include any camera, viewfinder, screen overlays, frame lines, text, or logos."
        )

        response=openai_client.images.generate(
            model="dall-e-3",
            prompt=image_prompt,
            size="1024x1792",
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