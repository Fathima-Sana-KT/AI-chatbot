from transformers import pipeline

generator = pipeline('text-generation', model='EleutherAI/gpt-neo-2.7B')

def generate_answer(prompt: str) -> str:
    response = generator(prompt, max_length=100, num_return_sequences=1)
    return response[0]['generated_text']
