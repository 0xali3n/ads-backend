from flask import Flask, jsonify, request
from flask_cors import CORS
from src.flow_after_imagegen import flow
from src.gemini_utils import gemini_for_chatbot, get_gemini_response
from src.imagen import get_imagen_images
from src.prompts import CAPTION_PROMPT, get_imagen_stage_prompt

app = Flask(__name__)
CORS(app) 


@app.route('/')
def home():
    return jsonify({'message': 'Welcome to my API!'})


@app.route(
    '/prompt',
    methods=['POST']
)
def initial_prompt():
    data = request.get_json()
    print(data)
    image_paths = data.get(
        'images', ["/home/sohamr/projects/genai-hack/final/gen-ai-hacks-backend/imgs/amul.jpeg"])
    colors_used = data.get('colors_pallete', [])
    offer = data.get('offer', "15% off")
    theme = data.get('theme', "Holi")
    # get example image from s3
    # store it at "image_path" if s3 link doesn't work

    print(f"Image paths: {image_paths}")
    print(f"Colors used: {colors_used}")
    print(f"Offer: {offer}")
    print(f"Theme: {theme}")
    print("____________-----------------______________")

    if not image_paths:
        return jsonify({'error': 'Image path is required'}), 400

    prompt = CAPTION_PROMPT

    response = get_gemini_response(prompt, image_paths, is_initial_prompt=True)

    print("Recieved initial prompt response")

    product_name = response.get('product_name')
    product_description = response.get('product_description')
    colors_used = response.get('colors_used')

    stage_1_prompt = get_imagen_stage_prompt(
        color_scheme=colors_used,  # from request body.colors_pallete + colors_used
        offer=offer,  # from request body
        theme=theme,  # from request body
        product_name=product_name,
        product_description=product_description,
        stage=1
    )

    response2 = get_gemini_response(stage_1_prompt, images=[])

    prompt3 = get_imagen_stage_prompt(
        color_scheme=colors_used,
        product_name=product_name,
        product_description=response2,
        offer=offer,
        theme=theme,
        user_target="families",
        user_prompt="a playful, vibrant design",
        stage=2,
    )

    print("Got final prompt")
    print("thos is the prompt3",prompt3)
    
    try:
        resp = get_imagen_images(prompt3)
        if resp.get('success'):
            images = resp.get('images', [])
        else:
            return jsonify({
                'error': 'Failed to generate images',
                'message': resp.get('message', 'Unknown error')
            }), 500
    except Exception as e:
        print(f"Error generating images: {e}")
        return jsonify({
            'error': 'Failed to generate images',
            'message': str(e)
        }), 500

    # to be called for final json array of all generated images flow(images,product_images,user_gen_id) (generated_imgs_urls,product_images,user_gen_id)

    return jsonify({
        'message': 'Initial prompt received', 
        'response': response, 
        'response2': response2, 
        'final_prompt': prompt3, 
        'images': images
    })

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
        images = get_imagen_images(response, 2)
        print("Images: ", images)
        return jsonify({
            'message': 'Chatbot response received',
            'response': response,
            'image': images["images"][0]
        })
    else:
        return jsonify({
            'message': 'Chatbot response received',
            'response': response
        })


if __name__ == '__main__':
    app.run(debug=True)
