from llama_cpp import Llama

LLM_PATH = "models/llm_weights/mistral-7b-instruct-v0.1.Q4_K_M.gguf"
llm = Llama(model_path=LLM_PATH, n_ctx=2048, n_threads=4)

def summarize_report(filepath):
    try:
        with open(filepath, "rb") as f:
            text = f.read().decode("utf-8", errors="ignore")[:2000]
        prompt = f"Summarize this medical report in plain English:\n\n{text}\n\nSummary:"
        result = llm(prompt, max_tokens=300, stop=["\n"])
        return result["choices"][0]["text"].strip()
    except Exception as e:
        return f"⚠️ Error summarizing report: {e}"
