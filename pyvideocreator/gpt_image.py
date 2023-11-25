import openai
from io import BytesIO
from PIL import Image
import os
import requests

class OpenAIImageGenerator:
    def __init__(self, api_key=None):
        self.client = openai.OpenAI(api_key=api_key if api_key else os.environ.get('OPENAI_API_KEY'))

    def generate_image(self, prompt, size="1024x1024", quality="standard", n=1, model="dall-e-3"):
        try:
            response = self.client.images.generate(
                model=model,
                prompt=prompt,
                size=size,
                quality=quality,
                n=n
            )
            return response.data[0].url
        except openai.OpenAIError as e:
            return f"Error: {e.http_status}, {e.error}"

    def edit_image(self, image_path, mask_path, prompt, size="1024x1024", n=1, model="dall-e-2"):
        try:
            with open(image_path, "rb") as image, open(mask_path, "rb") as mask:
                response = self.client.images.edit(
                    model=model,
                    image=image,
                    mask=mask,
                    prompt=prompt,
                    n=n,
                    size=size
                )
            return response.data[0].url
        except openai.OpenAIError as e:
            return f"Error: {e.http_status}, {e.error}"

    def create_image_variation(self, image_data, n=1, size="1024x1024", model="dall-e-2"):
        try:
            if isinstance(image_data, str):
                with open(image_data, "rb") as image:
                    byte_array = image.read()
            elif isinstance(image_data, BytesIO):
                byte_array = image_data.getvalue()
            else:
                raise ValueError("Unsupported image data type")

            response = self.client.images.create_variation(
                image=byte_array,
                n=n,
                model=model,
                size=size
            )
            return response.data[0].url
        except openai.OpenAIError as e:
            return f"Error: {e.http_status}, {e.error}"

    def resize_image(self, image_path, width, height, output_format='PNG'):
        image = Image.open(image_path)
        resized_image = image.resize((width, height))
        byte_stream = BytesIO()
        resized_image.save(byte_stream, format=output_format)
        return byte_stream
    
    def download_image(self, url, save_path):
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raises HTTPError for bad requests
    
            with open(save_path, 'wb') as f:
                f.write(response.content)
    
            return f"Image downloaded successfully: {save_path}"
        except requests.exceptions.HTTPError as e:
            return f"HTTP Error: {e}"
        except requests.exceptions.RequestException as e:
            return f"Error downloading image: {e}"

# # Example usage
# image_generator = OpenAIImageGenerator()
# image_url = image_generator.generate_image("a white terrier dog")
# save_path = "downloaded_terrier_dog.jpg"
# download_status = image_generator.download_image(image_url, save_path)
# print(download_status)
