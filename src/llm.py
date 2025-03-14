from groq import Groq
from src.circular_logger import logger, setup_logging

class LLM:
    def __init__(self, api_key: str):
        self.groq = Groq(api_key=api_key)
        setup_logging()

    def generate_response(self, prompt: str, context: str) -> str:
        logger.info(f"Generating response for prompt: {prompt} with context: {context}")

        response = self.groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant. You are given a prompt and some context. \
                 Use the context to help you answer the prompt. Always respond concisely with only what's important \
                 unless mentioned by the user otherwise."},
                {"role": "user", "content": prompt + ( "\n\nHere is some context that might be relevant to the prompt: " + context ) if context else ""}
            ]
        )
        return response.choices[0].message.content
