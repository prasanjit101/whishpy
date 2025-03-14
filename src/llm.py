from groq import Groq

class LLM:
    def __init__(self, api_key: str):
        self.groq = Groq(api_key=api_key)

    def generate_response(self, prompt: str) -> str:
        response = self.groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that can answer questions and help with tasks like writing emails, notes, and more."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    
    def generate_response_with_stream(self, prompt: str):
        response = self.groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that can answer questions and help with tasks like writing emails, notes, and more."},
                {"role": "user", "content": prompt}
                ],
            stream=True
        )
        for chunk in response:
            yield chunk.choices[0].delta.content
