import sys
from transformers import pipeline

print("Loading model...")
generator = pipeline("text2text-generation", model="google/flan-t5-large")

prompt = "What is soft computing? Differentiate between soft computing and hard computing."
prompt_formatted = (
    f"Write a detailed, comprehensive, university-level exam answer explaining: {prompt}\n\n"
    f"Include definition, step-by-step features, and a mock KTU marking scheme."
)

print("Generating...")
result = generator(
    prompt_formatted,
    max_length=512,
    min_length=120,
    do_sample=True,
    top_p=0.95,
    temperature=0.8,
    repetition_penalty=1.2
)
print("\n--- OUTPUT ---")
print(result[0]['generated_text'])
