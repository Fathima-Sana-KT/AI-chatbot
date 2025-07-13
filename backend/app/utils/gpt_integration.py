from transformers import pipeline

# Initialize only once
generator = pipeline("text2text-generation", model="google/flan-t5-large")  # or flan-t5-base

def huggingface_generate_answer(prompt: str) -> str:
    try:
        prompt_formatted = f"Answer the following technical question:\n{prompt}"
        result = generator(prompt_formatted, max_length=256, do_sample=False, top_p=0.95, temperature=0.7)

        raw_answer = result[0]['generated_text'].strip()
        if not raw_answer or len(raw_answer) < 10:
            return "⚠️ AI generation failed. Please try again."
        return raw_answer

    except Exception as e:
        print(f"❌ HuggingFace generation error: {e}")
        return "⚠️ AI generation failed. Please try again."
