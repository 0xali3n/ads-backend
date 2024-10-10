# Getting of object detection model
# bouding box
# ##replace products
# ##bouding box for transition image
# Color from each image


from src.banner_color_details import extract_color_palette
from src.embed_image import (draw_bounding_boxes_with_outline,
                             embed_images_within_bboxes)
from src.product_bb import get_bb, product_recog

final_json = [
    {
        "image_id": "user_gen_id",
        "raw_image_path": "",
        "banner_path": "",
        "banner_boudingbox_path": "",
        "top_colors": ""
    }
]
# user_gen_id= user_id + banner_id


def flow(images, product_images, user_gen_id):
    result = []
    for img_url in images:
        obj = {
            "image_id": user_gen_id,
            "raw_image_path": product_images,
            "banner_path": "",
            "banner_boudingbox_path": "",
            "top_colors": ""
        }

        # Product recognition from generated image
        recognized_pdt = product_recog(img_url, user_gen_id)

        # bouding box retrieval of product recognized image
        pdt_bb = get_bb(recognized_pdt, user_gen_id)

        # embedding original product to generated banner
        banner = embed_images_within_bboxes(
            recognized_pdt, product_images, pdt_bb, user_gen_id)
        obj['banner_path'] = banner

        # bouding box transition (adding outline border to showcase transition of object detection)
        bb_box_banner = f"bb_baner_{user_gen_id}"
        draw_bounding_boxes_with_outline(recognized_pdt, pdt_bb, bb_box_banner)
        obj['banner_boudingbox_path'] = bb_box_banner

        # top colors from banner (RGB FORMATED 2D LIST)
        obj['top_colors'], color_percetages = extract_color_palette(
            bb_box_banner)
        result.append(obj)

    return result
