from openai import OpenAI
import os
from dotenv import load_dotenv
from pydantic import Field
import base64
from io import BytesIO
from PIL import Image

load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
openai = OpenAI()

def generate_image(
    destination: str = Field(
        ..., description = "The city which the image of will be generated"
    )
):

    prompt = f"""
    Create a highly detailed and artistic digital painting of the city of {destination}. 
    The artwork should capture the essence of the city's unique architecture, atmosphere, and culture. 
    Include iconic landmarks, vibrant street life, and a dynamic skyline. 
    Use a blend of warm and cool tones to evoke a sense of depth and realism while maintaining an artistic flair. 
    The image should feel immersive, with intricate details in buildings, people, 
    and lighting effects that reflect the time of day—whether it's a golden sunset, a neon-lit night, or a bright morning. 
    The style should be a mix of realism and impressionism, with expressive brushstrokes adding movement and emotion to the scene.
    """
    
    try:
        response = openai.images.generate(
            model="dall-e-3",
            prompt=prompt,
            size="1024x1024",
            response_format="b64_json"
        )
        image_base64 = response.data[0].b64_json
        image_data = base64.b64decode(image_base64)
        image = Image.open(BytesIO(image_data))
        image.save(f"{destination}.jpg")
        
    except openai.OpenAIError as e:
        print(e.http_status)
        print(e.error)