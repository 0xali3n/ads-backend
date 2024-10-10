import cv2
import numpy as np
from PIL import Image

def embed_images_within_bboxes(base_image_path, embedding_image_paths, bboxes,user_gen_id):
    # Load base image
    base_image = cv2.imread(base_image_path)

    # Determine the minimum number of pairs to process
    num_pairs = min(len(embedding_image_paths), len(bboxes))

    # Iterate over the valid number of embedding images and bounding boxes
    for i in range(num_pairs):
        embedding_image_path = embedding_image_paths[i]
        bbox = bboxes[i]

        # Load the embedding image
        embedding_image = Image.open(embedding_image_path)

        # Bounding box coordinates (x, y, width, height)
        x, y, bbox_width, bbox_height = bbox

        # Check if the bounding box is wider than it is tall
        if bbox_width > bbox_height and embedding_image.height > embedding_image.width:
            # Rotate the embedding image if needed (make it landscape)
            embedding_image = embedding_image.rotate(90, expand=True)

        # Get dimensions of the embedding image
        img_width, img_height = embedding_image.size

        # Calculate scale factor to fit the image within the bounding box while maintaining aspect ratio
        scale_factor = min(bbox_width / img_width, bbox_height / img_height)

        # Resize the embedding image without distorting (keeping aspect ratio)
        new_width = int(img_width * scale_factor)
        new_height = int(img_height * scale_factor)
        resized_embedding_image = embedding_image.resize((new_width, new_height), Image.LANCZOS)

        # Calculate center position for the image to be placed in bounding box
        offset_x = x + (bbox_width - new_width) // 2
        offset_y = y + (bbox_height - new_height) // 2

        # Convert resized image to OpenCV format
        resized_embedding_image_cv = cv2.cvtColor(np.array(resized_embedding_image), cv2.COLOR_RGB2BGR)

        # Overlay the resized image on the base image
        base_image[offset_y:offset_y+new_height, offset_x:offset_x+new_width] = resized_embedding_image_cv

    # Save the final result or display it
    cv2.imwrite('output_image.jpg', base_image)
    # cv2.imshow('Result', base_image)
    final_banner = f'output_image_{user_gen_id}.jpg'
    return final_banner

import cv2

def crop_image_with_bbox(image_path, bbox, output_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image at {image_path}. Check the file path.")
        return
    
    # Bounding box coordinates (x, y, width, height)
    x, y, bbox_width, bbox_height = bbox

    # Crop the image using the bounding box coordinates
    cropped_image = image[y:y+bbox_height, x:x+bbox_width]

    # Save or display the cropped image
    cv2.imwrite(output_path, cropped_image)
    print(f"Cropped image saved as {output_path}.")


# bbox = (100, 50, 200, 150)  # (x, y, width, height)
# crop_image_with_bbox('base_image.jpg', 
#                      bbox, 
#                      'cropped_output.jpg')


import cv2

def draw_bounding_boxes_with_outline(image_path, bboxes, output_path):
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Error: Unable to load image at {image_path}. Check the file path.")
        return

    # Define a set of colors for each product (RGB)
    colors = [
        (0, 255, 0),    # Green
        (0, 0, 255),    # Red
        (255, 0, 0),    # Blue
        (0, 255, 255),  # Yellow
        (255, 0, 255),  # Magenta
        (255, 255, 0),  # Cyan
        (255, 255, 255) # White
    ]
    
    # Iterate over bounding boxes
    for i, bbox in enumerate(bboxes):
        x, y, bbox_width, bbox_height = bbox

        # Select a color based on the index (cycling through the color list)
        color = colors[i % len(colors)]
        
        # Draw a rectangle outline (border) around the bounding box
        cv2.rectangle(image, (x, y), (x + bbox_width, y + bbox_height), color, thickness=3)

    # Save or display the image with the outlines
    cv2.imwrite(output_path, image)
    print(f"Image with bounding boxes saved as {output_path}.")
    return output_path

# Example usage
bboxes = [
    (100, 50, 200, 150),   # Bounding box 1 (x, y, width, height)
    (300, 200, 100, 150),  # Bounding box 2
    (500, 100, 150, 200),  # Bounding box 3
    # Add more bounding boxes as needed
]

# draw_bounding_boxes_with_outline('output_file_1.png', 
#                                  bboxes, 
#                                  'output_file.png')
