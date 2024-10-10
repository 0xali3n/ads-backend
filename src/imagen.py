import os

import vertexai
from dotenv import load_dotenv
from vertexai.preview.vision_models import ImageGenerationModel

PROJECT_ID = "edit-ai-prod"

load_dotenv()

os.getenv("GOOGLE_APPLICATION_CREDENTIALS")


def get_imagen_images(prompt, number=4):
    try:

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
        print("Images: ", images)

        images[0].save(location="output_file_festival_hfddsoli_1.png",
                       include_generation_parameters=False)
        images[1].save(location="output_file_festival_hodsvsli_2.png",
                       include_generation_parameters=False)
        images[2].save(location="output_file_festival_hozfzli_3.png",
                       include_generation_parameters=False)
        images[3].save(location="output_file_festival_hofsdli__4.png",
                       include_generation_parameters=False)

        # Optional. View the generated image in a notebook.
        # images[0].show()
        s3_imgs = []
        for image in images:
            # save the image in s3
            s3_imgs.append(image._image_bytes)

        # print(
        #     f"Created output image using {len(images[0]._image_bytes)} bytes")
        # print(
        #     f"Created output image using {len(images[1]._image_bytes)} bytes")
        # print(
        #     f"Created output image using {len(images[2]._image_bytes)} bytes")
        # print(
        #     f"Created output image using {len(images[3]._image_bytes)} bytes")
        return {"success": True, "code": 200, "message": "Images generated", "images": s3_imgs}
    except Exception as e:
        print(f"Error: {e}")
        return {"success": True, "code": 200, "message": "Images generated"}
