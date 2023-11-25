import openai

class OpenAITextGenerator:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)

    def chat_completion(self, model: str, messages: list, max_tokens: int = 300, seed: int = None, response_format: dict = None):
        response = self.client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            seed=seed,
            response_format=response_format
        )
        return response.choices[0].message.content

    def legacy_completion(self, model: str, prompt: str, max_tokens: int = 300, logprobs: int = None):
        response = self.client.completions.create(
            model=model,
            prompt=prompt,
            max_tokens=max_tokens,
            logprobs=logprobs
        )
        return response.choices[0].text

# # Example Usage
# api_key = "your_openai_api_key"
# text_generator = OpenAITextGenerator(api_key)

# # Using Chat Completions API
# chat_messages = [
#     {"role": "system", "content": "You are a helpful assistant."},
#     {"role": "user", "content": "Who won the world series in 2020?"}
# ]
# print(text_generator.chat_completion("gpt-3.5-turbo", chat_messages))

# # Using Legacy Completions API
# prompt = "Write a tagline for an ice cream shop."
# print(text_generator.legacy_completion("gpt-3.5-turbo-instruct", prompt))
