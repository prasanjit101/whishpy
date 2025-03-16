from groq import Groq
import openai
from src.circular_logger import logger, setup_logging

class LLM:
    def __init__(self, api_key: str, provider: str = "groq"):
        if provider == "groq":
            self.provider = "groq"
            self.groq = Groq(api_key=api_key)
        elif provider == "openai":
            self.provider = "openai"
            self.openai = openai.OpenAI(api_key=api_key)
        else:
            raise ValueError("Invalid provider. Must be 'groq' or 'openai'.")
        setup_logging()

    def generate_response(self, prompt: str, context: str) -> str:
        logger.info(f"Generating response for prompt: {prompt} with context: {context} using provider: {self.provider}")

        if self.provider == "groq":
            response = self.groq.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. You are given a prompt and some context. \
                     Use the context to help you answer the prompt. Always respond concisely with only what's important \
                     unless mentioned by the user otherwise."},
                    {"role": "user", "content": prompt +  ("\n\nHere is some context that might be relevant to the prompt: " + context  if context else "")}
                ]
            )
            return response.choices[0].message.content
        elif self.provider == "openai":
            response = self.openai.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant. You are given a prompt and some context. \
                     Use the context to help you answer the prompt. Always respond concisely with only what's important \
                     unless mentioned by the user otherwise."},
                    {"role": "user", "content": prompt +  ("\n\nHere is some context that might be relevant to the prompt: " + context  if context else "")}
                ]
            )
            return response.choices[0].message.content
        else:
            raise ValueError("Invalid provider. Must be 'groq' or 'openai'.")
