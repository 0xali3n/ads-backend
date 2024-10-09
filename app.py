from flask import Flask, jsonify, request
from src.gemini_utils import get_gemini_response
from src.imagen import get_imagen_images
from src.prompts import CAPTION_PROMPT, get_imagen_stage_prompt

app = Flask(__name__)


@app.route('/')
def home():
    return jsonify({'message': 'Welcome to my API!'})


@app.route(
    '/prompt',
    methods=['POST']
)
def initial_prompt():
    data = request.get_json()
    image_path = data.get('image_path')

    if not image_path:
        return jsonify({'error': 'Image path is required'}), 400

    prompt = CAPTION_PROMPT

    response = get_gemini_response(prompt, image_path, is_initial_prompt=True)

    print("Recieved initial prompt response")

    product_name = response.get('product_name')
    product_description = response.get('product_description')
    colors_used = response.get('colors_used')

    stage_1_prompt = get_imagen_stage_prompt(
        color_scheme=colors_used,
        offer="15% off",
        product_name=product_name,
        product_description=product_description,
        theme="Independence Day of India",
        stage=1
    )

    response2 = get_gemini_response(stage_1_prompt)

    prompt3 = get_imagen_stage_prompt(
        color_scheme=colors_used,
        offer="15% off",
        product_name=product_name,
        product_description=response2,
        theme="Independence Day of India",
        stage=2,
        user_target="families",
        user_prompt="a playful, vibrant design",
    )

    print("Got final prompt")

    # response3 = get_gemini_response(prompt3)

    get_imagen_images(prompt3)

    return jsonify({'message': 'Initial prompt received', 'image_path': image_path, 'response': response, 'response2': response2, 'final_prompt': prompt3})

    # return jsonify({'message': 'Image path received', 'image_path': image_path, 'response': response})


if __name__ == '__main__':
    app.run(debug=True)
