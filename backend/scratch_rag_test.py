import sys
from transformers import pipeline

print("Loading model...")
generator = pipeline("text2text-generation", model="google/flan-t5-large")

context = "Module 5: Soft Computing Techniques. Introduction to Soft Computing, components of soft computing: Fuzzy logic, Neural Networks, Genetic Algorithms. Difference between Soft Computing and Hard Computing. Applications of fuzzy systems and neural networks."
prompt = "What is soft computing? Differentiate between soft computing and hard computing."

prompt_formatted = (
    f"Use the syllabus guidelines below to write a detailed, comprehensive, university-level answer for this question.\n"
    f"Syllabus Guidelines:\n{context}\n\n"
    f"Question: {prompt}\n\n"
    f"Write a detailed response explaining the concepts step-by-step. Include a definition, key features/advantages, and a mock KTU marking scheme."
)

print("Generating...")
result = generator(
    prompt_formatted,
    max_length=512,
    min_length=150,
    do_sample=True,
    top_p=0.92,
    temperature=0.75,
    repetition_penalty=1.2
)
print("\n--- OUTPUT ---")
print(result[0]['generated_text'])
