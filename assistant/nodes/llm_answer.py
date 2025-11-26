# assistant/nodes/llm_answer.py
import google.generativeai as genai

model = genai.GenerativeModel("gemini-2.5-flash")

def llm_answer(state):
    res = model.generate_content(state["prompt"])
    return {"answer": res.text}
