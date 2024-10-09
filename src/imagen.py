import os

import vertexai
from dotenv import load_dotenv
from vertexai.preview.vision_models import ImageGenerationModel

PROJECT_ID = "edit-ai-prod"

load_dotenv()

os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def get_imagen_images(prompt):
    vertexai.init(project=PROJECT_ID, location="us-central1")

    print("Init success")

    model = ImageGenerationModel.from_pretrained("imagen-3.0-generate-001")

    print("Model loaded")

    print("Prompt: ", prompt)

    images = model.generate_images(
        prompt=prompt,
        # Optional parameters
        number_of_images=4,
        language="en",
        # You can't use a seed value and watermark at the same time.
        # add_watermark=False,
        # seed=100,
        aspect_ratio="1:1",
        safety_filter_level="block_some",
        person_generation="allow_adult",
    )

    print("Images generated")

    images[0].save(location="output_file_1.png",
                   include_generation_parameters=False)
    images[1].save(location="output_file_2.png",
                   include_generation_parameters=False)
    images[2].save(location="output_file_3.png",
                   include_generation_parameters=False)
    images[3].save(location="output_file_4.png",
                   include_generation_parameters=False)

    # Optional. View the generated image in a notebook.
    # images[0].show()

    print(f"Created output image using {len(images[0]._image_bytes)} bytes")
    print(f"Created output image using {len(images[1]._image_bytes)} bytes")
    print(f"Created output image using {len(images[2]._image_bytes)} bytes")
    print(f"Created output image using {len(images[3]._image_bytes)} bytes")
