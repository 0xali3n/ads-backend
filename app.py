from flask import Flask, jsonify, request
from src.gemini_utils import gemini_for_chatbot, get_gemini_response
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

    # get example image from s3
    # store it at "image_path" if s3 link doesn't work

    if not image_path:
        return jsonify({'error': 'Image path is required'}), 400

    prompt = CAPTION_PROMPT

    response = get_gemini_response(prompt, image_path, is_initial_prompt=True)

    print("Recieved initial prompt response")

    product_name = response.get('product_name')
    product_description = response.get('product_description')
    colors_used = response.get('colors_used')

    stage_1_prompt = get_imagen_stage_prompt(
        color_scheme=colors_used,  # from request body.colors_pallete + colors_used
        offer="15% off",  # from request body
        theme="Holi",  # from request body
        product_name=product_name,
        product_description=product_description,
        stage=1
    )

    response2 = get_gemini_response(stage_1_prompt)

    prompt3 = get_imagen_stage_prompt(
        color_scheme=colors_used,
        product_name=product_name,
        product_description=response2,
        offer="15% off",
        theme="Holi",
        user_target="families",
        user_prompt="a playful, vibrant design",
        stage=2,
    )

    print("Got final prompt")

    # response3 = get_gemini_response(prompt3)

    get_imagen_images(prompt3)

    return jsonify({'message': 'Initial prompt received', 'image_path': image_path, 'response': response, 'response2': response2, 'final_prompt': prompt3})

    # return jsonify({'message': 'Image path received', 'image_path': image_path, 'response': response})


@app.route(
    '/chat-bot',
    methods=['POST']
)
def get_completions():
    data = request.get_json()
    prompt = data.get('prompt', "")
    history = data.get('history', [])
    is_image = data.get('is_image', False)

    response = gemini_for_chatbot(prompt, history, is_image)

    if is_image:
        images = get_imagen_images(response, 1)

        return jsonify({
            'message': 'Chatbot response received',
            'response': response,
            'image': images[0]
        })
    else:
        return jsonify({
            'message': 'Chatbot response received',
            'response': response
        })


if __name__ == '__main__':
    app.run(debug=True)
