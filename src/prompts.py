CAPTION_PROMPT = '''
Analyze the given product image(s) and the provided theme. Generate a detailed, vivid description that incorporates both elements.
Focus on:
1. Main product features and characteristics
2. Colors, textures, and materials
3. Style and design elements
4. Unique selling points or standout features
5. Overall aesthetic and mood conveyed by the image(s)
6. How the product relates to or embodies the given theme
7. Thematic elements present in the image or suggested by the product
Describe the product(s) and theme in a way that captures their combined essence and appeal, using sensory and evocative language.
Aim for a description that is both accurate and compelling, suitable for themed marketing purposes.
Give product description and product name as the result. Product description should include a very strong description, and colors used. Frame the description in such a way that a new image can be generated using a multi-modal model. Include proper names, colors, textures and design without fail.
Output should be in JSON format with following keys:
- product_name
- product_description
- colors_used
'''


def get_imagen_stage_prompt(theme: str, offer: str, product_name: str, product_description: str, color_scheme: str, stage: int, tagline="", user_prompt="", user_target=""):

    if (not theme or theme == ""):
        theme = """Modern Seasonal Celebration' theme. This theme should:
Incorporate abstract, geometric representations of seasonal elements. For example:
Spring: Stylized flowers, fresh leaves, and pastel color accents
Summer: Sun-inspired patterns, wave-like forms, and bright, warm colors
Autumn: Leaf silhouettes, warm earth tones, and subtle harvest imagery
Winter: Snowflake-inspired geometric shapes, cool blues and silvers, and crystalline textures
Use a modern, minimalist approach to seasonal imagery, avoiding cliché or overly literal representations.
Include subtle animated elements like gentle particle effects or smooth color transitions to represent the dynamic nature of the seasons.
Blend the seasonal elements seamlessly with the product, creating a fresh and contemporary look.
Employ a color palette that combines neutral tones with pops of season-appropriate colors.
Incorporate abstract background patterns that suggest movement and change, reflective of the seasonal theme.
This fallback theme should create a visually appealing, versatile backdrop that can complement a wide range of products while still providing a sense of timeliness and celebration"""

    prompt1 = f"""
Create a detailed prompt for an AI image generator to produce a visually striking, theme-oriented product banner for {product_name} brand. The theme is {theme} Incorporate the following elements:
Product and theme description: {product_description}
Enhanced themed offer: {offer}
Color palette: {color_scheme}
Guidelines for the prompt:
Describe the desired layout and composition of the banner, emphasizing how it should prominently feature key symbols and colors associated with the theme (e.g., for Independence Day of India, include the Indian flag, saffron, white, and green colors, and patriotic symbols)
Specify how the product should be portrayed in relation to the theme, integrating it seamlessly with thematic elements
Indicate where and how the themed offer text should appear, possibly incorporating theme-related typography or design elements
Detail how the color palette should be utilized, ensuring it complements the theme's traditional colors
Explain how the theme should dominate the overall design, including specific instructions for incorporating iconic imagery, patterns, or motifs associated with the theme
Suggest additional graphic elements or visual effects that enhance the thematic presentation (e.g., fireworks for Independence Day, traditional patterns, or historical landmarks)
Specify the desired style and mood of the banner, ensuring it aligns with both the product and the celebratory or cultural significance of the theme
Include instructions for incorporating theme-specific symbols, icons, or cultural elements, providing examples relevant to the given theme
If applicable, suggest ways to blend modern and traditional elements to create a contemporary yet culturally relevant design
Craft a comprehensive prompt that will guide the AI image generator to create a cohesive, attractive, and effective product banner that seamlessly integrates the product, offer, and theme. Ensure that the theme is unmistakably represented through visual elements, creating a banner that resonates with the cultural or celebratory context while effectively promoting the product
"""

    target = ""
    user_specs = ""
    tagline = ""

    if (offer != ""):
        tagline = f"""Include a tagline '{offer}' in a complementary font that matches the theme."""

    if (user_target != ""):
        target = f"""
Target Audience Appeal:
Design with {user_target} in mind.
Balance modern design elements with traditional thematic components"""

    if (user_prompt != ""):
        user_specs = f"""
Additional Details:
Incorporate {user_prompt}.
Ensure the overall mood is {theme}.
Create a cohesive, visually appealing banner that effectively promotes the while immersing the viewer in the {theme} celebration.
"""

    prompt2 = f"""{product_description}
Follow these detailed instructions:
Layout and Composition:
1. Position the {product_name} prominently at the center or slightly off-center.
2. Surround the product with thematic elements based on the event in the theme.
3. Ensure a clean, uncluttered design that draws attention to both the product and thematic elements.
Color Scheme:
1. Use a primary color palette of {theme}.
2. Incorporate theme colors harmoniously with the brand palette.
3. Apply subtle gradients and color transitions to add depth and visual interest.
Promotional Offer:
1. Display the offer '{offer}' in large, bold typography.
2. Position the offer at the [specific location, e.g., 'top-right corner'] in a visually striking manner.
3. Create a custom badge or text box for the offer, incorporating theme-related design elements.
Typography and Text:
1. Use a bold, easily readable font for the main offer.
{tagline}

Ensure all text is clearly visible against the background, using contrasting colors if necessary.
Thematic Integration:
1. Incorporate [{theme}, e.g., 'flowing tricolor ribbons, stylized peacock feathers, and Devanagari script accents'].
2. Add subtle patterns or textures inspired by [{theme}, e.g., 'traditional Indian textiles or architectural motifs'].
3. Include small animated elements if possible, such as [e.g., 'gently waving flags or shimmering light effects'].
Lighting and Effects:
1. Apply soft, directional lighting to highlight the product.
2. Use subtle glow effects around key elements to create depth.
3. Add gentle shadows to ground the product and text elements.
Branding:
1. Ensure the logo is clearly visible but doesn't overpower the main elements.
{target}
{user_specs}
"""
    if stage == 1:
        return prompt1
    elif stage == 2:
        return prompt2
