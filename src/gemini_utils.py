import json
import os
from io import BytesIO

import google.generativeai as genai
import PIL.Image
import requests
from dotenv import load_dotenv
from google.ai.generativelanguage_v1beta.types import content

load_dotenv()

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


def get_gemini_response(prompt: str, images: list[str], is_initial_prompt: bool = False):
    generation_config = {
        "temperature": 0.4,
        "top_p": 1,
        "top_k": 32,
        "max_output_tokens": 4096,
        "response_mime_type": "application/json",
    }

    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                  generation_config=generation_config)
    prompt_parts = [prompt]
    for img_path in images:
        if img_path != "":
            print(f"Fetching image from: {img_path}")
            response = requests.get(img_path)
            print(f"Response status code: {response.status_code}")
            print(f"Response content type: {response.headers.get('content-type')}")
            print(f"Response content length: {len(response.content)}")
            try:
                img = PIL.Image.open(BytesIO(response.content))
                prompt_parts.append(img)
            except Exception as e:
                print(f"Error processing image: {e}")
                print(f"Response content: {response.content[:100]}")  # Print first 100 bytes
                raise
    # else:
    #     prompt_parts = [
    #         f"""{prompt}"""
    #     ]

    response = model.generate_content(prompt_parts)

    print(response.text)

    if is_initial_prompt:
        try:
            response_json = json.loads(response.text)
            return {
                "product_name": response_json.get("product_name", ""),
                "product_description": response_json.get("product_description", ""),
                "colors_used": response_json.get("colors_used", [])
            }
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            return {
                "product_name": "",
                "product_description": "",
                "colors_used": []
            }
    else:
        return response.text


def gemini_for_chatbot(current_prompt: str, history: list[str] = [], require_image: bool = False):

    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    model = genai.GenerativeModel(model_name="gemini-1.5-flash",
                                  generation_config=generation_config)
    prompt_parts = ""
    if require_image:
        prompt_parts = f"""Generate an image which is clearly related to the following description: {current_prompt}"""
    else:
        prompt_parts = f"""{current_prompt}"""

    chat_session = model.start_chat(
        history=[],
    )

    response = chat_session.send_message(prompt_parts)

    return response.text
