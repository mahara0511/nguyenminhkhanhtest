# assistant/nodes/build_prompt.py

def build_prompt(state):
    context = "\n---\n".join(state["retrieved_chunks"])

    prompt = f"""
You are OptiBot, the customer-support bot for OptiSigns.com.
Only answer using the provided documents.
Max 5 bullet points; else link to the doc.
Cite up to 3 article URLs from metadata.

=== DOCUMENTS ===
{context}

=== QUESTION ===
{state["query"]}
"""

    return {"prompt": prompt}
