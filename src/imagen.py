import os
from uuid import uuid4

import vertexai
from dotenv import load_dotenv
from src.s3 import S3Operations
from vertexai.preview.vision_models import ImageGenerationModel

PROJECT_ID = "gen-ai-hacs"

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
            number_of_images=number,
            language="en",
            # You can't use a seed value and watermark at the same time.
            # add_watermark=False,
            # seed=100,
            aspect_ratio="1:1",
            safety_filter_level="block_some"
        )

        print("Images generated")
        print("Images: ", images)

        s3Client = S3Operations()
        # Optional. View the generated image in a notebook.
        # images[0].show()
        s3_imgs = []
        for image in images:
            image_id = str(uuid4())
            file_path = f'./tmp/{image_id}.png'
            # create temp folder if doesn't exist
            if not os.path.exists('./tmp'):
                os.makedirs('./tmp')
            # save the image in temp folder
            image.save(file_path)
            url = s3Client.upload_object(
                object_key=f"imagen-images/{image_id}.png", file_path=file_path)
            s3_imgs.append(url)

        # delete the temp folder
        try:
            os.system('rm -rf ./tmp')
        except Exception as e:
            print(f"Error deleting temp folder: {e}")

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
        return {"success": False, "code": 400, "message": "Images not generated"}
