import base64
import openai
from typing import List, Union

class OpenAIVision:
    def __init__(self, api_key: str, model: str = "gpt-4-vision-preview"):
        self.client = openai.OpenAI(api_key=api_key)
        self.model = model

    def encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def analyze_image(self, image_contents: List[Union[str, dict]], max_tokens: int = 300, detail: str = "auto") -> str:
        messages = [{
            "role": "user",
            "content": image_contents
        }]
        
        # Adjusting image detail if specified
        for content in image_contents:
            if "type" in content and content["type"] == "image_url" and "image_url" in content:
                content["image_url"]["detail"] = detail

        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content

# # Example Usage
# api_key = "your_openai_api_key"
# vision_api = OpenAIVision(api_key)

# # Analyzing a single image by URL
# # image_url = {
# #     "type": "image_url",
# #     "image_url": {
# #         "url": "https://example.com/image.jpg"
# #     }
# # }
# # print(vision_api.analyze_image([image_url]))

# # Analyzing a local image (base64 encoded)
# image_path = "C:/Users/Erick/Pictures/Camera Roll/bd4.jpg"
# base64_image = vision_api.encode_image(image_path)
# base64_image_content = {
#     "type": "image_url",
#     "image_url": {
#         "url": f"data:image/jpeg;base64,{base64_image}"
#     }
# }
# print(vision_api.analyze_image([base64_image_content]))


